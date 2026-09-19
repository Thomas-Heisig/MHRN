#!/usr/bin/env python3
"""Verify persisted DATA for EXP-REC-002-CLEAN-R2-20260919."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXP_ID = "EXP-REC-002-CLEAN-R2-20260919"
OUT = ROOT / "research/experiments" / EXP_ID
PREREG = ROOT / "research/preregistrations/PREREG-REC-002-CLEAN-R2.json"


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
    assert manifest["research_question"] == "RQ-REC-002"
    assert manifest["hypothesis"] == "H-REC-002-A"
    assert manifest["protocol"] == "recurrence_scale_clean_r2"
    assert manifest["source_freeze"]["dirty_before_execution"] is False
    assert manifest["scientific_evidence"] is False
    assert manifest["automatic_evidence_promotion"] is False
    assert manifest["human_review_status"] == "PENDING"
    assert manifest["independent_replication"] is False
    assert manifest["integrity"]["pass"] is True
    assert stats["integrity"]["pass"] is True
    assert review["human_review_status"] == "PENDING"
    assert review["ai_review_does_not_satisfy_human_gate"] is True

    seeds = set(map(int, prereg["seeds"]))
    expected = {"loop_delay_1", "loop_delay_2", "loop_delay_4", "loop_delay_8"}
    assert isinstance(runs, list)
    assert len(runs) == 80
    assert {int(row["seed"]) for row in runs} == seeds
    assert {str(row["condition"]) for row in runs} == expected
    assert all(row["runtime_error"] is None for row in runs)
    assert all(int(row["metrics"]["ticks_requested"]) == 256 for row in runs)

    for seed in seeds:
        rows = [row for row in runs if int(row["seed"]) == seed]
        assert len(rows) == 4
        assert {str(row["condition"]) for row in rows} == expected

    hashes = manifest["artifacts_sha256"]
    assert hashes["preregistration"] == sha256(PREREG)
    assert hashes["evaluation_data"] == sha256(OUT / "data/evaluation.json")
    assert hashes["statistics"] == sha256(OUT / "analysis/statistics.json")

    for line in (OUT / "checksums.sha256").read_text(encoding="utf-8").splitlines():
        digest, relpath = line.split("  ", 1)
        assert sha256(OUT / relpath) == digest

    protected = manifest["gate_protection"]["source_digest_policy"]
    assert "Do not modify src/" in protected

    print(
        json.dumps(
            {
                "experiment_id": EXP_ID,
                "result_status": manifest["result_status"],
                "run_count": len(runs),
                "integrity": True,
                "all_primary_gates_pass": all(
                    bool(value) for value in manifest["primary_gates"].values()
                ),
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
