"""Static contract tests for the physical CUDA acceptance runner."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cuda_hardware_runner_exposes_canonical_fe3_and_builder_bridge() -> None:
    source = (ROOT / "scripts" / "run_cuda_hardware_acceptance.py").read_text(
        encoding="utf-8"
    )
    assert '"--include-fe3"' in source
    assert '"BUILDER_D3C_BRIDGE"' in source
    assert '"FROZEN_ENVIRONMENT_FE3_CPU_CUDA_D3C"' in source
    assert '"full_fe3_accepted": full_fe3_accepted' in source
    assert "scripts/run_fe_acceptance.py" in source
    assert "test_full_pan_builder_hardware_d3" in source
    assert "FE3_DETERMINISTIC_TARGET_V1.json" in source
    assert "HARDWARE_ACCEPTANCE_" in source


def test_frozen_environment_cli_executes_cuda_only_when_explicitly_enabled() -> None:
    source = (ROOT / "scripts" / "run_fe_acceptance.py").read_text(encoding="utf-8")
    assert '"--require-cuda"' in source
    assert "MHRN_TEST_CUDA_HARDWARE" in source
    assert "run_fe3_backend_parity" in source
    assert "CPUReferenceBackend" in source
    assert "CUDABackend" in source
    assert "REQUIRES_MHRN_TEST_CUDA_HARDWARE" in source
