"""Plasticity-rule descriptors for exploratory Playground sessions."""

from __future__ import annotations

PLASTICITY_RULES: dict[str, dict[str, object]] = {
    "none": {"name": "none", "label": "No plasticity", "available": True},
    "stdp": {"name": "stdp", "label": "Pair-based STDP", "available": True},
    "triplet_stdp": {
        "name": "triplet_stdp",
        "label": "Triplet STDP",
        "available": True,
        "note": "Exploratory trace-based triplet approximation.",
    },
    "metaplasticity": {
        "name": "metaplasticity",
        "label": "Metaplasticity",
        "available": True,
        "note": "Activity-dependent learning-rate modulation.",
    },
    "eligibility_trace": {
        "name": "eligibility_trace",
        "label": "Eligibility trace",
        "available": True,
    },
    "three_factor": {
        "name": "three_factor",
        "label": "Three-factor learning",
        "available": True,
        "note": "Eligibility × oscillatory exploratory modulator.",
    },
    "homeostatic": {
        "name": "homeostatic",
        "label": "Homeostatic weight scaling",
        "available": True,
    },
    "structural": {
        "name": "structural",
        "label": "Structural plasticity",
        "available": True,
        "note": "Bounded exploratory edge addition/removal; not canonical MHRN growth.",
    },
    "delay_plasticity": {
        "name": "delay_plasticity",
        "label": "Delay plasticity",
        "available": True,
        "note": "Bounded exploratory delay adjustment.",
    },
}


def require_plasticity_rule(name: str) -> dict[str, object]:
    rule = PLASTICITY_RULES.get(name)
    if rule is None:
        raise ValueError(f"unknown playground plasticity rule: {name}")
    if not bool(rule.get("available")):
        raise ValueError(f"playground plasticity rule is not executable yet: {name}")
    return rule
