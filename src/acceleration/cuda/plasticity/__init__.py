"""Canonical CUDA plasticity engineering package."""

from .backend import BuilderSynapseStepper
from .contracts import (
    LEARNING_CONTRACT_ID,
    LEARNING_CONTRACT_STATUS,
    PLASTICITY_SEMANTICS,
)
from .reference import SynapseConfig, SynapseState

__all__ = [
    "BuilderSynapseStepper",
    "LEARNING_CONTRACT_ID",
    "LEARNING_CONTRACT_STATUS",
    "PLASTICITY_SEMANTICS",
    "SynapseConfig",
    "SynapseState",
]
