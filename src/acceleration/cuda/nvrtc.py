"""Optional CUDA source compilation without a host C++ compiler."""

from __future__ import annotations

import ctypes
import os
import re
import shutil
from contextlib import nullcontext
from pathlib import Path

from .errors import CudaRuntimeUnavailable


def toolkit_root() -> Path:
    candidates = [os.environ.get("CUDA_PATH", ""), os.environ.get("CUDA_HOME", "")]
    compiler = shutil.which("nvcc")
    if compiler:
        candidates.append(str(Path(compiler).resolve().parent.parent))
    candidates.append("/usr/local/cuda")
    if os.name == "nt":
        base = Path(os.environ.get("ProgramFiles", "C:/Program Files"))
        candidates.extend(
            str(p)
            for p in sorted(
                (base / "NVIDIA GPU Computing Toolkit/CUDA").glob("v*"), reverse=True
            )
        )
    for candidate in candidates:
        if candidate and (Path(candidate) / "include/cooperative_groups.h").is_file():
            return Path(candidate)
    raise CudaRuntimeUnavailable("CUDA toolkit headers/NVRTC are required")


def compile_cuda_source(source: str, *, target_sm: str = "sm_86") -> str:
    """Compile a bounded trusted source string to PTX; no GPU is required."""
    if not re.fullmatch(r"sm_[0-9]{2,3}", target_sm):
        raise ValueError("invalid CUDA architecture")
    root = toolkit_root()
    patterns = (
        ["bin/nvrtc64_*.dll", "bin/x64/nvrtc64_*.dll"]
        if os.name == "nt"
        else ["lib64/libnvrtc.so*", "targets/x86_64-linux/lib/libnvrtc.so*"]
    )
    libraries = [
        p for pattern in patterns for p in root.glob(pattern) if ".alt." not in p.name
    ]
    if not libraries:
        raise CudaRuntimeUnavailable("NVRTC library is not installed")
    library = libraries[0]
    directory = (
        getattr(os, "add_dll_directory")(str(library.parent))
        if os.name == "nt"
        else nullcontext()
    )
    with directory:
        lib = ctypes.CDLL(str(library))
        lib.nvrtcCreateProgram.argtypes = [
            ctypes.POINTER(ctypes.c_void_p),
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]
        lib.nvrtcCompileProgram.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_char_p),
        ]
        lib.nvrtcGetProgramLogSize.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_size_t),
        ]
        lib.nvrtcGetProgramLog.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        lib.nvrtcGetPTXSize.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_size_t),
        ]
        lib.nvrtcGetPTX.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        lib.nvrtcDestroyProgram.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        program = ctypes.c_void_p()
        code = lib.nvrtcCreateProgram(
            ctypes.byref(program), source.encode(), b"recurrent.cu", 0, None, None
        )
        if code:
            raise CudaRuntimeUnavailable(f"nvrtcCreateProgram failed: {code}")
        try:
            options = [
                f"--gpu-architecture=compute_{target_sm[3:]}",
                f"--include-path={root / 'include'}",
                "--std=c++17",
                "--fmad=false",
            ]
            if (root / "include/cccl").is_dir():
                options.append(f"--include-path={root / 'include/cccl'}")
            encoded = (ctypes.c_char_p * len(options))(
                *(item.encode() for item in options)
            )
            code = lib.nvrtcCompileProgram(program, len(options), encoded)
            size = ctypes.c_size_t()
            lib.nvrtcGetProgramLogSize(program, ctypes.byref(size))
            log = ctypes.create_string_buffer(max(1, size.value))
            lib.nvrtcGetProgramLog(program, log)
            if code:
                raise CudaRuntimeUnavailable(
                    f"NVRTC compilation failed ({code}): {log.value.decode(errors='replace')}"
                )
            if lib.nvrtcGetPTXSize(program, ctypes.byref(size)):
                raise CudaRuntimeUnavailable("NVRTC PTX size unavailable")
            ptx = ctypes.create_string_buffer(size.value)
            if lib.nvrtcGetPTX(program, ptx):
                raise CudaRuntimeUnavailable("NVRTC PTX retrieval failed")
            return ptx.value.decode()
        finally:
            lib.nvrtcDestroyProgram(ctypes.byref(program))
