"""Observer-only longitudinal monitor for operational self-state research.

The monitor aggregates already exposed neuron state without mutating the core,
feeding rewards, changing thresholds, or authorizing actuators.  It is a
research instrument for preregistered longitudinal/self-reference studies and
must never be interpreted as evidence of consciousness, sentience, subjective
experience, or a complete self-model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class SelfMonitorSnapshot:
    """One immutable observation of aggregate internal state."""

    tick: int
    neuron_count: int
    active_neurons: int
    total_spikes: int
    mean_firing_rate: float
    mean_energy: float
    mean_threshold_adaptation: float
    mean_pre_trace: float
    mean_post_trace: float
    model_switch_count: int

    def to_dict(self) -> dict[str, int | float]:
        return {
            "tick": self.tick,
            "neuron_count": self.neuron_count,
            "active_neurons": self.active_neurons,
            "total_spikes": self.total_spikes,
            "mean_firing_rate": self.mean_firing_rate,
            "mean_energy": self.mean_energy,
            "mean_threshold_adaptation": self.mean_threshold_adaptation,
            "mean_pre_trace": self.mean_pre_trace,
            "mean_post_trace": self.mean_post_trace,
            "model_switch_count": self.model_switch_count,
        }


class SelfMonitor:
    """Bounded, read-only longitudinal observer over neuron state."""

    def __init__(self, *, max_history: int = 1024) -> None:
        if max_history < 1:
            raise ValueError("max_history must be >= 1")
        self.max_history = max_history
        self._history: list[SelfMonitorSnapshot] = []

    @property
    def history(self) -> tuple[SelfMonitorSnapshot, ...]:
        return tuple(self._history)

    def observe(self, network: Any, *, tick: int | None = None) -> SelfMonitorSnapshot:
        """Record aggregate state without writing to ``network`` or its neurons."""
        neurons = list(network.neurons.values())
        observed_tick = int(network.current_tick if tick is None else tick)
        snapshot = self._aggregate(neurons, tick=observed_tick)
        self._history.append(snapshot)
        overflow = len(self._history) - self.max_history
        if overflow > 0:
            del self._history[:overflow]
        return snapshot

    @staticmethod
    def _aggregate(neurons: Iterable[Any], *, tick: int) -> SelfMonitorSnapshot:
        values = list(neurons)
        count = len(values)
        if count == 0:
            return SelfMonitorSnapshot(
                tick=tick,
                neuron_count=0,
                active_neurons=0,
                total_spikes=0,
                mean_firing_rate=0.0,
                mean_energy=0.0,
                mean_threshold_adaptation=0.0,
                mean_pre_trace=0.0,
                mean_post_trace=0.0,
                model_switch_count=0,
            )

        def mean(name: str) -> float:
            return sum(float(getattr(neuron, name, 0.0)) for neuron in values) / count

        return SelfMonitorSnapshot(
            tick=tick,
            neuron_count=count,
            active_neurons=sum(
                1 for neuron in values if int(getattr(neuron, "spike_counter", 0)) > 0
            ),
            total_spikes=sum(int(getattr(neuron, "spike_counter", 0)) for neuron in values),
            mean_firing_rate=mean("firing_rate_estimate"),
            mean_energy=mean("energy"),
            mean_threshold_adaptation=mean("threshold_adaptation"),
            mean_pre_trace=mean("pre_trace"),
            mean_post_trace=mean("post_trace"),
            model_switch_count=sum(
                int(getattr(neuron, "model_switch_count", 0)) for neuron in values
            ),
        )


__all__ = ["SelfMonitor", "SelfMonitorSnapshot"]
