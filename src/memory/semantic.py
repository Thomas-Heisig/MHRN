"""Deterministic semantic prototypes derived across independent neural episodes.

The implementation compresses recurring sparse SNN activity across different
episodes into bounded prototypes. Repetitions within one episode cannot increase
semantic support. This is an engineering hypothesis probe for semantization, not
a claim of neocortical equivalence or accepted scientific evidence.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, cast

from .neural_episodic import NeuralEpisode, spike_ids_from_result

SEMANTIC_SCHEMA_VERSION = 1
SEMANTIC_OWNER = "memory.semantic_prototypes"


class SemanticMemoryError(ValueError):
    """Raised when semantic prototype state or configuration is invalid."""


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


def _ratio(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SemanticMemoryError(f"{name} must be numeric")
    result = float(value)
    if not 0.0 < result <= 1.0:
        raise SemanticMemoryError(f"{name} must be in (0, 1]")
    return result


def _dice(left: Sequence[int], right: Sequence[int]) -> float:
    left_set = set(left)
    right_set = set(right)
    if not left_set or not right_set:
        return 0.0
    return 2.0 * len(left_set & right_set) / (len(left_set) + len(right_set))


@dataclass(frozen=True, slots=True)
class SemanticConcept:
    """Compressed sparse representation supported by independent episodes."""

    concept_id: int
    sensor_id: str
    modality: str
    episode_ids: tuple[str, ...]
    neuron_episode_support: dict[int, int]
    prototype_spike_ids: tuple[int, ...]

    @property
    def episode_count(self) -> int:
        return len(self.episode_ids)

    def to_dict(self) -> dict[str, Any]:
        return {
            "concept_id": self.concept_id,
            "sensor_id": self.sensor_id,
            "modality": self.modality,
            "episode_ids": list(self.episode_ids),
            "neuron_episode_support": {
                str(key): self.neuron_episode_support[key]
                for key in sorted(self.neuron_episode_support)
            },
            "prototype_spike_ids": list(self.prototype_spike_ids),
        }


@dataclass(frozen=True, slots=True)
class SemanticMatch:
    concept: SemanticConcept
    score: float
    cue_coverage: float
    prototype_coverage: float


@dataclass(slots=True)
class _MutableConcept:
    concept_id: int
    sensor_id: str
    modality: str
    episode_ids: set[str]
    support: dict[int, int]


class SemanticMemory:
    """Bounded prototype memory built only from independent episode support."""

    def __init__(
        self,
        *,
        max_concepts: int = 128,
        min_episode_support: int = 2,
        prototype_support: float = 0.6,
        match_threshold: float = 0.5,
    ) -> None:
        if type(max_concepts) is not int or max_concepts <= 0:
            raise SemanticMemoryError("max_concepts must be a positive integer")
        if type(min_episode_support) is not int or min_episode_support <= 1:
            raise SemanticMemoryError("min_episode_support must exceed one")
        self.max_concepts = max_concepts
        self.min_episode_support = min_episode_support
        self.prototype_support = _ratio(prototype_support, "prototype_support")
        self.match_threshold = _ratio(match_threshold, "match_threshold")
        self._concepts: list[_MutableConcept] = []
        self._next_concept_id = 1

    def _prototype(self, concept: _MutableConcept) -> tuple[int, ...]:
        count = len(concept.episode_ids)
        if count == 0:
            return ()
        return tuple(
            sorted(
                neuron_id
                for neuron_id, support in concept.support.items()
                if support / count >= self.prototype_support
            )
        )

    def _frozen(self, concept: _MutableConcept) -> SemanticConcept:
        return SemanticConcept(
            concept_id=concept.concept_id,
            sensor_id=concept.sensor_id,
            modality=concept.modality,
            episode_ids=tuple(sorted(concept.episode_ids)),
            neuron_episode_support=dict(sorted(concept.support.items())),
            prototype_spike_ids=self._prototype(concept),
        )

    @property
    def concepts(self) -> tuple[SemanticConcept, ...]:
        return tuple(self._frozen(item) for item in self._concepts)

    @property
    def mature_concepts(self) -> tuple[SemanticConcept, ...]:
        return tuple(
            concept
            for concept in self.concepts
            if concept.episode_count >= self.min_episode_support
            and concept.prototype_spike_ids
        )

    def consolidate(self, episodes: Sequence[NeuralEpisode]) -> int:
        """Integrate one contribution per episode/context and return update count."""

        grouped: dict[tuple[str, str, str], set[int]] = defaultdict(set)
        for episode in episodes:
            key = (episode.episode_id, episode.sensor_id, episode.modality)
            grouped[key].update(episode.spike_ids)

        updates = 0
        for (episode_id, sensor_id, modality), neurons in sorted(grouped.items()):
            pattern = tuple(sorted(neurons))
            if not pattern:
                continue
            eligible = [
                concept
                for concept in self._concepts
                if concept.sensor_id == sensor_id
                and concept.modality == modality
                and episode_id not in concept.episode_ids
            ]
            scored = [
                (_dice(pattern, self._prototype(concept)), concept.concept_id, concept)
                for concept in eligible
            ]
            scored.sort(key=lambda item: (-item[0], item[1]))
            target = scored[0][2] if scored and scored[0][0] >= self.match_threshold else None
            if target is None:
                if len(self._concepts) >= self.max_concepts:
                    self._concepts.pop(0)
                target = _MutableConcept(
                    concept_id=self._next_concept_id,
                    sensor_id=sensor_id,
                    modality=modality,
                    episode_ids=set(),
                    support={},
                )
                self._next_concept_id += 1
                self._concepts.append(target)
            target.episode_ids.add(episode_id)
            for neuron_id in pattern:
                target.support[neuron_id] = target.support.get(neuron_id, 0) + 1
            updates += 1
        return updates

    def query(
        self,
        cue_spike_ids: Sequence[int],
        *,
        sensor_id: str,
        modality: str,
        limit: int = 8,
    ) -> tuple[SemanticMatch, ...]:
        """Match a held-out sparse cue against mature semantic prototypes."""

        if limit <= 0:
            return ()
        cue = spike_ids_from_result({"spike_ids": tuple(cue_spike_ids)})
        if not cue:
            return ()
        cue_set = set(cue)
        matches: list[SemanticMatch] = []
        for concept in self.mature_concepts:
            if concept.sensor_id != sensor_id or concept.modality != modality:
                continue
            prototype = set(concept.prototype_spike_ids)
            intersection = len(cue_set & prototype)
            if intersection == 0:
                continue
            matches.append(
                SemanticMatch(
                    concept=concept,
                    score=_dice(cue, concept.prototype_spike_ids),
                    cue_coverage=intersection / len(cue_set),
                    prototype_coverage=intersection / len(prototype),
                )
            )
        matches.sort(key=lambda item: (-item.score, item.concept.concept_id))
        return tuple(matches[:limit])

    def state_dict(self) -> dict[str, Any]:
        state: dict[str, Any] = {
            "schema_version": SEMANTIC_SCHEMA_VERSION,
            "owner": SEMANTIC_OWNER,
            "max_concepts": self.max_concepts,
            "min_episode_support": self.min_episode_support,
            "prototype_support": self.prototype_support,
            "match_threshold": self.match_threshold,
            "next_concept_id": self._next_concept_id,
            "concepts": [concept.to_dict() for concept in self.concepts],
        }
        state["integrity_digest"] = _digest(state)
        return state

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> "SemanticMemory":
        if state.get("schema_version") != SEMANTIC_SCHEMA_VERSION:
            raise SemanticMemoryError("unsupported semantic memory schema")
        if state.get("owner") != SEMANTIC_OWNER or state.get("integrity_digest") != _digest(
            state
        ):
            raise SemanticMemoryError("semantic memory integrity check failed")
        memory = cls(
            max_concepts=int(state["max_concepts"]),
            min_episode_support=int(state["min_episode_support"]),
            prototype_support=float(state["prototype_support"]),
            match_threshold=float(state["match_threshold"]),
        )
        next_concept_id = state.get("next_concept_id")
        if type(next_concept_id) is not int or next_concept_id <= 0:
            raise SemanticMemoryError("invalid next concept identifier")
        raw_concepts = state.get("concepts")
        if not isinstance(raw_concepts, list):
            raise SemanticMemoryError("concepts must be a list")
        for raw in cast(list[object], raw_concepts):
            if not isinstance(raw, dict):
                raise SemanticMemoryError("concept entry must be an object")
            item = cast(dict[str, Any], raw)
            raw_support = item.get("neuron_episode_support")
            raw_episodes = item.get("episode_ids")
            if not isinstance(raw_support, dict) or not isinstance(raw_episodes, list):
                raise SemanticMemoryError("invalid semantic support data")
            episode_ids = {str(value) for value in cast(list[object], raw_episodes)}
            support: dict[int, int] = {}
            for key, value in cast(dict[object, object], raw_support).items():
                neuron_id = int(str(key))
                if type(value) is not int or value <= 0:
                    raise SemanticMemoryError("semantic support must be positive")
                support[neuron_id] = value
            concept = _MutableConcept(
                concept_id=int(item["concept_id"]),
                sensor_id=str(item["sensor_id"]),
                modality=str(item["modality"]),
                episode_ids=episode_ids,
                support=support,
            )
            frozen = memory._frozen(concept)
            expected_prototype = spike_ids_from_result(
                {"spike_ids": item.get("prototype_spike_ids")}
            )
            if frozen.prototype_spike_ids != expected_prototype:
                raise SemanticMemoryError("semantic prototype is inconsistent")
            memory._concepts.append(concept)
        if len(memory._concepts) > memory.max_concepts:
            raise SemanticMemoryError("stored concepts exceed configured capacity")
        ids = [item.concept_id for item in memory._concepts]
        if len(ids) != len(set(ids)) or any(value <= 0 for value in ids):
            raise SemanticMemoryError("semantic concept identifiers are invalid")
        if ids and next_concept_id <= max(ids):
            raise SemanticMemoryError("next concept identifier is stale")
        memory._next_concept_id = next_concept_id
        return memory


__all__ = [
    "SemanticConcept",
    "SemanticMatch",
    "SemanticMemory",
    "SemanticMemoryError",
]
