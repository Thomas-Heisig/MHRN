"""Reference rebuilding is explicit, deterministic, bounded and non-destructive."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import pytest

from src.embodiment.models import ActionCommand, EnvironmentObservation, SensorFrame
from src.memory import MemoryStore, MemoryWorldModel, TransitionWorldModel
from src.memory.replay import CAPACITIES, FLAGS, ReplayError, rebuild_reference


def trace(flags: tuple[bool, ...] = (True, True, True, True)) -> dict:
    return {
        "kind": "mhrn.cognition.replay",
        "schema_version": 1,
        "run_id": "test-replay",
        "complete_from_reset": True,
        "configuration": dict.fromkeys(CAPACITIES, 2),
        "events": [
            {
                "episode_id": "episode-0",
                "tick": tick,
                "frame": {
                    "sensor_id": "test",
                    "modality": "digital",
                    "tick": tick,
                    "payload": {"cue": tick % 3},
                },
                "action": {
                    "actuator_id": "virtual",
                    "tick": tick,
                    "action": "stay",
                    "payload": None,
                },
                "observation": {
                    "tick": tick + 1,
                    "state": {"matched": False, "position": 0},
                    "reward": 0,
                    "terminated": False,
                    "truncated": False,
                },
                "controls": dict(zip(FLAGS, flags, strict=True)),
            }
            for tick in range(6)
        ],
    }


def write_source(tmp_path: Path, payload: dict) -> tuple[Path, str]:
    source = tmp_path / "trace.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    return source, hashlib.sha256(source.read_bytes()).hexdigest()


@pytest.mark.parametrize("flags", list(itertools.product((False, True), repeat=4)))
def test_replay_matches_direct_execution_at_capacity(
    tmp_path: Path, flags: tuple[bool, ...]
) -> None:
    payload = trace(flags)
    source, digest = write_source(tmp_path, payload)
    before = source.read_bytes()
    direct = MemoryWorldModel(
        MemoryStore(
            run_id="test-replay",
            **{key: 2 for key in CAPACITIES if key != "max_contexts"},
        ),
        TransitionWorldModel(max_contexts=2),
        "test-replay",
    )
    for event in payload["events"]:
        frame = SensorFrame(**event["frame"])
        action = ActionCommand(**event["action"])
        observed = EnvironmentObservation(**event["observation"])
        direct.store.set_controls(read_enabled=flags[0], write_enabled=flags[1])
        direct.prediction_enabled, direct.learning_enabled = flags[2:]
        direct.complete(
            frame,
            action,
            observed,
            frame.tick,
            direct.predict(frame, action, frame.tick),
        )
    state = rebuild_reference(source, tmp_path / "rebuilt", digest)
    restored = MemoryWorldModel.load(state)
    assert restored.state_dict() == direct.state_dict()
    assert source.read_bytes() == before
    provenance = json.loads((state.parent / "provenance.json").read_text())
    assert provenance["source_sha256"] == digest
    assert provenance["state_sha256"] == hashlib.sha256(state.read_bytes()).hexdigest()
    assert provenance["canonical_runtime_checkpoint"] is False
    assert provenance["scientific_evidence"] is False
    assert len(provenance["implementation_sha256"]) == 5
    # Continue after restore while triggering another FIFO eviction.
    frame = SensorFrame("test", 6, "digital", {"cue": 3})
    observed = EnvironmentObservation(7, {"matched": True, "position": 2})
    for model in (direct, restored):
        model.complete(frame, None, observed, 6, model.predict(frame, None, 6))
    assert restored.state_dict() == direct.state_dict()


@pytest.mark.parametrize(
    "case",
    [
        "hash",
        "gap",
        "reorder",
        "incomplete",
        "boolean",
        "capacity",
        "frame_tick",
        "result_tick",
        "nan",
        "empty",
        "legacy",
        "ended",
        "schema_bool",
    ],
)
def test_invalid_history_never_creates_destination(tmp_path: Path, case: str) -> None:
    payload = trace()
    if case == "gap":
        payload["events"][1]["tick"] = 7
    elif case == "reorder":
        payload["events"] = list(reversed(payload["events"]))
    elif case == "incomplete":
        payload["complete_from_reset"] = False
    elif case == "boolean":
        payload["events"][0]["controls"]["read_enabled"] = "false"
    elif case == "capacity":
        payload["configuration"]["max_contexts"] = True
    elif case == "frame_tick":
        payload["events"][0]["frame"]["tick"] = 1
    elif case == "result_tick":
        payload["events"][0]["observation"]["tick"] = 99
    elif case == "nan":
        payload["events"][0]["frame"]["payload"] = float("nan")
    elif case == "empty":
        payload["events"] = []
    elif case == "legacy":
        payload = {"schema_version": 1, "contexts": {}}
    elif case == "ended":
        payload["events"][0]["observation"]["terminated"] = True
    elif case == "schema_bool":
        payload["schema_version"] = True
    source, digest = write_source(tmp_path, payload)
    original = source.read_bytes()
    with pytest.raises(ReplayError):
        rebuild_reference(
            source, tmp_path / "absent", "0" * 64 if case == "hash" else digest
        )
    assert not (tmp_path / "absent").exists()
    assert source.read_bytes() == original


def test_existing_destination_and_duplicate_keys_are_rejected(tmp_path: Path) -> None:
    source, digest = write_source(tmp_path, trace())
    with pytest.raises(FileExistsError):
        rebuild_reference(source, tmp_path, digest)
    source.write_text('{"kind": 1, "kind": 2}')
    with pytest.raises(ReplayError, match="duplicate"):
        rebuild_reference(
            source, tmp_path / "absent", hashlib.sha256(source.read_bytes()).hexdigest()
        )
    assert not (tmp_path / "absent").exists()
