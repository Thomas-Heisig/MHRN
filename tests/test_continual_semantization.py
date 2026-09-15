from __future__ import annotations

import numpy as np

from src.research.continual_semantization import (
    MnistBundle,
    SeedResult,
    SplitMnistConfig,
    image_to_spike_ids,
    run_split_mnist_semantization,
    summarize_results,
)


def _synthetic_bundle(train_per_label: int = 4, test_per_label: int = 2) -> MnistBundle:
    train_images: list[np.ndarray] = []
    train_labels: list[int] = []
    test_images: list[np.ndarray] = []
    test_labels: list[int] = []
    for label in range(10):
        row = (label // 5) * 12 + 2
        col = (label % 5) * 5 + 1
        for offset in range(train_per_label):
            image = np.zeros((28, 28), dtype=np.uint8)
            image[row : row + 4, col : col + 4] = 255
            image[(row + offset) % 28, (col + offset) % 28] = 180
            train_images.append(image)
            train_labels.append(label)
        for offset in range(test_per_label):
            image = np.zeros((28, 28), dtype=np.uint8)
            image[row : row + 4, col : col + 4] = 255
            image[(row + offset + 1) % 28, (col + offset + 1) % 28] = 180
            test_images.append(image)
            test_labels.append(label)
    return MnistBundle(
        train_images=np.stack(train_images),
        train_labels=np.asarray(train_labels, dtype=np.uint8),
        test_images=np.stack(test_images),
        test_labels=np.asarray(test_labels, dtype=np.uint8),
        source_sha256={"synthetic": "unit-test"},
    )


def test_rate_code_is_deterministic_and_bounded() -> None:
    config = SplitMnistConfig(train_per_class=1, test_per_class=1, seeds=(1,))
    image = np.zeros((28, 28), dtype=np.uint8)
    image[0:4, 0:4] = 255
    first = image_to_spike_ids(image, config)
    second = image_to_spike_ids(image.copy(), config)
    assert first == second
    assert first
    assert max(first) < config.feature_count


def test_paired_conditions_use_equal_readout_update_budget() -> None:
    config = SplitMnistConfig(
        train_per_class=4,
        test_per_class=2,
        seeds=(7, 11),
        replay_fraction=0.25,
        semantic_min_episode_support=2,
        semantic_prototype_support=0.5,
        semantic_match_threshold=0.1,
        bootstrap_samples=100,
    )
    result = run_split_mnist_semantization(_synthetic_bundle(), config)
    by_seed: dict[int, dict[str, dict[str, object]]] = {}
    for run in result["runs"]:
        by_seed.setdefault(int(run["seed"]), {})[str(run["condition"])] = run
    assert set(by_seed) == {7, 11}
    for pair in by_seed.values():
        assert (
            pair["baseline"]["update_count"] == pair["semantic_replay"]["update_count"]
        )
        assert int(pair["semantic_replay"]["replay_update_count"]) > 0
    assert result["summary"]["automatic_evidence_promotion"] is False
    assert result["summary"]["human_review_required"] is True


def test_preregistered_decision_rule_requires_both_endpoints() -> None:
    config = SplitMnistConfig(seeds=(1, 2, 3, 4, 5, 6), bootstrap_samples=500)
    baseline = [
        SeedResult(seed, "baseline", (), 0.50, 0.30, 10, 0, 0, 0)
        for seed in config.seeds
    ]
    semantic = [
        SeedResult(seed, "semantic_replay", (), 0.56, 0.20, 10, 2, 2, 4)
        for seed in config.seeds
    ]
    summary = summarize_results(baseline, semantic, config)
    assert summary["accuracy_delta_mean"] > 0.03
    assert summary["forgetting_reduction_mean"] > 0.05
    assert summary["preregistered_primary_success"] is True
