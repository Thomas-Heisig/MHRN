"""PCA projection of arbitrary/5D playground coordinates."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def project_5d(
    coordinates: Sequence[Sequence[float]], components: int = 2
) -> list[list[float]]:
    if components not in (2, 3):
        raise ValueError("components must be 2 or 3")
    if not coordinates:
        return []
    width = max(len(point) for point in coordinates)
    matrix = np.zeros((len(coordinates), width), dtype=float)
    for row, point in enumerate(coordinates):
        matrix[row, : len(point)] = [float(value) for value in point]
    matrix -= matrix.mean(axis=0, keepdims=True)
    if matrix.shape[0] == 1:
        return [[0.0 for _ in range(components)]]
    _, _, vt = np.linalg.svd(matrix, full_matrices=False)
    available = min(components, vt.shape[0])
    projected = matrix @ vt[:available].T
    if available < components:
        projected = np.pad(projected, ((0, 0), (0, components - available)))
    return [
        [float(projected[row, column]) for column in range(projected.shape[1])]
        for row in range(projected.shape[0])
    ]
