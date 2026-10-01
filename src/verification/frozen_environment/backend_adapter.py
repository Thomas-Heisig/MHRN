"""Canonical FE-3 bridge between FrozenWorldSession and ExecutionBackend."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from src.embodiment.models import ActionCommand, JSONValue
from src.embodiment.msba import SymbolFrame
from src.embodiment.neural_io_contracts import BoundaryFrame, canonical_payload_bytes
from src.experience.frozen_environment import (
    FreezeMode,
    FrozenEnvironmentManifest,
    FrozenEnvironmentTrace,
    FrozenWorldAdapter,
    FrozenWorldSession,
    canonical_digest,
)
from src.runtime.backend import LiveInputExecutionBackend, StepResult
from src.verification.parity import (
    config_fingerprint,
    exact_frozen_environment_parity,
    execution_fingerprint,
)

from .acceptance import FEAcceptanceResult, WorldFactory

LiveBackendFactory = Callable[[], LiveInputExecutionBackend]


@dataclass(frozen=True, slots=True)
class FE3BackendRun:
    """One backend-driven causal FE-3 trajectory with explicit provenance."""

    trace: FrozenEnvironmentTrace
    backend_name: str
    backend_version: str
    input_fingerprint: str
    final_state_digest: str
    execution_fingerprint: str

    def to_mapping(self) -> dict[str, object]:
        return {
            "backend_name": self.backend_name,
            "backend_version": self.backend_version,
            "manifest_sha256": self.trace.manifest_sha256,
            "trace_sha256": self.trace.trace_sha256,
            "input_fingerprint": self.input_fingerprint,
            "final_state_digest": self.final_state_digest,
            "execution_fingerprint": self.execution_fingerprint,
        }


def build_deterministic_target_backend_config(ticks: int) -> dict[str, object]:
    """Return the bounded two-neuron FE-3 acceptance network."""

    if type(ticks) is not int or not 1 <= ticks <= 2000:
        raise ValueError("ticks must be an integer in [1,2000]")
    return {
        "n_neurons": 2,
        "ticks": ticks,
        "offsets": [0, 0, 0],
        "sources": [],
        "delays": [],
        "weights": [],
        "external": [0.0] * (ticks * 2),
        "voltage": [-65.0, -65.0],
        "adaptation": [0.0, 0.0],
        "model": "lif",
        "dt_ms": 1.0,
        "synapses": None,
        "rewards": [],
    }


def _state_int(state: Mapping[str, JSONValue], field: str) -> int:
    value = state.get(field)
    if type(value) is not int:
        raise ValueError(f"{field} must be an integer")
    return value


def deterministic_target_currents(
    state: Mapping[str, JSONValue],
) -> tuple[float, float]:
    """Encode target direction as a deterministic two-neuron current row."""

    position = _state_int(state, "position")
    target = _state_int(state, "target")
    if position < target:
        return (400.0, 0.0)
    if position > target:
        return (0.0, 400.0)
    return (0.0, 0.0)


def deterministic_target_boundary_frame(
    state: Mapping[str, JSONValue],
    *,
    tick: int,
) -> BoundaryFrame:
    """Serialize exact world sensor state into the canonical boundary plane."""

    payload, content_type = canonical_payload_bytes(dict(state))
    symbol = SymbolFrame(
        payload=payload,
        codec="fe3-deterministic-target-state-v1",
        sequence=tick,
        provenance="FROZEN_ENVIRONMENT_FE3",
    )
    return BoundaryFrame(
        schema_version=1,
        frame_id=f"fe3-target-state-{tick}",
        stream_id="fe3-target-state",
        sequence=tick,
        direction="input",
        kind="sensor",
        content_type=content_type,
        schema_id="deterministic-target-state-v1",
        symbol_frame=symbol,
        correlation_id=f"fe3-target-{tick}",
        priority=0,
        source_id="deterministic-target-v1",
        provenance="FROZEN_ENVIRONMENT_FE3",
        arrival_time_ns=None,
        admitted_tick=tick,
    )


def _decode_target_action(tick: int, step: StepResult) -> ActionCommand:
    spikes = set(step.spikes)
    if 0 in spikes and 1 in spikes:
        raise RuntimeError("FE-3 action decoder received conflicting left/right spikes")
    action = "right" if 0 in spikes else "left" if 1 in spikes else "hold"
    return ActionCommand("target-actuator", tick, action)


def run_fe3_backend_trace(
    manifest: FrozenEnvironmentManifest,
    world_factory: WorldFactory,
    backend_factory: LiveBackendFactory,
    *,
    seed: int = 12345,
) -> FE3BackendRun:
    """Run one causal sensor -> backend -> action -> world FE-3 trajectory."""

    if manifest.mode is not FreezeMode.FE3_FULL_DETERMINISTIC_LIVE_LOOP:
        raise ValueError("backend FE-3 requires an FE-3 manifest")
    if manifest.environment_id != "deterministic-target-v1":
        raise ValueError("first backend FE-3 adapter supports deterministic-target-v1")
    if not manifest.sensor_schedule:
        raise ValueError("FE-3 manifest requires a non-empty sensor schedule")

    world: FrozenWorldAdapter = world_factory()
    session = FrozenWorldSession(manifest, world)
    session.begin()

    backend = backend_factory()
    if not isinstance(backend, LiveInputExecutionBackend):
        raise TypeError("backend does not implement LiveInputExecutionBackend")
    if not backend.capabilities().supports_live_external_input:
        raise RuntimeError("backend does not declare live external input support")

    base_config = build_deterministic_target_backend_config(
        len(manifest.sensor_schedule)
    )
    backend.initialize(base_config, seed)
    live_rows: list[list[float]] = []

    for expected_tick, tick in enumerate(manifest.sensor_schedule):
        if tick != expected_tick:
            raise ValueError(
                "first backend FE-3 adapter requires a zero-based contiguous schedule"
            )
        sensor_state = dict(world.snapshot_state())
        currents = deterministic_target_currents(sensor_state)
        frame = deterministic_target_boundary_frame(sensor_state, tick=tick)
        backend.set_external_tick(tick, currents)
        step = backend.step(tick)
        action = _decode_target_action(tick, step)
        session.step(action, boundary_frames=(frame,))
        live_rows.append(list(currents))

    trace = session.trace()
    snapshot = backend.snapshot()
    input_fingerprint = canonical_digest(
        {
            "base_config_sha256": config_fingerprint(base_config),
            "live_external_rows": live_rows,
            "manifest_sha256": manifest.manifest_sha256,
        }
    )
    backend_name = str(getattr(backend, "backend_name", type(backend).__name__))
    backend_version = str(getattr(backend, "backend_version", "unknown"))
    return FE3BackendRun(
        trace=trace,
        backend_name=backend_name,
        backend_version=backend_version,
        input_fingerprint=input_fingerprint,
        final_state_digest=snapshot.state_digest,
        execution_fingerprint=execution_fingerprint(
            seed=seed,
            config_hash=input_fingerprint,
            backend_name=backend_name,
            backend_version=backend_version,
            ticks=len(manifest.sensor_schedule),
        ),
    )


def run_fe3_backend_parity(
    manifest: FrozenEnvironmentManifest,
    world_factory: WorldFactory,
    reference_backend_factory: LiveBackendFactory,
    candidate_backend_factory: LiveBackendFactory,
    *,
    seed: int = 12345,
) -> FEAcceptanceResult:
    """Require exact D3c world parity for two live-input execution backends."""

    reference = run_fe3_backend_trace(
        manifest, world_factory, reference_backend_factory, seed=seed
    )
    candidate = run_fe3_backend_trace(
        manifest, world_factory, candidate_backend_factory, seed=seed
    )
    parity = exact_frozen_environment_parity(reference.trace, candidate.trace)
    same_inputs = reference.input_fingerprint == candidate.input_fingerprint
    return FEAcceptanceResult(
        "FE-3-CPU-CUDA-D3C",
        parity.passed and same_inputs,
        {
            "scope": "CANONICAL_FROZEN_ENVIRONMENT_LIVE_BACKEND_D3C",
            "manifest_sha256": manifest.manifest_sha256,
            "parity": parity.to_mapping(),
            "reference": reference.to_mapping(),
            "candidate": candidate.to_mapping(),
            "live_input_fingerprint_exact": same_inputs,
            "trajectory_sha256_exact": (
                reference.trace.trace_sha256 == candidate.trace.trace_sha256
            ),
            "execution_fingerprints_equal": (
                reference.execution_fingerprint == candidate.execution_fingerprint
            ),
            "execution_fingerprint_rule": (
                "BACKEND_IDENTITY_IS_PROVENANCE; CPU/CUDA FINGERPRINTS "
                "ARE EXPECTED TO DIFFER"
            ),
            "network_d1_d2": "SEPARATE_WAVE4_ACCEPTANCE",
            "scientific_evidence": False,
        },
    )


__all__ = [
    "FE3BackendRun",
    "LiveBackendFactory",
    "build_deterministic_target_backend_config",
    "deterministic_target_boundary_frame",
    "deterministic_target_currents",
    "run_fe3_backend_parity",
    "run_fe3_backend_trace",
]
