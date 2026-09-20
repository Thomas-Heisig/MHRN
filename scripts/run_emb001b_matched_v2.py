#!/usr/bin/env python3
"""Run prospective matched-disturbance exploratory DATA for H-EMB-001-B."""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import subprocess
from pathlib import Path
from typing import Any

import yaml

from src.research.connectome_embodiment import LoopResult, _simulate

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research/preregistrations/PREREG-EMB001B-MATCHED-V2.json"
CONFIG = ROOT / "configs/learning_experiment.yaml"
EXP_ID = "EXP-EMB001B-MATCHED-V2-20260920"
OUT = ROOT / "research/experiments" / EXP_ID
CONDITIONS = ("closed_loop", "yoked_replay", "feedback_absent")


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


def digest_value(value: Any) -> str:
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


def sensor_metrics(result: LoopResult) -> dict[str, Any]:
    q_values = [float(pair[0]) for pair in result.sensor_tape]
    return {
        "sensor_tape_sha256": digest_value(result.sensor_tape),
        "motor_tape_sha256": digest_value(result.motor_tape),
        "sensor_path_mean_abs_q_rad": (
            sum(abs(value) for value in q_values) / len(q_values) if q_values else None
        ),
        "sensor_path_rms_q_rad": (
            math.sqrt(sum(value * value for value in q_values) / len(q_values))
            if q_values
            else None
        ),
    }


def compact_run(
    condition: str,
    seed: int,
    result: LoopResult,
    perturbation_sha256: str,
) -> dict[str, Any]:
    metrics = result.metrics
    sensory = sensor_metrics(result)
    return {
        "experiment_id": EXP_ID,
        "condition": condition,
        "seed": seed,
        "ticks_requested": int(metrics["ticks_requested"]),
        "ticks_executed": int(metrics["ticks_executed"]),
        "tracking_rmse_rad": float(metrics["tracking_rmse_rad"]),
        "sensor_path_mean_abs_q_rad": sensory["sensor_path_mean_abs_q_rad"],
        "sensor_path_rms_q_rad": sensory["sensor_path_rms_q_rad"],
        "sensor_tape_sha256": sensory["sensor_tape_sha256"],
        "motor_tape_sha256": sensory["motor_tape_sha256"],
        "donor_tape_sha256": metrics.get("donor_tape_sha256"),
        "total_spikes": int(metrics["total_spikes"]),
        "activated_neuron_count": int(metrics["activated_neuron_count"]),
        "synaptic_events_delivered": int(metrics["synaptic_events_delivered"]),
        "nonzero_action_ticks": int(metrics["nonzero_action_ticks"]),
        "graph": metrics["graph"],
        "initial_body_state": metrics["gateway_state_before"]["body"],
        "final_body_state": metrics["gateway_state_after"]["body"],
        "state_digest_before": result.before,
        "state_digest_after": result.after,
        "closed_loop_state_sha256": metrics["closed_loop_state_sha256"],
        "external_perturbation_schedule_sha256": perturbation_sha256,
        "runtime_error": result.error,
    }


def paired_descriptive(
    rows: dict[tuple[int, str], dict[str, Any]],
    seeds: tuple[int, ...],
    control: str,
    metric: str,
) -> dict[str, Any]:
    differences = [
        float(rows[(seed, control)][metric])
        - float(rows[(seed, "closed_loop")][metric])
        for seed in seeds
    ]
    return {
        "metric": metric,
        "reference": "closed_loop",
        "control": control,
        "n_paired_seeds": len(differences),
        "differences_control_minus_closed_loop": differences,
        "mean_difference": statistics.fmean(differences),
        "median_difference": statistics.median(differences),
        "minimum_difference": min(differences),
        "maximum_difference": max(differences),
        "fraction_closed_loop_lower": sum(value > 0.0 for value in differences)
        / len(differences),
        "ties": sum(value == 0.0 for value in differences),
        "p_value": None,
        "confirmatory_threshold_applied": False,
    }


def main() -> int:
    prereg = read_json(PREREG)
    if prereg.get("execution_authorized") is not True:
        raise RuntimeError("execution not authorized")
    if prereg.get("mode") != "PROSPECTIVE_EXPLORATORY_MATCHED_DISTURBANCE":
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

    perturbation_schedule = [
        0.003 if ticks // 4 <= tick < ticks // 2 else 0.0
        for tick in range(ticks)
    ]
    perturbation_sha256 = digest_value(perturbation_schedule)

    raw: dict[tuple[int, str], LoopResult] = {}
    serialized: list[dict[str, Any]] = []
    for seed in seeds:
        closed = _simulate(config, seed, ticks, "closed_loop", perturb=True)
        yoked = _simulate(
            config,
            seed,
            ticks,
            "yoked_replay",
            donor=closed,
            perturb=True,
        )
        absent = _simulate(config, seed, ticks, "feedback_absent", perturb=True)
        seed_results = {
            "closed_loop": closed,
            "yoked_replay": yoked,
            "feedback_absent": absent,
        }
        for condition in CONDITIONS:
            result = seed_results[condition]
            raw[(seed, condition)] = result
            serialized.append(
                compact_run(condition, seed, result, perturbation_sha256)
            )

    rows = {(int(row["seed"]), str(row["condition"])): row for row in serialized}
    per_seed_integrity: dict[str, dict[str, bool]] = {}
    for seed in seeds:
        closed = raw[(seed, "closed_loop")]
        yoked = raw[(seed, "yoked_replay")]
        absent = raw[(seed, "feedback_absent")]
        compact = [rows[(seed, condition)] for condition in CONDITIONS]
        per_seed_integrity[str(seed)] = {
            "same_initial_neural_state": len(
                {row["state_digest_before"] for row in compact}
            )
            == 1,
            "same_initial_body_state": len(
                {digest_value(row["initial_body_state"]) for row in compact}
            )
            == 1,
            "same_graph_fingerprint": len(
                {digest_value(row["graph"]) for row in compact}
            )
            == 1,
            "yoked_uses_actual_perturbed_closed_loop_sensor_tape": (
                yoked.metrics.get("donor_tape_sha256")
                == digest_value(closed.sensor_tape)
            ),
            "feedback_absent_observation_is_zero": all(
                float(point["observed_q_rad"]) == 0.0
                and float(point["observed_omega_rad_s"]) == 0.0
                for point in absent.metrics["trace"]
            ),
            "complete_sensor_tapes": (
                len(closed.sensor_tape) == ticks
                and len(yoked.sensor_tape) == ticks
                and len(absent.sensor_tape) == ticks
            ),
        }

    integrity_checks = {
        "clean_source_freeze": source["dirty_before_execution"] is False,
        "run_count": len(serialized) == len(seeds) * len(CONDITIONS),
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
        "identical_perturbation_contract": all(
            row["external_perturbation_schedule_sha256"] == perturbation_sha256
            for row in serialized
        ),
        "all_seed_pairing_checks": all(
            all(checks.values()) for checks in per_seed_integrity.values()
        ),
    }
    integrity = {
        "checks": integrity_checks,
        "per_seed": per_seed_integrity,
        "pass": all(integrity_checks.values()),
    }

    mean_outcomes: dict[str, dict[str, float]] = {}
    for condition in CONDITIONS:
        condition_rows = [rows[(seed, condition)] for seed in seeds]
        mean_outcomes[condition] = {
            "tracking_rmse_rad": statistics.fmean(
                float(row["tracking_rmse_rad"]) for row in condition_rows
            ),
            "sensor_path_rms_q_rad": statistics.fmean(
                float(row["sensor_path_rms_q_rad"]) for row in condition_rows
            ),
            "sensor_path_mean_abs_q_rad": statistics.fmean(
                float(row["sensor_path_mean_abs_q_rad"]) for row in condition_rows
            ),
        }

    comparisons = []
    for control in ("yoked_replay", "feedback_absent"):
        comparisons.append(
            paired_descriptive(rows, seeds, control, "tracking_rmse_rad")
        )
        comparisons.append(
            paired_descriptive(rows, seeds, control, "sensor_path_rms_q_rad")
        )

    status = (
        "COMPLETED_EXPLORATORY_DATA"
        if integrity["pass"]
        else "NOT_TESTED_INTEGRITY_FAILURE"
    )

    data_path = OUT / "data/evaluation.json"
    stats_path = OUT / "analysis/statistics.json"
    write_json(data_path, serialized)
    write_json(
        stats_path,
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "status": status,
            "analysis_mode": "preregistered_descriptive_exploratory",
            "integrity": integrity,
            "mean_outcomes": mean_outcomes,
            "paired_comparisons": comparisons,
            "p_values_computed": False,
            "confirmatory_thresholds_applied": False,
            "claim_boundary": prereg["claim_boundary"],
        },
    )

    manifest = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "stage": 5,
        "research_question": "RQ-EMB-001",
        "hypothesis": "H-EMB-001-B",
        "protocol": prereg["protocol"],
        "experiment_status": "completed" if integrity["pass"] else "not_tested",
        "result_status": status,
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "human_review_status": "PENDING",
        "independent_replication": False,
        "source_freeze": source,
        "design": design,
        "integrity": integrity,
        "results": {
            "mean_outcomes": mean_outcomes,
            "paired_comparisons": comparisons,
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
            "research_question": "RQ-EMB-001",
            "hypothesis": "H-EMB-001-B",
            "reviewer_type_required": "human",
            "human_review_status": "PENDING",
            "scientific_evidence": False,
            "automatic_evidence_promotion": False,
            "independent_replication": False,
            "ai_review_does_not_satisfy_human_gate": True,
            "result_status": status,
            "questions": [
                "Are all three arms exposed to the identical external perturbation schedule?",
                "Does yoked_replay use the actual perturbation-exposed closed_loop sensor tape from the same seed?",
                "Are initial neural state, body state and graph fingerprint matched within every seed?",
                "Does the analysis remain descriptive and exploratory without post-hoc confirmatory thresholds?",
                "Does the interpretation remain limited to the synthetic six-neuron fixed-decoder embodiment fixture?"
            ]
        },
    )

    report = f"""# {EXP_ID}

RQ-EMB-001 / H-EMB-001-B

Status: **{status}**
Mode: **prospective exploratory matched-disturbance DATA**

Source freeze: {source["commit"]}
Runs: {len(serialized)}
Paired seeds: {len(seeds)}
Ticks per run: {ticks}

## Mean outcomes

{json.dumps(mean_outcomes, indent=2, sort_keys=True)}

## Paired descriptive comparisons

Positive control-minus-closed_loop differences mean lower error in the
closed-loop arm.

{json.dumps(comparisons, indent=2, sort_keys=True)}

## Integrity

{json.dumps(integrity_checks, indent=2, sort_keys=True)}

## Boundary

{prereg["claim_boundary"]}

Human Review remains PENDING. No p-values or confirmatory support thresholds
were applied. No automatic EVID promotion or independent replication is claimed.
"""
    (OUT / "report.md").write_text(report, encoding="utf-8")

    checks = {
        "analysis/statistics.json": sha256(stats_path),
        "data/evaluation.json": sha256(data_path),
        "manifest.json": sha256(OUT / "manifest.json"),
        "report.md": sha256(OUT / "report.md"),
        "review_request.json": sha256(OUT / "review_request.json"),
    }
    (OUT / "checksums.sha256").write_text(
        "".join(
            f"{digest}  {path}\n"
            for path, digest in sorted(checks.items())
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "experiment_id": EXP_ID,
                "status": status,
                "integrity": integrity["pass"],
                "run_count": len(serialized),
                "mean_outcomes": mean_outcomes,
                "paired_comparisons": comparisons,
                "human_review_status": "PENDING",
                "scientific_evidence": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
