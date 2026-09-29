"""Fail-closed Wave-4 CUDA capability/learning-semantics gate."""

from __future__ import annotations

from pathlib import Path

from src.acceleration.cuda import CUDABackend
from src.acceleration.cuda.plasticity.contracts import (
    LEARNING_CONTRACT_ID,
    LEARNING_CONTRACT_STATUS,
    PLASTICITY_SEMANTICS,
)

ROOT = Path(__file__).resolve().parents[1]
LEARNING_CONTRACT = (
    ROOT / "docs" / "02-architecture" / "MHRN_LEARNING_SYNAPSE_CONTRACT.md"
)


def failures() -> list[str]:
    problems: list[str] = []
    caps = CUDABackend().capabilities()

    expected = {
        "supports_recurrent": True,
        "supports_plasticity": True,
        "supports_pan_hyperstate": False,
        "supports_structural_plasticity": False,
        "max_neurons": 4096,
        "max_ticks": 2000,
        "max_edges": 65536,
        "deterministic": True,
        "plasticity_semantics": "NON_CANONICAL_DRAFT",
        "execution_mode": "BOUNDED_REPLAY_REFERENCE",
    }
    actual = caps.to_mapping()
    for key, value in expected.items():
        if actual.get(key) != value:
            problems.append(
                f"CUDA capability mismatch: {key}={actual.get(key)!r}, expected {value!r}"
            )

    if PLASTICITY_SEMANTICS != "NON_CANONICAL_DRAFT":
        problems.append(
            "plasticity semantics must remain NON_CANONICAL_DRAFT until contract alignment"
        )
    if LEARNING_CONTRACT_ID != "mhrn-learning-synapse-v1":
        problems.append(f"unexpected learning contract id: {LEARNING_CONTRACT_ID}")
    if LEARNING_CONTRACT_STATUS != "ALIGNMENT_PENDING":
        problems.append(
            "learning contract status must remain ALIGNMENT_PENDING in Wave 4"
        )

    if not LEARNING_CONTRACT.is_file():
        problems.append("canonical learning/synapse contract document is missing")
    else:
        text = LEARNING_CONTRACT.read_text(encoding="utf-8")
        required = (
            "canonical design contract; backend implementation alignment pending",
            "learning_contract_id = mhrn-learning-synapse-v1",
            "CPU and CUDA must not implement two merely similar learning rules",
        )
        for phrase in required:
            if phrase not in text:
                problems.append(
                    "learning contract document no longer contains required boundary: "
                    + phrase
                )

    return problems


def main() -> int:
    problems = failures()
    if problems:
        raise SystemExit(
            "Wave-4 CUDA semantic boundary failed:\n" + "\n".join(problems)
        )
    print("Wave-4 CUDA semantic boundary: PASS")
    print("plasticity_semantics=NON_CANONICAL_DRAFT")
    print("learning_contract_status=ALIGNMENT_PENDING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
