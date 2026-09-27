"""Neutral N-dimensional exploratory probes."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence


def occupancy_nd(
    coordinates: Sequence[Sequence[float]], bins: int = 8
) -> dict[str, int]:
    """Return raw occupancy counts without good/bad or quality semantics."""

    if bins < 2:
        raise ValueError("bins must be >= 2")
    counts: Counter[str] = Counter()
    for point in coordinates:
        key = ",".join(
            str(min(bins - 1, max(0, int(float(value) * bins)))) for value in point
        )
        counts[key] += 1
    return dict(counts)


def dimension_utilization(
    coordinates: Sequence[Sequence[float]],
) -> list[float]:
    if not coordinates:
        return []
    width = max(len(point) for point in coordinates)
    result: list[float] = []
    for axis in range(width):
        values = [float(point[axis]) for point in coordinates if axis < len(point)]
        result.append(max(values, default=0.0) - min(values, default=0.0))
    return result
