"""Benchmark bounded plastic-network stability and throughput.

The deterministic regular graph is an engineering load profile, not a
scientific workload or evidence of general plastic-network stability.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import random
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

BYTES_PER_NEURON_ESTIMATE = 4_096
BYTES_PER_SYNAPSE_ESTIMATE = 2_048
DEFAULT_MEMORY_BUDGET_BYTES = 2 * 1024**3
STAGE3_NEURON_RANGE = (10_000, 100_000)
STAGE3_SYNAPSE_RANGE = (100_000, 10_000_000)
INITIAL_WEIGHT = 0.05
MIN_WEIGHT = 0.0
MAX_WEIGHT = 0.5
SOURCE_CURRENT = 100.0
REWARD_VALUE = 1.0
STDP_A_PLUS = 0.1
STDP_A_MINUS = 0.12
STDP_TAU_TICKS = 20.0
ELIGIBILITY_TAU_TICKS = 200.0
REWARD_LEARNING_RATE = 0.01
PLASTICITY_MODES = {"asymmetric", "symmetric", "off"}
ACTIVITY_PROFILES = {"uniform", "heterogeneous_cohorts"}
COHORT_COUNT = 4
WEIGHT_VARIANCE_TOLERANCE = 1e-12


def estimate_peak_bytes(neuron_count: int, synapse_count: int) -> int:
    """Conservatively estimate Python object-graph memory before allocation."""
    return (
        neuron_count * BYTES_PER_NEURON_ESTIMATE
        + synapse_count * BYTES_PER_SYNAPSE_ESTIMATE
    )


def _build_network(
    neuron_count: int, synapse_count: int, seed: int
) -> tuple[Any, list[int], list[int]]:
    from src.core.network import Brain5DConfig, NeuralNetwork
    from src.core.spatial_index import linear_to_5d

    side = math.ceil(neuron_count ** (1.0 / 5.0))
    while side**5 < neuron_count:
        side += 1
    dimensions = (side, side, side, side, side)
    config = Brain5DConfig.from_dict(
        {
            "dimensions": dimensions,
            "simulation": {"max_delay": 1},
            "network": {
                "initial_connections_per_neuron": 0,
                "weight_min": MIN_WEIGHT,
                "weight_max": MAX_WEIGHT,
            },
            "stdp": {
                "a_plus": STDP_A_PLUS,
                "a_minus": STDP_A_MINUS,
                "tau_plus": STDP_TAU_TICKS,
                "tau_minus": STDP_TAU_TICKS,
            },
        }
    )
    network = NeuralNetwork(config, random.Random(seed))
    neuron_ids = [
        network.add_neuron(linear_to_5d(index, dimensions))
        for index in range(neuron_count)
    ]
    source_count = neuron_count // 2
    source_ids = neuron_ids[:source_count]
    target_ids = neuron_ids[source_count:]
    random.Random(seed).shuffle(target_ids)
    if not source_ids or not target_ids:
        raise ValueError("at least two neurons are required")
    if synapse_count % source_count:
        raise ValueError("synapse_count must be divisible by the source population")
    degree = synapse_count // source_count
    if degree > len(target_ids):
        raise ValueError("synapse_count would create duplicate source-target edges")

    for source_index, source_id in enumerate(source_ids):
        first_target = source_index * degree
        for edge_index in range(degree):
            target_id = target_ids[(first_target + edge_index) % len(target_ids)]
            network.connect(source_id, target_id, weight=INITIAL_WEIGHT, delay=1)
    return network, source_ids, target_ids


def _weight_snapshot(network: Any, epoch: int) -> dict[str, Any]:
    weights = [
        synapse.weight for outgoing in network.synapses.values() for synapse in outgoing
    ]
    finite = all(math.isfinite(weight) for weight in weights)
    mean_weight = sum(weights) / len(weights) if weights else None
    variance = (
        sum((weight - mean_weight) ** 2 for weight in weights) / len(weights)
        if weights and mean_weight is not None
        else None
    )
    active_count = sum(weight > MIN_WEIGHT + 1e-12 for weight in weights)
    return {
        "epoch": epoch,
        "finite_weights": finite,
        "min_weight": min(weights, default=None),
        "max_weight": max(weights, default=None),
        "mean_weight": mean_weight,
        "weight_variance": variance,
        "active_weight_count": active_count,
        "active_weight_fraction": active_count / len(weights) if weights else None,
        "all_weights_equal": variance is not None
        and variance <= WEIGHT_VARIANCE_TOLERANCE,
        "at_lower_bound_count": sum(weight <= MIN_WEIGHT + 1e-12 for weight in weights),
        "at_upper_bound_count": sum(weight >= MAX_WEIGHT - 1e-12 for weight in weights),
        "out_of_bounds_weights": sum(
            weight < MIN_WEIGHT or weight > MAX_WEIGHT for weight in weights
        ),
    }


def _topology_digest(network: Any) -> str:
    edges = sorted(
        (source_id, synapse.target_id)
        for source_id, outgoing in network.synapses.items()
        for synapse in outgoing
    )
    payload = json.dumps(edges, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def _benchmark_source_digest() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def assess_stability(
    snapshots: list[dict[str, Any]],
    *,
    final_epoch_source_spikes: int,
    final_epoch_target_spikes: int,
    weight_diversity_required: bool,
) -> dict[str, bool]:
    final_snapshot = snapshots[-1]
    numeric_passed = all(
        bool(snapshot["finite_weights"]) and int(snapshot["out_of_bounds_weights"]) == 0
        for snapshot in snapshots
    )
    active_weight_fraction = float(final_snapshot["active_weight_fraction"] or 0.0)
    functional_passed = (
        final_epoch_source_spikes > 0
        and final_epoch_target_spikes > 0
        and active_weight_fraction > 0.0
    )
    final_variance = final_snapshot["weight_variance"]
    diversity_passed = not weight_diversity_required or (
        final_variance is not None and float(final_variance) > WEIGHT_VARIANCE_TOLERANCE
    )
    return {
        "numeric_stability_passed": numeric_passed,
        "functional_activity_passed": functional_passed,
        "weight_diversity_passed": diversity_passed,
        "stability_invariants_passed": (
            numeric_passed and functional_passed and diversity_passed
        ),
    }


def run_benchmark(
    *,
    neuron_count: int = 10_000,
    synapse_count: int = 100_000,
    epochs: int = 100,
    seed: int = 42,
    memory_budget_bytes: int = DEFAULT_MEMORY_BUDGET_BYTES,
    stability_interval: int = 10,
    plasticity_mode: str = "asymmetric",
    activity_profile: str = "heterogeneous_cohorts",
) -> dict[str, Any]:
    """Run repeated causal spike/reward phases and report engineering metrics."""
    if neuron_count < 4 or neuron_count % 2:
        raise ValueError("neuron_count must be an even integer >= 4")
    if synapse_count <= 0 or epochs <= 0 or stability_interval <= 0:
        raise ValueError(
            "synapse_count, epochs and stability_interval must be positive"
        )
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    if plasticity_mode not in PLASTICITY_MODES:
        raise ValueError(f"plasticity_mode must be one of {sorted(PLASTICITY_MODES)}")
    if activity_profile not in ACTIVITY_PROFILES:
        raise ValueError(f"activity_profile must be one of {sorted(ACTIVITY_PROFILES)}")
    estimated_bytes = estimate_peak_bytes(neuron_count, synapse_count)
    if estimated_bytes > memory_budget_bytes:
        raise ValueError(
            f"estimated allocation {estimated_bytes} bytes exceeds memory budget "
            f"{memory_budget_bytes} bytes"
        )

    from src.learning.learning_engine import LearningEngine

    learning_enabled = plasticity_mode != "off"
    a_minus = STDP_A_PLUS if plasticity_mode == "symmetric" else STDP_A_MINUS
    learning_config = {
        "stdp": {
            "enabled": learning_enabled,
            "a_plus": STDP_A_PLUS,
            "a_minus": a_minus,
            "tau_plus": STDP_TAU_TICKS,
            "tau_minus": STDP_TAU_TICKS,
            "min_weight": MIN_WEIGHT,
            "max_weight": MAX_WEIGHT,
        },
        "eligibility": {
            "enabled": learning_enabled,
            "tau_ticks": ELIGIBILITY_TAU_TICKS,
        },
        "reward": {
            "enabled": learning_enabled,
            "learning_rate": REWARD_LEARNING_RATE,
            "delay_ticks": 0,
            "clamp_weights": True,
            "reset_trace_after_reward": True,
        },
    }

    tracemalloc.start()
    setup_started = time.perf_counter()
    try:
        network, source_ids, target_ids = _build_network(
            neuron_count, synapse_count, seed
        )
        learning = LearningEngine(network, learning_config)
        learning.attach()
        _, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    setup_seconds = time.perf_counter() - setup_started

    initial_weights = {
        (source_id, synapse.target_id): synapse.weight
        for source_id, outgoing in network.synapses.items()
        for synapse in outgoing
    }
    incoming_degree: dict[int, int] = {}
    for outgoing in network.synapses.values():
        for synapse in outgoing:
            incoming_degree[synapse.target_id] = (
                incoming_degree.get(synapse.target_id, 0) + 1
            )

    estimated_synapse_candidate_visits = 0
    source_spikes = 0
    target_spikes = 0
    final_epoch_source_spikes = 0
    final_epoch_target_spikes = 0
    core_step_seconds = 0.0
    stability: list[dict[str, Any]] = []
    run_started = time.perf_counter()
    for epoch in range(1, epochs + 1):
        cohort = epoch % COHORT_COUNT
        active_sources = (
            source_ids
            if activity_profile == "uniform"
            else source_ids[cohort::COHORT_COUNT]
        )
        active_targets = (
            target_ids
            if activity_profile == "uniform"
            else target_ids[(cohort + 1) % COHORT_COUNT :: COHORT_COUNT]
        )
        network.inject_current_batch(dict.fromkeys(active_sources, SOURCE_CURRENT))
        source_result = network.step()
        core_step_seconds += source_result.core_step_ms / 1000.0
        source_spikes += len(source_result.spike_ids)
        final_epoch_source_spikes = len(source_result.spike_ids)
        estimated_synapse_candidate_visits += sum(
            len(network.synapses[neuron_id]) for neuron_id in source_result.spike_ids
        )

        network.inject_current_batch(dict.fromkeys(active_targets, SOURCE_CURRENT))
        target_result = network.step()
        core_step_seconds += target_result.core_step_ms / 1000.0
        target_spikes += len(target_result.spike_ids)
        final_epoch_target_spikes = len(target_result.spike_ids)
        if learning_enabled:
            estimated_synapse_candidate_visits += sum(
                incoming_degree.get(neuron_id, 0)
                for neuron_id in target_result.spike_ids
            )
            learning.set_reward(REWARD_VALUE, target_result.tick)
            estimated_synapse_candidate_visits += synapse_count

        if epoch % stability_interval == 0 or epoch == epochs:
            stability.append(_weight_snapshot(network, epoch))
    elapsed_seconds = time.perf_counter() - run_started

    final_snapshot = stability[-1]
    final_weight_count = network.synapse_count
    weight_diversity_required = (
        activity_profile == "heterogeneous_cohorts" and learning_enabled
    )
    stability_assessment = assess_stability(
        stability,
        final_epoch_source_spikes=final_epoch_source_spikes,
        final_epoch_target_spikes=final_epoch_target_spikes,
        weight_diversity_required=weight_diversity_required,
    )
    maximum_weight_drift = max(
        (
            abs(synapse.weight - initial_weights[(source_id, synapse.target_id)])
            for source_id, outgoing in network.synapses.items()
            for synapse in outgoing
        ),
        default=0.0,
    )
    stats = learning.stats
    return {
        "schema_version": 2,
        "benchmark": "stage3_plastic_network_scale",
        "scope": "engineering_verification_only",
        "scientific_evidence": False,
        "benchmark_source_sha256": _benchmark_source_digest(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu": platform.processor() or None,
        "logical_processors": os.cpu_count(),
        "seed": seed,
        "topology_sha256": _topology_digest(network),
        "plasticity_mode": plasticity_mode,
        "activity_profile": activity_profile,
        "topology": "deterministic_regular_bipartite",
        "neurons": neuron_count,
        "synapses": network.synapse_count,
        "out_degree": synapse_count // len(source_ids),
        "epochs": epochs,
        "ticks": epochs * 2,
        "estimated_peak_bytes": estimated_bytes,
        "tracemalloc_peak_bytes": int(peak_bytes),
        "memory_budget_bytes": memory_budget_bytes,
        "setup_seconds": setup_seconds,
        "simulation_seconds": elapsed_seconds,
        "core_step_seconds": core_step_seconds,
        "ticks_per_second": epochs * 2 / elapsed_seconds if elapsed_seconds else None,
        "estimated_synapse_candidate_visits": estimated_synapse_candidate_visits,
        "estimated_synapse_candidate_visits_per_second": (
            estimated_synapse_candidate_visits / elapsed_seconds
            if elapsed_seconds
            else None
        ),
        "candidate_visit_estimate": (
            "Outgoing adjacency traversals for source spikes, incoming learning "
            "event traversals for target spikes, plus one full reward scan per epoch."
        ),
        "source_spikes": source_spikes,
        "target_spikes": target_spikes,
        "final_epoch_source_spikes": final_epoch_source_spikes,
        "final_epoch_target_spikes": final_epoch_target_spikes,
        "learning_stats": stats.to_dict(),
        "maximum_absolute_weight_drift": maximum_weight_drift,
        "weight_bounds": {"minimum": MIN_WEIGHT, "maximum": MAX_WEIGHT},
        "final_weights_finite": final_snapshot["finite_weights"],
        "final_out_of_bounds_weights": final_snapshot["out_of_bounds_weights"],
        "weight_diversity_required": weight_diversity_required,
        **stability_assessment,
        "final_at_lower_bound_fraction": (
            final_snapshot["at_lower_bound_count"] / final_weight_count
            if final_weight_count
            else None
        ),
        "final_at_upper_bound_fraction": (
            final_snapshot["at_upper_bound_count"] / final_weight_count
            if final_weight_count
            else None
        ),
        "stability_snapshots": stability,
        "workload": {
            "topology": "source_i_to_targets[(i * out_degree + edge) % target_count]",
            "seed_effect": "seeded permutation of target node order before edge assignment",
            "initial_weight": INITIAL_WEIGHT,
            "connection_delay_ticks": 1,
            "source_and_target_current": SOURCE_CURRENT,
            "reward_per_epoch": REWARD_VALUE,
            "stdp": {
                "a_plus": STDP_A_PLUS,
                "a_minus": a_minus,
                "tau_ticks": STDP_TAU_TICKS,
            },
            "eligibility_tau_ticks": ELIGIBILITY_TAU_TICKS,
            "reward_learning_rate": REWARD_LEARNING_RATE,
            "reward_trace_reset": True,
            "plasticity_mode": plasticity_mode,
            "activity_profile": activity_profile,
            "cohort_count": COHORT_COUNT,
            "heterogeneous_profile_rule": (
                "sources: index mod 4 = epoch mod 4; targets: index mod 4 = "
                "(epoch + 1) mod 4"
            ),
            "mechanisms_included": [
                "pair_stdp",
                "eligibility_traces",
                "reward_modulated_plasticity",
            ],
            "mechanisms_excluded": [
                "firing_rate_homeostasis",
                "energy_homeostasis",
                "structural_growth_pruning",
                "checkpoint_restore",
            ],
        },
        "stage3_target_range": {
            "neurons": list(STAGE3_NEURON_RANGE),
            "synapses": list(STAGE3_SYNAPSE_RANGE),
            "lower_bound_covered": (
                neuron_count >= STAGE3_NEURON_RANGE[0]
                and synapse_count >= STAGE3_SYNAPSE_RANGE[0]
            ),
            "upper_bound_covered": (
                neuron_count >= STAGE3_NEURON_RANGE[1]
                and synapse_count >= STAGE3_SYNAPSE_RANGE[1]
            ),
        },
        "interpretation_limit": (
            "One deterministic topology/load profile; not general stability, "
            "scientific evidence, or full-range Stage-3 acceptance."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--neurons", type=int, default=10_000)
    parser.add_argument("--synapses", type=int, default=100_000)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--memory-budget-mib", type=int, default=2048)
    parser.add_argument("--stability-interval", type=int, default=10)
    parser.add_argument(
        "--plasticity-mode", choices=sorted(PLASTICITY_MODES), default="asymmetric"
    )
    parser.add_argument(
        "--activity-profile",
        choices=sorted(ACTIVITY_PROFILES),
        default="heterogeneous_cohorts",
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.memory_budget_mib <= 0:
        raise SystemExit("--memory-budget-mib must be positive")
    try:
        report = run_benchmark(
            neuron_count=args.neurons,
            synapse_count=args.synapses,
            epochs=args.epochs,
            seed=args.seed,
            memory_budget_bytes=args.memory_budget_mib * 1024**2,
            stability_interval=args.stability_interval,
            plasticity_mode=args.plasticity_mode,
            activity_profile=args.activity_profile,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    payload = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
