"""Deterministic topology generators for the exploratory playground.

The module distinguishes three geometry classes:
- classical graph topologies,
- generic N-D geometry (1..32 dimensions),
- native MHRN 5D geometry using the canonical coordinate packing contract.

No topology is ranked or recommended by this module.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Sequence

from src.core.spatial_index import pack_coords

from ..models import Coordinate, Edge, Topology

Generator = Callable[..., Topology]


def _grid_coords(n: int, dims: int) -> tuple[Coordinate, ...]:
    side = max(2, math.ceil(n ** (1.0 / dims)))
    coords: list[Coordinate] = []
    for index in range(n):
        value = index
        point: list[float] = []
        for _ in range(dims):
            point.append(float(value % side) / float(max(side - 1, 1)))
            value //= side
        coords.append(tuple(point))
    return tuple(coords)


def _mhrn_coords(n: int) -> tuple[tuple[Coordinate, ...], tuple[int, ...]]:
    """Create canonical-style integer 5D coordinates and packed neuron IDs."""

    side = max(2, math.ceil(n ** (1.0 / 5.0)))
    coords: list[Coordinate] = []
    packed: list[int] = []
    for index in range(n):
        value = index
        raw: list[int] = []
        for _ in range(5):
            raw.append(value % side)
            value //= side
        x, y, z, d4, d5 = raw
        packed.append(pack_coords(x, y, z, d4, d5))
        denom = float(max(side - 1, 1))
        coords.append(tuple(component / denom for component in raw))
    return tuple(coords), tuple(packed)


def _distance(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _ring_edges(n: int) -> list[Edge]:
    return [(i, (i + 1) % n) for i in range(n)]


def _unique_random_edges(
    n: int, budget: int, rng: random.Random, initial: Sequence[Edge] | None = None
) -> tuple[Edge, ...]:
    edges = list(dict.fromkeys(initial or ()))
    seen = set(edges)
    max_edges = n * (n - 1)
    target = min(budget, max_edges)
    while len(edges) < target:
        source = rng.randrange(n)
        target_id = rng.randrange(n - 1)
        if target_id >= source:
            target_id += 1
        edge = (source, target_id)
        if edge in seen:
            continue
        seen.add(edge)
        edges.append(edge)
    return tuple(edges)


def _nearest_edges(
    coordinates: Sequence[Sequence[float]], budget: int, k: int
) -> tuple[Edge, ...]:
    n = len(coordinates)
    candidates: list[tuple[float, int, int]] = []
    for source in range(n):
        nearest = sorted(
            (
                (_distance(coordinates[source], coordinates[target]), target)
                for target in range(n)
                if target != source
            ),
            key=lambda item: item[0],
        )[:k]
        candidates.extend((dist, source, target) for dist, target in nearest)
    candidates.sort(key=lambda item: item[0])
    return tuple((source, target) for _, source, target in candidates[:budget])


def _distance_edges(
    coordinates: Sequence[Sequence[float]],
    budget: int,
    rng: random.Random,
    radius: float,
) -> tuple[Edge, ...]:
    candidates: list[tuple[float, int, int]] = []
    n = len(coordinates)
    for source in range(n):
        for target in range(n):
            if source == target:
                continue
            dist = _distance(coordinates[source], coordinates[target])
            if dist <= radius:
                candidates.append((dist, source, target))
    rng.shuffle(candidates)
    candidates.sort(key=lambda item: item[0])
    initial = [(source, target) for _, source, target in candidates[:budget]]
    return _unique_random_edges(n, budget, rng, initial)


def _base(
    name: str,
    dims: int,
    n: int,
    budget: int,
    seed: int,
    *,
    metadata: dict[str, object] | None = None,
) -> Topology:
    rng = random.Random(seed)
    coords = _grid_coords(n, dims)
    edges = _unique_random_edges(n, budget, rng, _ring_edges(n))
    return Topology(
        name=name,
        dimensions=dims,
        edges=edges,
        coordinates=coords,
        metadata={
            "seed": seed,
            "edge_budget": budget,
            "generator": name,
            "geometry_class": "generic",
            **(metadata or {}),
        },
    )


def ring_1d(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    coords = tuple((i / max(n - 1, 1),) for i in range(n))
    edges = _unique_random_edges(n, budget, rng, _ring_edges(n))
    return Topology(
        "1d_ring",
        1,
        edges,
        coords,
        {"seed": seed, "edge_budget": budget, "geometry_class": "classical"},
    )


def grid_2d(n: int, budget: int, seed: int, **_: object) -> Topology:
    return _base("2d_grid", 2, n, budget, seed)


def grid_3d(n: int, budget: int, seed: int, **_: object) -> Topology:
    return _base("3d_grid", 3, n, budget, seed)


def generic_nd(
    n: int, budget: int, seed: int, *, dimensions: int = 5, **_: object
) -> Topology:
    return _base(
        "generic_nd",
        dimensions,
        n,
        budget,
        seed,
        metadata={"requested_dimensions": dimensions},
    )


def generic_nd_distance(
    n: int,
    budget: int,
    seed: int,
    *,
    dimensions: int = 5,
    radius: float = 0.35,
    **_: object,
) -> Topology:
    coords = _grid_coords(n, dimensions)
    rng = random.Random(seed)
    return Topology(
        "generic_nd_distance",
        dimensions,
        _distance_edges(coords, budget, rng, radius),
        coords,
        {
            "seed": seed,
            "edge_budget": budget,
            "radius": radius,
            "geometry_class": "generic_nd",
        },
    )


def generic_nd_knn(
    n: int,
    budget: int,
    seed: int,
    *,
    dimensions: int = 5,
    k_neighbors: int = 8,
    **_: object,
) -> Topology:
    coords = _grid_coords(n, dimensions)
    return Topology(
        "generic_nd_knn",
        dimensions,
        _nearest_edges(coords, budget, k_neighbors),
        coords,
        {
            "seed": seed,
            "edge_budget": budget,
            "k_neighbors": k_neighbors,
            "geometry_class": "generic_nd",
        },
    )


def mhrn_experimental_nd(
    n: int,
    budget: int,
    seed: int,
    *,
    dimensions: int = 6,
    **_: object,
) -> Topology:
    """Experimental >5D extension of MHRN coordinate semantics.

    This deliberately does not reuse the canonical 5D packed integer ID.
    Coordinates remain explicit tuples until a versioned N-D storage/ID
    contract exists.
    """

    if dimensions <= 5:
        raise ValueError("mhrn_experimental_nd requires dimensions > 5")
    topology = _base(
        "mhrn_experimental_nd",
        dimensions,
        n,
        budget,
        seed,
        metadata={
            "geometry_class": "mhrn_experimental_nd",
            "coordinate_semantics": [
                "x",
                "y",
                "z",
                "d4",
                "d5",
                *[f"d{index}" for index in range(6, dimensions + 1)],
            ],
            "canonical_packed_id": False,
            "packing_contract": "explicit_tuple_only",
            "note": (
                "Experimental extension of MHRN geometry beyond 5D; "
                "not the canonical Brain5D storage representation."
            ),
        },
    )
    return topology


def mhrn_experimental_nd_distance(
    n: int,
    budget: int,
    seed: int,
    *,
    dimensions: int = 6,
    radius: float = 0.35,
    **_: object,
) -> Topology:
    if dimensions <= 5:
        raise ValueError("mhrn_experimental_nd_distance requires dimensions > 5")
    coords = _grid_coords(n, dimensions)
    rng = random.Random(seed)
    return Topology(
        "mhrn_experimental_nd_distance",
        dimensions,
        _distance_edges(coords, budget, rng, radius),
        coords,
        {
            "seed": seed,
            "edge_budget": budget,
            "radius": radius,
            "geometry_class": "mhrn_experimental_nd",
            "canonical_packed_id": False,
            "packing_contract": "explicit_tuple_only",
        },
    )


def mhrn_experimental_nd_neighbourhood(
    n: int,
    budget: int,
    seed: int,
    *,
    dimensions: int = 6,
    k_neighbors: int = 8,
    **_: object,
) -> Topology:
    if dimensions <= 5:
        raise ValueError("mhrn_experimental_nd_neighbourhood requires dimensions > 5")
    coords = _grid_coords(n, dimensions)
    return Topology(
        "mhrn_experimental_nd_neighbourhood",
        dimensions,
        _nearest_edges(coords, budget, k_neighbors),
        coords,
        {
            "seed": seed,
            "edge_budget": budget,
            "k_neighbors": k_neighbors,
            "geometry_class": "mhrn_experimental_nd",
            "canonical_packed_id": False,
            "packing_contract": "explicit_tuple_only",
        },
    )


def mhrn_5d(n: int, budget: int, seed: int, **_: object) -> Topology:
    coords, packed = _mhrn_coords(n)
    rng = random.Random(seed)
    edges = _unique_random_edges(n, budget, rng, _ring_edges(n))
    return Topology(
        "mhrn_5d",
        5,
        edges,
        coords,
        {
            "seed": seed,
            "edge_budget": budget,
            "geometry_class": "mhrn_native_5d",
            "coordinate_semantics": ["x", "y", "z", "d4", "d5"],
            "packed_neuron_ids": list(packed),
            "packing_contract": "src.core.spatial_index.pack_coords",
        },
    )


def mhrn_5d_distance(
    n: int,
    budget: int,
    seed: int,
    *,
    radius: float = 0.35,
    **_: object,
) -> Topology:
    coords, packed = _mhrn_coords(n)
    rng = random.Random(seed)
    return Topology(
        "mhrn_5d_distance",
        5,
        _distance_edges(coords, budget, rng, radius),
        coords,
        {
            "seed": seed,
            "edge_budget": budget,
            "radius": radius,
            "geometry_class": "mhrn_native_5d",
            "coordinate_semantics": ["x", "y", "z", "d4", "d5"],
            "packed_neuron_ids": list(packed),
        },
    )


def mhrn_5d_neighbourhood(
    n: int,
    budget: int,
    seed: int,
    *,
    k_neighbors: int = 8,
    **_: object,
) -> Topology:
    coords, packed = _mhrn_coords(n)
    return Topology(
        "mhrn_5d_neighbourhood",
        5,
        _nearest_edges(coords, budget, k_neighbors),
        coords,
        {
            "seed": seed,
            "edge_budget": budget,
            "k_neighbors": k_neighbors,
            "geometry_class": "mhrn_native_5d",
            "coordinate_semantics": ["x", "y", "z", "d4", "d5"],
            "packed_neuron_ids": list(packed),
        },
    )


def shuffled_5d(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    topology = mhrn_5d(n, budget, seed)
    coords = list(topology.coordinates)
    rng.shuffle(coords)
    return Topology(
        "5d_shuffled",
        5,
        topology.edges,
        tuple(coords),
        {**topology.metadata, "geometry_class": "control", "shuffled": True},
    )


def random_sparse(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    return Topology(
        "random_graph",
        2,
        _unique_random_edges(n, budget, rng),
        _grid_coords(n, 2),
        {"seed": seed, "edge_budget": budget, "geometry_class": "classical"},
    )


def dense(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    all_edges = [(a, b) for a in range(n) for b in range(n) if a != b]
    rng.shuffle(all_edges)
    return Topology(
        "dense",
        2,
        tuple(all_edges[:budget]),
        _grid_coords(n, 2),
        {"seed": seed, "edge_budget": budget, "geometry_class": "classical"},
    )


def feedforward(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    thirds = (max(1, n // 4), max(2, 3 * n // 4))
    input_end, hidden_end = thirds
    candidates = [
        (source, target)
        for source in range(n)
        for target in range(n)
        if (
            (source < input_end <= target < hidden_end)
            or (input_end <= source < hidden_end <= target)
        )
    ]
    rng.shuffle(candidates)
    return Topology(
        "feedforward",
        2,
        tuple(candidates[:budget]),
        _grid_coords(n, 2),
        {"seed": seed, "edge_budget": budget, "acyclic": True},
    )


def input_hidden_output(n: int, budget: int, seed: int, **kwargs: object) -> Topology:
    topology = feedforward(n, budget, seed, **kwargs)
    return Topology(
        "input_hidden_output",
        topology.dimensions,
        topology.edges,
        topology.coordinates,
        {
            **topology.metadata,
            "layers": ["input", "hidden", "output"],
        },
    )


def recurrent(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    motif = _ring_edges(n) + [((i + 1) % n, i) for i in range(n)]
    return Topology(
        "recurrent",
        2,
        _unique_random_edges(n, budget, rng, motif),
        _grid_coords(n, 2),
        {"seed": seed, "edge_budget": budget, "recurrent": True},
    )


def reservoir(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    edges = _unique_random_edges(n, budget, rng)
    return Topology(
        "reservoir",
        3,
        edges,
        _grid_coords(n, 3),
        {
            "seed": seed,
            "edge_budget": budget,
            "recurrent": True,
            "readout_intent": "reservoir/liquid-state exploration",
        },
    )


def bipartite(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    split = max(1, n // 2)
    candidates = [(a, b) for a in range(split) for b in range(split, n)] + [
        (b, a) for a in range(split) for b in range(split, n)
    ]
    rng.shuffle(candidates)
    return Topology(
        "bipartite",
        2,
        tuple(candidates[:budget]),
        _grid_coords(n, 2),
        {"seed": seed, "edge_budget": budget, "partitions": [split, n - split]},
    )


def small_world(
    n: int,
    budget: int,
    seed: int,
    *,
    rewiring_probability: float = 0.15,
    **_: object,
) -> Topology:
    rng = random.Random(seed)
    k = max(2, min(n - 1, budget // n))
    if k % 2:
        k -= 1
    edges: list[Edge] = []
    for source in range(n):
        for offset in range(1, k // 2 + 1):
            edges.append((source, (source + offset) % n))
    rewired: list[Edge] = []
    for edge in edges:
        if rng.random() < rewiring_probability:
            target = rng.randrange(n - 1)
            if target >= edge[0]:
                target += 1
            rewired.append((edge[0], target))
        else:
            rewired.append(edge)
    final_edges = _unique_random_edges(n, budget, rng, rewired[:budget])
    return Topology(
        "small_world",
        2,
        final_edges,
        _grid_coords(n, 2),
        {
            "seed": seed,
            "rewiring_probability": rewiring_probability,
            "edge_budget": budget,
        },
    )


def scale_free(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    edges = _ring_edges(n)
    seen = set(edges)
    degree = [2 for _ in range(n)]
    while len(edges) < budget:
        source = rng.randrange(n)
        total = sum(degree)
        pick = rng.uniform(0.0, float(total))
        acc = 0.0
        target = 0
        for idx, value in enumerate(degree):
            acc += value
            if acc >= pick:
                target = idx
                break
        edge = (source, target)
        if source == target or edge in seen:
            continue
        seen.add(edge)
        edges.append(edge)
        degree[source] += 1
        degree[target] += 1
    return Topology(
        "scale_free",
        2,
        tuple(edges[:budget]),
        _grid_coords(n, 2),
        {"seed": seed, "edge_budget": budget, "attachment": "degree_weighted"},
    )


def modular(
    n: int,
    budget: int,
    seed: int,
    *,
    modules: int = 4,
    dimensions: int = 2,
    recurrent_mode: bool = False,
    **_: object,
) -> Topology:
    rng = random.Random(seed)
    modules = max(1, min(modules, n))
    edges: list[Edge] = []
    seen: set[Edge] = set()
    while len(edges) < budget:
        source = rng.randrange(n)
        source_module = source % modules
        if rng.random() < 0.82:
            candidates = [
                i for i in range(n) if i != source and i % modules == source_module
            ]
        else:
            candidates = [
                i for i in range(n) if i != source and i % modules != source_module
            ]
        if not candidates:
            continue
        target = rng.choice(candidates)
        edge = (source, target)
        if edge in seen:
            continue
        seen.add(edge)
        edges.append(edge)
        if recurrent_mode and len(edges) < budget:
            reverse = (target, source)
            if reverse not in seen:
                seen.add(reverse)
                edges.append(reverse)
    return Topology(
        "recurrent_modular" if recurrent_mode else "modular",
        dimensions,
        tuple(edges[:budget]),
        _grid_coords(n, dimensions),
        {
            "seed": seed,
            "edge_budget": budget,
            "modules": modules,
            "recurrent": recurrent_mode,
        },
    )


def recurrent_modular(n: int, budget: int, seed: int, **kwargs: object) -> Topology:
    modules_value = kwargs.get("modules", 4)
    dimensions_value = kwargs.get("dimensions", 2)
    modules = modules_value if isinstance(modules_value, int) else 4
    dimensions = dimensions_value if isinstance(dimensions_value, int) else 2
    return modular(
        n,
        budget,
        seed,
        modules=modules,
        dimensions=dimensions,
        recurrent_mode=True,
    )


def recurrent_small_world(n: int, budget: int, seed: int, **kwargs: object) -> Topology:
    rewiring_value = kwargs.get("rewiring_probability", 0.15)
    rewiring_probability = (
        float(rewiring_value)
        if isinstance(rewiring_value, (int, float))
        and not isinstance(rewiring_value, bool)
        else 0.15
    )
    topology = small_world(
        n,
        budget,
        seed,
        rewiring_probability=rewiring_probability,
    )
    reverse = [(b, a) for a, b in topology.edges]
    rng = random.Random(seed ^ 0xA11CE)
    edges = _unique_random_edges(
        n,
        budget,
        rng,
        list(topology.edges[: budget // 2]) + reverse[: budget // 2],
    )
    return Topology(
        "recurrent_small_world",
        topology.dimensions,
        edges,
        topology.coordinates,
        {**topology.metadata, "recurrent": True},
    )


def hierarchical(n: int, budget: int, seed: int, **_: object) -> Topology:
    rng = random.Random(seed)
    edges = [((child - 1) // 2, child) for child in range(1, n)]
    return Topology(
        "hierarchical",
        2,
        _unique_random_edges(n, budget, rng, edges[:budget]),
        _grid_coords(n, 2),
        {"seed": seed, "edge_budget": budget, "branching_factor": 2},
    )


TOPOLOGY_REGISTRY: dict[str, Generator] = {
    "1d_ring": ring_1d,
    "2d_grid": grid_2d,
    "3d_grid": grid_3d,
    "generic_nd": generic_nd,
    "generic_nd_distance": generic_nd_distance,
    "generic_nd_knn": generic_nd_knn,
    "mhrn_experimental_nd": mhrn_experimental_nd,
    "mhrn_experimental_nd_distance": mhrn_experimental_nd_distance,
    "mhrn_experimental_nd_neighbourhood": mhrn_experimental_nd_neighbourhood,
    "mhrn_5d": mhrn_5d,
    "mhrn_5d_distance": mhrn_5d_distance,
    "mhrn_5d_neighbourhood": mhrn_5d_neighbourhood,
    "5d_shuffled": shuffled_5d,
    "random_graph": random_sparse,
    "dense": dense,
    "feedforward": feedforward,
    "input_hidden_output": input_hidden_output,
    "recurrent": recurrent,
    "reservoir": reservoir,
    "bipartite": bipartite,
    "small_world": small_world,
    "scale_free": scale_free,
    "modular": modular,
    "recurrent_modular": recurrent_modular,
    "recurrent_small_world": recurrent_small_world,
    "hierarchical": hierarchical,
}


def build_topology(
    name: str,
    n: int,
    budget: int,
    seed: int,
    *,
    dimensions: int = 5,
    radius: float = 0.35,
    k_neighbors: int = 8,
    rewiring_probability: float = 0.15,
    modules: int = 4,
) -> Topology:
    try:
        generator = TOPOLOGY_REGISTRY[name]
    except KeyError as exc:
        raise ValueError(f"unknown playground topology: {name}") from exc
    return generator(
        n,
        budget,
        seed,
        dimensions=dimensions,
        radius=radius,
        k_neighbors=k_neighbors,
        rewiring_probability=rewiring_probability,
        modules=modules,
    )
