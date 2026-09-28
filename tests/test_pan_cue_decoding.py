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
