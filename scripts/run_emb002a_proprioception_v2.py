#!/usr/bin/env python3
"""Run prospective direct DATA for H-EMB-002-A."""

from __future__ import annotations

import hashlib
import json
import statistics
import subprocess
from pathlib import Path
from typing import Any

import yaml

from src.research.connectome_embodiment import LoopResult, _simulate

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research/preregistrations/PREREG-EMB002A-PROPRIOCEPTION-DIRECT-V2.json"
CONFIG = ROOT / "configs/learning_experiment.yaml"
EXP_ID = "EXP-EMB002A-PROPRIOCEPTION-V2-20260920"
OUT = ROOT / "research/experiments" / EXP_ID
CONDITIONS = (
    "closed_loop",
    "delayed_proprioception",
    "feedback_absent",
    "timing_shuffle",
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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


def compact(condition: str, seed: int, result: LoopResult) -> dict[str, Any]:
    m = result.metrics
    return {
        "experiment_id": EXP_ID,
        "condition": condition,
        "seed": seed,
        "ticks_requested": int(m["ticks_requested"]),
        "ticks_executed": int(m["ticks_executed"]),
        "tracking_rmse_rad": float(m["tracking_rmse_rad"]),
        "sensor_tape_sha256": digest(result.sensor_tape),
        "donor_tape_sha256": m.get("donor_tape_sha256"),
        "total_spikes": int(m["total_spikes"]),
        "synaptic_events_delivered": int(m["synaptic_events_delivered"]),
        "graph": m["graph"],
        "initial_body_state": m["gateway_state_before"]["body"],
        "final_body_state": m["gateway_state_after"]["body"],
        "state_digest_before": result.before,
        "state_digest_after": result.after,
        "runtime_error": result.error,
    }


def paired(rows: dict[tuple[int, str], dict[str, Any]], seeds: tuple[int, ...], control: str) -> dict[str, Any]:
    diffs = [
        float(rows[(seed, control)]["tracking_rmse_rad"])
        - float(rows[(seed, "closed_loop")]["tracking_rmse_rad"])
        for seed in seeds
    ]
    return {
        "metric": "tracking_rmse_rad",
        "reference": "closed_loop",
        "control": control,
        "n_paired_seeds": len(diffs),
        "differences_control_minus_closed_loop": diffs,
        "mean_difference": statistics.fmean(diffs),
        "median_difference": statistics.median(diffs),
        "minimum_difference": min(diffs),
        "maximum_difference": max(diffs),
        "fraction_closed_loop_lower": sum(value > 0.0 for value in diffs) / len(diffs),
        "ties": sum(value == 0.0 for value in diffs),
        "p_value": None,
        "confirmatory_threshold_applied": False,
    }


def main() -> int:
    prereg = read_json(PREREG)
    if prereg.get("execution_authorized") is not True:
        raise RuntimeError("execution not authorized")
    if prereg.get("mode") != "PROSPECTIVE_DIRECT_DATA":
        raise RuntimeError("unexpected preregistration mode")
    if OUT.exists():
        raise RuntimeError(f"output already exists: {OUT}")

    source = {
        "commit": git("rev-parse", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "dirty_before_execution": bool(
            git("status", "--porcelain", "--untracked-files=all")
        ),
    }
    if source["dirty_before_execution"]:
        raise RuntimeError("source worktree must be clean before execution")

    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    design = prereg["design"]
    seeds = tuple(int(seed) for seed in design["seeds"])
    ticks = int(design["ticks_per_run"])
    if ticks != 1000 or len(seeds) != 20 or len(set(seeds)) != 20:
        raise RuntimeError("unexpected frozen execution budget")

    raw: dict[tuple[int, str], LoopResult] = {}
    serialized: list[dict[str, Any]] = []
    for seed in seeds:
        closed = _simulate(config, seed, ticks, "closed_loop", perturb=True)
        delayed = _simulate(config, seed, ticks, "delayed_proprioception", perturb=True)
        absent = _simulate(config, seed, ticks, "feedback_absent", perturb=True)
        shuffled = _simulate(
            config,
            seed,
            ticks,
            "timing_shuffle",
            donor=closed,
            perturb=True,
        )
        seed_results = {
            "closed_loop": closed,
            "delayed_proprioception": delayed,
            "feedback_absent": absent,
            "timing_shuffle": shuffled,
        }
        for condition in CONDITIONS:
            result = seed_results[condition]
            raw[(seed, condition)] = result
            serialized.append(compact(condition, seed, result))

    rows = {(int(row["seed"]), str(row["condition"])): row for row in serialized}
    per_seed: dict[str, dict[str, bool]] = {}
    for seed in seeds:
        seed_rows = [rows[(seed, condition)] for condition in CONDITIONS]
        absent = raw[(seed, "feedback_absent")]
        shuffled = raw[(seed, "timing_shuffle")]
        closed = raw[(seed, "closed_loop")]
        per_seed[str(seed)] = {
            "same_initial_neural_state": len(
                {row["state_digest_before"] for row in seed_rows}
            )
            == 1,
            "same_initial_body_state": len(
                {digest(row["initial_body_state"]) for row in seed_rows}
            )
            == 1,
            "same_graph_fingerprint": len(
                {digest(row["graph"]) for row in seed_rows}
            )
            == 1,
            "timing_shuffle_uses_same_seed_closed_loop_donor": (
                shuffled.metrics.get("donor_tape_sha256")
                == digest(closed.sensor_tape)
            ),
            "feedback_absent_observation_is_zero": all(
                float(point["observed_q_rad"]) == 0.0
                and float(point["observed_omega_rad_s"]) == 0.0
                for point in absent.metrics["trace"]
            ),
        }

    checks = {
        "clean_source_freeze": source["dirty_before_execution"] is False,
        "run_count": len(serialized) == 80,
        "coverage": all(
            (seed, condition) in rows
            for seed in seeds
            for condition in CONDITIONS
        ),
        "runtime_errors_absent": all(
            row["runtime_error"] is None for row in serialized
        ),
        "all_ticks_complete": all(
            int(row["ticks_executed"]) == ticks for row in serialized
        ),
        "all_seed_pairing_checks": all(
            all(values.values()) for values in per_seed.values()
        ),
    }
    integrity = {"checks": checks, "per_seed": per_seed, "pass": all(checks.values())}

    means = {
        condition: statistics.fmean(
            float(rows[(seed, condition)]["tracking_rmse_rad"]) for seed in seeds
        )
        for condition in CONDITIONS
    }
    comparisons = [
        paired(rows, seeds, "delayed_proprioception"),
        paired(rows, seeds, "feedback_absent"),
        paired(rows, seeds, "timing_shuffle"),
    ]
    primary = comparisons[:2]
    data_support = (
        integrity["pass"]
        and all(item["mean_difference"] > 0.0 for item in primary)
        and all(item["fraction_closed_loop_lower"] > 0.5 for item in primary)
    )
    result_status = (
        "SUPPORTED_WITHIN_PREREGISTERED_DATA_RULE"
        if data_support
        else "NOT_SUPPORTED_WITHIN_PREREGISTERED_DATA_RULE"
    )
    if not integrity["pass"]:
        result_status = "NOT_TESTED_INTEGRITY_FAILURE"

    data_path = OUT / "data/evaluation.json"
    stats_path = OUT / "analysis/statistics.json"
    write_json(data_path, serialized)
    write_json(
        stats_path,
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "analysis_mode": "prospective_direct_descriptive",
            "result_status": result_status,
            "integrity": integrity,
            "mean_tracking_rmse_rad": means,
            "paired_comparisons": comparisons,
            "primary_data_support_rule_satisfied": data_support,
            "p_values_computed": False,
            "confirmatory_thresholds_applied": False,
            "claim_boundary": prereg["claim_boundary"],
        },
    )

    manifest = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "stage": 5,
        "research_question": "RQ-EMB-002",
        "hypothesis": "H-EMB-002-A",
        "protocol": prereg["protocol"],
        "experiment_status": "completed" if integrity["pass"] else "not_tested",
        "result_status": result_status,
        "direct_test_of_hypothesis": True,
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "human_review_status": "PENDING",
        "independent_replication": False,
        "source_freeze": source,
        "design": design,
        "integrity": integrity,
        "results": {
            "mean_tracking_rmse_rad": means,
            "paired_comparisons": comparisons,
            "primary_data_support_rule_satisfied": data_support,
        },
        "artifacts_sha256": {
            "preregistration": sha256(PREREG),
            "config": sha256(CONFIG),
            "runner_source": sha256(Path(__file__).resolve()),
            "canonical_embodiment_source": sha256(
                ROOT / "src/research/connectome_embodiment.py"
            ),
            "evaluation_data": sha256(data_path),
            "statistics": sha256(stats_path),
        },
        "claim_boundary": prereg["claim_boundary"],
    }
    write_json(OUT / "manifest.json", manifest)
    write_json(
        OUT / "review_request.json",
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "research_question": "RQ-EMB-002",
            "hypothesis": "H-EMB-002-A",
            "reviewer_type_required": "human",
            "human_review_status": "PENDING",
            "scientific_evidence": False,
            "automatic_evidence_promotion": False,
            "ai_review_does_not_satisfy_human_gate": True,
            "result_status": result_status,
            "questions": [
                "Was the 20-tick proprioceptive delay applied exactly as preregistered?",
                "Were all four arms paired on the same initial neural/body state per seed?",
                "Does the timing-shuffle arm use only the same-seed intact donor tape?",
                "Do both primary contrasts satisfy the preregistered DATA-only support rule?",
                "Is interpretation limited to the fixed synthetic six-neuron fixture?"
            ]
        },
    )
    report = f"""# {EXP_ID}

RQ-EMB-002 / H-EMB-002-A

Status: **{result_status}**
Mode: **prospective direct synthetic DATA**

Runs: {len(serialized)}
Paired seeds: {len(seeds)}
Ticks per run: {ticks}

## Mean tracking RMSE

{json.dumps(means, indent=2, sort_keys=True)}

## Paired comparisons

{json.dumps(comparisons, indent=2, sort_keys=True)}

## Integrity

{json.dumps(checks, indent=2, sort_keys=True)}

## Boundary

{prereg["claim_boundary"]}

Human Review remains PENDING. No p-values were computed. No automatic EVID
promotion or independent replication is claimed.
"""
    (OUT / "report.md").write_text(report, encoding="utf-8")

    checksums = {
        "analysis/statistics.json": sha256(stats_path),
        "data/evaluation.json": sha256(data_path),
        "manifest.json": sha256(OUT / "manifest.json"),
        "report.md": sha256(OUT / "report.md"),
        "review_request.json": sha256(OUT / "review_request.json"),
    }
    (OUT / "checksums.sha256").write_text(
        "".join(
            f"{digest_value}  {path}\n"
            for path, digest_value in sorted(checksums.items())
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "experiment_id": EXP_ID,
                "result_status": result_status,
                "integrity": integrity["pass"],
                "run_count": len(serialized),
                "means": means,
                "comparisons": comparisons,
                "human_review_status": "PENDING",
                "scientific_evidence": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
