#!/usr/bin/env python3
"""Verify EXP-SNN004-STDP-ASYM-R2-20260919 persisted DATA."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXP_ID = "EXP-SNN004-STDP-ASYM-R2-20260919"
OUT = ROOT / "research/experiments" / EXP_ID
PREREG = ROOT / "research/preregistrations/PREREG-SNN004-STDP-ASYM-R2.json"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = read_json(OUT / "manifest.json")
    stats = read_json(OUT / "analysis/statistics.json")
    review = read_json(OUT / "review_request.json")
    data = read_json(OUT / "data/evaluation.json")

    assert manifest["experiment_id"] == EXP_ID
    assert manifest["research_question"] == "RQ-SNN-004"
    assert manifest["hypothesis"] == "H-SNN-004-A"
    assert manifest["claim_id"] == "CLAIM-SNN-001"
    assert manifest["source_freeze"]["dirty_before_execution"] is False
    assert manifest["scientific_evidence"] is False
    assert manifest["automatic_evidence_promotion"] is False
    assert manifest["human_review_status"] == "PENDING"
    assert manifest["independent_replication"] is False
    assert manifest["integrity"]["pass"] is True
    assert all(bool(v) for v in manifest["primary_gates"].values())
    assert stats["status"] == "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
    assert review["human_review_status"] == "PENDING"
    assert review["ai_review_does_not_satisfy_human_gate"] is True

    measurements = data["measurements"]
    assert len(measurements) == 11
    assert {int(row["delta_t_ms"]) for row in measurements} == {
        -50,
        -20,
        -10,
        -5,
        -1,
        0,
        1,
        5,
        10,
        20,
        50,
    }
    assert all(int(row["repeated_evaluations"]) == 10 for row in measurements)

    hashes = manifest["artifacts_sha256"]
    assert hashes["preregistration"] == sha256(PREREG)
    assert hashes["evaluation_data"] == sha256(OUT / "data/evaluation.json")
    assert hashes["statistics"] == sha256(OUT / "analysis/statistics.json")

    for line in (OUT / "checksums.sha256").read_text(encoding="utf-8").splitlines():
        digest, relpath = line.split("  ", 1)
        assert sha256(OUT / relpath) == digest

    print(
        json.dumps(
            {
                "experiment_id": EXP_ID,
                "status": manifest["result_status"],
                "integrity": True,
                "primary_gates": manifest["primary_gates"],
                "human_review_status": "PENDING",
                "scientific_evidence": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
