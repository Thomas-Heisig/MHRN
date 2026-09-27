"""Registries for non-canonical playground building blocks."""

from .neuron_models import NEURON_MODELS
from .plasticity_rules import PLASTICITY_RULES
from .readouts import READOUTS
from .stimulus_generators import STIMULUS_REGISTRY
from .synapse_models import SYNAPSE_MODELS
from .topology_generators import TOPOLOGY_REGISTRY

__all__ = [
    "NEURON_MODELS",
    "PLASTICITY_RULES",
    "READOUTS",
    "STIMULUS_REGISTRY",
    "SYNAPSE_MODELS",
    "TOPOLOGY_REGISTRY",
]
