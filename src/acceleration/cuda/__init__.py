"""Canonical CUDA acceleration layer.

No module in this package may import :mod:`src.playground`.
"""

from .backend import CUDABackend, execution_backend_contract_check
from .driver import CudaDriver, DriverModule
from .errors import CudaDriverError, CudaRuntimeUnavailable
from .memory import DeviceAllocation
from .nvrtc import compile_cuda_source, toolkit_root
from .preflight import CooperativePreflight, cooperative_capacity, validate_cuda_block_size
from .ptxas import PtxasReport, assemble_ptx, parse_ptxas_verbose

__all__ = [
    "CUDABackend",
    "CooperativePreflight",
    "CudaDriver",
    "CudaDriverError",
    "CudaRuntimeUnavailable",
    "DeviceAllocation",
    "DriverModule",
    "PtxasReport",
    "assemble_ptx",
    "compile_cuda_source",
    "cooperative_capacity",
    "parse_ptxas_verbose",
    "toolkit_root",
    "execution_backend_contract_check",
    "validate_cuda_block_size",
]
