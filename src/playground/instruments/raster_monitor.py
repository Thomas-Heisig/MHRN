"""Raster-series helper for playground spike data."""

from __future__ import annotations

from collections.abc import Iterable, Mapping


def raster_rows(
    spikes: Iterable[Mapping[str, int]], limit: int = 10_000
) -> list[tuple[int, int]]:
    rows: list[tuple[int, int]] = []
    for spike in spikes:
        if len(rows) >= limit:
            break
        rows.append((int(spike["tick"]), int(spike["neuron_id"])))
    return rows
