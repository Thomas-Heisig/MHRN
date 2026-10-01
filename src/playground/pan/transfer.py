"""Matched synaptic transfer to disjoint cue channels with fresh-state controls."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from typing import cast

from .cue_controls import cue_control_overrides
from .cue_decoding import decode_cues
from .synaptic_checkpoint import SynapticCheckpoint


def _curve(state: dict[str, object], seed: int) -> list[dict[str, object]]:
    features = cast(list[list[float]], state["features"])
    labels = cast(list[int], state["labels"])
    split = len(features) * 2 // 3
    if split < 4:
        return []
    sizes = sorted(set([*range(4, split + 1, 4), split]))
    return [
        {
            "calibration_episodes": size,
            **decode_cues(
                features[:size] + features[split:],
                labels[:size] + labels[split:],
                seed=seed,
                train_episodes=size,
            ),
        }
        for size in sizes
    ]


def run_synaptic_transfer(payload: Mapping[str, object]) -> dict[str, object]:
    from ..builder.session import PlaygroundSession
    from ..models import PlaygroundConfig

    original = PlaygroundConfig.from_mapping(payload)
    if (
        original.n_neurons > 256
        or original.edge_budget > 4096
        or original.target_encoding != "one_hot"
        or original.action_space_size < 2
        or original.input_channels < 2 * original.action_space_size
    ):
        raise ValueError(
            "transfer requires one-hot cues, two disjoint cue banks, <=256 neurons and <=4096 edges"
        )
    pretrain_plasticity = payload.get("transfer_pretrain_plasticity", True)
    if type(pretrain_plasticity) is not bool:
        raise ValueError("transfer_pretrain_plasticity must be boolean")
    overrides = {
        **cue_control_overrides(),
        "target_cue_control": "aligned",
        "target_cue_channel": 0,
        "plasticity_rule": "stdp" if pretrain_plasticity else "none",
    }
    pretrain_config = PlaygroundConfig.from_mapping({**payload, **overrides})
    pretraining = PlaygroundSession(pretrain_config, capture_research_state=True).run()
    trained_state = cast(dict[str, object], pretraining["research_state"])
    checkpoint = SynapticCheckpoint.from_mapping(
        cast(dict[str, object], trained_state["synapses"])
    )
    novel_config = replace(
        pretrain_config,
        target_cue_channel=original.action_space_size,
        plasticity_rule="stdp",
    )
    conditions: list[dict[str, object]] = []
    for name, initial in (
        ("pretrained_synapses", checkpoint),
        ("fresh_synapses", None),
    ):
        result = PlaygroundSession(
            novel_config, initial_synapses=initial, capture_research_state=True
        ).run()
        state = cast(dict[str, object], result["research_state"])
        conditions.append(
            {
                "condition": name,
                "initial_synaptic_digest": initial.digest() if initial else None,
                "final_synaptic_digest": state["synaptic_digest"],
                "decoding_curve": _curve(state, original.seed),
                "full_spike_digest": cast(dict[str, object], result["monitors"])[
                    "full_spike_digest"
                ],
                "metrics": result["metrics"],
            }
        )
    return {
        "classification": "PLAYGROUND_SYNAPTIC_TRANSFER_PROBE",
        "scientific_evidence": False,
        "seed": original.seed,
        "pretraining_configuration": pretrain_config.to_dict(),
        "novel_configuration": novel_config.to_dict(),
        "transferred_state": checkpoint.to_dict(),
        "changed_pretraining_weights": sum(
            weight != original.weight for _, _, weight, _ in checkpoint.edges
        ),
        "reset_state": [
            "membrane",
            "PAN_hyperstate",
            "eligibility",
            "STP",
            "delayed_events",
            "policy",
            "environment",
        ],
        "conditions": conditions,
        "neural_transfer_claim": False,
        "scope": "SYNAPTIC_TRANSFER_EFFECT_ON_EXTERNAL_ACTIVITY_PROBE_CALIBRATION",
        "limitation": "Probe calibration curves do not establish neural task-learning speed or cognition.",
    }
