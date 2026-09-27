"""Neutral 2D topology projection."""

from __future__ import annotations

from collections.abc import Sequence


def project_2d(coordinates: Sequence[Sequence[float]]) -> list[list[float]]:
    points: list[list[float]] = []
    for point in coordinates:
        x = float(point[0]) if len(point) > 0 else 0.0
        y = float(point[1]) if len(point) > 1 else 0.0
        points.append([x, y])
    return points
