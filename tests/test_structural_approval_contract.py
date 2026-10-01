"""Wave-6 structural approval contract tests."""

from src.self_organization.approval import (
    ApprovalMode,
    StructuralPlasticityConfig,
    structural_approval_contract_check,
    structural_approval_contract_status,
    structural_policy_artifact_hash,
)


def _enabled(*, auto: bool = False) -> StructuralPlasticityConfig:
    return StructuralPlasticityConfig(
        enabled=True,
        dry_run=False,
        auto_approval=auto,
    )


def test_structural_policy_hash_is_stable_and_mode_bound() -> None:
    config = _enabled()
    first = structural_policy_artifact_hash(config, mode=ApprovalMode.MANUAL_ONLY)
    second = structural_policy_artifact_hash(config, mode=ApprovalMode.MANUAL_ONLY)
    disabled = structural_policy_artifact_hash(config, mode=ApprovalMode.DISABLED)
    assert first == second
    assert first != disabled


def test_manual_mode_fails_closed_without_explicit_authorization() -> None:
    blocked = structural_approval_contract_status(
        _enabled(),
        mode=ApprovalMode.MANUAL_ONLY,
        topology_changes_permitted=True,
        structural_barrier_available=True,
        journal_healthy=True,
        scientific_freeze_allows_mutation=True,
    )
    assert blocked.ready_for_mutation is False
    assert "MANUAL_AUTHORIZATION_REQUIRED" in blocked.to_mapping()["blockers"]

    allowed = structural_approval_contract_status(
        _enabled(),
        mode=ApprovalMode.MANUAL_ONLY,
        manual_authorization_present=True,
        topology_changes_permitted=True,
        structural_barrier_available=True,
        journal_healthy=True,
        scientific_freeze_allows_mutation=True,
    )
    assert allowed.ready_for_mutation is True


def test_preregistered_auto_requires_frozen_policy_artifact() -> None:
    blocked = structural_approval_contract_status(
        _enabled(auto=True),
        mode=ApprovalMode.PREREGISTERED_AUTO,
        topology_changes_permitted=True,
        structural_barrier_available=True,
        journal_healthy=True,
        scientific_freeze_allows_mutation=True,
    )
    assert blocked.ready_for_mutation is False
    assert "PREREGISTERED_POLICY_NOT_FROZEN" in blocked.to_mapping()["blockers"]

    allowed = structural_approval_contract_status(
        _enabled(auto=True),
        mode=ApprovalMode.PREREGISTERED_AUTO,
        preregistered_policy_frozen=True,
        topology_changes_permitted=True,
        structural_barrier_available=True,
        journal_healthy=True,
        scientific_freeze_allows_mutation=True,
    )
    assert allowed.ready_for_mutation is True


def test_structural_approval_descriptor_is_non_evidentiary() -> None:
    assert structural_approval_contract_check() is True
    mapping = structural_approval_contract_status().to_mapping()
    assert mapping["scientific_evidence"] is False
    assert mapping["ready_for_mutation"] is False
