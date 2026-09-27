"""Independent Brian2-side fixed-delay event probe for Stage-1 reference."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from reference.stage1_topology_brian2.integrator_probe import ProbeResult, run_trajectory


@dataclass(frozen=True)
class SynapseProbeTick:
    tick: int
    source: ProbeResult
    target: ProbeResult
    delivered_events: int
    target_synaptic_current: float

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        return value


def run_two_neuron_delay_probe(
    *,
    weight: float = 55.0,
    delay_ticks: int = 1,
    ticks: int = 3,
) -> list[SynapseProbeTick]:
    """Use an independent integer-tick queue around Brian2 neuron probes.

    The source receives current 100 at tick 0. Each source spike schedules one
    fixed-weight event for tick + delay_ticks. Due events are converted to target
    input current before the target's state transition for that tick.
    """

    source_currents = [100.0] + [0.0] * (ticks - 1)
    source_rows = run_trajectory(source_currents)

    queue: dict[int, list[float]] = {}
    target_currents: list[float] = []
    delivered_counts: list[int] = []
    for tick, source in enumerate(source_rows):
        due = queue.pop(tick, [])
        target_currents.append(sum(due))
        delivered_counts.append(len(due))
        if source.spiked:
            queue.setdefault(tick + delay_ticks, []).append(float(weight))

    target_rows = run_trajectory(target_currents)
    return [
        SynapseProbeTick(
            tick=tick,
            source=source_rows[tick],
            target=target_rows[tick],
            delivered_events=delivered_counts[tick],
            target_synaptic_current=target_currents[tick],
        )
        for tick in range(ticks)
    ]
