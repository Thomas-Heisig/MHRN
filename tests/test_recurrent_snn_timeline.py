"""Release-timeline regression for Stage 2 recurrent-SNN completion."""

from pathlib import Path

from src.dashboard.development_timeline import build_development_timeline

ROOT = Path(__file__).resolve().parents[1]


def _stage() -> dict[str, object]:
    timeline = build_development_timeline(ROOT)
    return next(item for item in timeline["stages"] if item["id"] == "recurrent_snn")


def test_recurrent_snn_stage_is_technically_complete_from_scoped_verification() -> None:
    stage = _stage()
    deterministic = next(
        item for item in stage["criteria"] if item["id"] == "deterministic_runtime"
    )

    assert stage["implementation_score"] == 1.0
    assert stage["verification_score"] >= 0.75
    assert stage["status"] == "reached"
    assert deterministic["status"] == "verified"
    assert "tests/test_recurrent_snn_contract.py" in deterministic["evidence"]
    assert (
        "research/generated/verification/recurrent_snn_reference.json"
        in deterministic["evidence"]
    )


def test_recurrent_snn_completion_keeps_scientific_boundary() -> None:
    timeline = build_development_timeline(ROOT)
    stage = next(item for item in timeline["stages"] if item["id"] == "recurrent_snn")

    assert stage["implementation_score"] == 1.0
    assert stage["research_readiness_score"] < 1.0
    assert any("cognition" in limit.lower() for limit in stage["known_limits"])
    assert timeline["scientific_note"].startswith(
        "Engineering maturity and technical verification do not imply scientific evidence"
    )
