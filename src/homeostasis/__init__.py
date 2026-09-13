"""Homeostatic self-regulation for MHRN.

This package provides firing-rate and energy homeostasis through a post-step
observer that continuously adjusts neuron thresholds and energy levels.
"""

from .engine import HomeostasisParameters, HomeostasisStats
from .hot_path import HotPathHomeostasisEngine as HomeostasisEngine
from .signals import HomeostasisSignal

__all__ = [
    "HomeostasisEngine",
    "HomeostasisParameters",
    "HomeostasisSignal",
    "HomeostasisStats",
]
