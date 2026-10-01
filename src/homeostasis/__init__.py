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
from .pan_parity_contract import (
    PAN_PARITY_CONTRACT_ID,
    PAN_PARITY_CONTRACT_STATUS,
    PANParityResult,
    PANParityThresholds,
    compare_pan_state_mappings,
    pan_parity_contract_check,
)
from .pan_wave5b_preflight import (
    PAN_WAVE5B_PREFLIGHT_ID,
    PanWave5BReadiness,
    evaluate_pan_wave5b_readiness,
    load_pan_wave5b_preflight,
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
    "PAN_PARITY_CONTRACT_ID",
    "PAN_PARITY_CONTRACT_STATUS",
    "PANParityResult",
    "PANParityThresholds",
    "PAN_WAVE5B_PREFLIGHT_ID",
    "PanWave5BReadiness",
    "compare_pan_state_mappings",
    "evaluate_pan_wave5b_readiness",
    "initialize_pan_state_mapping",
    "load_pan_wave5b_preflight",
    "pan_parity_contract_check",
    "pan_contract_check",
    "validate_pan_state_mapping",
]
