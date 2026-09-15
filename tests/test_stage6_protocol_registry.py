from __future__ import annotations

from pathlib import Path

from src.research.stage6_protocol_registry import (
    stage6_protocol_by_id,
    stage6_protocols_for_question,
    validate_stage6_bundle,
)

RESEARCH = Path(__file__).resolve().parents[1] / "research"


def test_stage6_registry_supports_multiple_protocols_per_question() -> None:
    memory = stage6_protocols_for_question(RESEARCH, "RQ-MEM-002")
    world = stage6_protocols_for_question(RESEARCH, "RQ-WM-001")

    assert {item["id"] for item in memory} == {
        "s6_epi_001_v1",
        "s6_sem_001_v1",
        "s6_rpl_001_v1",
    }
    assert {item["id"] for item in world} == {
        "s6_pe_001_v1",
        "s6_wm_001_v1",
        "s6_wm_002_v1",
        "s6_nwm_001_v1",
    }


def test_stage6_registry_resolves_neural_world_model_by_id() -> None:
    protocol = stage6_protocol_by_id(RESEARCH, "s6_nwm_001_v1")
    assert protocol is not None
    assert protocol["experiment_id"] == "S6-NWM-001"
    assert protocol["snn_involved"] is True


def test_stage6_protocol_and_preregistration_bundles_are_in_parity() -> None:
    summary = validate_stage6_bundle(RESEARCH)

    assert summary["protocol_count"] == 7
    assert summary["questions"] == {"RQ-MEM-002": 3, "RQ-WM-001": 4}
    assert summary["automatic_evidence_promotion"] is False
    assert summary["human_review_required"] is True
