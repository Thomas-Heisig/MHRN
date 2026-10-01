"""Fail-closed Wave-5B readiness projection for PAN CPU/CUDA parity.

The preflight can become ready without CUDA execution. Execution remains blocked
until the PAN semantic contract is frozen, physical FE-3 acceptance is reviewed,
and an explicit source-bound authorization record exists.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import cast

from src.homeostasis.pan_contract import PAN_CONTRACT_ID, PAN_CONTRACT_STATUS
from src.homeostasis.pan_parity_contract import (
    PAN_PARITY_CONTRACT_ID,
    PAN_PARITY_CONTRACT_STATUS,
    pan_parity_contract_check,
)
from src.verification.frozen_environment import load_manifest_artifact

PAN_WAVE5B_PREFLIGHT_ID = "mhrn-pan-wave5b-preflight-v1"
DEFAULT_PREFLIGHT_PATH = Path(
    "research/verification/pan/PAN_WAVE5B_PREFLIGHT_V1.json"
)
DEFAULT_AUTHORIZATION_PATH = Path(
    "research/verification/pan/PAN_WAVE5B_AUTHORIZATION.json"
)


@dataclass(frozen=True, slots=True)
class PanWave5BReadiness:
    """Non-evidentiary readiness state for the prospective Wave-5B run."""

    preflight_ready: bool
    manifest_sha256: str | None
    contract_id: str
    contract_status: str
    contract_frozen: bool
    parity_contract_id: str
    parity_contract_status: str
    physical_fe3_accepted: bool
    hardware_artifact: str | None
    gpu_identity: str | None
    execution_authorized: bool
    ready_for_execution: bool
    blockers: tuple[str, ...]
    next_gate: str

    def to_mapping(self) -> dict[str, object]:
        payload = asdict(self)
        payload["blockers"] = list(self.blockers)
        return {
            "classification": "PAN_WAVE5B_PREFLIGHT",
            "scientific_evidence": False,
            "integration_claimed": False,
            "preflight_id": PAN_WAVE5B_PREFLIGHT_ID,
            **payload,
        }


def _canonical_digest(payload: dict[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def load_pan_wave5b_preflight(path: Path) -> tuple[dict[str, object], str]:
    """Validate the static non-executing Wave-5B preflight manifest."""

    raw: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("PAN Wave-5B preflight must be a JSON object")
    payload = cast(dict[str, object], raw)
    if payload.get("artifact_type") != "MHRN_PAN_WAVE5B_PREFLIGHT":
        raise ValueError("unexpected PAN Wave-5B artifact_type")
    if payload.get("preflight_id") != PAN_WAVE5B_PREFLIGHT_ID:
        raise ValueError("unexpected PAN Wave-5B preflight_id")
    if payload.get("scientific_evidence") is not False:
        raise ValueError("PAN Wave-5B preflight must remain non-evidentiary")
    if payload.get("execution_authorized") is not False:
        raise ValueError("preflight manifest may not authorize execution")
    if payload.get("integration_claimed") is not False:
        raise ValueError("preflight manifest may not claim integration")

    contract = payload.get("contract")
    parity = payload.get("parity")
    fe3 = payload.get("fe3_manifest")
    hardware = payload.get("required_hardware")
    if not all(isinstance(item, dict) for item in (contract, parity, fe3, hardware)):
        raise ValueError("PAN Wave-5B manifest sections must be objects")

    contract_map = cast(dict[str, object], contract)
    parity_map = cast(dict[str, object], parity)
    if contract_map.get("id") != PAN_CONTRACT_ID:
        raise ValueError("PAN semantic contract id mismatch")
    if contract_map.get("required_status_for_execution") != "FROZEN":
        raise ValueError("Wave-5B must require a frozen PAN semantic contract")
    if parity_map.get("id") != PAN_PARITY_CONTRACT_ID:
        raise ValueError("PAN parity contract id mismatch")

    d2 = parity_map.get("d2")
    d3c = parity_map.get("d3c")
    if not isinstance(d2, dict) or not isinstance(d3c, dict):
        raise ValueError("PAN parity D2/D3c sections are required")
    tolerance = d2.get("abs_tolerance")
    if (
        isinstance(tolerance, bool)
        or not isinstance(tolerance, (int, float))
        or float(tolerance) <= 0.0
    ):
        raise ValueError("PAN parity tolerance must be positive")
    if d2.get("fail_closed_nonfinite") is not True:
        raise ValueError("PAN parity must fail closed on non-finite state")
    if d3c.get("required") is not True or d3c.get("exact_trajectory") is not True:
        raise ValueError("Wave-5B preflight requires exact D3c trajectory parity")

    return payload, _canonical_digest(payload)


def _latest_hardware_report(
    repo_root: Path,
) -> tuple[dict[str, object] | None, Path | None]:
    reports = sorted(
        (repo_root / "docs" / "canonical").glob("HARDWARE_ACCEPTANCE_*.json")
    )
    if not reports:
        return None, None
    latest = reports[-1]
    raw: object = json.loads(latest.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("hardware acceptance artifact must be an object")
    return cast(dict[str, object], raw), latest


def _hardware_is_accepted(
    report: dict[str, object] | None,
    *,
    required_gpu: str,
) -> tuple[bool, str | None]:
    if report is None:
        return False, None
    raw_identity = report.get("gpu_identity")
    identity = raw_identity if isinstance(raw_identity, str) else None
    accepted = (
        report.get("classification") == "CUDA_HARDWARE_ACCEPTANCE_REPORT"
        and report.get("scientific_evidence") is False
        and report.get("passed") is True
        and report.get("full_fe3_accepted") is True
        and identity is not None
        and required_gpu.lower() in identity.lower()
    )
    return accepted, identity


def _authorization_is_valid(
    path: Path,
    *,
    preflight_manifest_sha256: str,
) -> bool:
    if not path.exists():
        return False
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return False
    record = cast(dict[str, object], raw)
    reviewer = record.get("authorized_by")
    return (
        record.get("artifact_type") == "MHRN_PAN_WAVE5B_AUTHORIZATION"
        and record.get("preflight_id") == PAN_WAVE5B_PREFLIGHT_ID
        and record.get("preflight_manifest_sha256") == preflight_manifest_sha256
        and record.get("execution_authorized") is True
        and isinstance(reviewer, str)
        and bool(reviewer.strip())
    )


def _next_gate(
    *,
    contract_frozen: bool,
    physical_fe3_accepted: bool,
    execution_authorized: bool,
) -> str:
    if not contract_frozen and not physical_fe3_accepted:
        return "PAN_CONTRACT_FREEZE_REVIEW_AND_PHYSICAL_FE3_HARDWARE_ACCEPTANCE"
    if not contract_frozen:
        return "PAN_CONTRACT_FREEZE_REVIEW"
    if not physical_fe3_accepted:
        return "PHYSICAL_FE3_HARDWARE_ACCEPTANCE"
    if not execution_authorized:
        return "PAN_WAVE5B_EXECUTION_AUTHORIZATION"
    return "PAN_CPU_CUDA_PARITY_EXECUTION"


def evaluate_pan_wave5b_readiness(repo_root: Path) -> PanWave5BReadiness:
    """Project Wave-5B readiness without executing a backend."""

    manifest_path = repo_root / DEFAULT_PREFLIGHT_PATH
    try:
        manifest, manifest_digest = load_pan_wave5b_preflight(manifest_path)
        if not pan_parity_contract_check():
            raise ValueError("PAN parity contract self-check failed")

        fe3_spec = cast(dict[str, object], manifest["fe3_manifest"])
        fe3_path = repo_root / str(fe3_spec["path"])
        fe3 = load_manifest_artifact(fe3_path)
        fe3_valid = fe3.manifest_sha256 == str(fe3_spec["manifest_sha256"])

        hardware_spec = cast(dict[str, object], manifest["required_hardware"])
        required_gpu = str(hardware_spec["gpu_identity_contains"])
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return PanWave5BReadiness(
            preflight_ready=False,
            manifest_sha256=None,
            contract_id=PAN_CONTRACT_ID,
            contract_status=PAN_CONTRACT_STATUS,
            contract_frozen=False,
            parity_contract_id=PAN_PARITY_CONTRACT_ID,
            parity_contract_status=PAN_PARITY_CONTRACT_STATUS,
            physical_fe3_accepted=False,
            hardware_artifact=None,
            gpu_identity=None,
            execution_authorized=False,
            ready_for_execution=False,
            blockers=("PAN_WAVE5B_PREFLIGHT_INVALID",),
            next_gate="REPAIR_PAN_WAVE5B_PREFLIGHT",
        )

    report: dict[str, object] | None = None
    report_path: Path | None = None
    try:
        report, report_path = _latest_hardware_report(repo_root)
        hardware_accepted, gpu_identity = _hardware_is_accepted(
            report, required_gpu=required_gpu
        )
    except (OSError, ValueError, json.JSONDecodeError):
        hardware_accepted, gpu_identity = False, None

    contract_frozen = PAN_CONTRACT_STATUS == "FROZEN"
    authorization_path = repo_root / str(
        manifest.get("authorization_artifact", DEFAULT_AUTHORIZATION_PATH)
    )
    try:
        execution_authorized = _authorization_is_valid(
            authorization_path,
            preflight_manifest_sha256=manifest_digest,
        )
    except (OSError, ValueError, json.JSONDecodeError):
        execution_authorized = False

    blockers: list[str] = []
    if not fe3_valid:
        blockers.append("FE3_MANIFEST_DIGEST_MISMATCH")
    if not contract_frozen:
        blockers.append("PAN_CONTRACT_NOT_FROZEN")
    if not hardware_accepted:
        blockers.append("PHYSICAL_FE3_HARDWARE_NOT_ACCEPTED")
    if not execution_authorized:
        blockers.append("PAN_WAVE5B_EXECUTION_NOT_AUTHORIZED")

    preflight_ready = fe3_valid
    ready_for_execution = (
        preflight_ready
        and contract_frozen
        and hardware_accepted
        and execution_authorized
    )
    return PanWave5BReadiness(
        preflight_ready=preflight_ready,
        manifest_sha256=manifest_digest,
        contract_id=PAN_CONTRACT_ID,
        contract_status=PAN_CONTRACT_STATUS,
        contract_frozen=contract_frozen,
        parity_contract_id=PAN_PARITY_CONTRACT_ID,
        parity_contract_status=PAN_PARITY_CONTRACT_STATUS,
        physical_fe3_accepted=hardware_accepted,
        hardware_artifact=(
            str(report_path.relative_to(repo_root)) if report_path is not None else None
        ),
        gpu_identity=gpu_identity,
        execution_authorized=execution_authorized,
        ready_for_execution=ready_for_execution,
        blockers=tuple(blockers),
        next_gate=_next_gate(
            contract_frozen=contract_frozen,
            physical_fe3_accepted=hardware_accepted,
            execution_authorized=execution_authorized,
        ),
    )


__all__ = [
    "DEFAULT_AUTHORIZATION_PATH",
    "DEFAULT_PREFLIGHT_PATH",
    "PAN_WAVE5B_PREFLIGHT_ID",
    "PanWave5BReadiness",
    "evaluate_pan_wave5b_readiness",
    "load_pan_wave5b_preflight",
]
