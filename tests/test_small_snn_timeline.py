"""Release-timeline regression for Stage 1 small-SNN completion."""

from pathlib import Path

from src.dashboard.development_timeline import build_development_timeline

ROOT = Path(__file__).resolve().parents[1]


def test_small_snn_stage_is_technically_complete_from_scoped_verification() -> None:
    timeline = build_development_timeline(ROOT)
    stage = next(item for item in timeline["stages"] if item["id"] == "small_snn")
    spike = next(
        item for item in stage["criteria"] if item["id"] == "spike_propagation"
    )

    assert stage["implementation_score"] == 1.0
    assert stage["verification_score"] == 0.5
    assert stage["research_readiness_score"] < 0.5
    assert stage["status"] == "reached"
    assert spike["status"] == "verified"
    assert "tests/test_small_snn_contract.py" in spike["evidence"]
    assert (
        "research/generated/verification/small_snn_reference.json" in spike["evidence"]
    )


def test_small_snn_completion_does_not_claim_scientific_readiness() -> None:
    timeline = build_development_timeline(ROOT)
    stage = next(item for item in timeline["stages"] if item["id"] == "small_snn")

    assert stage["implementation_score"] == 1.0
    assert stage["research_readiness_score"] == 0.233
    assert "large-scale tractability" in stage["known_limits"][0]
    assert timeline["scientific_note"].startswith(
        "Engineering maturity and technical verification do not imply scientific evidence"
    )
