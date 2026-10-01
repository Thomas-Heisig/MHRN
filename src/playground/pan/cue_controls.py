"""Bounded matched input-cue interventions and pair-STDP ablation."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast


def run_cue_controls(payload: Mapping[str, object]) -> dict[str, object]:
    from ..models import PlaygroundConfig
    from ..service import run

    config = PlaygroundConfig.from_mapping(payload)
    if config.n_neurons > 256 or config.edge_budget > 4096:
        raise ValueError("cue controls are bounded to 256 neurons and 4096 edges")
    if config.target_encoding == "none" or config.action_space_size < 2:
        raise ValueError("cue controls require an encoded cue and at least two targets")
    overrides = cue_control_overrides()
    conditions: list[dict[str, object]] = []
    for plastic in (False, True):
        for cue in ("aligned", "randomized", "absent"):
            result = run(
                {
                    **payload,
                    **overrides,
                    "plasticity_rule": "stdp" if plastic else "none",
                    "target_cue_control": cue,
                }
            )
            conditions.append(
                {
                    "pair_stdp": plastic,
                    "input_cue_control": cue,
                    "probe": result["cue_decoding"],
                    "metrics": result["metrics"],
                    "target_history": cast(dict[str, object], result["closed_loop"])[
                        "target_history"
                    ],
                }
            )
    return {
        "classification": "PLAYGROUND_CUE_INTERVENTION_SUITE",
        "scientific_evidence": False,
        "seed": config.seed,
        "shared_configuration": config.to_dict(),
        "controlled_overrides": overrides,
        "conditions": conditions,
        "neural_learning_claim": False,
        "scope": "CUE_DECODE_AND_PAIR_STDP_ABLATION_WITHOUT_POLICY_CURRENT_FEEDBACK",
        "transfer_status": "SEPARATE_SYNAPTIC_TRANSFER_PROBE_AVAILABLE_TASK_LEARNING_UNPROVEN",
    }


def cue_control_overrides() -> dict[str, object]:
    return {
        "target_predictability": "stochastic",
        "behavior_target_mode": "cycle",
        "target_shuffle": False,
        "persist": False,
        "ensemble_runs": 1,
        "offload_enabled": False,
        "behavior_bias_current": 0.0,
        "behavior_learning_enabled": False,
        "action_coupling_strength": 0.0,
        "reward_signal_enabled": False,
        "sandbox_enabled": False,
        "posture_reward_enabled": False,
        "growth_enabled": False,
        "cortical_plasticity": False,
        "weight_decay": 0.0,
        "credit_assignment": "none",
        "synapse_model": "quantal_stp",
        "freeze_actions": False,
        "freeze_rewards": False,
        "frozen_action_sequence": [],
        "frozen_reward_sequence": [],
        "parity_reference_commit": "",
    }
