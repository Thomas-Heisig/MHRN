"""Compatibility re-export for Wave-4 CUDA plasticity reference."""

from src.acceleration.cuda.plasticity.reference import SynapseConfig, SynapseState
from src.runtime.determinism import release_uniform, ring_slot

__all__ = [
    "SynapseConfig",
    "SynapseState",
    "release_uniform",
    "ring_slot",
]
