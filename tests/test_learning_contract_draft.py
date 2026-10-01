"""Wave-7 learning/synapse contract draft tests."""

from src.learning.contract import (
    LEARNING_CONTRACT_ID,
    LEARNING_CONTRACT_STATUS,
    learning_contract_check,
    learning_contract_descriptor,
    learning_contract_hash,
    learning_contract_status,
)
from src.learning.learning_engine import LearningParameters


def test_learning_contract_hash_is_stable() -> None:
    assert learning_contract_hash() == learning_contract_hash()
    assert len(learning_contract_hash()) == 64


def test_learning_contract_inventory_matches_cpu_reference_defaults() -> None:
    descriptor = learning_contract_descriptor()
    defaults = LearningParameters()
    assert descriptor["same_tick_pair_rule"] == "ZERO_PAIR_CONTRIBUTION"
    assert defaults.a_plus == 0.1
    assert defaults.a_minus == 0.12
    assert defaults.tau_plus == 20.0
    assert defaults.tau_minus == 20.0


def test_learning_contract_fails_closed_on_known_cpu_cuda_gaps() -> None:
    state = learning_contract_status()
    mapping = state.to_mapping()
    assert LEARNING_CONTRACT_ID == "mhrn-learning-synapse-v0.1-draft"
    assert LEARNING_CONTRACT_STATUS == "DRAFT_NOT_FROZEN"
    assert state.ready_for_cross_backend_learning is False
    blockers = mapping["blockers"]
    assert isinstance(blockers, list)
    assert "LEARNING_CONTRACT_NOT_FROZEN" in blockers
    assert "STABLE_EDGE_ID_NOT_CANONICAL" in blockers
    assert "STP_SEMANTICS_NOT_FROZEN" in blockers
    assert "REWARD_CREDIT_SEMANTICS_NOT_ALIGNED" in blockers
    assert "WEIGHT_DECAY_SEMANTICS_NOT_ALIGNED" in blockers
    assert "CUDA_LEARNING_SEMANTICS_NOT_ALIGNED" in blockers
    assert mapping["scientific_evidence"] is False


def test_learning_contract_self_check_is_non_evidentiary() -> None:
    assert learning_contract_check() is True
