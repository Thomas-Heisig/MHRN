"""Compatibility orchestration for canonical Builder parity."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from src.verification.parity.runner import compare_builder_runs


def run_builder_parity(payload: Mapping[str, object]) -> dict[str, object]:
    """Run the Playground CPU/CUDA pair using canonical parity semantics."""

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
    cpu_loop = cast(dict[str, object], cpu["closed_loop"])
    gpu_loop = cast(dict[str, object], gpu["closed_loop"])
    return {
        "classification": "PLAYGROUND_BUILDER_BEHAVIORAL_PARITY",
        **compare_builder_runs(cpu, gpu),
        "seed": config.seed,
        "ticks": config.ticks,
        "behavioral_baseline": {
            "cpu": {
                key: cpu_loop[key]
                for key in ("episodes", "successes", "success_fraction")
            },
            "cuda": {
                key: gpu_loop[key]
                for key in ("episodes", "successes", "success_fraction")
            },
        },
    }


__all__ = ["compare_builder_runs", "run_builder_parity"]
