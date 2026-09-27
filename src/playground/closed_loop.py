"""Closed-loop environment helpers for the non-canonical Playground.

The implementation is deliberately bounded and deterministic. It creates an
actual action -> consequence -> reward loop for Playground experiments, but it
does not make scientific, biological, cognitive, or generalization claims.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .models import PlaygroundConfig


CLOSED_LOOP_PRESETS: dict[str, dict[str, object]] = {
    "open_loop_baseline": {
        "description": "Kein Aktions-Loop, kein Ziel- oder Reward-Signal.",
        "hypothesis": "Kontrolle: Verhalten bleibt ohne kausalen Loop am Zufallsniveau.",
        "expected_success": 0.25,
        "required_features": [],
        "settings": {
            "pan_feedback_gain": 0.05,
            "action_loop_enabled": False,
            "reward_signal_enabled": False,
            "target_encoding": "none",
            "input_topology": "uniform",
            "inhibitory_fraction": 0.0,
            "neuron_threshold_variance": 0.0,
            "neuron_tau_m_variance": 0.0,
        },
    },
    "strong_feedback_only": {
        "description": "Starkes PAN-Feedback ohne Aktions- oder Reward-Loop.",
        "hypothesis": "Prueft, ob starkes Feedback allein die Dynamik differenziert.",
        "expected_success": None,
        "required_features": ["pan_feedback"],
        "settings": {
            "pan_enabled": True,
            "pan_feedback_gain": 2.0,
            "pan_feedback_nonlinearity": "tanh",
            "pan_feedback_saturation": 20.0,
            "action_loop_enabled": False,
            "reward_signal_enabled": False,
            "target_encoding": "none",
            "input_topology": "uniform",
            "inhibitory_fraction": 0.0,
        },
    },
    "differentiated_input_only": {
        "description": "Acht getrennte Eingangskanaele ohne Aktions-Loop.",
        "hypothesis": "Prueft Input-Differenzierung ohne geschlossene Kausalitaetskette.",
        "expected_success": None,
        "required_features": ["differentiated_input"],
        "settings": {
            "input_topology": "channel_partitioned",
            "input_channels": 8,
            "input_amplitude_per_channel": [8, 8, 8, 8, 4, 4, 4, 4],
            "input_frequency_per_channel": [20, 22, 24, 26, 30, 32, 34, 36],
            "input_phase_per_channel": [0, 0.25, 0.5, 0.75, 0, 0.25, 0.5, 0.75],
            "pan_feedback_gain": 0.05,
            "action_loop_enabled": False,
            "reward_signal_enabled": False,
            "target_encoding": "none",
            "inhibitory_fraction": 0.0,
        },
    },
    "minimal_closed_loop": {
        "description": "Differenzierter Input + Ziel-Cue + Aktion + Reward.",
        "hypothesis": "Prueft, ob ein minimal geschlossener Loop Lernen ueber Zufall erlaubt.",
        "expected_success": 0.5,
        "required_features": ["action_loop", "target_cue", "reward_channel"],
        "settings": {
            "neuron_model": "pan_adex_5d",
            "pan_enabled": True,
            "behavior_learning_enabled": True,
            "input_topology": "channel_partitioned",
            "input_channels": 8,
            "target_encoding": "one_hot",
            "target_cue_channel": 0,
            "target_cue_current": 30.0,
            "target_persistence": 16,
            "action_loop_enabled": True,
            "action_space_size": 4,
            "action_to_input_map": "auto",
            "action_coupling_strength": 2.0,
            "pan_feedback_gain": 1.5,
            "pan_feedback_nonlinearity": "tanh",
            "reward_signal_enabled": True,
            "reward_magnitude": 5.0,
            "reward_channel": 1,
            "inhibitory_fraction": 0.2,
            "gaba_strength": 4.0,
            "neuron_threshold_variance": 0.15,
            "neuron_tau_m_variance": 0.1,
        },
    },
    "credit_assignment": {
        "description": "Minimaler Loop plus reward-modulated eligibility traces.",
        "hypothesis": "Prueft, ob zeitliche Kreditzuweisung die Policy-Anpassung stabilisiert.",
        "expected_success": None,
        "required_features": ["action_loop", "reward_modulated_stdp"],
        "settings": {
            "closed_loop_preset": "minimal_closed_loop",
            "credit_assignment": "reward_modulated_stdp",
            "credit_window": 64,
            "eligibility_trace_tau": 200.0,
            "td_lambda": 0.9,
            "gamma_discount": 0.95,
        },
    },
    "heterogeneous_network": {
        "description": "Minimaler Loop plus E/I- und Neuronen-Heterogenitaet.",
        "hypothesis": "Prueft, ob Heterogenitaet Synchronie reduziert und Aktivitaet differenziert.",
        "expected_success": None,
        "required_features": ["heterogeneity"],
        "settings": {
            "closed_loop_preset": "minimal_closed_loop",
            "inhibitory_fraction": 0.25,
            "gaba_strength": 6.0,
            "e_i_ratio": 3.0,
            "neuron_threshold_variance": 0.3,
            "neuron_tau_m_variance": 0.2,
            "refractory_variance": 0.3,
            "delay_distribution": "lognormal",
            "delay_mean_ticks": 3.0,
            "oscillation_enabled": True,
            "oscillation_frequency": 8.0,
        },
    },
    "spatial_embodiment": {
        "description": "Heterogener Loop mit raeumlich gekoppeltem Input.",
        "hypothesis": "Prueft, ob Geometrie-Input-Kopplung messbare Embodiment-Effekte erzeugt.",
        "expected_success": None,
        "required_features": ["spatial_input", "action_loop"],
        "settings": {
            "closed_loop_preset": "heterogeneous_network",
            "input_topology": "spatial_gradient",
            "geometry_input_coupling": True,
            "geometry_input_sigma": 0.2,
            "action_to_input_map": "spatial",
        },
    },
    "full_embodiment": {
        "description": "Raeumlicher Closed Loop plus Stick-Figure-Sandbox.",
        "hypothesis": "Explorativer Gesamtsandkasten fuer sensorimotorische Kopplung.",
        "expected_success": None,
        "required_features": ["spatial_input", "action_loop", "sandbox"],
        "settings": {
            "closed_loop_preset": "spatial_embodiment",
            "sandbox_enabled": True,
            "sandbox_physics": "stick_figure",
            "sandbox_action_coupling": "direct",
            "sandbox_sensor_noise": 0.05,
        },
    },
}


def closed_loop_catalog() -> dict[str, object]:
    """Return UI-safe closed-loop capabilities and preset metadata."""

    presets = []
    for name, item in CLOSED_LOOP_PRESETS.items():
        features = cast(list[str], item["required_features"])
        settings = cast(dict[str, object], item["settings"])
        presets.append(
            {
                "name": name,
                "description": item["description"],
                "hypothesis": item["hypothesis"],
                "expected_success": item["expected_success"],
                "required_features": list(features),
                "settings": dict(settings),
            }
        )
    return {
        "classification": "PLAYGROUND_CLOSED_LOOP",
        "scientific_evidence": False,
        "runtime_status": "IMPLEMENTED_BOUNDED_REFERENCE",
        "input_topologies": [
            "uniform",
            "channel_partitioned",
            "spatial_gradient",
            "random_per_neuron",
        ],
        "feedback_sources": ["population", "layer", "subset", "hypervector"],
        "feedback_targets": ["all", "layer", "random_subset"],
        "feedback_nonlinearities": ["linear", "tanh", "sign", "clip"],
        "target_encodings": ["none", "one_hot", "rate", "population_latency"],
        "target_predictability": ["deterministic", "stochastic", "adversarial"],
        "reward_shaping": ["sparse", "dense", "potential_based"],
        "credit_assignment": ["none", "trace", "reward_modulated_stdp"],
        "delay_distributions": ["fixed", "uniform", "lognormal", "gamma"],
        "presets": presets,
        "note": (
            "Closed-loop behavior is Playground-only. Preset expectations are "
            "hypotheses, not observed results or evidence."
        ),
    }


def _expand(values: Sequence[float], count: int, default: float) -> list[float]:
    clean = [float(value) for value in values]
    if not clean:
        return [default for _ in range(count)]
    return [clean[index % len(clean)] for index in range(count)]


class ClosedLoopRuntime:
    """Deterministic channelized action/consequence/reward environment."""

    def __init__(
        self,
        config: PlaygroundConfig,
        coordinates: Sequence[Sequence[float]],
    ) -> None:
        self.config = config
        self.n_neurons = config.n_neurons
        self.channels = config.input_channels
        self.coordinates = coordinates
        self.rng = random.Random(config.seed ^ 0xC105ED)
        self.channel_map = self._build_channel_map()
        self.amplitudes = _expand(
            config.input_amplitude_per_channel,
            self.channels,
            0.0,
        )
        self.frequencies = _expand(
            config.input_frequency_per_channel,
            self.channels,
            20.0,
        )
        self.phases = _expand(
            config.input_phase_per_channel,
            self.channels,
            0.0,
        )
        self.action_history: list[int] = []
        self.target_history: list[int] = []
        self.reward_history: list[float] = []
        self.successes = 0
        self.pending_actions: list[tuple[int, int, int]] = []
        self.pending_rewards: list[tuple[int, float, int, int]] = []
        self.delivered_rewards: list[tuple[int, int, float]] = []
        self.reward_trace = 0.0
        self.last_action: int | None = None
        self.previous_action: int | None = None
        self.target_permutation = list(range(config.action_space_size))
        if config.target_shuffle:
            self.rng.shuffle(self.target_permutation)

    def _build_channel_map(self) -> list[list[int]]:
        provided = self.config.input_channel_map
        if provided:
            return [list(group) for group in provided]

        groups: list[list[int]] = [[] for _ in range(self.channels)]
        if self.config.input_topology == "uniform":
            all_neurons = list(range(self.n_neurons))
            return [list(all_neurons) for _ in range(self.channels)]

        if (
            self.config.input_topology == "spatial_gradient"
            or self.config.geometry_input_coupling
        ) and self.coordinates:
            ordered = sorted(
                range(self.n_neurons),
                key=lambda index: float(self.coordinates[index][0])
                if self.coordinates[index]
                else 0.0,
            )
        elif self.config.input_topology == "random_per_neuron":
            ordered = list(range(self.n_neurons))
            self.rng.shuffle(ordered)
        else:
            ordered = list(range(self.n_neurons))

        for position, neuron_id in enumerate(ordered):
            channel = min(
                self.channels - 1,
                (position * self.channels) // max(self.n_neurons, 1),
            )
            if self.config.input_topology == "random_per_neuron":
                channel = self.rng.randrange(self.channels)
            groups[channel].append(neuron_id)
        return groups

    def _target_for_episode(self, episode: int) -> int:
        count = self.config.action_space_size
        mode = self.config.target_predictability
        if mode == "stochastic":
            target_rng = random.Random(self.config.seed ^ 0x7A267 ^ episode)
            target = target_rng.randrange(count)
        elif mode == "adversarial":
            target = (
                (self.last_action + 1) % count
                if self.last_action is not None
                else episode % count
            )
        else:
            target = episode % count
        if self.target_permutation:
            target = self.target_permutation[target % len(self.target_permutation)]
        return target

    def current_target(self, tick: int) -> int:
        episode_ticks = max(1, self.config.behavior_episode_ticks)
        episode = tick // episode_ticks
        return self._target_for_episode(episode)

    def _target_channel_values(self, tick: int) -> list[float]:
        values = [0.0 for _ in range(self.channels)]
        if self.config.target_encoding == "none":
            return values
        episode_ticks = max(1, self.config.behavior_episode_ticks)
        phase_tick = tick % episode_ticks
        if phase_tick >= self.config.target_persistence:
            return values
        target = self.current_target(tick)
        base = self.config.target_cue_channel % self.channels
        if self.config.target_encoding == "one_hot":
            channel = (base + target) % self.channels
            values[channel] = self.config.target_cue_current
        elif self.config.target_encoding == "rate":
            values[base] = self.config.target_cue_current * (
                (target + 1) / max(self.config.action_space_size, 1)
            )
        else:
            latency = target % max(1, self.config.target_persistence)
            if phase_tick == latency:
                values[base] = self.config.target_cue_current
        return values

    def _action_vector(self, action: int) -> list[float]:
        mapping = self.config.action_to_input_map
        if not isinstance(mapping, str) and mapping:
            rows = cast(Sequence[Sequence[float]], mapping)
            row = rows[action % len(rows)]
            return _expand(row, self.channels, 0.0)

        values = [0.0 for _ in range(self.channels)]
        base = self.config.action_feedback_channel % self.channels
        if mapping == "spatial":
            center = (
                action / max(self.config.action_space_size - 1, 1)
            ) * max(self.channels - 1, 1)
            sigma = max(self.config.geometry_input_sigma * self.channels, 0.5)
            for channel in range(self.channels):
                distance = (channel - center) / sigma
                values[channel] = math.exp(-0.5 * distance * distance)
        else:
            values[(base + action) % self.channels] = 1.0
        return values

    def _channel_values(self, tick: int) -> list[float]:
        time_s = tick * self.config.dt_ms / 1000.0
        values = []
        for channel in range(self.channels):
            phase = self.phases[channel]
            angle = 2.0 * math.pi * self.frequencies[channel] * time_s + phase
            carrier = 0.5 + 0.5 * math.sin(angle)
            values.append(self.amplitudes[channel] * carrier)

        target_values = self._target_channel_values(tick)
        for channel in range(self.channels):
            values[channel] += target_values[channel]

        active_actions: list[tuple[int, int, int]] = []
        for start, end, action in self.pending_actions:
            if start <= tick < end:
                vector = self._action_vector(action)
                for channel in range(self.channels):
                    noise = (
                        self.rng.gauss(0.0, self.config.action_noise)
                        if self.config.action_noise > 0.0
                        else 0.0
                    )
                    values[channel] += self.config.action_coupling_strength * (
                        vector[channel] + noise
                    )
            if tick < end:
                active_actions.append((start, end, action))
        self.pending_actions = active_actions

        remaining_rewards: list[tuple[int, float, int, int]] = []
        for reward_tick, reward, action, target in self.pending_rewards:
            if reward_tick <= tick:
                self.reward_trace += reward
                self.delivered_rewards.append((action, target, reward))
            else:
                remaining_rewards.append((reward_tick, reward, action, target))
        self.pending_rewards = remaining_rewards

        if self.config.reward_signal_enabled and abs(self.reward_trace) > 1e-12:
            channel = self.config.reward_channel % self.channels
            values[channel] += self.reward_trace
        self.reward_trace *= self.config.reward_decay
        if abs(self.reward_trace) < 1e-9:
            self.reward_trace = 0.0
        return values

    def currents(self, tick: int) -> list[float]:
        values = self._channel_values(tick)
        currents = [0.0 for _ in range(self.n_neurons)]
        counts = [0 for _ in range(self.n_neurons)]
        for channel, neurons in enumerate(self.channel_map):
            for neuron_id in neurons:
                if 0 <= neuron_id < self.n_neurons:
                    currents[neuron_id] += values[channel]
                    counts[neuron_id] += 1
        for neuron_id in range(self.n_neurons):
            if counts[neuron_id] > 1:
                currents[neuron_id] /= counts[neuron_id]
            noise_sigma = self.config.input_noise_sigma
            if self.config.sandbox_enabled:
                noise_sigma = min(
                    1.0,
                    noise_sigma + self.config.sandbox_sensor_noise,
                )
            if noise_sigma > 0.0:
                currents[neuron_id] += self.rng.gauss(0.0, noise_sigma)
        return currents

    def _reward(self, action: int, target: int) -> float:
        magnitude = self.config.reward_magnitude
        shaping = self.config.reward_shaping
        match = action == target
        if shaping == "dense":
            distance = abs(action - target) / max(
                self.config.action_space_size - 1,
                1,
            )
            reward = magnitude * (1.0 - 2.0 * distance)
        elif shaping == "potential_based":
            current_distance = abs(action - target)
            if self.previous_action is None:
                previous_distance = self.config.action_space_size - 1
            else:
                previous_distance = abs(self.previous_action - target)
            reward = magnitude * (previous_distance - current_distance) / max(
                self.config.action_space_size - 1,
                1,
            )
            if match:
                reward += magnitude
        else:
            reward = magnitude if match else 0.0
        return reward - self.config.reward_baseline

    def note_action(self, *, action: int, tick: int) -> tuple[int, float]:
        target = self.current_target(tick)
        reward = self._reward(action, target)
        if action == target:
            self.successes += 1
        self.previous_action = self.last_action
        self.last_action = action
        self.action_history.append(action)
        self.target_history.append(target)
        self.reward_history.append(reward)

        if self.config.action_loop_enabled:
            start = tick + self.config.action_loop_delay
            end = start + self.config.action_persistence
            self.pending_actions.append((start, end, action))
        if self.config.reward_signal_enabled:
            reward_tick = tick + self.config.reward_delay_ticks
            if self.config.reward_delay_ticks == 0:
                self.reward_trace += reward
                self.delivered_rewards.append((action, target, reward))
            else:
                self.pending_rewards.append((reward_tick, reward, action, target))
        return target, reward

    def consume_delivered_rewards(self) -> list[tuple[int, int, float]]:
        rewards = list(self.delivered_rewards)
        self.delivered_rewards.clear()
        return rewards

    def summary(self) -> dict[str, object]:
        episodes = len(self.action_history)
        return {
            "classification": "PLAYGROUND_CLOSED_LOOP",
            "scientific_evidence": False,
            "preset": self.config.closed_loop_preset,
            "input_topology": self.config.input_topology,
            "input_channels": self.channels,
            "channel_sizes": [len(group) for group in self.channel_map],
            "action_loop_enabled": self.config.action_loop_enabled,
            "action_space_size": self.config.action_space_size,
            "target_encoding": self.config.target_encoding,
            "reward_signal_enabled": self.config.reward_signal_enabled,
            "reward_shaping": self.config.reward_shaping,
            "credit_assignment": self.config.credit_assignment,
            "episodes": episodes,
            "successes": self.successes,
            "success_fraction": self.successes / episodes if episodes else 0.0,
            "action_history": list(self.action_history[-128:]),
            "target_history": list(self.target_history[-128:]),
            "reward_history": list(self.reward_history[-128:]),
            "pending_action_effects": len(self.pending_actions),
            "pending_rewards": len(self.pending_rewards),
            "causal_chain": "target/input -> network -> action -> delayed input/reward",
        }


def neuron_parameter_sets(
    base: Mapping[str, float],
    config: PlaygroundConfig,
) -> list[dict[str, float]]:
    """Create deterministic per-neuron threshold/tau variation."""

    rng = random.Random(config.seed ^ 0x4E455552)
    result: list[dict[str, float]] = []
    for _ in range(config.n_neurons):
        params = {key: float(value) for key, value in base.items()}
        if "threshold" in params and config.neuron_threshold_variance > 0.0:
            sigma = max(1.0, abs(params["threshold"]) * 0.1)
            params["threshold"] += rng.gauss(
                0.0,
                sigma * config.neuron_threshold_variance,
            )
        if config.neuron_tau_m_variance > 0.0:
            factor = max(
                0.1,
                1.0 + rng.gauss(0.0, config.neuron_tau_m_variance),
            )
            for key in ("tau_m_ms", "soma_tau_ms", "dendrite_tau_ms"):
                if key in params:
                    params[key] = max(0.05, params[key] * factor)
        result.append(params)
    return result


def inhibitory_mask(
    n_neurons: int,
    fraction: float,
    seed: int,
) -> list[bool]:
    rng = random.Random(seed ^ 0x1A11B17)
    order = list(range(n_neurons))
    rng.shuffle(order)
    count = int(round(n_neurons * fraction))
    selected = set(order[:count])
    return [index in selected for index in range(n_neurons)]


def sample_delay_ticks(
    config: PlaygroundConfig,
    rng: random.Random,
) -> int:
    """Sample one bounded synaptic delay according to the configured family."""

    mode = config.delay_distribution
    mean = max(1.0, config.delay_mean_ticks)
    if mode == "uniform":
        value = rng.uniform(1.0, max(1.0, 2.0 * mean - 1.0))
    elif mode == "lognormal":
        sigma = 0.5
        mu = math.log(mean) - 0.5 * sigma * sigma
        value = rng.lognormvariate(mu, sigma)
    elif mode == "gamma":
        value = rng.gammavariate(2.0, mean / 2.0)
    else:
        value = float(config.delay_ticks)
    return max(1, min(64, int(round(value))))


class TemporalDynamics:
    """Small deterministic refractory/adaptation/oscillation reference."""

    def __init__(self, config: PlaygroundConfig) -> None:
        self.config = config
        self.rng = random.Random(config.seed ^ 0x71AE)
        self.refractory_until = [-1 for _ in range(config.n_neurons)]
        self.adaptation = [0.0 for _ in range(config.n_neurons)]
        self.refractory_ticks = []
        for _ in range(config.n_neurons):
            jitter = self.rng.gauss(0.0, config.refractory_variance)
            self.refractory_ticks.append(max(1, int(round(1.0 + 2.0 * jitter))))

    def begin_tick(self) -> None:
        if self.config.adaptation_strength <= 0.0:
            return
        decay = math.exp(
            -self.config.dt_ms / max(self.config.adaptation_tau, 1e-6)
        )
        self.adaptation = [value * decay for value in self.adaptation]

    def can_step(self, neuron_id: int, tick: int) -> bool:
        return tick > self.refractory_until[neuron_id]

    def current_adjustment(self, neuron_id: int, tick: int) -> float:
        current = -self.config.adaptation_strength * self.adaptation[neuron_id]
        if self.config.oscillation_enabled:
            time_s = tick * self.config.dt_ms / 1000.0
            current += math.sin(
                2.0 * math.pi * self.config.oscillation_frequency * time_s
            )
        return current

    def note_spikes(self, spiked_neurons: Sequence[int], tick: int) -> None:
        for neuron_id in spiked_neurons:
            self.refractory_until[neuron_id] = (
                tick + self.refractory_ticks[neuron_id]
            )
            self.adaptation[neuron_id] += 1.0

    def summary(self) -> dict[str, object]:
        return {
            "classification": "PLAYGROUND_TEMPORAL_DYNAMICS",
            "scientific_evidence": False,
            "refractory_variance": self.config.refractory_variance,
            "adaptation_strength": self.config.adaptation_strength,
            "adaptation_tau_ms": self.config.adaptation_tau,
            "oscillation_enabled": self.config.oscillation_enabled,
            "oscillation_frequency_hz": self.config.oscillation_frequency,
            "mean_refractory_ticks": sum(self.refractory_ticks)
            / max(len(self.refractory_ticks), 1),
        }
