"""Explicit construction boundary for alternative neuron bodies.

The canonical NeuralNetwork still owns point neurons. Experimental HH and
multi-compartment cells are constructed here so they cannot be selected by a
hidden boolean or silently share incompatible state layouts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .biophysical_contracts import DendriticNonlinearity, NeuronStructure
from .compartment_neuron import CompartmentConfig, CompartmentNeuron
from .hh_neuron import HHConfig, HodgkinHuxleyNeuron
from .neuron import Neuron, NeuronConfig, NeuronType, create_neuron
from .neuron_models import NeuronModel


class BiophysicalNeuronModel(StrEnum):
    IZHIKEVICH = NeuronModel.IZHIKEVICH.value
    LIF = NeuronModel.LEAKY_INTEGRATE_AND_FIRE.value
    HODGKIN_HUXLEY = "hodgkin-huxley-na-k-ca-v1"


@dataclass(frozen=True, slots=True)
class BiophysicalNeuronConfig:
    model: BiophysicalNeuronModel = BiophysicalNeuronModel.IZHIKEVICH
    structure: NeuronStructure = NeuronStructure.POINT
    dendritic_nonlinearity: DendriticNonlinearity = DendriticNonlinearity.LINEAR
    point: NeuronConfig = NeuronConfig()
    hh: HHConfig = HHConfig()
    compartment: CompartmentConfig = CompartmentConfig()

    def __post_init__(self) -> None:
        if (
            self.structure is NeuronStructure.MULTI_COMPARTMENT
            and self.model is BiophysicalNeuronModel.HODGKIN_HUXLEY
        ):
            raise ValueError(
                "HH point dynamics and multi-compartment structure are separate treatments"
            )


def create_biophysical_neuron(
    neuron_id: int,
    config: BiophysicalNeuronConfig,
    *,
    neuron_type: NeuronType = NeuronType.REGULAR_SPIKING,
) -> Neuron | HodgkinHuxleyNeuron | CompartmentNeuron:
    if config.structure is NeuronStructure.MULTI_COMPARTMENT:
        compartment = CompartmentConfig(
            enabled=config.compartment.enabled,
            structure=NeuronStructure.MULTI_COMPARTMENT,
            compartments=config.compartment.compartments,
            dt_ms=config.compartment.dt_ms,
            soma_tau_ms=config.compartment.soma_tau_ms,
            dendrite_tau_ms=config.compartment.dendrite_tau_ms,
            coupling=config.compartment.coupling,
            resting_potential=config.compartment.resting_potential,
            spike_threshold=config.compartment.spike_threshold,
            reset_potential=config.compartment.reset_potential,
            dendritic_nonlinearity=config.dendritic_nonlinearity,
            nmda_plateau_threshold=config.compartment.nmda_plateau_threshold,
            nmda_plateau_gain=config.compartment.nmda_plateau_gain,
            enable_nmda_plateau=config.compartment.enable_nmda_plateau,
        )
        return CompartmentNeuron(neuron_id, compartment)
    if config.model is BiophysicalNeuronModel.HODGKIN_HUXLEY:
        return HodgkinHuxleyNeuron(neuron_id, config.hh)
    point_model = (
        NeuronModel.LEAKY_INTEGRATE_AND_FIRE
        if config.model is BiophysicalNeuronModel.LIF
        else NeuronModel.IZHIKEVICH
    )
    point_config = NeuronConfig.from_dict(config.point.to_dict())
    point_config = NeuronConfig.from_dict(
        {**point_config.to_dict(), "model": point_model.value}
    )
    return create_neuron(neuron_id, neuron_type, point_config)


__all__ = [
    "BiophysicalNeuronConfig",
    "BiophysicalNeuronModel",
    "create_biophysical_neuron",
]
