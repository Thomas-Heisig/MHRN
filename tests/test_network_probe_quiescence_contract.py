from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.research.network_probe import NetworkImpulseProbe


class _AlwaysQuiescentRuntime:
    def __init__(self) -> None:
        self.injected: dict[int, float] = {}

    def inject_current_batch(self, currents: Mapping[int, float]) -> None:
        self.injected = dict(currents)

    def step(self) -> dict[str, Any]:
        return {
            "quiescent": True,
            "spike_ids": (),
            "output_spike_ids": (),
            "delivered_events": 0,
            "synaptic_current_targets": 0,
            "total_synapses": 0,
        }


def test_full_window_probe_does_not_report_quiescence_early_stop() -> None:
    runtime = _AlwaysQuiescentRuntime()
    signature = NetworkImpulseProbe(
        source_neuron=1,
        current=100.0,
        max_ticks=5,
        min_ticks=5,
    ).run(runtime)

    assert signature.ticks_executed == 5
    assert signature.stopped_on_quiescence is False


def test_explicit_early_stop_probe_reports_quiescence_stop() -> None:
    runtime = _AlwaysQuiescentRuntime()
    signature = NetworkImpulseProbe(
        source_neuron=1,
        current=100.0,
        max_ticks=5,
        min_ticks=1,
    ).run(runtime)

    assert signature.ticks_executed == 1
    assert signature.stopped_on_quiescence is True
