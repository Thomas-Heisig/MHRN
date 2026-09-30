"""Static contract tests for the physical CUDA acceptance runner."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cuda_hardware_runner_exposes_fe3_bridge_without_claiming_full_fe3() -> None:
    source = (ROOT / "scripts" / "run_cuda_hardware_acceptance.py").read_text(
        encoding="utf-8"
    )
    assert '"--include-fe3"' in source
    assert '"BUILDER_D3C_BRIDGE"' in source
    assert '"PENDING_LIVE_BACKEND_ADAPTER"' in source
    assert '"full_fe3_accepted": False' in source
    assert "test_full_pan_builder_hardware_d3" in source


def test_frozen_environment_cli_still_fails_closed_for_cuda_requirement() -> None:
    source = (ROOT / "scripts" / "run_fe_acceptance.py").read_text(
        encoding="utf-8"
    )
    assert '"--require-cuda"' in source
    assert "PENDING_FROZEN_ENVIRONMENT_LIVE_BACKEND_ADAPTER" in source
    assert "if args.require_cuda:" in source
    assert "passed = False" in source
