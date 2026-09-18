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
    assert abs(float(stage0["score"]) - 0.825) < 1e-12

    by_id = {criterion["id"]: criterion for criterion in stage0["criteria"]}
    assert by_id["research_question"]["status"] == "met"
    assert by_id["protocol"]["status"] == "met"
    assert by_id["data"]["status"] == "met"
    assert by_id["reviewed_evidence"]["status"] == "partial"
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
    assert readiness["maturity_boundary"]["human_reviewed_evid_complete"] is False
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
    assert review["review_points"]["independent_replication"]["decision"] == "remains_open"
    assert promotion["scientific_evidence"] is False
    assert promotion["evidence_promotion_status"] == "BLOCKED_LEGACY_PROVENANCE_CONTRACT"
    assert promotion["independent_replication_complete"] is False


def test_stage0_partial_reviewed_evidence_is_explicitly_split() -> None:
    stage0 = next(stage for stage in _manifest()["stages"] if stage["stage"] == 0)
    by_id = {criterion["id"]: criterion for criterion in stage0["criteria"]}
    reviewed = by_id["reviewed_evidence"]
    independent = by_id["independent_replication"]
    assert reviewed["status"] == "partial"
    assert "Human Review" in reviewed["label"]
    assert "EVID" in reviewed["label"]
    assert independent["status"] == "partial"
    assert "keine unabhängig autorisierte Replikation" in independent["label"]
