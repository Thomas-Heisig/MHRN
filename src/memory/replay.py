"""Rebuild the v2 reference component from explicit, hash-bound raw events.

This is not an aggregate-v1 migration or a neural/runtime checkpoint restore.
Bounded episode exports cannot substitute for a complete input/control history.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from src.embodiment.models import ActionCommand, EnvironmentObservation, SensorFrame
from src.memory.layer import MemoryWorldModel, MemoryWorldModelError
from src.memory.store import MemoryStore
from src.memory.world_model import TransitionWorldModel

MAX_INPUT_BYTES = 8 * 1024 * 1024
MAX_EVENTS = 100_000
FLAGS = ("read_enabled", "write_enabled", "prediction_enabled", "learning_enabled")
CAPACITIES = (
    "episode_capacity",
    "working_capacity",
    "prediction_capacity",
    "retention_ticks",
    "max_contexts",
)


class ReplayError(ValueError):
    """The supplied history cannot safely rebuild a reference state."""


def _object(value: Any, keys: set[str], name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ReplayError(f"{name} requires exactly {sorted(keys)}")
    return value


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReplayError(f"{name} must be a non-empty string")
    return value


def _integer(value: Any, name: str, minimum: int = 0) -> int:
    if type(value) is not int or not minimum <= value <= MAX_EVENTS:
        raise ReplayError(f"{name} must be an integer in [{minimum}, {MAX_EVENTS}]")
    return value


def _flags(value: Any) -> dict[str, bool]:
    raw = _object(value, set(FLAGS), "controls")
    if any(type(item) is not bool for item in raw.values()):
        raise ReplayError("control values must be booleans")
    return dict(raw)


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReplayError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ReplayError(f"non-finite JSON constant: {value}")


def rebuild_reference(source: Path, destination: Path, expected_sha256: str) -> Path:
    """Replay from reset into a NEW directory; never rewrite a source or snapshot.

    The caller supplies the expected hash independently. The completeness flag is
    a source declaration, not independent evidence of the original run's history.
    """
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("rebuild requires a new destination directory")
    with source.open("rb") as stream:
        data = stream.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        raise ReplayError("replay exceeds the input byte budget")
    digest = hashlib.sha256(data).hexdigest()
    if len(expected_sha256) != 64 or digest != expected_sha256.lower():
        raise ReplayError("replay source SHA-256 mismatch")
    try:
        raw = json.loads(
            data, object_pairs_hook=_unique, parse_constant=_invalid_constant
        )
        # Also reject overflow such as 1e999, including nested sensor payloads.
        json.dumps(raw, allow_nan=False)
        packet = _object(
            raw,
            {
                "kind",
                "schema_version",
                "run_id",
                "complete_from_reset",
                "configuration",
                "events",
            },
            "replay",
        )
        if (
            packet["kind"] != "mhrn.cognition.replay"
            or type(packet["schema_version"]) is not int
            or packet["schema_version"] != 1
        ):
            raise ReplayError("unsupported replay protocol")
        if packet["complete_from_reset"] is not True:
            raise ReplayError("a complete history from reset must be declared")
        run_id = _text(packet["run_id"], "run_id")
        config = _object(packet["configuration"], set(CAPACITIES), "configuration")
        sizes = {key: _integer(config[key], key, 1) for key in CAPACITIES}
        store = MemoryStore(
            run_id=run_id,
            episode_capacity=sizes["episode_capacity"],
            working_capacity=sizes["working_capacity"],
            prediction_capacity=sizes["prediction_capacity"],
            retention_ticks=sizes["retention_ticks"],
        )
        model = MemoryWorldModel(
            store, TransitionWorldModel(max_contexts=sizes["max_contexts"]), run_id
        )
        events = packet["events"]
        if not isinstance(events, list) or not 1 <= len(events) <= MAX_EVENTS:
            raise ReplayError("replay requires a bounded, non-empty event list")
        seen: set[str] = set()
        episode: str | None = None
        last_tick = -1
        ended = False
        for raw_event in events:
            event = _object(
                raw_event,
                {"episode_id", "tick", "frame", "action", "observation", "controls"},
                "event",
            )
            current = _text(event["episode_id"], "episode_id")
            tick = _integer(event["tick"], "tick")
            if current != episode:
                if current in seen:
                    raise ReplayError("episode history is reordered")
                seen.add(current)
                episode, last_tick, ended = current, -1, False
                model.reset_episode(current)
            if tick != last_tick + 1 or ended:
                raise ReplayError(
                    "ticks must be contiguous from zero within each episode"
                )
            controls = _flags(event["controls"])
            store.set_controls(
                read_enabled=controls["read_enabled"],
                write_enabled=controls["write_enabled"],
            )
            model.prediction_enabled = controls["prediction_enabled"]
            model.learning_enabled = controls["learning_enabled"]
            frame_data = _object(
                event["frame"], {"sensor_id", "tick", "modality", "payload"}, "frame"
            )
            if _integer(frame_data["tick"], "frame.tick") != tick:
                raise ReplayError("sensor and event ticks differ")
            frame = SensorFrame(
                _text(frame_data["sensor_id"], "sensor_id"),
                tick,
                _text(frame_data["modality"], "modality"),
                frame_data["payload"],
            )
            action = None
            if event["action"] is not None:
                command = _object(
                    event["action"],
                    {"actuator_id", "tick", "action", "payload"},
                    "action",
                )
                if _integer(command["tick"], "action.tick") != tick:
                    raise ReplayError("action and event ticks differ")
                action = ActionCommand(
                    _text(command["actuator_id"], "actuator_id"),
                    tick,
                    _text(command["action"], "action"),
                    command["payload"],
                )
            observation = None
            if event["observation"] is not None:
                observed = _object(
                    event["observation"],
                    {"tick", "state", "reward", "terminated", "truncated"},
                    "observation",
                )
                if _integer(
                    observed["tick"], "observation.tick"
                ) != tick + 1 or not isinstance(observed["state"], dict):
                    raise ReplayError(
                        "expected a next-tick observation with object state"
                    )
                reward = observed["reward"]
                if type(reward) not in (int, float) or not math.isfinite(reward):
                    raise ReplayError("reward must be finite and numeric")
                if (
                    type(observed["terminated"]) is not bool
                    or type(observed["truncated"]) is not bool
                ):
                    raise ReplayError("episode termination flags must be boolean")
                observation = EnvironmentObservation(
                    tick + 1,
                    observed["state"],
                    reward,
                    observed["terminated"],
                    observed["truncated"],
                )
                ended = observation.terminated or observation.truncated
            prediction = model.predict(frame, action, tick)
            model.complete(frame, action, observation, tick, prediction)
            last_tick = tick
    except (KeyError, TypeError, ValueError, OverflowError, RecursionError) as error:
        if isinstance(error, ReplayError):
            raise
        raise ReplayError(f"invalid replay history: {error}") from error
    # Nothing has been written before the entire input has been validated/replayed.
    destination.mkdir(parents=False, exist_ok=False)
    state_path = model.save(destination / "state.json")
    sources = {
        name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
        for name in (
            "replay.py",
            "layer.py",
            "store.py",
            "world_model.py",
            "prediction_metrics.py",
        )
    }
    provenance = {
        "kind": "reference_rebuild_not_runtime_migration",
        "schema_version": 1,
        "source_sha256": digest,
        "event_count": len(events),
        "episode_count": len(seen),
        "source_completeness": "declared_not_independently_verified",
        "replay_protocol": "mhrn.cognition.replay.v1",
        "run_id": run_id,
        "state_sha256": hashlib.sha256(state_path.read_bytes()).hexdigest(),
        "implementation_sha256": sources,
        "scientific_evidence": False,
        "neural_memory_claim": False,
        "canonical_runtime_checkpoint": False,
    }
    with (destination / "provenance.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    return state_path


def main() -> None:
    """Command-line rebuild requiring explicit source and a new destination."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()
    try:
        print(rebuild_reference(args.source, args.destination, args.sha256))
    except (OSError, ReplayError, MemoryWorldModelError) as error:
        parser.exit(2, f"Rebuild rejected: {error}\n")


if __name__ == "__main__":
    main()
