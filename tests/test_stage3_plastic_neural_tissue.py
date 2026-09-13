"""Regression tests for the Stage-3 plastic neural tissue reference."""

from __future__ import annotations

from pathlib import Path

from scripts.run_stage3_reference import build_report
from src.dashboard.development_timeline import build_development_timeline

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ARTIFACT = (
    ROOT
    / "research"
    / "generated"
    / "verification"
    / "plastic_neural_tissue_reference.json"
)


def test_stage3_reference_controls_are_deterministic() -> None:
    report = build_report(run_tests=False)

    assert report["stage"] == 3
    assert report["status"] == "verified"
    assert report["scope"] == "engineering_verification"
    assert report["scientific_promotion"]["automatic_evidence_promotion"] is False

    proofs = report["proofs"]
    assert proofs["three_factor_learning_changes_weights"] is True
    assert proofs["learning_on_changes_fresh_probe_response"] is True
    assert proofs["learning_off_control_has_no_reward_updates"] is True
    assert proofs["sham_replay_destroys_eligibility_effect"] is True
    assert proofs["deterministic_learning_replay_identity"] is True
    assert proofs["finite_bounded_weight_summary"] is True


def test_stage3_reference_keeps_scientific_boundary_explicit() -> None:
    report = build_report(run_tests=False)

    note = report["scientific_promotion"]["note"]
    limits = report["limits"]
    assert "scientific claims" in note
    assert any("10,000-100,000" in item for item in limits)
    assert any("No cognition or consciousness" in item for item in limits)


def test_timeline_closes_stage2_and_tracks_stage3_reference_artifact() -> None:
    timeline = build_development_timeline(ROOT)
    stages = {item["id"]: item for item in timeline["stages"]}

    stage2 = stages["recurrent_snn"]
    assert stage2["implementation_score"] == 1.0
    assert stage2["status"] == "reached"
    assert stage2["next_technical_steps"] == []

    stage3 = stages["plastic_neural_tissue"]
    if REFERENCE_ARTIFACT.is_file():
        assert stage3["implementation_score"] == 1.0
        assert stage3["status"] == "reached"
    else:
        assert stage3["implementation_score"] < 1.0

    assert stage3["research_readiness_score"] < 1.0
    assert "R2 productive-learning evidence closure" in stage3["open_todos"]
