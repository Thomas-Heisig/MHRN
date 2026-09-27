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
                "learning": self.learning.summary(),
                "execution": self.switcher.summary(),
                "state_digest": self.state_digest(),
            }


class PANSessionDaemon:
    """In-process manager for persistent live sessions."""

    def __init__(self) -> None:
        self._sessions: dict[str, PANLiveSession] = {}
        self._lock = threading.RLock()

    def create(self, config: PlaygroundConfig) -> str:
        session_id = "PGLIVE-" + uuid.uuid4().hex[:12]
        with self._lock:
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
