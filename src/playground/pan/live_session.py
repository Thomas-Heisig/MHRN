"""Stateful PAN live-session runtime for the isolated Playground.

This module intentionally stays outside the canonical research runtime. It keeps
neuron/synapse state across API calls so PAN can be driven interactively.
"""

from __future__ import annotations

import hashlib
import random
import threading
import uuid
from collections import deque
from collections.abc import Mapping, Sequence

from ..models import PlaygroundConfig
from ..registry.neuron_models import get_neuron_model
from ..registry.topology_generators import build_topology
from .behavioral_learning import BehavioralLearningEngine
from .growth_engine import GrowthEngine
from .mode_switcher import ModeSwitcher
from .runtime import PANRuntime
from .thalamic_gating import ThalamicGating


def _checkpoint_int(value: object, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return int(value)
    return default


def _checkpoint_float(value: object, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    return default


class PANLiveSession:
    """Persistent, bounded PAN reference session."""

    def __init__(self, config: PlaygroundConfig) -> None:
        if config.target_cue_control != "aligned":
            raise ValueError(
                "input-cue interventions currently apply to Builder runs, not live sessions"
            )
        if config.neuron_backend != "cpu":
            raise ValueError(
                "CUDA membrane selection currently applies to Builder runs; live sessions require cpu"
            )
        if config.neuron_model != "pan_adex_5d":
            raise ValueError("PAN live session currently requires pan_adex_5d")
        self.config = config
        self.model = get_neuron_model("pan_adex_5d")
        self.topology = build_topology(
            config.topology,
            config.n_neurons,
            config.edge_budget,
            config.seed,
            dimensions=config.dimensions,
            radius=config.radius,
            k_neighbors=config.k_neighbors,
            rewiring_probability=config.rewiring_probability,
            modules=config.modules,
            geometry_lambda_a=config.geometry_lambda_a,
            geometry_lambda_b=config.geometry_lambda_b,
            geometry_sigma=config.geometry_sigma,
            geometry_p0=config.geometry_p0,
            geometry_mode=config.geometry_mode,
        )
        self.states = [
            self.model.state_factory(self.model.parameters)
            for _ in range(config.n_neurons)
        ]
        self.adjacency: list[set[int]] = [set() for _ in range(config.n_neurons)]
        self.incoming: list[set[int]] = [set() for _ in range(config.n_neurons)]
        self.weights: dict[tuple[int, int], float] = {}
        self.delays: dict[tuple[int, int], int] = {}
        self.eligibility: dict[tuple[int, int], float] = {}
        self.release_state: dict[tuple[int, int], float] = {}
        for source, target in self.topology.edges:
            self.adjacency[source].add(target)
            self.incoming[target].add(source)
            edge = (source, target)
            self.weights[edge] = config.weight
            self.delays[edge] = max(1, config.delay_ticks)
            self.eligibility[edge] = 0.0
            self.release_state[edge] = 1.0

        degree = [
            len(self.adjacency[index]) + len(self.incoming[index])
            for index in range(config.n_neurons)
        ]
        self.pan_runtime = PANRuntime(
            n_neurons=config.n_neurons,
            dimensions=config.pan_dimensions,
            seed=config.seed,
            feedback_gain=config.pan_feedback_gain,
            health_decay=config.pan_health_decay,
            apoptosis_threshold=config.pan_apoptosis_threshold,
            closed_loop=config.pan_closed_loop,
            coordinates=self.topology.coordinates,
            degree=degree,
        )
        self.pan_runtime.initialize(self.states)
        growth_edge_capacity = min(
            config.n_neurons * (config.n_neurons - 1),
            config.edge_budget
            + max(64, config.growth_max_new_synapses_per_barrier * 16),
        )
        self.growth = (
            GrowthEngine(
                n_neurons=config.n_neurons,
                edge_budget=growth_edge_capacity,
                max_synapses_per_neuron=config.growth_max_synapses_per_neuron,
                max_new_synapses_per_barrier=(
                    config.growth_max_new_synapses_per_barrier
                ),
                activity_threshold=config.growth_activity_threshold,
                coactivation_threshold=config.growth_coactivation_threshold,
                information_threshold=config.growth_information_threshold,
                prune_threshold=config.growth_prune_threshold,
                neurogenesis=config.growth_neurogenesis,
                synaptogenesis=config.growth_synaptogenesis,
                path_formation=config.growth_path_formation,
                pruning=config.growth_pruning,
            )
            if config.growth_enabled
            else None
        )
        self.growth_batch_ticks = max(
            1, round(config.clock_event_batch_ms / config.dt_ms)
        )
        self.growth_events: list[dict[str, object]] = []
        self.structural_added = 0
        self.structural_removed = 0

        self.pending = [
            [0.0 for _ in range(config.n_neurons)]
            for _ in range(max(65, config.delay_ticks + 2))
        ]
        self.tick = 0
        self.rng = random.Random(config.seed ^ 0x71AE)
        self.input_queue: deque[tuple[list[float], int]] = deque()
        self.last_input_currents = [0.0 for _ in range(config.n_neurons)]
        self.recent_spikes: deque[tuple[int, int]] = deque(maxlen=8192)
        self.output_counts = [0 for _ in range(config.behavior_action_count)]
        self.total_spikes = 0
        self.thalamic = (
            ThalamicGating(
                n_neurons=config.n_neurons,
                relay_threshold=config.thalamic_relay_threshold,
                attention_gain=config.thalamic_attention_gain,
                inhibition_gain=config.thalamic_inhibition_gain,
            )
            if config.thalamic_gating_enabled
            else None
        )
        self.learning_enabled = config.behavior_learning_enabled
        self.auto_reward_enabled = True
        self.learning = BehavioralLearningEngine(
            n_neurons=config.n_neurons,
            action_count=config.behavior_action_count,
            learning_rate=config.behavior_learning_rate,
            epsilon=config.behavior_epsilon,
            target_action=config.behavior_target_action,
            target_mode=config.behavior_target_mode,
            min_activity=config.behavior_min_activity,
            episode_ticks=config.behavior_episode_ticks,
            bias_current=config.behavior_bias_current,
            seed=config.seed,
        )
        self.switcher = ModeSwitcher(
            mode=config.execution_mode,
            initial_mode=config.execution_initial_mode,
            theta_high=config.execution_theta_high,
            theta_low=config.execution_theta_low,
            hysteresis=config.execution_hysteresis,
            min_dwell=config.execution_min_dwell,
            activity_window=config.execution_activity_window,
            transition_mode=config.execution_transition_mode,
            sync_on_switch=config.execution_sync_on_switch,
            log_transitions=config.execution_log_transitions,
            log_state_hash=config.execution_log_state_hash,
        )
        self.last_spikes: list[int] = []
        self.lock = threading.RLock()

    def inject_vector(
        self,
        values: Sequence[float],
        *,
        duration_ticks: int = 16,
        gain: float = 25.0,
    ) -> None:
        if duration_ticks < 1 or duration_ticks > 4096:
            raise ValueError("duration_ticks must be between 1 and 4096")
        vector = [0.0 for _ in range(self.config.n_neurons)]
        if not values:
            return
        for index, value in enumerate(values):
            neuron = index % self.config.n_neurons
            vector[neuron] += max(-1.0, min(1.0, float(value))) * gain
        with self.lock:
            self.input_queue.append((vector, duration_ticks))

    def _input_currents(self) -> list[float]:
        currents = [0.0 for _ in range(self.config.n_neurons)]
        if not self.input_queue:
            return currents
        vector, remaining = self.input_queue[0]
        currents = list(vector)
        remaining -= 1
        self.input_queue.popleft()
        if remaining > 0:
            self.input_queue.appendleft((vector, remaining))
        return currents

    def _decode_action(self, spikes: Sequence[int]) -> int | None:
        if not spikes:
            return None
        counts = [0 for _ in range(self.config.behavior_action_count)]
        for neuron in spikes:
            bucket = min(
                self.config.behavior_action_count - 1,
                neuron * self.config.behavior_action_count // self.config.n_neurons,
            )
            counts[bucket] += 1
        best = max(counts)
        if best <= 0:
            return None
        action = max(range(len(counts)), key=lambda idx: (counts[idx], -idx))
        self.output_counts[action] += 1
        return action

    def choose_strategy(self, context: str, options: int) -> int:
        with self.lock:
            return self.learning.choose_context_action(context, options)

    def apply_strategy_reward(
        self,
        *,
        context: str,
        action: int,
        reward: float,
        action_count: int,
    ) -> dict[str, object]:
        with self.lock:
            value = self.learning.apply_external_reward(
                context=context,
                action=action,
                reward=reward,
                action_count=action_count,
            )
            return {
                "classification": "PLAYGROUND_META_REWARD",
                "scientific_evidence": False,
                "context": context,
                "action": action,
                "reward": float(reward),
                "updated_value": value,
                "learning": self.learning.summary(),
            }

    def step(
        self, ticks: int = 32, *, include_topology: bool = True
    ) -> dict[str, object]:
        if ticks < 1 or ticks > 4096:
            raise ValueError("ticks must be between 1 and 4096")
        chunk_spikes: list[tuple[int, int]] = []
        actions: list[int] = []
        rewards: list[float] = []

        with self.lock:
            for _ in range(ticks):
                next_engine, reason = self.switcher.decide(self.tick)
                if reason is not None and next_engine != self.switcher.current_engine:
                    self.switcher.transition(
                        tick=self.tick,
                        new_engine=next_engine,
                        reason=reason,
                        states=self.states,
                        pending=self.pending,
                    )
                self.switcher.note_tick()

                slot = self.tick % len(self.pending)
                synaptic = self.pending[slot]
                self.pending[slot] = [0.0 for _ in range(self.config.n_neurons)]
                external = self._input_currents()
                self.last_input_currents = list(external)
                external = [value + self.config.pan_bias_current for value in external]
                if self.thalamic is not None:
                    external = self.thalamic.apply(external, self.last_spikes)
                behavior_bias = (
                    self.learning.bias_currents()
                    if self.learning_enabled
                    else [0.0 for _ in range(self.config.n_neurons)]
                )
                feedback = self.pan_runtime.feedback_currents()
                external = [
                    external[index] + behavior_bias[index] + feedback[index]
                    for index in range(self.config.n_neurons)
                ]

                if self.switcher.current_engine == "EVENT_ONLY":
                    active = [
                        index
                        for index in range(self.config.n_neurons)
                        if abs(external[index]) + abs(synaptic[index]) > 1e-12
                    ]
                else:
                    active = list(range(self.config.n_neurons))

                spiked: list[int] = []
                for neuron in active:
                    if not bool(self.states[neuron].get("pan_alive", True)):
                        continue
                    current = external[neuron] + synaptic[neuron]
                    if self.model.step(
                        self.states[neuron],
                        current,
                        self.config.dt_ms,
                        self.model.parameters,
                    ):
                        spiked.append(neuron)
                        self.total_spikes += 1
                        self.recent_spikes.append((self.tick, neuron))
                        chunk_spikes.append((self.tick, neuron))

                for source in spiked:
                    for target in self.adjacency[source]:
                        edge = (source, target)
                        delivery = (self.tick + self.delays[edge]) % len(self.pending)
                        self.pending[delivery][target] += self.weights[edge]

                if self.learning_enabled:
                    self.learning.observe(spiked)
                    if self.auto_reward_enabled:
                        reward = self.learning.maybe_learn(self.tick)
                        if reward is not None:
                            rewards.append(reward)

                self.pan_runtime.update(
                    tick=self.tick,
                    dt_ms=self.config.dt_ms,
                    states=self.states,
                    spiked_neurons=spiked,
                    plasticity_active=self.learning_enabled,
                )
                self.growth_events.extend(
                    {
                        "kind": "SPIKE",
                        "neuron_id": int(neuron_id),
                        "tick": self.tick,
                    }
                    for neuron_id in spiked
                )
                if (
                    self.growth is not None
                    and (self.tick + 1) % self.growth_batch_ticks == 0
                ):
                    added, removed = self.growth.evaluate(
                        tick=self.tick,
                        events=self.growth_events,
                        states=self.states,
                        adjacency=self.adjacency,
                        incoming=self.incoming,
                        weights=self.weights,
                        delays=self.delays,
                        eligibility=self.eligibility,
                        release_state=self.release_state,
                        default_weight=self.config.weight,
                        default_delay_ticks=self.config.delay_ticks,
                    )
                    self.structural_added += added
                    self.structural_removed += removed
                    self.growth_events.clear()
                    self.pan_runtime.degree = [
                        len(self.adjacency[index]) + len(self.incoming[index])
                        for index in range(self.config.n_neurons)
                    ]

                action = self._decode_action(spiked)
                if action is not None:
                    actions.append(action)

                self.switcher.observe(spiked, self.config.n_neurons)
                self.last_spikes = spiked
                self.tick += 1

        return {
            "classification": "PLAYGROUND_LIVE_SESSION",
            "scientific_evidence": False,
            "tick": self.tick,
            "chunk_ticks": ticks,
            "chunk_spikes": len(chunk_spikes),
            "total_spikes": self.total_spikes,
            "alive": self.total_spikes > 0,
            "recent_spikes": [
                {"tick": tick_value, "neuron_id": neuron_id}
                for tick_value, neuron_id in list(self.recent_spikes)[-256:]
            ],
            "mean_v": sum(float(state.get("v", 0.0)) for state in self.states)
            / max(1, len(self.states)),
            "min_v": min(
                (float(state.get("v", 0.0)) for state in self.states),
                default=0.0,
            ),
            "max_v": max(
                (float(state.get("v", 0.0)) for state in self.states),
                default=0.0,
            ),
            "degree_values": [
                len(self.adjacency[index]) + len(self.incoming[index])
                for index in range(self.config.n_neurons)
            ],
            "output_counts": list(self.output_counts),
            "input_active_neurons": sum(
                1 for value in self.last_input_currents if abs(value) > 1e-12
            ),
            "input_peak": max(
                (abs(value) for value in self.last_input_currents), default=0.0
            ),
            "topology": (
                {
                    "neuron_count": self.config.n_neurons,
                    "edge_count": len(self.topology.edges),
                    "dimensions": self.topology.dimensions,
                    "coordinates": self.topology.coordinates,
                    "edges": self.topology.edges,
                }
                if include_topology
                else None
            ),
            "actions": actions[-64:],
            "rewards": rewards[-64:],
            "learning_enabled": self.learning_enabled,
            "learning": self.learning.summary(),
            "execution": self.switcher.summary(),
            "thalamic": self.thalamic.summary() if self.thalamic else None,
            "pan": self.pan_runtime.summary(self.states),
            "growth": self.growth.summary() if self.growth else None,
            "edge_count": len(self.weights),
            "initial_edge_budget": self.config.edge_budget,
            "growth_edge_capacity": (
                self.growth.edge_budget
                if self.growth is not None
                else self.config.edge_budget
            ),
            "structural_added": self.structural_added,
            "structural_removed": self.structural_removed,
            "state_digest": self.state_digest(),
            "input_queue_depth": len(self.input_queue),
        }

    def state_digest(self) -> str:
        payload = ",".join(
            f"{float(state.get('v', 0.0)):.8f}:{float(state.get('w', 0.0)):.8f}"
            for state in self.states
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def export_checkpoint(self) -> dict[str, object]:
        """Export enough mutable state to resume this reference session."""

        with self.lock:
            return {
                "classification": "PLAYGROUND_LIVE_CHECKPOINT",
                "scientific_evidence": False,
                "tick": self.tick,
                "states": [dict(state) for state in self.states],
                "pending": [list(row) for row in self.pending],
                "recent_spikes": [list(item) for item in self.recent_spikes],
                "output_counts": list(self.output_counts),
                "total_spikes": self.total_spikes,
                "last_spikes": list(self.last_spikes),
                "network": {
                    "edges": [
                        {
                            "source": source,
                            "target": target,
                            "weight": self.weights[(source, target)],
                            "delay": self.delays[(source, target)],
                            "eligibility": self.eligibility.get((source, target), 0.0),
                            "release_state": self.release_state.get(
                                (source, target), 1.0
                            ),
                        }
                        for source, target in sorted(self.weights)
                    ],
                    "structural_added": self.structural_added,
                    "structural_removed": self.structural_removed,
                },
                "pan_runtime": {
                    "population_vector": list(self.pan_runtime.population_vector),
                    "feedback_abs_total": self.pan_runtime.feedback_abs_total,
                    "feedback_samples": self.pan_runtime.feedback_samples,
                    "apoptosis_events": list(self.pan_runtime.apoptosis_events),
                },
                "execution": {
                    "current_engine": self.switcher.current_engine,
                    "last_switch_tick": self.switcher.last_switch_tick,
                    "mode_history": list(self.switcher.mode_history),
                    "transitions": list(self.switcher.transitions),
                    "event_ticks": self.switcher.event_ticks,
                    "tick_ticks": self.switcher.tick_ticks,
                    "consistency_failures": self.switcher.consistency_failures,
                    "activity_history": list(self.switcher.monitor.history),
                },
                "growth": (
                    {
                        "activity_ema": list(self.growth.activity_ema),
                        "coactivation": [
                            [source, target, count]
                            for (source, target), count in sorted(
                                self.growth.coactivation.items()
                            )
                        ],
                        "neurogenesis_events": list(self.growth.neurogenesis_events),
                        "synaptogenesis_events": list(
                            self.growth.synaptogenesis_events
                        ),
                        "path_events": list(self.growth.path_events),
                        "pruning_events": list(self.growth.pruning_events),
                        "barriers": self.growth.barriers,
                        "pending_events": list(self.growth_events),
                    }
                    if self.growth is not None
                    else None
                ),
                "learning": {
                    "policy": list(self.learning.policy),
                    "activity": list(self.learning.activity),
                    "action_history": list(self.learning.action_history),
                    "reward_history": list(self.learning.reward_history),
                    "policy_updates": self.learning.policy_updates,
                    "correct_actions": self.learning.correct_actions,
                    "insufficient_activity_episodes": self.learning.insufficient_activity_episodes,
                    "target_history": list(self.learning.target_history),
                    "context_policies": {
                        key: list(value)
                        for key, value in self.learning.context_policies.items()
                    },
                    "context_weights": {
                        key: [list(row) for row in value]
                        for key, value in self.learning.context_weights.items()
                    },
                    "context_updates": dict(self.learning.context_updates),
                    "external_reward_history": list(
                        self.learning.external_reward_history
                    ),
                    "active_context": self.learning.active_context,
                },
            }

    def import_checkpoint(self, payload: Mapping[str, object]) -> None:
        """Restore a checkpoint created by :meth:`export_checkpoint`."""

        with self.lock:
            raw_states = payload.get("states")
            raw_pending = payload.get("pending")
            if not isinstance(raw_states, list) or len(raw_states) != len(self.states):
                raise ValueError("checkpoint state count mismatch")
            if not isinstance(raw_pending, list) or len(raw_pending) != len(
                self.pending
            ):
                raise ValueError("checkpoint pending buffer mismatch")
            restored_states: list[dict[str, object]] = []
            for item in raw_states:
                if not isinstance(item, dict):
                    raise ValueError("checkpoint contains invalid neuron state")
                restored_states.append(dict(item))
            restored_pending: list[list[float]] = []
            for row in raw_pending:
                if not isinstance(row, list) or len(row) != self.config.n_neurons:
                    raise ValueError("checkpoint contains invalid pending row")
                restored_pending.append([float(value) for value in row])
            self.states = restored_states
            self.pending = restored_pending
            self.tick = _checkpoint_int(payload.get("tick"), 0)
            self.total_spikes = _checkpoint_int(payload.get("total_spikes"), 0)
            raw_last_spikes = payload.get("last_spikes")
            self.last_spikes = (
                [_checkpoint_int(value) for value in raw_last_spikes]
                if isinstance(raw_last_spikes, list)
                else []
            )
            raw_counts = payload.get("output_counts")
            if isinstance(raw_counts, list):
                self.output_counts = [_checkpoint_int(value) for value in raw_counts]
            raw_recent = payload.get("recent_spikes")
            self.recent_spikes.clear()
            if isinstance(raw_recent, list):
                for item in raw_recent[-8192:]:
                    if isinstance(item, list) and len(item) == 2:
                        self.recent_spikes.append(
                            (_checkpoint_int(item[0]), _checkpoint_int(item[1]))
                        )

            raw_network = payload.get("network")
            if isinstance(raw_network, Mapping):
                raw_edges = raw_network.get("edges")
                if isinstance(raw_edges, list):
                    self.adjacency = [set() for _ in range(self.config.n_neurons)]
                    self.incoming = [set() for _ in range(self.config.n_neurons)]
                    self.weights = {}
                    self.delays = {}
                    self.eligibility = {}
                    self.release_state = {}
                    for item in raw_edges:
                        if not isinstance(item, Mapping):
                            continue
                        source = _checkpoint_int(item.get("source"), -1)
                        target = _checkpoint_int(item.get("target"), -1)
                        if not (
                            0 <= source < self.config.n_neurons
                            and 0 <= target < self.config.n_neurons
                            and source != target
                        ):
                            continue
                        edge = (source, target)
                        self.adjacency[source].add(target)
                        self.incoming[target].add(source)
                        self.weights[edge] = _checkpoint_float(item.get("weight"))
                        self.delays[edge] = max(
                            1, _checkpoint_int(item.get("delay"), 1)
                        )
                        self.eligibility[edge] = _checkpoint_float(
                            item.get("eligibility")
                        )
                        self.release_state[edge] = _checkpoint_float(
                            item.get("release_state"), 1.0
                        )
                self.structural_added = _checkpoint_int(
                    raw_network.get("structural_added"), 0
                )
                self.structural_removed = _checkpoint_int(
                    raw_network.get("structural_removed"), 0
                )

            raw_pan_runtime = payload.get("pan_runtime")
            if isinstance(raw_pan_runtime, Mapping):
                raw_population = raw_pan_runtime.get("population_vector")
                if isinstance(raw_population, list):
                    self.pan_runtime.population_vector = [
                        _checkpoint_float(value) for value in raw_population
                    ][: self.config.pan_dimensions]
                    if (
                        len(self.pan_runtime.population_vector)
                        < self.config.pan_dimensions
                    ):
                        self.pan_runtime.population_vector.extend(
                            [0.0]
                            * (
                                self.config.pan_dimensions
                                - len(self.pan_runtime.population_vector)
                            )
                        )
                self.pan_runtime.feedback_abs_total = _checkpoint_float(
                    raw_pan_runtime.get("feedback_abs_total"), 0.0
                )
                self.pan_runtime.feedback_samples = _checkpoint_int(
                    raw_pan_runtime.get("feedback_samples"), 0
                )
                raw_apoptosis = raw_pan_runtime.get("apoptosis_events")
                if isinstance(raw_apoptosis, list):
                    self.pan_runtime.apoptosis_events = [
                        dict(item) for item in raw_apoptosis if isinstance(item, dict)
                    ]

            raw_execution = payload.get("execution")
            if isinstance(raw_execution, Mapping):
                engine = raw_execution.get("current_engine")
                if engine in {"EVENT_ONLY", "TICK_ONLY"}:
                    self.switcher.current_engine = str(engine)
                self.switcher.last_switch_tick = _checkpoint_int(
                    raw_execution.get("last_switch_tick"), 0
                )
                raw_history = raw_execution.get("mode_history")
                if isinstance(raw_history, list):
                    self.switcher.mode_history = [
                        dict(item) for item in raw_history if isinstance(item, dict)
                    ]
                raw_transitions = raw_execution.get("transitions")
                if isinstance(raw_transitions, list):
                    self.switcher.transitions = [
                        dict(item) for item in raw_transitions if isinstance(item, dict)
                    ]
                self.switcher.event_ticks = _checkpoint_int(
                    raw_execution.get("event_ticks"), 0
                )
                self.switcher.tick_ticks = _checkpoint_int(
                    raw_execution.get("tick_ticks"), 0
                )
                self.switcher.consistency_failures = _checkpoint_int(
                    raw_execution.get("consistency_failures"), 0
                )
                raw_activity_history = raw_execution.get("activity_history")
                if isinstance(raw_activity_history, list):
                    self.switcher.monitor.history.clear()
                    for value in raw_activity_history[-self.switcher.monitor.window :]:
                        self.switcher.monitor.history.append(_checkpoint_float(value))

            raw_growth = payload.get("growth")
            if self.growth is not None and isinstance(raw_growth, Mapping):
                raw_activity_ema = raw_growth.get("activity_ema")
                if (
                    isinstance(raw_activity_ema, list)
                    and len(raw_activity_ema) == self.config.n_neurons
                ):
                    self.growth.activity_ema = [
                        _checkpoint_float(value) for value in raw_activity_ema
                    ]
                self.growth.coactivation.clear()
                raw_coactivation = raw_growth.get("coactivation")
                if isinstance(raw_coactivation, list):
                    for item in raw_coactivation:
                        if isinstance(item, list) and len(item) == 3:
                            source = _checkpoint_int(item[0], -1)
                            target = _checkpoint_int(item[1], -1)
                            count = _checkpoint_int(item[2], 0)
                            if (
                                0 <= source < self.config.n_neurons
                                and 0 <= target < self.config.n_neurons
                                and count > 0
                            ):
                                self.growth.coactivation[(source, target)] = count
                for attr in (
                    "neurogenesis_events",
                    "synaptogenesis_events",
                    "path_events",
                    "pruning_events",
                ):
                    raw_events = raw_growth.get(attr)
                    if isinstance(raw_events, list):
                        setattr(
                            self.growth,
                            attr,
                            [
                                dict(item)
                                for item in raw_events
                                if isinstance(item, dict)
                            ],
                        )
                self.growth.barriers = _checkpoint_int(raw_growth.get("barriers"), 0)
                raw_pending_growth = raw_growth.get("pending_events")
                self.growth_events = (
                    [
                        dict(item)
                        for item in raw_pending_growth
                        if isinstance(item, dict)
                    ]
                    if isinstance(raw_pending_growth, list)
                    else []
                )
                self.pan_runtime.degree = [
                    len(self.adjacency[index]) + len(self.incoming[index])
                    for index in range(self.config.n_neurons)
                ]

            learning = payload.get("learning")
            if isinstance(learning, Mapping):
                raw_policy = learning.get("policy")
                if isinstance(raw_policy, list):
                    self.learning.policy = [
                        _checkpoint_float(value) for value in raw_policy
                    ]
                raw_activity = learning.get("activity")
                if isinstance(raw_activity, list):
                    self.learning.activity = [
                        _checkpoint_float(value) for value in raw_activity
                    ]
                for name in ("action_history", "target_history"):
                    raw = learning.get(name)
                    if isinstance(raw, list):
                        setattr(
                            self.learning,
                            name,
                            [_checkpoint_int(value) for value in raw],
                        )
                raw_rewards = learning.get("reward_history")
                if isinstance(raw_rewards, list):
                    self.learning.reward_history = [
                        _checkpoint_float(value) for value in raw_rewards
                    ]
                self.learning.policy_updates = _checkpoint_int(
                    learning.get("policy_updates"), 0
                )
                self.learning.correct_actions = _checkpoint_int(
                    learning.get("correct_actions"), 0
                )
                self.learning.insufficient_activity_episodes = _checkpoint_int(
                    learning.get("insufficient_activity_episodes"), 0
                )
                raw_context = learning.get("context_policies")
                if isinstance(raw_context, Mapping):
                    self.learning.context_policies = {
                        str(key): [_checkpoint_float(value) for value in values]
                        for key, values in raw_context.items()
                        if isinstance(values, list)
                    }
                raw_weights = learning.get("context_weights")
                if isinstance(raw_weights, Mapping):
                    self.learning.context_weights = {
                        str(key): [
                            [_checkpoint_float(value) for value in row]
                            for row in rows
                            if isinstance(row, list)
                        ]
                        for key, rows in raw_weights.items()
                        if isinstance(rows, list)
                    }
                raw_updates = learning.get("context_updates")
                if isinstance(raw_updates, Mapping):
                    self.learning.context_updates = {
                        str(key): _checkpoint_int(value)
                        for key, value in raw_updates.items()
                    }
                raw_external = learning.get("external_reward_history")
                if isinstance(raw_external, list):
                    self.learning.external_reward_history = [
                        dict(item) for item in raw_external if isinstance(item, dict)
                    ]
                raw_active_context = learning.get("active_context")
                self.learning.active_context = (
                    str(raw_active_context)
                    if isinstance(raw_active_context, str)
                    else None
                )

    def snapshot(self) -> dict[str, object]:
        with self.lock:
            voltages = [float(state.get("v", 0.0)) for state in self.states]
            return {
                "classification": "PLAYGROUND_LIVE_SESSION",
                "scientific_evidence": False,
                "tick": self.tick,
                "total_spikes": self.total_spikes,
                "alive": self.total_spikes > 0,
                "mean_v": sum(voltages) / max(1, len(voltages)),
                "min_v": min(voltages, default=0.0),
                "max_v": max(voltages, default=0.0),
                "topology": {
                    "neuron_count": self.config.n_neurons,
                    "edge_count": len(self.topology.edges),
                    "dimensions": self.topology.dimensions,
                    "coordinates": self.topology.coordinates,
                    "edges": self.topology.edges,
                },
                "recent_spikes": [
                    {"tick": tick, "neuron_id": neuron}
                    for tick, neuron in list(self.recent_spikes)[-256:]
                ],
                "output_counts": list(self.output_counts),
                "input_queue_depth": len(self.input_queue),
                "learning_enabled": self.learning_enabled,
                "auto_reward_enabled": self.auto_reward_enabled,
                "learning": self.learning.summary(),
                "execution": self.switcher.summary(),
                "state_digest": self.state_digest(),
            }


class PANSessionDaemon:
    """In-process manager for persistent live sessions."""

    def __init__(self, max_sessions: int = 8) -> None:
        if max_sessions < 1:
            raise ValueError("max_sessions must be positive")
        self.max_sessions = max_sessions
        self._sessions: dict[str, PANLiveSession] = {}
        self._lock = threading.RLock()

    def create(self, config: PlaygroundConfig) -> str:
        session_id = "PGLIVE-" + uuid.uuid4().hex[:12]
        with self._lock:
            if len(self._sessions) >= self.max_sessions:
                raise RuntimeError("maximum live Playground sessions reached")
            self._sessions[session_id] = PANLiveSession(config)
        return session_id

    def get(self, session_id: str) -> PANLiveSession:
        with self._lock:
            try:
                return self._sessions[session_id]
            except KeyError as exc:
                raise KeyError("unknown live Playground session") from exc

    def stop(self, session_id: str) -> dict[str, object]:
        with self._lock:
            session = self._sessions.pop(session_id, None)
        if session is None:
            raise KeyError("unknown live Playground session")
        final = session.snapshot()
        final["stopped"] = True
        return final

    def stop_all(self) -> dict[str, object]:
        """Stop and remove every temporary in-process live session."""
        with self._lock:
            sessions = list(self._sessions.values())
            self._sessions.clear()
        return {
            "classification": "PLAYGROUND_LIVE_SESSIONS_CLEARED",
            "scientific_evidence": False,
            "cleared": len(sessions),
        }

    def list(self) -> list[dict[str, object]]:
        with self._lock:
            return [
                {"session_id": session_id, **session.snapshot()}
                for session_id, session in self._sessions.items()
            ]
