"""Contract tests for Stage-1 topology efficiency DRAFT and calibration."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-EFFICIENCY-R1.json"
CLAIMS = ROOT / "research" / "registry" / "claims.yaml"
HYPOTHESES = ROOT / "research" / "registry" / "hypotheses.yaml"


def _prereg() -> dict:
    return json.loads(PREREG.read_text(encoding="utf-8"))


def test_efficiency_line_is_unpromoted_and_unfrozen() -> None:
    prereg = _prereg()
    claims = yaml.safe_load(CLAIMS.read_text(encoding="utf-8")) or []
    hypotheses = yaml.safe_load(HYPOTHESES.read_text(encoding="utf-8")) or []
    claim = next(item for item in claims if item["id"] == "CLAIM-S1-EFFICIENCY-001")
    hypothesis = next(item for item in hypotheses if item["id"] == "H-SNN-003-C")

    assert prereg["status"] in {
        "DRAFT_BEFORE_FREEZE",
        "DRAFT_CALIBRATION_GATE_FAILED_FREEZE_BLOCKED",
    }
    assert prereg["execution_authorized"] is False
    assert prereg["scientific_evidence"] is False
    assert prereg["automatic_evidence_promotion"] is False
    assert claim["status"] == "untested"
    assert claim["evidence"] == []
    assert hypothesis["status"] == "untested"
    assert hypothesis["evidence"] == []

    if prereg["status"] == "DRAFT_CALIBRATION_GATE_FAILED_FREEZE_BLOCKED":
        assert prereg["execution_block"]["blocked"] is True
        assert (
            prereg["calibration"]["observed_status_after_run"][
                "3d_recruitment_matched_gate_passed"
            ]
            is False
        )


def test_efficiency_primary_family_is_exactly_eight_tests() -> None:
    prereg = _prereg()
    endpoints = prereg["evaluation"]["primary_endpoints"]
    contrasts = prereg["evaluation"]["primary_contrasts"]

    assert len(endpoints) == 2
    assert len(contrasts) == 4
    assert len(endpoints) * len(contrasts) == 8
    labels = {item["label"] for item in contrasts}
    assert labels == {
        "5d_vs_3d_reference",
        "5d_vs_5d_shuffled",
        "5d_vs_random_graph",
        "5d_vs_3d_recruitment_matched",
    }
    assert "5d_high_recruitment" not in {item["left"] for item in contrasts} | {
        item["right"] for item in contrasts
    }


def test_ratio_contract_prevents_denominator_cherry_picking() -> None:
    validity = _prereg()["evaluation"]["ratio_validity"]

    assert validity["total_spikes_minimum_per_run"] == 32
    assert validity["delivered_events_minimum_per_run"] == 32
    assert "No low-denominator run is deleted" in validity["failure_semantics"]
    assert "Compute each run's ratio first" in validity["ratio_computation"]
    assert "never bootstrapped separately" in validity["bootstrap"]


def test_decision_cases_are_predeclared_and_equal_value() -> None:
    rule = _prereg()["decision_rule"]

    assert (
        "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
        in rule["case_A_supports_specific_effect"]
    )
    assert "INCONCLUSIVE_SPECIFICITY" in rule["case_B_inconclusive_specificity"]
    assert "REFUTES_WITHIN_PROTOCOL" in rule["case_C_refutes"]
    assert "5d_high_recruitment" in rule["high_recruitment_role"]
    assert "scientifically valid outcomes" in rule["equal_value_rule"]


def test_seed_freeze_gate_is_required() -> None:
    prereg = _prereg()
    gate = prereg["seed_freeze_gate"]

    assert gate["required_before_freeze"] is True
    assert gate["allowed_occurrence"] == ("the preregistration file itself only")
    assert "blocks freeze" in gate["collision_semantics"]


def test_temporal_decoder_does_not_enter_efficiency_endpoints() -> None:
    prereg = _prereg()
    readout = prereg["matched_budgets"]["readout_contract"]

    assert readout["decoder"].startswith("none")
    assert "same propagation metrics" in readout["output_procedure"]


def test_valid_calibration_gate_failure_blocks_freeze() -> None:
    prereg = _prereg()
    observed = prereg["calibration"]["observed_status_after_run"]
    policy = prereg["calibration"]["failure_policy"]

    assert observed["verified_execution"] is True
    assert observed["evaluation_seeds_read_or_executed"] is False
    assert observed["3d_recruitment_matched_gate_passed"] is False
    assert observed["freeze_blocked"] is True
    assert "may not be rerun" in policy["valid_gate_failure"]
    assert "new preregistration/calibration revision" in policy["design_change"]
    assert prereg["execution_authorized"] is False
