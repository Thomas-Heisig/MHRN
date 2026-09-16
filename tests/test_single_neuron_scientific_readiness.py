"""Regression contract for scoped Stage-0 scientific readiness.

This test deliberately distinguishes research readiness from overall scientific
maturity. Human EVID promotion and independent authorship replication remain
separate gates.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "research/generated/verification/single_neuron_scientific_readiness.json"
DATA = ROOT / "research/experiments/EXP-STAGE0-20260916-MODEL-CONFORMANCE-V2/DATA/confirmatory_result.json"
PREREG = ROOT / "research/preregistrations/operational/single_neuron_conformance_v2.json"


def _load(path: Path) -> dict[str, object]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    return raw


def test_stage0_scoped_research_readiness_is_fully_proven() -> None:
    readiness = _load(READINESS)
    proofs = readiness["proofs"]
    assert isinstance(proofs, dict)
    assert readiness["status"] == "passed"
    assert readiness["research_readiness_score"] == 1.0
    assert readiness["research_readiness_percent"] == 100
    assert proofs and all(value is True for value in proofs.values())


def test_confirmatory_data_satisfy_both_selectable_models() -> None:
    data = _load(DATA)
    assert data["status"] == "passed"
    assert data["diagnostic_seed_overlap"] is False
    assert data["primary_success"] is True
    assert data["all_declared_hypotheses_pass"] is True
    results = data["results"]
    assert isinstance(results, dict)
    assert results["H-EVAL-006-A"]["supported_by_protocol"] is True
    assert results["H-EVAL-006-B"]["supported_by_protocol"] is True
    assert results["H-EVAL-006-C"]["supported_by_protocol"] is True


def test_readiness_does_not_forge_maturity_gates() -> None:
    readiness = _load(READINESS)
    boundary = readiness["maturity_boundary"]
    assert isinstance(boundary, dict)
    assert boundary["human_reviewed_evid_complete"] is False
    assert boundary["independent_authorship_replication_complete"] is False


def test_preregistration_keeps_izhikevich_default_and_lif_optional() -> None:
    prereg = _load(PREREG)
    axis = prereg["model_axis"]
    assert isinstance(axis, dict)
    assert axis["default_model"] == "izhikevich-2003"
    assert axis["optional_models"] == ["lif-current-v1"]
    validation = prereg["confirmatory_validation"]
    assert isinstance(validation, dict)
    assert validation["seeds"] == [21001, 21002, 21003]
    assert validation["seed_overlap_with_diagnostic"] is False
