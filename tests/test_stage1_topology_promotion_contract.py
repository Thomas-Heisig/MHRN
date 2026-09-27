"""Contract tests for the prospective Stage-1 topology promotion run."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-PROMO-R1.json"
CLAIMS = ROOT / "research" / "registry" / "claims.yaml"
RUNNER = ROOT / "scripts" / "run_stage1_topology_promotion_r1.py"

HISTORICAL_SEEDS = set(range(2101, 2121)) | set(range(6101, 6121)) | set(
    range(6201, 6221)
)


def _prereg() -> dict:
    return json.loads(PREREG.read_text(encoding="utf-8"))


def test_promotion_preregistration_is_scoped_and_data_only() -> None:
    prereg = _prereg()

    assert prereg["claim_id"] == "CLAIM-S1-TOPO-001"
    assert prereg["research_question"] == "RQ-SNN-003"
    assert prereg["hypothesis"] == "H-SNN-003-B"
    assert prereg["scientific_evidence"] is False
    assert prereg["automatic_evidence_promotion"] is False
    assert prereg["evidence_engine_contract"]["automatic_evidence_promotion"] is False
    assert prereg["provenance"]["independent_external_replication"] is False


def test_promotion_seeds_are_unique_and_disjoint_from_historical_topology_runs() -> None:
    prereg = _prereg()
    seeds = [int(seed) for seed in prereg["evaluation"]["seeds"]]

    assert len(seeds) == 20
    assert len(set(seeds)) == 20
    assert set(seeds).isdisjoint(HISTORICAL_SEEDS)


def test_promotion_preserves_v3_r1_matched_small_snn_envelope() -> None:
    prereg = _prereg()
    matched = prereg["matched_budgets"]

    assert matched["neuron_count"] == 64
    assert matched["expected_edge_count"] == 246
    assert matched["synaptic_weight"] == 55
    assert matched["evaluation_ticks"] == 128
    assert prereg["evaluation"]["primary_multiple_testing"].startswith(
        "Single Holm correction across all 10"
    )


def test_scoped_claim_exists_without_retroactive_evidence() -> None:
    claims = yaml.safe_load(CLAIMS.read_text(encoding="utf-8")) or []
    claim = next(item for item in claims if item["id"] == "CLAIM-S1-TOPO-001")

    assert claim["research_question"] == "RQ-SNN-003"
    assert claim["hypothesis"] == "H-SNN-003-B"
    assert claim["evidence"] == []
    assert claim["status"] == "untested"


def test_runner_refuses_unfrozen_or_unauthorized_execution() -> None:
    text = RUNNER.read_text(encoding="utf-8")

    assert 'FROZEN_BEFORE_PROMOTION_REPLICATION' in text
    assert 'execution_authorized' in text
    assert 'automatic EVID promotion must remain disabled' in text
    assert 'Refusing to overwrite existing experiment' in text
    assert 'promotion replication requires a clean git tree' in text
    assert 'record_provenance_digests' in text
    assert 'human_review_required=True' in text
    assert 'independent_authorship_replication=False' in text
