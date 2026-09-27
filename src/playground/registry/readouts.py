"""Small readout registry for playground summaries."""

from __future__ import annotations

from collections.abc import Sequence


def linear(rates: Sequence[float]) -> float:
    return sum(rates) / max(len(rates), 1)


def threshold(rates: Sequence[float]) -> int:
    return int(linear(rates) >= 10.0)


def population_vector(rates: Sequence[float]) -> list[float]:
    total = sum(rates)
    if total <= 0:
        return [0.0 for _ in rates]
    return [value / total for value in rates]


READOUTS = {
    "linear": linear,
    "threshold": threshold,
    "population_vector": population_vector,
}


def apply_readout(name: str, rates: Sequence[float]) -> object:
    try:
        readout = READOUTS[name]
    except KeyError as exc:
        raise ValueError(f"unknown playground readout: {name}") from exc
    return readout(rates)
