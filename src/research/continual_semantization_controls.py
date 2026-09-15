"""Preregistered CL-002 controls for semantic vs raw replay on Split-MNIST.

This module is deliberately inert while the operational preregistration keeps
``execution_authorized`` false. Synthetic unit tests may exercise pure helpers,
but empirical MNIST execution must pass an explicit authorization gate.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from src.memory import NeuralEpisode, SemanticMemory
from src.research.continual_semantization import (
    MnistBundle,
    OnlineSoftmaxReadout,
    SplitMnistConfig,
    TASKS,
    image_to_spike_ids,
)

EXPERIMENT_ID = "EXP-S6-SEM-CL-002"
CONDITIONS = (
    "B1_naive_online",
    "B2_raw_replay",
    "B3_semantic_prototype",
    "B4_random_prototype",
)
SEEDS = tuple(range(201, 210))
CAPACITY_PER_TASK = 50
REPLAY_UPDATES_PER_TRANSITION = 100
BOOTSTRAP_RESAMPLES = 20_000
SEMANTIC_MIN_EPISODE_SUPPORT = 8
SEMANTIC_PROTOTYPE_SUPPORT = 0.30
SEMANTIC_MATCH_THRESHOLD = 0.25


@dataclass(frozen=True, slots=True)
class ReplayObject:
    task_index: int
    label: int
    spike_ids: tuple[int, ...]
    source_rank: int


@dataclass(frozen=True, slots=True)
class CL002SeedResult:
    seed: int
    condition: str
    task_accuracy_matrix: tuple[tuple[float | None, ...], ...]
    final_average_accuracy: float
    mean_forgetting: float
    current_task_updates: int
    replay_updates: int
    stored_by_task: tuple[int, ...]
    aborted: bool = False
    abort_reason: str | None = None


@dataclass(frozen=True, slots=True)
class CL002Config:
    train_per_class: int = 1000
    test_per_class: int = 200
    pooling: int = 4
    thresholds: tuple[float, ...] = (0.2, 0.4, 0.6, 0.8)
    learning_rate: float = 0.025
    seeds: tuple[int, ...] = SEEDS
    capacity_per_task: int = CAPACITY_PER_TASK
    replay_updates_per_transition: int = REPLAY_UPDATES_PER_TRANSITION
    bootstrap_samples: int = BOOTSTRAP_RESAMPLES

    @property
    def encoder(self) -> SplitMnistConfig:
        return SplitMnistConfig(
            train_per_class=self.train_per_class,
            test_per_class=self.test_per_class,
            seeds=self.seeds,
            pooling=self.pooling,
            thresholds=self.thresholds,
            learning_rate=self.learning_rate,
            replay_fraction=0.0,
            semantic_max_concepts=128,
            semantic_min_episode_support=SEMANTIC_MIN_EPISODE_SUPPORT,
            semantic_prototype_support=SEMANTIC_PROTOTYPE_SUPPORT,
            semantic_match_threshold=SEMANTIC_MATCH_THRESHOLD,
            effect_threshold_accuracy=0.03,
            effect_threshold_forgetting=0.05,
            bootstrap_samples=self.bootstrap_samples,
        )


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_preregistration(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require_execution_authorized(preregistration: dict[str, Any]) -> None:
    if preregistration.get("experiment_id") != EXPERIMENT_ID:
        raise RuntimeError("wrong preregistration for CL-002")
    if preregistration.get("execution_authorized") is not True:
        raise RuntimeError("CL-002 empirical execution is not authorized")


def condition_order(seed: int) -> tuple[str, ...]:
    values = list(CONDITIONS)
    random.Random(seed ^ 0xC1002).shuffle(values)
    return tuple(values)


def _semantic_label(sensor_id: str) -> int:
    prefix = "split-mnist-label-"
    if not sensor_id.startswith(prefix):
        raise ValueError("unexpected semantic sensor id")
    return int(sensor_id[len(prefix) :])


def semantic_objects_for_task(
    memory: SemanticMemory,
    *,
    task_index: int,
    labels: tuple[int, int],
    capacity: int = CAPACITY_PER_TASK,
) -> tuple[ReplayObject, ...]:
    selected = [
        concept
        for concept in memory.mature_concepts
        if _semantic_label(concept.sensor_id) in labels
    ]
    selected.sort(key=lambda item: (_semantic_label(item.sensor_id), item.concept_id))
    output: list[ReplayObject] = []
    for rank, concept in enumerate(selected[:capacity]):
        output.append(
            ReplayObject(
                task_index=task_index,
                label=_semantic_label(concept.sensor_id),
                spike_ids=tuple(concept.prototype_spike_ids),
                source_rank=rank,
            )
        )
    return tuple(output)


def raw_objects_for_task(
    encoded: Sequence[tuple[int, tuple[int, ...], int]],
    *,
    task_index: int,
    realized_count: int,
) -> tuple[ReplayObject, ...]:
    if realized_count < 0:
        raise ValueError("realized_count must be non-negative")
    ordered = sorted(encoded, key=lambda item: item[0])[:realized_count]
    return tuple(
        ReplayObject(task_index, label, tuple(spikes), rank)
        for rank, (_, spikes, label) in enumerate(ordered)
    )


def _random_seed(seed: int, task_index: int, rank: int) -> int:
    payload = f"{seed}:{task_index}:{rank}:CL002-B4".encode("ascii")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big", signed=False)


def random_objects_matching_semantic(
    semantic: Sequence[ReplayObject],
    *,
    seed: int,
    feature_count: int,
) -> tuple[ReplayObject, ...]:
    output: list[ReplayObject] = []
    universe = np.arange(feature_count, dtype=np.int64)
    for item in semantic:
        if len(item.spike_ids) > feature_count:
            raise ValueError("prototype exceeds feature dimension")
        rng = np.random.default_rng(
            _random_seed(seed, item.task_index, item.source_rank)
        )
        picked = rng.choice(universe, size=len(item.spike_ids), replace=False)
        output.append(
            ReplayObject(
                task_index=item.task_index,
                label=item.label,
                spike_ids=tuple(sorted(int(value) for value in picked)),
                source_rank=item.source_rank,
            )
        )
    return tuple(output)


def canonical_replay_pool(
    by_task: Sequence[Sequence[ReplayObject]],
) -> tuple[ReplayObject, ...]:
    return tuple(
        sorted(
            itertools.chain.from_iterable(by_task),
            key=lambda item: (
                item.task_index,
                item.label,
                item.source_rank,
                item.spike_ids,
            ),
        )
    )


def replay_schedule(
    objects: Sequence[ReplayObject],
    *,
    updates: int = REPLAY_UPDATES_PER_TRANSITION,
) -> tuple[ReplayObject, ...]:
    if updates < 0:
        raise ValueError("updates must be non-negative")
    pool = tuple(objects)
    if not pool or updates == 0:
        return ()
    quotient, remainder = divmod(updates, len(pool))
    schedule: list[ReplayObject] = []
    for rank, item in enumerate(pool):
        schedule.extend([item] * (quotient + int(rank < remainder)))
    if len(schedule) != updates:
        raise RuntimeError("replay budget accounting failed")
    return tuple(schedule)


def _paired_bootstrap_ci(
    values: Sequence[float],
    *,
    samples: int = BOOTSTRAP_RESAMPLES,
    seed: int,
) -> tuple[float, float]:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1 or len(array) == 0 or not np.isfinite(array).all():
        raise ValueError("bootstrap requires finite paired differences")
    rng = np.random.default_rng(seed)
    draws = rng.choice(array, size=(samples, len(array)), replace=True).mean(axis=1)
    low, high = np.quantile(draws, [0.025, 0.975])
    return float(low), float(high)


def _paired_sign_flip_p(values: Sequence[float]) -> float:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1 or len(array) == 0 or not np.isfinite(array).all():
        raise ValueError("sign-flip requires finite paired differences")
    n = len(array)
    if n > 20:
        raise ValueError("CL-002 exact sign-flip implementation supports n <= 20")
    observed = abs(float(array.mean()))
    exceed = 0
    total = 1 << n
    for mask in range(total):
        signs = np.fromiter(
            (1.0 if mask & (1 << index) else -1.0 for index in range(n)),
            dtype=np.float64,
            count=n,
        )
        statistic = abs(float((array * signs).mean()))
        exceed += int(statistic + 1e-15 >= observed)
    return exceed / total


def summarize_confirmatory(
    results: Sequence[CL002SeedResult],
) -> dict[str, Any]:
    complete = [item for item in results if not item.aborted]
    by_condition: dict[str, dict[int, CL002SeedResult]] = {
        name: {} for name in CONDITIONS
    }
    for item in complete:
        if item.condition not in by_condition:
            raise ValueError("unexpected condition")
        if item.seed in by_condition[item.condition]:
            raise ValueError("duplicate seed-condition result")
        by_condition[item.condition][item.seed] = item

    paired = set(SEEDS)
    for condition in CONDITIONS:
        paired &= set(by_condition[condition])
    paired_seeds = sorted(paired)
    complete_pair_count = len(paired_seeds)

    if complete_pair_count < 9:
        return {
            "paired_seeds": paired_seeds,
            "complete_paired_seed_count": complete_pair_count,
            "preregistered_positive_semantic_effect": False,
            "result_classification": "incomplete_preregistered_run",
            "automatic_evidence_promotion": False,
            "human_review_required": True,
            "scientific_evidence": False,
        }

    b2 = by_condition["B2_raw_replay"]
    b3 = by_condition["B3_semantic_prototype"]
    b4 = by_condition["B4_random_prototype"]
    c1 = [
        b3[seed].final_average_accuracy - b2[seed].final_average_accuracy
        for seed in paired_seeds
    ]
    c2 = [b2[seed].mean_forgetting - b3[seed].mean_forgetting for seed in paired_seeds]
    c3 = [
        b3[seed].final_average_accuracy - b4[seed].final_average_accuracy
        for seed in paired_seeds
    ]

    contrasts: dict[str, dict[str, Any]] = {}
    specifications = (
        ("C1_accuracy_semantic_minus_raw", c1, 0.03, 2026091501),
        ("C2_forgetting_raw_minus_semantic", c2, 0.05, 2026091502),
        ("C3_accuracy_semantic_minus_random", c3, 0.03, 2026091503),
    )
    passed = True
    for name, values, threshold, bootstrap_seed in specifications:
        mean = float(np.mean(values))
        ci = _paired_bootstrap_ci(
            values,
            samples=BOOTSTRAP_RESAMPLES,
            seed=bootstrap_seed,
        )
        p = _paired_sign_flip_p(values)
        contrast_pass = mean >= threshold and ci[0] > 0.0 and p < 0.05
        passed = passed and contrast_pass
        contrasts[name] = {
            "paired_differences": list(values),
            "mean": mean,
            "minimum_effect": threshold,
            "bootstrap_95_ci": list(ci),
            "sign_flip_p": p,
            "passed": contrast_pass,
        }

    b3_worse_b2 = (
        contrasts["C1_accuracy_semantic_minus_raw"]["mean"] < 0.0
        or contrasts["C2_forgetting_raw_minus_semantic"]["mean"] < 0.0
    )
    classification = (
        "preregistered_positive_semantic_effect"
        if passed
        else (
            "negative_evidence_for_prototype_advantage"
            if b3_worse_b2
            else "null_or_inconclusive_result"
        )
    )
    return {
        "paired_seeds": paired_seeds,
        "complete_paired_seed_count": complete_pair_count,
        "contrasts": contrasts,
        "preregistered_positive_semantic_effect": passed,
        "result_classification": classification,
        "automatic_evidence_promotion": False,
        "human_review_required": True,
        "scientific_evidence": False,
    }


def _episode(
    *,
    seed: int,
    task_index: int,
    position: int,
    label: int,
    spike_ids: tuple[int, ...],
) -> NeuralEpisode:
    return NeuralEpisode(
        run_id=f"cl002-{seed}",
        episode_id=f"cl002-{seed}-{task_index}-{position}",
        tick=task_index * 1_000_000 + position,
        sensor_id=f"split-mnist-label-{label}",
        modality="pooled_rate_code",
        spike_ids=spike_ids,
        frame_payload={"label": label, "task": task_index},
        actual_state=None,
    )


def _sample_indices(
    labels: np.ndarray,
    label: int,
    count: int,
    rng: np.random.Generator,
) -> np.ndarray:
    available = np.flatnonzero(labels == label)
    if count > len(available):
        raise ValueError("insufficient examples")
    return np.asarray(rng.choice(available, size=count, replace=False), dtype=np.int64)


def _task_indices(
    labels: np.ndarray,
    pair: tuple[int, int],
    per_class: int,
    rng: np.random.Generator,
) -> np.ndarray:
    joined = np.concatenate(
        (
            _sample_indices(labels, pair[0], per_class, rng),
            _sample_indices(labels, pair[1], per_class, rng),
        )
    )
    rng.shuffle(joined)
    return joined


def _evaluate(
    readout: OnlineSoftmaxReadout,
    data: MnistBundle,
    indices: np.ndarray,
    encoder: SplitMnistConfig,
) -> float:
    correct = 0
    for raw_index in indices:
        index = int(raw_index)
        spikes = image_to_spike_ids(data.test_images[index], encoder)
        correct += int(readout.predict(spikes) == int(data.test_labels[index]))
    return correct / len(indices)


def _metrics(
    rows: Sequence[tuple[float | None, ...]],
) -> tuple[float, float]:
    final = [float(value) for value in rows[-1] if value is not None]
    forgetting: list[float] = []
    for task_index in range(len(TASKS) - 1):
        history = [
            float(row[task_index])
            for row in rows[task_index:]
            if row[task_index] is not None
        ]
        forgetting.append(max(history) - history[-1])
    return float(np.mean(final)), float(np.mean(forgetting))


def _finite_readout(readout: OnlineSoftmaxReadout) -> bool:
    return bool(np.isfinite(readout.weights).all() and np.isfinite(readout.bias).all())


def run_seed(
    data: MnistBundle,
    config: CL002Config,
    *,
    seed: int,
) -> tuple[CL002SeedResult, ...]:
    encoder = config.encoder
    train_rng = np.random.default_rng(seed)
    train_sets = [
        _task_indices(
            data.train_labels,
            pair,
            config.train_per_class,
            train_rng,
        )
        for pair in TASKS
    ]
    test_sets = [
        _task_indices(
            data.test_labels,
            pair,
            config.test_per_class,
            np.random.default_rng(seed * 1009 + task_index),
        )
        for task_index, pair in enumerate(TASKS)
    ]
    encoded_tasks: list[list[tuple[int, tuple[int, ...], int]]] = []
    semantic = SemanticMemory(
        max_concepts=128,
        min_episode_support=SEMANTIC_MIN_EPISODE_SUPPORT,
        prototype_support=SEMANTIC_PROTOTYPE_SUPPORT,
        match_threshold=SEMANTIC_MATCH_THRESHOLD,
    )
    semantic_by_task: list[tuple[ReplayObject, ...]] = []
    raw_by_task: list[tuple[ReplayObject, ...]] = []
    random_by_task: list[tuple[ReplayObject, ...]] = []

    for task_index, indices in enumerate(train_sets):
        encoded: list[tuple[int, tuple[int, ...], int]] = []
        episodes: list[NeuralEpisode] = []
        for position, raw_index in enumerate(indices):
            index = int(raw_index)
            label = int(data.train_labels[index])
            spikes = image_to_spike_ids(data.train_images[index], encoder)
            encoded.append((index, spikes, label))
            episodes.append(
                _episode(
                    seed=seed,
                    task_index=task_index,
                    position=position,
                    label=label,
                    spike_ids=spikes,
                )
            )
        encoded_tasks.append(encoded)
        semantic.consolidate(episodes)
        sem = semantic_objects_for_task(
            semantic,
            task_index=task_index,
            labels=TASKS[task_index],
            capacity=config.capacity_per_task,
        )
        realized = len(sem)
        semantic_by_task.append(sem)
        raw_by_task.append(
            raw_objects_for_task(
                encoded,
                task_index=task_index,
                realized_count=realized,
            )
        )
        random_by_task.append(
            random_objects_matching_semantic(
                sem,
                seed=seed,
                feature_count=encoder.feature_count,
            )
        )
        if not (
            len(raw_by_task[-1]) == len(semantic_by_task[-1]) == len(random_by_task[-1])
        ):
            raise RuntimeError("realized memory budget mismatch")

    outputs: list[CL002SeedResult] = []
    for condition in condition_order(seed):
        readout = OnlineSoftmaxReadout(
            encoder.feature_count,
            seed=seed ^ 0xA11CE,
            learning_rate=config.learning_rate,
        )
        rows: list[tuple[float | None, ...]] = []
        replay_updates = 0
        current_updates = 0
        aborted = False
        abort_reason: str | None = None
        stores = {
            "B2_raw_replay": raw_by_task,
            "B3_semantic_prototype": semantic_by_task,
            "B4_random_prototype": random_by_task,
        }
        try:
            for task_index, encoded in enumerate(encoded_tasks):
                if task_index > 0 and condition != "B1_naive_online":
                    pool = canonical_replay_pool(stores[condition][:task_index])
                    schedule = replay_schedule(
                        pool,
                        updates=config.replay_updates_per_transition,
                    )
                    for item in schedule:
                        readout.update(item.spike_ids, item.label)
                        replay_updates += 1
                for _, spikes, label in encoded:
                    readout.update(spikes, label)
                    current_updates += 1
                if not _finite_readout(readout):
                    raise FloatingPointError("NaN_or_Inf_in_condition_state")
                row: list[float | None] = []
                for eval_task, indices in enumerate(test_sets):
                    row.append(
                        None
                        if eval_task > task_index
                        else _evaluate(readout, data, indices, encoder)
                    )
                rows.append(tuple(row))
        except (FloatingPointError, ValueError, RuntimeError) as exc:
            aborted = True
            abort_reason = f"{type(exc).__name__}:{exc}"

        if aborted or len(rows) != len(TASKS):
            outputs.append(
                CL002SeedResult(
                    seed=seed,
                    condition=condition,
                    task_accuracy_matrix=tuple(rows),
                    final_average_accuracy=math.nan,
                    mean_forgetting=math.nan,
                    current_task_updates=current_updates,
                    replay_updates=replay_updates,
                    stored_by_task=tuple(
                        len(items) for items in stores.get(condition, ())
                    ),
                    aborted=True,
                    abort_reason=abort_reason or "incomplete_run",
                )
            )
            continue

        final_accuracy, mean_forgetting = _metrics(rows)
        outputs.append(
            CL002SeedResult(
                seed=seed,
                condition=condition,
                task_accuracy_matrix=tuple(rows),
                final_average_accuracy=final_accuracy,
                mean_forgetting=mean_forgetting,
                current_task_updates=current_updates,
                replay_updates=replay_updates,
                stored_by_task=(
                    tuple(len(items) for items in stores[condition])
                    if condition in stores
                    else (0, 0, 0, 0, 0)
                ),
            )
        )
    return tuple(outputs)


def run_experiment(
    data: MnistBundle,
    config: CL002Config,
    *,
    preregistration: dict[str, Any],
    source_hashes: dict[str, str],
) -> dict[str, Any]:
    require_execution_authorized(preregistration)
    runs = tuple(
        item for seed in config.seeds for item in run_seed(data, config, seed=seed)
    )
    return {
        "experiment_id": EXPERIMENT_ID,
        "benchmark": "Split-MNIST",
        "config": asdict(config),
        "dataset_sha256": data.source_sha256,
        "source_hashes": dict(sorted(source_hashes.items())),
        "runs": [asdict(item) for item in runs],
        "summary": summarize_confirmatory(runs),
        "automatic_evidence_promotion": False,
        "human_review_required": True,
        "scientific_evidence": False,
    }


def render_report(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# EXP-S6-SEM-CL-002 — Semantic vs Raw Replay",
        "",
        f"**Result classification:** `{summary['result_classification']}`",
        "",
        "This report is DATA ONLY. Human EVID review is required.",
        "",
        f"Complete paired seeds: {summary['complete_paired_seed_count']}",
    ]
    for name, detail in summary.get("contrasts", {}).items():
        lines.extend(
            [
                "",
                f"## {name}",
                f"- mean: {detail['mean']:+.6f}",
                f"- threshold: {detail['minimum_effect']:+.6f}",
                f"- 95% bootstrap CI: "
                f"{detail['bootstrap_95_ci'][0]:+.6f} to "
                f"{detail['bootstrap_95_ci'][1]:+.6f}",
                f"- paired sign-flip p: {detail['sign_flip_p']:.6f}",
                f"- passed: {detail['passed']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Governance",
            "- automatic DATA→EVID promotion: disabled",
            "- human review: required",
            "- null and negative outcomes are retained",
            "",
        ]
    )
    return "\n".join(lines)


def write_result_bundle(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "REPORT.md").write_text(render_report(result), encoding="utf-8")


__all__ = [
    "BOOTSTRAP_RESAMPLES",
    "CAPACITY_PER_TASK",
    "CL002Config",
    "CL002SeedResult",
    "CONDITIONS",
    "EXPERIMENT_ID",
    "REPLAY_UPDATES_PER_TRANSITION",
    "ReplayObject",
    "SEEDS",
    "canonical_replay_pool",
    "condition_order",
    "random_objects_matching_semantic",
    "raw_objects_for_task",
    "render_report",
    "replay_schedule",
    "require_execution_authorized",
    "run_experiment",
    "run_seed",
    "semantic_objects_for_task",
    "sha256_bytes",
    "summarize_confirmatory",
    "write_result_bundle",
]
