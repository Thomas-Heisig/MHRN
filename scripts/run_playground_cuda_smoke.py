"""Run a real single-tick CUDA gate-kernel smoke/parity check.

This script requires:
- NVIDIA driver visible to the process;
- ptxas on PATH (CUDA toolkit);
- a supported NVIDIA GPU.

It is intentionally not part of ordinary hosted CI because GitHub-hosted Linux
runners do not expose an NVIDIA device.
"""

from __future__ import annotations

import json

from src.playground.cuda import (
    GateLaunchInputs,
    compile_mapping,
    cpu_gate_reference,
    execute_gate_bundle,
    gate_execution_parity_summary,
)


def _inputs(bundle: object) -> GateLaunchInputs:
    manifest = getattr(bundle, "manifest")
    abi = manifest["kernel_abi"]
    pan_dimensions = int(abi["pan_dimensions"])
    return GateLaunchInputs.from_sequences(
        input_current=[1.0, 2.0, 0.5, 1.5],
        channel_masks=[0xFF] * 4,
        amplitudes=[1.0] * 8,
        reward_ring=[0.5],
        action_map=[
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            3.0,
            4.0,
            5.0,
            6.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        feedback_matrix=[0.0] * (4 * pan_dimensions),
        population=[0.0] * pan_dimensions,
        logits=[
            0.1,
            0.2,
            0.3,
            0.9,
            0.1,
            0.8,
            0.2,
            0.3,
            0.7,
            0.2,
            0.1,
            0.0,
            0.1,
            0.2,
            0.9,
            0.3,
        ],
        tick=0,
        target_index=2,
        previous_action=1,
        seed=12345,
        epsilon=0.0,
    )


def main() -> int:
    bundle = compile_mapping(
        {
            "closed_loop_preset": "minimal_closed_loop",
            "pan_feedback_gain": 0.0,
        }
    )
    inputs = _inputs(bundle)
    reference = cpu_gate_reference(bundle, inputs)
    cuda = execute_gate_bundle(bundle, inputs, block_size=64)
    parity = gate_execution_parity_summary(reference, cuda)
    result = {
        "classification": "PLAYGROUND_CUDA1_3_HARDWARE_SMOKE",
        "scientific_evidence": False,
        "reference": reference,
        "cuda": cuda,
        "parity": parity,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if parity["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
