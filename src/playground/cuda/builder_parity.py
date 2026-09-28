"""D1 and behavioral equivalence of actual CPU / CUDA-membrane Builder runs."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .runtime import max_abs_error


def compare_builder_runs(cpu: dict[str, Any], gpu: dict[str, Any]) -> dict[str, object]:
    try:
        actual_gpu = (
            gpu["execution"]["neuron_backend"] == "cuda_membrane"
            and gpu["execution"]["gpu_membrane_ticks"] > 0
        )
        d1 = (
            bool(cpu["monitors"]["full_spike_digest"])
            and cpu["monitors"]["full_spike_digest"]
            == gpu["monitors"]["full_spike_digest"]
        )
        left = [v for row in cpu["monitors"]["state_samples"] for v in row["v"]]
        right = [v for row in gpu["monitors"]["state_samples"] for v in row["v"]]
        error = max_abs_error(left, right)
        actions = bool(cpu["closed_loop"]["action_history"])
        d3 = actions and all(
            cpu["closed_loop"][name] == gpu["closed_loop"][name]
            for name in ("action_history", "target_history", "reward_history")
        )
        embodied = "sandbox" in cpu or "sandbox" in gpu
        body = (
            (
                cpu["sandbox"]["full_trajectory_digest"]
                == gpu["sandbox"]["full_trajectory_digest"]
            )
            if embodied
            else True
        )
        return {
            "passed": actual_gpu and d1 and error <= 1e-4 and d3 and body,
            "D1_full_spike_digest_exact": d1,
            "D2_sampled_voltage_max_error": error,
            "D3_actions_targets_rewards_exact": d3,
            "D3_full_body_trajectory_exact": body if embodied else None,
            "gpu_membrane_ticks": gpu["execution"]["gpu_membrane_ticks"],
            "scope": "REAL_BUILDER_CUDA_MEMBRANE_CPU_SYNAPSES_AND_ENVIRONMENT",
            "full_gpu_pan": False,
            "scientific_evidence": False,
        }
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        return {
            "passed": False,
            "failure_reason": str(exc),
            "scientific_evidence": False,
        }


def run_builder_parity(payload: Mapping[str, object]) -> dict[str, object]:
    from ..models import PlaygroundConfig
    from ..service import run

    options = {
        **payload,
        "persist": False,
        "ensemble_runs": 1,
        "offload_enabled": False,
    }
    config = PlaygroundConfig.from_mapping(options)
    if config.n_neurons > 256 or config.edge_budget > 4096:
        raise ValueError("Builder parity is bounded to 256 neurons and 4096 edges")
    cpu = run({**options, "neuron_backend": "cpu"})
    gpu = run({**options, "neuron_backend": "cuda_membrane"})
    return {
        "classification": "PLAYGROUND_BUILDER_BEHAVIORAL_PARITY",
        **compare_builder_runs(cpu, gpu),
        "seed": config.seed,
        "ticks": config.ticks,
    }
