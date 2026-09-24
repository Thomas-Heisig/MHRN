#!/usr/bin/env python3
"""Verify persisted DATA for EXP-EMB002A-DELAY-SWEEP-V4-20260924."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXP_ID = "EXP-EMB002A-DELAY-SWEEP-V4-20260924"
OUT = ROOT / "research/experiments" / EXP_ID
PREREG = (
    ROOT
    / "research/preregistrations/PREREG-EMB002A-PROPRIOCEPTION-DELAY-SWEEP-V4.json"
)
EXPECTED_DELAYS = (0, 5, 20, 50, 100, 200)
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
    assert manifest["hypothesis"] == "H-EMB-002-A"
    assert manifest["protocol"] == "embodied_proprioception_delay_sweep_v4"
    assert manifest["direct_test_of_hypothesis"] is False
    assert manifest["characterization_after_prior_non_support"] is True
    assert manifest["source_freeze"]["dirty_before_execution"] is False
    assert manifest["scientific_evidence"] is False
    assert manifest["automatic_evidence_promotion"] is False
    assert manifest["human_review_status"] == "PENDING"
    assert manifest["independent_replication"] is False
    assert manifest["integrity"]["pass"] is True
    assert stats["integrity"]["pass"] is True
    assert stats["binary_support_rule_applied"] is False
    assert stats["p_values_computed"] is False
    assert stats["confirmatory_thresholds_applied"] is False
    assert review["human_review_status"] == "PENDING"

    seeds = tuple(map(int, prereg["design"]["seeds"]))
    delays = tuple(map(int, prereg["design"]["delay_ticks"]))
    conditions = set(prereg["design"]["conditions"])
    assert len(seeds) == 20
    assert len(set(seeds)) == 20
    assert delays == EXPECTED_DELAYS
    assert conditions == EXPECTED_CONDITIONS
    assert isinstance(runs, list)
    assert len(runs) == 140
    assert {int(row["seed"]) for row in runs} == set(seeds)
    assert {str(row["condition"]) for row in runs} == EXPECTED_CONDITIONS
    assert all(row["runtime_error"] is None for row in runs)
    assert all(int(row["ticks_requested"]) == 1000 for row in runs)
    assert all(int(row["ticks_executed"]) == 1000 for row in runs)

    rows = {
        (int(row["seed"]), str(row["condition"])): row for row in runs
    }
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
        assert (
            len(
                {
                    json.dumps(row["graph"], sort_keys=True)
                    for row in seed_rows
                }
            )
            == 1
        )
        for delay in delays:
            row = rows[(seed, f"delay_{delay}")]
            assert int(row["requested_delay_ticks"]) == delay
            assert int(row["engine_proprioceptive_delay_ticks"]) == delay

    integrity = manifest["integrity"]["per_seed"]
    assert all(
        all(bool(value) for value in checks.values())
        for checks in integrity.values()
    )

    hashes = manifest["artifacts_sha256"]
    assert hashes["preregistration"] == sha256(PREREG)
    assert hashes["evaluation_data"] == sha256(OUT / "data/evaluation.json")
    assert hashes["statistics"] == sha256(OUT / "analysis/statistics.json")
    assert hashes["canonical_embodiment_source"] == sha256(
        ROOT / "src/research/connectome_embodiment.py"
    )

    for line in (OUT / "checksums.sha256").read_text(
        encoding="utf-8"
    ).splitlines():
        digest, relpath = line.split("  ", 1)
        assert sha256(OUT / relpath) == digest

    print(
        json.dumps(
            {
                "experiment_id": EXP_ID,
                "result_status": manifest["result_status"],
                "run_count": len(runs),
                "integrity": True,
                "means": manifest["results"]["mean_tracking_rmse_rad"],
                "delay_response_curve": manifest["results"][
                    "delay_response_curve"
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
