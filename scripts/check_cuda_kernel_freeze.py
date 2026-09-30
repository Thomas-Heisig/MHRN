"""Verify Wave-4 CUDA kernel extraction preserved kernel bytes exactly."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = (
    (
        ROOT / "src" / "playground" / "cuda" / "recurrent.cu",
        ROOT / "src" / "acceleration" / "cuda" / "recurrent" / "kernel.cu",
    ),
    (
        ROOT / "src" / "playground" / "cuda" / "builder_synapses.cu",
        ROOT / "src" / "acceleration" / "cuda" / "plasticity" / "kernel.cu",
    ),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kernel_mismatches() -> list[str]:
    mismatches: list[str] = []
    for legacy, canonical in PAIRS:
        if not legacy.is_file() or not canonical.is_file():
            mismatches.append(
                f"missing kernel pair: {legacy.relative_to(ROOT)} / "
                f"{canonical.relative_to(ROOT)}"
            )
            continue
        if legacy.read_bytes() != canonical.read_bytes():
            mismatches.append(
                f"kernel changed during extraction: "
                f"{legacy.relative_to(ROOT)}={sha256(legacy)} "
                f"{canonical.relative_to(ROOT)}={sha256(canonical)}"
            )
    return mismatches


def main() -> int:
    mismatches = kernel_mismatches()
    if mismatches:
        raise SystemExit("\n".join(mismatches))
    for legacy, canonical in PAIRS:
        print(
            f"kernel freeze PASS: {canonical.relative_to(ROOT)} "
            f"sha256={sha256(canonical)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
