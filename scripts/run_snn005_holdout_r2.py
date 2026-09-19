#!/usr/bin/env python3
"""Execute preregistered SNN-005 held-out learning experiment."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

from src.research.empirical_evaluation import (
    holm_adjust,
    paired_summary,
    run_association_generalization,
)

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research/preregistrations/PREREG-SNN005-HOLDOUT-R2.json"
CONFIG = ROOT / "configs/learning_experiment.yaml"
EXP_ID = "EXP-SNN005-HOLDOUT-R2-20260919"
OUT = ROOT / "research/experiments" / EXP_ID
CONDITIONS = (
    "learning_on",
    "learning_off",
    "sham_replay",
    "weight_reset",
    "weight_shuffle",
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def serialize_run(run: Any) -> dict[str, Any]:
    return {
        "experiment_id": EXP_ID,
        "condition": str(run.condition),
        "seed": int(run.seed),
        "metrics": dict(run.metrics),
        "state_digest_before": str(run.state_digest_before),
        "state_digest_after": str(run.state_digest_after),
        "runtime_error": run.runtime_error,
    }


def main() -> int:
    prereg = read_json(PREREG)
    if prereg["execution_authorized"] is not True:
        raise RuntimeError("execution not authorized")
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
    seeds = tuple(int(seed) for seed in prereg["design"]["seeds"])
    raw_runs = run_association_generalization(config, seeds=seeds)
    runs = [serialize_run(run) for run in raw_runs]

    by_key = {(row["seed"], row["condition"]): row for row in runs}
    integrity_checks = {
        "clean_source_freeze": source["dirty_before_execution"] is False,
        "run_count": len(runs) == 80,
        "coverage": all(
            (seed, condition) in by_key for seed in seeds for condition in CONDITIONS
        ),
        "runtime_errors_absent": all(row["runtime_error"] is None for row in runs),
        "holdout_episode_count": all(
            int(row["metrics"]["actual_test_episodes"]) == 40 for row in runs
        ),
        "evaluation_ticks": all(
            int(row["metrics"]["evaluation_ticks_per_episode"]) == 12 for row in runs
        ),
        "teacher_absent_during_test": all(
            row["metrics"]["test_teacher_present"] is False for row in runs
        ),
        "learning_engine_detached_during_test": all(
            row["metrics"]["test_learning_engine_attached"] is False for row in runs
        ),
        "fresh_network_per_episode": all(
            row["metrics"]["fresh_network_per_test_episode"] is True for row in runs
        ),
        "weights_frozen_during_test": all(
            row["metrics"]["weight_digest_before_test"]
            == row["metrics"]["weight_digest_after_test"]
            for row in runs
        ),
        "matched_test_inputs_within_seed": all(
            len(
                {
                    by_key[(seed, condition)]["metrics"]["test_input_digest"]
                    for condition in CONDITIONS
                }
            )
            == 1
            for seed in seeds
        ),
    }
    integrity = {"checks": integrity_checks, "pass": all(integrity_checks.values())}

    accuracies = {
        condition: [
            float(by_key[(seed, condition)]["metrics"]["test_accuracy"])
            for seed in seeds
        ]
        for condition in CONDITIONS
    }
    controls = ("learning_off", "sham_replay", "weight_reset", "weight_shuffle")
    comparisons = []
    for index, control in enumerate(controls):
        summary = paired_summary(
            accuracies["learning_on"],
            accuracies[control],
            seed=910 + index,
        )
        if summary["exact_two_sided_sign_flip_p"] is None:
            raise RuntimeError("exact sign-flip p-value unexpectedly unavailable")
        comparisons.append(
            {
                "reference": "learning_on",
                "control": control,
                "metric": "test_accuracy",
                **summary,
            }
        )

    adjusted = holm_adjust(
        [float(row["exact_two_sided_sign_flip_p"]) for row in comparisons]
    )
    for row, p_adj in zip(comparisons, adjusted):
        row["holm_adjusted_p"] = p_adj

    by_control = {row["control"]: row for row in comparisons}
    primary = by_control["learning_off"]
    mean_accuracy = {
        condition: sum(values) / len(values) for condition, values in accuracies.items()
    }

    scientific_gates = {
        "primary_mean_difference": float(primary["mean_difference"]) >= 0.10,
        "primary_ci_excludes_zero": float(primary["bootstrap_percentile_95_ci"][0])
        > 0.0,
        "primary_holm_significant": float(primary["holm_adjusted_p"]) < 0.05,
        "learning_on_beats_all_control_means": all(
            mean_accuracy["learning_on"] > mean_accuracy[control]
            for control in controls
        ),
        "all_control_contrasts_positive": all(
            float(row["mean_difference"]) > 0.0 for row in comparisons
        ),
        "all_control_contrasts_holm_significant": all(
            float(row["holm_adjusted_p"]) < 0.05 for row in comparisons
        ),
    }

    if not integrity["pass"]:
        status = "NOT_TESTED_INTEGRITY_FAILURE"
    elif all(scientific_gates.values()):
        status = "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
    else:
        status = "NO_PREDEFINED_SUPPORT_DETECTED"

    data_path = OUT / "data/evaluation.json"
    stats_path = OUT / "analysis/statistics.json"
    write_json(data_path, runs)
    write_json(
        stats_path,
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "status": status,
            "integrity": integrity,
            "scientific_gates": scientific_gates,
            "mean_accuracy": mean_accuracy,
            "comparisons": comparisons,
            "claim_boundary": prereg["claim_boundary"],
        },
    )

    manifest = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "stage": 1,
        "research_question": "RQ-SNN-005",
        "hypothesis": "H-SNN-005-A",
        "protocol": prereg["protocol"],
        "experiment_status": "completed" if integrity["pass"] else "not_tested",
        "result_status": status,
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "human_review_status": "PENDING",
        "independent_replication": False,
        "source_freeze": source,
        "design": prereg["design"],
        "integrity": integrity,
        "scientific_gates": scientific_gates,
        "results": {
            "mean_accuracy": mean_accuracy,
            "primary_comparison": primary,
            "comparisons": comparisons,
        },
        "artifacts_sha256": {
            "preregistration": sha256(PREREG),
            "config": sha256(CONFIG),
            "runner_source": sha256(Path(__file__).resolve()),
            "canonical_association_source": sha256(
                ROOT / "src/research/empirical_evaluation.py"
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
            "research_question": "RQ-SNN-005",
            "hypothesis": "H-SNN-005-A",
            "reviewer_type_required": "human",
            "human_review_status": "PENDING",
            "scientific_evidence": False,
            "automatic_evidence_promotion": False,
            "independent_replication": False,
            "ai_review_does_not_satisfy_human_gate": True,
            "result_status": status,
            "questions": [
                "Are the five arms matched and are held-out test inputs identical within each seed?",
                "Are teacher and LearningEngine absent during every evaluation episode?",
                "Do the paired seed-level inference and Holm family match the preregistered analysis?",
                "Does the interpretation remain limited to this synthetic association task?",
            ],
        },
    )

    report = f"""# {EXP_ID}

RQ-SNN-005 / H-SNN-005-A

Status: **{status}**

Source freeze: {source["commit"]}
Runs: {len(runs)}
Seeds: {len(seeds)}
Holdout episodes per arm/seed: 40

Mean held-out accuracy:

{json.dumps(mean_accuracy, indent=2, sort_keys=True)}

Primary and robustness comparisons:

{json.dumps(comparisons, indent=2, sort_keys=True)}

Scientific gates:

{json.dumps(scientific_gates, indent=2, sort_keys=True)}

Claim boundary:

{prereg["claim_boundary"]}

Human review remains PENDING. No automatic EVID promotion or independent
replication is claimed.
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
        "".join(f"{digest}  {path}\n" for path, digest in sorted(checks.items())),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "experiment_id": EXP_ID,
                "status": status,
                "integrity": integrity["pass"],
                "mean_accuracy": mean_accuracy,
                "scientific_gates": scientific_gates,
                "primary_comparison": primary,
                "human_review_status": "PENDING",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
