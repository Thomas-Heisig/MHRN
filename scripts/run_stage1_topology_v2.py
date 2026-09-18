#!/usr/bin/env python3
"""Run the preregistered Stage-1 topology propagation v2 experiment."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import platform
import random
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from src.core import NeuralNetwork
from src.core.synapse import SynapseConfig
from src.research.canonical_state import canonical_state_digest

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-V2.json"
CONFIG = ROOT / "configs" / "learning_experiment.yaml"
EXP_ID = "EXP-S1-TOPO-V2-20260918"
OUT = ROOT / "research" / "experiments" / EXP_ID
DATA = OUT / "data"
ANALYSIS = OUT / "analysis"

CONDITIONS = ("1d", "2d", "3d", "5d", "5d_shuffled", "random_graph")
PRIMARY_ENDPOINTS = ("active_fraction", "first_output_latency_censored")
PRIMARY_CONTRASTS = (
    ("1d", "2d"),
    ("2d", "3d"),
    ("3d", "5d"),
    ("5d", "5d_shuffled"),
    ("5d", "random_graph"),
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path} must be a JSON object")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def source_state() -> dict[str, Any]:
    status = git("status", "--porcelain")
    return {
        "commit": git("rev-parse", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "dirty_before_execution": bool(status),
        "status_before_execution": status.splitlines(),
    }


def load_config() -> dict[str, Any]:
    value = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("config must be a mapping")
    return dict(value)


def all_coords(shape: tuple[int, int, int, int, int]) -> list[tuple[int, int, int, int, int]]:
    coords = list(itertools.product(*(range(size) for size in shape)))
    if len(coords) != 64:
        raise ValueError(f"shape {shape} must contain 64 coordinates")
    return [tuple(int(v) for v in coord) for coord in coords]


def coordinate_score(
    coord: tuple[int, int, int, int, int],
    shape: tuple[int, int, int, int, int],
) -> float:
    return sum(
        float(value) / float(max(size - 1, 1))
        for value, size in zip(coord, shape, strict=True)
    )


def canonical_coords(
    shape: tuple[int, int, int, int, int],
) -> list[tuple[int, int, int, int, int]]:
    return sorted(all_coords(shape), key=lambda coord: (coordinate_score(coord, shape), coord))


def normalized_distance(
    left: tuple[int, int, int, int, int],
    right: tuple[int, int, int, int, int],
    shape: tuple[int, int, int, int, int],
) -> float:
    return math.sqrt(
        sum(
            (float(a - b) / float(max(size - 1, 1))) ** 2
            for a, b, size in zip(left, right, shape, strict=True)
        )
    )


def tie_key(seed: int, source: int, target: int) -> str:
    return hashlib.sha256(f"{seed}:{source}:{target}".encode()).hexdigest()


def shape_for(prereg: dict[str, Any], condition: str) -> tuple[int, int, int, int, int]:
    raw = tuple(int(v) for v in prereg["conditions"][condition])
    if len(raw) != 5:
        raise ValueError(condition)
    return raw  # type: ignore[return-value]


def edge_list(
    prereg: dict[str, Any],
    condition: str,
    seed: int,
    coords: list[tuple[int, int, int, int, int]],
) -> list[tuple[int, int]]:
    out_degree = int(prereg["matched_budgets"]["out_degree_cap"])
    shape = shape_for(prereg, condition)
    rng = random.Random(seed ^ 0x51A6E1)
    edges: list[tuple[int, int]] = []
    for source in range(len(coords) - 1):
        future = list(range(source + 1, len(coords)))
        degree = min(out_degree, len(future))
        if condition == "random_graph":
            targets = sorted(rng.sample(future, degree))
        else:
            targets = sorted(
                future,
                key=lambda target: (
                    normalized_distance(coords[source], coords[target], shape),
                    tie_key(seed, source, target),
                    target,
                ),
            )[:degree]
        edges.extend((source, target) for target in targets)
    return edges


def build_network(
    base_config: dict[str, Any],
    prereg: dict[str, Any],
    condition: str,
    seed: int,
    weight: float,
) -> tuple[NeuralNetwork, list[int], list[tuple[int, int, int, int, int]], list[tuple[int, int]]]:
    shape = shape_for(prereg, condition)
    coords = canonical_coords(shape)
    if condition == "5d_shuffled":
        random.Random(seed ^ 0x5D5D5D).shuffle(coords)

    values = dict(base_config)
    values["dimensions"] = list(shape)
    values["initial_neurons"] = 0
    simulation = dict(values.get("simulation", {}))
    simulation["max_delay"] = max(1, int(simulation.get("max_delay", 1)))
    values["simulation"] = simulation

    network = NeuralNetwork(values, random.Random(seed))
    neuron_ids = [network.add_neuron(coord) for coord in coords]

    input_labels = [int(v) for v in prereg["matched_budgets"]["stimulus_input_labels"]]
    output_labels = [int(v) for v in prereg["matched_budgets"]["output_labels"]]
    network.input_cells.update(neuron_ids[label] for label in input_labels)
    network.output_cells.update(neuron_ids[label] for label in output_labels)

    edges = edge_list(prereg, condition, seed, coords)
    synapse_config = SynapseConfig(w_max=max(200.0, weight))
    delay = int(prereg["matched_budgets"]["delay_ticks"])
    for source, target in edges:
        network.connect(
            neuron_ids[source],
            neuron_ids[target],
            weight,
            delay,
            config=synapse_config,
        )
    return network, neuron_ids, coords, edges


def degree_summary(edges: list[tuple[int, int]], count: int) -> dict[str, Any]:
    incoming = [0] * count
    outgoing = [0] * count
    for source, target in edges:
        outgoing[source] += 1
        incoming[target] += 1
    return {
        "edge_count": len(edges),
        "density": len(edges) / float(count * (count - 1)),
        "in_degree_min": min(incoming),
        "in_degree_max": max(incoming),
        "in_degree_mean": statistics.fmean(incoming),
        "out_degree_min": min(outgoing),
        "out_degree_max": max(outgoing),
        "out_degree_mean": statistics.fmean(outgoing),
        "out_degree_sequence": outgoing,
    }


def simulate(
    base_config: dict[str, Any],
    prereg: dict[str, Any],
    condition: str,
    seed: int,
    weight: float,
    include_graph: bool,
) -> dict[str, Any]:
    network, neuron_ids, coords, edges = build_network(
        base_config, prereg, condition, seed, weight
    )
    before = canonical_state_digest(network)
    ticks = int(prereg["matched_budgets"]["evaluation_ticks"])
    stimulus_ticks = int(prereg["matched_budgets"]["stimulus_ticks"])
    stimulus_current = float(prereg["matched_budgets"]["stimulus_current"])
    input_labels = [int(v) for v in prereg["matched_budgets"]["stimulus_input_labels"]]
    output_labels = [int(v) for v in prereg["matched_budgets"]["output_labels"]]
    input_ids = [neuron_ids[label] for label in input_labels]
    output_ids = {neuron_ids[label] for label in output_labels}

    active: set[int] = set()
    active_outputs: set[int] = set()
    total_spikes = 0
    delivered_events = 0
    first_output: int | None = None
    last_activity: int | None = None
    spike_counts: list[int] = []
    delivered_counts: list[int] = []

    for tick in range(ticks):
        if tick < stimulus_ticks:
            network.inject_current_batch(
                {neuron_id: stimulus_current for neuron_id in input_ids}
            )
        result = network.step()
        spikes = {int(v) for v in result.spike_ids}
        spike_counts.append(int(result.spikes_this_tick))
        delivered_counts.append(int(result.delivered_events))
        total_spikes += int(result.spikes_this_tick)
        delivered_events += int(result.delivered_events)
        if spikes:
            active.update(spikes)
            last_activity = tick
        output_spikes = spikes & output_ids
        if output_spikes:
            active_outputs.update(output_spikes)
            if first_output is None:
                first_output = tick

    payload: dict[str, Any] = {
        "condition": condition,
        "seed": seed,
        "synaptic_weight": weight,
        "ticks": ticks,
        "node_count": len(neuron_ids),
        "active_neurons": len(active),
        "active_fraction": len(active) / float(len(neuron_ids)),
        "active_output_neurons": len(active_outputs),
        "output_reach_fraction": len(active_outputs) / float(len(output_ids)),
        "first_output_latency": first_output,
        "first_output_latency_censored": first_output if first_output is not None else ticks + 1,
        "last_activity_tick": last_activity,
        "total_spikes": total_spikes,
        "delivered_events": delivered_events,
        "spike_counts_per_tick": spike_counts,
        "delivered_events_per_tick": delivered_counts,
        "state_digest_before": before,
        "state_digest_after": canonical_state_digest(network),
        "edge_digest": hashlib.sha256(json.dumps(edges).encode()).hexdigest(),
        "coordinate_digest": hashlib.sha256(json.dumps(coords).encode()).hexdigest(),
        "degree_summary": degree_summary(edges, len(neuron_ids)),
    }
    if include_graph:
        payload["coordinates_by_label"] = [list(coord) for coord in coords]
        payload["edges_by_label"] = [list(edge) for edge in edges]
    return payload


def median(values: list[float]) -> float:
    return float(statistics.median(values)) if values else 0.0


def summarize(runs: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        grouped[str(run["condition"])].append(run)
    summary: dict[str, Any] = {}
    for condition in CONDITIONS:
        rows = grouped[condition]
        summary[condition] = {
            "n": len(rows),
            "active_fraction_median": median([float(row["active_fraction"]) for row in rows]),
            "output_reach_fraction_median": median([float(row["output_reach_fraction"]) for row in rows]),
            "first_output_latency_censored_median": median([float(row["first_output_latency_censored"]) for row in rows]),
            "total_spikes_median": median([float(row["total_spikes"]) for row in rows]),
            "delivered_events_median": median([float(row["delivered_events"]) for row in rows]),
        }
    return summary


def calibration_gate(runs: list[dict[str, Any]], weight: float) -> dict[str, Any]:
    rows = [run for run in runs if float(run["synaptic_weight"]) == weight]
    summary = summarize(rows)
    passed = True
    conditions: dict[str, Any] = {}
    for condition in CONDITIONS:
        item = summary[condition]
        condition_pass = (
            item["active_fraction_median"] >= 0.25
            and item["output_reach_fraction_median"] >= 0.25
            and item["delivered_events_median"] >= 32.0
        )
        conditions[condition] = {**item, "pass": condition_pass}
        passed = passed and condition_pass
    return {"weight": weight, "pass": passed, "conditions": conditions}


def percentile(values: list[float], p: float) -> float:
    if len(values) == 1:
        return values[0]
    position = p * (len(values) - 1)
    lo = int(math.floor(position))
    hi = int(math.ceil(position))
    if lo == hi:
        return values[lo]
    part = position - lo
    return values[lo] * (1.0 - part) + values[hi] * part


def bootstrap_ci(differences: list[float], seed: int) -> list[float]:
    if not differences:
        return [0.0, 0.0]
    rng = random.Random(seed)
    n = len(differences)
    samples: list[float] = []
    for _ in range(5000):
        sample = [differences[rng.randrange(n)] for _ in range(n)]
        samples.append(float(statistics.median(sample)))
    samples.sort()
    return [percentile(samples, 0.025), percentile(samples, 0.975)]


def sign_test_p(differences: list[float]) -> float:
    nonzero = [value for value in differences if abs(value) > 1e-12]
    n = len(nonzero)
    if n == 0:
        return 1.0
    positives = sum(value > 0.0 for value in nonzero)
    tail = min(positives, n - positives)
    probability = sum(math.comb(n, k) for k in range(tail + 1)) / float(2**n)
    return min(1.0, 2.0 * probability)


def holm(records: list[dict[str, Any]]) -> None:
    ordered = sorted(enumerate(records), key=lambda item: float(item[1]["p_raw"]))
    total = len(ordered)
    running = 0.0
    for rank, (index, row) in enumerate(ordered):
        value = min(1.0, (total - rank) * float(row["p_raw"]))
        running = max(running, value)
        records[index]["p_holm"] = running


def analyze(evaluation: list[dict[str, Any]], alpha: float) -> dict[str, Any]:
    lookup = {
        (str(run["condition"]), int(run["seed"])): run
        for run in evaluation
    }
    seeds = sorted({int(run["seed"]) for run in evaluation})
    tests: list[dict[str, Any]] = []
    for endpoint in PRIMARY_ENDPOINTS:
        for left, right in PRIMARY_CONTRASTS:
            differences = [
                float(lookup[(right, seed)][endpoint])
                - float(lookup[(left, seed)][endpoint])
                for seed in seeds
            ]
            boot_seed = int(
                hashlib.sha256(f"{endpoint}:{left}:{right}".encode()).hexdigest()[:12],
                16,
            )
            tests.append(
                {
                    "endpoint": endpoint,
                    "contrast": [left, right],
                    "difference_definition": "right-minus-left",
                    "n_pairs": len(differences),
                    "nonzero_pairs": sum(abs(value) > 1e-12 for value in differences),
                    "median_difference": float(statistics.median(differences)),
                    "mean_difference": float(statistics.fmean(differences)),
                    "bootstrap_median_difference_ci95": bootstrap_ci(differences, boot_seed),
                    "p_raw": sign_test_p(differences),
                }
            )
    holm(tests)
    for row in tests:
        low, high = row["bootstrap_median_difference_ci95"]
        row["ci_excludes_zero"] = bool(low > 0.0 or high < 0.0)
        row["significant"] = bool(float(row["p_holm"]) < alpha and row["ci_excludes_zero"])
    return {
        "alpha": alpha,
        "test": "exact two-sided paired sign test",
        "multiple_testing": "Holm",
        "tests": tests,
        "any_primary_difference": any(bool(row["significant"]) for row in tests),
    }


def validate_design(
    prereg: dict[str, Any],
    calibration: list[dict[str, Any]],
    evaluation: list[dict[str, Any]],
    weight: float,
) -> dict[str, Any]:
    calibration_seeds = {int(v) for v in prereg["calibration"]["seeds"]}
    evaluation_seeds = {int(v) for v in prereg["evaluation"]["seeds"]}
    expected_edges = sum(min(4, 64 - source - 1) for source in range(63))
    checks = {
        "seed_sets_disjoint": calibration_seeds.isdisjoint(evaluation_seeds),
        "evaluation_condition_counts": all(
            sum(run["condition"] == condition for run in evaluation) == len(evaluation_seeds)
            for condition in CONDITIONS
        ),
        "node_count_matched": all(int(run["node_count"]) == 64 for run in evaluation),
        "edge_count_matched": all(
            int(run["degree_summary"]["edge_count"]) == expected_edges
            for run in evaluation
        ),
        "weight_frozen": all(float(run["synaptic_weight"]) == weight for run in evaluation),
        "calibration_seed_scope": all(int(run["seed"]) in calibration_seeds for run in calibration),
    }
    return {
        "expected_edge_count": expected_edges,
        "checks": checks,
        "pass": all(checks.values()),
    }


def render_report(
    prereg: dict[str, Any],
    source: dict[str, Any],
    gates: list[dict[str, Any]],
    chosen_weight: float | None,
    condition_summary: dict[str, Any] | None,
    primary: dict[str, Any] | None,
    integrity: dict[str, Any] | None,
    status: str,
) -> str:
    lines = [
        f"# {EXP_ID}: topology_propagation_v2",
        "",
        "Stage 1 - Kleines SNN",
        "Research question: RQ-SNN-003",
        "Hypothesis: H-SNN-003-B",
        f"Source freeze: {source['commit']}",
        f"Clean before execution: {not source['dirty_before_execution']}",
        "Data role: DATA; no automatic EVID promotion.",
        "",
        "## Activity calibration",
        "",
        "| weight | gate |",
        "| ---: | :---: |",
    ]
    for gate in gates:
        lines.append(f"| {gate['weight']:.1f} | {'PASS' if gate['pass'] else 'FAIL'} |")
    lines += ["", f"Chosen weight: {chosen_weight}", "", f"## Status: {status}", ""]
    if condition_summary is not None:
        lines += [
            "| condition | n | active fraction | output reach | first output latency | spikes | delivered events |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for condition in CONDITIONS:
            row = condition_summary[condition]
            lines.append(
                f"| {condition} | {row['n']} | {row['active_fraction_median']:.4f} | "
                f"{row['output_reach_fraction_median']:.4f} | "
                f"{row['first_output_latency_censored_median']:.2f} | "
                f"{row['total_spikes_median']:.2f} | {row['delivered_events_median']:.2f} |"
            )
        lines.append("")
    if primary is not None:
        lines += [
            "## Preregistered primary contrasts",
            "",
            "| endpoint | contrast | median delta | CI95 | Holm-p | significant |",
            "| --- | --- | ---: | --- | ---: | :---: |",
        ]
        for row in primary["tests"]:
            low, high = row["bootstrap_median_difference_ci95"]
            lines.append(
                f"| {row['endpoint']} | {row['contrast'][0]} -> {row['contrast'][1]} | "
                f"{row['median_difference']:.6g} | [{low:.6g}, {high:.6g}] | "
                f"{row['p_holm']:.6g} | {'yes' if row['significant'] else 'no'} |"
            )
        lines += [
            "",
            "A significant topology difference is not a claim that 5D is superior.",
            "",
        ]
    if integrity is not None:
        lines += [
            "## Integrity",
            "",
            f"Design checks: {'PASS' if integrity['pass'] else 'FAIL'}",
            f"Expected edges per evaluation run: {integrity['expected_edge_count']}",
            "",
        ]
    lines += [
        "## Local review after pull",
        "",
        "Run:",
        "python scripts/verify_stage1_topology_v2.py",
        "",
        "Raw data: data/calibration.json and data/evaluation.json.",
        "Statistics: analysis/statistics.json.",
        "",
        "## Claim boundary",
        "",
        str(prereg["claim_boundary"]),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    prereg = read_json(PREREG)
    if prereg["protocol"] != "topology_propagation_v2":
        raise RuntimeError("unexpected protocol")
    if prereg.get("execution_authorized") is not True:
        raise RuntimeError("execution not authorized")

    source = source_state()
    if source["dirty_before_execution"]:
        raise RuntimeError("source tree is dirty before execution")

    base_config = load_config()
    DATA.mkdir(parents=True, exist_ok=True)
    ANALYSIS.mkdir(parents=True, exist_ok=True)

    calibration: list[dict[str, Any]] = []
    gates: list[dict[str, Any]] = []
    chosen_weight: float | None = None
    for weight_raw in prereg["calibration"]["candidate_synaptic_weights"]:
        weight = float(weight_raw)
        for seed_raw in prereg["calibration"]["seeds"]:
            seed = int(seed_raw)
            for condition in CONDITIONS:
                calibration.append(
                    simulate(base_config, prereg, condition, seed, weight, False)
                )
        gate = calibration_gate(calibration, weight)
        gates.append(gate)
        if gate["pass"]:
            chosen_weight = weight
            break

    write_json(DATA / "calibration.json", calibration)
    write_json(ANALYSIS / "calibration_gate.json", gates)

    evaluation: list[dict[str, Any]] = []
    condition_summary: dict[str, Any] | None = None
    primary: dict[str, Any] | None = None
    integrity: dict[str, Any] | None = None
    status = "NOT_TESTED_ACTIVITY_GATE_FAILED"

    if chosen_weight is not None:
        for seed_raw in prereg["evaluation"]["seeds"]:
            seed = int(seed_raw)
            for condition in CONDITIONS:
                evaluation.append(
                    simulate(base_config, prereg, condition, seed, chosen_weight, True)
                )
        condition_summary = summarize(evaluation)
        primary = analyze(evaluation, float(prereg["evaluation"]["alpha"]))
        integrity = validate_design(prereg, calibration, evaluation, chosen_weight)
        if not integrity["pass"]:
            status = "NOT_TESTED_INTEGRITY_FAILURE"
        elif primary["any_primary_difference"]:
            status = "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
        else:
            status = "NO_PREDEFINED_TOPOLOGY_DIFFERENCE_DETECTED"

    write_json(DATA / "evaluation.json", evaluation)
    statistics_payload = {
        "experiment_id": EXP_ID,
        "protocol": prereg["protocol"],
        "chosen_synaptic_weight": chosen_weight,
        "activity_gate": gates,
        "condition_summary": condition_summary,
        "primary_analysis": primary,
        "integrity": integrity,
        "status": status,
        "claim_boundary": prereg["claim_boundary"],
    }
    write_json(ANALYSIS / "statistics.json", statistics_payload)

    artifact_hashes = {
        "preregistration": sha256(PREREG),
        "config": sha256(CONFIG),
        "runner_source": sha256(Path(__file__).resolve()),
        "calibration_data": sha256(DATA / "calibration.json"),
        "evaluation_data": sha256(DATA / "evaluation.json"),
        "calibration_gate": sha256(ANALYSIS / "calibration_gate.json"),
        "statistics": sha256(ANALYSIS / "statistics.json"),
    }
    manifest = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "stage": 1,
        "research_question": "RQ-SNN-003",
        "hypothesis": "H-SNN-003-B",
        "protocol": prereg["protocol"],
        "experiment_status": "completed" if chosen_weight is not None else "not_tested",
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "source_freeze": source,
        "software": {
            "python": sys.version,
            "platform": platform.platform(),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        },
        "design": {
            "calibration_seeds": [int(v) for v in prereg["calibration"]["seeds"]],
            "evaluation_seeds": [int(v) for v in prereg["evaluation"]["seeds"]],
            "chosen_synaptic_weight": chosen_weight,
            "conditions": list(CONDITIONS),
            "primary_endpoints": list(PRIMARY_ENDPOINTS),
            "primary_contrasts": [list(value) for value in PRIMARY_CONTRASTS],
        },
        "results": {
            "status": status,
            "calibration_run_count": len(calibration),
            "evaluation_run_count": len(evaluation),
            "activity_gate_passed": chosen_weight is not None,
            "design_integrity_passed": bool(integrity and integrity["pass"]),
            "any_primary_difference": bool(primary and primary["any_primary_difference"]),
        },
        "artifacts_sha256": artifact_hashes,
        "claim_boundary": prereg["claim_boundary"],
    }
    write_json(OUT / "manifest.json", manifest)
    (OUT / "report.md").write_text(
        render_report(
            prereg,
            source,
            gates,
            chosen_weight,
            condition_summary,
            primary,
            integrity,
            status,
        ),
        encoding="utf-8",
    )

    checksums = {
        "manifest.json": sha256(OUT / "manifest.json"),
        "report.md": sha256(OUT / "report.md"),
        "data/calibration.json": artifact_hashes["calibration_data"],
        "data/evaluation.json": artifact_hashes["evaluation_data"],
        "analysis/calibration_gate.json": artifact_hashes["calibration_gate"],
        "analysis/statistics.json": artifact_hashes["statistics"],
    }
    (OUT / "checksums.sha256").write_text(
        "".join(f"{digest}  {name}\n" for name, digest in sorted(checksums.items())),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "experiment_id": EXP_ID,
                "status": status,
                "chosen_synaptic_weight": chosen_weight,
                "calibration_runs": len(calibration),
                "evaluation_runs": len(evaluation),
                "source_freeze": source["commit"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
