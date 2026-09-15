"""Registered Stage-6 functional experiments.

These runners close engineering gaps around neural episodic recall, semantic
held-out generalization, replay reactivation, prediction-error ablations and
frozen multistep world-model evaluation. They intentionally return DATA-only
records. Passing these experiments never promotes a claim to accepted evidence.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from src.core.network import NeuralNetwork
from src.embodiment.models import SensorFrame
from src.learning import (
    LearningEngine,
    PredictionErrorPlasticity,
    PredictionErrorPlasticityConfig,
    PredictionErrorSignal,
)
from src.memory import (
    ActionConditionedWorldModel,
    ActionSequenceCandidate,
    EpisodicReplayScheduler,
    NeuralEpisode,
    NeuralEpisodicMemory,
    OfflineDecisionEvaluator,
    ReplayMode,
    SemanticMemory,
    StateAction,
)

Config = Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class Stage6Run:
    """Campaign-compatible immutable result row."""

    experiment_id: str
    condition: str
    seed: int
    metrics: dict[str, Any]
    state_digest_before: str
    state_digest_after: str
    runtime_error: str | None = None


def _digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def _coord(index: int) -> tuple[int, int, int, int, int]:
    values: list[int] = []
    remaining = index
    for _ in range(5):
        values.append(remaining % 8)
        remaining //= 8
    return (values[0], values[1], values[2], values[3], values[4])


def _probe_network(seed: int, neuron_count: int) -> tuple[NeuralNetwork, tuple[int, ...]]:
    if neuron_count <= 0 or neuron_count > 256:
        raise ValueError("neuron_count must be in [1, 256]")
    values: dict[str, Any] = {
        "dimensions": [8, 8, 8, 8, 8],
        "simulation": {"dt_ms": 1.0, "max_delay": 4, "debug_invariants": True},
        "network": {
            "weight_min": 0.0,
            "weight_max": 1.0,
            "initial_connections_per_neuron": 0,
            "neighbour_radius": 1.0,
        },
        "energy": {"initial": 1.0, "spike_cost": 0.001, "affects_firing": False},
        "topology": {
            "allow_self_connections": False,
            "allow_parallel_connections": False,
        },
        "neuron": {"a": 0.02, "b": 0.2, "c": -65.0, "d": 8.0},
    }
    network = NeuralNetwork(values, random.Random(seed))
    ids = tuple(network.add_neuron(_coord(index)) for index in range(neuron_count))
    return network, ids


def _spike(network: NeuralNetwork, neuron_ids: Sequence[int], current: float = 100.0) -> tuple[int, ...]:
    network.inject_current_batch({neuron_id: current for neuron_id in neuron_ids})
    return network.step().spike_ids


def _idle(network: NeuralNetwork, count: int = 1) -> None:
    for _ in range(count):
        network.step()


def _decode_value(
    spike_ids: Sequence[int],
    value_a: Sequence[int],
    value_b: Sequence[int],
) -> str | None:
    spikes = set(spike_ids)
    a_score = len(spikes.intersection(value_a))
    b_score = len(spikes.intersection(value_b))
    if a_score == b_score:
        return None
    return "A" if a_score > b_score else "B"


def _fallback_choice(seed: int, trial: int) -> str:
    return "A" if random.Random(seed * 104729 + trial * 7919).random() < 0.5 else "B"


def run_s6_epi_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Neural key/value recall after real SNN distractors without payload answers."""

    del config
    conditions = ("intact", "read_off", "write_off", "episode_shuffle")
    trials = 12
    delay_steps = 6
    runs: list[Stage6Run] = []

    for seed in seeds:
        targets = [
            "A" if random.Random(seed * 1009 + trial).random() < 0.5 else "B"
            for trial in range(trials)
        ]
        for condition in conditions:
            network, ids = _probe_network(seed ^ _digest(condition).__hash__(), 24)
            key_ids = ids[:trials]
            value_a = ids[12:15]
            value_b = ids[15:18]
            distractors = ids[18:24]
            memory = NeuralEpisodicMemory(
                run_id=f"s6-epi-{seed}-{condition}",
                capacity=trials + 4,
                retention_ticks=4096,
                read_enabled=condition != "read_off",
                write_enabled=condition != "write_off",
            )
            before = _digest(
                {"memory": memory.state_dict(), "tick": network.current_tick}
            )
            correct = 0
            retrievals = 0
            encoding_spikes = 0
            query_spikes = 0
            distractor_spikes = 0

            for trial, target in enumerate(targets):
                memory.reset_episode(f"trial-{trial}")
                value_ids = value_a if target == "A" else value_b
                encoding_pattern = _spike(network, (key_ids[trial], *value_ids))
                encoding_spikes += len(encoding_pattern)
                memory.record(
                    {"spike_ids": encoding_pattern},
                    SensorFrame(
                        "s6-epi-key-value",
                        network.current_tick - 1,
                        "neural_key_value",
                        {"phase": "encoding", "trial": trial},
                    ),
                    None,
                )

                for delay_index in range(delay_steps):
                    first = distractors[(trial + delay_index) % len(distractors)]
                    second = distractors[(trial + delay_index + 2) % len(distractors)]
                    distractor_spikes += len(_spike(network, (first, second)))

                query_pattern = _spike(network, (key_ids[trial],))
                query_spikes += len(query_pattern)
                matches = memory.recall(
                    query_pattern,
                    sensor_id="s6-epi-key-value",
                    modality="neural_key_value",
                    limit=4,
                    min_score=0.1,
                )
                selected_episode: NeuralEpisode | None = None
                if matches:
                    retrievals += 1
                    selected_episode = matches[0].episode
                if condition == "episode_shuffle" and selected_episode is not None:
                    alternatives = [
                        episode
                        for episode in memory.episodes
                        if episode.episode_id != selected_episode.episode_id
                    ]
                    selected_episode = (
                        alternatives[(seed + trial) % len(alternatives)]
                        if alternatives
                        else None
                    )
                selected = (
                    None
                    if selected_episode is None
                    else _decode_value(selected_episode.spike_ids, value_a, value_b)
                )
                if selected is None:
                    selected = _fallback_choice(seed, trial)
                correct += int(selected == target)
                _idle(network, 2)

            after = _digest(
                {
                    "memory": memory.state_dict(),
                    "tick": network.current_tick,
                    "total_spikes": network.total_spikes,
                }
            )
            runs.append(
                Stage6Run(
                    "S6-EPI-001",
                    condition,
                    seed,
                    {
                        "trials": trials,
                        "delay_steps": delay_steps,
                        "correct": correct,
                        "accuracy": correct / trials,
                        "retrievals": retrievals,
                        "encoding_spikes": encoding_spikes,
                        "query_spikes": query_spikes,
                        "distractor_spikes": distractor_spikes,
                        "stored_episodes": len(memory.episodes),
                        "snn_involved": True,
                        "target_in_memory_payload": False,
                        "answer_reads_payload": False,
                        "answer_reads_actual_state": False,
                        "held_out_from_payload": True,
                        "scientific_evidence": False,
                        "claim_scope": "neural_episodic_functional_data_only",
                    },
                    before,
                    after,
                )
            )
    return runs


def _episode_from_pattern(
    *,
    run_id: str,
    episode_id: str,
    tick: int,
    pattern: Sequence[int],
) -> NeuralEpisode:
    return NeuralEpisode(
        run_id=run_id,
        episode_id=episode_id,
        tick=tick,
        sensor_id="s6-semantic",
        modality="neural_concept",
        spike_ids=tuple(sorted(set(pattern))),
        frame_payload={"phase": "semantic_probe", "episode": episode_id},
        actual_state=None,
    )


def _concept_label(prototype: Sequence[int], core_a: Sequence[int], core_b: Sequence[int]) -> str | None:
    return _decode_value(prototype, core_a, core_b)


def run_s6_sem_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Held-out semantic prototype test with disjoint train/evaluation episodes."""

    del config
    conditions = ("intact", "episode_shuffle", "no_semantic")
    train_per_class = 6
    holdout_per_class = 4
    runs: list[Stage6Run] = []

    for seed in seeds:
        for condition in conditions:
            network, ids = _probe_network(seed + 2000, 48)
            core_a = ids[0:3]
            core_b = ids[3:6]
            nuisance = ids[6:46]
            semantic = SemanticMemory(
                max_concepts=8,
                min_episode_support=2,
                prototype_support=0.6,
                match_threshold=0.45,
            )
            before = _digest(semantic.state_dict())
            training: list[NeuralEpisode] = []
            train_targets = [
                label
                for pair in zip(
                    ["A"] * train_per_class,
                    ["B"] * train_per_class,
                    strict=True,
                )
                for label in pair
            ]
            shuffle_rng = random.Random(seed ^ 0x5E6A)
            shuffled_labels = list(train_targets)
            shuffle_rng.shuffle(shuffled_labels)

            for index, target in enumerate(train_targets):
                encoded_target = (
                    shuffled_labels[index] if condition == "episode_shuffle" else target
                )
                core = core_a if encoded_target == "A" else core_b
                pattern = _spike(network, (*core, nuisance[index]))
                training.append(
                    _episode_from_pattern(
                        run_id=f"s6-sem-{seed}-{condition}",
                        episode_id=f"train-{index}",
                        tick=network.current_tick - 1,
                        pattern=pattern,
                    )
                )
                _idle(network, 3)

            updates = 0 if condition == "no_semantic" else semantic.consolidate(training)
            correct = 0
            matched = 0
            evaluations = 0
            heldout_targets = ["A", "B"] * holdout_per_class
            for offset, target in enumerate(heldout_targets):
                core = core_a if target == "A" else core_b
                nuisance_id = nuisance[train_per_class * 2 + offset]
                pattern = _spike(network, (*core, nuisance_id))
                matches = semantic.query(
                    pattern,
                    sensor_id="s6-semantic",
                    modality="neural_concept",
                    limit=1,
                )
                predicted: str | None = None
                if matches:
                    matched += 1
                    predicted = _concept_label(
                        matches[0].concept.prototype_spike_ids,
                        core_a,
                        core_b,
                    )
                if predicted is None:
                    predicted = _fallback_choice(seed + 1, offset)
                correct += int(predicted == target)
                evaluations += 1
                _idle(network, 3)

            after = _digest(semantic.state_dict())
            runs.append(
                Stage6Run(
                    "S6-SEM-001",
                    condition,
                    seed,
                    {
                        "training_episodes": len(training),
                        "held_out_episodes": evaluations,
                        "train_eval_episode_overlap": 0,
                        "semantic_updates": updates,
                        "mature_concepts": len(semantic.mature_concepts),
                        "matched_holdout": matched,
                        "correct": correct,
                        "accuracy": correct / evaluations,
                        "snn_involved": True,
                        "held_out": True,
                        "answer_reads_payload": False,
                        "scientific_evidence": False,
                        "claim_scope": "held_out_semantic_generalization_data_only",
                    },
                    before,
                    after,
                )
            )
    return runs


def _replay_source(seed: int) -> tuple[tuple[NeuralEpisode, ...], int]:
    network, ids = _probe_network(seed + 3000, 32)
    core_a = ids[0:3]
    core_b = ids[3:6]
    nuisance = ids[6:22]
    episodes: list[NeuralEpisode] = []
    for index in range(12):
        target = "A" if index % 2 == 0 else "B"
        core = core_a if target == "A" else core_b
        pattern = _spike(network, (*core, nuisance[index]))
        episodes.append(
            _episode_from_pattern(
                run_id=f"s6-rpl-{seed}",
                episode_id=f"episode-{index}",
                tick=network.current_tick - 1,
                pattern=pattern,
            )
        )
        _idle(network, 2)
    return tuple(episodes), len(ids)


def _reactivation_fidelity(
    network: NeuralNetwork,
    episode: NeuralEpisode,
) -> float:
    observed = set(_spike(network, episode.spike_ids))
    expected = set(episode.spike_ids)
    if not expected:
        return 0.0
    return len(observed.intersection(expected)) / len(expected)


def run_s6_rpl_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Replay reactivation controls with an equal-step additional-awake comparator."""

    del config
    conditions = ("no_replay", "ordered", "shuffled", "equal_budget_awake")
    budget = 8
    runs: list[Stage6Run] = []

    for seed in seeds:
        source, neuron_count = _replay_source(seed)
        scheduler = EpisodicReplayScheduler(max_events=budget)
        for condition in conditions:
            network, _ = _probe_network(seed + 4000, neuron_count)
            semantic = SemanticMemory(
                max_concepts=8,
                min_episode_support=2,
                prototype_support=0.6,
                match_threshold=0.45,
            )
            before = _digest(
                {"semantic": semantic.state_dict(), "tick": network.current_tick}
            )
            selected: tuple[NeuralEpisode, ...]
            if condition == "no_replay":
                selected = ()
            elif condition == "ordered":
                selected = scheduler.plan(
                    source, mode=ReplayMode.ORDERED, budget=budget, seed=seed
                ).selected
            elif condition == "shuffled":
                selected = scheduler.plan(
                    source, mode=ReplayMode.SHUFFLED, budget=budget, seed=seed
                ).selected
            else:
                selected = tuple(source[-budget:])

            fidelities: list[float] = []
            if condition == "no_replay":
                _idle(network, budget)
            else:
                for episode in selected:
                    fidelities.append(_reactivation_fidelity(network, episode))
                    _idle(network, 1)
                semantic.consolidate(selected)

            after = _digest(
                {
                    "semantic": semantic.state_dict(),
                    "tick": network.current_tick,
                    "total_spikes": network.total_spikes,
                }
            )
            runs.append(
                Stage6Run(
                    "S6-RPL-001",
                    condition,
                    seed,
                    {
                        "requested_budget": budget,
                        "used_episode_budget": len(selected),
                        "network_step_budget": budget if condition == "no_replay" else len(selected) * 2,
                        "mean_reactivation_fidelity": (
                            sum(fidelities) / len(fidelities) if fidelities else None
                        ),
                        "semantic_updates": len(selected),
                        "mature_concepts": len(semantic.mature_concepts),
                        "ordered_replay": condition == "ordered",
                        "time_shuffled_replay": condition == "shuffled",
                        "additional_awake_control": condition == "equal_budget_awake",
                        "snn_involved": True,
                        "simulated_sleep_claim": False,
                        "scientific_evidence": False,
                        "claim_scope": "controlled_reactivation_data_only",
                    },
                    before,
                    after,
                )
            )
    return runs


def _plasticity_config() -> dict[str, Any]:
    return {
        "dimensions": [4, 4, 4, 4, 4],
        "simulation": {"dt_ms": 1.0, "max_delay": 4, "debug_invariants": True},
        "network": {
            "weight_min": 0.0,
            "weight_max": 1.0,
            "initial_connections_per_neuron": 0,
            "neighbour_radius": 1.0,
        },
        "neuron": {"a": 0.02, "b": 0.2, "c": -65.0, "d": 8.0},
        "energy": {"initial": 1.0, "spike_cost": 0.001, "affects_firing": False},
        "stdp": {
            "enabled": False,
            "a_plus": 0.1,
            "a_minus": 0.12,
            "tau_plus": 20.0,
            "tau_minus": 20.0,
            "min_weight": 0.0,
            "max_weight": 1.0,
        },
        "eligibility": {"enabled": True, "tau_ticks": 200.0},
        "reward": {
            "enabled": True,
            "learning_rate": 0.1,
            "delay_ticks": 0,
            "clamp_weights": True,
            "reset_trace_after_reward": False,
            "trace_epsilon": 1.0e-12,
        },
    }


def run_s6_pe_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Factor prediction error (correct/disabled/shuffled) by reward (on/off)."""

    del config
    runs: list[Stage6Run] = []
    for seed in seeds:
        for error_mode in ("correct", "disabled", "shuffled"):
            for reward_on in (False, True):
                condition = f"pe_{error_mode}__reward_{'on' if reward_on else 'off'}"
                values = _plasticity_config()
                network = NeuralNetwork(values, random.Random(seed))
                pre_id = network.add_neuron((0, 0, 0, 0, 0))
                post_id = network.add_neuron((1, 0, 0, 0, 0))
                network.connect(pre_id, post_id, 0.5, 1)
                learning = LearningEngine(network, values)
                modulator = PredictionErrorPlasticity(
                    learning,
                    PredictionErrorPlasticityConfig(
                        enabled=error_mode != "disabled",
                        learning_rate=0.05,
                    ),
                )
                before = _digest(
                    {"weight": network.synapses[pre_id][0].weight, "condition": condition}
                )

                network.inject_current(pre_id, 100.0)
                pre_result = network.step()
                learning.update(pre_result)
                for _ in range(4):
                    learning.update(network.step())
                network.inject_current(post_id, 100.0)
                post_result = network.step()
                learning.update(post_result)

                reward_calls = 0
                if reward_on:
                    learning.set_reward(1.0, post_result.tick)
                    reward_calls = 1
                signal_value = 1.0
                if error_mode == "shuffled":
                    signal_value = (
                        -1.0
                        if random.Random(seed ^ 0xE770).random() < 0.5
                        else 1.0
                    )
                changed = modulator.apply(
                    PredictionErrorSignal(signal_value, post_result.tick)
                )
                final_weight = network.synapses[pre_id][0].weight
                after = _digest(
                    {
                        "weight": final_weight,
                        "pe_stats": modulator.stats,
                        "reward_calls": reward_calls,
                    }
                )
                runs.append(
                    Stage6Run(
                        "S6-PE-001",
                        condition,
                        seed,
                        {
                            "prediction_error_mode": error_mode,
                            "prediction_error_value": signal_value,
                            "prediction_error_enabled": error_mode != "disabled",
                            "prediction_error_weight_updates": changed,
                            "reward_enabled_condition": reward_on,
                            "reward_calls": reward_calls,
                            "final_weight": final_weight,
                            "weight_delta": final_weight - 0.5,
                            "eligibility_nonzero": abs(
                                learning.get_eligibility(
                                    pre_id, post_id, post_result.tick
                                )
                            )
                            > 0.0,
                            "reward_path_called_by_pe": False,
                            "snn_involved": True,
                            "scientific_evidence": False,
                            "claim_scope": "prediction_error_reward_factorial_data_only",
                        },
                        before,
                        after,
                    )
                )
    return runs


def _wm_action(name: str) -> StateAction:
    return StateAction(name, {})


def _wm_next(position: int, action: str) -> int:
    if action == "right":
        return min(4, position + 1)
    return max(0, position - 1)


def _train_multistep_model(*, shuffled: bool = False) -> ActionConditionedWorldModel:
    model = ActionConditionedWorldModel(max_contexts=64)
    for position in range(5):
        for action in ("left", "right"):
            next_position = _wm_next(position, action)
            if shuffled:
                next_position = 4 - next_position
            for _ in range(3):
                model.update(
                    {"position": position},
                    _wm_action(action),
                    {"position": next_position},
                )
    return model


def run_s6_wm_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Frozen multistep hold-out evaluation against shuffled/persistence/no-model."""

    del config
    conditions = ("frozen_correct", "frozen_shuffled", "persistence", "no_model")
    runs: list[Stage6Run] = []
    horizon = 3
    trials = 20
    for seed in seeds:
        schedules = [
            tuple(
                "right" if random.Random(seed * 10000 + trial * 17 + step).random() < 0.5 else "left"
                for step in range(horizon)
            )
            for trial in range(trials)
        ]
        starts = [random.Random(seed * 313 + trial).randrange(5) for trial in range(trials)]
        for condition in conditions:
            model = _train_multistep_model(shuffled=condition == "frozen_shuffled")
            before = _digest(model.state_dict())
            completed = 0
            exact = 0
            absolute_errors: list[float] = []
            for start, schedule in zip(starts, schedules, strict=True):
                actual = start
                for action in schedule:
                    actual = _wm_next(actual, action)
                predicted: int | None
                if condition == "no_model":
                    predicted = None
                elif condition == "persistence":
                    predicted = start
                else:
                    rollout = model.rollout(
                        {"position": start},
                        tuple(_wm_action(action) for action in schedule),
                        max_steps=horizon,
                    )
                    final = rollout.final_state
                    predicted = None if final is None else int(final["position"])
                    completed += int(not rollout.terminated_early)
                if predicted is not None:
                    exact += int(predicted == actual)
                    absolute_errors.append(abs(float(predicted - actual)))
            after = _digest(model.state_dict())
            runs.append(
                Stage6Run(
                    "S6-WM-001",
                    condition,
                    seed,
                    {
                        "held_out_trials": trials,
                        "horizon": horizon,
                        "frozen_during_evaluation": True,
                        "evaluated_predictions": len(absolute_errors),
                        "completed_rollouts": completed,
                        "exact_final_state": exact,
                        "exact_final_state_rate": (
                            exact / len(absolute_errors) if absolute_errors else None
                        ),
                        "mean_absolute_final_state_error": (
                            sum(absolute_errors) / len(absolute_errors)
                            if absolute_errors
                            else None
                        ),
                        "train_test_split_digest": _digest({"starts": starts, "schedules": schedules}),
                        "scientific_evidence": False,
                        "claim_scope": "frozen_multistep_reference_data_only",
                    },
                    before,
                    after,
                )
            )
    return runs


def _decision_training(shuffled: bool = False) -> ActionConditionedWorldModel:
    model = ActionConditionedWorldModel(max_contexts=64)
    for scenario in range(8):
        start = {"node": "start", "scenario": scenario, "utility": 0}
        left_mid = {"node": "left", "scenario": scenario, "utility": 0}
        right_mid = {"node": "right", "scenario": scenario, "utility": 0}
        left_utility = 10 if scenario % 2 == 0 else 2
        right_utility = 2 if scenario % 2 == 0 else 10
        if shuffled:
            left_utility, right_utility = right_utility, left_utility
        model.update(start, _wm_action("left"), left_mid)
        model.update(start, _wm_action("right"), right_mid)
        model.update(
            left_mid,
            _wm_action("finish"),
            {"node": "goal", "scenario": scenario, "utility": left_utility},
        )
        model.update(
            right_mid,
            _wm_action("finish"),
            {"node": "goal", "scenario": scenario, "utility": right_utility},
        )
    return model


def _rollout_utility(rollout: Any) -> float:
    final = rollout.final_state
    if final is None:
        return -math.inf
    return float(final.get("utility", 0.0))


def run_s6_wm_002(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Offline choice utility with correct, disabled, shuffled and persistence controls."""

    del config
    conditions = ("correct", "disabled", "shuffled", "persistence")
    runs: list[Stage6Run] = []
    scenarios = tuple(range(8))
    for seed in seeds:
        for condition in conditions:
            model = _decision_training(shuffled=condition == "shuffled")
            before = _digest(model.state_dict())
            achieved = 0.0
            optimal = 0.0
            recommendations = 0
            for scenario in scenarios:
                left_utility = 10 if scenario % 2 == 0 else 2
                right_utility = 2 if scenario % 2 == 0 else 10
                optimal += float(max(left_utility, right_utility))
                if condition == "disabled":
                    chosen = "left" if random.Random(seed * 97 + scenario).random() < 0.5 else "right"
                elif condition == "persistence":
                    chosen = "left"
                else:
                    evaluator = OfflineDecisionEvaluator(model, _rollout_utility, max_steps=2)
                    result = evaluator.evaluate(
                        {"node": "start", "scenario": scenario, "utility": 0},
                        (
                            ActionSequenceCandidate(
                                "left", (_wm_action("left"), _wm_action("finish"))
                            ),
                            ActionSequenceCandidate(
                                "right", (_wm_action("right"), _wm_action("finish"))
                            ),
                        ),
                    )
                    chosen = result.selected_label or "left"
                    recommendations += int(result.selected_label is not None)
                achieved += float(left_utility if chosen == "left" else right_utility)
            after = _digest(model.state_dict())
            runs.append(
                Stage6Run(
                    "S6-WM-002",
                    condition,
                    seed,
                    {
                        "scenarios": len(scenarios),
                        "achieved_utility": achieved,
                        "optimal_utility": optimal,
                        "utility_ratio": achieved / optimal,
                        "recommendations": recommendations,
                        "frozen_during_evaluation": True,
                        "actuation_authority": False,
                        "scientific_evidence": False,
                        "claim_scope": "offline_decision_benefit_data_only",
                    },
                    before,
                    after,
                )
            )
    return runs


__all__ = [
    "Stage6Run",
    "run_s6_epi_001",
    "run_s6_pe_001",
    "run_s6_rpl_001",
    "run_s6_sem_001",
    "run_s6_wm_001",
    "run_s6_wm_002",
]
