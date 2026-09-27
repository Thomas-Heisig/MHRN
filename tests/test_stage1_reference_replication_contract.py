"""Contract tests for the Stage-1 cross-implementation reference replication DRAFT."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-REFERENCE-R1.json"
RUNNER_PROTOCOL = (
    ROOT / "reference" / "stage1_topology_brian2" / "reference_protocol.json"
)


def _prereg() -> dict:
    return json.loads(PREREG.read_text(encoding="utf-8"))


def test_reference_replication_is_draft_and_partial_only() -> None:
    prereg = _prereg()

    assert prereg["status"] == "DRAFT_PRE_FREEZE_GATES_PENDING"
    assert prereg["execution_authorized"] is False
    assert prereg["freeze_authorization"]["allowed"] is False
    assert prereg["automatic_evidence_promotion"] is False
    assert prereg["replication_credit_target"] == "partial_only"
    assert prereg["maturity_target_if_successful"]["contribution"] == 0.075
    assert prereg["maturity_target_if_successful"]["stage1_maturity"] == "85% -> 92.5%"


def test_reference_implementation_must_not_import_mhrn_runtime() -> None:
    independence = _prereg()["independence_contract"]

    assert independence["framework"] == "Brian2"
    assert independence["framework_version"] == "2.10.1"
    assert independence["separate_package_required"] is True
    assert "src" in independence["forbidden_import_prefixes"]
    assert "MHRN NeuralNetwork" in independence["forbidden_runtime_dependencies"]
    assert "partial" in independence["authorship_limit"]


def test_reference_primary_family_and_equivalence_are_frozen() -> None:
    prereg = _prereg()
    evaluation = prereg["evaluation"]
    targets = prereg["canonical_targets"]

    assert evaluation["primary_endpoint"] == "first_output_latency_censored"
    assert len(evaluation["primary_contrasts"]) == 5
    assert (
        "five first-output-latency contrasts" in evaluation["primary_multiple_testing"]
    )
    assert set(targets["frozen_bounds"]) == {
        "1d_to_2d",
        "2d_to_3d",
        "3d_to_5d",
        "5d_to_5d_shuffled",
        "5d_to_random_graph",
    }


def test_reference_decision_has_partial_failed_and_inconclusive_paths() -> None:
    decision = _prereg()["decision_rule"]

    assert decision["partial_replication"]
    assert decision["failed_replication"]
    assert decision["inconclusive"]
    assert "equally reportable scientific outcomes" in decision["equal_value_rule"]


def test_reference_runner_is_blinded_to_expected_effects() -> None:
    prereg = _prereg()
    text = prereg["independence_contract"]["runner_blinding"].lower()

    assert "must not contain or load" in text
    assert "effect sizes" in text
    assert "separate verifier" in text


def test_reference_success_cannot_grant_full_replication_credit() -> None:
    semantics = _prereg()["maturity_semantics"]

    assert "7.5/15" in semantics["success"]
    assert "85% to 92.5%" in semantics["success"]
    assert "15/15" in semantics["full_credit"]


def test_reference_runner_protocol_is_sanitized() -> None:
    protocol = json.loads(RUNNER_PROTOCOL.read_text(encoding="utf-8"))
    serialized = json.dumps(protocol, sort_keys=True).lower()

    assert protocol["framework"] == "Brian2"
    assert protocol["framework_version"] == "2.10.1"
    assert "canonical_targets" not in serialized
    assert "frozen_bounds" not in serialized
    assert "evid-2026-19" not in serialized
    assert "exp-s1-topo-promo-r1-20260927" not in serialized
    assert "equivalence_bounds" not in serialized


def test_reference_equivalence_bounds_are_resolution_aware() -> None:
    prereg = _prereg()
    targets = prereg["canonical_targets"]

    assert "1.0 tick" in targets["equivalence_bounds_rule"]
    assert targets["frozen_bounds"]["3d_to_5d"] == [-2.0, 0.0]
    assert "must separately retain" in targets["direction_rule"]
    assert "median must be <0" in targets["direction_rule"]


def test_reference_prefreeze_gates_are_mandatory() -> None:
    prereg = _prereg()
    gates = prereg["prefreeze_requirements"]

    assert gates["integrator_parity"]["required"] is True
    assert gates["mechanism_audit"]["required"] is True
    assert gates["runner_independence_scan"]["required"] is True
    assert gates["seed_freshness"]["required"] is True
