"""In-memory monitors for bounded playground simulations."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SpikeMonitor:
    ticks: list[int] = field(default_factory=list)
    neuron_ids: list[int] = field(default_factory=list)

    def record(self, tick: int, neuron_id: int) -> None:
        self.ticks.append(tick)
        self.neuron_ids.append(neuron_id)

    def rows(self, limit: int = 10_000) -> list[dict[str, int]]:
        return [
            {"tick": tick, "neuron_id": neuron_id}
            for tick, neuron_id in list(zip(self.ticks, self.neuron_ids))[:limit]
        ]


@dataclass(slots=True)
class StateMonitor:
    samples: list[dict[str, object]] = field(default_factory=list)

    def record(self, tick: int, states: list[dict[str, float]], stride: int) -> None:
        if tick % stride:
            return
        self.samples.append(
            {
                "tick": tick,
                "v": [round(state.get("v", 0.0), 5) for state in states],
            }
        )


@dataclass(slots=True)
class RateMonitor:
    counts: list[int]

    @classmethod
    def create(cls, n_neurons: int) -> "RateMonitor":
        return cls([0 for _ in range(n_neurons)])

    def record(self, neuron_id: int) -> None:
        self.counts[neuron_id] += 1

    def rates_hz(self, ticks: int, dt_ms: float) -> list[float]:
        seconds = max(ticks * dt_ms / 1000.0, 1e-9)
        return [count / seconds for count in self.counts]
