#!/usr/bin/env python3
"""Freeze Stage-1 topology reference protocol after all executable pre-freeze gates pass.

This script cannot authorize the reference evaluation. It only creates a provenance
freeze record and changes the preregistration status to FROZEN_BEFORE_REFERENCE_RUNNER.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-REFERENCE-R1.json"
FREEZE = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-REFERENCE-R1.freeze.json"
AUDIT = ROOT / "research" / "audits" / "STAGE1_TOPOLOGY_REFERENCE_MECHANISM_AUDIT_20260927.json"
PARITY = ROOT / "research" / "calibrations" / "CAL-S1-TOPO-REFERENCE-INTEGRATOR-R1" / "result.json"
RESET = ROOT / "research" / "calibrations" / "CAL-S1-TOPO-REFERENCE-RESET-R1" / "result.json"
SYNAPSE = ROOT / "research" / "calibrations" / "CAL-S1-TOPO-REFERENCE-SYNAPSE-R1" / "result.json"
RUNNER_PROTOCOL = ROOT / "reference" / "stage1_topology_brian2" / "reference_protocol.json"
RUNNER_SOURCE = ROOT / "reference" / "stage1_topology_brian2" / "runner.py"
VERIFIER_SOURCE = ROOT / "scripts" / "verify_stage1_topology_reference_r1.py"
TRANSLATION = ROOT / "reference" / "stage1_topology_brian2" / "TRANSLATION.md"
INDEPENDENCE = ROOT / "scripts" / "check_stage1_reference_independence.py"
SEED_FRESHNESS = ROOT / "scripts" / "check_stage1_reference_seed_freshness.py"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_gate(script: Path) -> None:
    subprocess.run(
        ["python", str(script.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
    )


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> int:
    if FREEZE.exists():
        raise FileExistsError(f"Freeze record already exists: {FREEZE}")
    if git("status", "--porcelain"):
        raise RuntimeError("Reference freeze requires a clean git tree")

    prereg = read_json(PREREG)
    if prereg.get("status") != "DRAFT_PRE_FREEZE_GATES_PENDING":
        raise RuntimeError(
            "Reference preregistration is not in the pre-freeze-gates-pending state"
        )
    if prereg.get("execution_authorized") is not False:
        raise RuntimeError("Reference execution must remain unauthorized before freeze")

    for required in (
        AUDIT,
        PARITY,
        RESET,
        SYNAPSE,
        RUNNER_PROTOCOL,
        RUNNER_SOURCE,
        VERIFIER_SOURCE,
        TRANSLATION,
    ):
        if not required.is_file():
            raise RuntimeError(f"Missing pre-freeze artifact: {required.relative_to(ROOT)}")

    audit = read_json(AUDIT)
    parity = read_json(PARITY)
    reset = read_json(RESET)
    synapse = read_json(SYNAPSE)
    if audit.get("pass") is not True:
        raise RuntimeError("Mechanism audit did not pass")
    if parity.get("pass") is not True:
        raise RuntimeError("Integrator parity did not pass")
    if parity.get("provenance", {}).get("brian2_version") != "2.10.1":
        raise RuntimeError("Integrator parity did not use Brian2 2.10.1")
    multi_tick = parity.get("multi_tick")
    if not isinstance(multi_tick, dict) or multi_tick.get("pass") is not True:
        raise RuntimeError("Multi-tick integrator parity did not pass")
    if multi_tick.get("contains_spike") is not True:
        raise RuntimeError("Multi-tick parity did not exercise a spike")
    if reset.get("pass") is not True:
        raise RuntimeError("Explicit reset parity did not pass")
    if synapse.get("pass") is not True:
        raise RuntimeError("Synapse-delay parity did not pass")

    runner_protocol = read_json(RUNNER_PROTOCOL)
    if runner_protocol.get("seeds") != prereg["evaluation"]["seeds"]:
        raise RuntimeError("Blinded reference protocol seed block differs from preregistration")
    if runner_protocol.get("framework_version") != "2.10.1":
        raise RuntimeError("Blinded reference protocol framework version mismatch")

    # Re-run dynamic gates at the exact freeze commit.
    run_gate(INDEPENDENCE)
    run_gate(SEED_FRESHNESS)

    source_hashes = audit.get("source_sha256")
    if not isinstance(source_hashes, dict) or not source_hashes:
        raise RuntimeError("Mechanism audit is not source-hash bound")
    for rel, expected in source_hashes.items():
        current = sha256(ROOT / rel)
        if current != expected:
            raise RuntimeError(f"Mechanism audit source drift: {rel}")

    prereg_sha_before = sha256(PREREG)
    freeze = {
        "schema_version": 1,
        "preregistration_id": prereg["preregistration_id"],
        "freeze_date": "2026-09-27",
        "freeze_commit": git("rev-parse", "HEAD"),
        "preregistration_sha256_before_status_update": prereg_sha_before,
        "mechanism_audit": {
            "path": str(AUDIT.relative_to(ROOT)),
            "sha256": sha256(AUDIT),
            "pass": True,
        },
        "integrator_parity": {
            "path": str(PARITY.relative_to(ROOT)),
            "sha256": sha256(PARITY),
            "pass": True,
            "single_tick_pass": all(
                bool(case.get("pass")) for case in parity.get("cases", [])
            ),
            "multi_tick_pass": bool(parity["multi_tick"]["pass"]),
            "multi_tick_contains_spike": bool(parity["multi_tick"]["contains_spike"]),
            "tolerance_abs": parity["tolerance_abs"],
            "brian2_version": parity["provenance"]["brian2_version"],
        },
        "reset_parity": {
            "path": str(RESET.relative_to(ROOT)),
            "sha256": sha256(RESET),
            "pass": True,
            "tolerance_abs": reset["tolerance_abs"],
        },
        "synapse_delay_parity": {
            "path": str(SYNAPSE.relative_to(ROOT)),
            "sha256": sha256(SYNAPSE),
            "pass": True,
            "weight": synapse["weight"],
            "delay_ticks": synapse["delay_ticks"],
            "tolerance_abs": synapse["tolerance_abs"],
        },
        "translation_specification": {
            "path": str(TRANSLATION.relative_to(ROOT)),
            "sha256": sha256(TRANSLATION),
        },
        "sanitized_runner_protocol": {
            "path": str(RUNNER_PROTOCOL.relative_to(ROOT)),
            "sha256": sha256(RUNNER_PROTOCOL),
        },
        "reference_runner": {
            "path": str(RUNNER_SOURCE.relative_to(ROOT)),
            "sha256": sha256(RUNNER_SOURCE),
            "execution_authorized": False,
        },
        "reference_verifier": {
            "path": str(VERIFIER_SOURCE.relative_to(ROOT)),
            "sha256": sha256(VERIFIER_SOURCE),
        },
        "evaluation_seeds": prereg["evaluation"]["seeds"],
        "canonical_target_digest": hashlib.sha256(
            json.dumps(
                prereg["canonical_targets"],
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest(),
        "decision_rule_digest": hashlib.sha256(
            json.dumps(
                prereg["decision_rule"],
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest(),
        "execution_authorized": False,
        "reference_data_created": False,
        "scientific_evidence": False,
        "replication_credit_awarded": False,
        "note": (
            "This record freezes the scientific comparison contract only. "
            "The full Brian2 reference runner must still be implemented, independently "
            "scanned, hash-bound and separately authorized before any evaluation DATA."
        ),
    }
    FREEZE.write_text(
        json.dumps(freeze, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    prereg["status"] = "FROZEN_BEFORE_REFERENCE_RUNNER"
    prereg["execution_authorized"] = False
    prereg["freeze_authorization"] = {
        "allowed": True,
        "rule": (
            "All pre-freeze gates passed and are bound into the freeze record. "
            "Reference evaluation remains unauthorized until the separate runner "
            "implementation is independently scanned, hash-bound and explicitly authorized."
        ),
        "reference_runner_implementation_allowed": True,
        "reference_runner_execution_allowed": False,
    }
    prereg["freeze_record"] = str(FREEZE.relative_to(ROOT))
    prereg["freeze_semantics"] = (
        "Scientific translation, targets, equivalence bounds, endpoints and decision "
        "criteria are frozen. Reference evaluation remains forbidden until a separately "
        "reviewed runner implementation is hash-bound and explicitly authorized."
    )
    PREREG.write_text(
        json.dumps(prereg, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "FROZEN_CONTRACT_ONLY", "execution_authorized": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
