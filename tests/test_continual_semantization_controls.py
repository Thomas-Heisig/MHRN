from __future__ import annotations

from collections import Counter

import pytest

from src.memory import NeuralEpisode, SemanticMemory
from src.research.continual_semantization_controls import (
    CL002Config,
    CL002SeedResult,
    CONDITIONS,
    ReplayObject,
    SEEDS,
    condition_order,
    random_objects_matching_semantic,
    raw_objects_for_task,
    replay_schedule,
    require_execution_authorized,
    semantic_objects_for_task,
    summarize_confirmatory,
)


def _episode(index: int, label: int, spikes: tuple[int, ...]) -> NeuralEpisode:
    return NeuralEpisode(
        run_id="synthetic-cl002",
        episode_id=f"episode-{label}-{index}",
        tick=index,
        sensor_id=f"split-mnist-label-{label}",
        modality="pooled_rate_code",
        spike_ids=spikes,
        frame_payload={"synthetic": True},
        actual_state=None,
    )


def _result(
    seed: int,
    condition: str,
    *,
    accuracy: float,
    forgetting: float,
    aborted: bool = False,
) -> CL002SeedResult:
    return CL002SeedResult(
        seed=seed,
        condition=condition,
        task_accuracy_matrix=(),
        final_average_accuracy=accuracy,
        mean_forgetting=forgetting,
        current_task_updates=10_000,
        replay_updates=0 if condition == "B1_naive_online" else 400,
        stored_by_task=(0, 0, 0, 0, 0),
        aborted=aborted,
        abort_reason="synthetic abort" if aborted else None,
    )


def test_execution_is_blocked_until_preregistration_authorizes_it() -> None:
    with pytest.raises(RuntimeError, match="not authorized"):
        require_execution_authorized(
            {"experiment_id": "EXP-S6-SEM-CL-002", "execution_authorized": False}
        )


def test_condition_order_is_deterministic_seeded_permutation() -> None:
    first = condition_order(201)
    second = condition_order(201)
    assert first == second
    assert set(first) == set(CONDITIONS)
    assert len(first) == len(CONDITIONS)


def test_semantic_prototype_uses_existing_mhrn_support_rule() -> None:
    memory = SemanticMemory(
        max_concepts=128,
        min_episode_support=8,
        prototype_support=0.30,
        match_threshold=0.25,
    )
    memory.consolidate(
        [_episode(i, 0, (1, 2, 3)) for i in range(8)]
        + [_episode(100 + i, 1, (4, 5, 6)) for i in range(8)]
    )
    objects = semantic_objects_for_task(
        memory,
        task_index=0,
        labels=(0, 1),
        capacity=50,
    )
    assert [item.label for item in objects] == [0, 1]
    assert objects[0].spike_ids == (1, 2, 3)
    assert objects[1].spike_ids == (4, 5, 6)


def test_realized_raw_budget_matches_semantic_count_without_replacement() -> None:
    encoded = [
        (9, (9,), 1),
        (2, (2,), 0),
        (7, (7,), 1),
        (4, (4,), 0),
    ]
    raw = raw_objects_for_task(encoded, task_index=0, realized_count=2)
    assert len(raw) == 2
    assert [item.spike_ids for item in raw] == [(2,), (4,)]


def test_random_control_matches_semantic_objectwise_but_not_spike_identity() -> None:
    semantic = (
        ReplayObject(task_index=2, label=4, spike_ids=(1, 2, 3, 4), source_rank=0),
        ReplayObject(task_index=2, label=5, spike_ids=(5, 6), source_rank=1),
    )
    first = random_objects_matching_semantic(semantic, seed=203, feature_count=196)
    second = random_objects_matching_semantic(semantic, seed=203, feature_count=196)
    assert first == second
    assert [(item.task_index, item.label) for item in first] == [(2, 4), (2, 5)]
    assert [len(item.spike_ids) for item in first] == [4, 2]
    assert all(len(set(item.spike_ids)) == len(item.spike_ids) for item in first)
    assert all(0 <= spike < 196 for item in first for spike in item.spike_ids)
    assert first != semantic


def test_replay_schedule_is_exactly_100_and_balanced() -> None:
    pool = tuple(
        ReplayObject(task_index=0, label=i % 2, spike_ids=(i,), source_rank=i)
        for i in range(7)
    )
    schedule = replay_schedule(pool, updates=100)
    assert len(schedule) == 100
    counts = Counter(item.source_rank for item in schedule)
    assert max(counts.values()) - min(counts.values()) <= 1


def test_config_freezes_cl001_encoder_and_cl002_budgets() -> None:
    config = CL002Config()
    encoder = config.encoder
    assert config.seeds == SEEDS
    assert config.capacity_per_task == 50
    assert config.replay_updates_per_transition == 100
    assert encoder.semantic_min_episode_support == 8
    assert encoder.semantic_prototype_support == 0.30
    assert encoder.semantic_match_threshold == 0.25


def test_confirmatory_rule_passes_only_when_all_three_contrasts_pass() -> None:
    results: list[CL002SeedResult] = []
    for seed in SEEDS:
        results.extend(
            [
                _result(seed, "B1_naive_online", accuracy=0.20, forgetting=0.90),
                _result(seed, "B2_raw_replay", accuracy=0.50, forgetting=0.50),
                _result(seed, "B3_semantic_prototype", accuracy=0.60, forgetting=0.30),
                _result(seed, "B4_random_prototype", accuracy=0.50, forgetting=0.55),
            ]
        )
    summary = summarize_confirmatory(results)
    assert summary["complete_paired_seed_count"] == 9
    assert summary["preregistered_positive_semantic_effect"] is True
    assert summary["result_classification"] == "preregistered_positive_semantic_effect"
    assert all(item["passed"] for item in summary["contrasts"].values())
    assert summary["automatic_evidence_promotion"] is False
    assert summary["scientific_evidence"] is False


def test_any_unresolved_aborted_seed_precludes_positive_confirmatory_result() -> None:
    results: list[CL002SeedResult] = []
    for seed in SEEDS:
        for condition in CONDITIONS:
            results.append(
                _result(
                    seed,
                    condition,
                    accuracy=0.60 if condition == "B3_semantic_prototype" else 0.50,
                    forgetting=0.30 if condition == "B3_semantic_prototype" else 0.50,
                    aborted=seed == 209 and condition == "B4_random_prototype",
                )
            )
    summary = summarize_confirmatory(results)
    assert summary["complete_paired_seed_count"] == 8
    assert summary["preregistered_positive_semantic_effect"] is False
    assert summary["result_classification"] == "incomplete_preregistered_run"
