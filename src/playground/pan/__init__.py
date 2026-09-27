"""Exploratory PAN layer for the isolated MHRN Playground.

PAN results are PLAYGROUND only. Nothing here is scientific DATA or EVID.
"""

from .behavioral_learning import BehavioralLearningEngine
from .candidates import pan_research_candidates
from .cortical_organization import CorticalOrganization
from .dual_scheduler import DualModeScheduler
from .gate_schematic import GateSchematic, settings_to_gates
from .growth_engine import GrowthEngine
from .hardware_profile import hardware_profile
from .mode_switcher import ActivityMonitor, ModeSwitcher, state_integrity_hash
from .hypervector import axis_schema, bind, bundle
from .literature import PAN_LITERATURE, pan_literature_context
from .memory_pool import CUDAMemoryPool
from .runtime import PANRuntime
from .ssd_offloader import SSDOffloader
from .thalamic_gating import ThalamicGating

__all__ = [
    "PANRuntime",
    "BehavioralLearningEngine",
    "CorticalOrganization",
    "ThalamicGating",
    "hardware_profile",
    "ActivityMonitor",
    "ModeSwitcher",
    "state_integrity_hash",
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
