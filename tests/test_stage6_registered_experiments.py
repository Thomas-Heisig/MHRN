from __future__ import annotations

from src.research.stage6_experiments import (
    run_s6_epi_001,
    run_s6_pe_001,
    run_s6_rpl_001,
    run_s6_sem_001,
    run_s6_wm_001,
    run_s6_wm_002,
)


def _by_condition(runs: list[object], condition: str) -> object:
    return next(run for run in runs if getattr(run, "condition") == condition)


def test_s6_epi_001_uses_snn_and_never_reads_answer_payload() -> None:
    runs = run_s6_epi_001({}, (101,))
    assert len(runs) == 4
    assert {run.condition for run in runs} == {
        "intact",
        "read_off",
        "write_off",
        "episode_shuffle",
    }
    for run in runs:
        assert run.metrics["snn_involved"] is True
        assert run.metrics["target_in_memory_payload"] is False
        assert run.metrics["answer_reads_payload"] is False
        assert run.metrics["answer_reads_actual_state"] is False
        assert run.metrics["scientific_evidence"] is False
        assert run.metrics["distractor_spikes"] > 0
    assert _by_condition(runs, "write_off").metrics["stored_episodes"] == 0  # type: ignore[attr-defined]


def test_s6_epi_001_is_deterministic_for_same_seed() -> None:
    first = run_s6_epi_001({}, (103,))
    second = run_s6_epi_001({}, (103,))
    assert first == second


def test_s6_sem_001_uses_disjoint_held_out_episodes() -> None:
    runs = run_s6_sem_001({}, (101,))
    assert len(runs) == 3
    for run in runs:
        assert run.metrics["train_eval_episode_overlap"] == 0
        assert run.metrics["held_out"] is True
        assert run.metrics["snn_involved"] is True
        assert run.metrics["scientific_evidence"] is False
    assert _by_condition(runs, "no_semantic").metrics["semantic_updates"] == 0  # type: ignore[attr-defined]


def test_s6_replay_has_equal_snn_step_budget_and_controls() -> None:
    runs = run_s6_rpl_001({}, (101,))
    assert len(runs) == 4
    assert {run.condition for run in runs} == {
        "no_replay",
        "ordered",
        "shuffled",
        "equal_budget_awake",
    }
    for run in runs:
        assert run.metrics["budget_matched"] is True
        assert run.metrics["snn_steps_used"] == run.metrics["snn_step_budget"]
        assert run.metrics["snn_involved"] is True
        assert run.metrics["simulated_sleep_claim"] is False


def test_s6_prediction_error_is_factorial_and_reward_separate() -> None:
    runs = run_s6_pe_001({}, (101,))
    assert len(runs) == 6
    conditions = {run.condition for run in runs}
    for pe_mode in ("correct", "disabled", "shuffled"):
        assert f"pe_{pe_mode}__reward_on" in conditions
        assert f"pe_{pe_mode}__reward_off" in conditions
    for run in runs:
        assert run.metrics["reward_path_called_by_pe"] is False
        expected_calls = 1 if run.metrics["reward_on"] else 0
        assert run.metrics["reward_calls"] == expected_calls
        assert run.metrics["snn_involved"] is True


def test_s6_multistep_world_model_is_frozen_and_controlled() -> None:
    runs = run_s6_wm_001({}, (101,))
    assert len(runs) == 4
    assert {run.condition for run in runs} == {
        "frozen_correct",
        "frozen_shuffled",
        "persistence",
        "no_model",
    }
    for run in runs:
        assert run.metrics["frozen_during_evaluation"] is True
        assert run.metrics["scientific_evidence"] is False
    correct = _by_condition(runs, "frozen_correct")
    assert correct.state_digest_before == correct.state_digest_after  # type: ignore[attr-defined]
    assert correct.metrics["exact_final_state_rate"] == 1.0  # type: ignore[attr-defined]


def test_s6_offline_decision_benefit_has_no_actuation_authority() -> None:
    runs = run_s6_wm_002({}, (101,))
    assert len(runs) == 4
    for run in runs:
        assert run.metrics["actuation_authority"] is False
        assert run.metrics["frozen_during_evaluation"] is True
        assert run.metrics["scientific_evidence"] is False
    correct = _by_condition(runs, "correct")
    shuffled = _by_condition(runs, "shuffled")
    assert correct.metrics["utility_ratio"] == 1.0  # type: ignore[attr-defined]
    assert shuffled.metrics["utility_ratio"] < correct.metrics["utility_ratio"]  # type: ignore[attr-defined]
