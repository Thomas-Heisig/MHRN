"""Fail-closed Wave-4 canonical cross-backend parity contract gate.

Hosted CI does not have physical CUDA. This gate verifies that CPU and CUDA
conform to the canonical ExecutionBackend surface, share one canonical
configuration identity, and that the named physical acceptance test is wired
through canonical parity functions rather than Playground helpers.

Physical D1/D2 execution is performed by scripts/run_cuda_hardware_acceptance.py.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path

from src.acceleration.cuda import CUDABackend
from src.acceleration.cuda.recurrent import (
    CPUReferenceBackend,
    recurrent_fixture,
    recurrent_inputs_to_mapping,
)
from src.runtime.backend import ExecutionBackend
from src.verification.parity import config_fingerprint

ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = ROOT / "tests" / "test_cuda_wave4_backend.py"
HARDWARE_TEST = "test_physical_cpu_cuda_cross_backend_d1_d2_parity"


def _hardware_test_source() -> str:
    source = TEST_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(TEST_FILE))
    for node in tree.body:
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == HARDWARE_TEST
        ):
            segment = ast.get_source_segment(source, node)
            if segment is None:
                raise RuntimeError("could not recover hardware acceptance test source")
            return segment
    raise RuntimeError(f"missing named hardware acceptance test: {HARDWARE_TEST}")


def failures() -> list[str]:
    problems: list[str] = []

    cpu: ExecutionBackend = CPUReferenceBackend()
    cuda: ExecutionBackend = CUDABackend()
    config = recurrent_inputs_to_mapping(
        recurrent_fixture(n_neurons=8, ticks=4, model="lif")
    )
    seed = 12345
    cpu.initialize(config, seed)
    cuda.initialize(config, seed)

    cpu_config = cpu.snapshot().payload.get("config")
    cuda_config = cuda.snapshot().payload.get("config")
    if not isinstance(cpu_config, Mapping) or not isinstance(cuda_config, Mapping):
        problems.append("backend snapshots must expose canonical mapping configs")
    elif config_fingerprint(cpu_config) != config_fingerprint(cuda_config):
        problems.append("CPU/CUDA canonical configuration fingerprints differ")

    try:
        test_source = _hardware_test_source()
    except RuntimeError as exc:
        problems.append(str(exc))
        test_source = ""

    required_tokens = (
        "CPUReferenceBackend",
        "CUDABackend",
        "exact_spike_parity",
        "state_vector_parity",
        "MHRN_TEST_CUDA_HARDWARE",
        "tolerance=1.0e-4",
    )
    for token in required_tokens:
        if token not in test_source:
            problems.append(
                "hardware parity acceptance test is missing canonical token: " + token
            )

    if "playground" in test_source.lower():
        problems.append(
            "hardware parity acceptance test must not use Playground parity helpers"
        )

    return problems


def main() -> int:
    problems = failures()
    if problems:
        raise SystemExit(
            "Wave-4 canonical parity contract failed:\n" + "\n".join(problems)
        )
    print("Wave-4 canonical parity contract: PASS")
    print("hardware acceptance test: PRESENT / OPT-IN")
    print("D3 status: NOT_CLAIMED_IN_WAVE4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
