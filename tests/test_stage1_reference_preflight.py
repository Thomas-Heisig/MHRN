"""Pre-freeze contract tests for Stage-1 Brian2 reference replication."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-REFERENCE-R1.json"
PROTOCOL = ROOT / "reference" / "stage1_topology_brian2" / "reference_protocol.json"


def _prereg() -> dict:
    return json.loads(PREREG.read_text(encoding="utf-8"))


def test_reference_freeze_is_blocked_until_all_gates_pass() -> None:
    prereg = _prereg()
    assert prereg["status"] == "DRAFT_PRE_FREEZE_GATES_PENDING"
    assert prereg["execution_authorized"] is False
    assert prereg["freeze_authorization"]["allowed"] is False
    assert prereg["freeze_authorization"]["reference_runner_implementation_allowed"] is True
    assert prereg["freeze_authorization"]["reference_runner_execution_allowed"] is False


def test_reference_protocol_seed_block_matches_preregistration() -> None:
    prereg = _prereg()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert protocol["seeds"] == prereg["evaluation"]["seeds"]
    seeds = prereg["evaluation"]["seeds"]
    assert len(seeds) == 20
    assert all(int(right) - int(left) == 1 for left, right in zip(seeds, seeds[1:]))
    assert min(map(int, seeds)) > 800_000_000


def test_resolution_aware_small_effect_bound_is_frozen() -> None:
    prereg = _prereg()
    assert prereg["canonical_targets"]["frozen_bounds"]["3d_to_5d"] == [-1.5, -0.5]
    assert "known sensitivity limitation" in prereg["canonical_targets"]["resolution_note"]


def test_mechanism_audit_requires_adaptation_and_homeostasis_translation() -> None:
    gate = _prereg()["pre_freeze_gates"]["mechanism_audit"]
    assert gate["required"] is True
    assert gate["status"] == "PASS_DOCUMENTED"
    text = gate["rule"].lower()
    assert "threshold adaptation" in text
    assert "homeostasis" in text


def test_reference_outcome_classes_are_fully_predeclared() -> None:
    rule = _prereg()["decision_rule"]
    assert rule["partial_replication"]
    assert rule["failed_replication"]
    assert rule["inconclusive"]
    assert "equally reportable scientific outcomes" in rule["equal_value_rule"]


def test_reset_and_synapse_prefreeze_gates_are_mandatory() -> None:
    prereg = _prereg()
    requirements = prereg["prefreeze_requirements"]

    assert requirements["reset_parity"]["required"] is True
    assert requirements["synapse_delay_parity"]["required"] is True
    assert requirements["reset_parity"]["tolerance_abs"] == 1e-12
    assert requirements["synapse_delay_parity"]["tolerance_abs"] == 1e-12
    assert prereg["freeze_authorization"]["allowed"] is False
