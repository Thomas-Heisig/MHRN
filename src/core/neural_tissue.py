"""Experimental multi-timescale neural-tissue integration for MHRN.

This module extends the canonical neuron/synapse/network primitives without
changing their deterministic Stage-0/Stage-2 semantics. Biophysically inspired
state is kept in explicit sidecars and advanced on separate clocks:

* tick: membrane/spike transmission (owned by :mod:`src.core.network`)
* plasticity: calcium/STP/metaplastic state
* consolidation: slow tagging, confidence and resource recovery
* development: structural-plasticity proposals

The implementation is deliberately an engineering research model. Variables
such as calcium, receptor gain, ATP reserve and neuromodulator gain are bounded
surrogates; they are not claimed to reproduce a biological cell quantitatively.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from .network import NeuralNetwork, StepResult
from .synapse import Synapse


def _clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


class ConnectionRole(StrEnum):
    """Functional identity used for context and structural policies."""

    FEEDFORWARD = "feedforward"
    FEEDBACK = "feedback"
    LATERAL = "lateral"
    MODULATORY = "modulatory"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class TimescaleConfig:
    """Explicit clocks for mechanisms slower than membrane integration."""

    plasticity_interval_ticks: int = 10
    consolidation_interval_ticks: int = 1_000
    development_interval_ticks: int = 100_000

    def __post_init__(self) -> None:
        values = (
            self.plasticity_interval_ticks,
            self.consolidation_interval_ticks,
            self.development_interval_ticks,
        )
        if any(value < 1 for value in values):
            raise ValueError("all timescale intervals must be >= 1 tick")
        if self.consolidation_interval_ticks < self.plasticity_interval_ticks:
            raise ValueError("consolidation must not be faster than plasticity")
        if self.development_interval_ticks < self.consolidation_interval_ticks:
            raise ValueError("development must not be faster than consolidation")


@dataclass(frozen=True, slots=True)
class NeuralTissueConfig:
    """Research controls for the multi-timescale integration layer."""

    timescales: TimescaleConfig = field(default_factory=TimescaleConfig)
    calcium_decay: float = 0.90
    calcium_spike_increment: float = 0.25
    messenger_decay: float = 0.97
    prediction_decay: float = 0.95
    metabolic_recovery: float = 0.01
    plasticity_energy_cost: float = 0.002
    stp_recovery: float = 0.08
    stp_facilitation: float = 0.12
    vesicle_recovery: float = 0.05
    bcm_rate: float = 0.02
    confidence_rate: float = 0.02
    consolidation_rate: float = 0.05
    structural_prune_confidence: float = 0.05
    structural_grow_activity: float = 0.40
    enable_weight_updates: bool = False
    enable_structural_mutation: bool = False

    def __post_init__(self) -> None:
        bounded = {
            "calcium_decay": self.calcium_decay,
            "messenger_decay": self.messenger_decay,
            "prediction_decay": self.prediction_decay,
            "metabolic_recovery": self.metabolic_recovery,
            "stp_recovery": self.stp_recovery,
            "stp_facilitation": self.stp_facilitation,
            "vesicle_recovery": self.vesicle_recovery,
            "bcm_rate": self.bcm_rate,
            "confidence_rate": self.confidence_rate,
            "consolidation_rate": self.consolidation_rate,
            "structural_prune_confidence": self.structural_prune_confidence,
            "structural_grow_activity": self.structural_grow_activity,
        }
        for name, value in bounded.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")
        if self.calcium_spike_increment < 0.0:
            raise ValueError("calcium_spike_increment must be >= 0")
        if self.plasticity_energy_cost < 0.0:
            raise ValueError("plasticity_energy_cost must be >= 0")


@dataclass(slots=True)
class NeuronTissueState:
    """Slow state associated with one canonical :class:`Neuron`.

    ``basal_drive`` and ``apical_drive`` provide a minimal two-compartment
    context representation. ``calcium`` and ``second_messenger`` bridge spike
    events into slower plasticity and consolidation clocks.
    """

    basal_drive: float = 0.0
    apical_drive: float = 0.0
    calcium: float = 0.0
    second_messenger: float = 0.0
    neuromodulator_gain: float = 1.0
    prediction: float = 0.0
    prediction_error: float = 0.0
    salience: float = 0.0
    intrinsic_excitability: float = 0.5
    metabolic_reserve: float = 1.0
    glial_support: float = 0.5
    activity_memory: float = 0.0

    def integrate_context(self, *, basal: float = 0.0, apical: float = 0.0) -> float:
        """Store compartment drives and return bounded coincidence gain."""
        self.basal_drive = float(basal)
        self.apical_drive = float(apical)
        coincidence = math.tanh(abs(basal) * abs(apical))
        return 1.0 + 0.5 * coincidence

    def on_tick(self, *, spiked: bool, config: NeuralTissueConfig) -> None:
        self.calcium *= config.calcium_decay
        self.second_messenger *= config.messenger_decay
        self.prediction_error *= config.prediction_decay
        self.activity_memory = 0.98 * self.activity_memory + (0.02 if spiked else 0.0)
        self.metabolic_reserve = _clip(
            self.metabolic_reserve + config.metabolic_recovery
        )
        if spiked:
            self.calcium = _clip(
                self.calcium + config.calcium_spike_increment, 0.0, 4.0
            )
            self.second_messenger = _clip(
                self.second_messenger + 0.1 * self.calcium, 0.0, 4.0
            )
            self.metabolic_reserve = _clip(self.metabolic_reserve - 0.005)

    def plasticity_step(self, observed_spike: float) -> None:
        self.prediction_error = observed_spike - self.prediction
        self.prediction = 0.9 * self.prediction + 0.1 * observed_spike
        self.salience = _clip(0.9 * self.salience + 0.1 * abs(self.prediction_error))
        calcium_target = _clip(self.calcium / 2.0)
        self.intrinsic_excitability = _clip(
            0.995 * self.intrinsic_excitability + 0.005 * calcium_target
        )

    def consolidate(self) -> None:
        self.glial_support = _clip(
            0.99 * self.glial_support + 0.01 * (1.0 - abs(self.prediction_error))
        )

    def to_dict(self) -> dict[str, float]:
        return {key: float(value) for key, value in asdict(self).items()}


@dataclass(slots=True)
class SynapseTissueState:
    """Slow/STP state associated with one canonical :class:`Synapse`."""

    connection_role: ConnectionRole = ConnectionRole.UNKNOWN
    depression_resource: float = 1.0
    facilitation: float = 0.0
    ready_vesicle_fraction: float = 1.0
    release_probability: float = 0.5
    presynaptic_calcium: float = 0.0
    ampa_gain: float = 1.0
    nmda_gain: float = 0.5
    gaba_a_gain: float = 0.0
    gaba_b_gain: float = 0.0
    retrograde_signal: float = 0.0
    bcm_threshold: float = 0.5
    synaptic_tag: float = 0.0
    consolidation: float = 0.0
    modulation_gain: float = 1.0
    confidence: float = 0.5
    dynamic_delay_offset: int = 0
    silent: bool = False
    frozen: bool = False
    cumulative_plasticity_cost: float = 0.0
    use_count: int = 0

    def effective_release(self, config: NeuralTissueConfig) -> float:
        """Advance deterministic Tsodyks-Markram-like STP and return release."""
        self.facilitation = _clip(
            self.facilitation + config.stp_facilitation * (1.0 - self.facilitation)
        )
        probability = _clip(self.release_probability + 0.5 * self.facilitation)
        released = self.depression_resource * self.ready_vesicle_fraction * probability
        self.depression_resource = _clip(self.depression_resource - released)
        self.ready_vesicle_fraction = _clip(self.ready_vesicle_fraction - 0.5 * released)
        self.presynaptic_calcium = _clip(self.presynaptic_calcium + 0.2, 0.0, 4.0)
        self.use_count += 1
        return 0.0 if self.silent else released * self.modulation_gain

    def recover(self, config: NeuralTissueConfig) -> None:
        self.depression_resource = _clip(
            self.depression_resource
            + config.stp_recovery * (1.0 - self.depression_resource)
        )
        self.ready_vesicle_fraction = _clip(
            self.ready_vesicle_fraction
            + config.vesicle_recovery * (1.0 - self.ready_vesicle_fraction)
        )
        self.facilitation = _clip(self.facilitation * (1.0 - config.stp_recovery))
        self.presynaptic_calcium *= 0.9
        self.retrograde_signal *= 0.95

    def plasticity_signal(
        self,
        *,
        pre_activity: float,
        post_activity: float,
        post_calcium: float,
        config: NeuralTissueConfig,
    ) -> float:
        """Return a bounded BCM-like candidate update without applying it."""
        self.bcm_threshold = _clip(
            (1.0 - config.bcm_rate) * self.bcm_threshold
            + config.bcm_rate * post_activity * post_activity
        )
        coincidence = pre_activity * post_activity
        direction = post_activity - self.bcm_threshold
        calcium_gate = _clip(post_calcium / 2.0)
        delta = coincidence * direction * calcium_gate * self.modulation_gain
        self.synaptic_tag = _clip(0.95 * self.synaptic_tag + 0.05 * abs(delta))
        self.retrograde_signal = _clip(0.9 * self.retrograde_signal + 0.1 * post_calcium)
        agreement = 1.0 if delta >= 0.0 else 0.0
        self.confidence = _clip(
            (1.0 - config.confidence_rate) * self.confidence
            + config.confidence_rate * agreement
        )
        return 0.0 if self.frozen else delta

    def consolidate(self, config: NeuralTissueConfig) -> None:
        capture = self.synaptic_tag * self.confidence
        self.consolidation = _clip(
            self.consolidation + config.consolidation_rate * capture
        )
        self.synaptic_tag *= 1.0 - config.consolidation_rate
        if self.consolidation >= 0.95:
            self.frozen = True

    @property
    def effective_delay_offset(self) -> int:
        return max(-1, min(1, self.dynamic_delay_offset))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["connection_role"] = self.connection_role.value
        return payload


@dataclass(frozen=True, slots=True)
class StructuralProposal:
    """Auditable development-timescale proposal; mutation is optional."""

    action: str
    pre_id: int
    post_id: int
    reason: str
    score: float


@dataclass(frozen=True, slots=True)
class TissueStepReport:
    """One network step plus slower-clock activity."""

    network: StepResult
    plasticity_ran: bool
    consolidation_ran: bool
    development_ran: bool
    structural_proposals: tuple[StructuralProposal, ...] = ()
    plasticity_energy_spent: float = 0.0


class NeuralTissueController:
    """Attach explicit slow biological-computation surrogates to a network.

    The controller does not replace ``NeuralNetwork.step``. It composes it and
    synchronizes sidecars from canonical IDs, preserving existing persistence,
    deterministic event ordering and the separation from ``LearningEngine``.
    Weight mutation and structural mutation are disabled by default so research
    experiments must opt in explicitly.
    """

    def __init__(
        self,
        network: NeuralNetwork,
        config: NeuralTissueConfig | None = None,
    ) -> None:
        self.network = network
        self.config = config or NeuralTissueConfig()
        self.neurons: dict[int, NeuronTissueState] = {}
        self.synapses: dict[tuple[int, int], SynapseTissueState] = {}
        self.last_structural_proposals: tuple[StructuralProposal, ...] = ()
        self._sync_topology()

    def _sync_topology(self) -> None:
        current_neurons = set(self.network.neurons)
        for neuron_id in current_neurons:
            self.neurons.setdefault(neuron_id, NeuronTissueState())
        for neuron_id in tuple(self.neurons):
            if neuron_id not in current_neurons:
                del self.neurons[neuron_id]

        current_synapses: set[tuple[int, int]] = set()
        for pre_id, outgoing in self.network.synapses.items():
            for synapse in outgoing:
                key = (pre_id, synapse.target_id)
                current_synapses.add(key)
                self.synapses.setdefault(key, SynapseTissueState())
        for key in tuple(self.synapses):
            if key not in current_synapses:
                del self.synapses[key]

    def set_connection_role(
        self,
        pre_id: int,
        post_id: int,
        role: ConnectionRole | str,
    ) -> None:
        self._sync_topology()
        key = (pre_id, post_id)
        if key not in self.synapses:
            raise KeyError(f"synapse {pre_id}->{post_id} does not exist")
        self.synapses[key].connection_role = ConnectionRole(role)

    def set_neuromodulator(self, neuron_id: int, gain: float) -> None:
        self._sync_topology()
        self.neurons[neuron_id].neuromodulator_gain = _clip(gain, 0.0, 2.0)

    def set_attention_gain(self, pre_id: int, post_id: int, gain: float) -> None:
        self._sync_topology()
        self.synapses[(pre_id, post_id)].modulation_gain = _clip(gain, 0.0, 2.0)

    def compartment_gain(
        self,
        neuron_id: int,
        *,
        basal: float = 0.0,
        apical: float = 0.0,
    ) -> float:
        self._sync_topology()
        return self.neurons[neuron_id].integrate_context(basal=basal, apical=apical)

    def _find_synapse(self, pre_id: int, post_id: int) -> Synapse | None:
        for synapse in self.network.synapses.get(pre_id, []):
            if synapse.target_id == post_id:
                return synapse
        return None

    def _run_plasticity(self, result: StepResult) -> float:
        spent = 0.0
        spikes = set(result.spike_ids)
        for neuron_id, state in self.neurons.items():
            state.plasticity_step(1.0 if neuron_id in spikes else 0.0)

        for (pre_id, post_id), state in self.synapses.items():
            state.recover(self.config)
            pre_activity = 1.0 if pre_id in spikes else self.neurons[pre_id].activity_memory
            post_activity = (
                1.0 if post_id in spikes else self.neurons[post_id].activity_memory
            )
            if pre_id in spikes:
                state.effective_release(self.config)
            delta = state.plasticity_signal(
                pre_activity=pre_activity,
                post_activity=post_activity,
                post_calcium=self.neurons[post_id].calcium,
                config=self.config,
            )
            if delta == 0.0:
                continue
            cost = abs(delta) * self.config.plasticity_energy_cost
            reserve = self.neurons[post_id].metabolic_reserve
            if cost > reserve:
                continue
            self.neurons[post_id].metabolic_reserve = _clip(reserve - cost)
            state.cumulative_plasticity_cost += cost
            spent += cost
            if self.config.enable_weight_updates:
                synapse = self._find_synapse(pre_id, post_id)
                if synapse is not None and not state.frozen:
                    bounded_delta = max(-0.01, min(0.01, 0.01 * delta))
                    old = synapse.weight
                    synapse.weight = max(
                        synapse.config.w_min,
                        min(synapse.config.w_max, old + bounded_delta),
                    )
                    if synapse.weight != old:
                        synapse.update_count += 1
                        synapse.mark_dirty()
        return spent

    def _run_consolidation(self) -> None:
        for state in self.neurons.values():
            state.consolidate()
        for state in self.synapses.values():
            state.consolidate(self.config)

    def _development_proposals(self) -> tuple[StructuralProposal, ...]:
        proposals: list[StructuralProposal] = []
        for (pre_id, post_id), state in sorted(self.synapses.items()):
            if state.confidence < self.config.structural_prune_confidence:
                proposals.append(
                    StructuralProposal(
                        action="prune",
                        pre_id=pre_id,
                        post_id=post_id,
                        reason="low_confidence",
                        score=1.0 - state.confidence,
                    )
                )
        active = sorted(
            (
                (state.activity_memory, neuron_id)
                for neuron_id, state in self.neurons.items()
                if state.activity_memory >= self.config.structural_grow_activity
            ),
            reverse=True,
        )
        if len(active) >= 2:
            _, pre_id = active[0]
            _, post_id = active[1]
            if pre_id != post_id and self._find_synapse(pre_id, post_id) is None:
                proposals.append(
                    StructuralProposal(
                        action="grow",
                        pre_id=pre_id,
                        post_id=post_id,
                        reason="coactive_unconnected_pair",
                        score=min(active[0][0], active[1][0]),
                    )
                )
        return tuple(proposals)

    def _apply_structural_proposals(
        self, proposals: tuple[StructuralProposal, ...]
    ) -> None:
        if not self.config.enable_structural_mutation:
            return
        for proposal in proposals:
            if proposal.action == "prune":
                self.network.disconnect(proposal.pre_id, proposal.post_id)
            elif proposal.action == "grow":
                if proposal.pre_id not in self.network.neurons:
                    continue
                if proposal.post_id not in self.network.neurons:
                    continue
                try:
                    self.network.connect(
                        proposal.pre_id,
                        proposal.post_id,
                        weight=max(self.network.network_config.weight_min, 0.05),
                        delay=1,
                    )
                except ValueError:
                    continue
        self._sync_topology()

    def step(self) -> TissueStepReport:
        """Advance canonical network one tick and slower clocks when due."""
        self._sync_topology()
        result = self.network.step()
        spikes = set(result.spike_ids)
        for neuron_id, state in self.neurons.items():
            state.on_tick(spiked=neuron_id in spikes, config=self.config)

        tick_number = result.tick + 1
        timescales = self.config.timescales
        plasticity_ran = tick_number % timescales.plasticity_interval_ticks == 0
        consolidation_ran = (
            tick_number % timescales.consolidation_interval_ticks == 0
        )
        development_ran = tick_number % timescales.development_interval_ticks == 0

        spent = self._run_plasticity(result) if plasticity_ran else 0.0
        if consolidation_ran:
            self._run_consolidation()
        proposals: tuple[StructuralProposal, ...] = ()
        if development_ran:
            proposals = self._development_proposals()
            self.last_structural_proposals = proposals
            self._apply_structural_proposals(proposals)

        return TissueStepReport(
            network=result,
            plasticity_ran=plasticity_ran,
            consolidation_ran=consolidation_ran,
            development_ran=development_ran,
            structural_proposals=proposals,
            plasticity_energy_spent=spent,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize only the sidecar state; canonical network stays separate."""
        return {
            "schema_version": 1,
            "timescales": asdict(self.config.timescales),
            "config": {
                key: value
                for key, value in asdict(self.config).items()
                if key != "timescales"
            },
            "neurons": {
                str(neuron_id): state.to_dict()
                for neuron_id, state in sorted(self.neurons.items())
            },
            "synapses": {
                f"{pre_id}:{post_id}": state.to_dict()
                for (pre_id, post_id), state in sorted(self.synapses.items())
            },
        }


__all__ = [
    "ConnectionRole",
    "NeuralTissueConfig",
    "NeuralTissueController",
    "NeuronTissueState",
    "StructuralProposal",
    "SynapseTissueState",
    "TimescaleConfig",
    "TissueStepReport",
]
