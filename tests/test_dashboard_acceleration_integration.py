"""Tests for the canonical CUDA/FE-3 dashboard projection."""

from __future__ import annotations

import json
from pathlib import Path

from src.dashboard.integration_status import IntegrationStatusBuilder

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "research"
    / "verification"
    / "frozen_environment"
    / "FE3_DETERMINISTIC_TARGET_V1.json"
)
PREFLIGHT = ROOT / "research" / "verification" / "pan" / "PAN_WAVE5B_PREFLIGHT_V1.json"


def _copy_preflight_inputs(repo_root: Path) -> None:
    manifest_target = (
        repo_root
        / "research"
        / "verification"
        / "frozen_environment"
        / "FE3_DETERMINISTIC_TARGET_V1.json"
    )
    manifest_target.parent.mkdir(parents=True, exist_ok=True)
    manifest_target.write_bytes(MANIFEST.read_bytes())

    preflight_target = (
        repo_root / "research" / "verification" / "pan" / "PAN_WAVE5B_PREFLIGHT_V1.json"
    )
    preflight_target.parent.mkdir(parents=True, exist_ok=True)
    preflight_target.write_bytes(PREFLIGHT.read_bytes())


def _builder(repo_root: Path) -> IntegrationStatusBuilder:
    return IntegrationStatusBuilder(None, repo_root=repo_root)


def test_acceleration_status_exposes_canonical_backend_and_manifest() -> None:
    status = _builder(ROOT)._build_acceleration_status()

    assert status["classification"] == "MHRN_ACCELERATION_INTEGRATION_STATUS"
    assert status["scientific_evidence"] is False
    assert status["software_path_closed"] is True
    waves = {item["id"]: item for item in status["waves"]}
    assert waves["wave5"]["status"] == "preflight_ready"

    pan = status["pan_wave5b_preflight"]
    assert isinstance(pan, dict)
    assert pan["preflight_ready"] is True
    assert pan["contract_frozen"] is False
    assert pan["ready_for_execution"] is False

    backend = status["backend"]
    assert isinstance(backend, dict)
    assert backend["status"] == "integrated"
    assert backend["contract_ok"] is True
    capabilities = backend["capabilities"]
    assert isinstance(capabilities, dict)
    assert capabilities["supports_live_external_input"] is True
    assert capabilities["supports_pan_hyperstate"] is False

    manifest = status["fe3_manifest"]
    assert isinstance(manifest, dict)
    assert manifest["valid"] is True
    assert (
        manifest["manifest_sha256"]
        == "e0356fcfafb5b9af37b080754ba00877f60c662243a262a3bc348e310c092e35"
    )


def test_hardware_status_is_derived_from_reviewed_artifact(tmp_path: Path) -> None:
    _copy_preflight_inputs(tmp_path)

    canonical = tmp_path / "docs" / "canonical"
    canonical.mkdir(parents=True)
    report = {
        "classification": "CUDA_HARDWARE_ACCEPTANCE_REPORT",
        "scientific_evidence": False,
        "gpu_identity": "NVIDIA GeForce RTX 3060, driver test",
        "wave4_physical": "PASS",
        "builder_d3c_bridge": "PASS",
        "frozen_environment_fe3": "PASS",
        "full_fe3_accepted": True,
        "passed": True,
    }
    (canonical / "HARDWARE_ACCEPTANCE_2026-09-30.json").write_text(
        json.dumps(report), encoding="utf-8"
    )

    status = _builder(tmp_path)._build_acceleration_status()
    hardware = status["hardware_acceptance"]
    assert isinstance(hardware, dict)
    assert hardware["status"] == "passed"
    assert hardware["accepted"] is True
    assert status["physical_hardware_accepted"] is True
    assert status["next_gate"] == "PAN_CONTRACT_FREEZE_REVIEW"


def test_missing_hardware_artifact_stays_pending(tmp_path: Path) -> None:
    _copy_preflight_inputs(tmp_path)
    (tmp_path / "docs" / "canonical").mkdir(parents=True)

    status = _builder(tmp_path)._build_acceleration_status()
    hardware = status["hardware_acceptance"]
    assert isinstance(hardware, dict)
    assert hardware["status"] == "pending"
    assert hardware["accepted"] is False
    assert status["physical_hardware_accepted"] is False
    assert status["next_gate"] == (
        "PAN_CONTRACT_FREEZE_REVIEW_AND_PHYSICAL_FE3_HARDWARE_ACCEPTANCE"
    )
