"""Backend-neutral CUDA cooperative launch preflight contracts."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CooperativePreflight:
    """Host/device limits required for a cooperative persistent launch."""

    cooperative_launch: bool
    multiprocessor_count: int
    active_blocks_per_sm: int
    block_size: int
    required_blocks: int
    resident_block_capacity: int
    launch_fits: bool
    n_neurons: int

    def to_mapping(self) -> dict[str, object]:
        return {
            "cooperative_launch": self.cooperative_launch,
            "multiprocessor_count": self.multiprocessor_count,
            "active_blocks_per_sm": self.active_blocks_per_sm,
            "block_size": self.block_size,
            "required_blocks": self.required_blocks,
            "resident_block_capacity": self.resident_block_capacity,
            "launch_fits": self.launch_fits,
            "n_neurons": self.n_neurons,
        }


def validate_cuda_block_size(block_size: int) -> int:
    """Validate a legal one-dimensional CUDA block size."""

    if isinstance(block_size, bool) or not isinstance(block_size, int):
        raise ValueError("block_size must be an integer")
    if not 1 <= block_size <= 1024:
        raise ValueError("block_size must be in [1, 1024]")
    if block_size % 32 != 0:
        raise ValueError("block_size must be a multiple of 32")
    return block_size


def cooperative_capacity(
    *,
    n_neurons: int,
    block_size: int,
    multiprocessor_count: int,
    active_blocks_per_sm: int,
    cooperative_launch: bool = True,
) -> CooperativePreflight:
    """Pure helper used by CI to verify occupancy-bound grid logic."""

    if (
        min(
            n_neurons,
            block_size,
            multiprocessor_count,
            active_blocks_per_sm,
        )
        <= 0
    ):
        raise ValueError("cooperative capacity inputs must be positive")
    required = math.ceil(n_neurons / block_size)
    capacity = multiprocessor_count * active_blocks_per_sm
    return CooperativePreflight(
        cooperative_launch=cooperative_launch,
        multiprocessor_count=multiprocessor_count,
        active_blocks_per_sm=active_blocks_per_sm,
        block_size=block_size,
        required_blocks=required,
        resident_block_capacity=capacity,
        launch_fits=cooperative_launch and required <= capacity,
        n_neurons=n_neurons,
    )
