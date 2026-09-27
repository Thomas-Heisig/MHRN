"""Contract tests for corrected Stage-1 Brian2 reference replication R2."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-REFERENCE-R2.json"
Q = ROOT / "reference" / "stage1_topology_brian2" / "reference_protocol_r2.json"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def test_r2_pre_data_partial_only():
    p = load(P)
    assert p["status"] in {
        "DRAFT_PRE_FREEZE_GATES_PENDING",
        "FROZEN_BEFORE_REFERENCE_EXECUTION_AUTHORIZATION",
    }
    assert p["execution_authorized"] is False
    assert p["replication_credit_target"] == "partial_only"
    assert p["maturity_target_if_successful"]["stage1_maturity"] == "85% -> 92.5%"
    assert p["supersession"]["reference_data_created_under_r1"] is False


def test_r2_mapping_and_bounds():
    p = load(P)
    assert (
        "sum(value_i/max(size_i-1,1))"
        in p["translation_contract"]["topology_generation"]["coordinate_order"]
    )
    assert p["canonical_targets"]["frozen_bounds"]["3d_to_5d"] == [-1.5, -0.5]
    assert p["prefreeze_requirements"]["topology_mapping_parity"]["required"] is True


def test_r2_protocol_blinded_and_fresh():
    p = load(P)
    q = load(Q)
    s = json.dumps(q, sort_keys=True).lower()
    assert q["framework"] == "Brian2" and q["framework_version"] == "2.10.1"
    assert q["seeds"] == p["evaluation"]["seeds"]
    assert len(q["seeds"]) == 20 and min(q["seeds"]) > 820_000_000
    for token in (
        "canonical_targets",
        "frozen_bounds",
        "evid-2026-19",
        "equivalence_bounds",
    ):
        assert token not in s


def test_r2_authorization_requires_human_record():
    p = load(P)
    assert (
        p["execution_authorization_requirements"]["automatic_authorization_forbidden"]
        is True
    )
    assert any(
        "human execution-authorization record" in x
        for x in p["execution_authorization_requirements"]["all_required"]
    )
