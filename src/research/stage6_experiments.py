"""Deterministic Stage-6 functional experiment runners.

The runners in this module generate DATA only. They exercise the real SNN where
that distinction matters and keep technical controls explicit. No successful run
promotes an RQ or hypothesis to accepted evidence automatically.
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
    experiment_id: str
    condition: str
    seed: int
    metrics: dict[str, Any]
    state_digest_before: str
    state_digest_after: str
    runtime_error: str | None = None


def _digest(value: object) -> str:
    raw = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _condition_seed(seed: int, condition: str) -> int:
    raw = hashlib.sha256(condition.encode("utf-8")).digest()
    return seed ^ int.from_bytes(raw[:4], "big")


def _coord(index: int) -> tuple[int, int, int, int, int]:
    values: list[int] = []
    remaining = index
    for _ in range(5):
        values.append(remaining % 8)
        remaining //= 8
    return (values[0], values[1], values[2], values[3], values[4])


def _network(seed: int, neuron_count: int) -> tuple[NeuralNetwork, tuple[int, ...]]:
    if type(neuron_count) is not int or not 0 < neuron_count <= 256:
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
        "neuron": {"a": 0.02, "b": 0.2, "c": -65.0, "d": 8.0},
        "energy": {"initial": 1.0, "spike_cost": 0.001, "affects_firing": False},
        "topology": {
            "allow_self_connections": False,
            "allow_parallel_connections": False,
        },
    }
    network = NeuralNetwork(values, random.Random(seed))
    ids = tuple(network.add_neuron(_coord(index)) for index in range(neuron_count))
    return network, ids


def _pulse(
    network: NeuralNetwork,
    neuron_ids: Sequence[int],
    *,
    current: float = 100.0,
) -> tuple[int, ...]:
    network.inject_current_batch({neuron_id: current for neuron_id in neuron_ids})
    return network.step().spike_ids


def _idle(network: NeuralNetwork, steps: int) -> None:
    for _ in range(steps):
        network.step()


def _decode_binary(
    pattern: Sequence[int],
    class_a: Sequence[int],
    class_b: Sequence[int],
) -> str | None:
    spikes = set(pattern)
    a = len(spikes.intersection(class_a))
    b = len(spikes.intersection(class_b))
    if a == b:
        return None
    return "A" if a > b else "B"


def _chance(seed: int, index: int) -> str:
    return "A" if random.Random(seed * 104729 + index * 7919).random() < 0.5 else "B"


def run_s6_epi_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """SNN key/value recall after distractors without reading stored payload answers."""

    del config
    runs: list[Stage6Run] = []
    conditions = ("intact", "read_off", "write_off", "episode_shuffle")
    trials = 12
    delay_steps = 6
    for seed in seeds:
        targets = [
            "A" if random.Random(seed * 1009 + trial).random() < 0.5 else "B"
            for trial in range(trials)
        ]
        for condition in conditions:
            network, ids = _network(_condition_seed(seed, condition), 24)
            keys = ids[:trials]
            class_a = ids[12:15]
            class_b = ids[15:18]
            distractors = ids[18:24]
            memory = NeuralEpisodicMemory(
                run_id=f"s6-epi-{seed}-{condition}",
                capacity=32,
                retention_ticks=4096,
                read_enabled=condition != "read_off",
                write_enabled=condition != "write_off",
            )
            before = _digest({"memory": memory.state_dict(), "tick": network.current_tick})
            correct = 0
            retrievals = 0
            distractor_spikes = 0
            for trial, target in enumerate(targets):
                memory.reset_episode(f"trial-{trial}")
                value_ids = class_a if target == "A" else class_b
                encoded = _pulse(network, (keys[trial], *value_ids))
                memory.record(
                    {"spike_ids": encoded},
                    SensorFrame(
                        "s6-epi",
                        network.current_tick - 1,
                        "neural_key_value",
                        {"phase": "encoding", "trial": trial},
                    ),
                    None,
                )
                for offset in range(delay_steps):
                    first = distractors[(trial + offset) % len(distractors)]
                    second = distractors[(trial + offset + 2) % len(distractors)]
                    distractor_spikes += len(_pulse(network, (first, second)))
                query = _pulse(network, (keys[trial],))
                matches = memory.recall(
                    query,
                    sensor_id="s6-epi",
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
                        item
                        for item in memory.episodes
                        if item.episode_id != selected_episode.episode_id
                    ]
                    selected_episode = (
                        alternatives[(seed + trial) % len(alternatives)]
                        if alternatives
                        else None
                    )
                selected = (
                    None
                    if selected_episode is None
                    else _decode_binary(selected_episode.spike_ids, class_a, class_b)
                )
                if selected is None:
                    selected = _chance(seed, trial)
                correct += int(selected == target)
                _idle(network, 2)
            after = _digest(
                {
                    "memory": memory.state_dict(),
                    "tick": network.current_tick,
                    "spikes": network.total_spikes,
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
                        "stored_episodes": len(memory.episodes),
                        "distractor_spikes": distractor_spikes,
                        "snn_involved": True,
                        "target_in_memory_payload": False,
                        "answer_reads_payload": False,
                        "answer_reads_actual_state": False,
                        "scientific_evidence": False,
                        "claim_scope": "neural_episodic_functional_data_only",
                    },
                    before,
                    after,
                )
            )
    return runs


def _episode(
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
        frame_payload={"phase": "probe", "episode": episode_id},
        actual_state=None,
    )


def run_s6_sem_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Cross-episode prototype learning with disjoint held-out neural episodes."""

    del config
    runs: list[Stage6Run] = []
    conditions = ("intact", "label_shuffle", "no_semantic")
    train_per_class = 6
    holdout_per_class = 4
    for seed in seeds:
        for condition in conditions:
            network, ids = _network(_condition_seed(seed + 2000, condition), 48)
            class_a = ids[0:3]
            class_b = ids[3:6]
            nuisance = ids[6:40]
            semantic = SemanticMemory(
                max_concepts=8,
                min_episode_support=2,
                prototype_support=0.6,
                match_threshold=0.45,
            )
            before = _digest(semantic.state_dict())
            targets = ["A", "B"] * train_per_class
            encoded_targets = list(targets)
            if condition == "label_shuffle":
                random.Random(seed ^ 0x5E6A).shuffle(encoded_targets)
            training: list[NeuralEpisode] = []
            for index, encoded_target in enumerate(encoded_targets):
                core = class_a if encoded_target == "A" else class_b
                pattern = _pulse(network, (*core, nuisance[index]))
                training.append(
                    _episode(
                        f"s6-sem-{seed}-{condition}",
                        f"train-{index}",
                        network.current_tick - 1,
                        pattern,
                    )
                )
                _idle(network, 3)
            updates = 0 if condition == "no_semantic" else semantic.consolidate(training)
            correct = 0
            matched = 0
            heldout = ["A", "B"] * holdout_per_class
            for offset, target in enumerate(heldout):
                core = class_a if target == "A" else class_b
                pattern = _pulse(network, (*core, nuisance[len(training) + offset]))
                matches = semantic.query(
                    pattern,
                    sensor_id="s6-semantic",
                    modality="neural_concept",
                    limit=1,
                )
                predicted: str | None = None
                if matches:
                    matched += 1
                    predicted = _decode_binary(
                        matches[0].concept.prototype_spike_ids,
                        class_a,
                        class_b,
                    )
                if predicted is None:
                    predicted = _chance(seed + 1, offset)
                correct += int(predicted == target)
                _idle(network, 3)
            after = _digest(semantic.state_dict())
            runs.append(
                Stage6Run(
                    "S6-SEM-001",
                    condition,
                    seed,
                    {
                        "training_episodes": len(training),
                        "held_out_episodes": len(heldout),
                        "train_eval_episode_overlap": 0,
                        "semantic_updates": updates,
                        "mature_concepts": len(semantic.mature_concepts),
                        "matched_holdout": matched,
                        "correct": correct,
                        "accuracy": correct / len(heldout),
                        "snn_involved": True,
                        "held_out": True,
                        "answer_reads_payload": False,
                        "scientific_evidence": False,
                        "claim_scope": "semantic_generalization_data_only",
                    },
                    before,
                    after,
                )
            )
    return runs


def _replay_source(seed: int) -> tuple[NeuralEpisode, ...]:
    network, ids = _network(seed + 3000, 32)
    class_a = ids[0:3]
    class_b = ids[3:6]
    nuisance = ids[6:20]
    episodes: list[NeuralEpisode] = []
    for index in range(12):
        core = class_a if index % 2 == 0 else class_b
        pattern = _pulse(network, (*core, nuisance[index]))
        episodes.append(
            _episode(
                f"s6-rpl-{seed}",
                f"episode-{index}",
                network.current_tick - 1,
                pattern,
            )
        )
        _idle(network, 2)
    return tuple(episodes)


def _reactivate(network: NeuralNetwork, episode: NeuralEpisode) -> float:
    expected = set(episode.spike_ids)
    observed = set(_pulse(network, episode.spike_ids))
    if not expected:
        return 0.0
    return len(expected.intersection(observed)) / len(expected)


def run_s6_rpl_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Replay/no-replay/shuffle/equal-awake comparison with matched SNN steps."""

    del config
    runs: list[Stage6Run] = []
    conditions = ("no_replay", "ordered", "shuffled", "equal_budget_awake")
    budget = 8
    step_budget = budget * 2
    for seed in seeds:
        source = _replay_source(seed)
        scheduler = EpisodicReplayScheduler(max_events=budget)
        for condition in conditions:
            network, _ = _network(_condition_seed(seed + 4000, condition), 32)
            semantic = SemanticMemory(
                max_concepts=8,
                min_episode_support=2,
                prototype_support=0.6,
                match_threshold=0.45,
            )
            before = _digest({"semantic": semantic.state_dict(), "tick": network.current_tick})
            if condition == "ordered":
                selected = scheduler.plan(
                    source,
                    mode=ReplayMode.ORDERED,
                    budget=budget,
                    seed=seed,
                ).selected
            elif condition == "shuffled":
                selected = scheduler.plan(
                    source,
                    mode=ReplayMode.SHUFFLED,
                    budget=budget,
                    seed=seed,
                ).selected
            elif condition == "equal_budget_awake":
                selected = source[-budget:]
            else:
                selected = ()
            fidelities: list[float] = []
            if selected:
                for episode in selected:
                    fidelities.append(_reactivate(network, episode))
                    _idle(network, 1)
                semantic.consolidate(selected)
            else:
                _idle(network, step_budget)
            steps_used = network.current_tick
            after = _digest(
                {
                    "semantic": semantic.state_dict(),
                    "tick": steps_used,
                    "spikes": network.total_spikes,
                }
            )
            runs.append(
                Stage6Run(
                    "S6-RPL-001",
                    condition,
                    seed,
                    {
                        "episode_budget": budget,
                        "snn_step_budget": step_budget,
                        "snn_steps_used": steps_used,
                        "budget_matched": steps_used == step_budget,
                        "selected_episodes": len(selected),
                        "mean_reactivation_fidelity": (
                            sum(fidelities) / len(fidelities) if fidelities else None
                        ),
                        "mature_concepts": len(semantic.mature_concepts),
                        "ordered_replay": condition == "ordered",
                        "shuffled_replay": condition == "shuffled",
                        "additional_awake_control": condition == "equal_budget_awake",
                        "simulated_sleep_claim": False,
                        "snn_involved": True,
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
    """Prediction-error correct/disabled/shuffled crossed with reward on/off."""

    del config
    runs: list[Stage6Run] = []
    for seed in seeds:
        for pe_mode in ("correct", "disabled", "shuffled"):
            for reward_on in (False, True):
                condition = f"pe_{pe_mode}__reward_{'on' if reward_on else 'off'}"
                values = _plasticity_config()
                network = NeuralNetwork(values, random.Random(seed))
                pre_id = network.add_neuron((0, 0, 0, 0, 0))
                post_id = network.add_neuron((1, 0, 0, 0, 0))
                network.connect(pre_id, post_id, 0.5, 1)
                learning = LearningEngine(network, values)
                modulator = PredictionErrorPlasticity(
                    learning,
                    PredictionErrorPlasticityConfig(
                        enabled=pe_mode != "disabled",
                        learning_rate=0.05,
                    ),
                )
                before = _digest({"weight": network.synapses[pre_id][0].weight})
                network.inject_current(pre_id, 100.0)
                learning.update(network.step())
                for _ in range(4):
                    learning.update(network.step())
                network.inject_current(post_id, 100.0)
                post_result = network.step()
                learning.update(post_result)
                reward_calls = 0
                if reward_on:
                    learning.set_reward(1.0, post_result.tick)
                    reward_calls = 1
                pe_value = 1.0
                if pe_mode == "shuffled":
                    pe_value = -1.0 if random.Random(seed ^ 0xE770).random() < 0.5 else 1.0
                pe_updates = modulator.apply(
                    PredictionErrorSignal(pe_value, post_result.tick)
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
                            "prediction_error_mode": pe_mode,
                            "prediction_error_value": pe_value,
                            "prediction_error_updates": pe_updates,
                            "reward_on": reward_on,
                            "reward_calls": reward_calls,
                            "reward_path_called_by_pe": False,
                            "final_weight": final_weight,
                            "weight_delta": final_weight - 0.5,
                            "eligibility_nonzero": abs(
                                learning.get_eligibility(
                                    pre_id,
                                    post_id,
                                    post_result.tick,
                                )
                            )
                            > 0.0,
                            "snn_involved": True,
                            "scientific_evidence": False,
                            "claim_scope": "prediction_error_reward_factorial_data_only",
                        },
                        before,
                        after,
                    )
                )
    return runs


def _action(name: str) -> StateAction:
    return StateAction(name, {})


def _next_position(position: int, action: str) -> int:
    return min(4, position + 1) if action == "right" else max(0, position - 1)


def _position_model(*, shuffled: bool = False) -> ActionConditionedWorldModel:
    model = ActionConditionedWorldModel(max_contexts=64)
    for position in range(5):
        for action in ("left", "right"):
            following = _next_position(position, action)
            if shuffled:
                following = 4 - following
            for _ in range(3):
                model.update(
                    {"position": position},
                    _action(action),
                    {"position": following},
                )
    return model


def run_s6_wm_001(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Frozen multi-step hold-out prediction against explicit controls."""

    del config
    runs: list[Stage6Run] = []
    conditions = ("frozen_correct", "frozen_shuffled", "persistence", "no_model")
    horizon = 3
    trials = 20
    for seed in seeds:
        starts = [random.Random(seed * 313 + index).randrange(5) for index in range(trials)]
        schedules = [
            tuple(
                "right"
                if random.Random(seed * 10000 + trial * 17 + step).random() < 0.5
                else "left"
                for step in range(horizon)
            )
            for trial in range(trials)
        ]
        split_digest = _digest({"starts": starts, "schedules": schedules})
        for condition in conditions:
            model = _position_model(shuffled=condition == "frozen_shuffled")
            before = _digest(model.state_dict())
            errors: list[float] = []
            exact = 0
            completed = 0
            for start, schedule in zip(starts, schedules, strict=True):
                actual = start
                for action in schedule:
                    actual = _next_position(actual, action)
                if condition == "no_model":
                    predicted: int | None = None
                elif condition == "persistence":
                    predicted = start
                else:
                    rollout = model.rollout(
                        {"position": start},
                        tuple(_action(action) for action in schedule),
                        max_steps=horizon,
                    )
                    final = rollout.final_state
                    predicted = None if final is None else int(final["position"])
                    completed += int(not rollout.terminated_early)
                if predicted is not None:
                    exact += int(predicted == actual)
                    errors.append(abs(float(predicted - actual)))
            after = _digest(model.state_dict())
            runs.append(
                Stage6Run(
                    "S6-WM-001",
                    condition,
                    seed,
                    {
                        "held_out_trials": trials,
                        "horizon": horizon,
                        "train_test_split_digest": split_digest,
                        "frozen_during_evaluation": True,
                        "evaluated_predictions": len(errors),
                        "completed_rollouts": completed,
                        "exact_final_state_rate": (
                            exact / len(errors) if errors else None
                        ),
                        "mean_absolute_final_state_error": (
                            sum(errors) / len(errors) if errors else None
                        ),
                        "scientific_evidence": False,
                        "claim_scope": "frozen_multistep_reference_data_only",
                    },
                    before,
                    after,
                )
            )
    return runs


def _decision_model(*, shuffled: bool = False) -> ActionConditionedWorldModel:
    model = ActionConditionedWorldModel(max_contexts=64)
    for scenario in range(8):
        start = {"node": "start", "scenario": scenario, "utility": 0}
        left = {"node": "left", "scenario": scenario, "utility": 0}
        right = {"node": "right", "scenario": scenario, "utility": 0}
        left_utility = 10 if scenario % 2 == 0 else 2
        right_utility = 2 if scenario % 2 == 0 else 10
        if shuffled:
            left_utility, right_utility = right_utility, left_utility
        model.update(start, _action("left"), left)
        model.update(start, _action("right"), right)
        model.update(
            left,
            _action("finish"),
            {"node": "goal", "scenario": scenario, "utility": left_utility},
        )
        model.update(
            right,
            _action("finish"),
            {"node": "goal", "scenario": scenario, "utility": right_utility},
        )
    return model


def _utility(rollout: Any) -> float:
    final = rollout.final_state
    if final is None:
        return -math.inf
    return float(final.get("utility", 0.0))


def run_s6_wm_002(
    config: Config,
    seeds: tuple[int, ...] = (101, 102, 103),
) -> list[Stage6Run]:
    """Offline decision benefit with correct/disabled/shuffled/persistence controls."""

    del config
    runs: list[Stage6Run] = []
    conditions = ("correct", "disabled", "shuffled", "persistence")
    scenarios = tuple(range(8))
    for seed in seeds:
        for condition in conditions:
            model = _decision_model(shuffled=condition == "shuffled")
            before = _digest(model.state_dict())
            achieved = 0.0
            optimal = 0.0
            recommendations = 0
            for scenario in scenarios:
                left_utility = 10 if scenario % 2 == 0 else 2
                right_utility = 2 if scenario % 2 == 0 else 10
                optimal += float(max(left_utility, right_utility))
                if condition == "disabled":
                    chosen = (
                        "left"
                        if random.Random(seed * 97 + scenario).random() < 0.5
                        else "right"
                    )
                elif condition == "persistence":
                    chosen = "left"
                else:
                    evaluator = OfflineDecisionEvaluator(model, _utility, max_steps=2)
                    recommendation = evaluator.evaluate(
                        {"node": "start", "scenario": scenario, "utility": 0},
                        (
                            ActionSequenceCandidate(
                                "left",
                                (_action("left"), _action("finish")),
                            ),
                            ActionSequenceCandidate(
                                "right",
                                (_action("right"), _action("finish")),
                            ),
                        ),
                    )
                    chosen = recommendation.selected_label or "left"
                    recommendations += int(recommendation.selected_label is not None)
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


RUNNERS = {
    "s6_epi_001_v1": run_s6_epi_001,
    "s6_sem_001_v1": run_s6_sem_001,
    "s6_rpl_001_v1": run_s6_rpl_001,
    "s6_pe_001_v1": run_s6_pe_001,
    "s6_wm_001_v1": run_s6_wm_001,
    "s6_wm_002_v1": run_s6_wm_002,
}

__all__ = [
    "RUNNERS",
    "Stage6Run",
    "run_s6_epi_001",
    "run_s6_pe_001",
    "run_s6_rpl_001",
    "run_s6_sem_001",
    "run_s6_wm_001",
    "run_s6_wm_002",
]
