"""Canonical PTX assembly and resource-report helpers."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .errors import CudaDriverError, CudaRuntimeUnavailable


@dataclass(frozen=True, slots=True)
class PtxasReport:
    """Measured resource report emitted by ptxas."""

    target_sm: str
    registers: int | None
    shared_bytes: int | None
    constant_bytes: int | None
    stack_bytes: int | None
    spill_store_bytes: int | None
    spill_load_bytes: int | None
    cubin_path: Path
    verbose_output: str

    def to_mapping(self) -> dict[str, object]:
        return {
            "target_sm": self.target_sm,
            "registers": self.registers,
            "shared_bytes": self.shared_bytes,
            "constant_bytes": self.constant_bytes,
            "stack_bytes": self.stack_bytes,
            "spill_store_bytes": self.spill_store_bytes,
            "spill_load_bytes": self.spill_load_bytes,
            "cubin_path": str(self.cubin_path),
            "verbose_output": self.verbose_output,
        }


_REGISTER_RE = re.compile(r"Used\s+(\d+)\s+registers")
_SMEM_RE = re.compile(r"(\d+)\s+bytes smem")
_CMEM_RE = re.compile(r"(\d+)\s+bytes cmem\[\d+\]")
_STACK_RE = re.compile(r"(\d+)\s+bytes stack frame")
_SPILL_STORE_RE = re.compile(r"(\d+)\s+bytes spill stores")
_SPILL_LOAD_RE = re.compile(r"(\d+)\s+bytes spill loads")


def _first_int(pattern: re.Pattern[str], text: str) -> int | None:
    match = pattern.search(text)
    return int(match.group(1)) if match else None


def parse_ptxas_verbose(
    verbose_output: str,
    *,
    target_sm: str,
    cubin_path: Path,
) -> PtxasReport:
    """Parse stable resource fields from ptxas verbose diagnostics."""

    constant_values = [int(value) for value in _CMEM_RE.findall(verbose_output)]
    return PtxasReport(
        target_sm=target_sm,
        registers=_first_int(_REGISTER_RE, verbose_output),
        shared_bytes=_first_int(_SMEM_RE, verbose_output),
        constant_bytes=sum(constant_values) if constant_values else None,
        stack_bytes=_first_int(_STACK_RE, verbose_output),
        spill_store_bytes=_first_int(_SPILL_STORE_RE, verbose_output),
        spill_load_bytes=_first_int(_SPILL_LOAD_RE, verbose_output),
        cubin_path=cubin_path,
        verbose_output=verbose_output,
    )


def assemble_ptx(
    ptx_source: str,
    *,
    target_sm: str = "sm_86",
    output_dir: Path | None = None,
    ptxas: str = "ptxas",
) -> PtxasReport:
    """Assemble generated PTX and return measured ptxas resources."""

    executable = shutil.which(ptxas)
    if executable is None:
        raise CudaRuntimeUnavailable(f"{ptxas} is not available on PATH")

    root = output_dir or Path(tempfile.mkdtemp(prefix="mhrn-ptxas-"))
    root.mkdir(parents=True, exist_ok=True)
    ptx_path = root / "pan_gate_kernel.ptx"
    cubin_path = root / "pan_gate_kernel.cubin"
    ptx_path.write_text(ptx_source, encoding="utf-8")

    process = subprocess.run(
        [
            executable,
            "--verbose",
            f"--gpu-name={target_sm}",
            str(ptx_path),
            "--output-file",
            str(cubin_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    verbose = "\n".join(part for part in (process.stdout, process.stderr) if part)
    if process.returncode != 0:
        raise CudaDriverError(
            "ptxas rejected generated PTX " f"(exit={process.returncode}):\n{verbose}"
        )
    return parse_ptxas_verbose(
        verbose,
        target_sm=target_sm,
        cubin_path=cubin_path,
    )
