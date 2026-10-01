"""Canonical PAN draft-semantics tests for Wave 5A."""

from __future__ import annotations

import pytest

from src.homeostasis.pan_contract import (
    PAN_CONTRACT_ID,
    PAN_CONTRACT_STATUS,
    PAN_STATE_FIELDS,
    PAN_UPDATE_ORDER,
    PANFormulaParameters,
    initialize_pan_state_mapping,
    pan_contract_check,
    validate_pan_state_mapping,
)
from src.playground.pan.runtime import PANRuntime


def _runtime() -> PANRuntime:
    return PANRuntime(
        n_neurons=2,
        dimensions=10,
        seed=42,
        feedback_gain=1.0,
        health_decay=0.0,
        apoptosis_threshold=0.2,
        closed_loop=True,
        coordinates=[[0.0, 0.5], [1.0, 0.5]],
        degree=[1, 1],
    )


def test_pan_draft_contract_is_backend_neutral_and_self_consistent() -> None:
    assert PAN_CONTRACT_ID == "mhrn-pan-hyperstate-v0.1-draft"
    assert PAN_CONTRACT_STATUS == "DRAFT_NOT_FROZEN"
    assert pan_contract_check()
    assert len(PAN_STATE_FIELDS) == len(set(PAN_STATE_FIELDS))
    assert len(PAN_UPDATE_ORDER) == len(set(PAN_UPDATE_ORDER))
    assert PANFormulaParameters().neuromodulation_period_ticks == 64


def test_pan_state_initializer_matches_current_reference_surface() -> None:
    state: dict[str, object] = {}
    initialize_pan_state_mapping(state, neuron_id=1, dimensions=10)
    assert tuple(state) == PAN_STATE_FIELDS
    validate_pan_state_mapping(state, dimensions=10)
    assert state["pan_health"] == 1.0
    assert state["pan_activity_ema"] == 0.01
    assert state["pan_neuron_id"] == 1
    assert state["pan_x_hd"] == [0.0] * 10


def test_pan_state_validation_fails_closed_on_nonfinite_or_wrong_width() -> None:
    state: dict[str, object] = {}
    initialize_pan_state_mapping(state, neuron_id=0, dimensions=5)
    state["pan_energy"] = float("nan")
    with pytest.raises(ValueError, match="pan_energy must be finite"):
        validate_pan_state_mapping(state, dimensions=5)

    initialize_pan_state_mapping(state, neuron_id=0, dimensions=5)
    state["pan_x_hd"] = [0.0] * 4
    with pytest.raises(ValueError, match="dimension mismatch"):
        validate_pan_state_mapping(state, dimensions=5)


def test_playground_pan_consumes_draft_contract_without_claiming_evidence() -> None:
    runtime = _runtime()
    states: list[dict[str, object]] = [{"v": -65.0}, {"v": -64.0}]
    runtime.initialize(states)
    runtime.update(
        tick=0,
        dt_ms=1.0,
        states=states,
        spiked_neurons=[0],
        plasticity_active=True,
    )
    summary = runtime.summary(states)
    assert summary["classification"] == "PLAYGROUND_PAN"
    assert summary["scientific_evidence"] is False
    assert summary["evidence_eligible"] is False
    assert summary["pan_contract_id"] == PAN_CONTRACT_ID
    assert summary["pan_contract_status"] == PAN_CONTRACT_STATUS
