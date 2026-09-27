"""Synapse model descriptors for the non-canonical Playground."""

from __future__ import annotations

SYNAPSE_MODELS: dict[str, dict[str, object]] = {
    "static": {
        "name": "static",
        "label": "Static weighted synapse",
        "available": True,
    },
    "stdp": {
        "name": "stdp",
        "label": "Pair-based STDP synapse",
        "available": True,
    },
    "triplet_stdp": {
        "name": "triplet_stdp",
        "label": "Triplet STDP synapse",
        "available": True,
        "note": "Exploratory bounded approximation.",
    },
    "quantal_stp": {
        "name": "quantal_stp",
        "label": "Quantal / short-term plastic synapse",
        "available": True,
        "note": "Exploratory release-probability and depression model.",
    },
    "eligibility_trace": {
        "name": "eligibility_trace",
        "label": "Eligibility-trace synapse",
        "available": True,
        "note": "Exploratory local eligibility state.",
    },
    "three_factor": {
        "name": "three_factor",
        "label": "Three-factor synapse",
        "available": True,
        "note": "Exploratory eligibility × modulator update.",
    },
    "pan_stp_stdp": {
        "name": "pan_stp_stdp",
        "label": "PAN · STP + pair-STDP",
        "available": True,
        "note": (
            "Exploratory combination of release-state depression/recovery and "
            "pair-STDP; not a canonical PAN or MHRN mechanism."
        ),
    },
    "delay_plastic": {
        "name": "delay_plastic",
        "label": "Delay-plastic synapse",
        "available": True,
        "note": "Exploratory bounded delay adaptation.",
    },
}


def require_synapse_model(name: str) -> dict[str, object]:
    model = SYNAPSE_MODELS.get(name)
    if model is None:
        raise ValueError(f"unknown playground synapse model: {name}")
    if not bool(model.get("available")):
        raise ValueError(f"playground synapse model is not executable yet: {name}")
    return model
