"""Wave-4 plasticity capability markers with Wave-7 draft linkage."""

from __future__ import annotations

from typing import Final

from src.learning.contract import (
    LEARNING_CONTRACT_ID as LEARNING_DRAFT_CONTRACT_ID,
)
from src.learning.contract import (
    LEARNING_CONTRACT_STATUS as LEARNING_DRAFT_CONTRACT_STATUS,
)

PLASTICITY_SEMANTICS: Final[str] = "NON_CANONICAL_DRAFT"

# Frozen Wave-4 compatibility boundary. These values are intentionally retained
# so the extracted CUDA backend does not retroactively change its acceptance
# contract while Wave 7 is still drafting the common learning semantics.
LEARNING_CONTRACT_ID: Final[str] = "mhrn-learning-synapse-v1"
LEARNING_CONTRACT_STATUS: Final[str] = "ALIGNMENT_PENDING"

__all__ = [
    "LEARNING_CONTRACT_ID",
    "LEARNING_CONTRACT_STATUS",
    "LEARNING_DRAFT_CONTRACT_ID",
    "LEARNING_DRAFT_CONTRACT_STATUS",
    "PLASTICITY_SEMANTICS",
]
