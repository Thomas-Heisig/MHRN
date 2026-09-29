"""Canonical backend parity framework."""

from .contract import ParityClass, ParityContract, ParityResult, default_parity_contract
from .d1_spikes import exact_spike_parity
from .d2_state import max_abs_error, state_vector_parity
from .d3_behavior import exact_behavior_parity, metric_behavior_parity
from .fingerprint import config_fingerprint, execution_fingerprint
from .runner import compare_builder_runs

__all__ = [
    "ParityClass",
    "ParityContract",
    "ParityResult",
    "compare_builder_runs",
    "config_fingerprint",
    "default_parity_contract",
    "exact_behavior_parity",
    "exact_spike_parity",
    "execution_fingerprint",
    "max_abs_error",
    "metric_behavior_parity",
    "state_vector_parity",
]
