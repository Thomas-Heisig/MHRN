from __future__ import annotations

from src.research.semantic_contracts import (
    classify_design_adequacy,
    classify_semantic_status,
)


def test_det_001_accepts_same_seed_tonic_replica_pair() -> None:
    status, note = classify_semantic_status(
        "RQ-DET-001",
        "tonic_spike_reproducibility_v1",
        {"same_seed_tonic_replica_pair"},
    )
    assert status == "DIRECT_MATCH"
    assert "identischem Seed" in note


def test_det_001_accepts_explicit_network_replica_pairs() -> None:
    status, _ = classify_semantic_status(
        "RQ-DET-001",
        "deterministic_replica_v1",
        {
            "recurrence_off_replica_a",
            "recurrence_off_replica_b",
            "recurrence_on_replica_a",
            "recurrence_on_replica_b",
        },
    )
    assert status == "DIRECT_MATCH"


def test_snn_002_rejects_tonic_pair_and_points_to_det_001() -> None:
    status, note = classify_semantic_status(
        "RQ-SNN-002",
        "tonic_spike_reproducibility_v1",
        {"same_seed_tonic_replica_pair"},
    )
    assert status == "MISMATCH"
    assert "RQ-DET-001" in note


def test_snn_002_keeps_registered_recurrence_contract() -> None:
    status, _ = classify_semantic_status(
        "RQ-SNN-002",
        "science_suite_v1",
        {"recurrence_off", "recurrence_on"},
    )
    assert status == "DIRECT_MATCH"


def test_snn_003_accepts_registered_topology_conditions() -> None:
    status, note = classify_semantic_status(
        "RQ-SNN-003",
        "topology_propagation_v1",
        {"1d", "2d", "3d", "5d", "5d_shuffled", "random_graph"},
    )
    assert status == "DIRECT_MATCH"
    assert "Testadäquanz" in note


def test_snn_003_v1_is_semantically_matched_but_design_inadequate() -> None:
    status, note = classify_design_adequacy(
        "RQ-SNN-003",
        "topology_propagation_v1",
    )
    assert status == "INADEQUATE_TO_TEST_HYPOTHESIS"
    assert "Drei-Neuronen-Kette" in note
    assert "kein Nullbefund" in note
