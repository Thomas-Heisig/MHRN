from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src" / "dashboard" / "static" / "scientific-progress.json"
INTEGRITY = ROOT / "research" / "INTEGRITY_AND_ATTRIBUTION.md"
RELATED = ROOT / "research" / "RELATED_WORK.md"
LOADER = ROOT / "src" / "dashboard" / "static" / "formula-renderer.js"
TIMELINE = ROOT / "src" / "dashboard" / "static" / "scientific-progress.js"


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_scientific_manifest_covers_canonical_stages_zero_through_ten() -> None:
    data = _manifest()
    stages = data["stages"]
    assert isinstance(stages, list)
    assert [stage["stage"] for stage in stages] == list(range(11))
    assert all(0.0 <= float(stage["score"]) <= 1.0 for stage in stages)


def test_scientific_weights_are_explicit_and_normalized() -> None:
    data = _manifest()
    weights = data["weights"]
    assert isinstance(weights, dict)
    assert set(weights) == {
        "research_question",
        "protocol",
        "data",
        "reviewed_evidence",
        "independent_replication",
        "attribution",
    }
    assert abs(sum(float(value) for value in weights.values()) - 1.0) < 1e-9


def test_stage6_does_not_overclaim_memory_or_world_model_maturity() -> None:
    stage6 = next(stage for stage in _manifest()["stages"] if stage["stage"] == 6)
    boundary = str(stage6["claim_boundary"]).lower()
    assert "keine semantization" in boundary
    assert "kein hierarchisches predictive coding" in boundary
    assert "kein generatives weltmodell" in boundary
    assert float(stage6["score"]) < 0.5


def test_integrity_policy_refuses_false_plagiarism_certification() -> None:
    text = (
        INTEGRITY.read_text(encoding="utf-8")
        .lower()
        .replace("**", "")
        .replace("__", "")
    )
    assert "does not certify" in text
    assert "similarity" in text
    assert "human source review" in text
    assert "ai-generated references" in text


def test_related_work_quarantines_unverified_citations() -> None:
    text = RELATED.read_text(encoding="utf-8")
    assert "ArithSpec" in text and "QUARANTINED" in text
    assert "NeuroEval" in text
    assert "D'Alba" in text
    assert "Predictive coding with spiking neural networks" in text
    assert "Spiking world model" in text


def test_scientific_timeline_is_loaded_without_replacing_formula_contract() -> None:
    loader = LOADER.read_text(encoding="utf-8")
    timeline = TIMELINE.read_text(encoding="utf-8")
    assert 'import "./scientific-progress.js"' in loader
    assert 'MATH_ROOT_SELECTOR = ".fm-markdown, .pub-reader-article"' in loader
    assert 'processHtmlClass: "fm-markdown|pub-reader-article"' in loader
    assert "scientific-progress.json" in timeline
    assert "Wissenschaftliche Timeline" in timeline
    assert "keine Kognitionskennzahl" in timeline


def test_stage0_score_matches_current_weighted_evidence_state() -> None:
    data = _manifest()
    stage0 = next(stage for stage in data["stages"] if stage["stage"] == 0)
    weights = data["weights"]
    scale = data["status_scale"]

    expected = 0.0
    for criterion in stage0["criteria"]:
        status_value = scale[criterion["status"]]
        assert status_value is not None
        expected += float(weights[criterion["id"]]) * float(status_value)

    assert abs(float(stage0["score"]) - expected) < 1e-12
    assert abs(float(stage0["score"]) - 0.925) < 1e-12

    by_id = {criterion["id"]: criterion for criterion in stage0["criteria"]}
    assert by_id["research_question"]["status"] == "met"
    assert by_id["protocol"]["status"] == "met"
    assert by_id["data"]["status"] == "met"
    assert by_id["reviewed_evidence"]["status"] == "met"
    assert by_id["independent_replication"]["status"] == "partial"
    assert by_id["attribution"]["status"] == "met"


def test_stage0_keeps_scoped_readiness_separate_from_total_maturity() -> None:
    readiness = json.loads(
        (
            ROOT
            / "research/generated/verification/single_neuron_scientific_readiness.json"
        ).read_text(encoding="utf-8")
    )
    stage0 = next(stage for stage in _manifest()["stages"] if stage["stage"] == 0)
    assert readiness["research_readiness_percent"] == 100
    assert float(stage0["score"]) < 1.0
    assert readiness["maturity_boundary"]["human_reviewed_evid_complete"] is True
    assert (
        readiness["maturity_boundary"]["independent_authorship_replication_complete"]
        is False
    )


def test_stage0_human_review_is_complete_but_evid_promotion_remains_blocked() -> None:
    review = json.loads(
        (
            ROOT
            / "research/experiments/EXP-STAGE0-20260916-MODEL-CONFORMANCE-V2/human_scientific_review.json"
        ).read_text(encoding="utf-8")
    )
    promotion = json.loads(
        (
            ROOT
            / "research/experiments/EXP-STAGE0-20260916-MODEL-CONFORMANCE-V2/EVIDENCE_PROMOTION_STATUS.json"
        ).read_text(encoding="utf-8")
    )
    assert review["review_status"] == "completed"
    assert review["decision"] == "supports_scoped_claim"
    assert (
        review["review_points"]["independent_replication"]["decision"] == "remains_open"
    )
    assert promotion["scientific_evidence"] is False
    assert (
        promotion["evidence_promotion_status"] == "BLOCKED_LEGACY_PROVENANCE_CONTRACT"
    )
    assert promotion["independent_replication_complete"] is False


def test_stage0_reviewed_evidence_is_met_after_canonical_promotion() -> None:
    stage0 = next(stage for stage in _manifest()["stages"] if stage["stage"] == 0)
    by_id = {criterion["id"]: criterion for criterion in stage0["criteria"]}
    reviewed = by_id["reviewed_evidence"]
    independent = by_id["independent_replication"]
    evidence = json.loads(
        (ROOT / "research/registry/evidence/EVID-2026-18.json").read_text(
            encoding="utf-8"
        )
    )
    promotion = json.loads(
        (
            ROOT
            / "research/experiments/EXP-STAGE0-20260918-MODEL-CONFORMANCE-V2-PROMO-R1/EVIDENCE_PROMOTION_STATUS.json"
        ).read_text(encoding="utf-8")
    )
    assert reviewed["status"] == "met"
    assert "Human Review" in reviewed["label"]
    assert "EvidenceEngine" in reviewed["label"]
    assert evidence["claim_id"] == "CLAIM-EVAL-006"
    assert evidence["status"] == "supports"
    assert promotion["evidence_id"] == "EVID-2026-18"
    assert promotion["evidence_promotion_status"] == "COMPLETED"
    assert promotion["independent_replication_complete"] is False
    assert independent["status"] == "partial"
    assert "keine unabhängig autorisierte Replikation" in independent["label"]


def test_stage0_partial_semantics_are_contractual_not_result_dependent() -> None:
    stage0 = next(stage for stage in _manifest()["stages"] if stage["stage"] == 0)
    contracts = stage0["criterion_contracts"]
    reviewed = contracts["reviewed_evidence"]
    replication = contracts["independent_replication"]

    assert reviewed["decomposition"]["human_scientific_review_fraction"] == 0.5
    assert (
        reviewed["decomposition"]["canonical_evidence_engine_promotion_fraction"] == 0.5
    )
    assert "not result favorability" in reviewed["anti_gaming_rule"]
    assert replication["decomposition"]["external_reference_comparison_fraction"] == 0.5
    assert (
        replication["decomposition"]["independent_authorship_replication_fraction"]
        == 0.5
    )
    assert "can never satisfy" in replication["anti_conflation_rule"]


def test_stage1_score_matches_consolidated_scientific_state() -> None:
    data = _manifest()
    stage1 = next(stage for stage in data["stages"] if stage["stage"] == 1)
    weights = data["weights"]
    scale = data["status_scale"]

    expected = 0.0
    for criterion in stage1["criteria"]:
        status_value = scale[criterion["status"]]
        assert status_value is not None
        expected += float(weights[criterion["id"]]) * float(status_value)

    assert abs(float(stage1["score"]) - expected) < 1e-12
    assert abs(float(stage1["score"]) - 0.75) < 1e-12

    by_id = {criterion["id"]: criterion for criterion in stage1["criteria"]}
    assert by_id["research_question"]["status"] == "met"
    assert by_id["protocol"]["status"] == "met"
    assert by_id["data"]["status"] == "met"
    assert by_id["reviewed_evidence"]["status"] == "partial"
    assert by_id["independent_replication"]["status"] == "open"
    assert by_id["attribution"]["status"] == "met"


def test_stage1_review_and_evid_boundaries_remain_separate() -> None:
    stage1 = next(stage for stage in _manifest()["stages"] if stage["stage"] == 1)
    contracts = stage1["criterion_contracts"]
    reviewed = contracts["reviewed_evidence"]
    independent = contracts["independent_replication"]

    assert reviewed["decomposition"]["human_scientific_review_fraction"] == 0.5
    assert (
        reviewed["decomposition"]["canonical_evidence_engine_promotion_fraction"] == 0.5
    )
    assert "cannot by itself create EVID" in reviewed["anti_gaming_rule"]
    assert "can never be counted" in independent["anti_conflation_rule"]

    decision = (
        ROOT / "research/decisions/2026-09-25_stage1_scientific_consolidation.md"
    ).read_text(encoding="utf-8")
    assert "BLOCKED_CURRENT_EVIDENCE_ENGINE_CONTRACT" in decision
    assert "STAGE1-TOPOLOGY-LINE-001" in decision
    assert "STAGE1-TEMPORAL-ORDER-LINE-002" in decision
