"""Canonical comparison of bounded Builder-shaped backend results."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .d1_spikes import exact_spike_parity
from .d2_state import max_abs_error
from .d3_behavior import exact_behavior_parity
from .fingerprint import config_fingerprint, execution_fingerprint


def _fingerprint(result: Mapping[str, Any], backend_name: str) -> str:
    config = result.get("config")
    config_map = dict(config) if isinstance(config, Mapping) else {}
    seed = int(config_map.get("seed", 0))
    ticks = max(1, int(config_map.get("ticks", 1)))
    return execution_fingerprint(
        seed=seed,
        config_hash=config_fingerprint(config_map),
        backend_name=backend_name,
        backend_version="builder-v1",
        ticks=ticks,
    )


def compare_builder_runs(
    cpu: dict[str, Any],
    gpu: dict[str, Any],
) -> dict[str, object]:
    try:
        execution = gpu["execution"]
        actual_gpu = (
            execution["neuron_backend"] in {"cuda_membrane", "cuda_pan"}
            and execution["gpu_membrane_ticks"] > 0
        )
        d1_result = exact_spike_parity(
            cpu["monitors"]["spikes"],
            gpu["monitors"]["spikes"],
        )
        digest_exact = (
            bool(cpu["monitors"]["full_spike_digest"])
            and cpu["monitors"]["full_spike_digest"]
            == gpu["monitors"]["full_spike_digest"]
        )
        d1 = d1_result.passed and digest_exact

        left = [v for row in cpu["monitors"]["state_samples"] for v in row["v"]]
        right = [v for row in gpu["monitors"]["state_samples"] for v in row["v"]]
        error = max_abs_error(left, right)

        cpu_loop = cpu["closed_loop"]
        gpu_loop = gpu["closed_loop"]
        embodied = "sandbox" in cpu or "sandbox" in gpu
        body_left = (
            cpu["sandbox"]["full_trajectory_digest"]
            if embodied and "sandbox" in cpu
            else None
        )
        body_right = (
            gpu["sandbox"]["full_trajectory_digest"]
            if embodied and "sandbox" in gpu
            else None
        )
        d3_result = exact_behavior_parity(
            reference_actions=cpu_loop["action_history"],
            candidate_actions=gpu_loop["action_history"],
            reference_targets=cpu_loop["target_history"],
            candidate_targets=gpu_loop["target_history"],
            reference_rewards=cpu_loop["reward_history"],
            candidate_rewards=gpu_loop["reward_history"],
            reference_body_digest=body_left,
            candidate_body_digest=body_right,
        )
        d3 = d3_result.passed

        pan_error: float | None = None
        synapse_error: float | None = None
        resource_error: float | None = None
        queue_error: float | None = None
        rng_exact: bool | None = None
        state_ok = True

        if "research_state" in cpu and "research_state" in gpu:
            left_state, right_state = cpu["research_state"], gpu["research_state"]
            left_edges = left_state["synapses"]["edges"]
            right_edges = right_state["synapses"]["edges"]
            topology = [(e[0], e[1], e[3]) for e in left_edges] == [
                (e[0], e[1], e[3]) for e in right_edges
            ]
            synapse_error = max_abs_error(
                [e[2] for e in left_edges], [e[2] for e in right_edges]
            )
            resource_error = max_abs_error(
                left_state["release_resources"]
                + left_state["eligibility"]
                + left_state["neuron_traces"],
                right_state["release_resources"]
                + right_state["eligibility"]
                + right_state["neuron_traces"],
            )
            queue_error = max_abs_error(
                [x for row in left_state["pending_currents"] for x in row],
                [x for row in right_state["pending_currents"] for x in row],
            )
            rng_exact = left_state["rng_state"] == right_state["rng_state"]
            state_ok = (
                topology
                and synapse_error <= 1e-12
                and resource_error <= 1e-12
                and queue_error <= 1e-12
                and rng_exact
                and left_state["last_spike"] == right_state["last_spike"]
                and left_state["eligibility_last_tick"]
                == right_state["eligibility_last_tick"]
            )

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

        if execution["neuron_backend"] == "cuda_pan":
            state_ok = (
                state_ok
                and pan_error is not None
                and execution.get("gpu_pan_population_calls", 0)
                == execution["gpu_membrane_ticks"]
                and execution.get("gpu_neuron_trace_ticks", 0)
                == execution["gpu_membrane_ticks"]
                and execution.get("gpu_delay_consumed_ticks", 0)
                == execution["gpu_membrane_ticks"]
                and execution.get("gpu_pan_ticks", 0) == execution["gpu_membrane_ticks"]
            )

        cpu_fp = _fingerprint(cpu, "cpu")
        gpu_fp = _fingerprint(gpu, str(execution["neuron_backend"]))
        return {
            "passed": actual_gpu and d1 and error <= 1e-4 and d3 and state_ok,
            "D2_full_pan_state_max_error": pan_error,
            "D2_full_synaptic_weight_max_error": synapse_error,
            "D2_STP_eligibility_max_error": resource_error,
            "D2_pending_current_max_error": queue_error,
            "RNG_builder_state_exact": rng_exact,
            "gpu_pan_population_calls": execution.get("gpu_pan_population_calls", 0),
            "gpu_neuron_trace_ticks": execution.get("gpu_neuron_trace_ticks", 0),
            "gpu_delay_consumed_ticks": execution.get("gpu_delay_consumed_ticks", 0),
            "gpu_synaptic_emissions": execution.get("gpu_synaptic_emissions", 0),
            "gpu_synaptic_plasticity_calls": execution.get(
                "gpu_synaptic_plasticity_calls", 0
            ),
            "gpu_synaptic_reward_calls": execution.get("gpu_synaptic_reward_calls", 0),
            "D1_full_spike_digest_exact": d1,
            "D2_sampled_voltage_max_error": error,
            "D3_actions_targets_rewards_exact": d3,
            "D3_full_body_trajectory_exact": (
                d3_result.details.get("body_exact") if embodied else None
            ),
            "cpu_execution_fingerprint": cpu_fp,
            "gpu_execution_fingerprint": gpu_fp,
            "gpu_membrane_ticks": execution["gpu_membrane_ticks"],
            "gpu_pan_feedback_calls": execution.get("gpu_pan_feedback_calls", 0),
            "scope": (
                "REAL_BUILDER_CUDA_PAN_SYNAPSES_RESIDENT_QUEUE_CPU_WORLD"
                if execution["neuron_backend"] == "cuda_pan"
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
