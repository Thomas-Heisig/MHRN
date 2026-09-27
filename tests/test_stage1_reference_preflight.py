"""Historical pre-freeze provenance tests for Stage-1 R1 reference replication."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREREG=ROOT/"research"/"preregistrations"/"PREREG-S1-TOPO-REFERENCE-R1.json"
FREEZE=ROOT/"research"/"preregistrations"/"PREREG-S1-TOPO-REFERENCE-R1.freeze.json"
DEVIATION=ROOT/"research"/"decisions"/"2026-09-27_stage1_reference_r1_prefreeze_deviation.json"

def test_r1_freeze_and_abort_provenance_coexist()->None:
    p=json.loads(PREREG.read_text(encoding="utf-8")); f=json.loads(FREEZE.read_text(encoding="utf-8")); d=json.loads(DEVIATION.read_text(encoding="utf-8"))
    assert p["execution_authorized"] is False
    assert f["reference_data_created"] is False
    assert f["replication_credit_awarded"] is False
    assert d["status"]=="FROZEN_ABORTED_BEFORE_REFERENCE_DATA"
    assert d["reference_data_created"] is False

def test_r1_parity_gates_were_hash_bound_before_abort()->None:
    f=json.loads(FREEZE.read_text(encoding="utf-8"))
    assert f["integrator_parity"]["pass"] is True
    assert f["reset_parity"]["pass"] is True
    assert f["synapse_delay_parity"]["pass"] is True
    assert f["mechanism_audit"]["pass"] is True
