"""Compact data contract for custom playground dashboards."""

from __future__ import annotations

from collections.abc import Mapping

from .rate import population_rate_series
from .raster import raster_series
from .topology_2d import project_2d
from .topology_5d_projection import project_5d


def dashboard_payload(result: Mapping[str, object]) -> dict[str, object]:
    topology = result.get("topology", {})
    coordinates = (
        topology.get("coordinates", []) if isinstance(topology, Mapping) else []
    )
    dimensions = (
        int(topology.get("dimensions", 0)) if isinstance(topology, Mapping) else 0
    )
    projection = (
        project_5d(coordinates, components=2)
        if dimensions >= 4
        else project_2d(coordinates)
    )
    return {
        "manifest": result.get("manifest"),
        "metrics": result.get("metrics"),
        "raster": raster_series(result),
        "population_rate_hz": population_rate_series(result),
        "topology_projection": projection,
    }
