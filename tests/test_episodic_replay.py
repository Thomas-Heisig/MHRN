from __future__ import annotations

from src.memory.episodic_replay import (
    EpisodicReplayScheduler,
    ReplayMode,
    consolidate_replay,
)
from src.memory.neural_episodic import NeuralEpisode
from src.memory.semantic import SemanticMemory


def _episode(episode_id: str, tick: int, spikes: tuple[int, ...]) -> NeuralEpisode:
    return NeuralEpisode(
        run_id="replay-run",
        episode_id=episode_id,
        tick=tick,
        sensor_id="camera",
        modality="vision",
        spike_ids=spikes,
        frame_payload={"cue": episode_id},
        actual_state={"ok": True},
    )


def _episodes() -> tuple[NeuralEpisode, ...]:
    return (
        _episode("a-1", 3, (1, 2, 3, 8)),
        _episode("a-2", 1, (1, 2, 3, 9)),
        _episode("a-3", 2, (1, 2, 3, 10)),
        _episode("noise", 4, (40, 41, 42)),
    )


def test_off_replay_consumes_no_budget_and_causes_no_semantic_updates() -> None:
    scheduler = EpisodicReplayScheduler(max_events=4)
    plan = scheduler.plan(_episodes(), mode=ReplayMode.OFF, budget=4, seed=7)
    semantic = SemanticMemory(min_episode_support=3)

    result = consolidate_replay(semantic, plan)

    assert plan.used_budget == 0
    assert result.semantic_updates == 0
    assert semantic.concepts == ()


def test_ordered_replay_is_tick_deterministic_and_budget_bounded() -> None:
    scheduler = EpisodicReplayScheduler(max_events=2)
    source = _episodes()
    plan = scheduler.plan(source, mode=ReplayMode.ORDERED, budget=99, seed=123)

    assert [item.tick for item in plan.selected] == [1, 2]
    assert plan.used_budget == 2
    assert source == _episodes()


def test_shuffled_replay_is_seeded_and_changes_order_without_changing_members() -> None:
    scheduler = EpisodicReplayScheduler(max_events=4)
    source = _episodes()
    first = scheduler.plan(source, mode=ReplayMode.SHUFFLED, budget=4, seed=11)
    second = scheduler.plan(source, mode=ReplayMode.SHUFFLED, budget=4, seed=11)
    other = scheduler.plan(source, mode=ReplayMode.SHUFFLED, budget=4, seed=12)

    assert first.selected == second.selected
    assert first.source_digest == second.source_digest == other.source_digest
    assert set(item.episode_id for item in first.selected) == set(
        item.episode_id for item in source
    )
    assert first.selected != other.selected


def test_duplicate_traces_from_same_episode_do_not_inflate_replay_budget() -> None:
    scheduler = EpisodicReplayScheduler(max_events=8)
    source = (
        _episode("same", 1, (1, 2)),
        _episode("same", 2, (2, 3)),
        _episode("other", 3, (1, 2, 3)),
    )

    plan = scheduler.plan(source, mode=ReplayMode.ORDERED, budget=8)

    assert [item.episode_id for item in plan.selected] == ["same", "other"]
    assert plan.used_budget == 2


def test_replay_can_form_semantic_concept_only_when_independent_support_is_replayed(
) -> None:
    scheduler = EpisodicReplayScheduler(max_events=4)
    semantic = SemanticMemory(
        min_episode_support=3,
        prototype_support=2 / 3,
        match_threshold=0.5,
    )

    partial = scheduler.plan(_episodes(), mode=ReplayMode.ORDERED, budget=2)
    partial_result = consolidate_replay(semantic, partial)
    assert partial_result.mature_concepts_after == 0

    full = scheduler.plan(_episodes(), mode=ReplayMode.ORDERED, budget=4)
    full_result = consolidate_replay(semantic, full)
    assert full_result.semantic_updates == 2
    assert full_result.mature_concepts_after == 1
    assert semantic.mature_concepts[0].prototype_spike_ids == (1, 2, 3)
