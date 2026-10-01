"""Draft canonical learning/synapse contract descriptor.

This module inventories current CPU semantics and known CUDA-reference
differences. Presence of the descriptor does not authorize cross-backend
learning equivalence or scientific use.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Final

LEARNING_CONTRACT_ID: Final[str] = "mhrn-learning-synapse-v0.1-draft"
LEARNING_CONTRACT_STATUS: Final[str] = "DRAFT_NOT_FROZEN"
LEARNING_CPU_REFERENCE: Final[str] = "src.learning.learning_engine.LearningEngine"
LEARNING_CUDA_STATUS: Final[str] = "NON_CANONICAL_DRAFT"


def learning_contract_descriptor() -> dict[str, object]:
    """Return the current normative inventory without claiming a freeze."""

    return {
        "classification": "LEARNING_SYNAPSE_CONTRACT_DESCRIPTOR",
        "scientific_evidence": False,
        "contract_id": LEARNING_CONTRACT_ID,
        "contract_status": LEARNING_CONTRACT_STATUS,
        "cpu_reference": LEARNING_CPU_REFERENCE,
        "cuda_status": LEARNING_CUDA_STATUS,
        "event_order": "SORTED_(PRE_ID,TARGET_ID)_AFTER_COMPLETED_NETWORK_TICK",
        "same_tick_pair_rule": "ZERO_PAIR_CONTRIBUTION",
        "stdp": {
            "rule": "NEAREST_NEIGHBOUR_PAIR",
            "ltp": "+a_plus*exp(-dt/tau_plus), dt>0",
            "ltd": "-a_minus*exp(dt/tau_minus), dt<0",
            "direct_weight_clamp": True,
        },
        "eligibility": {
            "rule": "LAZY_EXPONENTIAL_DECAY_THEN_ADD_PAIR_DELTA",
            "decay": "exp(-dt/tau_ticks)",
            "checkpointed_cpu_state": True,
        },
        "reward": {
            "effective_tick": "emitted_tick+reward_delay_ticks",
            "rule": "learning_rate*reward*eligibility(effective_tick)",
            "due_order": "PENDING_REWARD_INSERTION_ORDER",
            "synapse_order": "SORTED_STABLE_KEY",
            "optional_trace_reset": True,
        },
        "delayed_signal": {
            "required_rule": "EMITTED_DELAYED_AMPLITUDE_IS_IMMUTABLE",
            "cross_backend_alignment": False,
        },
        "stp_candidate": {
            "status": "CUDA_REFERENCE_CANDIDATE_NOT_FROZEN",
            "release_rng": "COUNTER_RNG(seed,tick,edge)",
            "release_probability": "min(0.95,0.25+0.7*available)",
            "depletion": "max(0.1,available*0.72)",
            "recovery": "min(1.0,available+0.025)",
        },
        "known_semantic_gaps": [
            "CPU_STABLE_IDENTITY_IS_(PRE_ID,TARGET_ID)_AND_DOES_NOT_CANONICALIZE_PARALLEL_EDGES",
            "CPU_REFERENCE_HAS_NO_CANONICAL_STP_STATE",
            "CUDA_REFERENCE_USES_FIXED_CREDIT_WINDOW_WHILE_CPU_REFERENCE_USES_DELAYED_REWARD_PLUS_ELIGIBILITY",
            "CUDA_REFERENCE_APPLIES_PER_TICK_WEIGHT_DECAY_WHILE_CPU_REFERENCE_DOES_NOT",
            "CUDA_REFERENCE_PAIR_AMPLITUDES_DIFFER_FROM_CPU_DEFAULTS",
            "CPU_CUDA_LEARNING_SEMANTICS_NOT_ALIGNED",
        ],
    }


def learning_contract_hash() -> str:
    payload = json.dumps(
        learning_contract_descriptor(),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class LearningContractState:
    contract_frozen: bool = False
    stable_edge_identity_complete: bool = False
    stp_semantics_frozen: bool = False
    reward_credit_semantics_aligned: bool = False
    weight_decay_semantics_aligned: bool = False
    cuda_semantics_aligned: bool = False
    checkpoint_roundtrip_available: bool = True

    @property
    def ready_for_cross_backend_learning(self) -> bool:
        return (
            self.contract_frozen
            and self.stable_edge_identity_complete
            and self.stp_semantics_frozen
            and self.reward_credit_semantics_aligned
            and self.weight_decay_semantics_aligned
            and self.cuda_semantics_aligned
            and self.checkpoint_roundtrip_available
        )

    def to_mapping(self) -> dict[str, object]:
        blockers: list[str] = []
        if not self.contract_frozen:
            blockers.append("LEARNING_CONTRACT_NOT_FROZEN")
        if not self.stable_edge_identity_complete:
            blockers.append("STABLE_EDGE_ID_NOT_CANONICAL")
        if not self.stp_semantics_frozen:
            blockers.append("STP_SEMANTICS_NOT_FROZEN")
        if not self.reward_credit_semantics_aligned:
            blockers.append("REWARD_CREDIT_SEMANTICS_NOT_ALIGNED")
        if not self.weight_decay_semantics_aligned:
            blockers.append("WEIGHT_DECAY_SEMANTICS_NOT_ALIGNED")
        if not self.cuda_semantics_aligned:
            blockers.append("CUDA_LEARNING_SEMANTICS_NOT_ALIGNED")
        if not self.checkpoint_roundtrip_available:
            blockers.append("LEARNING_CHECKPOINT_ROUNDTRIP_NOT_AVAILABLE")
        return {
            "classification": "LEARNING_SYNAPSE_CONTRACT_STATUS",
            "scientific_evidence": False,
            "contract_id": LEARNING_CONTRACT_ID,
            "contract_status": LEARNING_CONTRACT_STATUS,
            "descriptor_hash": learning_contract_hash(),
            "cpu_reference": LEARNING_CPU_REFERENCE,
            "cuda_status": LEARNING_CUDA_STATUS,
            "ready_for_cross_backend_learning": self.ready_for_cross_backend_learning,
            "blockers": blockers,
        }


def learning_contract_status() -> LearningContractState:
    return LearningContractState()


def learning_contract_check() -> bool:
    first = learning_contract_hash()
    second = learning_contract_hash()
    state = learning_contract_status()
    mapping = state.to_mapping()
    blockers = mapping["blockers"]
    return (
        isinstance(blockers, list)
        and first == second
        and len(first) == 64
        and not state.ready_for_cross_backend_learning
        and mapping["scientific_evidence"] is False
        and "LEARNING_CONTRACT_NOT_FROZEN" in blockers
    )


__all__ = [
    "LEARNING_CONTRACT_ID",
    "LEARNING_CONTRACT_STATUS",
    "LEARNING_CPU_REFERENCE",
    "LEARNING_CUDA_STATUS",
    "LearningContractState",
    "learning_contract_check",
    "learning_contract_descriptor",
    "learning_contract_hash",
    "learning_contract_status",
]
