"""Cue-conditioned policy learning, causal credit and negative controls."""

from copy import deepcopy

import pytest

from src.playground import PlaygroundConfig
from src.playground.closed_loop import ClosedLoopRuntime
from src.playground.pan import BehavioralLearningEngine
from src.playground.service import run


def test_contexts_learn_arbitrary_action_mapping_from_reward() -> None:
    learner = BehavioralLearningEngine(n_neurons=8, epsilon=0.1, learning_rate=0.3)
    learner.activity = [0.2, 0.3, 0.8, 0.1]
    targets = [2, 0, 3, 1]
    success = []
    for episode in range(1200):
        context = f"symbol:{episode % 4}"
        target = targets[episode % 4]
        learner.activate_context(context, 4)
        action = learner.choose_action()
        learner.apply_external_reward(
            context=context,
            action=action,
            target=target,
            reward=1.0 if action == target else -0.25,
        )
        success.append(action == target)
    assert sum(success[-400:]) / 400 > 0.85
    assert sum(success[-400:]) > sum(success[:400])
    assert learner.policy == [0.0] * 4
    assert len(learner.context_policies) == 4


def test_delayed_reward_uses_original_context_and_features() -> None:
    learner = BehavioralLearningEngine(n_neurons=8, learning_rate=0.3)
    learner.activate_context("old", 4)
    learner.activate_context("new", 4)
    other = deepcopy(learner.context_weights["new"])
    learner.activity = [0.0, 1.0, 0.0, 0.0]
    learner.apply_external_reward(
        context="old",
        action=2,
        target=2,
        reward=1.0,
        activity=[1.0, 0.0, 0.0, 0.0],
    )
    assert learner.active_context == "new"
    assert learner.context_weights["new"] == other
    assert learner.context_weights["old"][2][0] > 0.0
    assert learner.context_weights["old"][2][1] == 0.0
    assert learner.context_updates == {"old": 1}


@pytest.mark.parametrize("encoding", ["one_hot", "rate", "population_latency"])
def test_cue_memory_is_observable_and_resets_each_episode(encoding: str) -> None:
    config = PlaygroundConfig.from_mapping(
        {
            "closed_loop_preset": "pan_full_balanced",
            "target_encoding": encoding,
            "behavior_episode_ticks": 8,
            "target_persistence": 4,
            "target_shuffle": False,
        }
    )
    loop = ClosedLoopRuntime(config, [])
    loop.currents(0)
    first = loop.observed_context
    assert first is not None
    loop.currents(7)
    assert loop.observed_context == first
    loop.currents(8)
    if encoding == "population_latency":
        assert loop.observed_context is None
        loop.currents(9)
    assert loop.observed_context is not None
    assert loop.observed_context != first


@pytest.mark.parametrize(
    "overrides", [{"target_encoding": "none"}, {"target_cue_current": 0.0}]
)
def test_hidden_targets_do_not_create_contexts(overrides: dict[str, object]) -> None:
    result = run(
        {
            "closed_loop_preset": "pan_full_balanced",
            "n_neurons": 32,
            "edge_budget": 64,
            "ticks": 128,
            "persist": False,
            **overrides,
        }
    )
    assert result["behavioral_learning"]["context_policies"] == {}
    assert result["behavioral_learning"]["active_context"] is None


def test_silent_context_cannot_receive_learning_credit() -> None:
    learner = BehavioralLearningEngine(n_neurons=8)
    learner.activate_context("cue", 4)
    before = deepcopy(learner.context_policies)
    assert (
        learner.apply_external_reward(context="cue", action=0, target=0, reward=1) == 0
    )
    assert learner.context_policies == before
    assert learner.policy_updates == 0
    assert learner.insufficient_activity_episodes == 1


@pytest.mark.parametrize(
    "preset,count", [("g1_two_action_simple", 2), ("g2_one_action_trivial", 1)]
)
def test_sanity_presets_use_fixed_target_and_actual_action_count(
    preset: str, count: int
) -> None:
    config = PlaygroundConfig.from_mapping({"closed_loop_preset": preset})
    assert config.action_space_size == config.behavior_action_count == count
    loop = ClosedLoopRuntime(config, [])
    assert {loop.current_target(tick) for tick in range(2000)} == {0}


def test_delayed_closed_loop_credits_each_recorded_cue() -> None:
    result = run(
        {
            "closed_loop_preset": "pan_full_balanced",
            "n_neurons": 32,
            "edge_budget": 64,
            "ticks": 256,
            "behavior_episode_ticks": 8,
            "reward_delay_ticks": 17,
            "persist": False,
        }
    )
    loop = result["closed_loop"]
    behavior = result["behavioral_learning"]
    assert sum(behavior["context_updates"].values()) == behavior["policy_updates"]
    assert behavior["episodes"] == loop["episodes"] - loop["pending_rewards"]
    assert behavior["target_history"] == loop["target_history"][: behavior["episodes"]]
    assert len(behavior["context_policies"]) == 4


@pytest.mark.parametrize(
    "preset,threshold",
    [
        ("pan_full_balanced", 0.4),
        ("g1_two_action_simple", 0.9),
        ("g2_one_action_trivial", 1.0),
    ],
)
def test_end_to_end_learning_sanity(preset: str, threshold: float) -> None:
    result = run(
        {
            "closed_loop_preset": preset,
            "n_neurons": 32,
            "edge_budget": 64,
            "ticks": 2000,
            "persist": False,
        }
    )
    assert result["closed_loop"]["success_fraction"] >= threshold
    assert result["behavioral_learning"]["policy_updates"] > 0
