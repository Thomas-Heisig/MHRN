"""Pre-execution implementation for EXP-S6-SEM-CL-003.

CL-003 tests replay dose x representation with a constant total readout-update
budget. Empirical execution is blocked until a separate authorization record
exists and all freeze-bound files match their SHA-256 manifest.
"""

from __future__ import annotations

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
    TASKS,
    MnistBundle,
    OnlineSoftmaxReadout,
    SplitMnistConfig,
    image_to_spike_ids,
)
from src.research.continual_semantization_controls import (
    ReplayObject,
    random_objects_matching_semantic,
    raw_objects_for_task,
    semantic_objects_for_task,
)

EXPERIMENT_ID = "EXP-S6-SEM-CL-003"
SEEDS = tuple(range(301, 313))
CONDITIONS = ("R05", "S05", "R20", "S20", "X20", "R40", "S40")
DOSE_REPLAY_SLOTS = {"05": 100, "20": 400, "40": 800}
BOOTSTRAP_RESAMPLES = 20_000
SEMANTIC_MIN_EPISODE_SUPPORT = 8
SEMANTIC_PROTOTYPE_SUPPORT = 0.30
SEMANTIC_MATCH_THRESHOLD = 0.25
CAPACITY_PER_TASK = 50
TASK_UPDATE_SLOTS = 2000


@dataclass(frozen=True, slots=True)
class CL003Config:
    train_per_class: int = 1000
    test_per_class: int = 200
    pooling: int = 4
    thresholds: tuple[float, ...] = (0.2, 0.4, 0.6, 0.8)
    learning_rate: float = 0.025
    seeds: tuple[int, ...] = SEEDS
    capacity_per_task: int = CAPACITY_PER_TASK
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


@dataclass(frozen=True, slots=True)
class CL003SeedResult:
    seed: int
    condition: str
    task_accuracy_matrix: tuple[tuple[float | None, ...], ...]
    final_average_accuracy: float
    mean_forgetting: float
    current_task_updates: int
    replay_updates: int
    total_updates: int
    stored_by_task: tuple[int, ...]
    aborted: bool = False
    abort_reason: str | None = None


def require_execution_authorized(preregistration: dict[str, Any]) -> None:
    if preregistration.get("experiment_id") != EXPERIMENT_ID:
        raise RuntimeError("wrong preregistration for CL-003")
    if preregistration.get("execution_authorized") is not True:
        raise RuntimeError("CL-003 empirical execution is not authorized")


def condition_order(seed: int) -> tuple[str, ...]:
    values = list(CONDITIONS)
    random.Random(seed ^ 0xC1003).shuffle(values)
    return tuple(values)


def _dose_key(condition: str) -> str:
    return condition[-2:]


def replay_slot_mask(total_slots: int, replay_slots: int) -> tuple[int, ...]:
    """Return deterministic, maximally spread replay positions.

    For preregistered sizes (2000 with 100/400/800 replay slots), rounded
    midpoint targets are unique. A deterministic nearest-free fallback is kept
    for completeness and never consults empirical data.
    """

    if total_slots <= 0:
        raise ValueError("total_slots must be positive")
    if not 0 <= replay_slots < total_slots:
        raise ValueError("replay_slots must satisfy 0 <= replay_slots < total_slots")
    if replay_slots == 0:
        return ()

    targets = [
        int(round(((rank + 0.5) * total_slots / replay_slots) - 0.5))
        for rank in range(replay_slots)
    ]
    used: set[int] = set()
    resolved: list[int] = []
    for target in targets:
        target = min(max(target, 0), total_slots - 1)
        if target not in used:
            chosen = target
        else:
            chosen = -1
            for distance in range(1, total_slots):
                for candidate in (target - distance, target + distance):
                    if 0 <= candidate < total_slots and candidate not in used:
                        chosen = candidate
                        break
                if chosen >= 0:
                    break
            if chosen < 0:
                raise RuntimeError("could not resolve replay slot collision")
        used.add(chosen)
        resolved.append(chosen)
    result = tuple(sorted(resolved))
    if len(result) != replay_slots or len(set(result)) != replay_slots:
        raise RuntimeError("invalid replay slot mask")
    return result


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


def _episode(
    *,
    seed: int,
    task_index: int,
    position: int,
    label: int,
    spike_ids: tuple[int, ...],
) -> NeuralEpisode:
    return NeuralEpisode(
        run_id=f"cl003-{seed}",
        episode_id=f"cl003-{seed}-{task_index}-{position}",
        tick=task_index * 1_000_000 + position,
        sensor_id=f"split-mnist-label-{label}",
        modality="pooled_rate_code",
        spike_ids=spike_ids,
        frame_payload={"label": label, "task": task_index},
        actual_state=None,
    )


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


def _metrics(rows: Sequence[tuple[float | None, ...]]) -> tuple[float, float]:
    final = [float(value) for value in rows[-1] if value is not None]
    forgetting: list[float] = []
    for task_index in range(len(TASKS) - 1):
        history: list[float] = []
        for row in rows[task_index:]:
            value = row[task_index]
            if value is not None:
                history.append(float(value))
        forgetting.append(max(history) - history[-1])
    return float(np.mean(final)), float(np.mean(forgetting))


def _finite_readout(readout: OnlineSoftmaxReadout) -> bool:
    return bool(np.isfinite(readout.weights).all() and np.isfinite(readout.bias).all())


def _canonical_pool(
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


def balanced_replay_sequence(
    objects: Sequence[ReplayObject],
    count: int,
) -> tuple[ReplayObject, ...]:
    pool = tuple(objects)
    if count < 0:
        raise ValueError("count must be non-negative")
    if count == 0 or not pool:
        return ()
    quotient, remainder = divmod(count, len(pool))
    result: list[ReplayObject] = []
    for rank, item in enumerate(pool):
        result.extend([item] * (quotient + int(rank < remainder)))
    if len(result) != count:
        raise RuntimeError("balanced replay accounting failed")
    return tuple(result)


def _paired_bootstrap_ci(
    values: Sequence[float],
    *,
    samples: int,
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
        raise ValueError("exact sign-flip implementation supports n <= 20")
    observed = abs(float(array.mean()))
    exceed = 0
    total = 1 << n
    for mask in range(total):
        signs = np.fromiter(
            (1.0 if mask & (1 << index) else -1.0 for index in range(n)),
            dtype=np.float64,
            count=n,
        )
        exceed += int(abs(float((array * signs).mean())) + 1e-15 >= observed)
    return exceed / total


def _contrast(
    values: Sequence[float],
    *,
    minimum_effect: float | None,
    bootstrap_seed: int,
    samples: int,
) -> dict[str, Any]:
    mean = float(np.mean(values))
    ci = _paired_bootstrap_ci(values, samples=samples, seed=bootstrap_seed)
    p = _paired_sign_flip_p(values)
    passed = None
    if minimum_effect is not None:
        passed = mean >= minimum_effect and ci[0] > 0.0 and p < 0.05
    return {
        "paired_differences": [float(value) for value in values],
        "mean": mean,
        "minimum_effect": minimum_effect,
        "bootstrap_95_ci": list(ci),
        "sign_flip_p": p,
        "passed": passed,
    }


def summarize_confirmatory(results: Sequence[CL003SeedResult]) -> dict[str, Any]:
    complete = [item for item in results if not item.aborted]
    by_condition: dict[str, dict[int, CL003SeedResult]] = {
        condition: {} for condition in CONDITIONS
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
    if len(paired_seeds) < len(SEEDS):
        return {
            "paired_seeds": paired_seeds,
            "complete_paired_seed_count": len(paired_seeds),
            "H1_passed": False,
            "H2_passed": False,
            "result_classification": "incomplete_preregistered_run",
            "automatic_evidence_promotion": False,
            "human_review_required": True,
            "scientific_evidence": False,
        }

    def metric(condition: str, seed: int, name: str) -> float:
        return float(getattr(by_condition[condition][seed], name))

    c1 = [
        metric("S20", seed, "final_average_accuracy")
        - metric("R20", seed, "final_average_accuracy")
        for seed in paired_seeds
    ]
    c2 = [
        metric("R20", seed, "mean_forgetting") - metric("S20", seed, "mean_forgetting")
        for seed in paired_seeds
    ]
    c3 = [
        metric("S20", seed, "final_average_accuracy")
        - metric("X20", seed, "final_average_accuracy")
        for seed in paired_seeds
    ]
    c4 = [
        (
            metric("S20", seed, "final_average_accuracy")
            - metric("R20", seed, "final_average_accuracy")
        )
        - (
            metric("S05", seed, "final_average_accuracy")
            - metric("R05", seed, "final_average_accuracy")
        )
        for seed in paired_seeds
    ]
    s40_acc = [
        metric("S40", seed, "final_average_accuracy")
        - metric("R40", seed, "final_average_accuracy")
        for seed in paired_seeds
    ]
    s40_forgetting = [
        metric("R40", seed, "mean_forgetting") - metric("S40", seed, "mean_forgetting")
        for seed in paired_seeds
    ]

    contrasts = {
        "C1_S20_minus_R20_accuracy": _contrast(
            c1,
            minimum_effect=0.03,
            bootstrap_seed=20260915031,
            samples=BOOTSTRAP_RESAMPLES,
        ),
        "C2_R20_minus_S20_forgetting": _contrast(
            c2,
            minimum_effect=0.05,
            bootstrap_seed=20260915032,
            samples=BOOTSTRAP_RESAMPLES,
        ),
        "C3_S20_minus_X20_accuracy": _contrast(
            c3,
            minimum_effect=0.03,
            bootstrap_seed=20260915033,
            samples=BOOTSTRAP_RESAMPLES,
        ),
        "C4_dose_interaction_accuracy": _contrast(
            c4,
            minimum_effect=0.015,
            bootstrap_seed=20260915034,
            samples=BOOTSTRAP_RESAMPLES,
        ),
    }
    secondary = {
        "S40_minus_R40_accuracy": _contrast(
            s40_acc,
            minimum_effect=None,
            bootstrap_seed=20260915035,
            samples=BOOTSTRAP_RESAMPLES,
        ),
        "R40_minus_S40_forgetting": _contrast(
            s40_forgetting,
            minimum_effect=None,
            bootstrap_seed=20260915036,
            samples=BOOTSTRAP_RESAMPLES,
        ),
    }
    h1 = all(
        contrasts[name]["passed"]
        for name in (
            "C1_S20_minus_R20_accuracy",
            "C2_R20_minus_S20_forgetting",
            "C3_S20_minus_X20_accuracy",
        )
    )
    h2 = bool(contrasts["C4_dose_interaction_accuracy"]["passed"])
    dose_table = {}
    for dose in ("05", "20", "40"):
        raw = f"R{dose}"
        semantic = f"S{dose}"
        dose_table[dose] = {
            "semantic_minus_raw_accuracy_mean": float(
                np.mean(
                    [
                        metric(semantic, seed, "final_average_accuracy")
                        - metric(raw, seed, "final_average_accuracy")
                        for seed in paired_seeds
                    ]
                )
            ),
            "raw_minus_semantic_forgetting_mean": float(
                np.mean(
                    [
                        metric(raw, seed, "mean_forgetting")
                        - metric(semantic, seed, "mean_forgetting")
                        for seed in paired_seeds
                    ]
                )
            ),
        }
    if h1 and h2:
        classification = "H1_positive_H2_positive"
    elif h1:
        classification = "H1_positive_H2_negative"
    elif h2:
        classification = "H1_negative_H2_positive"
    else:
        classification = "H1_negative_H2_negative"
    return {
        "paired_seeds": paired_seeds,
        "complete_paired_seed_count": len(paired_seeds),
        "contrasts": contrasts,
        "secondary_40_percent": secondary,
        "dose_table": dose_table,
        "H1_passed": h1,
        "H2_passed": h2,
        "result_classification": classification,
        "automatic_evidence_promotion": False,
        "human_review_required": True,
        "scientific_evidence": False,
    }


def run_seed(
    data: MnistBundle,
    config: CL003Config,
    *,
    seed: int,
) -> tuple[CL003SeedResult, ...]:
    encoder = config.encoder
    train_rng = np.random.default_rng(seed)
    train_sets = [
        _task_indices(data.train_labels, pair, config.train_per_class, train_rng)
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
        if len(encoded) != TASK_UPDATE_SLOTS:
            raise RuntimeError("CL-003 requires exactly 2000 current examples per task")
        encoded_tasks.append(encoded)
        semantic.consolidate(episodes)
        sem = semantic_objects_for_task(
            semantic,
            task_index=task_index,
            labels=TASKS[task_index],
            capacity=config.capacity_per_task,
        )
        semantic_by_task.append(sem)
        raw_by_task.append(
            raw_objects_for_task(
                encoded,
                task_index=task_index,
                realized_count=len(sem),
            )
        )
        random_by_task.append(
            random_objects_matching_semantic(
                sem,
                seed=seed ^ 0xC1003,
                feature_count=encoder.feature_count,
            )
        )
        if not (
            len(semantic_by_task[-1]) == len(raw_by_task[-1]) == len(random_by_task[-1])
        ):
            raise RuntimeError("CL-003 memory budget mismatch")

    stores = {
        "R05": raw_by_task,
        "S05": semantic_by_task,
        "R20": raw_by_task,
        "S20": semantic_by_task,
        "X20": random_by_task,
        "R40": raw_by_task,
        "S40": semantic_by_task,
    }

    outputs: list[CL003SeedResult] = []
    for condition in condition_order(seed):
        readout = OnlineSoftmaxReadout(
            encoder.feature_count,
            seed=seed ^ 0xA11CE,
            learning_rate=config.learning_rate,
        )
        rows: list[tuple[float | None, ...]] = []
        current_updates = 0
        replay_updates = 0
        aborted = False
        abort_reason: str | None = None
        dose = _dose_key(condition)
        replay_slots = DOSE_REPLAY_SLOTS[dose]
        replay_positions = set(replay_slot_mask(TASK_UPDATE_SLOTS, replay_slots))

        try:
            for task_index, encoded in enumerate(encoded_tasks):
                if task_index == 0:
                    for _, spikes, label in encoded:
                        readout.update(spikes, label)
                        current_updates += 1
                else:
                    pool = _canonical_pool(stores[condition][:task_index])
                    replay_sequence = balanced_replay_sequence(pool, replay_slots)
                    if len(replay_sequence) != replay_slots and pool:
                        raise RuntimeError("CL-003 replay sequence length mismatch")
                    replay_cursor = 0
                    for slot, (_, spikes, label) in enumerate(encoded):
                        if slot in replay_positions and pool:
                            item = replay_sequence[replay_cursor]
                            replay_cursor += 1
                            readout.update(item.spike_ids, item.label)
                            replay_updates += 1
                        else:
                            readout.update(spikes, label)
                            current_updates += 1
                    if pool and replay_cursor != replay_slots:
                        raise RuntimeError("CL-003 replay slot accounting failed")
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
        except (FloatingPointError, RuntimeError, ValueError) as exc:
            aborted = True
            abort_reason = f"{type(exc).__name__}:{exc}"

        total_updates = current_updates + replay_updates
        stored = tuple(len(items) for items in stores[condition])
        if aborted or len(rows) != len(TASKS) or total_updates != 10_000:
            if not aborted and total_updates != 10_000:
                abort_reason = f"update_budget_mismatch:{total_updates}"
            outputs.append(
                CL003SeedResult(
                    seed=seed,
                    condition=condition,
                    task_accuracy_matrix=tuple(rows),
                    final_average_accuracy=math.nan,
                    mean_forgetting=math.nan,
                    current_task_updates=current_updates,
                    replay_updates=replay_updates,
                    total_updates=total_updates,
                    stored_by_task=stored,
                    aborted=True,
                    abort_reason=abort_reason or "incomplete_run",
                )
            )
            continue
        final_accuracy, mean_forgetting = _metrics(rows)
        outputs.append(
            CL003SeedResult(
                seed=seed,
                condition=condition,
                task_accuracy_matrix=tuple(rows),
                final_average_accuracy=final_accuracy,
                mean_forgetting=mean_forgetting,
                current_task_updates=current_updates,
                replay_updates=replay_updates,
                total_updates=total_updates,
                stored_by_task=stored,
            )
        )
    return tuple(outputs)


def run_experiment(
    data: MnistBundle,
    config: CL003Config,
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
        "# EXP-S6-SEM-CL-003 — Replay Dose × Representation",
        "",
        f"**Result classification:** `{summary['result_classification']}`",
        f"**H1 passed:** {summary['H1_passed']}",
        f"**H2 passed:** {summary['H2_passed']}",
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
                f"- minimum effect: {detail['minimum_effect']:+.6f}",
                f"- 95% bootstrap CI: {detail['bootstrap_95_ci'][0]:+.6f} to {detail['bootstrap_95_ci'][1]:+.6f}",
                f"- paired sign-flip p: {detail['sign_flip_p']:.6f}",
                f"- passed: {detail['passed']}",
            ]
        )
    for name, detail in summary.get("secondary_40_percent", {}).items():
        lines.extend(
            [
                "",
                f"## Secondary: {name}",
                f"- mean: {detail['mean']:+.6f}",
                f"- 95% bootstrap CI: {detail['bootstrap_95_ci'][0]:+.6f} to {detail['bootstrap_95_ci'][1]:+.6f}",
                f"- paired sign-flip p: {detail['sign_flip_p']:.6f}",
            ]
        )
    lines.extend(
        [
            "",
            "## Dose table",
            "",
            "```json",
            json.dumps(summary.get("dose_table", {}), indent=2, sort_keys=True),
            "```",
            "",
            "## Governance",
            "- automatic DATA→EVID promotion: disabled",
            "- human review: required",
            "- negative/null outcomes are retained",
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
    "CL003Config",
    "CL003SeedResult",
    "CONDITIONS",
    "DOSE_REPLAY_SLOTS",
    "EXPERIMENT_ID",
    "SEEDS",
    "TASK_UPDATE_SLOTS",
    "balanced_replay_sequence",
    "condition_order",
    "render_report",
    "replay_slot_mask",
    "require_execution_authorized",
    "run_experiment",
    "run_seed",
    "summarize_confirmatory",
    "write_result_bundle",
]
