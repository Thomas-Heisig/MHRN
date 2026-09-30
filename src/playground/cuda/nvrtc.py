"""Compatibility re-export for canonical MHRN NVRTC helpers."""

from src.acceleration.cuda.nvrtc import compile_cuda_source, toolkit_root

__all__ = ["compile_cuda_source", "toolkit_root"]
