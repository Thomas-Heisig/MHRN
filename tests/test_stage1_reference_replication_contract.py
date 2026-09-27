"""Historical contract tests for the aborted-before-DATA Stage-1 R1 reference protocol."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREREG=ROOT/"research"/"preregistrations"/"PREREG-S1-TOPO-REFERENCE-R1.json"
DEVIATION=ROOT/"research"/"decisions"/"2026-09-27_stage1_reference_r1_prefreeze_deviation.json"
PROTOCOL=ROOT/"reference"/"stage1_topology_brian2"/"reference_protocol.json"

def test_r1_is_preserved_but_may_not_authorize_execution()->None:
    p=json.loads(PREREG.read_text(encoding="utf-8")); d=json.loads(DEVIATION.read_text(encoding="utf-8"))
    assert p["status"]=="FROZEN_BEFORE_REFERENCE_RUNNER"
    assert p["execution_authorized"] is False
    assert d["status"]=="FROZEN_ABORTED_BEFORE_REFERENCE_DATA"
    assert d["reference_data_created"] is False
    assert d["replication_credit_awarded"] is False
    assert d["stage1_maturity_change"]==0
    assert "PREREG-S1-TOPO-REFERENCE-R2" in d["governance_action"][3]

def test_r1_strict_bound_and_blinding_history_are_preserved()->None:
    p=json.loads(PREREG.read_text(encoding="utf-8")); q=json.loads(PROTOCOL.read_text(encoding="utf-8"))
    assert p["canonical_targets"]["frozen_bounds"]["3d_to_5d"]==[-1.5,-0.5]
    s=json.dumps(q,sort_keys=True).lower()
    for token in ("canonical_targets","frozen_bounds","evid-2026-19","equivalence_bounds"):
        assert token not in s
