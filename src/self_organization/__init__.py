"""Self-organization and controlled structural plasticity."""

from .approval import (
    STRUCTURAL_APPROVAL_CONTRACT_ID,
    STRUCTURAL_APPROVAL_CONTRACT_STATUS,
    ApprovalDecision,
    ApprovalMode,
    ProposalApprovalPolicy,
    StructuralApprovalContractState,
    StructuralPlasticityConfig,
    structural_approval_contract_check,
    structural_approval_contract_status,
    structural_policy_artifact_hash,
)
from .coordinator import (
    ProposalDecision,
    SelfOrganizationCoordinator,
    SelfOrganizationSnapshot,
)
from .engine import SelfOrganizationEngine
from .morphology import MorphologyBudget, MorphologyLedger, StructuralCostModel
from .plasticity import (
    ChangeKind,
    PlasticitySafetyLimits,
    StructuralChange,
    StructuralPlasticityEngine,
)
from .policy import (
    PolicyReport,
    ProposalKind,
    SelfOrganizationParameters,
    SelfOrganizationPolicy,
    SelfOrganizationPolicyConfig,
    StructuralAction,
    StructuralProposal,
)

__all__ = [
    "STRUCTURAL_APPROVAL_CONTRACT_ID",
    "STRUCTURAL_APPROVAL_CONTRACT_STATUS",
    "ApprovalDecision",
    "ApprovalMode",
    "ChangeKind",
    "PlasticitySafetyLimits",
    "PolicyReport",
    "MorphologyBudget",
    "MorphologyLedger",
    "ProposalApprovalPolicy",
    "ProposalDecision",
    "ProposalKind",
    "SelfOrganizationCoordinator",
    "SelfOrganizationEngine",
    "SelfOrganizationParameters",
    "SelfOrganizationPolicy",
    "SelfOrganizationPolicyConfig",
    "SelfOrganizationSnapshot",
    "StructuralAction",
    "StructuralChange",
    "StructuralCostModel",
    "StructuralApprovalContractState",
    "StructuralPlasticityConfig",
    "structural_approval_contract_check",
    "structural_approval_contract_status",
    "structural_policy_artifact_hash",
    "StructuralPlasticityEngine",
    "StructuralProposal",
]
