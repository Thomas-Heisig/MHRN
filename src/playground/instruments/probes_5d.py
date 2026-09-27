"""MHRN-5D exploratory occupancy probe.

This reports distribution only. It deliberately has no quality scale,
recommendation, score, or claim that 5D is superior.
"""

from __future__ import annotations

from collections.abc import Sequence

from .probes_nd import occupancy_nd


def occupancy(coordinates: Sequence[Sequence[float]], bins: int = 8) -> dict[str, int]:
    selected = [tuple(point[:5]) for point in coordinates if len(point) >= 5]
    return occupancy_nd(selected, bins=bins)
