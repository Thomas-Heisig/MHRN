#!/usr/bin/env python3
"""Run the preregistered Stage-1 topology v3 time-resolved replication."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from run_stage1_topology_v2 import (
    CONDITIONS,
    PRIMARY_CONTRASTS,
    bootstrap_ci,
    build_network,
    holm,
    load_config,
    read_json,
    sha256,
    sign_test_p,
    write_json,
)
from src.research.canonical_state import canonical_state_digest

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-V3-TIME-RESOLVED.json"
CONFIG = ROOT / "configs" / "learning_experiment.yaml"
EXP_ID = "EXP-S1-TOPO-V3-20260918"
OUT = ROOT / "research" / "experiments" / EXP_ID
DATA = OUT / "data"
ANALYSIS = OUT / "analysis"

PRIMARY_ENDPOINTS = ("activation_auc_0_32", "half_activation_latency_censored")
REPLICATION_ENDPOINT = "first_output_latency_censored"


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
    }


def simulate(
    base_config: dict[str, Any],
    prereg: dict[str, Any],
    condition: str,
    seed: int,
) -> dict[str, Any]:
    weight = float(prereg["matched_budgets"]["synaptic_weight"])
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
    auc_window = int(prereg["evaluation"]["auc_window_ticks"])
    half_threshold = float(prereg["evaluation"]["half_activation_threshold"])
    censor = int(prereg["evaluation"]["censor_sentinel"])

    active: set[int] = set()
    active_outputs: set[int] = set()
    total_spikes = 0
    delivered_events = 0
    first_output: int | None = None
    half_activation: int | None = None
    last_activity: int | None = None
    cumulative_active_fraction: list[float] = []

    for tick in range(ticks):
        if tick < stimulus_ticks:
            network.inject_current_batch(
                {neuron_id: stimulus_current for neuron_id in input_ids}
            )
        result = network.step()
        spikes = {int(v) for v in result.spike_ids}
        total_spikes += int(result.spikes_this_tick)
        delivered_events += int(result.delivered_events)
        if spikes:
            active.update(spikes)
            last_activity = tick
        active_fraction = len(active) / float(len(neuron_ids))
        cumulative_active_fraction.append(active_fraction)
        if half_activation is None and active_fraction >= half_threshold:
            half_activation = tick
        output_spikes = spikes & output_ids
        if output_spikes:
            active_outputs.update(output_spikes)
            if first_output is None:
                first_output = tick

    auc = float(sum(cumulative_active_fraction[:auc_window]))
    return {
        "condition": condition,
        "seed": seed,
        "synaptic_weight": weight,
        "ticks": ticks,
        "node_count": len(neuron_ids),
        "edge_count": len(edges),
        "active_neurons": len(active),
        "final_active_fraction": len(active) / float(len(neuron_ids)),
        "activation_auc_0_32": auc,
        "half_activation_latency": half_activation,
        "half_activation_latency_censored": (
            half_activation if half_activation is not None else censor
        ),
        "active_output_neurons": len(active_outputs),
        "output_reach_fraction": len(active_outputs) / float(len(output_ids)),
        "first_output_latency": first_output,
        "first_output_latency_censored": (
            first_output if first_output is not None else censor
        ),
        "last_activity_tick": last_activity,
        "total_spikes": total_spikes,
        "delivered_events": delivered_events,
        "cumulative_active_fraction_per_tick": cumulative_active_fraction,
        "state_digest_before": before,
        "state_digest_after": canonical_state_digest(network),
        "edge_digest": hashlib.sha256(json.dumps(edges).encode()).hexdigest(),
        "coordinate_digest": hashlib.sha256(json.dumps(coords).encode()).hexdigest(),
        "degree_summary": degree_summary(edges, len(neuron_ids)),
        "coordinates_by_label": [list(coord) for coord in coords],
        "edges_by_label": [list(edge) for edge in edges],
    }


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
            "activation_auc_0_32_median": median(
                [float(row["activation_auc_0_32"]) for row in rows]
            ),
            "half_activation_latency_censored_median": median(
                [float(row["half_activation_latency_censored"]) for row in rows]
            ),
            "first_output_latency_censored_median": median(
                [float(row["first_output_latency_censored"]) for row in rows]
            ),
            "final_active_fraction_median": median(
                [float(row["final_active_fraction"]) for row in rows]
            ),
            "output_reach_fraction_median": median(
                [float(row["output_reach_fraction"]) for row in rows]
            ),
            "total_spikes_median": median([float(row["total_spikes"]) for row in rows]),
            "delivered_events_median": median(
                [float(row["delivered_events"]) for row in rows]
            ),
        }
    return summary


def analyze_endpoint(
    evaluation: list[dict[str, Any]],
    endpoint: str,
    alpha: float,
) -> list[dict[str, Any]]:
    lookup = {(str(run["condition"]), int(run["seed"])): run for run in evaluation}
    seeds = sorted({int(run["seed"]) for run in evaluation})
    tests: list[dict[str, Any]] = []
    for left, right in PRIMARY_CONTRASTS:
        differences = [
            float(lookup[(right, seed)][endpoint])
            - float(lookup[(left, seed)][endpoint])
            for seed in seeds
        ]
        boot_seed = int(
            hashlib.sha256(f"{EXP_ID}:{endpoint}:{left}:{right}".encode()).hexdigest()[
                :12
            ],
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
                "bootstrap_median_difference_ci95": bootstrap_ci(
                    differences, boot_seed
                ),
                "p_raw": sign_test_p(differences),
            }
        )
    holm(tests)
    for row in tests:
        low, high = row["bootstrap_median_difference_ci95"]
        row["ci_excludes_zero"] = bool(low > 0.0 or high < 0.0)
        row["significant"] = bool(
            float(row["p_holm"]) < alpha and row["ci_excludes_zero"]
        )
    return tests


def analyze(evaluation: list[dict[str, Any]], prereg: dict[str, Any]) -> dict[str, Any]:
    alpha = float(prereg["evaluation"]["alpha"])
    primary_tests: list[dict[str, Any]] = []
    for endpoint in PRIMARY_ENDPOINTS:
        primary_tests.extend(analyze_endpoint(evaluation, endpoint, alpha))

    replication_tests = analyze_endpoint(evaluation, REPLICATION_ENDPOINT, alpha)

    low_dim = {("1d", "2d"), ("2d", "3d")}
    ceiling_resolution = any(
        row["significant"] and tuple(row["contrast"]) in low_dim
        for row in primary_tests
    )
    replication_supported = all(
        row["significant"] and float(row["median_difference"]) < 0.0
        for row in replication_tests
    )
    if ceiling_resolution and replication_supported:
        status = "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
    elif ceiling_resolution or replication_supported:
        status = "PARTIAL_SUPPORT_WITHIN_PREREGISTERED_PROTOCOL"
    else:
        status = "NO_PREDEFINED_SUPPORT_DETECTED"

    return {
        "alpha": alpha,
        "primary_test": "exact two-sided paired sign test",
        "primary_multiple_testing": "Holm across 10 time-resolved tests",
        "primary_tests": primary_tests,
        "replication_endpoint": REPLICATION_ENDPOINT,
        "replication_multiple_testing": "Holm across 5 latency tests",
        "replication_tests": replication_tests,
        "ceiling_resolution_supported": ceiling_resolution,
        "replication_supported": replication_supported,
        "status": status,
    }


def validate_design(
    prereg: dict[str, Any], evaluation: list[dict[str, Any]]
) -> dict[str, Any]:
    seeds = {int(v) for v in prereg["evaluation"]["seeds"]}
    expected_edges = int(prereg["matched_budgets"]["expected_edge_count"])
    old_seeds = set(range(2101, 2121))
    checks = {
        "evaluation_condition_counts": all(
            sum(run["condition"] == condition for run in evaluation) == len(seeds)
            for condition in CONDITIONS
        ),
        "evaluation_seed_set": {int(run["seed"]) for run in evaluation} == seeds,
        "v2_seed_disjoint": seeds.isdisjoint(old_seeds),
        "node_count_matched": all(int(run["node_count"]) == 64 for run in evaluation),
        "edge_count_matched": all(
            int(run["edge_count"]) == expected_edges for run in evaluation
        ),
        "weight_frozen": all(
            float(run["synaptic_weight"])
            == float(prereg["matched_budgets"]["synaptic_weight"])
            for run in evaluation
        ),
        "evaluation_ticks_matched": all(
            int(run["ticks"]) == int(prereg["matched_budgets"]["evaluation_ticks"])
            for run in evaluation
        ),
    }
    return {
        "expected_edge_count": expected_edges,
        "checks": checks,
        "pass": all(checks.values()),
    }


def render_report(
    prereg: dict[str, Any],
    source: dict[str, Any],
    summary: dict[str, Any],
    analysis: dict[str, Any],
    integrity: dict[str, Any],
) -> str:
    lines = [
        f"# {EXP_ID}: topology_propagation_v3_time_resolved_replication",
        "",
        "Stage 1 - Kleines SNN",
        "Research question: RQ-SNN-003",
        "Hypothesis: H-SNN-003-B",
        f"Source freeze: {source['commit']}",
        f"Clean before execution: {not source['dirty_before_execution']}",
        "Data role: DATA; no automatic EVID promotion.",
        "",
        "## Fixed design",
        "",
        f"- neurons per condition: {prereg['matched_budgets']['neuron_count']}",
        f"- edges per condition: {integrity['expected_edge_count']}",
        f"- synaptic weight: {prereg['matched_budgets']['synaptic_weight']}",
        f"- evaluation seeds: {len(prereg['evaluation']['seeds'])}",
        "- V2 evaluation seeds are not reused.",
        "",
        f"## Status: {analysis['status']}",
        "",
        "## Condition summaries",
        "",
        "| condition | n | activation AUC 0-32 | half-active latency | first-output latency | final active fraction |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for condition in CONDITIONS:
        row = summary[condition]
        lines.append(
            f"| {condition} | {row['n']} | {row['activation_auc_0_32_median']:.6g} | "
            f"{row['half_activation_latency_censored_median']:.6g} | "
            f"{row['first_output_latency_censored_median']:.6g} | "
            f"{row['final_active_fraction_median']:.6g} |"
        )
    lines += [
        "",
        "## Primary time-resolved contrasts",
        "",
        "| endpoint | contrast | median delta | CI95 | Holm-p | significant |",
        "| --- | --- | ---: | --- | ---: | :---: |",
    ]
    for row in analysis["primary_tests"]:
        low, high = row["bootstrap_median_difference_ci95"]
        lines.append(
            f"| {row['endpoint']} | {row['contrast'][0]} -> {row['contrast'][1]} | "
            f"{row['median_difference']:.6g} | [{low:.6g}, {high:.6g}] | "
            f"{row['p_holm']:.6g} | {'yes' if row['significant'] else 'no'} |"
        )
    lines += [
        "",
        "## V2 first-output latency replication",
        "",
        "| contrast | median delta | CI95 | Holm-p | significant |",
        "| --- | ---: | --- | ---: | :---: |",
    ]
    for row in analysis["replication_tests"]:
        low, high = row["bootstrap_median_difference_ci95"]
        lines.append(
            f"| {row['contrast'][0]} -> {row['contrast'][1]} | "
            f"{row['median_difference']:.6g} | [{low:.6g}, {high:.6g}] | "
            f"{row['p_holm']:.6g} | {'yes' if row['significant'] else 'no'} |"
        )
    lines += [
        "",
        f"Ceiling-resolution criterion: {'PASS' if analysis['ceiling_resolution_supported'] else 'FAIL'}",
        f"V2 latency replication criterion: {'PASS' if analysis['replication_supported'] else 'FAIL'}",
        f"Design integrity: {'PASS' if integrity['pass'] else 'FAIL'}",
        "",
        "## Claim boundary",
        "",
        str(prereg["interpretation_boundary"]),
        "",
        "## Local review after pull",
        "",
        "Run:",
        "python scripts/verify_stage1_topology_v3.py",
        "",
        "Raw data: data/evaluation.json.",
        "Statistics: analysis/statistics.json.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    prereg = read_json(PREREG)
    if prereg["protocol"] != "topology_propagation_v3_time_resolved_replication":
        raise RuntimeError("unexpected protocol")
    if prereg.get("execution_authorized") is not True:
        raise RuntimeError("execution not authorized")

    source = source_state()
    if source["dirty_before_execution"]:
        raise RuntimeError("source tree is dirty before execution")

    base_config = load_config()
    DATA.mkdir(parents=True, exist_ok=True)
    ANALYSIS.mkdir(parents=True, exist_ok=True)

    evaluation: list[dict[str, Any]] = []
    for seed_raw in prereg["evaluation"]["seeds"]:
        seed = int(seed_raw)
        for condition in CONDITIONS:
            evaluation.append(simulate(base_config, prereg, condition, seed))

    summary = summarize(evaluation)
    analysis = analyze(evaluation, prereg)
    integrity = validate_design(prereg, evaluation)
    if not integrity["pass"]:
        analysis["status"] = "NOT_TESTED_INTEGRITY_FAILURE"

    write_json(DATA / "evaluation.json", evaluation)
    statistics_payload = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "protocol": prereg["protocol"],
        "condition_summary": summary,
        "analysis": analysis,
        "integrity": integrity,
        "claim_boundary": prereg["interpretation_boundary"],
    }
    write_json(ANALYSIS / "statistics.json", statistics_payload)

    artifact_hashes = {
        "preregistration": sha256(PREREG),
        "config": sha256(CONFIG),
        "runner_source": sha256(Path(__file__).resolve()),
        "evaluation_data": sha256(DATA / "evaluation.json"),
        "statistics": sha256(ANALYSIS / "statistics.json"),
    }
    manifest = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "stage": 1,
        "research_question": "RQ-SNN-003",
        "hypothesis": "H-SNN-003-B",
        "protocol": prereg["protocol"],
        "experiment_status": "completed" if integrity["pass"] else "not_tested",
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "source_freeze": source,
        "software": {
            "python": sys.version,
            "platform": platform.platform(),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        },
        "design": {
            "evaluation_seeds": [int(v) for v in prereg["evaluation"]["seeds"]],
            "synaptic_weight": float(prereg["matched_budgets"]["synaptic_weight"]),
            "conditions": list(CONDITIONS),
            "primary_endpoints": list(PRIMARY_ENDPOINTS),
            "replication_endpoint": REPLICATION_ENDPOINT,
            "primary_contrasts": [list(value) for value in PRIMARY_CONTRASTS],
        },
        "results": {
            "status": analysis["status"],
            "evaluation_run_count": len(evaluation),
            "design_integrity_passed": bool(integrity["pass"]),
            "ceiling_resolution_supported": bool(
                analysis["ceiling_resolution_supported"]
            ),
            "replication_supported": bool(analysis["replication_supported"]),
        },
        "artifacts_sha256": artifact_hashes,
        "claim_boundary": prereg["interpretation_boundary"],
    }
    write_json(OUT / "manifest.json", manifest)
    (OUT / "report.md").write_text(
        render_report(prereg, source, summary, analysis, integrity),
        encoding="utf-8",
    )

    checksums = {
        "manifest.json": sha256(OUT / "manifest.json"),
        "report.md": sha256(OUT / "report.md"),
        "data/evaluation.json": artifact_hashes["evaluation_data"],
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
                "status": analysis["status"],
                "evaluation_runs": len(evaluation),
                "ceiling_resolution_supported": analysis[
                    "ceiling_resolution_supported"
                ],
                "replication_supported": analysis["replication_supported"],
                "source_freeze": source["commit"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
