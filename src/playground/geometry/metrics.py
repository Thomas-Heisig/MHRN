"""Geometry metrics for non-canonical Playground topologies.

The geometric coordinate contract is independent of PAN state dimensions:

    g_i = (x, y, z, a, b)

x/y/z are normalized Cartesian coordinates. a/b are cyclic angular
coordinates on a torus S1 x S1. They are not a Klein-bottle identification.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence


def cyclic_distance(left: float, right: float, period: float = 2.0 * math.pi) -> float:
    """Shortest distance on a periodic scalar coordinate."""

    delta = abs(float(left) - float(right)) % period
    return min(delta, period - delta)


def geometric_components(
    left: Sequence[float],
    right: Sequence[float],
    *,
    lambda_a: float,
    lambda_b: float,
) -> dict[str, float]:
    """Return spatial, toroidal and additive mixed distances."""

    if len(left) < 5 or len(right) < 5:
        raise ValueError("geometric_5d coordinates require x,y,z,a,b")

    spatial_sq = sum(
        (float(left[index]) - float(right[index])) ** 2 for index in range(3)
    )
    da = cyclic_distance(float(left[3]), float(right[3]))
    db = cyclic_distance(float(left[4]), float(right[4]))

    # Normalize cyclic distances by pi so each periodic component is in [0,1].
    da_norm = da / math.pi
    db_norm = db / math.pi
    topological_sq = lambda_a * da_norm**2 + lambda_b * db_norm**2

    spatial = math.sqrt(spatial_sq)
    topological = math.sqrt(topological_sq)
    mixed = math.sqrt(spatial_sq + topological_sq)
    shortcut_union = min(spatial, topological)

    return {
        "spatial_distance": spatial,
        "topological_distance": topological,
        "mixed_distance": mixed,
        "shortcut_union_distance": shortcut_union,
        "cyclic_a": da,
        "cyclic_b": db,
    }


def connection_distance(
    left: Sequence[float],
    right: Sequence[float],
    *,
    lambda_a: float,
    lambda_b: float,
    mode: str,
) -> float:
    components = geometric_components(
        left,
        right,
        lambda_a=lambda_a,
        lambda_b=lambda_b,
    )
    if mode == "mixed_additive":
        return components["mixed_distance"]
    if mode == "shortcut_union":
        return components["shortcut_union_distance"]
    raise ValueError(f"unknown geometric connection mode: {mode}")


def connection_probability(
    left: Sequence[float],
    right: Sequence[float],
    *,
    lambda_a: float,
    lambda_b: float,
    radius: float,
    sigma: float,
    p0: float,
    mode: str,
) -> float:
    distance = connection_distance(
        left,
        right,
        lambda_a=lambda_a,
        lambda_b=lambda_b,
        mode=mode,
    )
    if distance > radius:
        return 0.0
    scale = max(sigma, 1e-9)
    return p0 * math.exp(-(distance**2) / (2.0 * scale**2))


def conduction_delay_ticks(
    left: Sequence[float],
    right: Sequence[float],
    *,
    velocity_per_tick: float,
    minimum_ticks: int = 1,
    maximum_ticks: int = 64,
) -> int:
    """Distance delay using x/y/z only; a/b never shorten conduction length."""

    if len(left) < 3 or len(right) < 3:
        return minimum_ticks
    spatial = math.sqrt(
        sum((float(left[index]) - float(right[index])) ** 2 for index in range(3))
    )
    velocity = max(float(velocity_per_tick), 1e-9)
    delay = max(minimum_ticks, math.ceil(spatial / velocity))
    return min(maximum_ticks, delay)


def _out_degree(n: int, edges: Sequence[Sequence[int]]) -> list[int]:
    values = [0 for _ in range(n)]
    for edge in edges:
        if len(edge) < 2:
            continue
        source = int(edge[0])
        if 0 <= source < n:
            values[source] += 1
    return values


def _morans_i_xyz(
    coordinates: Sequence[Sequence[float]],
    values: Sequence[float],
) -> float | None:
    """Inverse-distance Moran's I over x/y/z, for descriptive diagnostics."""

    n = len(coordinates)
    if n < 3 or len(values) != n:
        return None
    mean = sum(values) / n
    denominator = sum((value - mean) ** 2 for value in values)
    if denominator <= 1e-12:
        return None

    weighted = 0.0
    weight_sum = 0.0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            spatial_sq = sum(
                (float(coordinates[i][axis]) - float(coordinates[j][axis])) ** 2
                for axis in range(3)
            )
            if spatial_sq <= 1e-12:
                continue
            weight = 1.0 / math.sqrt(spatial_sq)
            weight_sum += weight
            weighted += weight * (values[i] - mean) * (values[j] - mean)

    if weight_sum <= 0.0:
        return None
    return (n / weight_sum) * (weighted / denominator)


def geometry_diagnostics(
    coordinates: Sequence[Sequence[float]],
    edges: Sequence[Sequence[int]],
    *,
    lambda_a: float,
    lambda_b: float,
    radius: float,
    mode: str,
    delays: Mapping[tuple[int, int], int] | None = None,
    apoptosis_events: Sequence[Mapping[str, object]] | None = None,
    activity_values: Sequence[float] | None = None,
) -> dict[str, object]:
    """Describe geometry without quality scoring or scientific promotion."""

    n = len(coordinates)
    spatial_only = 0
    topological_only = 0
    both = 0
    neither = 0
    spatial_distances: list[float] = []
    topological_distances: list[float] = []
    mixed_distances: list[float] = []

    for edge in edges:
        if len(edge) < 2:
            continue
        source, target = int(edge[0]), int(edge[1])
        if not (0 <= source < n and 0 <= target < n):
            continue
        components = geometric_components(
            coordinates[source],
            coordinates[target],
            lambda_a=lambda_a,
            lambda_b=lambda_b,
        )
        spatial = components["spatial_distance"]
        topological = components["topological_distance"]
        spatial_distances.append(spatial)
        topological_distances.append(topological)
        mixed_distances.append(components["mixed_distance"])

        spatial_near = spatial <= radius
        topological_near = topological <= radius
        if spatial_near and topological_near:
            both += 1
        elif spatial_near:
            spatial_only += 1
        elif topological_near:
            topological_only += 1
        else:
            neither += 1

    degrees = _out_degree(n, edges)
    delay_values = list(delays.values()) if delays is not None else []

    apoptosis_positions: list[dict[str, object]] = []
    for event in apoptosis_events or ():
        neuron_id_raw = event.get("neuron_id")
        if isinstance(neuron_id_raw, int) and 0 <= neuron_id_raw < n:
            apoptosis_positions.append(
                {
                    "neuron_id": neuron_id_raw,
                    "position": [float(value) for value in coordinates[neuron_id_raw]],
                    "tick": event.get("tick"),
                }
            )

    def mean(values: Sequence[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    return {
        "classification": "PLAYGROUND_GEOMETRY",
        "scientific_evidence": False,
        "geometry_dimensions": 5,
        "axes": [
            {"name": "x", "type": "cartesian", "range": "[0,1]"},
            {"name": "y", "type": "cartesian", "range": "[0,1]"},
            {"name": "z", "type": "cartesian", "range": "[0,1]"},
            {"name": "a", "type": "cyclic_torus", "range": "[0,2pi)"},
            {"name": "b", "type": "cyclic_torus", "range": "[0,2pi)"},
        ],
        "topological_manifold": "torus_S1_x_S1",
        "klein_bottle_status": "NOT_IMPLEMENTED",
        "connection_mode": mode,
        "lambda_a": lambda_a,
        "lambda_b": lambda_b,
        "connection_radius": radius,
        "mean_out_degree": mean([float(value) for value in degrees]),
        "out_degree": degrees,
        "spatial_autocorrelation": {
            "metric": "morans_i_inverse_xyz_distance",
            "out_degree_morans_i": _morans_i_xyz(
                coordinates,
                [float(value) for value in degrees],
            ),
            "activity_morans_i": (
                _morans_i_xyz(coordinates, activity_values)
                if activity_values is not None
                else None
            ),
        },
        "edge_distances": {
            "mean_spatial_xyz": mean(spatial_distances),
            "mean_topological_ab": mean(topological_distances),
            "mean_additive_mixed": mean(mixed_distances),
        },
        "topological_vs_spatial_edges": {
            "spatial_only": spatial_only,
            "topological_only": topological_only,
            "both": both,
            "neither": neither,
            "topological_shortcut_fraction": (
                topological_only / max(len(spatial_distances), 1)
            ),
        },
        "delay_model": {
            "source": "xyz_euclidean_only",
            "topological_axes_affect_delay": False,
            "mean_delay_ticks": (
                mean([float(value) for value in delay_values])
                if delay_values
                else None
            ),
            "adm_status": "NOT_IMPLEMENTED",
        },
        "activity_dependent_positioning_status": "NOT_IMPLEMENTED",
        "pid_position_force_status": "NOT_IMPLEMENTED",
        "neurogenesis_status": "NOT_IMPLEMENTED",
        "neurogenesis_positions": [],
        "apoptosis_positions": apoptosis_positions,
        "interpretation": (
            "Descriptive geometry only; no claim that 5D, toroidal axes, "
            "or shortcut modes improve network quality."
        ),
    }
