#!/usr/bin/env python3
"""Verify the prospective Stage-1 topology promotion replication."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-PROMO-R1.json"
EXPERIMENT_ID = "EXP-S1-TOPO-PROMO-R1-20260927"
OUT = ROOT / "research" / "experiments" / EXPERIMENT_ID
TOPOLOGY_RUNNER = ROOT / "scripts" / "run_stage1_topology_v3_r1.py"
HISTORICAL_SEEDS = set(range(2101, 2121)) | set(range(6101, 6121)) | set(
    range(6201, 6221)
)


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_topology() -> Any:
    spec = importlib.util.spec_from_file_location("stage1_topology_v3_r1", TOPOLOGY_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load topology runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.EXP_ID = EXPERIMENT_ID
    return module


def main() -> int:
    errors: list[str] = []
    required = [
        OUT / "manifest.json",
        OUT / "report.md",
        OUT / "data" / "evaluation.json",
        OUT / "analysis" / "statistics.json",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(ROOT)}")
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1

    prereg = _read(PREREG)
    manifest = _read(OUT / "manifest.json")
    evaluation_raw = _read(OUT / "data" / "evaluation.json")
    statistics = _read(OUT / "analysis" / "statistics.json")

    if not isinstance(evaluation_raw, list):
        errors.append("evaluation data is not a list")
        evaluation: list[dict[str, Any]] = []
    else:
        evaluation = [dict(row) for row in evaluation_raw if isinstance(row, dict)]

    if prereg.get("status") != "FROZEN_BEFORE_PROMOTION_REPLICATION":
        errors.append("preregistration was not frozen")
    if prereg.get("execution_authorized") is not True:
        errors.append("execution was not authorized")
    if prereg.get("claim_id") != "CLAIM-S1-TOPO-001":
        errors.append("claim id mismatch")

    seeds = {int(seed) for seed in prereg["evaluation"]["seeds"]}
    if seeds & HISTORICAL_SEEDS:
        errors.append("promotion seeds overlap historical topology seeds")
    if len(seeds) != 20:
        errors.append("promotion requires 20 unique evaluation seeds")

    topo = _load_topology()
    recomputed_summary = topo.summarize(evaluation)
    recomputed_analysis = topo.analyze(evaluation, prereg)
    recomputed_integrity = topo.validate_design(prereg, evaluation)
    recomputed_integrity.setdefault("checks", {})[
        "all_historical_topology_seeds_disjoint"
    ] = seeds.isdisjoint(HISTORICAL_SEEDS)
    recomputed_integrity["pass"] = bool(
        recomputed_integrity.get("pass")
        and recomputed_integrity["checks"]["all_historical_topology_seeds_disjoint"]
    )

    if statistics.get("condition_summary") != recomputed_summary:
        errors.append("condition summary differs from deterministic recomputation")
    if statistics.get("analysis") != recomputed_analysis:
        errors.append("analysis differs from deterministic recomputation")
    if statistics.get("integrity") != recomputed_integrity:
        errors.append("integrity differs from deterministic recomputation")
    if not recomputed_integrity["pass"]:
        errors.append("design integrity did not pass")

    if manifest.get("experiment_id") != EXPERIMENT_ID:
        errors.append("manifest experiment id mismatch")
    if manifest.get("experiment_status") != "completed":
        errors.append("manifest is not completed")
    validity = manifest.get("validity", {})
    if validity.get("valid") is not True:
        errors.append("manifest validity.valid is not true")
    if validity.get("runtime_error_count") != 0:
        errors.append("runtime_error_count is not zero")
    if validity.get("fatal_error_count") != 0:
        errors.append("fatal_error_count is not zero")
    if manifest.get("git", {}).get("dirty") is not False:
        errors.append("source tree was dirty before execution")

    digests = manifest.get("provenance_digests")
    if not isinstance(digests, dict) or set(digests) != {
        "code",
        "config",
        "prompt",
        "data",
    }:
        errors.append("provenance_digests incomplete")
    elif any(
        not isinstance(value, str)
        or len(value) != 64
        or any(ch not in "0123456789abcdef" for ch in value)
        for value in digests.values()
    ):
        errors.append("invalid provenance digest format")
    freeze = manifest.get("source_freeze_sha")
    if not isinstance(freeze, str) or len(freeze) != 64:
        errors.append("source_freeze_sha missing or malformed")

    results = manifest.get("results", {})
    if results.get("claim_id") != "CLAIM-S1-TOPO-001":
        errors.append("manifest result claim mismatch")
    if results.get("automatic_evidence_promotion") is not False:
        errors.append("automatic EVID promotion must be false")
    if results.get("scientific_evidence") is not False:
        errors.append("execution incorrectly claims EVID")
    if results.get("human_review_required") is not True:
        errors.append("canonical human review is not required")
    if results.get("independent_authorship_replication") is not False:
        errors.append("internal promotion run incorrectly claims independence")

    human_review = OUT / "human_review.json"
    if human_review.exists():
        review = _read(human_review)
        if review.get("experiment_id") != EXPERIMENT_ID:
            errors.append("human review experiment id mismatch")
        if review.get("decision") not in {"supports", "refutes", "inconclusive"}:
            errors.append("human review decision is not canonical")

    payload = {
        "status": "PASS" if not errors else "FAIL",
        "experiment_id": EXPERIMENT_ID,
        "claim_id": "CLAIM-S1-TOPO-001",
        "evaluation_runs": len(evaluation),
        "result_status": recomputed_analysis["status"],
        "design_integrity_passed": recomputed_integrity["pass"],
        "promotion_manifest_ready_for_human_review": not errors,
        "human_review_present": human_review.exists(),
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
