"""Bounded behavior/policy learning for the non-canonical PAN Playground."""

from __future__ import annotations

import math
import random
from collections.abc import Sequence


class BehavioralLearningEngine:
    """Learn an action policy from population activity and scalar reward.

    This reference learner stores policy parameters and traces, not raw external
    payloads. It is deliberately small and deterministic for Playground use.
    """

    def __init__(
        self,
        *,
        n_neurons: int,
        action_count: int = 4,
        learning_rate: float = 0.05,
        epsilon: float = 0.05,
        target_action: int = 0,
        target_mode: str = "cycle",
        min_activity: float = 0.01,
        episode_ticks: int = 16,
        bias_current: float = 3.0,
        seed: int = 0,
        output_neurons: Sequence[int] | None = None,
    ) -> None:
        if n_neurons < 1:
            raise ValueError("n_neurons must be positive")
        if not 1 <= action_count <= 32:
            raise ValueError("action_count must be between 1 and 32")
        if not 0.0 < learning_rate <= 1.0:
            raise ValueError("learning_rate must be between 0 and 1")
        if not 0.0 <= epsilon <= 1.0:
            raise ValueError("epsilon must be between 0 and 1")
        if not 0 <= target_action < action_count:
            raise ValueError("target_action outside action range")
        if target_mode not in {"fixed", "cycle"}:
            raise ValueError("target_mode must be fixed or cycle")
        if not 0.0 <= min_activity <= 1.0:
            raise ValueError("min_activity must be between 0 and 1")
        if episode_ticks < 1:
            raise ValueError("episode_ticks must be positive")
        self.n_neurons = n_neurons
        self.action_count = action_count
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.target_action = target_action
        self.target_mode = target_mode
        self.min_activity = min_activity
        self.episode_ticks = episode_ticks
        self.bias_current = bias_current
        self.rng = random.Random(seed ^ 0x5A17)
        self.policy = [0.0 for _ in range(action_count)]
        self.output_neurons = list(output_neurons or range(n_neurons))
        self.activity = [0.0 for _ in range(action_count)]
        self.action_history: list[int] = []
        self.reward_history: list[float] = []
        self.policy_updates = 0
        self.correct_actions = 0
        self.insufficient_activity_episodes = 0
        self.target_history: list[int] = []
        self.context_policies: dict[str, list[float]] = {}
        self.context_weights: dict[str, list[list[float]]] = {}
        self.context_updates: dict[str, int] = {}
        self.external_reward_history: list[dict[str, object]] = []
        self.active_context: str | None = None
        self.external_reward_updates = 0

    def _bucket(self, neuron_id: int) -> int:
        if not self.output_neurons:
            return 0
        try:
            position = self.output_neurons.index(neuron_id)
        except ValueError:
            return -1
        return min(
            self.action_count - 1,
            (position * self.action_count) // max(1, len(self.output_neurons)),
        )

    def observe(self, spiked_neurons: Sequence[int]) -> None:
        instantaneous = [0.0 for _ in range(self.action_count)]
        for neuron_id in spiked_neurons:
            bucket = self._bucket(int(neuron_id))
            if bucket >= 0:
                instantaneous[bucket] += 1.0
        norm = max(1.0, max(instantaneous, default=0.0))
        for action in range(self.action_count):
            value = instantaneous[action] / norm
            self.activity[action] = 0.8 * self.activity[action] + 0.2 * value

    def choose_action(self) -> int:
        if self.rng.random() < self.epsilon:
            return self.rng.randrange(self.action_count)
        scores = [
            self.policy[action] + self.activity[action]
            for action in range(self.action_count)
        ]
        return max(
            range(self.action_count), key=lambda action: (scores[action], -action)
        )

    def apply_external_reward(
        self,
        *,
        action: int,
        reward: float,
        target: int | None = None,
        context: str | None = None,
        action_count: int | None = None,
    ) -> float:
        """Apply external reward to the base policy or a named context policy."""

        if context is not None:
            count = self.action_count if action_count is None else action_count
            if not 2 <= count <= 16:
                raise ValueError("action_count must be between 2 and 16")
            if not 0 <= action < count:
                raise ValueError("action outside context action range")
            bounded = max(-2.0, min(2.0, float(reward)))
            policy = self.context_policies.setdefault(
                context, [0.0 for _ in range(count)]
            )
            weights = self.context_weights.setdefault(
                context,
                [[0.0 for _ in range(self.action_count)] for _ in range(count)],
            )
            if len(policy) != count or len(weights) != count:
                raise ValueError("context action_count changed after initialization")
            prediction = policy[action] + sum(
                weight * feature
                for weight, feature in zip(weights[action], self.activity)
            )
            error = bounded - prediction
            policy[action] += self.learning_rate * error
            for index, feature in enumerate(self.activity):
                weights[action][index] += self.learning_rate * error * feature
            self.context_updates[context] = self.context_updates.get(context, 0) + 1
            self.external_reward_history.append(
                {"context": context, "action": action, "reward": bounded}
            )
            if len(self.external_reward_history) > 512:
                del self.external_reward_history[:-512]
            self.external_reward_updates += 1
            return policy[action]

        if not 0 <= action < self.action_count:
            raise ValueError("action outside action range")
        activity_level = max(self.activity, default=0.0)
        applied = float(reward)
        if activity_level < self.min_activity:
            applied = 0.0
            self.insufficient_activity_episodes += 1
        else:
            prediction = self.policy[action]
            self.policy[action] += self.learning_rate * (applied - prediction)
            self.policy_updates += 1
            self.external_reward_updates += 1
            if target is not None and action == target:
                self.correct_actions += 1
        if target is not None:
            self.target_history.append(int(target))
        self.action_history.append(action)
        self.reward_history.append(applied)
        return applied

    def maybe_learn(self, tick: int) -> float | None:
        if (tick + 1) % self.episode_ticks != 0:
            return None
        episode_index = len(self.action_history)
        target = (
            self.target_action
            if self.target_mode == "fixed"
            else (self.target_action + episode_index) % self.action_count
        )
        action = self.choose_action()
        reward = 1.0 if action == target else -0.25
        return self.apply_external_reward(
            action=action,
            reward=reward,
            target=target,
        )

    def choose_context_action(self, context: str, action_count: int) -> int:
        """Choose an action from a learned context policy.

        Context policies learn strategy choices (for example which source to
        search) and intentionally do not store task payloads or factual answers.
        """

        if not 2 <= action_count <= 16:
            raise ValueError("action_count must be between 2 and 16")
        policy = self.context_policies.setdefault(
            context, [0.0 for _ in range(action_count)]
        )
        weights = self.context_weights.setdefault(
            context,
            [[0.0 for _ in range(self.action_count)] for _ in range(action_count)],
        )
        self.active_context = context
        if len(policy) != action_count or len(weights) != action_count:
            raise ValueError("context action_count changed after initialization")
        if self.rng.random() < self.epsilon:
            return self.rng.randrange(action_count)
        scores = [
            policy[action]
            + sum(
                weight * feature
                for weight, feature in zip(weights[action], self.activity)
            )
            for action in range(action_count)
        ]
        return max(range(action_count), key=lambda action: (scores[action], -action))

    def activate_context(self, context: str, action_count: int) -> None:
        if not 2 <= action_count <= 16:
            raise ValueError("action_count must be between 2 and 16")
        policy = self.context_policies.setdefault(
            context, [0.0 for _ in range(action_count)]
        )
        weights = self.context_weights.setdefault(
            context,
            [[0.0 for _ in range(self.action_count)] for _ in range(action_count)],
        )
        if len(policy) != action_count or len(weights) != action_count:
            raise ValueError("context action_count changed after initialization")
        self.active_context = context

    @property
    def learning_enabled_external(self) -> bool:
        """External reward path is available whenever this learner exists."""

        return True

    def bias_currents(self) -> list[float]:
        if not self.output_neurons:
            return [0.0 for _ in range(self.n_neurons)]
        scores = [math.tanh(value) for value in self.policy]
        if self.active_context is not None:
            context_policy = self.context_policies.get(self.active_context, [])
            context_weights = self.context_weights.get(self.active_context, [])
            for action, value in enumerate(context_policy[: self.action_count]):
                contextual = 0.0
                if action < len(context_weights):
                    contextual = sum(
                        weight * feature
                        for weight, feature in zip(
                            context_weights[action], self.activity
                        )
                    )
                scores[action] += math.tanh(value + contextual)
        currents = [0.0 for _ in range(self.n_neurons)]
        for neuron_id in self.output_neurons:
            bucket = self._bucket(neuron_id)
            if bucket >= 0:
                currents[neuron_id] = self.bias_current * scores[bucket]
        return currents

    def summary(self) -> dict[str, object]:
        episodes = len(self.action_history)
        return {
            "classification": "PLAYGROUND_BEHAVIORAL_LEARNING",
            "scientific_evidence": False,
            "mode": "REWARD_MODULATED_POLICY_REFERENCE",
            "stores_raw_payloads": False,
            "stores": ["policy_parameters", "activity_traces", "reward_history"],
            "action_count": self.action_count,
            "target_action": self.target_action,
            "target_mode": self.target_mode,
            "min_activity": self.min_activity,
            "learning_rate": self.learning_rate,
            "epsilon": self.epsilon,
            "episode_ticks": self.episode_ticks,
            "policy": list(self.policy),
            "activity": list(self.activity),
            "episodes": episodes,
            "correct_actions": self.correct_actions,
            "success_fraction": self.correct_actions / episodes if episodes else 0.0,
            "action_history": list(self.action_history[-128:]),
            "reward_history": list(self.reward_history[-128:]),
            "policy_updates": self.policy_updates,
            "external_reward_updates": self.external_reward_updates,
            "insufficient_activity_episodes": self.insufficient_activity_episodes,
            "target_history": list(self.target_history[-128:]),
            "context_policies": {
                key: list(value) for key, value in self.context_policies.items()
            },
            "context_weights": {
                key: [list(row) for row in value]
                for key, value in self.context_weights.items()
            },
            "context_updates": dict(self.context_updates),
            "external_reward_history": list(self.external_reward_history[-128:]),
            "active_context": self.active_context,
        }
