"""Pre-freeze contract tests for Stage-1 Brian2 reference replication R2."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-REFERENCE-R2.json"


def p():
    return json.loads(P.read_text(encoding="utf-8"))


def test_all_r2_prefreeze_gates_mandatory():
    r = p()["prefreeze_requirements"]
    for g in (
        "integrator_parity",
        "mechanism_audit",
        "runner_independence_scan",
        "seed_freshness",
        "reset_parity",
        "synapse_delay_parity",
        "topology_mapping_parity",
    ):
        assert r[g]["required"] is True


def test_freeze_is_not_execution_authorization():
    v = p()
    assert v["execution_authorized"] is False
    assert v["freeze_authorization"]["reference_runner_execution_allowed"] is False
    assert (
        v["execution_authorization_requirements"]["automatic_authorization_forbidden"]
        is True
    )


def test_runner_verifier_separate():
    i = p()["independence_contract"]
    assert i["runner_source"].endswith("runner_r2.py")
    assert i["verifier_source"].endswith("verify_stage1_topology_reference_r2.py")
    assert i["runner_source"] != i["verifier_source"]


def test_reused_synapse_probe_preserves_calibrated_bytes():
    """Even formatting changes invalidate the strict historical reuse contract."""
    artifact = json.loads(
        (
            ROOT / "research/calibrations/CAL-S1-TOPO-REFERENCE-SYNAPSE-R1/result.json"
        ).read_text(encoding="utf-8")
    )
    source = ROOT / "reference/stage1_topology_brian2/synapse_probe.py"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == (
        artifact["provenance"]["reference_probe_sha256"]
    )
