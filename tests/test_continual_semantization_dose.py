from __future__ import annotations

from collections import Counter

import pytest

from src.research.continual_semantization_controls import ReplayObject
from src.research.continual_semantization_dose import (
    CONDITIONS,
    SEEDS,
    CL003Config,
    CL003SeedResult,
    balanced_replay_sequence,
    condition_order,
    replay_slot_mask,
    require_execution_authorized,
    summarize_confirmatory,
)


def _result(
    seed: int,
    condition: str,
    *,
    accuracy: float,
    forgetting: float,
    aborted: bool = False,
) -> CL003SeedResult:
    replay = {
        "R05": 400,
        "S05": 400,
        "R20": 1600,
        "S20": 1600,
        "X20": 1600,
        "R40": 3200,
        "S40": 3200,
    }[condition]
    return CL003SeedResult(
        seed=seed,
        condition=condition,
        task_accuracy_matrix=(),
        final_average_accuracy=accuracy,
        mean_forgetting=forgetting,
        current_task_updates=10_000 - replay,
        replay_updates=replay,
        total_updates=10_000,
        stored_by_task=(3, 3, 3, 3, 3),
        aborted=aborted,
        abort_reason="synthetic abort" if aborted else None,
    )


def test_execution_blocked_before_authorization() -> None:
    with pytest.raises(RuntimeError, match="not authorized"):
        require_execution_authorized(
            {"experiment_id": "EXP-S6-SEM-CL-003", "execution_authorized": False}
        )


def test_replay_slot_masks_have_exact_unique_counts_and_are_spread() -> None:
    for count in (100, 400, 800):
        mask = replay_slot_mask(2000, count)
        assert len(mask) == count
        assert len(set(mask)) == count
        assert mask == tuple(sorted(mask))
        assert min(mask) >= 0
        assert max(mask) < 2000
        gaps = [right - left for left, right in zip(mask, mask[1:])]
        assert max(gaps) - min(gaps) <= 1


def test_same_dose_conditions_share_identical_slot_mask() -> None:
    assert replay_slot_mask(2000, 100) == replay_slot_mask(2000, 100)
    assert replay_slot_mask(2000, 400) == replay_slot_mask(2000, 400)
    assert replay_slot_mask(2000, 800) == replay_slot_mask(2000, 800)


def test_condition_order_is_deterministic_permutation() -> None:
    first = condition_order(301)
    second = condition_order(301)
    assert first == second
    assert set(first) == set(CONDITIONS)
    assert len(first) == 7


def test_balanced_replay_sequence_uses_objects_with_max_difference_one() -> None:
    objects = tuple(
        ReplayObject(
            task_index=0, label=index % 2, spike_ids=(index,), source_rank=index
        )
        for index in range(7)
    )
    schedule = balanced_replay_sequence(objects, 400)
    counts = Counter(item.source_rank for item in schedule)
    assert len(schedule) == 400
    assert max(counts.values()) - min(counts.values()) <= 1


def test_default_config_freezes_new_seeds_and_constant_budget_inputs() -> None:
    config = CL003Config()
    assert config.seeds == SEEDS
    assert config.train_per_class == 1000
    assert config.test_per_class == 200
    assert config.encoder.semantic_min_episode_support == 8
    assert config.encoder.semantic_prototype_support == 0.30
    assert config.encoder.semantic_match_threshold == 0.25


def test_h1_and_h2_can_pass_on_known_synthetic_effects() -> None:
    results: list[CL003SeedResult] = []
    for seed in SEEDS:
        values = {
            "R05": (0.50, 0.50),
            "S05": (0.505, 0.49),
            "R20": (0.50, 0.50),
            "S20": (0.57, 0.40),
            "X20": (0.51, 0.52),
            "R40": (0.53, 0.46),
            "S40": (0.56, 0.42),
        }
        for condition, (accuracy, forgetting) in values.items():
            results.append(
                _result(
                    seed,
                    condition,
                    accuracy=accuracy,
                    forgetting=forgetting,
                )
            )
    summary = summarize_confirmatory(results)
    assert summary["complete_paired_seed_count"] == 12
    assert summary["H1_passed"] is True
    assert summary["H2_passed"] is True
    assert summary["result_classification"] == "H1_positive_H2_positive"
    assert summary["automatic_evidence_promotion"] is False
    assert summary["scientific_evidence"] is False


def test_h1_negative_h2_negative_on_equal_synthetic_conditions() -> None:
    results: list[CL003SeedResult] = []
    for seed in SEEDS:
        for condition in CONDITIONS:
            results.append(_result(seed, condition, accuracy=0.50, forgetting=0.50))
    summary = summarize_confirmatory(results)
    assert summary["H1_passed"] is False
    assert summary["H2_passed"] is False
    assert summary["result_classification"] == "H1_negative_H2_negative"


def test_any_aborted_condition_makes_run_incomplete() -> None:
    results: list[CL003SeedResult] = []
    for seed in SEEDS:
        for condition in CONDITIONS:
            results.append(
                _result(
                    seed,
                    condition,
                    accuracy=0.5,
                    forgetting=0.5,
                    aborted=seed == 312 and condition == "S40",
                )
            )
    summary = summarize_confirmatory(results)
    assert summary["complete_paired_seed_count"] == 11
    assert summary["H1_passed"] is False
    assert summary["H2_passed"] is False
    assert summary["result_classification"] == "incomplete_preregistered_run"
