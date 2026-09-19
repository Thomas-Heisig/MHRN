#!/usr/bin/env python3
"""Verify persisted DATA for EXP-S1-TEMP-ORDER-V2-20260919."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXP_ID = "EXP-S1-TEMP-ORDER-V2-20260919"
OUT = ROOT / "research/experiments" / EXP_ID
PREREG = ROOT / "research/preregistrations/PREREG-S1-TEMP-ORDER-V2.json"


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
    seeds = set(map(int, prereg["evaluation"]["seeds"]))

    assert manifest["experiment_id"] == EXP_ID
    assert manifest["stage"] == 1
    assert manifest["research_question"] == "RQ-TEMP-002"
    assert manifest["hypothesis"] == "H-TEMP-002-A"
    assert manifest["protocol"] == "stage1_two_channel_temporal_order_v2"
    assert manifest["scientific_evidence"] is False
    assert manifest["automatic_evidence_promotion"] is False
    assert manifest["human_review_status"] == "PENDING"
    assert manifest["independent_replication"] is False
    assert manifest["source_freeze"]["dirty_before_execution"] is False
    assert manifest["integrity"]["pass"] is True
    assert stats["integrity"]["pass"] is True
    assert review["human_review_status"] == "PENDING"
    assert review["ai_review_does_not_satisfy_human_gate"] is True

    assert isinstance(runs, list)
    assert len(runs) == len(seeds) * 6
    assert {int(r["seed"]) for r in runs} == seeds
    assert {r["arm"] for r in runs} == {"intact", "identity_destroyed"}
    assert {r["order"] for r in runs} == {"forward", "reverse", "simultaneous"}
    assert all(r["node_count"] == 6 and r["edge_count"] == 4 for r in runs)

    for seed in seeds:
        rows = [r for r in runs if int(r["seed"]) == seed]
        assert len(rows) == 6
        assert len({
            (round(float(r["synaptic_weight"]), 12),
             round(float(r["stimulus_current"]), 12),
             round(float(r["total_injected_charge"]), 12))
            for r in rows
        }) == 1

    hashes = manifest["artifacts_sha256"]
    assert hashes["preregistration"] == sha256(PREREG)
    assert hashes["evaluation_data"] == sha256(OUT / "data/evaluation.json")
    assert hashes["statistics"] == sha256(OUT / "analysis/statistics.json")

    for line in (OUT / "checksums.sha256").read_text(encoding="utf-8").splitlines():
        digest, relpath = line.split("  ", 1)
        assert sha256(OUT / relpath) == digest

    print(json.dumps({
        "experiment_id": EXP_ID,
        "result_status": manifest["result_status"],
        "run_count": len(runs),
        "integrity": True,
        "human_review_status": "PENDING",
        "scientific_evidence": False,
        "independent_replication": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
