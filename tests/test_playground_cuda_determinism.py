"""CUDA-1.1 CPU determinism and frozen-loop parity contracts."""

from __future__ import annotations

import pytest

from src.playground.cuda import (
    behavioral_parity_summary,
    cpu_determinism_summary,
    exact_spike_parity_summary,
    gate_parity_summary,
    parity_contract,
)
from src.playground.models import PlaygroundConfig
from src.playground.service import determinism, run


def _p3_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "closed_loop_preset": "minimal_closed_loop",
        "name": "cuda1-determinism",
        "n_neurons": 12,
        "edge_budget": 24,
        "k_neighbors": 8,
        "ticks": 16,
        "behavior_episode_ticks": 4,
        "behavior_min_activity": 0.0,
        "seed": 12345,
        "persist": False,
    }
    payload.update(overrides)
    return payload


def test_cpu_reference_is_exactly_deterministic_for_same_seed() -> None:
    first = run(_p3_payload())
    second = run(_p3_payload())

    summary = cpu_determinism_summary(first, second)
    assert summary["spike_train_exact"] is True
    assert summary["projection_exact"] is True
    assert summary["fingerprint_first"] == summary["fingerprint_second"]
    assert summary["passed"] is True


def test_cpu_determinism_projection_ignores_session_identity_and_wall_clock() -> None:
    first = run(_p3_payload(ticks=8))
    second = run(_p3_payload(ticks=8))

    second["session_id"] = "IGNORED-BY-DETERMINISM-CONTRACT"
    second["created_at"] = "2099-01-01T00:00:00+00:00"
    summary = cpu_determinism_summary(first, second)
    assert summary["wall_clock_excluded"] is True
    assert summary["session_identity_excluded"] is True
    assert summary["passed"] is True


def test_freeze_actions_and_rewards_replay_cpu_reference_trace() -> None:
    reference = run(_p3_payload())
    loop = reference["closed_loop"]
    assert isinstance(loop, dict)
    actions = loop["action_history"]
    rewards = loop["reward_history"]
    assert isinstance(actions, list)
    assert isinstance(rewards, list)
    assert len(actions) == 4
    assert len(rewards) == 4

    replay = run(
        _p3_payload(
            freeze_actions=True,
            frozen_action_sequence=actions,
            freeze_rewards=True,
            frozen_reward_sequence=rewards,
            parity_reference_source="CPU_PYTHON_PLAYGROUND",
            parity_reference_commit="abcdef1",
        )
    )
    replay_loop = replay["closed_loop"]
    assert isinstance(replay_loop, dict)
    assert replay_loop["parity_mode"] == "FROZEN_ACTIONS_AND_REWARDS"
    assert replay_loop["action_history"] == actions
    assert replay_loop["reward_history"] == rewards
    assert replay["monitors"]["spikes"] == reference["monitors"]["spikes"]


def test_freeze_configuration_fails_closed_without_complete_trace() -> None:
    with pytest.raises(ValueError, match="frozen_action_sequence"):
        PlaygroundConfig.from_mapping(
            _p3_payload(
                freeze_actions=True,
                frozen_action_sequence=[0, 1],
                parity_reference_commit="abcdef1",
            )
        )

    with pytest.raises(ValueError, match="frozen_reward_sequence"):
        PlaygroundConfig.from_mapping(
            _p3_payload(
                freeze_rewards=True,
                frozen_reward_sequence=[1.0],
                parity_reference_commit="abcdef1",
            )
        )

    with pytest.raises(ValueError, match="parity_reference_commit"):
        PlaygroundConfig.from_mapping(
            _p3_payload(
                freeze_actions=True,
                frozen_action_sequence=[0, 1, 2, 3],
            )
        )


def test_parity_contract_defines_d1_d2_d3_numeric_acceptance() -> None:
    contract = parity_contract()
    classes = contract["classes"]
    assert isinstance(classes, dict)

    d1 = classes["D1"]
    d2 = classes["D2"]
    d3 = classes["D3"]
    assert isinstance(d1, dict)
    assert isinstance(d2, dict)
    assert isinstance(d3, dict)

    assert d1["allowed_spike_mismatches"] == 0
    assert d2["voltage_max_abs_error"] == 1.0e-4
    assert d2["weight_max_abs_error"] == 1.0e-4
    assert d3["spike_count_relative_error"] == 0.005
    assert d3["success_fraction_abs_error"] == 0.02


def test_d1_d2_d3_parity_evaluators_are_explicit() -> None:
    d1 = exact_spike_parity_summary(
        [(0, 1), (2, 3)],
        [(0, 1), (2, 3)],
        reference_commit="abcdef1",
    )
    assert d1["parity_class"] == "D1"
    assert d1["passed"] is True

    d2 = gate_parity_summary(
        [0.0, 1.0],
        [5.0e-5, 1.00005],
        reference_commit="abcdef1",
    )
    assert d2["parity_class"] == "D2"
    assert d2["gates_compared"] == [
        "A1",
        "A2",
        "A3",
        "A4",
        "B1",
        "C1",
        "C2",
        "D1",
    ]
    assert d2["passed"] is True

    d3 = behavioral_parity_summary(
        reference_spike_count=1000,
        candidate_spike_count=1005,
        reference_success_fraction=0.5,
        candidate_success_fraction=0.52,
        reference_commit="abcdef1",
    )
    assert d3["parity_class"] == "D3"
    assert d3["passed"] is True


def test_service_determinism_returns_replay_reference_trace() -> None:
    result = determinism(_p3_payload())
    assert result["classification"] == "PLAYGROUND_CPU_DETERMINISM"
    assert result["passed"] is True
    reference = result["reference"]
    assert isinstance(reference, dict)
    assert reference["seed"] == 12345
    assert len(reference["action_sequence"]) == 4
    assert len(reference["reward_sequence"]) == 4
    assert result["scientific_evidence"] is False
