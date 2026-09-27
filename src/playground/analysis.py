"""Descriptive analysis for non-canonical Playground sessions.

All metrics are exploratory diagnostics. They are not scientific evidence,
do not enter the research registry, and never contribute to maturity.
"""

from __future__ import annotations

import math
from collections import Counter, deque
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np

from .instruments.probes_nd import dimension_utilization, occupancy_nd


def _mean(values: Sequence[float]) -> float:
    return float(sum(values) / len(values)) if values else 0.0


def _std(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = _mean(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def _spike_trains(
    spikes: Sequence[Mapping[str, int]], n_neurons: int
) -> list[list[int]]:
    trains: list[list[int]] = [[] for _ in range(n_neurons)]
    for spike in spikes:
        neuron_id = int(spike.get("neuron_id", -1))
        tick = int(spike.get("tick", -1))
        if 0 <= neuron_id < n_neurons and tick >= 0:
            trains[neuron_id].append(tick)
    return trains


def _isi_metrics(trains: Sequence[Sequence[int]], dt_ms: float) -> dict[str, object]:
    isi: list[float] = []
    neuron_cv: list[float] = []
    burst_count = 0
    for train in trains:
        local = [
            (train[index] - train[index - 1]) * dt_ms for index in range(1, len(train))
        ]
        isi.extend(local)
        if len(local) >= 2:
            mean = _mean(local)
            if mean > 0:
                neuron_cv.append(_std(local) / mean)
        burst_count += sum(1 for value in local if value <= 10.0)
    return {
        "isi_mean_ms": _mean(isi),
        "isi_std_ms": _std(isi),
        "isi_cv_mean": _mean(neuron_cv),
        "burst_interval_count": burst_count,
        "burst_fraction": burst_count / max(len(isi), 1),
    }


def _latency_metrics(
    trains: Sequence[Sequence[int]], ticks: int, dt_ms: float
) -> dict[str, object]:
    first = [train[0] for train in trains if train]
    last = [train[-1] for train in trains if train]
    return {
        "first_spike_latency_ms": min(first, default=ticks) * dt_ms,
        "median_first_spike_latency_ms": (
            float(np.median(first)) * dt_ms if first else None
        ),
        "last_spike_ms": max(last, default=-1) * dt_ms if last else None,
        "persistence_fraction": (
            max(last, default=-1) / max(ticks - 1, 1) if last else 0.0
        ),
        "propagation_depth_proxy": len({tick for train in trains for tick in train}),
        "recurrently_active_neurons": sum(1 for train in trains if len(train) >= 2),
    }


def _population_dynamics(
    tick_counts: Sequence[int], n_neurons: int, dt_ms: float
) -> dict[str, object]:
    if not tick_counts:
        return {
            "synchrony_index": 0.0,
            "population_fano": 0.0,
            "dominant_frequency_hz": 0.0,
            "spectral_power": [],
        }
    values = np.asarray(tick_counts, dtype=float)
    mean = float(values.mean())
    variance = float(values.var())
    synchrony = float(values.max() / max(n_neurons, 1))
    centered = values - mean
    frequencies = np.fft.rfftfreq(len(values), d=dt_ms / 1000.0)
    spectrum = np.abs(np.fft.rfft(centered)) ** 2
    if len(spectrum) > 1:
        index = int(np.argmax(spectrum[1:]) + 1)
        dominant = float(frequencies[index])
    else:
        dominant = 0.0
    sample = [
        {"hz": float(frequencies[index]), "power": float(spectrum[index])}
        for index in range(min(len(spectrum), 128))
    ]
    return {
        "synchrony_index": synchrony,
        "population_fano": variance / mean if mean > 0 else 0.0,
        "dominant_frequency_hz": dominant,
        "spectral_power": sample,
    }


def _adjacency(
    n: int, edges: Sequence[Sequence[int]]
) -> tuple[list[set[int]], list[set[int]]]:
    outgoing: list[set[int]] = [set() for _ in range(n)]
    incoming: list[set[int]] = [set() for _ in range(n)]
    for edge in edges:
        if len(edge) < 2:
            continue
        source, target = int(edge[0]), int(edge[1])
        if 0 <= source < n and 0 <= target < n and source != target:
            outgoing[source].add(target)
            incoming[target].add(source)
    return outgoing, incoming


def _components(outgoing: Sequence[set[int]]) -> list[int]:
    undirected = [set(values) for values in outgoing]
    for source, targets in enumerate(outgoing):
        for target in targets:
            undirected[target].add(source)
    seen: set[int] = set()
    sizes: list[int] = []
    for node in range(len(undirected)):
        if node in seen:
            continue
        queue = [node]
        seen.add(node)
        size = 0
        while queue:
            current = queue.pop()
            size += 1
            for target in undirected[current]:
                if target not in seen:
                    seen.add(target)
                    queue.append(target)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def _clustering(outgoing: Sequence[set[int]]) -> float:
    values: list[float] = []
    for node, neighbours in enumerate(outgoing):
        neighbours = set(neighbours)
        for source, targets in enumerate(outgoing):
            if node in targets:
                neighbours.add(source)
        degree = len(neighbours)
        if degree < 2:
            continue
        links = 0
        ordered = list(neighbours)
        for index, left in enumerate(ordered):
            for right in ordered[index + 1 :]:
                if right in outgoing[left] or left in outgoing[right]:
                    links += 1
        values.append((2.0 * links) / (degree * (degree - 1)))
    return _mean(values)


def _mean_path(outgoing: Sequence[set[int]], sample_limit: int = 64) -> float:
    n = len(outgoing)
    if n < 2:
        return 0.0
    sources = list(range(min(n, sample_limit)))
    distances: list[int] = []
    for source in sources:
        queue: deque[tuple[int, int]] = deque([(source, 0)])
        seen = {source}
        while queue:
            node, depth = queue.popleft()
            for target in outgoing[node]:
                if target in seen:
                    continue
                seen.add(target)
                distances.append(depth + 1)
                queue.append((target, depth + 1))
    return _mean([float(value) for value in distances])


def _cycle_proxy(outgoing: Sequence[set[int]]) -> dict[str, object]:
    reciprocal = 0
    for source, targets in enumerate(outgoing):
        reciprocal += sum(1 for target in targets if source in outgoing[target])
    reciprocal //= 2
    self_return_3 = 0
    for source, targets in enumerate(outgoing):
        for middle in targets:
            for end in outgoing[middle]:
                if source in outgoing[end]:
                    self_return_3 += 1
    return {
        "reciprocal_pairs": reciprocal,
        "three_cycle_count_proxy": self_return_3 // 3,
    }


def _topology_metrics(
    coordinates: Sequence[Sequence[float]],
    edges: Sequence[Sequence[int]],
    modules: int,
) -> dict[str, object]:
    n = len(coordinates)
    outgoing, incoming = _adjacency(n, edges)
    in_degree = [len(values) for values in incoming]
    out_degree = [len(values) for values in outgoing]
    components = _components(outgoing)
    distances = [
        math.sqrt(
            sum(
                (float(coordinates[source][axis]) - float(coordinates[target][axis]))
                ** 2
                for axis in range(
                    min(len(coordinates[source]), len(coordinates[target]))
                )
            )
        )
        for source, target in (
            (int(edge[0]), int(edge[1])) for edge in edges if len(edge) >= 2
        )
        if 0 <= source < n and 0 <= target < n
    ]
    internal = 0
    valid_edges = 0
    for edge in edges:
        if len(edge) < 2:
            continue
        source, target = int(edge[0]), int(edge[1])
        if 0 <= source < n and 0 <= target < n:
            valid_edges += 1
            if source % max(modules, 1) == target % max(modules, 1):
                internal += 1
    hub_threshold = _mean([float(value) for value in out_degree]) + 2.0 * _std(
        [float(value) for value in out_degree]
    )
    return {
        "in_degree": in_degree,
        "out_degree": out_degree,
        "degree_histogram": dict(Counter(in_degree + out_degree)),
        "mean_in_degree": _mean([float(value) for value in in_degree]),
        "mean_out_degree": _mean([float(value) for value in out_degree]),
        "max_in_degree": max(in_degree, default=0),
        "max_out_degree": max(out_degree, default=0),
        "hub_neurons": [
            index for index, value in enumerate(out_degree) if value >= hub_threshold
        ],
        "clustering_coefficient": _clustering(outgoing),
        "mean_path_length": _mean_path(outgoing),
        "connected_components": components,
        "largest_component_fraction": (
            components[0] / max(n, 1) if components else 0.0
        ),
        "module_internal_edge_fraction": internal / max(valid_edges, 1),
        "edge_distance_mean": _mean(distances),
        "edge_distance_std": _std(distances),
        "edge_distance_min": min(distances, default=0.0),
        "edge_distance_max": max(distances, default=0.0),
        **_cycle_proxy(outgoing),
    }


def _dimensionality(
    coordinates: Sequence[Sequence[float]],
) -> dict[str, object]:
    if not coordinates:
        return {
            "coordinate_dimensions": 0,
            "pca_explained_variance_ratio": [],
            "effective_dimensionality": 0.0,
            "participation_ratio": 0.0,
            "dimension_variance": [],
        }
    width = max(len(point) for point in coordinates)
    matrix = np.zeros((len(coordinates), width), dtype=float)
    for row, point in enumerate(coordinates):
        matrix[row, : len(point)] = [float(value) for value in point]
    variances = np.var(matrix, axis=0)
    centered = matrix - matrix.mean(axis=0, keepdims=True)
    if len(coordinates) > 1:
        singular = np.linalg.svd(centered, full_matrices=False, compute_uv=False)
        eigen = singular**2
    else:
        eigen = np.zeros(width, dtype=float)
    total = float(eigen.sum())
    ratios = (eigen / total).tolist() if total > 0 else [0.0] * len(eigen)
    denom = float(np.sum(eigen**2))
    participation = (total * total / denom) if denom > 0 else 0.0
    return {
        "coordinate_dimensions": width,
        "pca_explained_variance_ratio": [float(value) for value in ratios],
        "effective_dimensionality": float(participation),
        "participation_ratio": float(participation),
        "dimension_variance": [float(value) for value in variances],
        "dimension_utilization": dimension_utilization(coordinates),
        "occupancy": {
            "bins_per_dimension": 4,
            "occupied_cells": len(occupancy_nd(coordinates, bins=4)),
            "distribution": occupancy_nd(coordinates, bins=4),
            "interpretation": (
                "Structural distribution only; no quality or superiority score."
            ),
        },
    }


def analyze_result(
    result: Mapping[str, object],
    *,
    initial_weight: float,
    final_weights: Sequence[float],
    initial_edge_count: int,
    final_edge_count: int,
    structural_added: int = 0,
    structural_removed: int = 0,
    runtime_seconds: float = 0.0,
) -> dict[str, object]:
    config = result.get("config", {})
    topology = result.get("topology", {})
    monitors = result.get("monitors", {})
    if not isinstance(config, Mapping):
        config = {}
    if not isinstance(topology, Mapping):
        topology = {}
    if not isinstance(monitors, Mapping):
        monitors = {}
    n = int(config.get("n_neurons", 0))
    ticks = int(config.get("ticks", 0))
    dt_ms = float(config.get("dt_ms", 1.0))
    spikes_raw = monitors.get("spikes", [])
    spikes = (
        [item for item in spikes_raw if isinstance(item, Mapping)]
        if isinstance(spikes_raw, Sequence)
        else []
    )
    tick_counts_raw = monitors.get("tick_spike_counts", [])
    tick_counts = (
        [int(value) for value in tick_counts_raw]
        if isinstance(tick_counts_raw, Sequence)
        else []
    )
    trains = _spike_trains(spikes, n)
    coordinates_raw = topology.get("coordinates", [])
    coordinates = (
        [item for item in coordinates_raw if isinstance(item, Sequence)]
        if isinstance(coordinates_raw, Sequence)
        else []
    )
    edges_raw = topology.get("edges", [])
    edges = (
        [item for item in edges_raw if isinstance(item, Sequence)]
        if isinstance(edges_raw, Sequence)
        else []
    )
    weights = [float(value) for value in final_weights]
    changed = [value - initial_weight for value in weights]
    saturation = sum(1 for value in weights if value <= 1e-12 or value >= 100.0 - 1e-12)
    total_spikes = len(spikes)
    duration_s = max(ticks * dt_ms / 1000.0, 1e-9)
    return {
        "classification": {
            "class": "PLAYGROUND",
            "scientific_evidence": False,
            "interpretation": "descriptive_exploration_only",
        },
        "spike_time": {
            **_isi_metrics(trains, dt_ms),
            **_latency_metrics(trains, ticks, dt_ms),
            **_population_dynamics(tick_counts, n, dt_ms),
        },
        "network": _topology_metrics(
            coordinates,
            edges,
            int(config.get("modules", 1)),
        ),
        "plasticity": {
            "weight_change_mean": _mean(changed),
            "weight_change_std": _std(changed),
            "weight_min": min(weights, default=0.0),
            "weight_max": max(weights, default=0.0),
            "potentiated_fraction": (
                sum(1 for value in changed if value > 1e-12) / max(len(changed), 1)
            ),
            "depressed_fraction": (
                sum(1 for value in changed if value < -1e-12) / max(len(changed), 1)
            ),
            "weight_saturation_fraction": saturation / max(len(weights), 1),
            "initial_edge_count": initial_edge_count,
            "final_edge_count": final_edge_count,
            "structural_edges_added": structural_added,
            "structural_edges_removed": structural_removed,
        },
        "dimensionality": _dimensionality(coordinates),
        "performance": {
            "runtime_seconds": runtime_seconds,
            "simulated_seconds": duration_s,
            "neuron_updates_per_second": (
                n * ticks / runtime_seconds if runtime_seconds > 0 else None
            ),
            "spikes_per_runtime_second": (
                total_spikes / runtime_seconds if runtime_seconds > 0 else None
            ),
            "synaptic_edges": final_edge_count,
        },
    }


def ensemble_summary(results: Sequence[Mapping[str, object]]) -> dict[str, object]:
    if not results:
        return {"runs": 0}
    mean_rates: list[float] = []
    active: list[float] = []
    spikes: list[float] = []
    for result in results:
        metrics = result.get("metrics", {})
        if not isinstance(metrics, Mapping):
            continue
        mean_rates.append(float(metrics.get("mean_rate_hz", 0.0)))
        active.append(float(metrics.get("active_fraction", 0.0)))
        spikes.append(float(metrics.get("total_spikes", 0.0)))
    return {
        "runs": len(results),
        "seed_to_seed": {
            "mean_rate_hz_mean": _mean(mean_rates),
            "mean_rate_hz_std": _std(mean_rates),
            "active_fraction_mean": _mean(active),
            "active_fraction_std": _std(active),
            "total_spikes_mean": _mean(spikes),
            "total_spikes_std": _std(spikes),
        },
        "note": "Exploratory robustness summary; not a preregistered replication.",
    }
