"""Wave-5B PAN parity/preflight tests without CUDA execution."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from src.homeostasis.pan_contract import initialize_pan_state_mapping
from src.homeostasis.pan_parity_contract import (
    PAN_PARITY_CONTRACT_STATUS,
    PANParityThresholds,
    compare_pan_state_mappings,
    pan_parity_contract_check,
)
from src.homeostasis.pan_wave5b_preflight import (
    DEFAULT_PREFLIGHT_PATH,
    evaluate_pan_wave5b_readiness,
)

ROOT = Path(__file__).resolve().parents[1]
FE3_SOURCE = (
    ROOT
    / "research"
    / "verification"
    / "frozen_environment"
    / "FE3_DETERMINISTIC_TARGET_V1.json"
)
PREFLIGHT_SOURCE = ROOT / DEFAULT_PREFLIGHT_PATH


def _pan_state(neuron_id: int = 0, dimensions: int = 5) -> dict[str, object]:
    state: dict[str, object] = {}
    initialize_pan_state_mapping(
        state,
        neuron_id=neuron_id,
        dimensions=dimensions,
    )
    return state


def _prepare_repo_root(tmp_path: Path) -> Path:
    fe3_target = (
        tmp_path
        / "research"
        / "verification"
        / "frozen_environment"
        / "FE3_DETERMINISTIC_TARGET_V1.json"
    )
    fe3_target.parent.mkdir(parents=True)
    fe3_target.write_bytes(FE3_SOURCE.read_bytes())

    preflight_target = tmp_path / DEFAULT_PREFLIGHT_PATH
    preflight_target.parent.mkdir(parents=True)
    preflight_target.write_bytes(PREFLIGHT_SOURCE.read_bytes())

    (tmp_path / "docs" / "canonical").mkdir(parents=True)
    return tmp_path


def test_pan_parity_contract_is_pure_and_fail_closed() -> None:
    assert PAN_PARITY_CONTRACT_STATUS == "DRAFT_PREFLIGHT"
    assert pan_parity_contract_check()

    reference = _pan_state()
    candidate = deepcopy(reference)
    result = compare_pan_state_mappings(
        [reference],
        [candidate],
        dimensions=5,
    )
    assert result.passed
    assert result.max_abs_error == 0.0
    assert result.to_mapping()["scientific_evidence"] is False

    candidate["pan_energy"] = 1.0 - 2e-12
    failed = compare_pan_state_mappings(
        [reference],
        [candidate],
        dimensions=5,
        thresholds=PANParityThresholds(abs_tolerance=1e-12),
    )
    assert not failed.passed

    candidate["pan_energy"] = float("nan")
    with pytest.raises(ValueError, match="pan_energy must be finite"):
        compare_pan_state_mappings(
            [reference],
            [candidate],
            dimensions=5,
        )


def test_wave5b_preflight_is_ready_but_execution_is_blocked_without_hardware(
    tmp_path: Path,
) -> None:
    repo_root = _prepare_repo_root(tmp_path)
    status = evaluate_pan_wave5b_readiness(repo_root)

    assert status.preflight_ready is True
    assert status.contract_frozen is False
    assert status.physical_fe3_accepted is False
    assert status.execution_authorized is False
    assert status.ready_for_execution is False
    assert "PAN_CONTRACT_NOT_FROZEN" in status.blockers
    assert "PHYSICAL_FE3_HARDWARE_NOT_ACCEPTED" in status.blockers
    assert status.next_gate == (
        "PAN_CONTRACT_FREEZE_REVIEW_AND_PHYSICAL_FE3_HARDWARE_ACCEPTANCE"
    )


def test_reviewed_rtx_fe3_artifact_does_not_bypass_contract_freeze(
    tmp_path: Path,
) -> None:
    repo_root = _prepare_repo_root(tmp_path)
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
    report_path = repo_root / "docs" / "canonical" / "HARDWARE_ACCEPTANCE_2026-10-01.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")

    status = evaluate_pan_wave5b_readiness(repo_root)

    assert status.preflight_ready is True
    assert status.physical_fe3_accepted is True
    assert status.contract_frozen is False
    assert status.ready_for_execution is False
    assert status.next_gate == "PAN_CONTRACT_FREEZE_REVIEW"


def test_preflight_manifest_corruption_fails_closed(tmp_path: Path) -> None:
    repo_root = _prepare_repo_root(tmp_path)
    preflight_path = repo_root / DEFAULT_PREFLIGHT_PATH
    payload = json.loads(preflight_path.read_text(encoding="utf-8"))
    payload["execution_authorized"] = True
    preflight_path.write_text(json.dumps(payload), encoding="utf-8")

    status = evaluate_pan_wave5b_readiness(repo_root)

    assert status.preflight_ready is False
    assert status.ready_for_execution is False
    assert status.blockers == ("PAN_WAVE5B_PREFLIGHT_INVALID",)
