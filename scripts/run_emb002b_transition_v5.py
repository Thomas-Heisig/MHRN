#!/usr/bin/env python3
"""Run prospective transition-resolution DATA for H-EMB-002-B."""

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
PREREG = (
    ROOT
    / "research/preregistrations/PREREG-EMB002B-PROPRIOCEPTION-TRANSITION-V5.json"
)
CONFIG = ROOT / "configs/learning_experiment.yaml"
EXP_ID = "EXP-EMB002B-TRANSITION-V5-20260924"
OUT = ROOT / "research/experiments" / EXP_ID
EXPECTED_DELAYS = (0, 50, 60, 70, 80, 90, 100)
CONDITIONS = tuple(f"delay_{delay}" for delay in EXPECTED_DELAYS) + (
    "feedback_absent",
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


def compact(
    condition: str,
    seed: int,
    result: LoopResult,
    requested_delay_ticks: int | None,
) -> dict[str, Any]:
    metrics = result.metrics
    return {
        "experiment_id": EXP_ID,
        "condition": condition,
        "seed": seed,
        "requested_delay_ticks": requested_delay_ticks,
        "engine_proprioceptive_delay_ticks": int(
            metrics["proprioceptive_delay_ticks"]
        ),
        "ticks_requested": int(metrics["ticks_requested"]),
        "ticks_executed": int(metrics["ticks_executed"]),
        "tracking_rmse_rad": float(metrics["tracking_rmse_rad"]),
        "sensor_tape_sha256": digest(result.sensor_tape),
        "total_spikes": int(metrics["total_spikes"]),
        "synaptic_events_delivered": int(metrics["synaptic_events_delivered"]),
        "graph": metrics["graph"],
        "initial_body_state": metrics["gateway_state_before"]["body"],
        "final_body_state": metrics["gateway_state_after"]["body"],
        "state_digest_before": result.before,
        "state_digest_after": result.after,
        "runtime_error": result.error,
    }


def paired(
    rows: dict[tuple[int, str], dict[str, Any]],
    seeds: tuple[int, ...],
    control: str,
) -> dict[str, Any]:
    differences = [
        float(rows[(seed, control)]["tracking_rmse_rad"])
        - float(rows[(seed, "delay_0")]["tracking_rmse_rad"])
        for seed in seeds
    ]
    return {
        "metric": "tracking_rmse_rad",
        "reference": "delay_0",
        "control": control,
        "n_paired_seeds": len(differences),
        "differences_control_minus_delay_0": differences,
        "mean_difference": statistics.fmean(differences),
        "median_difference": statistics.median(differences),
        "minimum_difference": min(differences),
        "maximum_difference": max(differences),
        "fraction_delay_0_lower": (
            sum(value > 0.0 for value in differences) / len(differences)
        ),
        "ties": sum(value == 0.0 for value in differences),
        "p_value": None,
    }


def trace_matches_delay(result: LoopResult, delay_ticks: int) -> bool:
    trace = result.metrics["trace"]
    if len(trace) != len(result.sensor_tape):
        return False
    for index, point in enumerate(trace):
        expected = result.sensor_tape[max(0, index - delay_ticks)]
        if float(point["observed_q_rad"]) != float(expected[0]):
            return False
        if float(point["observed_omega_rad_s"]) != float(expected[1]):
            return False
    return True


def main() -> int:
    prereg = read_json(PREREG)
    if prereg.get("execution_authorized") is not True:
        raise RuntimeError("execution not authorized")
    if prereg.get("mode") != "PROSPECTIVE_TRANSITION_RESOLUTION":
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
    plan = prereg["analysis_plan"]
    seeds = tuple(int(seed) for seed in design["seeds"])
    delays = tuple(int(delay) for delay in design["delay_ticks"])
    ticks = int(design["ticks_per_run"])
    if delays != EXPECTED_DELAYS:
        raise RuntimeError("unexpected frozen delay grid")
    if ticks != 1000 or len(seeds) != 24 or len(set(seeds)) != 24:
        raise RuntimeError("unexpected frozen execution budget")

    raw: dict[tuple[int, str], LoopResult] = {}
    serialized: list[dict[str, Any]] = []
    for seed in seeds:
        for delay in delays:
            label = f"delay_{delay}"
            result = _simulate(
                config,
                seed,
                ticks,
                "delayed_proprioception",
                perturb=True,
                delay_ticks=delay,
            )
            raw[(seed, label)] = result
            serialized.append(compact(label, seed, result, delay))

        absent = _simulate(
            config,
            seed,
            ticks,
            "feedback_absent",
            perturb=True,
        )
        raw[(seed, "feedback_absent")] = absent
        serialized.append(compact("feedback_absent", seed, absent, None))

    rows = {
        (int(row["seed"]), str(row["condition"])): row for row in serialized
    }
    per_seed: dict[str, dict[str, bool]] = {}
    for seed in seeds:
        seed_rows = [rows[(seed, condition)] for condition in CONDITIONS]
        absent = raw[(seed, "feedback_absent")]
        per_seed[str(seed)] = {
            "same_initial_neural_state": (
                len({row["state_digest_before"] for row in seed_rows}) == 1
            ),
            "same_initial_body_state": (
                len(
                    {
                        digest(row["initial_body_state"])
                        for row in seed_rows
                    }
                )
                == 1
            ),
            "same_graph_fingerprint": (
                len({digest(row["graph"]) for row in seed_rows}) == 1
            ),
            "delay_metadata_exact": all(
                int(
                    rows[(seed, f"delay_{delay}")][
                        "engine_proprioceptive_delay_ticks"
                    ]
                )
                == delay
                for delay in delays
            ),
            "delay_observation_alignment_exact": all(
                trace_matches_delay(raw[(seed, f"delay_{delay}")], delay)
                for delay in delays
            ),
            "feedback_absent_observation_is_zero": all(
                float(point["observed_q_rad"]) == 0.0
                and float(point["observed_omega_rad_s"]) == 0.0
                for point in absent.metrics["trace"]
            ),
        }

    checks = {
        "clean_source_freeze": source["dirty_before_execution"] is False,
        "run_count": len(serialized) == 192,
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
    integrity = {
        "checks": checks,
        "per_seed": per_seed,
        "pass": all(checks.values()),
    }

    means = {
        condition: statistics.fmean(
            float(rows[(seed, condition)]["tracking_rmse_rad"])
            for seed in seeds
        )
        for condition in CONDITIONS
    }
    comparisons = {
        condition: paired(rows, seeds, condition)
        for condition in CONDITIONS
        if condition != "delay_0"
    }

    tolerance_margin = float(plan["tolerance_margin_rad"])
    degradation_margin = float(plan["degradation_margin_rad"])
    fraction_required = float(plan["degradation_fraction_required"])
    assay_margin = float(plan["assay_control_margin_rad"])

    primary_checks = {
        "delay_50_within_tolerance": (
            comparisons["delay_50"]["mean_difference"] <= tolerance_margin
        ),
        "delay_60_within_tolerance": (
            comparisons["delay_60"]["mean_difference"] <= tolerance_margin
        ),
        "delay_90_degraded": (
            comparisons["delay_90"]["mean_difference"] >= degradation_margin
            and comparisons["delay_90"]["fraction_delay_0_lower"]
            >= fraction_required
        ),
        "delay_100_degraded": (
            comparisons["delay_100"]["mean_difference"] >= degradation_margin
            and comparisons["delay_100"]["fraction_delay_0_lower"]
            >= fraction_required
        ),
    }
    assay_valid = (
        comparisons["feedback_absent"]["mean_difference"] >= assay_margin
        and comparisons["feedback_absent"]["fraction_delay_0_lower"] >= 0.95
    )

    qualifying = [
        delay
        for delay in delays
        if delay > 0
        and comparisons[f"delay_{delay}"]["mean_difference"]
        >= degradation_margin
        and comparisons[f"delay_{delay}"]["fraction_delay_0_lower"]
        >= fraction_required
    ]
    transition = {
        "earliest_registered_degraded_delay_ticks": (
            min(qualifying) if qualifying else None
        ),
        "qualifying_delays_ticks": qualifying,
        "localization_only_delays": list(design["localization_only_delays"]),
        "degradation_margin_rad": degradation_margin,
        "fraction_required": fraction_required,
    }

    support = integrity["pass"] and assay_valid and all(primary_checks.values())
    if not integrity["pass"]:
        result_status = "NOT_TESTED_INTEGRITY_FAILURE"
    elif support:
        result_status = "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
    else:
        result_status = "NOT_SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"

    data_path = OUT / "data/evaluation.json"
    stats_path = OUT / "analysis/statistics.json"
    write_json(data_path, serialized)
    write_json(
        stats_path,
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "analysis_mode": "prospective_transition_resolution",
            "result_status": result_status,
            "integrity": integrity,
            "mean_tracking_rmse_rad": means,
            "paired_comparisons": comparisons,
            "primary_checks": primary_checks,
            "assay_valid": assay_valid,
            "transition_localization": transition,
            "support_rule_satisfied": support,
            "p_values_computed": False,
            "confirmatory_thresholds_applied": True,
            "thresholds_frozen_before_v5_data": True,
            "claim_boundary": prereg["claim_boundary"],
        },
    )

    manifest = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "stage": 5,
        "research_question": "RQ-EMB-002",
        "hypothesis": "H-EMB-002-B",
        "protocol": prereg["protocol"],
        "experiment_status": (
            "completed" if integrity["pass"] else "not_tested"
        ),
        "result_status": result_status,
        "direct_test_of_hypothesis": True,
        "derived_from_exploratory_v4": True,
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
            "primary_checks": primary_checks,
            "assay_valid": assay_valid,
            "transition_localization": transition,
            "support_rule_satisfied": support,
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
            "hypothesis": "H-EMB-002-B",
            "reviewer_type_required": "human",
            "human_review_status": "PENDING",
            "scientific_evidence": False,
            "automatic_evidence_promotion": False,
            "ai_review_does_not_satisfy_human_gate": True,
            "result_status": result_status,
            "questions": [
                "Were seeds 925001-925024 fresh and disjoint from V3/V4?",
                "Were all registered delays applied exactly and verified against their same-run sensor tapes?",
                "Were all eight arms paired on the same initial neural/body state and graph per seed?",
                "Were the +0.01 rad tolerance and +0.03 rad degradation margins frozen before V5 DATA?",
                "Did both tolerance rules, both degradation rules and the feedback-absent assay-control rule pass?",
                "Is any transition claim restricted to this synthetic six-neuron fixture and the registered delay grid?",
            ],
        },
    )

    report = f"""# {EXP_ID}

RQ-EMB-002 / H-EMB-002-B

Status: **{result_status}**
Mode: **prospective transition-resolution synthetic DATA**

Runs: {len(serialized)}
Paired seeds: {len(seeds)}
Ticks per run: {ticks}
Frozen delays: {list(delays)}

## Mean tracking RMSE

{json.dumps(means, indent=2, sort_keys=True)}

## Primary rule checks

{json.dumps(primary_checks, indent=2, sort_keys=True)}

Assay validity: {assay_valid}
Support rule satisfied: {support}

## Paired comparisons versus delay_0

{json.dumps(comparisons, indent=2, sort_keys=True)}

## Transition localization

{json.dumps(transition, indent=2, sort_keys=True)}

## Integrity

{json.dumps(checks, indent=2, sort_keys=True)}

## Boundary

{prereg["claim_boundary"]}

No p-values were computed. The effect margins were frozen before V5 DATA.
Human Review remains PENDING. No automatic EVID promotion or independent
replication is claimed.
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
                "primary_checks": primary_checks,
                "assay_valid": assay_valid,
                "transition_localization": transition,
                "human_review_status": "PENDING",
                "scientific_evidence": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
