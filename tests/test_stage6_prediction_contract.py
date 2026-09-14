"""Regression proofs for the statistical baseline, not neural-memory evidence."""

from __future__ import annotations

import copy
import json
from dataclasses import replace

import pytest

from src.embodiment.models import ActionCommand, EnvironmentObservation, SensorFrame
from src.memory.prediction_metrics import compare_prediction
from src.memory.world_model import TransitionWorldModel


def frame(label="A", sensor="sensor"):
    return SensorFrame(sensor, 1, "digital", {"label": label})


def action():
    return ActionCommand("actuator", 1, "right")


def predict(model, label="A", sensor="sensor"):
    return model.predict(frame(label, sensor), action(), target_tick=2, persistence_state=None)


@pytest.mark.parametrize("value", [True, False, "true", "false", "hello", None])
def test_categorical_type_survives_prediction_and_sorted_roundtrip(value):
    model = TransitionWorldModel()
    model.update(frame(), action(), EnvironmentObservation(2, {"value": value}))
    restored = TransitionWorldModel.from_state_dict(json.loads(json.dumps(model.state_dict(), sort_keys=True)))
    for item in (model, restored):
        result = predict(item).predicted_state["value"]
        assert type(result) is type(value)
        assert result == value
        assert item.error({"value": result}, {"value": value}) == 0.0


def test_original_boolean_bug_has_zero_error_for_correct_prediction():
    model = TransitionWorldModel()
    observed = {"position": 3, "matched": True}
    model.update(frame(), action(), EnvironmentObservation(2, observed))
    assert model.error(predict(model).predicted_state, observed) == 0.0
    assert model.error({"matched": 1}, {"matched": True}) == 1.0


def test_optional_numeric_fields_use_their_own_observation_count():
    model = TransitionWorldModel()
    model.update(frame(), action(), EnvironmentObservation(2, {"x": 8.0}))
    model.update(frame(), action(), EnvironmentObservation(3, {"y": 2.0}))
    assert predict(model).predicted_state == {"x": 8.0, "y": 2.0}


def test_fifo_continuation_after_sorted_serialization_at_capacity():
    continuous = TransitionWorldModel(max_contexts=2)
    for name in ("Z", "A"):
        continuous.update(frame(name), action(), EnvironmentObservation(2, {"x": 1.0}))
    restored = TransitionWorldModel.from_state_dict(json.loads(json.dumps(continuous.state_dict(), sort_keys=True)))
    for name in ("B", "C", "D", "A"):
        for model in (continuous, restored):
            model.update(frame(name), action(), EnvironmentObservation(3, {"x": 2.0}))
        assert continuous.state_dict() == restored.state_dict()
        assert [predict(continuous, key) for key in ("Z", "A", "B")] == [predict(restored, key) for key in ("Z", "A", "B")]


def test_reads_do_not_change_fifo_or_model_state():
    model = TransitionWorldModel()
    model.update(frame(), action(), EnvironmentObservation(2, {"x": 1.0}))
    before = copy.deepcopy(model.state_dict())
    for _ in range(5):
        predict(model)
    assert model.state_dict() == before
    exported = model.state_dict()
    next(iter(exported["contexts"].values()))["numeric_sum"]["x"] = 999
    assert model.state_dict() == before


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -float("inf")])
def test_invalid_update_does_not_evict_or_partially_mutate_context(invalid):
    model = TransitionWorldModel(max_contexts=1)
    model.update(frame(), action(), EnvironmentObservation(2, {"x": 1.0}))
    before = copy.deepcopy(model.state_dict())
    with pytest.raises(ValueError):
        model.update(frame("B"), action(), EnvironmentObservation(2, {"ok": 2.0, "bad": invalid}))
    assert model.state_dict() == before


def test_separate_error_units_and_explicit_missing_coverage():
    errors = compare_prediction({"x": 2.0, "matched": True}, {"x": 5.0, "matched": False, "absent": 1, "metadata": []})
    assert errors.numeric_absolute == {"x": 3.0}
    assert errors.categorical_mismatch == {"matched": 1.0}
    assert errors.missing_fields == ("absent",)
    assert errors.unsupported_fields == ("metadata",)
    assert errors.coverage == pytest.approx(2 / 3)
    assert compare_prediction(None, {"x": 1}).legacy_mean_error is None
    assert compare_prediction(None, {"x": 1}).coverage == 0.0
    assert compare_prediction(None, None).coverage is None


def test_no_cross_sensor_or_cross_actuator_statistics():
    model = TransitionWorldModel()
    model.update(frame(), action(), EnvironmentObservation(2, {"x": 1.0}))
    assert predict(model, sensor="foreign").source == "persistence_reference"
    other = replace(action(), actuator_id="other")
    assert model.predict(frame(), other, target_tick=2, persistence_state=None).source == "persistence_reference"


@pytest.mark.parametrize("capacity", [0, -1, True, 1.5])
def test_capacity_requires_positive_integer(capacity):
    with pytest.raises(ValueError):
        TransitionWorldModel(max_contexts=capacity)


def test_legacy_restore_fails_explicitly_instead_of_guessing_lost_information():
    with pytest.raises(ValueError, match="replay-based rebuild"):
        TransitionWorldModel.from_state_dict({"model_version": 1, "max_contexts": 2, "contexts": {}})


def test_corrupt_order_is_rejected():
    model = TransitionWorldModel()
    model.update(frame(), action(), EnvironmentObservation(2, {"x": 1.0}))
    state = model.state_dict()
    state["context_order"] *= 2
    with pytest.raises(ValueError, match="order"):
        TransitionWorldModel.from_state_dict(state)
