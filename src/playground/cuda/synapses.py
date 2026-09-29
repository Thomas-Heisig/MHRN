"""Ordered scalar synapse oracle for the bounded CUDA plasticity reference."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.runtime.determinism import release_uniform, ring_slot

if TYPE_CHECKING:
    from .recurrent import RecurrentInputs


@dataclass(frozen=True)
class SynapseConfig:
    stdp: bool = True
    stp: bool = True
    reward_modulated: bool = True
    seed: int = 12345
    learning_rate: float = 0.2
    weight_decay: float = 0.001
    weight_max: float = 20.0
    eligibility_tau: float = 100.0
    credit_window: int = 64
    td_lambda: float = 0.9
    gamma: float = 0.99

    def parameters(self) -> list[float]:
        return [
            float(self.stdp),
            float(self.stp),
            float(self.reward_modulated),
            float(self.seed),
            self.learning_rate,
            self.weight_decay,
            self.weight_max,
            self.eligibility_tau,
            float(self.credit_window),
            self.td_lambda,
            self.gamma,
        ]

    def validate(self) -> None:
        if any(
            type(value) is not bool
            for value in (self.stdp, self.stp, self.reward_modulated)
        ):
            raise ValueError("synapse mode flags must be boolean")
        if type(self.seed) is not int or not 0 <= self.seed <= 0xFFFFFFFF:
            raise ValueError("synapse seed must be uint32")
        if type(self.credit_window) is not int or not 0 <= self.credit_window <= 2000:
            raise ValueError("credit_window must be in [0,2000]")
        for name, value, low, high in (
            ("learning_rate", self.learning_rate, 0.0, 1.0),
            ("weight_decay", self.weight_decay, 0.0, 1.0),
            ("weight_max", self.weight_max, 0.001, 100.0),
            ("eligibility_tau", self.eligibility_tau, 0.001, 10000.0),
            ("td_lambda", self.td_lambda, 0.0, 1.0),
            ("gamma", self.gamma, 0.0, 1.0),
        ):
            if (
                isinstance(value, bool)
                or not math.isfinite(value)
                or not low <= value <= high
            ):
                raise ValueError(f"invalid synapse {name}")



class SynapseState:
    def __init__(self, inputs: RecurrentInputs, config: SynapseConfig) -> None:
        self.inputs = inputs
        self.config = config
        self.weights = list(inputs.weights)
        self.eligibility = [0.0] * len(inputs.sources)
        self.available = [1.0] * len(inputs.sources)
        self.last_event = [-10_000_000] * len(inputs.sources)
        self.last_spike = [-10_000_000] * inputs.n_neurons
        self.ring_size = max(inputs.delays, default=1) + 1
        self.emitted = [[0.0] * len(inputs.sources) for _ in range(self.ring_size)]

    def incoming(self, tick: int, neuron: int) -> float:
        # Kept for external callers; the membrane oracle sums in edge order.
        return sum(
            self.edge_current(tick, edge)
            for edge in range(
                self.inputs.offsets[neuron], self.inputs.offsets[neuron + 1]
            )
        )

    def edge_current(self, tick: int, edge: int) -> float:
        previous = tick - self.inputs.delays[edge]
        return self.emitted[ring_slot(previous, self.ring_size)][edge] if previous >= 0 else 0.0

    def update(self, tick: int, spikes: list[int], reward: float) -> None:
        c, inputs = self.config, self.inputs
        for target in range(inputs.n_neurons):
            for edge in range(inputs.offsets[target], inputs.offsets[target + 1]):
                source = inputs.sources[edge]
                pre, post = spikes[source], spikes[target]
                weight = self.weights[edge]
                eligibility = self.eligibility[edge] * math.exp(
                    -inputs.dt_ms / c.eligibility_tau
                )
                # Match ascending-neuron pair-rule ordering, including self edges.
                operations = ("pre", "post") if source <= target else ("post", "pre")
                for operation in operations:
                    if operation == "pre" and pre:
                        if c.stdp and 0 < tick - self.last_spike[target] <= 20:
                            weight = max(0.0, weight - 0.08)
                        eligibility -= 0.5
                    if operation == "post" and post:
                        if c.stdp and 0 < tick - self.last_spike[source] <= 20:
                            weight = min(100.0, weight + 0.1)
                        eligibility += 1.0
                if pre or post:
                    self.last_event[edge] = tick
                if (
                    c.reward_modulated
                    and tick - self.last_event[edge] <= c.credit_window
                ):
                    weight = min(
                        100.0,
                        max(
                            0.0,
                            weight
                            + c.learning_rate
                            * c.td_lambda
                            * c.gamma
                            * eligibility
                            * reward,
                        ),
                    )
                amplitude = weight if pre else 0.0
                available = self.available[edge]
                if c.stp:
                    if pre:
                        amplitude *= float(
                            release_uniform(c.seed, tick, edge)
                            < min(0.95, 0.25 + 0.7 * available)
                        )
                        available = max(0.1, available * 0.72)
                    available = min(1.0, available + 0.025)
                self.available[edge] = available
                self.emitted[ring_slot(tick, self.ring_size)][edge] = amplitude
                self.weights[edge] = min(
                    c.weight_max, max(0.0, weight * (1.0 - c.weight_decay))
                )
                self.eligibility[edge] = eligibility
        for neuron, spike in enumerate(spikes):
            if spike:
                self.last_spike[neuron] = tick
