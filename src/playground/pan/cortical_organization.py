"""Hybrid fixed-layer/plastic-connectivity organization for PAN Playground."""

from __future__ import annotations

from collections.abc import Sequence


class CorticalOrganization:
    """Assign neurons to layers while allowing bounded gain adaptation.

    Layer labels are an engineering condition, not a claim of cortical biology.
    """

    def __init__(
        self,
        *,
        n_neurons: int,
        layers: int = 6,
        plasticity: bool = True,
        learning_rate: float = 0.01,
    ) -> None:
        if n_neurons < 1:
            raise ValueError("n_neurons must be positive")
        if not 2 <= layers <= 12:
            raise ValueError("layers must be between 2 and 12")
        if not 0.0 <= learning_rate <= 1.0:
            raise ValueError("learning_rate must be between 0 and 1")
        self.n_neurons = n_neurons
        self.layers = layers
        self.plasticity = plasticity
        self.learning_rate = learning_rate
        self.layer_of = [
            min(layers - 1, (index * layers) // n_neurons)
            for index in range(n_neurons)
        ]
        self.gains = [1.0 for _ in range(layers)]
        self.updates = 0

    def apply(self, currents: Sequence[float]) -> list[float]:
        if len(currents) != self.n_neurons:
            raise ValueError("current vector size mismatch")
        return [
            float(value) * self.gains[self.layer_of[index]]
            for index, value in enumerate(currents)
        ]

    def observe(self, spiked_neurons: Sequence[int], reward: float = 0.0) -> None:
        if not self.plasticity:
            return
        counts = [0 for _ in range(self.layers)]
        for neuron_id in spiked_neurons:
            if 0 <= neuron_id < self.n_neurons:
                counts[self.layer_of[neuron_id]] += 1
        for layer, count in enumerate(counts):
            activity = count / max(1, self.n_neurons // self.layers)
            delta = self.learning_rate * reward * activity
            self.gains[layer] = min(1.5, max(0.5, self.gains[layer] + delta))
        self.updates += 1

    def output_layer_neurons(self) -> list[int]:
        target = self.layers - 1
        return [
            index for index, layer in enumerate(self.layer_of) if layer == target
        ]

    def summary(self) -> dict[str, object]:
        counts = [
            sum(1 for value in self.layer_of if value == layer)
            for layer in range(self.layers)
        ]
        return {
            "classification": "PLAYGROUND_CORTICAL_ORGANIZATION",
            "scientific_evidence": False,
            "biological_equivalence_claim": False,
            "mode": "FIXED_LAYER_ASSIGNMENT_PLASTIC_GAINS",
            "layers": self.layers,
            "layer_counts": counts,
            "plasticity_enabled": self.plasticity,
            "learning_rate": self.learning_rate,
            "layer_gains": list(self.gains),
            "updates": self.updates,
        }
