"""Regression coverage for the canonical Stage-1 scientific contract.

These tests protect registry and governance structure only. They do not promote
historical DATA to EVID and they do not assert scientific outcomes.
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research" / "registry"
BASELINE = REGISTRY / "stage1_baseline.json"
REPLICATION = ROOT / "INDEPENDENT_REPLICATION.md"


def _claims() -> dict[str, dict]:
    raw = yaml.safe_load((REGISTRY / "claims.yaml").read_text(encoding="utf-8")) or []
    return {item["id"]: item for item in raw}


def test_stage1_scoped_claims_are_registered_without_retroactive_evidence() -> None:
    claims = _claims()

    topo = claims["CLAIM-S1-TOPO-001"]
    assert topo["research_question"] == "RQ-SNN-003"
    assert topo["hypothesis"] == "H-SNN-003-B"
    assert topo["status"] == "inconclusive"
    assert topo["evidence"] == ["EVID-2026-19"]
    assert "EXP-S1-TOPO-V2-20260918" in topo["experiments"]
    assert "EXP-S1-TOPO-V3-R1-20260918" in topo["experiments"]
    assert "EXP-S1-TOPO-PROMO-R1-20260927" in topo["experiments"]

    temporal = claims["CLAIM-S1-TEMP-001"]
    assert temporal["research_question"] == "RQ-TEMP-002"
    assert temporal["hypothesis"] == "H-TEMP-002-A"
    assert temporal["status"] == "inconclusive"
    assert temporal["evidence"] == ["EVID-2026-20"]
    assert temporal["experiments"] == [
        "EXP-S1-TEMP-ORDER-V2-20260919",
        "EXP-S1-TEMP-PROMO-R1-20260927",
    ]


def test_stage1_claim_boundaries_do_not_assert_stronger_results() -> None:
    claims = _claims()

    topo_claim = claims["CLAIM-S1-TOPO-001"]["claim"].lower()
    assert "5d" in topo_claim
    assert "nicht vorausgesetzt" in topo_claim

    temporal_claim = claims["CLAIM-S1-TEMP-001"]["claim"].lower()
    assert "identity-destroyed" in temporal_claim
    assert "sechsneuronigen" in temporal_claim


def test_stage1_baseline_tracks_canonical_topology_evid_without_overclaim() -> None:
    import json

    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    assessment = baseline["evid_promotion_assessment"]

    assert assessment["scientific_evidence"] is True
    assert assessment["topology_evidence_id"] == "EVID-2026-19"
    assert assessment["temporal_evidence_id"] == "EVID-2026-20"
    assert assessment["automatic_evidence_promotion"] is False
    assert baseline["maturity"]["percent"] == 85
    assert (
        baseline["maturity"]["weighting_contract"]["reviewed_evidence"][
            "canonical_evid_promotion_subgate"
        ]
        == "complete"
    )
    assert baseline["independent_replication"]["complete"] is False


def test_independent_replication_call_includes_central_topology_line() -> None:
    text = REPLICATION.read_text(encoding="utf-8")

    assert "EXP-S1-TOPO-V2-20260918" in text
    assert "EXP-S1-TOPO-V3-R1-20260918" in text
    assert "RQ-SNN-003" in text
    assert "does **not** count as independent scientific replication" in text
