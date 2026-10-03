"""Explicit approval policy for structural proposals."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
from typing import Protocol


class ProposalLike(Protocol):
    @property
    def confidence(self) -> float: ...
    @property
    def kind(self) -> object: ...


STRUCTURAL_APPROVAL_CONTRACT_ID = "mhrn-structural-approval-v0.1"
STRUCTURAL_APPROVAL_CONTRACT_STATUS = "DESCRIPTOR_IMPLEMENTED_BARRIER_ALIGNMENT_PENDING"


class ApprovalMode(str, Enum):
    """Governed structural-mutation authorization modes."""

    MANUAL_ONLY = "MANUAL_ONLY"
    POLICY_AUTO = "POLICY_AUTO"
    PREREGISTERED_AUTO = "PREREGISTERED_AUTO"
    DISABLED = "DISABLED"


@dataclass(frozen=True, slots=True)
class StructuralPlasticityConfig:
    enabled: bool = False
    dry_run: bool = True
    auto_approval: bool = False
    auto_approval_threshold: float = 0.8
    max_changes_per_tick: int = 5
    max_neuron_additions_per_tick: int = 2
    max_neuron_removals_per_tick: int = 0
    max_synapse_additions_per_tick: int = 5
    max_synapse_removals_per_tick: int = 5
    min_neurons: int = 100
    max_neurons: int = 10_000
    allow_neuron_pruning: bool = False
    allow_synapse_pruning: bool = True
    cooldown_ticks: int = 100


def structural_policy_artifact_hash(
    config: StructuralPlasticityConfig,
    *,
    mode: ApprovalMode,
) -> str:
    """Return a stable provenance hash for the approval policy."""

    payload = {
        "contract_id": STRUCTURAL_APPROVAL_CONTRACT_ID,
        "mode": mode.value,
        "config": asdict(config),
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class StructuralApprovalContractState:
    """Fail-closed projection of the executable approval contract."""

    mode: ApprovalMode
    policy_artifact_hash: str
    execution_enabled: bool
    policy_auto_enabled: bool
    manual_authorization_present: bool
    preregistered_policy_frozen: bool
    topology_changes_permitted: bool
    structural_barrier_available: bool
    journal_healthy: bool
    scientific_freeze_allows_mutation: bool

    @property
    def mode_authorized(self) -> bool:
        """Return whether the selected approval mode has its own authority."""

        if self.mode is ApprovalMode.DISABLED:
            return False
        if self.mode is ApprovalMode.MANUAL_ONLY:
            return self.manual_authorization_present
        if self.mode is ApprovalMode.POLICY_AUTO:
            return self.policy_auto_enabled
        return self.policy_auto_enabled and self.preregistered_policy_frozen

    @property
    def ready_for_mutation(self) -> bool:
        return (
            self.execution_enabled
            and self.mode_authorized
            and self.topology_changes_permitted
            and self.structural_barrier_available
            and self.journal_healthy
            and self.scientific_freeze_allows_mutation
        )

    def to_mapping(self) -> dict[str, object]:
        blockers: list[str] = []
        if not self.execution_enabled:
            blockers.append("STRUCTURAL_EXECUTION_DISABLED_OR_DRY_RUN")
        if self.mode is ApprovalMode.DISABLED:
            blockers.append("STRUCTURAL_APPROVAL_DISABLED")
        elif self.mode is ApprovalMode.MANUAL_ONLY:
            if not self.manual_authorization_present:
                blockers.append("MANUAL_AUTHORIZATION_REQUIRED")
        elif self.mode is ApprovalMode.POLICY_AUTO:
            if not self.policy_auto_enabled:
                blockers.append("POLICY_AUTO_NOT_ENABLED")
        elif self.mode is ApprovalMode.PREREGISTERED_AUTO:
            if not self.policy_auto_enabled:
                blockers.append("POLICY_AUTO_NOT_ENABLED")
            if not self.preregistered_policy_frozen:
                blockers.append("PREREGISTERED_POLICY_NOT_FROZEN")
        if not self.topology_changes_permitted:
            blockers.append("TOPOLOGY_CHANGES_NOT_PERMITTED")
        if not self.structural_barrier_available:
            blockers.append("STRUCTURAL_BARRIER_NOT_AVAILABLE")
        if not self.journal_healthy:
            blockers.append("STRUCTURAL_JOURNAL_NOT_HEALTHY")
        if not self.scientific_freeze_allows_mutation:
            blockers.append("SCIENTIFIC_FREEZE_BLOCKS_MUTATION")
        return {
            "classification": "STRUCTURAL_APPROVAL_CONTRACT_STATUS",
            "scientific_evidence": False,
            "contract_id": STRUCTURAL_APPROVAL_CONTRACT_ID,
            "contract_status": STRUCTURAL_APPROVAL_CONTRACT_STATUS,
            "mode": self.mode.value,
            "policy_artifact_hash": self.policy_artifact_hash,
            "execution_enabled": self.execution_enabled,
            "policy_auto_enabled": self.policy_auto_enabled,
            "manual_authorization_present": self.manual_authorization_present,
            "preregistered_policy_frozen": self.preregistered_policy_frozen,
            "topology_changes_permitted": self.topology_changes_permitted,
            "structural_barrier_available": self.structural_barrier_available,
            "journal_healthy": self.journal_healthy,
            "scientific_freeze_allows_mutation": self.scientific_freeze_allows_mutation,
            "mode_authorized": self.mode_authorized,
            "ready_for_mutation": self.ready_for_mutation,
            "blockers": blockers,
        }


def structural_approval_contract_status(
    config: StructuralPlasticityConfig | None = None,
    *,
    mode: ApprovalMode = ApprovalMode.DISABLED,
    manual_authorization_present: bool = False,
    preregistered_policy_frozen: bool = False,
    topology_changes_permitted: bool = False,
    structural_barrier_available: bool = False,
    journal_healthy: bool = False,
    scientific_freeze_allows_mutation: bool = False,
) -> StructuralApprovalContractState:
    cfg = config or StructuralPlasticityConfig()
    execution_enabled = bool(cfg.enabled and not cfg.dry_run)
    policy_auto_enabled = bool(execution_enabled and cfg.auto_approval)
    return StructuralApprovalContractState(
        mode=mode,
        policy_artifact_hash=structural_policy_artifact_hash(cfg, mode=mode),
        execution_enabled=execution_enabled,
        policy_auto_enabled=policy_auto_enabled,
        manual_authorization_present=manual_authorization_present,
        preregistered_policy_frozen=preregistered_policy_frozen,
        topology_changes_permitted=topology_changes_permitted,
        structural_barrier_available=structural_barrier_available,
        journal_healthy=journal_healthy,
        scientific_freeze_allows_mutation=scientific_freeze_allows_mutation,
    )


def structural_approval_contract_check() -> bool:
    """Self-check descriptor identity, hashing and fail-closed mode semantics."""

    manual_cfg = StructuralPlasticityConfig(
        enabled=True,
        dry_run=False,
        auto_approval=False,
    )
    auto_cfg = StructuralPlasticityConfig(
        enabled=True,
        dry_run=False,
        auto_approval=True,
    )
    first = structural_policy_artifact_hash(
        manual_cfg,
        mode=ApprovalMode.MANUAL_ONLY,
    )
    second = structural_policy_artifact_hash(
        manual_cfg,
        mode=ApprovalMode.MANUAL_ONLY,
    )
    different = structural_policy_artifact_hash(
        manual_cfg,
        mode=ApprovalMode.DISABLED,
    )
    blocked_manual = structural_approval_contract_status(
        manual_cfg,
        mode=ApprovalMode.MANUAL_ONLY,
        topology_changes_permitted=True,
        structural_barrier_available=True,
        journal_healthy=True,
        scientific_freeze_allows_mutation=True,
    )
    allowed_manual = structural_approval_contract_status(
        manual_cfg,
        mode=ApprovalMode.MANUAL_ONLY,
        manual_authorization_present=True,
        topology_changes_permitted=True,
        structural_barrier_available=True,
        journal_healthy=True,
        scientific_freeze_allows_mutation=True,
    )
    blocked_preregistered = structural_approval_contract_status(
        auto_cfg,
        mode=ApprovalMode.PREREGISTERED_AUTO,
        topology_changes_permitted=True,
        structural_barrier_available=True,
        journal_healthy=True,
        scientific_freeze_allows_mutation=True,
    )
    return (
        first == second
        and first != different
        and not blocked_manual.ready_for_mutation
        and allowed_manual.ready_for_mutation
        and not blocked_preregistered.ready_for_mutation
        and blocked_manual.to_mapping()["scientific_evidence"] is False
    )


@dataclass(frozen=True, slots=True)
class ApprovalDecision:
    approved: bool
    automatic: bool
    reason: str


class ProposalApprovalPolicy:
    """Approves only explicitly allowed, safe high-confidence proposals."""

    def __init__(self, config: StructuralPlasticityConfig) -> None:
        self.config = config

    def evaluate(
        self,
        proposal: ProposalLike,
        *,
        safety_ok: bool,
        cooldown_ok: bool,
        kind_allowed: bool,
    ) -> ApprovalDecision:
        if not self.config.enabled:
            return ApprovalDecision(False, False, "structural plasticity disabled")
        if self.config.dry_run:
            return ApprovalDecision(False, False, "dry-run mode")
        if not self.config.auto_approval:
            return ApprovalDecision(False, False, "manual approval required")
        if not safety_ok:
            return ApprovalDecision(False, True, "safety limits rejected proposal")
        if not cooldown_ok:
            return ApprovalDecision(False, True, "cooldown active")
        if not kind_allowed:
            return ApprovalDecision(False, True, "proposal kind disabled")
        for value in (proposal.confidence, self.config.auto_approval_threshold):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or not 0.0 <= value <= 1.0
            ):
                return ApprovalDecision(False, True, "invalid confidence or threshold")
        if proposal.confidence < self.config.auto_approval_threshold:
            return ApprovalDecision(False, True, "confidence below threshold")
        return ApprovalDecision(True, True, "auto-approval threshold satisfied")
