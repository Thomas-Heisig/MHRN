"""Bounded PAN hyperstate runtime for non-canonical Playground sessions."""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any

from .candidates import pan_research_candidates
from .hypervector import axis_schema, bundle

PANState = MutableMapping[str, Any]


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _sigmoid(value: float) -> float:
    value = max(-40.0, min(40.0, value))
    return 1.0 / (1.0 + math.exp(-value))


class PANRuntime:
    """Exploratory PAN controller layered on the generic Playground engine."""

    def __init__(
        self,
        *,
        n_neurons: int,
        dimensions: int,
        seed: int,
        feedback_gain: float,
        health_decay: float,
        apoptosis_threshold: float,
        closed_loop: bool,
        coordinates: Sequence[Sequence[float]],
        degree: Sequence[int],
        feedback_delay: int = 0,
        feedback_source: str = "population",
        feedback_target: str = "all",
        feedback_nonlinearity: str = "linear",
        feedback_threshold: float = 0.0,
        feedback_saturation: float = 100.0,
    ) -> None:
        if not 5 <= dimensions <= 32:
            raise ValueError("PAN dimensions must be between 5 and 32")
        self.n_neurons = n_neurons
        self.dimensions = dimensions
        self.feedback_gain = feedback_gain
        self.health_decay = health_decay
        self.apoptosis_threshold = apoptosis_threshold
        self.closed_loop = closed_loop
        self.coordinates = coordinates
        self.degree = degree
        self.feedback_delay = feedback_delay
        self.feedback_source = feedback_source
        self.feedback_target = feedback_target
        self.feedback_nonlinearity = feedback_nonlinearity
        self.feedback_threshold = feedback_threshold
        self.feedback_saturation = feedback_saturation
        rng = random.Random(seed ^ 0x50414E)
        scale = 1.0 / math.sqrt(max(dimensions, 1))
        self.feedback_weights: list[list[float]] = [
            [rng.uniform(-scale, scale) for _ in range(dimensions)]
            for _ in range(n_neurons)
        ]
        self.population_vector = [0.0 for _ in range(dimensions)]
        self.feedback_history: list[list[float]] = []
        target_rng = random.Random(seed ^ 0xFADE)
        self.random_target_mask = [target_rng.random() < 0.5 for _ in range(n_neurons)]
        self.feedback_abs_total = 0.0
        self.feedback_samples = 0
        self.apoptosis_events: list[dict[str, object]] = []

    def initialize(self, states: Sequence[PANState]) -> None:
        """Attach bounded PAN state variables to existing neuron states."""

        if len(states) != self.n_neurons:
            raise ValueError("PAN state count does not match n_neurons")
        for neuron_id, state in enumerate(states):
            state["pan_health"] = 1.0
            state["pan_amplitude"] = 1.0
            state["pan_energy"] = 1.0
            state["pan_activity_ema"] = 0.01
            state["pan_consolidation"] = 0.0
            state["pan_alive"] = True
            state["pan_information_proxy"] = 0.0
            state["pan_x_hd"] = [0.0 for _ in range(self.dimensions)]
            state["pan_neuron_id"] = neuron_id

    def _feedback_vector(self) -> list[float]:
        if self.feedback_delay <= 0:
            vector = list(self.population_vector)
        elif len(self.feedback_history) > self.feedback_delay:
            vector = list(self.feedback_history[-1 - self.feedback_delay])
        else:
            vector = [0.0 for _ in range(self.dimensions)]

        if self.feedback_source == "layer":
            cutoff = max(1, self.dimensions // 2)
            vector = [
                value if index < cutoff else 0.0 for index, value in enumerate(vector)
            ]
        elif self.feedback_source == "subset":
            vector = [
                value if index % 2 == 0 else 0.0 for index, value in enumerate(vector)
            ]
        elif self.feedback_source == "hypervector":
            vector = [math.tanh(value) for value in vector]
        return vector

    def feedback_currents(self) -> list[float]:
        """Project a selectable delayed PAN source back to target neurons."""

        if not self.closed_loop:
            return [0.0 for _ in range(self.n_neurons)]
        vector = self._feedback_vector()
        currents: list[float] = []
        layer_limit = max(1, self.n_neurons // 4)
        for neuron_id, row in enumerate(self.feedback_weights):
            enabled = True
            if self.feedback_target == "layer":
                enabled = neuron_id < layer_limit
            elif self.feedback_target == "random_subset":
                enabled = self.random_target_mask[neuron_id]
            raw = sum(weight * value for weight, value in zip(row, vector))
            if self.feedback_nonlinearity == "tanh":
                shaped = math.tanh(raw)
            elif self.feedback_nonlinearity == "sign":
                shaped = 1.0 if raw > 0.0 else (-1.0 if raw < 0.0 else 0.0)
            elif self.feedback_nonlinearity == "clip":
                shaped = max(-1.0, min(1.0, raw))
            else:
                shaped = raw
            if abs(shaped) < self.feedback_threshold:
                shaped = 0.0
            current = self.feedback_gain * shaped if enabled else 0.0
            current = max(
                -self.feedback_saturation,
                min(self.feedback_saturation, current),
            )
            currents.append(current)
            self.feedback_abs_total += abs(current)
            self.feedback_samples += 1
        return currents

    def _position_projection(self, neuron_id: int) -> float:
        if neuron_id >= len(self.coordinates):
            return 0.0
        point = self.coordinates[neuron_id]
        if not point:
            return 0.0
        return _clamp(sum(float(value) for value in point) / len(point))

    def update(
        self,
        *,
        tick: int,
        dt_ms: float,
        states: Sequence[PANState],
        spiked_neurons: Sequence[int],
        plasticity_active: bool,
    ) -> None:
        """Advance PAN health, energy and hyperstate after one network tick."""

        spiked = set(spiked_neurons)
        vectors: list[list[float]] = []
        target_activity = 0.02
        dt_s = dt_ms / 1000.0
        for neuron_id, state in enumerate(states):
            alive = bool(state.get("pan_alive", True))
            if not alive:
                vectors.append([float(value) for value in state.get("pan_x_hd", [])])
                continue

            did_spike = neuron_id in spiked
            activity = float(state.get("pan_activity_ema", 0.01))
            activity = 0.97 * activity + 0.03 * (1.0 if did_spike else 0.0)
            energy = float(state.get("pan_energy", 1.0))
            energy += 0.015 * (1.0 - energy)
            if did_spike:
                energy -= 0.035
            energy = _clamp(energy)

            p = _clamp(activity, 1e-6, 1.0 - 1e-6)
            surprise_bits = -math.log2(p if did_spike else (1.0 - p))
            information_proxy = _clamp(surprise_bits / 8.0)

            stress = abs(activity - target_activity) + max(0.0, 0.35 - energy)
            health = float(state.get("pan_health", 1.0))
            health -= self.health_decay * dt_s
            health -= 0.0015 * stress
            health += 0.0005 * max(0.0, 1.0 - stress)
            health = _clamp(health)

            consolidation = float(state.get("pan_consolidation", 0.0))
            consolidation = _clamp(
                0.995 * consolidation + (0.005 if did_spike else 0.0)
            )
            amplitude = _clamp(0.2 + 0.8 * health, 0.2, 1.0)

            membrane = float(state.get("v", -65.0))
            threshold = float(state.get("pan_threshold", -50.0))
            excitability = _sigmoid((membrane - threshold) / 5.0)
            plasticity = health if plasticity_active else 0.0
            neuromodulation = 0.5 + 0.5 * math.sin(2.0 * math.pi * (tick % 64) / 64.0)
            coupling = _clamp(self.degree[neuron_id] / max(self.n_neurons - 1, 1))

            vector = [0.0 for _ in range(self.dimensions)]
            base_values = [
                (tick + 1) * dt_s,
                excitability,
                plasticity,
                information_proxy,
                health,
                neuromodulation,
                energy,
                self._position_projection(neuron_id),
                consolidation,
                coupling,
            ]
            for index, value in enumerate(base_values[: self.dimensions]):
                vector[index] = float(value)

            state["pan_health"] = health
            state["pan_amplitude"] = amplitude
            state["pan_energy"] = energy
            state["pan_activity_ema"] = activity
            state["pan_consolidation"] = consolidation
            state["pan_information_proxy"] = information_proxy
            state["pan_x_hd"] = vector

            if health <= self.apoptosis_threshold:
                state["pan_alive"] = False
                self.apoptosis_events.append(
                    {
                        "tick": tick,
                        "neuron_id": neuron_id,
                        "health": health,
                    }
                )
            vectors.append(vector)

        if vectors:
            self.population_vector = [
                sum(vector[index] for vector in vectors) / len(vectors)
                for index in range(self.dimensions)
            ]
            self.feedback_history.append(list(self.population_vector))
            keep = max(2, self.feedback_delay + 2)
            if len(self.feedback_history) > keep:
                self.feedback_history = self.feedback_history[-keep:]

    def summary(self, states: Sequence[Mapping[str, Any]]) -> dict[str, object]:
        """Return descriptive PAN diagnostics with explicit evidence boundaries."""

        health = [float(state.get("pan_health", 1.0)) for state in states]
        energy = [float(state.get("pan_energy", 1.0)) for state in states]
        alive = sum(1 for state in states if bool(state.get("pan_alive", True)))
        vectors = [
            [float(value) for value in state.get("pan_x_hd", [])] for state in states
        ]
        sample = [
            {
                "neuron_id": index,
                "alive": bool(state.get("pan_alive", True)),
                "health": float(state.get("pan_health", 1.0)),
                "energy": float(state.get("pan_energy", 1.0)),
                "amplitude": float(state.get("pan_amplitude", 1.0)),
                "x_hd": [float(value) for value in state.get("pan_x_hd", [])],
            }
            for index, state in enumerate(states[:128])
        ]
        feedback_mean = (
            self.feedback_abs_total / self.feedback_samples
            if self.feedback_samples
            else 0.0
        )
        return {
            "classification": "PLAYGROUND_PAN",
            "scientific_evidence": False,
            "evidence_eligible": False,
            "dimensions": self.dimensions,
            "axes": axis_schema(self.dimensions),
            "population_vector": list(self.population_vector),
            "population_bundle": bundle(vectors),
            "closed_loop": self.closed_loop,
            "feedback_gain": self.feedback_gain,
            "feedback_delay": self.feedback_delay,
            "feedback_source": self.feedback_source,
            "feedback_target": self.feedback_target,
            "feedback_nonlinearity": self.feedback_nonlinearity,
            "feedback_threshold": self.feedback_threshold,
            "feedback_saturation": self.feedback_saturation,
            "mean_abs_feedback_current": feedback_mean,
            "alive_neurons": alive,
            "apoptotic_neurons": self.n_neurons - alive,
            "apoptosis_events": list(self.apoptosis_events),
            "mean_health": sum(health) / len(health) if health else 0.0,
            "min_health": min(health, default=0.0),
            "mean_energy": sum(energy) / len(energy) if energy else 0.0,
            "information_axis": "local_surprise_proxy_not_PID",
            "pid_status": "NOT_IMPLEMENTED",
            "world_model_status": (
                "exploratory_state_space_only_not_validated_world_model"
            ),
            "homeostasis": {
                "ultrafast_target_ms": 5.0,
                "fast_target_ms": 2000.0,
                "medium_target_ms": 300000.0,
                "slow_target_ms": 3600000.0,
                "note": (
                    "Continuous bounded approximation; no claim that these "
                    "timescales reproduce biological or canonical MHRN dynamics."
                ),
            },
            "state_sample": sample,
            "research_candidates": pan_research_candidates(),
            "promotion_path": (
                "new hypothesis -> preregistration -> freeze -> new canonical "
                "DATA run -> Human Review -> optional EVID"
            ),
        }
