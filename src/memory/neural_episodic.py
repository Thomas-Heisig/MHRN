"""Bounded episodic traces tied to observed SNN spike patterns.

This module stores sparse activity patterns produced by the network and supports
context-bound partial-cue retrieval. It is an engineering mechanism for Stage 6,
not evidence that the biological hippocampus has been reproduced. Retrieval is
read-only and does not change network state or action selection by itself.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, cast

from src.embodiment.models import (
    EnvironmentObservation,
    JSONValue,
    SensorFrame,
)

NEURAL_EPISODIC_SCHEMA_VERSION = 1
NEURAL_EPISODIC_OWNER = "memory.neural_episodic"


class NeuralEpisodicMemoryError(ValueError):
    """Raised when a neural episodic memory contract is invalid."""


def _json_copy(value: object) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=True, allow_nan=False))


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _digest(state: dict[str, Any]) -> str:
    unsigned = dict(state)
    unsigned.pop("integrity_digest", None)
    return hashlib.sha256(_canonical(unsigned)).hexdigest()


def spike_ids_from_result(result: object) -> tuple[int, ...]:
    """Extract a deterministic sparse network pattern from StepResult-like data."""

    raw: object | None
    if isinstance(result, Mapping):
        mapping = cast(Mapping[object, object], result)
        raw = mapping.get("spike_ids")
        if raw is None:
            raw = mapping.get("output_spike_ids")
    else:
        raw = getattr(result, "spike_ids", None)
        if raw is None:
            raw = getattr(result, "output_spike_ids", None)
    if raw is None:
        return ()
    if isinstance(raw, (str, bytes)) or not isinstance(raw, Sequence):
        raise NeuralEpisodicMemoryError("network spike pattern must be a sequence")
    values: set[int] = set()
    for value in cast(Sequence[object], raw):
        if type(value) is not int or value < 0:
            raise NeuralEpisodicMemoryError(
                "network spike IDs must be non-negative integers"
            )
        values.add(value)
    return tuple(sorted(values))


@dataclass(frozen=True, slots=True)
class NeuralEpisode:
    """One context-bound sparse activity trace and its observed outcome."""

    run_id: str
    episode_id: str
    tick: int
    sensor_id: str
    modality: str
    spike_ids: tuple[int, ...]
    frame_payload: JSONValue
    actual_state: dict[str, JSONValue] | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "episode_id": self.episode_id,
            "tick": self.tick,
            "sensor_id": self.sensor_id,
            "modality": self.modality,
            "spike_ids": list(self.spike_ids),
            "frame_payload": _json_copy(self.frame_payload),
            "actual_state": _json_copy(self.actual_state),
        }


@dataclass(frozen=True, slots=True)
class NeuralRecallMatch:
    """Deterministic similarity result for one stored activity trace."""

    episode: NeuralEpisode
    score: float
    cue_coverage: float
    engram_coverage: float


class NeuralEpisodicMemory:
    """Bounded sparse-pattern memory with independent read/write controls."""

    def __init__(
        self,
        *,
        run_id: str,
        capacity: int = 256,
        retention_ticks: int = 4096,
        read_enabled: bool = True,
        write_enabled: bool = True,
    ) -> None:
        if type(capacity) is not int or capacity <= 0:
            raise NeuralEpisodicMemoryError("capacity must be a positive integer")
        if type(retention_ticks) is not int or retention_ticks <= 0:
            raise NeuralEpisodicMemoryError(
                "retention_ticks must be a positive integer"
            )
        if type(read_enabled) is not bool or type(write_enabled) is not bool:
            raise NeuralEpisodicMemoryError("memory controls must be booleans")
        self.run_id = run_id
        self.capacity = capacity
        self.retention_ticks = retention_ticks
        self.read_enabled = read_enabled
        self.write_enabled = write_enabled
        self._episode_id = "episode-0"
        self._episodes: list[NeuralEpisode] = []

    @property
    def episodes(self) -> tuple[NeuralEpisode, ...]:
        return tuple(self._episodes)

    def reset_episode(self, episode_id: str) -> None:
        if not episode_id:
            raise NeuralEpisodicMemoryError("episode_id must not be empty")
        self._episode_id = episode_id

    def record(
        self,
        result: object,
        frame: SensorFrame,
        observation: EnvironmentObservation | None,
    ) -> NeuralEpisode | None:
        """Bind the current SNN activity pattern to context and observed outcome."""

        if not self.write_enabled:
            return None
        pattern = spike_ids_from_result(result)
        if not pattern:
            return None
        trace = NeuralEpisode(
            run_id=self.run_id,
            episode_id=self._episode_id,
            tick=frame.tick,
            sensor_id=frame.sensor_id,
            modality=frame.modality,
            spike_ids=pattern,
            frame_payload=cast(JSONValue, _json_copy(frame.payload)),
            actual_state=(
                None
                if observation is None
                else cast(dict[str, JSONValue], _json_copy(observation.state))
            ),
        )
        self._episodes.append(trace)
        cutoff = frame.tick - self.retention_ticks + 1
        self._episodes = [item for item in self._episodes if item.tick >= cutoff]
        self._episodes = self._episodes[-self.capacity :]
        return trace

    def recall(
        self,
        cue_spike_ids: Sequence[int],
        *,
        sensor_id: str | None = None,
        modality: str | None = None,
        limit: int = 8,
        min_score: float = 0.0,
    ) -> tuple[NeuralRecallMatch, ...]:
        """Retrieve traces by sparse overlap without mutating stored state."""

        if not self.read_enabled or limit <= 0:
            return ()
        if not 0.0 <= min_score <= 1.0:
            raise NeuralEpisodicMemoryError("min_score must be between zero and one")
        cue = spike_ids_from_result({"spike_ids": tuple(cue_spike_ids)})
        if not cue:
            return ()
        cue_set = set(cue)
        matches: list[NeuralRecallMatch] = []
        for episode in self._episodes:
            if sensor_id is not None and episode.sensor_id != sensor_id:
                continue
            if modality is not None and episode.modality != modality:
                continue
            engram = set(episode.spike_ids)
            intersection = len(cue_set & engram)
            if intersection == 0:
                continue
            cue_coverage = intersection / len(cue_set)
            engram_coverage = intersection / len(engram)
            score = (2.0 * intersection) / (len(cue_set) + len(engram))
            if score >= min_score:
                matches.append(
                    NeuralRecallMatch(
                        episode=episode,
                        score=score,
                        cue_coverage=cue_coverage,
                        engram_coverage=engram_coverage,
                    )
                )
        matches.sort(
            key=lambda item: (
                -item.score,
                -item.cue_coverage,
                -item.episode.tick,
                item.episode.episode_id,
            )
        )
        return tuple(matches[:limit])

    def state_dict(self) -> dict[str, Any]:
        state: dict[str, Any] = {
            "schema_version": NEURAL_EPISODIC_SCHEMA_VERSION,
            "owner": NEURAL_EPISODIC_OWNER,
            "run_id": self.run_id,
            "capacity": self.capacity,
            "retention_ticks": self.retention_ticks,
            "read_enabled": self.read_enabled,
            "write_enabled": self.write_enabled,
            "episode_id": self._episode_id,
            "episodes": [item.to_dict() for item in self._episodes],
        }
        state["integrity_digest"] = _digest(state)
        return state

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> "NeuralEpisodicMemory":
        if state.get("schema_version") != NEURAL_EPISODIC_SCHEMA_VERSION:
            raise NeuralEpisodicMemoryError("unsupported neural episodic schema")
        if state.get("owner") != NEURAL_EPISODIC_OWNER or state.get(
            "integrity_digest"
        ) != _digest(state):
            raise NeuralEpisodicMemoryError("neural episodic integrity check failed")
        read_enabled = state.get("read_enabled")
        write_enabled = state.get("write_enabled")
        if type(read_enabled) is not bool or type(write_enabled) is not bool:
            raise NeuralEpisodicMemoryError("memory controls must be booleans")
        memory = cls(
            run_id=str(state["run_id"]),
            capacity=int(state["capacity"]),
            retention_ticks=int(state["retention_ticks"]),
            read_enabled=read_enabled,
            write_enabled=write_enabled,
        )
        memory._episode_id = str(state["episode_id"])
        raw_episodes = state.get("episodes")
        if not isinstance(raw_episodes, list):
            raise NeuralEpisodicMemoryError("episodes must be a list")
        for raw in cast(list[object], raw_episodes):
            if not isinstance(raw, dict):
                raise NeuralEpisodicMemoryError("episode entry must be an object")
            item = cast(dict[str, Any], raw)
            spikes = spike_ids_from_result({"spike_ids": item.get("spike_ids")})
            memory._episodes.append(
                NeuralEpisode(
                    run_id=str(item["run_id"]),
                    episode_id=str(item["episode_id"]),
                    tick=int(item["tick"]),
                    sensor_id=str(item["sensor_id"]),
                    modality=str(item["modality"]),
                    spike_ids=spikes,
                    frame_payload=cast(JSONValue, item["frame_payload"]),
                    actual_state=(
                        None
                        if item["actual_state"] is None
                        else cast(dict[str, JSONValue], item["actual_state"])
                    ),
                )
            )
        if len(memory._episodes) > memory.capacity:
            raise NeuralEpisodicMemoryError(
                "stored episodes exceed configured capacity"
            )
        if any(item.run_id != memory.run_id for item in memory._episodes):
            raise NeuralEpisodicMemoryError("stored episode run identity mismatch")
        return memory


__all__ = [
    "NeuralEpisode",
    "NeuralEpisodicMemory",
    "NeuralEpisodicMemoryError",
    "NeuralRecallMatch",
    "spike_ids_from_result",
]
