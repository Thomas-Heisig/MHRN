"""Exploratory PAN layer for the isolated MHRN Playground.

PAN results are PLAYGROUND only. Nothing here is scientific DATA or EVID.
"""

from .candidates import pan_research_candidates
from .hypervector import axis_schema, bind, bundle
from .runtime import PANRuntime

__all__ = [
    "PANRuntime",
    "axis_schema",
    "bind",
    "bundle",
    "pan_research_candidates",
]
