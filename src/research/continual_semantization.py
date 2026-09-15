"""Bounded Split-MNIST continual-learning probe for MHRN semantic consolidation.

This module intentionally isolates one mechanism: semantic prototype consolidation
via :class:`src.memory.semantic.SemanticMemory`. The comparison uses an identical
rate-coded spiking input representation and online softmax readout in both
conditions. The treatment replaces a preregistered fraction of current-task
readout updates with replay of mature semantic prototypes from earlier tasks.

The runner produces DATA only. It does not promote a scientific claim without
human review.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import random
import struct
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from src.memory import NeuralEpisode, SemanticMemory

TASKS: tuple[tuple[int, int], ...] = ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9))
MNIST_BASE_URL = "https://storage.googleapis.com/cvdf-datasets/mnist"
MNIST_FILES: dict[str, str] = {
    "train_images": "train-images-idx3-ubyte.gz",
    "train_labels": "train-labels-idx1-ubyte.gz",
    "test_images": "t10k-images-idx3-ubyte.gz",
    "test_labels": "t10k-labels-idx1-ubyte.gz",
}


@dataclass(frozen=True, slots=True)
class SplitMnistConfig:
    """Frozen benchmark parameters used by the preregistered probe."""

    train_per_class: int = 1000
    test_per_class: int = 200
    seeds: tuple[int, ...] = tuple(range(101, 111))
    pooling: int = 4
    thresholds: tuple[float, ...] = (0.2, 0.4, 0.6, 0.8)
    learning_rate: float = 0.025
    replay_fraction: float = 0.20
    semantic_max_concepts: int = 128
    semantic_min_episode_support: int = 8
    semantic_prototype_support: float = 0.30
    semantic_match_threshold: float = 0.25
    effect_threshold_accuracy: float = 0.03
    effect_threshold_forgetting: float = 0.05
    bootstrap_samples: int = 20000

    def __post_init__(self) -> None:
        if self.train_per_class <= 0 or self.test_per_class <= 0:
            raise ValueError("sample counts must be positive")
        if not self.seeds:
            raise ValueError("at least one seed is required")
        if 28 % self.pooling != 0:
            raise ValueError("pooling must divide 28")
        if not self.thresholds or tuple(sorted(self.thresholds)) != self.thresholds:
            raise ValueError("thresholds must be non-empty and sorted")
        if any(not 0.0 < value < 1.0 for value in self.thresholds):
            raise ValueError("thresholds must be in (0, 1)")
        if not 0.0 < self.learning_rate <= 1.0:
            raise ValueError("learning_rate must be in (0, 1]")
        if not 0.0 <= self.replay_fraction < 1.0:
            raise ValueError("replay_fraction must be in [0, 1)")
        if self.bootstrap_samples <= 0:
            raise ValueError("bootstrap_samples must be positive")

    @property
    def pooled_side(self) -> int:
        return 28 // self.pooling

    @property
    def feature_count(self) -> int:
        return self.pooled_side * self.pooled_side * len(self.thresholds)


@dataclass(frozen=True, slots=True)
class MnistBundle:
    train_images: np.ndarray
    train_labels: np.ndarray
    test_images: np.ndarray
    test_labels: np.ndarray
    source_sha256: dict[str, str]


@dataclass(frozen=True, slots=True)
class SeedResult:
    seed: int
    condition: str
    task_accuracy_matrix: tuple[tuple[float | None, ...], ...]
    final_average_accuracy: float
    mean_forgetting: float
    update_count: int
    replay_update_count: int
    semantic_concepts: int
    semantic_prototype_spikes: int


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return
    temporary = target.with_suffix(target.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "MHRN-research/1"})
    with urllib.request.urlopen(request, timeout=120) as response, temporary.open(
        "wb"
    ) as output:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            output.write(chunk)
    temporary.replace(target)


def _read_idx_images(path: Path) -> np.ndarray:
    with gzip.open(path, "rb") as handle:
        header = handle.read(16)
        if len(header) != 16:
            raise ValueError(f"invalid MNIST image header: {path}")
        magic, count, rows, cols = struct.unpack(">IIII", header)
        if magic != 2051 or rows != 28 or cols != 28:
            raise ValueError(f"unexpected MNIST image schema: {path}")
        payload = handle.read()
    expected = count * rows * cols
    if len(payload) != expected:
        raise ValueError(f"truncated MNIST image payload: {path}")
    return np.frombuffer(payload, dtype=np.uint8).reshape(count, rows, cols).copy()


def _read_idx_labels(path: Path) -> np.ndarray:
    with gzip.open(path, "rb") as handle:
        header = handle.read(8)
        if len(header) != 8:
            raise ValueError(f"invalid MNIST label header: {path}")
        magic, count = struct.unpack(">II", header)
        if magic != 2049:
            raise ValueError(f"unexpected MNIST label schema: {path}")
        payload = handle.read()
    if len(payload) != count:
        raise ValueError(f"truncated MNIST label payload: {path}")
    return np.frombuffer(payload, dtype=np.uint8).copy()


def load_mnist(cache_dir: Path) -> MnistBundle:
    """Download/cache canonical MNIST IDX files and return verified arrays."""

    paths: dict[str, Path] = {}
    for key, filename in MNIST_FILES.items():
        path = cache_dir / filename
        _download(f"{MNIST_BASE_URL}/{filename}", path)
        paths[key] = path
    return MnistBundle(
        train_images=_read_idx_images(paths["train_images"]),
        train_labels=_read_idx_labels(paths["train_labels"]),
        test_images=_read_idx_images(paths["test_images"]),
        test_labels=_read_idx_labels(paths["test_labels"]),
        source_sha256={key: _sha256(path) for key, path in paths.items()},
    )


def image_to_spike_ids(image: np.ndarray, config: SplitMnistConfig) -> tuple[int, ...]:
    """Encode one 28x28 image as deterministic pooled rate-code spike channels."""

    array = np.asarray(image, dtype=np.float32)
    if array.shape != (28, 28):
        raise ValueError("MNIST image must be 28x28")
    normalized = array / 255.0
    side = config.pooled_side
    pooled = normalized.reshape(side, config.pooling, side, config.pooling).mean(
        axis=(1, 3)
    )
    bins = len(config.thresholds)
    spikes: list[int] = []
    for pixel_index, value in enumerate(pooled.reshape(-1)):
        amplitude = float(value)
        for threshold_index, threshold in enumerate(config.thresholds):
            if amplitude >= threshold:
                spikes.append(pixel_index * bins + threshold_index)
    return tuple(spikes)


class OnlineSoftmaxReadout:
    """Minimal online readout over sparse spike channels.

    The same readout is used for both conditions. Sequential softmax updates act
    on all output classes and therefore provide a simple catastrophic-forgetting
    baseline without any retention mechanism.
    """

    def __init__(self, feature_count: int, seed: int, learning_rate: float) -> None:
        if feature_count <= 0:
            raise ValueError("feature_count must be positive")
        self.learning_rate = float(learning_rate)
        rng = np.random.default_rng(seed)
        self.weights = rng.normal(0.0, 1e-3, size=(10, feature_count)).astype(
            np.float64
        )
        self.bias = np.zeros(10, dtype=np.float64)
        self.update_count = 0

    def scores(self, spike_ids: Sequence[int]) -> np.ndarray:
        if not spike_ids:
            return self.bias.copy()
        index = np.fromiter(spike_ids, dtype=np.int64)
        return self.weights[:, index].sum(axis=1) + self.bias

    def predict(self, spike_ids: Sequence[int]) -> int:
        return int(np.argmax(self.scores(spike_ids)))

    def update(self, spike_ids: Sequence[int], label: int) -> float:
        scores = self.scores(spike_ids)
        scores -= float(np.max(scores))
        exp = np.exp(scores)
        probabilities = exp / float(np.sum(exp))
        loss = -math.log(max(float(probabilities[label]), 1e-12))
        gradient = probabilities
        gradient[label] -= 1.0
        if spike_ids:
            index = np.fromiter(spike_ids, dtype=np.int64)
            self.weights[:, index] -= self.learning_rate * gradient[:, None]
        self.bias -= self.learning_rate * gradient
        self.update_count += 1
        return loss


def _sample_indices(
    labels: np.ndarray,
    label: int,
    count: int,
    rng: np.random.Generator,
) -> np.ndarray:
    available = np.flatnonzero(labels == label)
    if count > len(available):
        raise ValueError(f"requested {count} examples for label {label}, only {len(available)}")
    selected = rng.choice(available, size=count, replace=False)
    return np.asarray(selected, dtype=np.int64)


def _task_indices(
    labels: np.ndarray,
    pair: tuple[int, int],
    per_class: int,
    rng: np.random.Generator,
) -> np.ndarray:
    joined = np.concatenate(
        [
            _sample_indices(labels, pair[0], per_class, rng),
            _sample_indices(labels, pair[1], per_class, rng),
        ]
    )
    rng.shuffle(joined)
    return joined


def _semantic_label(concept_sensor_id: str) -> int:
    prefix = "split-mnist-label-"
    if not concept_sensor_id.startswith(prefix):
        raise ValueError("unexpected semantic sensor id")
    return int(concept_sensor_id[len(prefix) :])


def _prototype_pool(memory: SemanticMemory) -> tuple[tuple[tuple[int, ...], int], ...]:
    output: list[tuple[tuple[int, ...], int]] = []
    for concept in memory.mature_concepts:
        output.append((concept.prototype_spike_ids, _semantic_label(concept.sensor_id)))
    return tuple(output)


def _episode(
    *,
    seed: int,
    task_index: int,
    sample_index: int,
    label: int,
    spike_ids: tuple[int, ...],
) -> NeuralEpisode:
    return NeuralEpisode(
        run_id=f"split-mnist-sem-{seed}",
        episode_id=f"seed-{seed}-task-{task_index}-sample-{sample_index}",
        tick=task_index * 1_000_000 + sample_index,
        sensor_id=f"split-mnist-label-{label}",
        modality="pooled_rate_code",
        spike_ids=spike_ids,
        frame_payload={"label": label, "task": task_index},
        actual_state=None,
    )


def _evaluate_task(
    readout: OnlineSoftmaxReadout,
    images: np.ndarray,
    labels: np.ndarray,
    indices: np.ndarray,
    config: SplitMnistConfig,
) -> float:
    correct = 0
    for index in indices:
        spikes = image_to_spike_ids(images[int(index)], config)
        correct += int(readout.predict(spikes) == int(labels[int(index)]))
    return correct / len(indices)


def _run_condition(
    data: MnistBundle,
    config: SplitMnistConfig,
    *,
    seed: int,
    condition: str,
) -> SeedResult:
    if condition not in {"baseline", "semantic_replay"}:
        raise ValueError("unsupported condition")
    select_rng = np.random.default_rng(seed)
    schedule_rng = random.Random(seed ^ 0x53454D)
    readout = OnlineSoftmaxReadout(
        config.feature_count,
        seed=seed ^ 0xA11CE,
        learning_rate=config.learning_rate,
    )
    semantic = SemanticMemory(
        max_concepts=config.semantic_max_concepts,
        min_episode_support=config.semantic_min_episode_support,
        prototype_support=config.semantic_prototype_support,
        match_threshold=config.semantic_match_threshold,
    )
    test_sets = [
        _task_indices(
            data.test_labels,
            pair,
            config.test_per_class,
            np.random.default_rng(seed * 1009 + task_index),
        )
        for task_index, pair in enumerate(TASKS)
    ]
    accuracy_rows: list[tuple[float | None, ...]] = []
    replay_updates = 0

    for task_index, pair in enumerate(TASKS):
        train_indices = _task_indices(
            data.train_labels,
            pair,
            config.train_per_class,
            select_rng,
        )
        encoded: list[tuple[int, tuple[int, ...], int]] = []
        episodes: list[NeuralEpisode] = []
        for position, raw_index in enumerate(train_indices):
            index = int(raw_index)
            label = int(data.train_labels[index])
            spikes = image_to_spike_ids(data.train_images[index], config)
            encoded.append((index, spikes, label))
            episodes.append(
                _episode(
                    seed=seed,
                    task_index=task_index,
                    sample_index=position,
                    label=label,
                    spike_ids=spikes,
                )
            )

        prior_prototypes = _prototype_pool(semantic)
        replay_budget = 0
        if condition == "semantic_replay" and prior_prototypes:
            replay_budget = int(round(config.replay_fraction * len(encoded)))
        current_budget = len(encoded) - replay_budget
        current_positions = list(range(len(encoded)))
        schedule_rng.shuffle(current_positions)
        current_positions = current_positions[:current_budget]
        updates: list[tuple[tuple[int, ...], int, bool]] = [
            (encoded[position][1], encoded[position][2], False)
            for position in current_positions
        ]
        if replay_budget:
            for _ in range(replay_budget):
                spikes, label = prior_prototypes[
                    schedule_rng.randrange(len(prior_prototypes))
                ]
                updates.append((spikes, label, True))
        schedule_rng.shuffle(updates)
        if len(updates) != len(encoded):
            raise RuntimeError("readout update budget diverged between conditions")
        for spikes, label, replayed in updates:
            readout.update(spikes, label)
            replay_updates += int(replayed)

        if condition == "semantic_replay":
            semantic.consolidate(episodes)

        row: list[float | None] = []
        for eval_task in range(len(TASKS)):
            if eval_task > task_index:
                row.append(None)
            else:
                row.append(
                    _evaluate_task(
                        readout,
                        data.test_images,
                        data.test_labels,
                        test_sets[eval_task],
                        config,
                    )
                )
        accuracy_rows.append(tuple(row))

    final_row = accuracy_rows[-1]
    final_values = [float(value) for value in final_row if value is not None]
    forgetting_values: list[float] = []
    for task_index in range(len(TASKS) - 1):
        history = [
            float(row[task_index])
            for row in accuracy_rows[task_index:]
            if row[task_index] is not None
        ]
        forgetting_values.append(max(history) - history[-1])
    mature = semantic.mature_concepts if condition == "semantic_replay" else ()
    return SeedResult(
        seed=seed,
        condition=condition,
        task_accuracy_matrix=tuple(accuracy_rows),
        final_average_accuracy=float(np.mean(final_values)),
        mean_forgetting=float(np.mean(forgetting_values)),
        update_count=readout.update_count,
        replay_update_count=replay_updates,
        semantic_concepts=len(mature),
        semantic_prototype_spikes=sum(len(item.prototype_spike_ids) for item in mature),
    )


def _bootstrap_ci(
    values: Sequence[float], *, samples: int, seed: int = 20260915
) -> tuple[float, float]:
    array = np.asarray(values, dtype=np.float64)
    if len(array) == 0:
        raise ValueError("bootstrap requires values")
    if len(array) == 1:
        value = float(array[0])
        return (value, value)
    rng = np.random.default_rng(seed)
    draws = rng.choice(array, size=(samples, len(array)), replace=True).mean(axis=1)
    low, high = np.quantile(draws, [0.025, 0.975])
    return float(low), float(high)


def _exact_sign_flip_p(values: Sequence[float]) -> float:
    array = np.asarray(values, dtype=np.float64)
    n = len(array)
    if n == 0:
        raise ValueError("sign-flip test requires values")
    observed = abs(float(np.mean(array)))
    if n > 20:
        rng = np.random.default_rng(20260915)
        signs = rng.choice((-1.0, 1.0), size=(100000, n))
        permuted = np.abs((signs * array).mean(axis=1))
        return float(
            (np.count_nonzero(permuted >= observed) + 1) / (len(permuted) + 1)
        )
    exceed = 0
    total = 1 << n
    for mask in range(total):
        signed = [
            value if mask & (1 << index) else -value
            for index, value in enumerate(array)
        ]
        if abs(float(np.mean(signed))) + 1e-15 >= observed:
            exceed += 1
    return exceed / total


def summarize_results(
    baseline: Sequence[SeedResult],
    semantic: Sequence[SeedResult],
    config: SplitMnistConfig,
) -> dict[str, Any]:
    baseline_by_seed = {item.seed: item for item in baseline}
    semantic_by_seed = {item.seed: item for item in semantic}
    if set(baseline_by_seed) != set(semantic_by_seed):
        raise ValueError("paired conditions must have identical seeds")
    seeds = sorted(baseline_by_seed)
    accuracy_delta = [
        semantic_by_seed[seed].final_average_accuracy
        - baseline_by_seed[seed].final_average_accuracy
        for seed in seeds
    ]
    forgetting_reduction = [
        baseline_by_seed[seed].mean_forgetting
        - semantic_by_seed[seed].mean_forgetting
        for seed in seeds
    ]
    accuracy_ci = _bootstrap_ci(
        accuracy_delta, samples=config.bootstrap_samples, seed=20260915
    )
    forgetting_ci = _bootstrap_ci(
        forgetting_reduction, samples=config.bootstrap_samples, seed=20260916
    )
    accuracy_mean = float(np.mean(accuracy_delta))
    forgetting_mean = float(np.mean(forgetting_reduction))
    accuracy_p = _exact_sign_flip_p(accuracy_delta)
    forgetting_p = _exact_sign_flip_p(forgetting_reduction)
    primary_success = (
        forgetting_mean >= config.effect_threshold_forgetting
        and forgetting_ci[0] > 0.0
        and forgetting_p < 0.05
        and accuracy_mean >= config.effect_threshold_accuracy
        and accuracy_ci[0] > 0.0
        and accuracy_p < 0.05
    )
    negative = forgetting_ci[1] < 0.0 or accuracy_ci[1] < 0.0
    classification = (
        "preregistered_positive_result"
        if primary_success
        else "negative_result"
        if negative
        else "null_or_inconclusive_result"
    )
    return {
        "paired_seeds": seeds,
        "baseline_final_accuracy_mean": float(
            np.mean([baseline_by_seed[seed].final_average_accuracy for seed in seeds])
        ),
        "semantic_final_accuracy_mean": float(
            np.mean([semantic_by_seed[seed].final_average_accuracy for seed in seeds])
        ),
        "baseline_forgetting_mean": float(
            np.mean([baseline_by_seed[seed].mean_forgetting for seed in seeds])
        ),
        "semantic_forgetting_mean": float(
            np.mean([semantic_by_seed[seed].mean_forgetting for seed in seeds])
        ),
        "accuracy_delta_mean": accuracy_mean,
        "accuracy_delta_bootstrap_95_ci": list(accuracy_ci),
        "accuracy_delta_sign_flip_p": accuracy_p,
        "forgetting_reduction_mean": forgetting_mean,
        "forgetting_reduction_bootstrap_95_ci": list(forgetting_ci),
        "forgetting_reduction_sign_flip_p": forgetting_p,
        "effect_threshold_accuracy": config.effect_threshold_accuracy,
        "effect_threshold_forgetting": config.effect_threshold_forgetting,
        "preregistered_primary_success": primary_success,
        "result_classification": classification,
        "automatic_evidence_promotion": False,
        "human_review_required": True,
        "scientific_evidence": False,
    }


def run_split_mnist_semantization(
    data: MnistBundle, config: SplitMnistConfig
) -> dict[str, Any]:
    """Run paired baseline/treatment experiments for every preregistered seed."""

    baseline = [
        _run_condition(data, config, seed=seed, condition="baseline")
        for seed in config.seeds
    ]
    semantic = [
        _run_condition(data, config, seed=seed, condition="semantic_replay")
        for seed in config.seeds
    ]
    return {
        "experiment_id": "EXP-S6-SEM-CL-001",
        "benchmark": "Split-MNIST",
        "scenario": "class-incremental-single-head",
        "tasks": [list(pair) for pair in TASKS],
        "mechanism": "MHRN SemanticMemory prototype consolidation + bounded replay",
        "baseline": (
            "identical rate-coded spiking representation + online softmax readout; "
            "no semantic memory"
        ),
        "config": asdict(config),
        "dataset_sha256": data.source_sha256,
        "runs": [asdict(item) for item in (*baseline, *semantic)],
        "summary": summarize_results(baseline, semantic, config),
    }


def render_report(result: dict[str, Any]) -> str:
    summary = result["summary"]
    status = summary["result_classification"]
    return "\n".join(
        [
            "# EXP-S6-SEM-CL-001 — Split-MNIST Semantization Ablation",
            "",
            f"**Result classification:** `{status}`",
            "",
            "This report is DATA ONLY. Human review is required before any claim is promoted.",
            "",
            "## Primary comparison",
            "",
            f"- Baseline final average accuracy: {summary['baseline_final_accuracy_mean']:.4f}",
            f"- Semantic final average accuracy: {summary['semantic_final_accuracy_mean']:.4f}",
            f"- Accuracy delta: {summary['accuracy_delta_mean']:+.4f} "
            f"(95% bootstrap CI {summary['accuracy_delta_bootstrap_95_ci'][0]:+.4f} to "
            f"{summary['accuracy_delta_bootstrap_95_ci'][1]:+.4f}; "
            f"sign-flip p={summary['accuracy_delta_sign_flip_p']:.6f})",
            f"- Baseline mean forgetting: {summary['baseline_forgetting_mean']:.4f}",
            f"- Semantic mean forgetting: {summary['semantic_forgetting_mean']:.4f}",
            f"- Forgetting reduction: {summary['forgetting_reduction_mean']:+.4f} "
            f"(95% bootstrap CI {summary['forgetting_reduction_bootstrap_95_ci'][0]:+.4f} to "
            f"{summary['forgetting_reduction_bootstrap_95_ci'][1]:+.4f}; "
            f"sign-flip p={summary['forgetting_reduction_sign_flip_p']:.6f})",
            "",
            "## Preregistered decision rule",
            "",
            f"Positive result requires accuracy delta >= {summary['effect_threshold_accuracy']:.2f}, "
            f"forgetting reduction >= {summary['effect_threshold_forgetting']:.2f}, positive 95% "
            "paired bootstrap lower bounds, and two-sided paired sign-flip p < 0.05 for both endpoints.",
            "",
            f"**Primary rule passed:** {summary['preregistered_primary_success']}",
            "",
            "## Governance",
            "",
            "- automatic evidence promotion: disabled",
            "- human review: required",
            "- scope: one mechanism, one benchmark, one simple baseline",
            "",
        ]
    )


def write_result_bundle(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "REPORT.md").write_text(render_report(result), encoding="utf-8")


__all__ = [
    "MnistBundle",
    "OnlineSoftmaxReadout",
    "SeedResult",
    "SplitMnistConfig",
    "TASKS",
    "image_to_spike_ids",
    "load_mnist",
    "render_report",
    "run_split_mnist_semantization",
    "summarize_results",
    "write_result_bundle",
]
