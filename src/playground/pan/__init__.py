"""Exploratory PAN layer for the isolated MHRN Playground.

PAN results are PLAYGROUND only. Nothing here is scientific DATA or EVID.
"""

from .candidates import pan_research_candidates
from .dual_scheduler import DualModeScheduler
from .gate_schematic import GateSchematic, settings_to_gates
from .growth_engine import GrowthEngine
from .hypervector import axis_schema, bind, bundle
from .literature import PAN_LITERATURE, pan_literature_context
from .memory_pool import CUDAMemoryPool
from .runtime import PANRuntime
from .ssd_offloader import SSDOffloader

__all__ = [
    "PANRuntime",
    "DualModeScheduler",
    "GateSchematic",
    "GrowthEngine",
    "CUDAMemoryPool",
    "SSDOffloader",
    "settings_to_gates",
    "axis_schema",
    "bind",
    "bundle",
    "PAN_LITERATURE",
    "pan_literature_context",
    "pan_research_candidates",
]
