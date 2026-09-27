#!/usr/bin/env python3
"""Verify prospective Stage-1 Temporal-Order promotion DATA."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TEMP-PROMO-R1.json"
EXPERIMENT_ID = "EXP-S1-TEMP-PROMO-R1-20260927"
OUT = ROOT / "research" / "experiments" / EXPERIMENT_ID
CANDIDATE = ROOT / "scripts" / "run_stage1_temporal_order_v2.py"

HISTORICAL_SEEDS = (
    set(range(101, 121))
    | set(range(2101, 2121))
    | set(range(6101, 6121))
    | set(range(6201, 6221))
    | set(range(6301, 6321))
    | set(range(7101, 7121))
)


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_candidate() -> Any:
    spec = importlib.util.spec_from_file_location("stage1_temporal_order_v2", CANDIDATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load temporal-order V2 runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.EXP_ID = EXPERIMENT_ID
    return module


def _integrity(
    runs: list[dict[str, Any]], prereg: dict[str, Any], temporal: Any
) -> dict[str, Any]:
    seeds = {int(v) for v in prereg["evaluation"]["seeds"]}
    checks = {
        "run_count": len(runs) == len(seeds) * len(temporal.ARMS) * len(temporal.ORDERS),
        "coverage": all(
            sum(
                int(r["seed"]) == seed and r["arm"] == arm and r["order"] == order
                for r in runs
            )
            == 1
            for seed in seeds
            for arm in temporal.ARMS
            for order in temporal.ORDERS
        ),
        "network_budget": all(
            int(r["node_count"]) == 6 and int(r["edge_count"]) == 4 for r in runs
        ),
        "paired_parameters": all(
            len(
                {
                    (
                        round(float(r["synaptic_weight"]), 12),
                        round(float(r["stimulus_current"]), 12),
                        round(float(r["total_injected_charge"]), 12),
                    )
                    for r in runs
                    if int(r["seed"]) == seed
                }
            )
            == 1
            for seed in seeds
        ),
        "matched_injected_charge": all(
            len(
                {
                    round(float(r["total_injected_charge"]), 12)
                    for r in runs
                    if int(r["seed"]) == seed
                }
            )
            == 1
            for seed in seeds
        ),
        "historical_seed_disjoint": seeds.isdisjoint(HISTORICAL_SEEDS),
        "unique_seed_count": len(seeds) == len(prereg["evaluation"]["seeds"]) == 20,
        "arm_set": {str(r["arm"]) for r in runs}
        == {"intact", "identity_destroyed"},
        "order_set": {str(r["order"]) for r in runs}
        == {"forward", "reverse", "simultaneous"},
    }
    return {"checks": checks, "pass": all(checks.values())}


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
    runs_raw = _read(OUT / "data" / "evaluation.json")
    statistics = _read(OUT / "analysis" / "statistics.json")
    if not isinstance(runs_raw, list):
        errors.append("evaluation data is not a list")
        runs: list[dict[str, Any]] = []
    else:
        runs = [dict(row) for row in runs_raw if isinstance(row, dict)]

    if prereg.get("status") != "FROZEN_BEFORE_PROMOTION_REPLICATION":
        errors.append("preregistration was not frozen")
    if prereg.get("execution_authorized") is not True:
        errors.append("execution was not authorized")
    if prereg.get("claim_id") != "CLAIM-S1-TEMP-001":
        errors.append("claim id mismatch")

    seeds = {int(seed) for seed in prereg["evaluation"]["seeds"]}
    if seeds & HISTORICAL_SEEDS:
        errors.append("promotion seeds overlap historical Stage-1 seeds")
    if len(seeds) != 20:
        errors.append("promotion requires 20 unique evaluation seeds")

    temporal = _load_candidate()
    recomputed_analysis = temporal.analyze(runs, prereg)
    recomputed_integrity = _integrity(runs, prereg, temporal)
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
    if results.get("claim_id") != "CLAIM-S1-TEMP-001":
        errors.append("manifest result claim mismatch")
    if results.get("automatic_evidence_promotion") is not False:
        errors.append("automatic EVID promotion must be false")
    if results.get("scientific_evidence") is not False:
        errors.append("execution incorrectly claims EVID")
    if results.get("human_review_required") is not True:
        errors.append("canonical human review is not required")
    if results.get("independent_authorship_replication") is not False:
        errors.append("internal promotion run incorrectly claims independence")

    summary = recomputed_analysis["summary"]
    payload = {
        "status": "PASS" if not errors else "FAIL",
        "experiment_id": EXPERIMENT_ID,
        "claim_id": "CLAIM-S1-TEMP-001",
        "evaluation_runs": len(runs),
        "result_status": recomputed_analysis["status"],
        "design_integrity_passed": recomputed_integrity["pass"],
        "intact_order_accuracy_median": summary["intact_order_accuracy_median"],
        "identity_destroyed_order_accuracy_median": summary[
            "identity_destroyed_order_accuracy_median"
        ],
        "paired_accuracy_delta_median": summary["paired_accuracy_delta_median"],
        "promotion_manifest_ready_for_human_review": not errors,
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
