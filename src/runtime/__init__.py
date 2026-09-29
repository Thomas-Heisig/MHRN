"""Runtime contracts and lazily loaded control primitives for MHRN.

The package root deliberately avoids importing control eagerly. Canonical
low-level modules such as src.runtime.determinism must remain usable without
importing Playground-facing runtime controllers and creating circular imports.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .backend import (
    BackendCapabilities,
    BackendState,
    ExecutionBackend,
    RunResult,
    StepResult,
)
from .modes import ObservabilityProfile, StateMode, validate_modes

if TYPE_CHECKING:
    from .control import ControlCommand, ControlMode, ControlSnapshot, RuntimeController

__all__ = [
    "BackendCapabilities",
    "BackendState",
    "ExecutionBackend",
    "RunResult",
    "StepResult",
    "ControlCommand",
    "ControlMode",
    "ControlSnapshot",
    "RuntimeController",
    "ObservabilityProfile",
    "StateMode",
    "validate_modes",
]


def __getattr__(name: str) -> object:
    if name in {"ControlCommand", "ControlMode", "ControlSnapshot", "RuntimeController"}:
        from . import control

        return getattr(control, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
