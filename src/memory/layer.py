"""Observation-only memory/prediction integration with independent ablations."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.embodiment.models import ActionCommand, EnvironmentObservation, SensorFrame

from .store import MemoryStore, PredictionRecord
from .world_model import TransitionWorldModel, WorldPrediction


class MemoryWorldModelError(ValueError):
    """Raised when the memory/world-model runtime contract is misused."""


def _boolean(value: Any, name: str) -> bool:
    if type(value) is not bool:
        raise MemoryWorldModelError(f"{name} must be a boolean")
    return value


@dataclass(slots=True)
class MemoryWorldModel:
    """Observer only: no prediction/error is silently injected into SNN learning."""

    store: MemoryStore
    world_model: TransitionWorldModel
    run_id: str
    enabled: bool = True
    persistence_path: Path | None = None
    _episode_id: str = "episode-0"
    prediction_enabled: bool = True
    learning_enabled: bool = True
    _previous: dict[str, Any] | None = field(default=None, repr=False)
    last_error_components: dict[str, Any] | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        _boolean(self.enabled, "enabled")
        _boolean(self.prediction_enabled, "prediction_enabled")
        _boolean(self.learning_enabled, "learning_enabled")
        if self.run_id != self.store.run_id:
            raise MemoryWorldModelError("store and predictor run identities differ")

    def reset_episode(self, episode_id: str) -> None:
        self._episode_id = episode_id
        self._previous = None
        self.last_error_components = None

    def predict(
        self, frame: SensorFrame, action: ActionCommand | None, tick: int
    ) -> WorldPrediction | None:
        if not self.enabled or not self.prediction_enabled:
            return None
        previous_state = None
        if (
            self._previous is not None
            and self._previous["sensor_id"] == frame.sensor_id
            and self._previous["modality"] == frame.modality
        ):
            previous_state = self._previous["state"]
        return self.world_model.predict(
            frame, action, target_tick=tick + 1, persistence_state=previous_state
        )

    def complete(
        self,
        frame: SensorFrame,
        action: ActionCommand | None,
        observation: EnvironmentObservation | None,
        tick: int,
        prediction: WorldPrediction | None,
    ) -> None:
        if not self.enabled:
            return
        self.store.record(frame, action, observation, episode_id=self._episode_id)
        self.last_error_components = None
        if observation is None:
            return
        # Score the pre-action prediction before any model update (prequential).
        if prediction is not None:
            self.last_error_components = self.world_model.error_components(
                prediction.predicted_state, observation.state
            )
            if self.store.write_enabled:
                self.store.record_prediction(
                    PredictionRecord(
                        self.run_id,
                        self._episode_id,
                        tick,
                        prediction.target_tick,
                        prediction.source,
                        prediction.predicted_state,
                        observation.state,
                        self.world_model.error(
                            prediction.predicted_state, observation.state
                        ),
                        prediction.uncertainty,
                    )
                )
        if self.learning_enabled:
            self.world_model.update(frame, action, observation)
        # A single prior observation is independent of episodic read/write flags.
        self._previous = {
            "sensor_id": frame.sensor_id,
            "modality": frame.modality,
            "state": copy.deepcopy(observation.state),
        }
        if self.persistence_path is not None:
            self.save(self.persistence_path)

    def state_dict(self) -> dict[str, Any]:
        state = {
            "schema_version": 2,
            "owner": "memory.world_model.integration",
            "run_id": self.run_id,
            "enabled": self.enabled,
            "episode_id": self._episode_id,
            "prediction_enabled": self.prediction_enabled,
            "learning_enabled": self.learning_enabled,
            "previous_observation": copy.deepcopy(self._previous),
            "last_error_components": copy.deepcopy(self.last_error_components),
            "world_model": self.world_model.state_dict(),
            "memory": self.store.state_dict(),
        }
        unsigned = json.dumps(
            state,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        state["integrity_digest"] = hashlib.sha256(unsigned.encode("utf-8")).hexdigest()
        return state

    def save(self, path: Path | None = None) -> Path:
        destination = path or self.persistence_path
        if destination is None:
            raise MemoryWorldModelError("coupled persistence path is not configured")
        payload = json.dumps(
            self.state_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
        destination.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(
            prefix=f".{destination.name}.", dir=str(destination.parent)
        )
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, destination)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return destination

    @classmethod
    def load(cls, path: Path) -> "MemoryWorldModel":
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(state, dict) or state.get("schema_version") != 2:
                raise MemoryWorldModelError(
                    "unsupported coupled state schema; retain legacy file and rebuild from a provenance-bound replay"
                )
            unsigned = dict(state)
            digest = unsigned.pop("integrity_digest", None)
            expected = hashlib.sha256(
                json.dumps(
                    unsigned,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=True,
                    allow_nan=False,
                ).encode("utf-8")
            ).hexdigest()
            if (
                state.get("owner") != "memory.world_model.integration"
                or digest != expected
            ):
                raise MemoryWorldModelError("coupled state integrity check failed")
            previous = state.get("previous_observation")
            if previous is not None and (
                not isinstance(previous, dict)
                or not isinstance(previous.get("sensor_id"), str)
                or not isinstance(previous.get("modality"), str)
                or not isinstance(previous.get("state"), dict)
            ):
                raise MemoryWorldModelError("invalid previous observation")
            return cls(
                store=MemoryStore.from_state_dict(state["memory"]),
                world_model=TransitionWorldModel.from_state_dict(state["world_model"]),
                run_id=str(state["run_id"]),
                enabled=_boolean(state["enabled"], "enabled"),
                persistence_path=path,
                _episode_id=str(state["episode_id"]),
                prediction_enabled=_boolean(
                    state["prediction_enabled"], "prediction_enabled"
                ),
                learning_enabled=_boolean(
                    state["learning_enabled"], "learning_enabled"
                ),
                _previous=copy.deepcopy(previous),
                last_error_components=copy.deepcopy(state.get("last_error_components")),
            )
        except MemoryWorldModelError:
            raise
        except (OSError, KeyError, TypeError, ValueError) as error:
            raise MemoryWorldModelError(
                "coupled state could not be restored"
            ) from error
