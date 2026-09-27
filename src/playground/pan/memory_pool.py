"""CUDA memory-budget planning for the bounded Playground reference backend."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MemoryEstimate:
    """Estimated tensor/storage footprint for a hypothetical CUDA layout."""

    neurons: int
    synapses: int
    state_dimensions: int
    state_bytes: int
    hypervector_bytes: int
    geometry_bytes: int
    synapse_bytes: int
    feedback_bytes: int
    event_bytes: int
    workspace_bytes: int

    @property
    def total_bytes(self) -> int:
        return (
            self.state_bytes
            + self.hypervector_bytes
            + self.geometry_bytes
            + self.synapse_bytes
            + self.feedback_bytes
            + self.event_bytes
            + self.workspace_bytes
        )

    def descriptor(self) -> dict[str, object]:
        return {
            "neurons": self.neurons,
            "synapses": self.synapses,
            "state_dimensions": self.state_dimensions,
            "state_bytes": self.state_bytes,
            "hypervector_bytes": self.hypervector_bytes,
            "geometry_bytes": self.geometry_bytes,
            "synapse_bytes": self.synapse_bytes,
            "feedback_bytes": self.feedback_bytes,
            "event_bytes": self.event_bytes,
            "workspace_bytes": self.workspace_bytes,
            "total_bytes": self.total_bytes,
            "total_mib": self.total_bytes / (1024**2),
        }


class CUDAMemoryPool:
    """Budget planner only; it does not allocate Torch/CUDA tensors."""

    def __init__(self, max_mb: int = 2048, high_watermark: float = 0.85) -> None:
        if max_mb < 128:
            raise ValueError("cuda memory budget must be at least 128 MiB")
        if not 0.5 <= high_watermark <= 0.99:
            raise ValueError("high_watermark must be between 0.5 and 0.99")
        self.max_bytes = max_mb * 1024**2
        self.high_watermark = high_watermark

    def estimate(
        self,
        *,
        neurons: int,
        synapses: int,
        state_dimensions: int,
        event_capacity: int = 10_000,
    ) -> MemoryEstimate:
        if neurons < 1 or synapses < 0 or state_dimensions < 1:
            raise ValueError("memory estimate dimensions must be non-negative")
        fp16 = 2
        int32 = 4
        uint16 = 2
        state_bytes = neurons * 3 * fp16
        hypervector_bytes = neurons * state_dimensions * fp16
        geometry_bytes = neurons * 5 * fp16
        # src int32 + dst int32 + weight fp16 + delay uint16
        synapse_bytes = synapses * (2 * int32 + fp16 + uint16)
        feedback_bytes = neurons * state_dimensions * fp16
        event_bytes = event_capacity * 16
        workspace_bytes = max(64 * 1024**2, 2 * (state_bytes + hypervector_bytes))
        return MemoryEstimate(
            neurons=neurons,
            synapses=synapses,
            state_dimensions=state_dimensions,
            state_bytes=state_bytes,
            hypervector_bytes=hypervector_bytes,
            geometry_bytes=geometry_bytes,
            synapse_bytes=synapse_bytes,
            feedback_bytes=feedback_bytes,
            event_bytes=event_bytes,
            workspace_bytes=workspace_bytes,
        )

    def summary(self, estimate: MemoryEstimate) -> dict[str, object]:
        high_water_bytes = int(self.max_bytes * self.high_watermark)
        return {
            "classification": "PLAYGROUND_STORAGE_BUDGET",
            "scientific_evidence": False,
            "cuda_budget_bytes": self.max_bytes,
            "cuda_budget_mib": self.max_bytes / (1024**2),
            "high_watermark": self.high_watermark,
            "high_watermark_bytes": high_water_bytes,
            "estimate": estimate.descriptor(),
            "fits_budget": estimate.total_bytes <= self.max_bytes,
            "fits_high_watermark": estimate.total_bytes <= high_water_bytes,
            "allocation_mode": "REFERENCE_ESTIMATE_ONLY",
            "cuda_allocation_status": "NOT_IMPLEMENTED_IN_PYTHON_REFERENCE_BACKEND",
        }
