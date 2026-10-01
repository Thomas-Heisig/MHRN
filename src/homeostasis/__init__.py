"""Homeostatic self-regulation for MHRN.

This package provides firing-rate and energy homeostasis through a post-step
observer that continuously adjusts neuron thresholds and energy levels.
"""

from .engine import HomeostasisParameters, HomeostasisStats
from .hot_path import HotPathHomeostasisEngine as HomeostasisEngine
from .pan_contract import (
    PAN_CONTRACT_ID,
    PAN_CONTRACT_STATUS,
    PAN_STATE_FIELDS,
    PAN_UPDATE_ORDER,
    PANFormulaParameters,
    initialize_pan_state_mapping,
    pan_contract_check,
    validate_pan_state_mapping,
)
from .signals import HomeostasisSignal

__all__ = [
    "HomeostasisEngine",
    "HomeostasisParameters",
    "HomeostasisSignal",
    "HomeostasisStats",
    "PAN_CONTRACT_ID",
    "PAN_CONTRACT_STATUS",
    "PAN_STATE_FIELDS",
    "PAN_UPDATE_ORDER",
    "PANFormulaParameters",
    "initialize_pan_state_mapping",
    "pan_contract_check",
    "validate_pan_state_mapping",
]
