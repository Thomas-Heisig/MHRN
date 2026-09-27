#!/usr/bin/env python3
"""Confirmatory Stage-1 topology efficiency R1 evaluation.

Execution is impossible until calibration results and seed-freshness evidence are
frozen into the preregistration and explicit execution authorization is granted.
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import subprocess
import time
from pathlib import Path
from typing import Any

from run_stage1_topology_v2 import bootstrap_ci, build_network, holm, load_config

from src.research.canonical_state import canonical_state_digest
from src.research.experiment_recorder import ExperimentRecorder
from src.research_assistant.governance import (
    DataPartition,
    NetworkMode,
    ResearchRunMode,
)

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-EFFICIENCY-R1.json"
EXPERIMENT_ID = "EXP-S1-TOPO-EFFICIENCY-R1-20260927"
OUT = ROOT / "research" / "experiments" / EXPERIMENT_ID
CALIBRATION = ROOT / "research" / "calibrations" / "CAL-S1-TOPO-EFFICIENCY-R1-20260927"
CONFIG = ROOT / "configs" / "learning_experiment.yaml"

CONDITIONS = (
    "3d_reference",
    "5d_reference",
    "5d_shuffled",
    "random_graph",
    "3d_recruitment_matched",
    "5d_high_recruitment",
)
PRIMARY_ENDPOINTS = (
    "activation_auc_per_spike",
    "activation_auc_per_delivered_event",
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _canonical_digest(value: object) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return _sha256_bytes(raw)


def _tracked_source_digest() -> str:
    names = (
        subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        .decode()
        .split("\0")
    )
    selected: dict[str, str] = {}
    for name in names:
        if not name:
            continue
        if name.startswith(("src/", "scripts/")) or name in {
            "pyproject.toml",
            "configs/learning_experiment.yaml",
            "research/preregistrations/PREREG-S1-TOPO-EFFICIENCY-R1.json",
        }:
            selected[name] = _sha256_file(ROOT / name)
    return _canonical_digest(selected)


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _topology_prereg(prereg: dict[str, Any]) -> dict[str, Any]:
    adapted = dict(prereg)
    adapted["conditions"] = {
        "3d": prereg["conditions"]["3d_reference"]["shape"],
        "5d": prereg["conditions"]["5d_reference"]["shape"],
        "5d_shuffled": prereg["conditions"]["5d_shuffled"]["shape"],
        "random_graph": prereg["conditions"]["random_graph"]["shape"],
    }
    matched = dict(prereg["matched_budgets"])
    matched["stimulus_current"] = float(
        prereg["calibration"]["reference_stimulus_current"]
    )
    adapted["matched_budgets"] = matched
    return adapted


def _graph_condition(condition: str) -> str:
    return {
        "3d_reference": "3d",
        "5d_reference": "5d",
        "5d_shuffled": "5d_shuffled",
        "random_graph": "random_graph",
        "3d_recruitment_matched": "3d",
        "5d_high_recruitment": "5d",
    }[condition]


def _stimulus_current(prereg: dict[str, Any], condition: str) -> float:
    if condition == "3d_recruitment_matched":
        return float(
            prereg["frozen_calibration"]["3d_recruitment_matched_stimulus_current"]
        )
    if condition == "5d_high_recruitment":
        return float(
            prereg["frozen_calibration"]["5d_high_recruitment_stimulus_current"]
        )
    return float(prereg["calibration"]["reference_stimulus_current"])


def simulate(
    config: dict[str, Any],
    prereg: dict[str, Any],
    condition: str,
    seed: int,
) -> dict[str, Any]:
    graph_condition = _graph_condition(condition)
    current = _stimulus_current(prereg, condition)
    weight = float(prereg["matched_budgets"]["synaptic_weight"])
    network, neuron_ids, coords, edges = build_network(
        config, _topology_prereg(prereg), graph_condition, seed, weight
    )
    before = canonical_state_digest(network)

    ticks = int(prereg["matched_budgets"]["evaluation_ticks"])
    stimulus_ticks = int(prereg["matched_budgets"]["stimulus_ticks"])
    input_labels = [int(v) for v in prereg["matched_budgets"]["stimulus_input_labels"]]
    output_labels = [int(v) for v in prereg["matched_budgets"]["output_labels"]]
    input_ids = [neuron_ids[label] for label in input_labels]
    output_ids = {neuron_ids[label] for label in output_labels}
    auc_window = int(prereg["matched_budgets"]["auc_window_ticks"])

    active: set[int] = set()
    active_outputs: set[int] = set()
    cumulative_active_fraction: list[float] = []
    total_spikes = 0
    delivered_events = 0
    first_output: int | None = None

    for tick in range(ticks):
        if tick < stimulus_ticks:
            network.inject_current_batch({nid: current for nid in input_ids})
        result = network.step()
        spikes = {int(v) for v in result.spike_ids}
        total_spikes += int(result.spikes_this_tick)
        delivered_events += int(result.delivered_events)
        active.update(spikes)
        output_spikes = spikes & output_ids
        active_outputs.update(output_spikes)
        if first_output is None and output_spikes:
            first_output = tick
        cumulative_active_fraction.append(len(active) / float(len(neuron_ids)))

    auc = float(sum(cumulative_active_fraction[:auc_window]))
    auc_per_spike = auc / float(total_spikes) if total_spikes else math.inf
    auc_per_event = auc / float(delivered_events) if delivered_events else math.inf
    return {
        "condition": condition,
        "graph_condition": graph_condition,
        "seed": seed,
        "stimulus_current": current,
        "synaptic_weight": weight,
        "ticks": ticks,
        "node_count": len(neuron_ids),
        "edge_count": len(edges),
        "activation_auc_0_32": auc,
        "activation_auc_per_spike": auc_per_spike,
        "activation_auc_per_delivered_event": auc_per_event,
        "total_spikes": total_spikes,
        "delivered_events": delivered_events,
        "final_active_fraction": len(active) / float(len(neuron_ids)),
        "output_reach_fraction": len(active_outputs) / float(len(output_ids)),
        "first_output_latency_censored": (
            first_output if first_output is not None else ticks + 1
        ),
        "state_digest_before": before,
        "state_digest_after": canonical_state_digest(network),
        "edge_digest": hashlib.sha256(json.dumps(edges).encode()).hexdigest(),
        "coordinate_digest": hashlib.sha256(json.dumps(coords).encode()).hexdigest(),
    }


def _one_sided_sign_test_p(values: list[float]) -> float:
    nonzero = [value for value in values if abs(value) > 1e-12]
    if not nonzero:
        return 1.0
    positives = sum(value > 0.0 for value in nonzero)
    return min(
        1.0,
        sum(math.comb(len(nonzero), k) for k in range(positives, len(nonzero) + 1))
        / (2 ** len(nonzero)),
    )


def _summaries(runs: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for condition in CONDITIONS:
        rows = [row for row in runs if row["condition"] == condition]
        out[condition] = {
            "n": len(rows),
            "activation_auc_0_32_median": float(
                statistics.median(row["activation_auc_0_32"] for row in rows)
            ),
            "activation_auc_per_spike_median": float(
                statistics.median(row["activation_auc_per_spike"] for row in rows)
            ),
            "activation_auc_per_delivered_event_median": float(
                statistics.median(
                    row["activation_auc_per_delivered_event"] for row in rows
                )
            ),
            "total_spikes_median": float(
                statistics.median(row["total_spikes"] for row in rows)
            ),
            "delivered_events_median": float(
                statistics.median(row["delivered_events"] for row in rows)
            ),
            "final_active_fraction_median": float(
                statistics.median(row["final_active_fraction"] for row in rows)
            ),
            "first_output_latency_censored_median": float(
                statistics.median(row["first_output_latency_censored"] for row in rows)
            ),
        }
    return out


def _analyze(runs: list[dict[str, Any]], prereg: dict[str, Any]) -> dict[str, Any]:
    seeds = list(map(int, prereg["evaluation"]["seeds"]))
    lookup = {(row["condition"], int(row["seed"])): row for row in runs}
    tests: list[dict[str, Any]] = []

    for endpoint in PRIMARY_ENDPOINTS:
        for contrast in prereg["evaluation"]["primary_contrasts"]:
            left = str(contrast["left"])
            right = str(contrast["right"])
            differences = [
                float(lookup[(right, seed)][endpoint])
                - float(lookup[(left, seed)][endpoint])
                for seed in seeds
            ]
            boot_seed = int(
                hashlib.sha256(
                    f"{EXPERIMENT_ID}:{endpoint}:{left}:{right}".encode()
                ).hexdigest()[:12],
                16,
            )
            tests.append(
                {
                    "endpoint": endpoint,
                    "contrast_label": contrast["label"],
                    "contrast": [left, right],
                    "difference_definition": "right-minus-left",
                    "n_pairs": len(differences),
                    "nonzero_pairs": sum(abs(v) > 1e-12 for v in differences),
                    "positive_pairs": sum(v > 0.0 for v in differences),
                    "median_difference": float(statistics.median(differences)),
                    "bootstrap_median_difference_ci95": bootstrap_ci(
                        differences, boot_seed
                    ),
                    "p_raw": _one_sided_sign_test_p(differences),
                }
            )
    holm(tests)
    for row in tests:
        low, high = row["bootstrap_median_difference_ci95"]
        row["positive_ci"] = bool(low > 0.0 and high > 0.0)
        row["significant_positive"] = bool(
            float(row["p_holm"]) < float(prereg["evaluation"]["alpha"])
            and row["positive_ci"]
            and float(row["median_difference"]) > 0.0
        )

    by_label: dict[str, dict[str, dict[str, Any]]] = {}
    for row in tests:
        by_label.setdefault(row["contrast_label"], {})[row["endpoint"]] = row

    def passes(label: str) -> bool:
        return all(
            by_label[label][endpoint]["significant_positive"]
            for endpoint in PRIMARY_ENDPOINTS
        )

    three_d = passes("5d_vs_3d_reference")
    shuffled = passes("5d_vs_5d_shuffled")
    random_graph = passes("5d_vs_random_graph")
    recruitment = passes("5d_vs_3d_recruitment_matched")

    if not three_d:
        status = "REFUTES_WITHIN_PROTOCOL"
        decision_case = "C"
    elif not shuffled or not random_graph:
        status = "INCONCLUSIVE_SPECIFICITY"
        decision_case = "B_specificity"
    elif not recruitment:
        status = "REFUTES_WITHIN_PROTOCOL"
        decision_case = "B_recruitment"
    else:
        status = "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
        decision_case = "A"

    return {
        "alpha": float(prereg["evaluation"]["alpha"]),
        "primary_test": "exact one-sided paired sign test",
        "primary_multiple_testing": prereg["evaluation"]["multiple_testing"],
        "primary_tests": tests,
        "decision_case": decision_case,
        "status": status,
        "exploratory_latency_only": True,
    }


def _integrity(runs: list[dict[str, Any]], prereg: dict[str, Any]) -> dict[str, Any]:
    seeds = set(map(int, prereg["evaluation"]["seeds"]))
    floor = prereg["evaluation"]["ratio_validity"]
    checks = {
        "run_count": len(runs) == len(CONDITIONS) * len(seeds),
        "coverage": all(
            sum(
                row["condition"] == condition and int(row["seed"]) == seed
                for row in runs
            )
            == 1
            for condition in CONDITIONS
            for seed in seeds
        ),
        "node_count": all(int(row["node_count"]) == 64 for row in runs),
        "edge_count": all(
            int(row["edge_count"])
            == int(prereg["matched_budgets"]["expected_edge_count"])
            for row in runs
        ),
        "spike_denominator_floor": all(
            int(row["total_spikes"]) >= int(floor["total_spikes_minimum_per_run"])
            for row in runs
        ),
        "event_denominator_floor": all(
            int(row["delivered_events"])
            >= int(floor["delivered_events_minimum_per_run"])
            for row in runs
        ),
        "finite_ratios": all(
            math.isfinite(float(row["activation_auc_per_spike"]))
            and math.isfinite(float(row["activation_auc_per_delivered_event"]))
            for row in runs
        ),
    }
    return {"checks": checks, "pass": all(checks.values())}


def main() -> None:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    if prereg.get("status") != "FROZEN_BEFORE_EFFICIENCY_EVALUATION":
        raise RuntimeError("efficiency preregistration is not frozen for evaluation")
    if prereg.get("execution_authorized") is not True:
        raise RuntimeError("efficiency evaluation is not authorized")
    if prereg.get("claim_id") != "CLAIM-S1-EFFICIENCY-001":
        raise RuntimeError("unexpected scoped efficiency claim")
    if OUT.exists():
        raise FileExistsError(f"Refusing to overwrite existing experiment: {OUT}")

    frozen_calibration = prereg.get("frozen_calibration")
    seed_freeze = prereg.get("seed_freeze_record")
    if not isinstance(frozen_calibration, dict):
        raise RuntimeError("frozen calibration binding is missing")
    if (
        not isinstance(seed_freeze, dict)
        or seed_freeze.get("collision_free") is not True
    ):
        raise RuntimeError("seed freshness freeze record is missing or failed")
    calibration_result = CALIBRATION / "result.json"
    if not calibration_result.is_file():
        raise RuntimeError("calibration result is missing")
    if _sha256_file(calibration_result) != frozen_calibration.get("result_sha256"):
        raise RuntimeError("calibration result hash does not match frozen binding")

    recorder = ExperimentRecorder(EXPERIMENT_ID, output_dir=OUT, fail_fast=True)
    if recorder.manifest["git"].get("dirty") is not False:
        raise RuntimeError("efficiency evaluation requires a clean git tree")

    started = time.perf_counter()
    base_config = load_config()
    runs = [
        simulate(base_config, prereg, condition, int(seed))
        for seed in prereg["evaluation"]["seeds"]
        for condition in CONDITIONS
    ]
    summary = _summaries(runs)
    integrity = _integrity(runs, prereg)
    if integrity["pass"]:
        analysis = _analyze(runs, prereg)
    else:
        analysis = {
            "status": "NOT_TESTED_DENOMINATOR_VALIDITY",
            "decision_case": "NOT_TESTED",
            "primary_tests": [],
            "primary_multiple_testing": prereg["evaluation"]["multiple_testing"],
        }

    data_path = OUT / "data" / "evaluation.json"
    stats_path = OUT / "analysis" / "statistics.json"
    report_path = OUT / "report.md"
    _write_json(data_path, runs)
    _write_json(
        stats_path,
        {
            "schema_version": 1,
            "experiment_id": EXPERIMENT_ID,
            "claim_id": prereg["claim_id"],
            "condition_summary": summary,
            "analysis": analysis,
            "integrity": integrity,
            "claim_boundary": prereg["claim_boundary"],
        },
    )
    report_path.write_text(
        (
            f"# {EXPERIMENT_ID}\n\n"
            f"Status: `{analysis['status']}`\n\n"
            f"Decision case: `{analysis['decision_case']}`\n\n"
            f"Design integrity: {integrity['pass']}\n\n"
            "This execution creates DATA only. Human review and explicit EVID promotion "
            "remain separate.\n\n"
            f"## Claim boundary\n\n{prereg['claim_boundary']}\n"
        ),
        encoding="utf-8",
    )

    config_digest = _sha256_file(PREREG)
    prompt_digest = _sha256_bytes(b"NO_PROMPT_STAGE1_TOPOLOGY_EFFICIENCY_R1")
    analysis_digest = _sha256_bytes(
        b"8_TEST_SINGLE_HOLM_ONE_SIDED_SIGN_PAIRED_RATIO_BOOTSTRAP_DECISION_ABC"
    )
    recorder.record_config(str(PREREG.relative_to(ROOT)), config_digest)
    recorder.record_research_links(
        research_questions=[prereg["research_question"]],
        hypotheses=[prereg["hypothesis"]],
    )
    recorder.record_research_run_mode(ResearchRunMode.CONFIRMATORY)
    recorder.record_network_mode(NetworkMode.OFFLINE)
    recorder.record_data_partition(DataPartition.SCIENTIFIC_HOLDOUT)
    recorder.lock_confirmatory_run(
        protocol=prereg,
        prompt_digest=prompt_digest,
        analysis_digest=analysis_digest,
    )
    recorder.record_simulation_params(
        seeds=sorted(map(int, prereg["evaluation"]["seeds"])),
        dt_ms=1.0,
        neuron_count=64,
        edge_count=int(prereg["matched_budgets"]["expected_edge_count"]),
    )
    recorder.record_artifact("evaluation_data", "data/evaluation.json")
    recorder.record_artifact("statistics", "analysis/statistics.json")
    recorder.record_artifact("report", "report.md")
    recorder.record_provenance_digests(
        code_digest=_tracked_source_digest(),
        config_digest=config_digest,
        prompt_digest=prompt_digest,
        data_digest=_sha256_file(data_path),
    )
    recorder.record_results(
        claim_id=prereg["claim_id"],
        protocol=prereg["protocol"],
        result_status=analysis["status"],
        decision_case=analysis["decision_case"],
        design_integrity_passed=bool(integrity["pass"]),
        automatic_evidence_promotion=False,
        scientific_evidence=False,
        human_review_required=True,
        independent_authorship_replication=False,
    )
    recorder.record_runtime(time.perf_counter() - started)
    recorder.mark_completed().save()

    print(
        json.dumps(
            {
                "experiment_id": EXPERIMENT_ID,
                "status": analysis["status"],
                "decision_case": analysis["decision_case"],
                "runs": len(runs),
                "integrity": integrity["pass"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
