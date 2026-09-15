"""Experimental spiking transition-model candidate for Stage 6.

The model binds discrete state/action contexts to dedicated context neurons and
learns context -> next-state associations through the existing pair-STDP
pipeline. Prediction is produced by subsequent output-neuron spikes, not by a
transition lookup table. The discrete context encoder is intentionally explicit:
this is an experimental exact-context neural associator, not evidence of a
continuous or generalising biological world model.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from src.core.network import NeuralNetwork
from src.learning.learning_engine import LearningEngine


class SpikingWorldModelError(ValueError):
    """Raised when the experimental spiking world-model contract is invalid."""


@dataclass(frozen=True, slots=True)
class SpikingContext:
    """Discrete state/action context presented to one context neuron."""

    state_key: str
    action_key: str

    def __post_init__(self) -> None:
        if not self.state_key or not self.action_key:
            raise SpikingWorldModelError("state_key and action_key must be non-empty")


@dataclass(frozen=True, slots=True)
class SpikingWorldPrediction:
    """One output decoded from actual SNN spikes."""

    predicted_state: str | None
    output_spike_ids: tuple[int, ...]
    latency_steps: int | None
    source: str = "spiking_stdp_associator"
    scientific_status: str = "experimental_exact_context_neural_candidate"


class SpikingTransitionWorldModel:
    """Bounded STDP-trained context-to-next-state spiking associator.

    Learning is teacher-forced: the context neuron spikes before the observed
    next-state output neuron. The existing LearningEngine then changes synaptic
    weights through pair STDP. During ``predict`` the LearningEngine is never
    updated, including post-inference cooldown, so inference cannot learn.
    """

    scientific_status = "experimental_exact_context_neural_candidate"

    def __init__(
        self,
        *,
        seed: int = 0,
        max_contexts: int = 64,
        max_states: int = 32,
        training_repetitions: int = 3,
        cooldown_steps: int = 8,
        inference_steps: int = 4,
    ) -> None:
        for name, value in (
            ("max_contexts", max_contexts),
            ("max_states", max_states),
            ("training_repetitions", training_repetitions),
            ("cooldown_steps", cooldown_steps),
            ("inference_steps", inference_steps),
        ):
            if type(value) is not int or value <= 0:
                raise SpikingWorldModelError(f"{name} must be a positive integer")
        if max_contexts + max_states > 1024:
            raise SpikingWorldModelError("combined neural capacity exceeds 1024")

        config: dict[str, Any] = {
            "dimensions": [4, 4, 4, 4, 4],
            "simulation": {"dt_ms": 1.0, "max_delay": 4, "debug_invariants": True},
            "network": {
                "weight_min": 0.0,
                "weight_max": 200.0,
                "initial_connections_per_neuron": 0,
                "neighbour_radius": 1.0,
            },
            "neuron": {"a": 0.02, "b": 0.2, "c": -65.0, "d": 8.0},
            "energy": {"initial": 1.0, "spike_cost": 0.001, "affects_firing": False},
            "topology": {
                "allow_self_connections": False,
                "allow_parallel_connections": False,
            },
            "stdp": {
                "enabled": True,
                "a_plus": 100.0,
                "a_minus": 0.0,
                "tau_plus": 20.0,
                "tau_minus": 20.0,
                "min_weight": 0.0,
                "max_weight": 200.0,
            },
            "eligibility": {"enabled": False, "tau_ticks": 200.0},
            "reward": {"enabled": False},
        }
        self.network = NeuralNetwork(config, random.Random(seed))
        self.learning = LearningEngine(self.network, config)
        self.max_contexts = max_contexts
        self.max_states = max_states
        self.training_repetitions = training_repetitions
        self.cooldown_steps = cooldown_steps
        self.inference_steps = inference_steps
        self._context_neurons: dict[SpikingContext, int] = {}
        self._state_neurons: dict[str, int] = {}
        self._state_by_neuron: dict[int, str] = {}

    @staticmethod
    def _coord(index: int) -> tuple[int, int, int, int, int]:
        values: list[int] = []
        remaining = index
        for _ in range(5):
            values.append(remaining % 4)
            remaining //= 4
        return (values[0], values[1], values[2], values[3], values[4])

    def _add_neuron(self) -> int:
        index = len(self.network.neurons)
        if index >= 1024:
            raise SpikingWorldModelError("neural address capacity exhausted")
        return self.network.add_neuron(self._coord(index))

    def _ensure_state(self, state_key: str) -> int:
        if not state_key:
            raise SpikingWorldModelError("next state must be non-empty")
        existing = self._state_neurons.get(state_key)
        if existing is not None:
            return existing
        if len(self._state_neurons) >= self.max_states:
            raise SpikingWorldModelError("next-state capacity exhausted")
        neuron_id = self._add_neuron()
        self._state_neurons[state_key] = neuron_id
        self._state_by_neuron[neuron_id] = state_key
        for context_id in self._context_neurons.values():
            self.network.connect(context_id, neuron_id, 0.0, 1)
        return neuron_id

    def _ensure_context(self, context: SpikingContext) -> int:
        existing = self._context_neurons.get(context)
        if existing is not None:
            return existing
        if len(self._context_neurons) >= self.max_contexts:
            raise SpikingWorldModelError("context capacity exhausted")
        neuron_id = self._add_neuron()
        self._context_neurons[context] = neuron_id
        for output_id in self._state_neurons.values():
            self.network.connect(neuron_id, output_id, 0.0, 1)
        return neuron_id

    def _cooldown(self, *, learning: bool) -> None:
        for _ in range(self.cooldown_steps):
            result = self.network.step()
            if learning:
                self.learning.update(result)

    def observe(
        self,
        context: SpikingContext,
        next_state: str,
        *,
        repetitions: int | None = None,
    ) -> None:
        """Teacher-force one observed transition through pair-STDP."""

        repeats = self.training_repetitions if repetitions is None else repetitions
        if type(repeats) is not int or repeats <= 0:
            raise SpikingWorldModelError("repetitions must be a positive integer")
        output_id = self._ensure_state(next_state)
        context_id = self._ensure_context(context)
        for _ in range(repeats):
            self.network.inject_current(context_id, 100.0)
            self.learning.update(self.network.step())
            self.network.inject_current(output_id, 100.0)
            self.learning.update(self.network.step())
            self._cooldown(learning=True)

    def predict(self, context: SpikingContext) -> SpikingWorldPrediction:
        """Return the first learned next-state output that actually spikes."""

        context_id = self._context_neurons.get(context)
        if context_id is None:
            return SpikingWorldPrediction(None, (), None)
        before = self.synaptic_weights(context)
        self.network.inject_current(context_id, 100.0)
        self.network.step()
        all_output_spikes: list[int] = []
        latency: int | None = None
        for step in range(1, self.inference_steps + 1):
            result = self.network.step()
            outputs = tuple(
                neuron_id
                for neuron_id in result.spike_ids
                if neuron_id in self._state_by_neuron
            )
            if outputs:
                all_output_spikes.extend(outputs)
                latency = step
                break
        self._cooldown(learning=False)
        after = self.synaptic_weights(context)
        if after != before:
            raise SpikingWorldModelError("inference changed synaptic weights")
        unique = tuple(sorted(set(all_output_spikes)))
        predicted = self._state_by_neuron.get(unique[0]) if len(unique) == 1 else None
        return SpikingWorldPrediction(predicted, unique, latency)

    def synaptic_weights(self, context: SpikingContext) -> dict[str, float]:
        """Inspect learned context-output weights for research diagnostics."""

        context_id = self._context_neurons.get(context)
        if context_id is None:
            return {}
        by_target = {
            synapse.target_id: synapse.weight
            for synapse in self.network.synapses.get(context_id, ())
        }
        return {
            state: float(by_target.get(neuron_id, 0.0))
            for state, neuron_id in sorted(self._state_neurons.items())
        }

    @property
    def context_count(self) -> int:
        return len(self._context_neurons)

    @property
    def state_count(self) -> int:
        return len(self._state_neurons)


__all__ = [
    "SpikingContext",
    "SpikingTransitionWorldModel",
    "SpikingWorldModelError",
    "SpikingWorldPrediction",
]
