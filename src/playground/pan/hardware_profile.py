"""Hardware planning profiles for PAN Playground.

Profiles are architecture estimates. They do not assert actual CUDA execution.
"""

from __future__ import annotations


def hardware_profile(name: str) -> dict[str, object]:
    profiles: dict[str, dict[str, object]] = {
        "reference_cpu": {
            "backend": "PYTHON_REFERENCE",
            "register_native": False,
            "ptx_gates": False,
            "runtime_verified": True,
        },
        "cuda_8gb_balanced_plan": {
            "backend": "CUDA_TARGET_PLAN",
            "vram_gib": 8,
            "usable_vram_gib_estimate": 6.9,
            "registers_per_neuron_plan": 256,
            "register_limited_neurons_estimate": 12_288,
            "recommended_synapses_estimate": 50_000_000,
            "target_synapses_per_neuron_estimate": 4_069,
            "register_native": "NOT_IMPLEMENTED",
            "ptx_gates": "NOT_IMPLEMENTED",
            "persistent_kernel": "NOT_IMPLEMENTED",
            "dynamic_parallelism": "NOT_IMPLEMENTED",
            "runtime_verified": False,
            "note": "Capacity values are planning estimates, not benchmark results.",
        },
    }
    if name not in profiles:
        raise ValueError(f"unknown hardware profile: {name}")
    return {"name": name, **profiles[name]}
