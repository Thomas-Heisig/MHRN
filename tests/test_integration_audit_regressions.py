"""Regressions for checkpoint integrity and fail-closed operator boundaries."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from types import SimpleNamespace
from typing import Any, cast

import pytest

from src.acceleration.cuda import CUDABackend
from src.acceleration.cuda.recurrent import (
    CPUReferenceBackend,
    recurrent_fixture,
    recurrent_inputs_to_mapping,
)
from src.acceleration.cuda.recurrent.state import stable_digest
from src.dashboard.operator_bridge import OperatorBridge
from src.runtime.backend import BackendState
from src.self_organization.approval import (
    ProposalApprovalPolicy,
    StructuralPlasticityConfig,
)
from src.verification.parity import state_vector_parity


@pytest.fixture(params=[CPUReferenceBackend, CUDABackend])
def backend(request: pytest.FixtureRequest) -> CPUReferenceBackend | CUDABackend:
    instance = request.param()
    config = recurrent_inputs_to_mapping(
        recurrent_fixture(n_neurons=8, ticks=4, model="lif")
    )
    instance.initialize(config, 12345)
    return cast(CPUReferenceBackend | CUDABackend, instance)


def test_live_input_does_not_change_existing_snapshot(
    backend: CPUReferenceBackend | CUDABackend,
) -> None:
    snapshot = backend.snapshot()
    original = deepcopy(snapshot.payload)
    backend.set_external_tick(0, [7.0] * 8)
    assert snapshot.payload == original
    assert stable_digest(snapshot.payload) == snapshot.state_digest


def test_snapshot_edits_do_not_change_live_backend(
    backend: CPUReferenceBackend | CUDABackend,
) -> None:
    snapshot = backend.snapshot()
    config = cast(dict[str, Any], snapshot.payload["config"])
    config["voltage"][0] += 10.0
    assert backend.snapshot().state_digest == snapshot.state_digest


def test_corrupt_restore_is_rejected_without_changing_backend(
    backend: CPUReferenceBackend | CUDABackend,
) -> None:
    snapshot = backend.snapshot()
    payload = deepcopy(dict(snapshot.payload))
    config = cast(dict[str, Any], payload["config"])
    config["voltage"][0] += 10.0
    damaged = replace(snapshot, payload=payload)
    with pytest.raises(ValueError, match="digest mismatch"):
        backend.restore(damaged)
    assert backend.snapshot() == snapshot


@pytest.mark.parametrize("tick,payload_tick", [(1, 0), (5, 5), (True, True)])
def test_restore_rejects_invalid_cursor_before_resetting_backend(
    backend: CPUReferenceBackend | CUDABackend, tick: int, payload_tick: int
) -> None:
    original = backend.snapshot()
    payload = deepcopy(dict(original.payload))
    payload["tick"] = payload_tick
    damaged = BackendState(tick, payload, stable_digest(payload))
    with pytest.raises(ValueError, match="tick"):
        backend.restore(damaged)
    assert backend.snapshot() == original


def test_cpu_checkpoint_continuation_matches_uninterrupted_run() -> None:
    config = recurrent_inputs_to_mapping(
        recurrent_fixture(n_neurons=8, ticks=4, model="lif")
    )
    backend = CPUReferenceBackend()
    backend.initialize(config, 12345)
    backend.run(2)
    checkpoint = backend.snapshot()
    expected = backend.run(2)
    resumed = CPUReferenceBackend()
    resumed.restore(checkpoint)
    assert resumed.run(2) == expected


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -0.1, 1.1, True])
@pytest.mark.parametrize("field", ["confidence", "threshold"])
def test_auto_approval_rejects_invalid_confidence_and_threshold(
    value: float, field: str
) -> None:
    policy = ProposalApprovalPolicy(
        StructuralPlasticityConfig(
            enabled=True,
            dry_run=False,
            auto_approval=True,
            auto_approval_threshold=value if field == "threshold" else 0.8,
        )
    )
    proposal = SimpleNamespace(
        confidence=value if field == "confidence" else 0.9, kind="neurogenesis"
    )
    assert not policy.evaluate(
        proposal, safety_ok=True, cooldown_ok=True, kind_allowed=True
    ).approved


@pytest.mark.parametrize("tolerance", [float("inf"), float("nan"), -1.0, True])
def test_parity_rejects_invalid_tolerance(tolerance: float) -> None:
    result = state_vector_parity([0.0], [0.0], tolerance=tolerance)
    assert not result.passed
    assert "tolerance" in str(result.details["failure_reason"])


def test_zero_tolerance_allows_only_exact_state() -> None:
    assert state_vector_parity([1.0], [1.0], tolerance=0.0).passed
    assert not state_vector_parity([1.0], [1.01], tolerance=0.0).passed


def test_real_operator_bridge_updates_slots_config_and_preserves_other_fields() -> None:
    policy = ProposalApprovalPolicy(
        StructuralPlasticityConfig(enabled=True, auto_approval_threshold=0.85)
    )
    bridge = OperatorBridge(
        cast(Any, SimpleNamespace(network=SimpleNamespace())),
        approval_policy=policy,
        live_projection=cast(Any, SimpleNamespace()),
    )
    result = bridge.update_structural_config(max_changes_per_tick=3)
    assert result.ok
    assert bridge.approval_policy is not None
    assert bridge.approval_policy.config.max_changes_per_tick == 3
    assert bridge.approval_policy.config.enabled
    assert bridge.approval_policy.config.auto_approval_threshold == 0.85
    updated = bridge.approval_policy.config
    assert not bridge.update_structural_config(unknown_setting=1).ok
    assert bridge.approval_policy.config == updated
