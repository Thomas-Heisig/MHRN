"""Neutral 3D topology projection."""

from __future__ import annotations

from collections.abc import Sequence


def project_3d(coordinates: Sequence[Sequence[float]]) -> list[list[float]]:
    points: list[list[float]] = []
    for point in coordinates:
        points.append(
            [
                float(point[0]) if len(point) > 0 else 0.0,
                float(point[1]) if len(point) > 1 else 0.0,
                float(point[2]) if len(point) > 2 else 0.0,
            ]
        )
    return points
