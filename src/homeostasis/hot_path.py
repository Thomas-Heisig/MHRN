"""Semantics-preserving homeostasis hot path.

The numerical update equations are unchanged from ``engine.HomeostasisEngine``.
The optimization removes the per-tick neuron sort, avoids rebuilding a live-ID
set on every tick, and emits at most one dirty notification per neuron after
homeostatic mutation.
"""

from __future__ import annotations

import math
from collections.abc import Mapping

from src.core.network import NeuralNetwork, StepResult

from .engine import HomeostasisEngine, HomeostasisStats, _clamp


class HotPathHomeostasisEngine(HomeostasisEngine):
    """Homeostasis engine with O(N) iteration and unchanged equations."""

    def __init__(self, network: NeuralNetwork, config: Mapping[str, object]) -> None:
        super().__init__(network, config)
        self._known_neuron_count = len(network.neurons)

    def update(self, step_result: StepResult) -> None:
        if not self.params.enabled:
            return

        spike_ids = set(step_result.spike_ids)
        alpha = 1.0 - math.exp(-1.0 / self.params.rate_tau_ticks)
        instantaneous_hz = 1000.0

        rate_sum = 0.0
        threshold_sum = 0.0
        energy_sum = 0.0
        active_neurons = 0

        # Topology removal is rare. Only pay the stale-rate cleanup cost when
        # the network size changed instead of materializing set(neurons) every tick.
        neuron_count = len(self.network.neurons)
        if neuron_count != self._known_neuron_count:
            stale = [
                neuron_id
                for neuron_id in self._rates_hz
                if neuron_id not in self.network.neurons
            ]
            for neuron_id in stale:
                self._rates_hz.pop(neuron_id, None)
            self._known_neuron_count = neuron_count

        # Python dict insertion order is stable. MHRN construction and restore
        # are deterministic, so an O(N log N) sort provides no additional
        # numerical determinism here.
        for neuron_id, neuron in self.network.neurons.items():
            previous_rate = self._rates_hz.get(neuron_id, 0.0)
            sample = instantaneous_hz if neuron_id in spike_ids else 0.0
            rate = previous_rate + alpha * (sample - previous_rate)
            self._rates_hz[neuron_id] = rate

            if neuron_id in spike_ids:
                active_neurons += 1

            changed = False
            rate_error = rate - self.params.target_rate_hz
            adjustment = self.params.threshold_learning_rate * rate_error
            next_threshold = _clamp(
                neuron.threshold_adaptation + adjustment,
                self.params.threshold_min,
                self.params.threshold_max,
            )
            if next_threshold != neuron.threshold_adaptation:
                neuron.threshold_adaptation = next_threshold
                changed = True

            if self.params.energy_enabled:
                recovery = self.params.energy_recovery_rate * (
                    self.params.target_energy - neuron.energy
                )
                next_energy = _clamp(
                    neuron.energy + recovery,
                    self.params.energy_min,
                    self.params.energy_max,
                )
                if next_energy != neuron.energy:
                    neuron.energy = next_energy
                    changed = True

            if changed:
                neuron.mark_dirty()

            rate_sum += rate
            threshold_sum += neuron.threshold_adaptation
            energy_sum += neuron.energy

        self._updates += 1
        count = neuron_count
        mean_rate = rate_sum / count if count else 0.0
        mean_threshold = threshold_sum / count if count else 0.0
        mean_energy = energy_sum / count if count else 0.0

        self._last_stats = HomeostasisStats(
            enabled=True,
            updates=self._updates,
            target_rate_hz=self.params.target_rate_hz,
            mean_rate_hz=mean_rate,
            mean_rate_error_hz=mean_rate - self.params.target_rate_hz,
            mean_threshold_adaptation=mean_threshold,
            target_energy=self.params.target_energy,
            mean_energy=mean_energy,
            mean_energy_error=self.params.target_energy - mean_energy,
            active_neurons=active_neurons,
        )


__all__ = ["HotPathHomeostasisEngine"]
