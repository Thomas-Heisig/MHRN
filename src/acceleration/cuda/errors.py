"""Canonical CUDA acceleration errors."""

class CudaRuntimeUnavailable(RuntimeError):
    """Raised when an optional CUDA-1 dependency is not available."""


class CudaDriverError(RuntimeError):
    """Raised when a CUDA Driver API call fails."""
