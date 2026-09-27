"""Raster visualization data preparation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


def raster_series(
    result: Mapping[str, object], limit: int = 10_000
) -> dict[str, list[int]]:
    monitors = result.get("monitors", {})
    spikes = monitors.get("spikes", []) if isinstance(monitors, Mapping) else []
    ticks: list[int] = []
    neuron_ids: list[int] = []
    if isinstance(spikes, Sequence):
        for item in spikes[:limit]:
            if isinstance(item, Mapping):
                ticks.append(int(item.get("tick", 0)))
                neuron_ids.append(int(item.get("neuron_id", 0)))
    return {"ticks": ticks, "neuron_ids": neuron_ids}
