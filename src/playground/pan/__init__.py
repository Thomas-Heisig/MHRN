"""Exploratory PAN layer for the isolated MHRN Playground.

PAN results are PLAYGROUND only. Nothing here is scientific DATA or EVID.
"""

from .candidates import pan_research_candidates
from .hypervector import axis_schema, bind, bundle
from .literature import PAN_LITERATURE, pan_literature_context
from .runtime import PANRuntime

__all__ = [
    "PANRuntime",
    "axis_schema",
    "bind",
    "bundle",
    "PAN_LITERATURE",
    "pan_literature_context",
    "pan_research_candidates",
]
