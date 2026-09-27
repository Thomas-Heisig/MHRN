#!/usr/bin/env python3
"""Verify Stage-1 topology efficiency R1 confirmatory DATA."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from run_stage1_topology_efficiency_r1 import (
    CALIBRATION,
    CONDITIONS,
    EXPERIMENT_ID,
    OUT,
    PREREG,
    _analyze,
    _integrity,
    _sha256_file,
    _summaries,
)

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    required = [
        OUT / "manifest.json",
        OUT / "report.md",
        OUT / "data" / "evaluation.json",
        OUT / "analysis" / "statistics.json",
        PREREG,
        CALIBRATION / "result.json",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(ROOT)}")
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1

    prereg = read_json(PREREG)
    manifest = read_json(OUT / "manifest.json")
    runs_raw = read_json(OUT / "data" / "evaluation.json")
    statistics = read_json(OUT / "analysis" / "statistics.json")
    runs = [dict(row) for row in runs_raw if isinstance(row, dict)]

    if prereg.get("status") != "FROZEN_BEFORE_EFFICIENCY_EVALUATION":
        errors.append("preregistration is not frozen")
    if prereg.get("execution_authorized") is not True:
        errors.append("execution is not authorized")

    frozen_calibration = prereg.get("frozen_calibration", {})
    if _sha256_file(CALIBRATION / "result.json") != frozen_calibration.get(
        "result_sha256"
    ):
        errors.append("frozen calibration hash mismatch")
    seed_freeze = prereg.get("seed_freeze_record", {})
    if seed_freeze.get("collision_free") is not True:
        errors.append("seed freeze record is not collision-free")

    if len(runs) != 120:
        errors.append(f"expected 120 evaluation runs, got {len(runs)}")
    seeds = set(map(int, prereg["evaluation"]["seeds"]))
    for condition in CONDITIONS:
        if sum(row["condition"] == condition for row in runs) != len(seeds):
            errors.append(f"condition coverage mismatch: {condition}")

    recomputed_summary = _summaries(runs)
    recomputed_integrity = _integrity(runs, prereg)
    if recomputed_integrity["pass"]:
        recomputed_analysis = _analyze(runs, prereg)
    else:
        recomputed_analysis = {
            "status": "NOT_TESTED_DENOMINATOR_VALIDITY",
            "decision_case": "NOT_TESTED",
            "primary_tests": [],
            "primary_multiple_testing": prereg["evaluation"]["multiple_testing"],
        }

    if statistics.get("condition_summary") != recomputed_summary:
        errors.append("condition summary differs from deterministic recomputation")
    if statistics.get("integrity") != recomputed_integrity:
        errors.append("integrity differs from deterministic recomputation")
    if statistics.get("analysis") != recomputed_analysis:
        errors.append("analysis differs from deterministic recomputation")

    if recomputed_integrity["pass"] and len(recomputed_analysis["primary_tests"]) != 8:
        errors.append("primary Holm family does not contain exactly 8 tests")

    if manifest.get("experiment_id") != EXPERIMENT_ID:
        errors.append("manifest experiment id mismatch")
    if manifest.get("experiment_status") != "completed":
        errors.append("manifest experiment status is not completed")
    if manifest.get("validity", {}).get("valid") is not True:
        errors.append("manifest validity.valid is not true")
    if manifest.get("validity", {}).get("runtime_error_count") != 0:
        errors.append("runtime_error_count is not zero")
    if manifest.get("validity", {}).get("fatal_error_count") != 0:
        errors.append("fatal_error_count is not zero")
    if manifest.get("git", {}).get("dirty") is not False:
        errors.append("source tree was dirty")
    if manifest.get("results", {}).get("scientific_evidence") is not False:
        errors.append("execution incorrectly claims EVID")
    if manifest.get("results", {}).get("automatic_evidence_promotion") is not False:
        errors.append("automatic EVID promotion is not false")

    provenance = manifest.get("provenance_digests")
    if not isinstance(provenance, dict) or set(provenance) != {
        "code",
        "config",
        "prompt",
        "data",
    }:
        errors.append("provenance_digests incomplete")
    freeze = manifest.get("source_freeze_sha")
    if not isinstance(freeze, str) or len(freeze) != 64:
        errors.append("source_freeze_sha missing or malformed")

    payload = {
        "status": "PASS" if not errors else "FAIL",
        "experiment_id": EXPERIMENT_ID,
        "result_status": recomputed_analysis["status"],
        "decision_case": recomputed_analysis["decision_case"],
        "runs": len(runs),
        "design_integrity_passed": recomputed_integrity["pass"],
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
