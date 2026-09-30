"""Canonical FE-3 live-backend bridge tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from src.acceleration.cuda import CUDABackend
from src.acceleration.cuda.recurrent import CPUReferenceBackend
from src.embodiment.deterministic import DeterministicTargetEnvironment
from src.runtime.backend import LiveInputExecutionBackend
from src.verification.frozen_environment import (
    deterministic_target_currents,
    load_manifest_artifact,
    run_fe3_backend_parity,
    run_fe3_backend_trace,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "research"
    / "verification"
    / "frozen_environment"
    / "FE3_DETERMINISTIC_TARGET_V1.json"
)
MANIFEST_SHA256 = "e0356fcfafb5b9af37b080754ba00877f60c662243a262a3bc348e310c092e35"


def _world() -> DeterministicTargetEnvironment:
    return DeterministicTargetEnvironment(target=2)


def test_fe3_manifest_is_versioned_and_self_verifying() -> None:
    manifest = load_manifest_artifact(MANIFEST)
    assert manifest.manifest_sha256 == MANIFEST_SHA256
    assert manifest.environment_id == "deterministic-target-v1"
    assert manifest.sensor_schedule == (0, 1, 2)


def test_deterministic_target_sensor_encoder_covers_both_directions_and_hold() -> None:
    assert deterministic_target_currents({"position": 0, "target": 2}) == (400.0, 0.0)
    assert deterministic_target_currents({"position": 3, "target": 2}) == (0.0, 400.0)
    assert deterministic_target_currents({"position": 2, "target": 2}) == (0.0, 0.0)


def test_cpu_reference_backend_declares_live_external_input_contract() -> None:
    backend = CPUReferenceBackend()
    assert isinstance(backend, LiveInputExecutionBackend)
    assert backend.capabilities().supports_live_external_input is True


def test_fe3_cpu_self_backend_bridge_is_exact_and_causal() -> None:
    manifest = load_manifest_artifact(MANIFEST)
    result = run_fe3_backend_parity(
        manifest,
        _world,
        CPUReferenceBackend,
        CPUReferenceBackend,
    )
    assert result.passed, result.to_mapping()
    assert result.details["live_input_fingerprint_exact"] is True
    assert result.details["trajectory_sha256_exact"] is True

    run = run_fe3_backend_trace(manifest, _world, CPUReferenceBackend)
    assert len(run.trace.records) == 3
    assert all(record.boundary_frame_hashes for record in run.trace.records)


@pytest.mark.skipif(
    os.environ.get("MHRN_TEST_CUDA_HARDWARE") != "1",
    reason="opt-in physical CUDA FE-3 acceptance",
)
def test_physical_fe3_cpu_cuda_d3c_exact() -> None:
    manifest = load_manifest_artifact(MANIFEST)
    result = run_fe3_backend_parity(
        manifest,
        _world,
        CPUReferenceBackend,
        CUDABackend,
    )
    assert result.passed, result.to_mapping()
    assert result.details["live_input_fingerprint_exact"] is True
    assert result.details["trajectory_sha256_exact"] is True
    # Wave-3 provenance deliberately includes backend identity.
    assert result.details["execution_fingerprints_equal"] is False
