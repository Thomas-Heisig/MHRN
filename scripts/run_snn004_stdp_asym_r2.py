#!/usr/bin/env python3
"""Execute preregistered SNN-004 STDP asymmetry clean R2."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from src.research.stdp_pair_timing import (
    DELTA_T_MS,
    INITIAL_WEIGHT,
    PARAMETERS,
    REPLICATIONS,
    run_pair_timing_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research/preregistrations/PREREG-SNN004-STDP-ASYM-R2.json"
EXP_ID = "EXP-SNN004-STDP-ASYM-R2-20260919"
OUT = ROOT / "research/experiments" / EXP_ID


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


def main() -> int:
    prereg = read_json(PREREG)
    if prereg["execution_authorized"] is not True:
        raise RuntimeError("execution not authorized")
    if OUT.exists():
        raise RuntimeError(f"output already exists: {OUT}")

    source = {
        "commit": git("rev-parse", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "dirty_before_execution": bool(git("status", "--porcelain")),
    }
    if source["dirty_before_execution"]:
        raise RuntimeError("source tree must be clean")

    result = run_pair_timing_protocol()
    rows = result["measurements"]
    by_dt = {int(row["delta_t_ms"]): row for row in rows}

    mirror_checks = {}
    for dt in (1, 5, 10, 20, 50):
        pos = float(by_dt[dt]["mean_delta_weight"])
        neg = float(by_dt[-dt]["mean_delta_weight"])
        mirror_checks[str(dt)] = {
            "positive_delta": pos,
            "negative_delta": neg,
            "absolute_ltd_exceeds_ltp": abs(neg) > pos,
        }

    gates = {
        "complete_timing_grid": set(by_dt) == set(DELTA_T_MS),
        "replication_count": all(
            int(row["repeated_evaluations"]) == REPLICATIONS for row in rows
        ),
        "positive_dt_potentiates": all(
            float(by_dt[dt]["mean_delta_weight"]) > 0
            for dt in DELTA_T_MS
            if dt > 0
        ),
        "negative_dt_depresses": all(
            float(by_dt[dt]["mean_delta_weight"]) < 0
            for dt in DELTA_T_MS
            if dt < 0
        ),
        "zero_dt_unchanged": float(by_dt[0]["mean_delta_weight"]) == 0.0,
        "mirror_asymmetry": all(
            bool(item["absolute_ltd_exceeds_ltp"])
            for item in mirror_checks.values()
        ),
        "deterministic_identity": bool(result["summary"]["deterministic_identity"]),
        "mean_direction_and_asymmetry": (
            float(result["summary"]["mean_ltp"]) > 0
            and float(result["summary"]["mean_ltd"]) < 0
            and abs(float(result["summary"]["mean_ltd"]))
            > float(result["summary"]["mean_ltp"])
        ),
    }

    integrity_checks = {
        "clean_source_freeze": source["dirty_before_execution"] is False,
        "protocol_id": result["protocol"] == "stdp_pair_timing_v1",
        "initial_weight": float(result["conditions"]["initial_weight"]) == INITIAL_WEIGHT,
        "replications": int(
            result["conditions"]["repeated_evaluations_per_condition"]
        )
        == REPLICATIONS,
        "independent_runs_zero": int(
            result["conditions"]["independent_runs_per_condition"]
        )
        == 0,
        "parameter_match": result["conditions"]["parameters"] == PARAMETERS.to_dict(),
    }
    integrity = {"checks": integrity_checks, "pass": all(integrity_checks.values())}

    status = (
        "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
        if integrity["pass"] and all(gates.values())
        else (
            "NOT_TESTED_INTEGRITY_FAILURE"
            if not integrity["pass"]
            else "NO_PREDEFINED_SUPPORT_DETECTED"
        )
    )

    data_path = OUT / "data/evaluation.json"
    stats_path = OUT / "analysis/statistics.json"
    write_json(data_path, result)
    write_json(
        stats_path,
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "status": status,
            "primary_gates": gates,
            "mirror_checks": mirror_checks,
            "summary": result["summary"],
            "integrity": integrity,
            "claim_boundary": prereg["claim_boundary"],
        },
    )

    manifest = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "stage": 1,
        "research_question": "RQ-SNN-004",
        "hypothesis": "H-SNN-004-A",
        "claim_id": "CLAIM-SNN-001",
        "protocol": prereg["protocol"],
        "experiment_status": "completed" if integrity["pass"] else "not_tested",
        "result_status": status,
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "human_review_status": "PENDING",
        "independent_replication": False,
        "source_freeze": source,
        "design": prereg["design"],
        "primary_gates": gates,
        "integrity": integrity,
        "results": {
            "mean_ltp": result["summary"]["mean_ltp"],
            "mean_ltd": result["summary"]["mean_ltd"],
            "zero_delta_weight": result["summary"]["zero_delta_weight"],
            "conditions": result["summary"]["conditions"],
            "repeated_evaluations": result["summary"]["repeated_evaluations"],
        },
        "artifacts_sha256": {
            "preregistration": sha256(PREREG),
            "runner_source": sha256(Path(__file__).resolve()),
            "canonical_stdp_pair_source": sha256(
                ROOT / "src/research/stdp_pair_timing.py"
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
            "research_question": "RQ-SNN-004",
            "hypothesis": "H-SNN-004-A",
            "claim_id": "CLAIM-SNN-001",
            "reviewer_type_required": "human",
            "human_review_status": "PENDING",
            "scientific_evidence": False,
            "automatic_evidence_promotion": False,
            "independent_replication": False,
            "ai_review_does_not_satisfy_human_gate": True,
            "result_status": status,
            "questions": [
                "Does the registered timing curve directly test the scoped pair-based STDP asymmetry claim?",
                "Are positive, negative and zero timing controls interpreted correctly?",
                "Is the mirror-pair magnitude asymmetry appropriately tied to the frozen a_minus > a_plus parameterization?",
                "Does the interpretation remain below any functional-learning, memory or biological-equivalence claim?",
            ],
        },
    )

    report = f"""# {EXP_ID}

RQ-SNN-004 / H-SNN-004-A

Status: **{status}**

- source freeze: {source["commit"]}
- clean tree: true
- timing conditions: {len(rows)}
- repeated evaluations: {result["summary"]["repeated_evaluations"]}
- independent runs: {result["summary"]["independent_runs"]}
- mean LTP: {result["summary"]["mean_ltp"]}
- mean LTD: {result["summary"]["mean_ltd"]}
- zero-delta change: {result["summary"]["zero_delta_weight"]}

Primary gates:

{json.dumps(gates, indent=2, sort_keys=True)}

Claim boundary:

{prereg["claim_boundary"]}

Human review remains PENDING. This DATA artifact does not create EVID automatically.
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
                "gates": gates,
                "mean_ltp": result["summary"]["mean_ltp"],
                "mean_ltd": result["summary"]["mean_ltd"],
                "human_review_status": "PENDING",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
