"""Bounded deterministic replay plans for Stage-6 consolidation experiments.

Replay here means re-selection of previously recorded neural episodes for an
explicit consolidation consumer. It is not simulated sleep, does not directly
inject spikes into the running network, and does not modify rewards or actions.
The scheduler is deliberately separable so ordered, shuffled and disabled
conditions can be compared with matched budgets.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from enum import StrEnum

from .neural_episodic import NeuralEpisode
from .semantic import SemanticMemory


class ReplayMode(StrEnum):
    OFF = "off"
    ORDERED = "ordered"
    SHUFFLED = "shuffled"


class EpisodicReplayError(ValueError):
    """Raised when a replay plan violates its bounded contract."""


@dataclass(frozen=True, slots=True)
class ReplayPlan:
    """Immutable selection of unique episode/context contributions."""

    mode: ReplayMode
    seed: int
    requested_budget: int
    selected: tuple[NeuralEpisode, ...]
    source_digest: str

    @property
    def used_budget(self) -> int:
        return len(self.selected)


@dataclass(frozen=True, slots=True)
class ReplayConsolidationResult:
    plan: ReplayPlan
    semantic_updates: int
    mature_concepts_before: int
    mature_concepts_after: int


def _episode_key(episode: NeuralEpisode) -> tuple[str, str, str]:
    return (episode.episode_id, episode.sensor_id, episode.modality)


def _source_digest(episodes: tuple[NeuralEpisode, ...]) -> str:
    payload = [episode.to_dict() for episode in episodes]
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


class EpisodicReplayScheduler:
    """Create bounded replay plans without mutating the episodic source."""

    def __init__(self, *, max_events: int = 64) -> None:
        if type(max_events) is not int or max_events <= 0:
            raise EpisodicReplayError("max_events must be a positive integer")
        self.max_events = max_events

    def plan(
        self,
        episodes: tuple[NeuralEpisode, ...],
        *,
        mode: ReplayMode | str,
        budget: int,
        seed: int = 0,
    ) -> ReplayPlan:
        if type(budget) is not int or budget < 0:
            raise EpisodicReplayError("budget must be a non-negative integer")
        if type(seed) is not int:
            raise EpisodicReplayError("seed must be an integer")
        try:
            replay_mode = ReplayMode(mode)
        except ValueError as error:
            raise EpisodicReplayError("unsupported replay mode") from error
        effective_budget = min(budget, self.max_events)

        # Semantic support counts independent episode/context contributions. A
        # repeated trace from the same episode/context must not consume replay
        # budget or inflate semantic evidence.
        unique: dict[tuple[str, str, str], NeuralEpisode] = {}
        for episode in sorted(
            episodes,
            key=lambda item: (
                item.tick,
                item.episode_id,
                item.sensor_id,
                item.modality,
            ),
        ):
            unique.setdefault(_episode_key(episode), episode)
        candidates = list(unique.values())

        if replay_mode is ReplayMode.OFF or effective_budget == 0:
            selected: tuple[NeuralEpisode, ...] = ()
        elif replay_mode is ReplayMode.ORDERED:
            selected = tuple(candidates[:effective_budget])
        else:
            rng = random.Random(seed)
            rng.shuffle(candidates)
            selected = tuple(candidates[:effective_budget])

        return ReplayPlan(
            mode=replay_mode,
            seed=seed,
            requested_budget=budget,
            selected=selected,
            source_digest=_source_digest(episodes),
        )


def consolidate_replay(
    semantic_memory: SemanticMemory,
    plan: ReplayPlan,
) -> ReplayConsolidationResult:
    """Apply exactly the selected replay plan to semantic consolidation."""

    before = len(semantic_memory.mature_concepts)
    updates = semantic_memory.consolidate(plan.selected)
    after = len(semantic_memory.mature_concepts)
    return ReplayConsolidationResult(
        plan=plan,
        semantic_updates=updates,
        mature_concepts_before=before,
        mature_concepts_after=after,
    )


__all__ = [
    "EpisodicReplayError",
    "EpisodicReplayScheduler",
    "ReplayConsolidationResult",
    "ReplayMode",
    "ReplayPlan",
    "consolidate_replay",
]
