"""D1 and behavioral equivalence of actual CPU / CUDA-membrane Builder runs."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .runtime import max_abs_error


def compare_builder_runs(cpu: dict[str, Any], gpu: dict[str, Any]) -> dict[str, object]:
    try:
        actual_gpu = (
            gpu["execution"]["neuron_backend"] in {"cuda_membrane", "cuda_pan"}
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
        pan_error: float | None = None
        synapse_error: float | None = None
        state_ok = True
        if "research_state" in cpu and "research_state" in gpu:
            left_state, right_state = cpu["research_state"], gpu["research_state"]
            left_edges, right_edges = (
                left_state["synapses"]["edges"],
                right_state["synapses"]["edges"],
            )
            topology = [(e[0], e[1], e[3]) for e in left_edges] == [
                (e[0], e[1], e[3]) for e in right_edges
            ]
            synapse_error = max_abs_error(
                [e[2] for e in left_edges], [e[2] for e in right_edges]
            )
            state_ok = topology and synapse_error <= 1e-12
            pan_left, pan_right = left_state["pan_states"], right_state["pan_states"]
            if any(pan_left):

                def numeric(states: list[dict[str, Any]]) -> list[float]:
                    return [
                        float(value)
                        for state in states
                        for key in sorted(state)
                        for value in (
                            state[key] if isinstance(state[key], list) else [state[key]]
                        )
                    ]

                pan_error = max_abs_error(numeric(pan_left), numeric(pan_right))
                state_ok = (
                    state_ok
                    and pan_error <= 1e-12
                    and [sorted(s) for s in pan_left] == [sorted(s) for s in pan_right]
                )
        if gpu["execution"]["neuron_backend"] == "cuda_pan":
            state_ok = (
                state_ok
                and pan_error is not None
                and gpu["execution"].get("gpu_pan_ticks", 0)
                == gpu["execution"]["gpu_membrane_ticks"]
            )
        return {
            "passed": actual_gpu and d1 and error <= 1e-4 and d3 and body and state_ok,
            "D2_full_pan_state_max_error": pan_error,
            "D2_full_synaptic_weight_max_error": synapse_error,
            "D1_full_spike_digest_exact": d1,
            "D2_sampled_voltage_max_error": error,
            "D3_actions_targets_rewards_exact": d3,
            "D3_full_body_trajectory_exact": body if embodied else None,
            "gpu_membrane_ticks": gpu["execution"]["gpu_membrane_ticks"],
            "scope": (
                "REAL_BUILDER_CUDA_PAN_STATE_CPU_SYNAPSES_AND_ENVIRONMENT"
                if gpu["execution"]["neuron_backend"] == "cuda_pan"
                else "REAL_BUILDER_CUDA_MEMBRANE_CPU_SYNAPSES_AND_ENVIRONMENT"
            ),
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
    from ..builder.session import PlaygroundSession
    from ..models import PlaygroundConfig

    options = {
        **payload,
        "persist": False,
        "ensemble_runs": 1,
        "offload_enabled": False,
    }
    config = PlaygroundConfig.from_mapping(options)
    if config.n_neurons > 256 or config.edge_budget > 4096:
        raise ValueError("Builder parity is bounded to 256 neurons and 4096 edges")
    selected = "cuda_pan" if config.neuron_backend == "cuda_pan" else "cuda_membrane"
    cpu = PlaygroundSession(
        PlaygroundConfig.from_mapping({**options, "neuron_backend": "cpu"}),
        capture_research_state=True,
    ).run()
    gpu = PlaygroundSession(
        PlaygroundConfig.from_mapping({**options, "neuron_backend": selected}),
        capture_research_state=True,
    ).run()
    return {
        "classification": "PLAYGROUND_BUILDER_BEHAVIORAL_PARITY",
        **compare_builder_runs(cpu, gpu),
        "seed": config.seed,
        "ticks": config.ticks,
    }
