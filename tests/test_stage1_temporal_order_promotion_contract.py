"""Contract tests for prospective Stage-1 Temporal-Order promotion R1."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TEMP-PROMO-R1.json"
CLAIMS = ROOT / "research" / "registry" / "claims.yaml"
RUNNER = ROOT / "scripts" / "run_stage1_temporal_order_promotion_r1.py"

HISTORICAL_SEEDS = (
    set(range(101, 121))
    | set(range(2101, 2121))
    | set(range(6101, 6121))
    | set(range(6201, 6221))
    | set(range(6301, 6321))
    | set(range(7101, 7121))
)


def _prereg() -> dict:
    return json.loads(PREREG.read_text(encoding="utf-8"))


def test_temporal_promotion_is_scoped_and_data_only() -> None:
    prereg = _prereg()

    assert prereg["claim_id"] == "CLAIM-S1-TEMP-001"
    assert prereg["research_question"] == "RQ-TEMP-002"
    assert prereg["hypothesis"] == "H-TEMP-002-A"
    assert prereg["scientific_evidence"] is False
    assert prereg["automatic_evidence_promotion"] is False
    assert prereg["evidence_engine_contract"]["automatic_evidence_promotion"] is False
    assert prereg["provenance"]["independent_external_replication"] is False


def test_temporal_promotion_seeds_are_unique_and_historically_disjoint() -> None:
    seeds = [int(seed) for seed in _prereg()["evaluation"]["seeds"]]

    assert len(seeds) == 20
    assert len(set(seeds)) == 20
    assert set(seeds).isdisjoint(HISTORICAL_SEEDS)


def test_temporal_promotion_preserves_identity_destroyed_control() -> None:
    prereg = _prereg()

    assert prereg["task"]["neuron_count"] == 6
    assert prereg["task"]["synapse_count"] == 4
    assert prereg["arms"]["intact"]
    assert "identity" in prereg["arms"]["identity_destroyed"].lower()
    assert prereg["evaluation"]["primary_contrast"] == (
        "intact minus identity_destroyed, paired by seed"
    )
    assert prereg["analysis"]["multiple_testing"].startswith("not applicable")


def test_temporal_scoped_claim_remains_separate_from_topology_evidence() -> None:
    claims = yaml.safe_load(CLAIMS.read_text(encoding="utf-8")) or []
    temporal = next(item for item in claims if item["id"] == "CLAIM-S1-TEMP-001")
    topology = next(item for item in claims if item["id"] == "CLAIM-S1-TOPO-001")

    assert temporal["research_question"] == "RQ-TEMP-002"
    assert temporal["hypothesis"] == "H-TEMP-002-A"
    assert temporal["evidence"] == []
    assert temporal["status"] == "untested"
    assert topology["evidence"] == ["EVID-2026-19"]


def test_temporal_runner_requires_freeze_clean_tree_and_human_review() -> None:
    text = RUNNER.read_text(encoding="utf-8")

    assert "FROZEN_BEFORE_PROMOTION_REPLICATION" in text
    assert "execution_authorized" in text
    assert "automatic EVID promotion must remain disabled" in text
    assert "Refusing to overwrite existing experiment" in text
    assert "promotion replication requires a clean git tree" in text
    assert "record_provenance_digests" in text
    assert "human_review_required=True" in text
    assert "independent_authorship_replication=False" in text
