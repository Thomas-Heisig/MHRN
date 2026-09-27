"""Stateful PAN live-session runtime for the isolated Playground.

This module intentionally stays outside the canonical research runtime. It keeps
neuron/synapse state across API calls so PAN can be driven interactively.
"""

from __future__ import annotations

import hashlib
import math
import random
import threading
import uuid
from collections import deque
from collections.abc import Mapping, Sequence

from ..models import PlaygroundConfig
from ..registry.neuron_models import get_neuron_model
from ..registry.topology_generators import build_topology
from .behavioral_learning import BehavioralLearningEngine
from .mode_switcher import ModeSwitcher
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
        self.adjacency: list[list[int]] = [[] for _ in range(config.n_neurons)]
        self.weights: dict[tuple[int, int], float] = {}
        self.delays: dict[tuple[int, int], int] = {}
        for source, target in self.topology.edges:
            self.adjacency[source].append(target)
            self.weights[(source, target)] = config.weight
            self.delays[(source, target)] = max(1, config.delay_ticks)

        self.pending = [
            [0.0 for _ in range(config.n_neurons)]
            for _ in range(max(65, config.delay_ticks + 2))
        ]
        self.tick = 0
        self.rng = random.Random(config.seed ^ 0x71AE)
        self.input_queue: deque[tuple[list[float], int]] = deque()
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
                neuron * self.config.behavior_action_count
                // self.config.n_neurons,
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

    def step(self, ticks: int = 32) -> dict[str, object]:
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
                external = [
                    value + self.config.pan_bias_current for value in external
                ]
                if self.thalamic is not None:
                    external = self.thalamic.apply(external, self.last_spikes)
                behavior_bias = (
                    self.learning.bias_currents()
                    if self.learning_enabled
                    else [0.0 for _ in range(self.config.n_neurons)]
                )
                external = [
                    external[index] + behavior_bias[index]
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
                        delivery = (
                            self.tick + self.delays[edge]
                        ) % len(self.pending)
                        self.pending[delivery][target] += self.weights[edge]

                if self.learning_enabled:
                    self.learning.observe(spiked)
                    if self.auto_reward_enabled:
                        reward = self.learning.maybe_learn(self.tick)
                        if reward is not None:
                            rewards.append(reward)
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
            "actions": actions[-64:],
            "rewards": rewards[-64:],
            "learning_enabled": self.learning_enabled,
            "learning": self.learning.summary(),
            "execution": self.switcher.summary(),
            "thalamic": self.thalamic.summary() if self.thalamic else None,
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
                },
            }

    def import_checkpoint(self, payload: Mapping[str, object]) -> None:
        """Restore a checkpoint created by :meth:`export_checkpoint`."""

        with self.lock:
            raw_states = payload.get("states")
            raw_pending = payload.get("pending")
            if not isinstance(raw_states, list) or len(raw_states) != len(self.states):
                raise ValueError("checkpoint state count mismatch")
            if not isinstance(raw_pending, list) or len(raw_pending) != len(self.pending):
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

            learning = payload.get("learning")
            if isinstance(learning, Mapping):
                raw_policy = learning.get("policy")
                if isinstance(raw_policy, list):
                    self.learning.policy = [_checkpoint_float(value) for value in raw_policy]
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

    def list(self) -> list[dict[str, object]]:
        with self._lock:
            return [
                {"session_id": session_id, **session.snapshot()}
                for session_id, session in self._sessions.items()
            ]
