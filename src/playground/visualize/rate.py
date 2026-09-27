"""Rate visualization data preparation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


def population_rate_series(result: Mapping[str, object]) -> list[float]:
    config = result.get("config", {})
    monitors = result.get("monitors", {})
    if not isinstance(config, Mapping) or not isinstance(monitors, Mapping):
        return []
    counts = monitors.get("tick_spike_counts", [])
    if not isinstance(counts, Sequence):
        return []
    n = max(1, int(config.get("n_neurons", 1)))
    dt_ms = max(1e-9, float(config.get("dt_ms", 1.0)))
    return [float(value) / n / (dt_ms / 1000.0) for value in counts]
