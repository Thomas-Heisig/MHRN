#!/usr/bin/env python3
"""Verify persisted DATA for EXP-EMB002-PROPRIO-V2-20260920."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXP_ID = "EXP-EMB002-PROPRIO-V2-20260920"
OUT = ROOT / "research/experiments" / EXP_ID
PREREG = ROOT / "research/preregistrations/PREREG-EMB002-PROPRIO-V2.json"


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
    assert manifest["protocol"] == "embodied_proprioception_matched_v2"
    assert manifest["source_freeze"]["dirty_before_execution"] is False
    assert manifest["scientific_evidence"] is False
    assert manifest["automatic_evidence_promotion"] is False
    assert manifest["human_review_status"] == "PENDING"
    assert manifest["independent_replication"] is False
    assert manifest["integrity"]["pass"] is True
    assert stats["integrity"]["pass"] is True
    assert stats["p_values_computed"] is False
    assert stats["confirmatory_thresholds_applied"] is False
    assert review["human_review_status"] == "PENDING"

    seeds = set(map(int, prereg["design"]["seeds"]))
    conditions = set(prereg["design"]["conditions"])
    assert len(seeds) == 20
    assert conditions == {
        "closed_loop",
        "feedback_absent",
        "delayed_proprioception",
        "timing_shuffle",
    }
    assert isinstance(runs, list)
    assert len(runs) == 80
    assert {int(row["seed"]) for row in runs} == seeds
    assert {str(row["condition"]) for row in runs} == conditions

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
        assert (
            rows[(seed, "timing_shuffle")]["donor_tape_sha256"]
            == rows[(seed, "closed_loop")]["sensor_tape_sha256"]
        )

    primary = {
        (item["control"], item["metric"])
        for item in stats["paired_comparisons"]
        if item["predeclared_role"] == "primary"
    }
    assert primary == {
        ("feedback_absent", "tracking_rmse_rad"),
        ("delayed_proprioception", "tracking_rmse_rad"),
    }

    assert all(row["runtime_error"] is None for row in runs)
    assert all(int(row["ticks_requested"]) == 1000 for row in runs)
    assert all(int(row["ticks_executed"]) == 1000 for row in runs)
    assert len({row["external_perturbation_schedule_sha256"] for row in runs}) == 1

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
                "status": manifest["result_status"],
                "run_count": len(runs),
                "integrity": True,
                "mean_outcomes": manifest["results"]["mean_outcomes"],
                "human_review_status": "PENDING",
                "scientific_evidence": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
