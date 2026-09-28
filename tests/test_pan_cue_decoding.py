"""Offline probes must separate activity information from learning claims."""

import random

from src.playground.pan.cue_decoding import decode_cues


def test_activity_only_probe_recovers_held_out_code_and_reports_controls() -> None:
    labels = [i % 4 for i in range(120)]
    features = [[float(i == label) for i in range(4)] for label in labels]
    result = decode_cues(features, labels, policy_feedback=True)
    assert result["accuracy"] == 1
    assert result["permuted_label_accuracy_mean"] < 0.4
    assert result["policy_feedback_confound"] is True
    assert result["neural_learning_demonstrated"] is False
    assert result["train_episodes"] + result["test_episodes"] == 120


def test_randomized_cue_and_absent_activity_do_not_decode_target() -> None:
    labels = [i % 4 for i in range(240)]
    rng = random.Random(17)
    random_cues = [rng.randrange(4) for _ in labels]
    features = [[float(i == cue) for i in range(4)] for cue in random_cues]
    assert decode_cues(features, labels)["accuracy"] < 0.4
    assert decode_cues([[0.0] * 4 for _ in labels], labels)["accuracy"] == 0.25


def test_missing_classes_empty_and_nonfinite_fail_closed() -> None:
    for features, labels in [
        ([], []),
        ([[float("nan")]] * 12, [0, 1] * 6),
        ([[1.0]] * 12, [0] * 8 + [1] * 4),
    ]:
        result = decode_cues(features, labels)
        assert "accuracy" not in result


def test_randomized_input_preserves_evaluator_targets_and_changes_emitted_cue() -> None:
    from src.playground.closed_loop import ClosedLoopRuntime
    from src.playground.models import PlaygroundConfig

    aligned = ClosedLoopRuntime(
        PlaygroundConfig.from_mapping({"closed_loop_preset": "pan_full_balanced"}), []
    )
    randomized = ClosedLoopRuntime(
        PlaygroundConfig.from_mapping(
            {
                "closed_loop_preset": "pan_full_balanced",
                "target_cue_control": "randomized",
            }
        ),
        [],
    )
    absent = ClosedLoopRuntime(
        PlaygroundConfig.from_mapping(
            {"closed_loop_preset": "pan_full_balanced", "target_cue_control": "absent"}
        ),
        [],
    )
    changed = 0
    for episode in range(100):
        tick = episode * 64
        assert (
            aligned.current_target(tick)
            == randomized.current_target(tick)
            == absent.current_target(tick)
        )
        a, r = aligned._target_channel_values(tick), randomized._target_channel_values(
            tick
        )
        changed += a != r
        assert sum(absent._target_channel_values(tick)) == 0
        assert sum(a) == sum(r)
    assert 55 < changed < 95


def test_matched_six_condition_suite_has_no_explicit_policy_current() -> None:
    from src.playground.pan.cue_controls import run_cue_controls

    result = run_cue_controls(
        {
            "closed_loop_preset": "pan_full_balanced",
            "n_neurons": 32,
            "edge_budget": 64,
            "ticks": 256,
            "behavior_episode_ticks": 8,
            "persist": False,
        }
    )
    assert len(result["conditions"]) == 6
    assert result["neural_learning_claim"] is False
    for condition in result["conditions"]:
        assert condition["probe"]["policy_feedback_confound"] is False
        assert condition["probe"]["input_cue_control"] == condition["input_cue_control"]
    targets = [row["target_history"] for row in result["conditions"]]
    assert all(target == targets[0] for target in targets)
