#!/usr/bin/env python3
"""Execute the preregistered REC-002 clean-tree replication R2."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from src.research.followup_experiments import run_recurrence_scale

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research/preregistrations/PREREG-REC-002-CLEAN-R2.json"
CONFIG = ROOT / "configs/learning_experiment.yaml"
EXP_ID = "EXP-REC-002-CLEAN-R2-20260919"
OUT = ROOT / "research/experiments" / EXP_ID


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def serialise_run(run: Any) -> dict[str, Any]:
    return {
        "experiment_id": EXP_ID,
        "condition": str(run.condition),
        "seed": int(run.seed),
        "metrics": dict(run.metrics),
        "state_digest_before": str(run.state_digest_before),
        "state_digest_after": str(run.state_digest_after),
        "runtime_error": run.runtime_error,
    }


def signature(row: dict[str, Any]) -> tuple[int, int, int]:
    metrics = row["metrics"]
    return (
        int(metrics.get("last_response_latency", -1)),
        int(metrics.get("recurrent_events", -1)),
        int(metrics.get("propagation_depth", -1)),
    )


def analyse(runs: list[dict[str, Any]], prereg: dict[str, Any]) -> dict[str, Any]:
    seeds = [int(seed) for seed in prereg["seeds"]]
    expected = {"loop_delay_1", "loop_delay_2", "loop_delay_4", "loop_delay_8"}
    per_seed: list[dict[str, Any]] = []

    for seed in seeds:
        rows = [row for row in runs if int(row["seed"]) == seed]
        by_condition = {str(row["condition"]): row for row in rows}
        control = by_condition["loop_delay_1"]
        control_sig = signature(control)
        treatment_sigs = {
            name: signature(by_condition[name])
            for name in ("loop_delay_2", "loop_delay_4", "loop_delay_8")
        }
        each_differs_from_control = all(
            sig != control_sig for sig in treatment_sigs.values()
        )
        unique_treatment_signatures = len(set(treatment_sigs.values()))
        per_seed.append(
            {
                "seed": seed,
                "coverage_complete": set(by_condition) == expected,
                "control_signature": list(control_sig),
                "treatment_signatures": {
                    name: list(sig) for name, sig in treatment_sigs.items()
                },
                "each_treatment_differs_from_delay1": each_differs_from_control,
                "unique_treatment_signature_count": unique_treatment_signatures,
                "at_least_two_treatments_distinct": unique_treatment_signatures >= 2,
            }
        )

    gates = {
        "full_grid_every_seed": all(row["coverage_complete"] for row in per_seed),
        "every_treatment_differs_from_delay1": all(
            row["each_treatment_differs_from_delay1"] for row in per_seed
        ),
        "treatment_delays_not_all_identical": all(
            row["at_least_two_treatments_distinct"] for row in per_seed
        ),
    }
    summary = {
        "seed_count": len(seeds),
        "run_count": len(runs),
        "all_primary_gates_pass": all(gates.values()),
        "unique_primary_signatures": len({signature(row) for row in runs}),
        "condition_signatures": {},
    }
    for condition in sorted(expected):
        signatures = sorted(
            {signature(row) for row in runs if row["condition"] == condition}
        )
        summary["condition_signatures"][condition] = [list(sig) for sig in signatures]

    return {
        "status": (
            "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
            if all(gates.values())
            else "NO_PREDEFINED_SUPPORT_DETECTED"
        ),
        "gates": gates,
        "summary": summary,
        "per_seed": per_seed,
    }


def main() -> int:
    prereg = read_json(PREREG)
    if prereg.get("execution_authorized") is not True:
        raise RuntimeError("preregistration is not execution-authorized")
    if prereg.get("protocol") != "recurrence_scale_clean_r2":
        raise RuntimeError("unexpected protocol")
    if OUT.exists():
        raise RuntimeError(f"output already exists: {OUT}")

    source = {
        "commit": git("rev-parse", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "dirty_before_execution": bool(git("status", "--porcelain")),
    }
    if source["dirty_before_execution"]:
        raise RuntimeError("source tree must be clean before scientific execution")

    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    seeds = tuple(int(seed) for seed in prereg["seeds"])
    scientific_runs = run_recurrence_scale(config, seeds=seeds, ticks=256)
    runs = [serialise_run(run) for run in scientific_runs]

    expected_conditions = {"loop_delay_1", "loop_delay_2", "loop_delay_4", "loop_delay_8"}
    integrity_checks = {
        "clean_source_freeze": source["dirty_before_execution"] is False,
        "run_count": len(runs) == 80,
        "seed_count": {int(row["seed"]) for row in runs} == set(seeds),
        "condition_grid": {str(row["condition"]) for row in runs} == expected_conditions,
        "exact_coverage": all(
            sum(
                int(row["seed"]) == seed and str(row["condition"]) == condition
                for row in runs
            )
            == 1
            for seed in seeds
            for condition in expected_conditions
        ),
        "tick_contract": all(
            int(row["metrics"].get("ticks_requested", -1)) == 256 for row in runs
        ),
        "fixed_recurrent_weight": all(
            int(row["metrics"].get("loop_delay_ticks", -1)) in {1, 2, 4, 8}
            for row in runs
        ),
        "runtime_errors_absent": all(row["runtime_error"] is None for row in runs),
        "fresh_seeds": set(seeds).isdisjoint(range(101, 121))
        and set(seeds).isdisjoint(range(7301, 7321))
        and set(seeds).isdisjoint(range(7101, 7121)),
    }
    integrity = {"checks": integrity_checks, "pass": all(integrity_checks.values())}
    analysis = analyse(runs, prereg)
    if not integrity["pass"]:
        analysis["status"] = "NOT_TESTED_INTEGRITY_FAILURE"

    data_path = OUT / "data/evaluation.json"
    stats_path = OUT / "analysis/statistics.json"
    write_json(data_path, runs)
    write_json(
        stats_path,
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "analysis": analysis,
            "integrity": integrity,
            "inference_note": prereg["analysis_plan"]["inference_policy"],
            "claim_boundary": prereg["claim_boundary"],
        },
    )

    manifest = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "research_question": prereg["research_question"],
        "hypothesis": prereg["hypothesis"],
        "protocol": prereg["protocol"],
        "experiment_status": "completed" if integrity["pass"] else "not_tested",
        "result_status": analysis["status"],
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "human_review_status": "PENDING",
        "independent_replication": False,
        "source_freeze": source,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "os_name": os.name,
        },
        "design": {
            "seed_count": len(seeds),
            "run_count": len(runs),
            "ticks": 256,
            "recurrent_weight": 100.0,
            "delays": [1, 2, 4, 8],
        },
        "results": analysis["summary"],
        "primary_gates": analysis["gates"],
        "integrity": integrity,
        "artifacts_sha256": {
            "preregistration": sha256(PREREG),
            "parent_preregistration": sha256(
                ROOT / "research/preregistrations/PREREG-REC-002.json"
            ),
            "config": sha256(CONFIG),
            "runner_source": sha256(Path(__file__).resolve()),
            "canonical_recurrence_runner": sha256(
                ROOT / "src/research/followup_experiments.py"
            ),
            "evaluation_data": sha256(data_path),
            "statistics": sha256(stats_path),
        },
        "claim_boundary": prereg["claim_boundary"],
        "gate_protection": prereg["gate_protection"],
    }
    write_json(OUT / "manifest.json", manifest)
    write_json(
        OUT / "review_request.json",
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "reviewer_type_required": "human",
            "human_review_status": "PENDING",
            "scientific_evidence": False,
            "automatic_evidence_promotion": False,
            "independent_replication": False,
            "ai_review_does_not_satisfy_human_gate": True,
            "research_question": prereg["research_question"],
            "hypothesis": prereg["hypothesis"],
            "result_status": analysis["status"],
            "interpretation_boundary": prereg["claim_boundary"],
            "questions": [
                "Was the run executed on a clean source freeze with the complete 4-delay grid?",
                "Does every treatment delay differ from delay 1 in at least one preregistered primary outcome?",
                "Are at least two treatment-delay signatures distinct for every seed?",
                "Does the interpretation avoid monotonic-superiority, memory, cognition, scaling and independent-replication claims?",
            ],
        },
    )

    report = f"""# {EXP_ID}: REC-002 clean-tree R2

Research question: {prereg["research_question"]}  
Hypothesis: {prereg["hypothesis"]}  
Source freeze: {source["commit"]}  
Clean before execution: true  
Runs: {len(runs)}  
Data role: DATA only; no automatic EVID promotion.

## Reason for R2

The registered REC-002 delay ladder is a semantic DIRECT_MATCH, but the latest 20-seed confirmatory run was provenance-blocked by a dirty source tree. R2 repeats the same registered intervention on the current green source freeze using fresh seeds. Historical DATA are unchanged.

## Result

**Status: {analysis["status"]}**

Primary gates:

{json.dumps(analysis["gates"], indent=2, sort_keys=True)}

Condition signatures:

{json.dumps(analysis["summary"]["condition_signatures"], indent=2, sort_keys=True)}

## Inference boundary

{prereg["analysis_plan"]["inference_policy"]}

## Claim boundary

{prereg["claim_boundary"]}

## Gate protection

This experiment branch does not modify src/, configs/, tests/, research/schemas/ or pyproject.toml. Merge is permitted only after experiment verification and pull-request CI are green.

## Governance

Human review remains PENDING. This is not independently authored replication and does not create EVID automatically.
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
                "status": analysis["status"],
                "integrity": integrity["pass"],
                "runs": len(runs),
                "gates": analysis["gates"],
                "condition_signatures": analysis["summary"]["condition_signatures"],
                "human_review_status": "PENDING",
                "scientific_evidence": False,
                "independent_replication": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
