"""Reference-component integration checks, not neural-memory evidence."""

from __future__ import annotations

import itertools
import json
from dataclasses import replace

import pytest

from src.embodiment.models import ActionCommand, EnvironmentObservation, SensorFrame
from src.experience.composition import build_experience_subsystem
from src.memory.layer import MemoryWorldModel, MemoryWorldModelError
from src.memory.store import MemoryStore
from src.memory.world_model import TransitionWorldModel


def make_layer(**kwargs):
    return MemoryWorldModel(
        MemoryStore(run_id="stage6-test"),
        TransitionWorldModel(max_contexts=2),
        "stage6-test",
        **kwargs,
    )


def cycle(layer, tick, label="A"):
    frame = SensorFrame("sensor", tick, "digital", {"label": label})
    action = ActionCommand("actuator", tick, "right")
    observed = EnvironmentObservation(tick + 1, {"x": float(tick), "matched": True})
    prediction = layer.predict(frame, action, tick)
    layer.complete(frame, action, observed, tick, prediction)
    return prediction


@pytest.mark.parametrize(
    "read,write,infer,learn", list(itertools.product((False, True), repeat=4))
)
def test_all_four_controls_are_independent(read, write, infer, learn):
    layer = make_layer(prediction_enabled=infer, learning_enabled=learn)
    layer.store.set_controls(read_enabled=read, write_enabled=write)
    for tick in (1, 2):
        prediction = cycle(layer, tick)
        assert (prediction is not None) is infer
    assert len(layer.store.episodes) == (2 if write else 0)
    assert len(layer.store.predictions) == (2 if write and infer else 0)
    assert bool(layer.world_model.state_dict()["contexts"]) is learn
    assert len(layer.store.recall()) == (2 if read and write else 0)


def test_persistence_uses_only_previous_observation_and_clears_on_episode_reset():
    layer = make_layer(learning_enabled=False)
    layer.store.set_controls(read_enabled=False, write_enabled=False)
    assert cycle(layer, 1).predicted_state is None
    frame = SensorFrame("sensor", 2, "digital", {"label": "new"})
    action = ActionCommand("actuator", 2, "right")
    assert layer.predict(frame, action, 2).predicted_state == {
        "x": 1.0,
        "matched": True,
    }
    assert (
        layer.predict(replace(frame, sensor_id="foreign"), action, 2).predicted_state
        is None
    )
    layer.reset_episode("new-episode")
    assert layer.predict(frame, action, 2).predicted_state is None


def test_save_load_continuation_at_capacity_preserves_predictions_and_state(tmp_path):
    continuous = make_layer()
    cycle(continuous, 1, "Z")
    cycle(continuous, 2, "A")
    path = tmp_path / "coupled-v2.json"
    continuous.save(path)
    restored = MemoryWorldModel.load(path)
    assert restored.state_dict() == continuous.state_dict()
    for tick, label in enumerate(("B", "C", "A", "D"), start=3):
        assert cycle(continuous, tick, label) == cycle(restored, tick, label)
        assert restored.state_dict() == continuous.state_dict()


def test_save_load_preserves_separate_controls(tmp_path):
    layer = make_layer(prediction_enabled=False, learning_enabled=True)
    layer.store.set_controls(read_enabled=False, write_enabled=False)
    cycle(layer, 1)
    path = tmp_path / "controls.json"
    layer.save(path)
    restored = MemoryWorldModel.load(path)
    assert restored.prediction_enabled is False
    assert restored.learning_enabled is True
    assert restored.store.controls() == {"read_enabled": False, "write_enabled": False}
    assert restored.state_dict() == layer.state_dict()


def test_legacy_load_does_not_modify_original_file(tmp_path):
    path = tmp_path / "legacy.json"
    original = json.dumps({"schema_version": 1})
    path.write_text(original, encoding="utf-8")
    with pytest.raises(MemoryWorldModelError, match="retain legacy"):
        MemoryWorldModel.load(path)
    assert path.read_text(encoding="utf-8") == original


@pytest.mark.parametrize("name", ["enabled", "prediction_enabled", "learning_enabled"])
def test_string_boolean_is_not_silently_coerced(name):
    with pytest.raises(MemoryWorldModelError, match="boolean"):
        make_layer(**{name: "false"})


def test_composition_exposes_predictor_controls_without_reusing_memory_flags():
    config = {
        "experience": {
            "enabled": True,
            "sensor": {
                "provider": "deterministic_trace",
                "trace": [{"cpu_percent": 1.0}],
            },
            "memory": {
                "enabled": True,
                "prediction_enabled": False,
                "learning_enabled": False,
            },
        }
    }
    engine = build_experience_subsystem(config, object(), object())
    assert engine.memory.prediction_enabled is False
    assert engine.memory.learning_enabled is False
    assert engine.memory.store.read_enabled is True
    assert engine.memory.store.write_enabled is True
