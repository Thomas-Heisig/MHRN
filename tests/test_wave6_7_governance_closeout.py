"""Governance closeout tests for Waves 6/7 and CPU self-parity preregistration."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_wave6_7_draft_documents_have_explicit_governance_overrides() -> None:
    payload = json.loads(
        (ROOT / "research" / "document_governance_overrides.json").read_text(
            encoding="utf-8"
        )
    )
    overrides = payload["overrides"]
    for path in (
        "docs/canonical/STRUCTURAL_APPROVAL_CONTRACT_DRAFT.md",
        "docs/canonical/LEARNING_CONTRACT_DRAFT.md",
    ):
        item = overrides[path]
        assert item["status"] == "current_wip"
        assert "not_data_or_evidence" in item["evidence_role"]


def test_first_structural_governance_run_is_manual_but_not_authorized() -> None:
    decision = (
        ROOT / "research" / "decisions" / "2026-10-01_wave6_first_governed_run_mode.md"
    ).read_text(encoding="utf-8")
    assert "MANUAL_ONLY" in decision
    assert "system default remains `DISABLED`" in decision
    assert "execution not authorized" in decision


def test_wave7_divergence_inventory_has_exact_five_open_blockers() -> None:
    payload = json.loads(
        (
            ROOT / "research" / "specifications" / "WAVE7_LEARNING_DIVERGENCES.json"
        ).read_text(encoding="utf-8")
    )
    assert payload["cross_backend_learning_equivalence"] is False
    blockers = payload["blockers"]
    assert [item["id"] for item in blockers] == [
        "EDGE_IDENTITY",
        "STP",
        "REWARD_CREDIT",
        "WEIGHT_DECAY",
        "PAIR_DEFAULTS",
    ]
    assert all(item["status"] == "OPEN" for item in blockers)


def test_cpu_self_parity_preregistration_is_frozen_and_cpu_only() -> None:
    payload = json.loads(
        (ROOT / "research" / "preregistrations" / "PREREG-CPU-PAR-001.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["research_question"] == "RQ-CPU-PAR-001"
    assert payload["hypothesis"] == "H-CPU-PAR-001-A"
    assert payload["mode"] == "CONFIRMATORY"
    assert payload["seed_strategy"]["exact_seeds"] == list(range(910001, 910021))
    assert payload["structural_governance"]["approval_mode"] == "DISABLED"
    assert payload["execution"]["authorized"] is False
    assert payload["freeze"]["status"] == "FROZEN"
    assert len(payload["primary_outcomes"]) == 2
