"""FE-1/FE-2/FE-3 engineering acceptance using canonical parity."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import TypeAlias

from src.embodiment.models import ActionCommand, EnvironmentObservation
from src.experience.frozen_environment import (
    FreezeMode,
    FrozenBoundaryFrame,
    FrozenBoundaryReplay,
    FrozenEnvironmentManifest,
    FrozenEnvironmentTrace,
    FrozenWorldAdapter,
    FrozenWorldSession,
)
from src.verification.parity import exact_frozen_environment_parity

WorldFactory: TypeAlias = Callable[[], FrozenWorldAdapter]
ActionPolicy: TypeAlias = Callable[[int, EnvironmentObservation | None], ActionCommand]


@dataclass(frozen=True, slots=True)
class FEAcceptanceResult:
    """One non-evidentiary engineering acceptance result."""

    stage: str
    passed: bool
    details: Mapping[str, object] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, object]:
        return {
            "classification": "FROZEN_ENVIRONMENT_ENGINEERING_VERIFICATION",
            "scientific_evidence": False,
            "stage": self.stage,
            "passed": self.passed,
            **dict(self.details),
        }


def run_fe1_integrity(manifest: FrozenEnvironmentManifest) -> FEAcceptanceResult:
    """Verify manifest/frame integrity and exact FE-1 replay ordering."""

    if manifest.mode is not FreezeMode.FE1_BOUNDARY_REPLAY:
        raise ValueError("FE-1 integrity requires an FE-1 manifest")
    replay = FrozenBoundaryReplay(manifest)
    actual: list[str] = []
    expected: list[str] = []
    grouped: dict[int, list[FrozenBoundaryFrame]] = {}
    for frame in manifest.boundary_frames:
        grouped.setdefault(frame.admitted_tick, []).append(frame)

    for tick in manifest.sensor_schedule:
        restored = replay.frames_for_tick(tick)
        actual.extend(
            FrozenBoundaryFrame.from_frame(frame).record_sha256 for frame in restored
        )
        expected.extend(
            frame.record_sha256
            for frame in sorted(
                grouped.get(tick, []),
                key=lambda item: (item.stream_id, item.sequence),
            )
        )

    passed = bool(expected) and actual == expected
    return FEAcceptanceResult(
        "FE-1",
        passed,
        {
            "manifest_sha256": manifest.manifest_sha256,
            "frame_count": len(expected),
            "frame_hashes_exact": actual == expected,
            "replay_exhausted_exactly": True,
        },
    )


def _run_trace(
    manifest: FrozenEnvironmentManifest,
    world_factory: WorldFactory,
    policy: ActionPolicy,
) -> FrozenEnvironmentTrace:
    world = world_factory()
    session = FrozenWorldSession(manifest, world)
    session.begin()
    previous: EnvironmentObservation | None = None
    for tick in manifest.sensor_schedule:
        action = policy(tick, previous)
        if action.tick != tick:
            raise ValueError("action policy returned a command for the wrong tick")
        previous = session.step(action)
    return session.trace()


def run_fe2_replay_determinism(
    manifest: FrozenEnvironmentManifest,
    world_factory: WorldFactory,
    policy: ActionPolicy,
    *,
    repeats: int = 10,
) -> FEAcceptanceResult:
    """Run the same frozen world repeatedly and require exact trace identity."""

    if manifest.mode not in {
        FreezeMode.FE2_FROZEN_WORLD_LIVE_ACTIONS,
        FreezeMode.FE3_FULL_DETERMINISTIC_LIVE_LOOP,
    }:
        raise ValueError("FE-2 replay requires an FE-2 or FE-3 manifest")
    if repeats < 2:
        raise ValueError("repeats must be >= 2")

    traces = tuple(_run_trace(manifest, world_factory, policy) for _ in range(repeats))
    digests = tuple(trace.trace_sha256 for trace in traces)
    passed = len(set(digests)) == 1 and bool(traces[0].records)
    return FEAcceptanceResult(
        "FE-2",
        passed,
        {
            "manifest_sha256": manifest.manifest_sha256,
            "repeats": repeats,
            "trace_sha256": digests[0],
            "all_trace_digests_exact": len(set(digests)) == 1,
            "record_count": len(traces[0].records),
        },
    )


def run_fe3_cpu_self_control(
    manifest: FrozenEnvironmentManifest,
    world_factory: WorldFactory,
    policy: ActionPolicy,
) -> FEAcceptanceResult:
    """CPU/self D3c control using the canonical D3 parity comparator.

    This is an environment/parity plumbing control only. Network-level D1/D2
    and physical CPU-vs-CUDA D3 remain separate acceptance steps.
    """

    if manifest.mode is not FreezeMode.FE3_FULL_DETERMINISTIC_LIVE_LOOP:
        raise ValueError("FE-3 CPU control requires an FE-3 manifest")
    reference = _run_trace(manifest, world_factory, policy)
    candidate = _run_trace(manifest, world_factory, policy)
    parity = exact_frozen_environment_parity(reference, candidate)
    return FEAcceptanceResult(
        "FE-3-CPU-SELF",
        parity.passed,
        {
            "parity": parity.to_mapping(),
            "scope": "D3C_ENVIRONMENT_TRAJECTORY_CPU_SELF_CONTROL",
            "network_d1_d2": "NOT_IN_SCOPE",
            "cuda_d3": "PENDING_PHYSICAL_CLOSED_LOOP_ADAPTER",
        },
    )


__all__ = [
    "ActionPolicy",
    "FEAcceptanceResult",
    "WorldFactory",
    "run_fe1_integrity",
    "run_fe2_replay_determinism",
    "run_fe3_cpu_self_control",
]
