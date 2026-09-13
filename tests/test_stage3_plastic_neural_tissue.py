"""Regression tests for the Stage-3 plastic neural tissue reference."""

from __future__ import annotations

from scripts.run_stage3_reference import build_report


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
