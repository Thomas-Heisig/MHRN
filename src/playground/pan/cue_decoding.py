"""Held-out activity decoding; labels are used only by this offline probe."""

from __future__ import annotations

import math
import random
from collections import Counter


def decode_cues(
    features: list[list[float]],
    labels: list[int],
    *,
    seed: int = 12345,
    policy_feedback: bool = False,
    train_episodes: int | None = None,
) -> dict[str, object]:
    """Fit centroids on early complete episodes and score later episodes.

    No episode, label or explicit policy value is included in the features.
    This measures decodability, not acquisition of representations or cognition.
    """
    base: dict[str, object] = {
        "classification": "EXPLORATORY_ACTIVITY_CUE_PROBE",
        "scientific_evidence": False,
        "split": "chronological_complete_episodes",
        "feature_source": "neuron_spike_counts",
        "policy_feedback_confound": policy_feedback,
        "neural_learning_demonstrated": False,
        "transfer_status": "NOT_MEASURED_REQUIRES_TRAINED_NETWORK_CHECKPOINT",
        "randomized_cue_status": "LABEL_PERMUTATION_ONLY_NOT_INPUT_INTERVENTION",
    }
    if (
        len(features) != len(labels)
        or len(features) < 8
        or not features
        or not features[0]
        or any(len(row) != len(features[0]) for row in features)
        or any(not math.isfinite(value) for row in features for value in row)
    ):
        return {**base, "status": "INSUFFICIENT_OR_INVALID_EPISODES"}
    split = len(features) * 2 // 3 if train_episodes is None else train_episodes
    if type(split) is not int or not 1 <= split < len(features):
        return {**base, "status": "INVALID_TRAIN_TEST_SPLIT"}
    train, test = features[:split], features[split:]
    train_labels, test_labels = labels[:split], labels[split:]
    classes = sorted(set(labels))
    if len(features) * len(features[0]) * len(classes) * 64 > 8_000_000:
        return {**base, "status": "PROBE_BUDGET_EXCEEDED"}
    if len(classes) < 2 or set(train_labels) != set(test_labels):
        return {**base, "status": "INSUFFICIENT_CLASS_COVERAGE"}

    def predictions(training_labels: list[int]) -> list[int]:
        counts = Counter(training_labels)
        centroids = {label: [0.0] * len(features[0]) for label in classes}
        for row, label in zip(train, training_labels):
            for index, value in enumerate(row):
                centroids[label][index] += value / counts[label]
        return [
            min(
                classes,
                key=lambda label: sum(
                    (value - center) ** 2
                    for value, center in zip(row, centroids[label])
                ),
            )
            for row in test
        ]

    predicted = predictions(train_labels)
    accuracy = sum(a == b for a, b in zip(predicted, test_labels)) / len(test)
    rng = random.Random(seed ^ 0xDEC0DE)
    null_scores: list[float] = []
    for _ in range(64):
        shuffled = list(train_labels)
        rng.shuffle(shuffled)
        null_scores.append(
            sum(a == b for a, b in zip(predictions(shuffled), test_labels)) / len(test)
        )
    majority = max(Counter(train_labels), key=lambda label: train_labels.count(label))
    return {
        **base,
        "status": "DESCRIPTIVE_ONLY",
        "train_episodes": len(train),
        "test_episodes": len(test),
        "classes": classes,
        "accuracy": accuracy,
        "majority_baseline": test_labels.count(majority) / len(test),
        "uniform_chance": 1 / len(classes),
        "predictions": predicted,
        "test_labels": test_labels,
        "permutations": len(null_scores),
        "permuted_label_accuracy_mean": sum(null_scores) / len(null_scores),
        "permutation_tail_fraction": (1 + sum(x >= accuracy for x in null_scores))
        / (1 + len(null_scores)),
    }
