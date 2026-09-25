#!/usr/bin/env python3
"""Verify persisted DATA for EXP-EMB002B-TRANSITION-V5-20260924."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXP_ID = "EXP-EMB002B-TRANSITION-V5-20260924"
OUT = ROOT / "research/experiments" / EXP_ID
PREREG = (
    ROOT / "research/preregistrations/PREREG-EMB002B-PROPRIOCEPTION-TRANSITION-V5.json"
)
EXPECTED_DELAYS = (0, 50, 60, 70, 80, 90, 100)
EXPECTED_CONDITIONS = {
    *(f"delay_{delay}" for delay in EXPECTED_DELAYS),
    "feedback_absent",
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    prereg = read_json(PREREG)
    manifest = read_json(OUT / "manifest.json")
    stats = read_json(OUT / "analysis/statistics.json")
    review = read_json(OUT / "review_request.json")
    runs = json.loads((OUT / "data/evaluation.json").read_text(encoding="utf-8"))

    assert manifest["experiment_id"] == EXP_ID
    assert manifest["research_question"] == "RQ-EMB-002"
    assert manifest["hypothesis"] == "H-EMB-002-B"
    assert manifest["protocol"] == "embodied_proprioception_transition_v5"
    assert manifest["direct_test_of_hypothesis"] is True
    assert manifest["derived_from_exploratory_v4"] is True
    assert manifest["source_freeze"]["dirty_before_execution"] is False
    assert manifest["scientific_evidence"] is False
    assert manifest["automatic_evidence_promotion"] is False
    assert manifest["human_review_status"] == "PENDING"
    assert manifest["independent_replication"] is False
    assert manifest["integrity"]["pass"] is True
    assert stats["integrity"]["pass"] is True
    assert stats["p_values_computed"] is False
    assert stats["confirmatory_thresholds_applied"] is True
    assert stats["thresholds_frozen_before_v5_data"] is True
    assert review["human_review_status"] == "PENDING"

    seeds = tuple(map(int, prereg["design"]["seeds"]))
    delays = tuple(map(int, prereg["design"]["delay_ticks"]))
    conditions = set(prereg["design"]["conditions"])
    assert len(seeds) == 24
    assert len(set(seeds)) == 24
    assert min(seeds) == 925001
    assert max(seeds) == 925024
    assert delays == EXPECTED_DELAYS
    assert conditions == EXPECTED_CONDITIONS
    assert isinstance(runs, list)
    assert len(runs) == 192
    assert {int(row["seed"]) for row in runs} == set(seeds)
    assert {str(row["condition"]) for row in runs} == EXPECTED_CONDITIONS
    assert all(row["runtime_error"] is None for row in runs)
    assert all(int(row["ticks_requested"]) == 1000 for row in runs)
    assert all(int(row["ticks_executed"]) == 1000 for row in runs)

    rows = {(int(row["seed"]), str(row["condition"])): row for row in runs}
    for seed in seeds:
        seed_rows = [rows[(seed, condition)] for condition in conditions]
        assert len({row["state_digest_before"] for row in seed_rows}) == 1
        assert (
            len(
                {
                    json.dumps(row["initial_body_state"], sort_keys=True)
                    for row in seed_rows
                }
            )
            == 1
        )
        assert len({json.dumps(row["graph"], sort_keys=True) for row in seed_rows}) == 1
        for delay in delays:
            row = rows[(seed, f"delay_{delay}")]
            assert int(row["requested_delay_ticks"]) == delay
            assert int(row["engine_proprioceptive_delay_ticks"]) == delay

    integrity = manifest["integrity"]["per_seed"]
    assert all(
        all(bool(value) for value in checks.values()) for checks in integrity.values()
    )

    comparisons = stats["paired_comparisons"]
    primary = stats["primary_checks"]
    tolerance = float(prereg["analysis_plan"]["tolerance_margin_rad"])
    degradation = float(prereg["analysis_plan"]["degradation_margin_rad"])
    fraction = float(prereg["analysis_plan"]["degradation_fraction_required"])
    assert primary["delay_50_within_tolerance"] == (
        comparisons["delay_50"]["mean_difference"] <= tolerance
    )
    assert primary["delay_60_within_tolerance"] == (
        comparisons["delay_60"]["mean_difference"] <= tolerance
    )
    for condition in ("delay_90", "delay_100"):
        assert primary[f"{condition}_degraded"] == (
            comparisons[condition]["mean_difference"] >= degradation
            and comparisons[condition]["fraction_delay_0_lower"] >= fraction
        )

    hashes = manifest["artifacts_sha256"]
    assert hashes["preregistration"] == sha256(PREREG)
    assert hashes["evaluation_data"] == sha256(OUT / "data/evaluation.json")
    assert hashes["statistics"] == sha256(OUT / "analysis/statistics.json")
    assert hashes["canonical_embodiment_source"] == sha256(
        ROOT / "src/research/connectome_embodiment.py"
    )

    for line in (OUT / "checksums.sha256").read_text(encoding="utf-8").splitlines():
        digest, relpath = line.split("  ", 1)
        assert sha256(OUT / relpath) == digest

    print(
        json.dumps(
            {
                "experiment_id": EXP_ID,
                "result_status": manifest["result_status"],
                "run_count": len(runs),
                "integrity": True,
                "primary_checks": manifest["results"]["primary_checks"],
                "assay_valid": manifest["results"]["assay_valid"],
                "transition_localization": manifest["results"][
                    "transition_localization"
                ],
                "human_review_status": "PENDING",
                "scientific_evidence": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
