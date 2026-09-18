from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from src.knowledge.models import KnowledgeItem, SourceRecord
from src.learning import (
    LearningDataPartition,
    LearningObjective,
    LearningPlanOrigin,
    LearningPreparationGuard,
    LearningPreparationService,
    LearningSourceRef,
)


def _objective() -> LearningObjective:
    return LearningObjective(
        objective_id="OBJ-001",
        description="Discriminate two environment outcomes after controlled exposure.",
        success_metric="held-out task success",
        evaluation_question="Does performance improve over the pre-learning baseline?",
    )


def _source() -> LearningSourceRef:
    return LearningSourceRef(
        source_id="SRC-001",
        digest="abc123",
        origin="deterministic_environment",
        partition=LearningDataPartition.TRAIN,
        trust="CONTROLLED",
    )


def test_human_preparation_plan_is_non_executable_and_digest_bound() -> None:
    service = LearningPreparationService()
    proposal = service.create_proposal(
        plan_id="LP-001",
        objective=_objective(),
        sources=[_source()],
        baseline_protocol="Run a pre-learning behavior and impulse-response baseline.",
        exposure_protocol="Expose the system to the registered environment episodes.",
        evaluation_protocol="Repeat the same held-out evaluation after learning.",
        stopping_rule="Stop after the preregistered episode count.",
        controls=["learning_off", "same_seed"],
    )

    assert proposal.origin is LearningPlanOrigin.HUMAN
    assert proposal.authority == "proposal_only"
    assert proposal.to_dict()["executed"] is False
    assert len(proposal.digest) == 64

    approved = service.approve(proposal, approved_by="operator")
    assert approved.to_dict()["runtime_authority"] == "none"
    assert approved.to_dict()["executed"] is False
    assert len(approved.digest) == 64


def test_ai_preparation_requires_provenance_and_remains_proposal_only() -> None:
    service = LearningPreparationService()

    with pytest.raises(ValueError, match="ai_interaction_id"):
        service.create_proposal(
            plan_id="LP-AI-001",
            objective=_objective(),
            sources=[_source()],
            baseline_protocol="Measure the baseline first.",
            exposure_protocol="Prepare a sequence of controlled environment episodes.",
            evaluation_protocol="Evaluate on an isolated holdout partition.",
            stopping_rule="Use the preregistered stopping rule.",
            origin=LearningPlanOrigin.AI_ASSISTED,
        )

    proposal = service.create_proposal(
        plan_id="LP-AI-002",
        objective=_objective(),
        sources=[_source()],
        baseline_protocol="Measure the baseline first.",
        exposure_protocol="Prepare a sequence of controlled environment episodes.",
        evaluation_protocol="Evaluate on an isolated holdout partition.",
        stopping_rule="Use the preregistered stopping rule.",
        origin=LearningPlanOrigin.AI_ASSISTED,
        ai_interaction_id="AI-INTERACTION-001",
    )

    assert proposal.authority == "proposal_only"
    assert proposal.ai_interaction_id == "AI-INTERACTION-001"
    assert proposal.to_dict()["executed"] is False


@pytest.mark.parametrize(
    "payload",
    [
        {"weights": [0.1, 0.2]},
        {"training": {"spike_pattern": [1, 0, 1]}},
        {"training": {"injected_current": 4.2}},
        {"evaluation": [{"reward_value": 1.0}]},
        {"nested": {"plasticity_update": {"synapse_weight": 0.9}}},
    ],
)
def test_guard_rejects_direct_neural_or_reward_writes(
    payload: dict[str, object],
) -> None:
    with pytest.raises(PermissionError):
        LearningPreparationGuard.validate_mapping(payload)


def test_guard_allows_protocol_metadata_and_provenance() -> None:
    LearningPreparationGuard.validate_mapping(
        {
            "objective": "learn a causal relation",
            "baseline": "pre-learning probe",
            "source": {"digest": "abc", "partition": "train"},
            "protocol": {"episodes": 50, "holdout": True},
            "evaluation": {"metric": "task_success", "repeat": 10},
        }
    )


def test_source_refs_are_derived_from_knowledge_and_environment_provenance() -> None:
    item = KnowledgeItem(
        item_id="ITEM-001",
        source=SourceRecord(
            source_id="SRC-KNOWLEDGE-001",
            source_type="document",
            locator="fixture://knowledge",
            retrieved_at_ns=1,
            content_sha256="knowledge-digest",
            trust_classification="REVIEWED",
        ),
        title="Controlled relation",
        content="A validated knowledge item.",
        language="en",
        confidence=1.0,
    )

    knowledge_ref = LearningSourceRef.from_knowledge_item(
        item, partition=LearningDataPartition.VALIDATION
    )
    environment_ref = LearningSourceRef.from_environment_capture(
        {
            "environment_id": "ENV-001",
            "capture_id": "CAP-001",
            "digest": "environment-digest",
        },
        partition=LearningDataPartition.HOLDOUT,
    )

    assert knowledge_ref.to_dict() == {
        "source_id": "SRC-KNOWLEDGE-001",
        "digest": "knowledge-digest",
        "origin": "knowledge:document",
        "partition": "validation",
        "trust": "REVIEWED",
    }
    assert environment_ref.to_dict() == {
        "source_id": "ENV-001:CAP-001",
        "digest": "environment-digest",
        "origin": "environment:ENV-001",
        "partition": "holdout",
        "trust": "CONTROLLED",
    }


@pytest.mark.parametrize("field", ["environment_id", "capture_id", "digest"])
def test_environment_capture_derivation_fails_closed_for_missing_provenance(
    field: str,
) -> None:
    capture = {
        "environment_id": "ENV-001",
        "capture_id": "CAP-001",
        "digest": "environment-digest",
    }
    capture[field] = ""

    with pytest.raises(ValueError, match=field):
        LearningSourceRef.from_environment_capture(capture)


def test_partition_leakage_guard_rejects_cross_partition_digest_overlap() -> None:
    sources = [
        _source(),
        LearningSourceRef(
            source_id="SRC-002",
            digest="abc123",
            origin="deterministic_environment",
            partition=LearningDataPartition.HOLDOUT,
        ),
    ]

    with pytest.raises(ValueError, match="leakage"):
        LearningPreparationGuard.validate_partition_leakage(sources)


def test_partition_leakage_guard_rejects_labels_in_holdout() -> None:
    holdout = LearningSourceRef(
        source_id="LABEL-001",
        digest="gold-digest",
        origin="gold_label",
        partition=LearningDataPartition.HOLDOUT,
    )

    with pytest.raises(ValueError, match="label"):
        LearningPreparationGuard.validate_partition_leakage(
            [holdout], gold_label_digests={"gold-digest"}
        )


def test_preparation_persistence_keeps_proposal_and_approval_separate(
    tmp_path: Path,
) -> None:
    service = LearningPreparationService(tmp_path / "preparations")
    proposal = service.create_proposal(
        plan_id="LP-PERSIST-001",
        objective=_objective(),
        sources=[_source()],
        baseline_protocol="baseline",
        exposure_protocol="exposure",
        evaluation_protocol="evaluation",
        stopping_rule="fixed episodes",
    )
    proposal_path = service.persist_proposal(proposal)
    approved = service.approve(proposal, approved_by="operator")
    approved_path = service.persist_approved(approved)

    assert proposal_path.name == "LP-PERSIST-001.json"
    assert approved_path.name == "LP-PERSIST-001-approved.json"
    assert len(service.list_plans()) == 2
    assert service.load_proposal("LP-PERSIST-001").digest == proposal.digest


def test_repository_stage6_source_binding_is_versioned_and_requires_reapproval() -> None:
    root = Path(__file__).resolve().parents[1]
    preparations = root / "research" / "learning" / "preparations"
    service = LearningPreparationService(preparations)

    original = service.load_proposal("LP-20260917194217")
    original_stored = json.loads(
        (preparations / "LP-20260917194217.json").read_text(encoding="utf-8")
    )
    original_approved = json.loads(
        (preparations / "LP-20260917194217-approved.json").read_text(encoding="utf-8")
    )
    assert original.digest == original_stored["digest"]
    assert original.digest == "0d47182d05f2d65d44957a1242f770a3576518c9034b7b014cf8ae4f06333d11"
    assert original_approved["digest"] == "d24210d7e2f83994bc3365cde2010cb865bb6e1d23839e710c5b43bea7232b10"

    revision = service.load_proposal("LP-20260917194217-R1")
    revision_stored = json.loads(
        (preparations / "LP-20260917194217-R1.json").read_text(encoding="utf-8")
    )
    assert revision.digest == revision_stored["digest"]
    assert "requires explicit human reapproval" in revision.rationale

    sources = {source.source_id: source for source in revision.sources}
    expected_paths = {
        "CL-002-EVID": root
        / "research"
        / "experiments"
        / "EXP-S6-SEM-CL-002"
        / "EVID.json",
        "CL-003-DATA": root
        / "research"
        / "experiments"
        / "EXP-S6-SEM-CL-003"
        / "results"
        / "results.json",
    }
    assert set(sources) == set(expected_paths)
    for source_id, path in expected_paths.items():
        assert sources[source_id].trust == "VERIFIED"
        assert sources[source_id].digest == hashlib.sha256(path.read_bytes()).hexdigest()

    assert not (preparations / "LP-20260917194217-R1-approved.json").exists()
    assert revision.authority == "proposal_only"
    assert revision.to_dict()["executed"] is False
