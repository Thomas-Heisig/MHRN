"""Verify archived reproduction bytes without modifying or rerunning the study."""

import hashlib
import json
from pathlib import Path


def main() -> None:
    report = (
        Path(__file__).resolve().parents[1]
        / "research/reviews/DETERMINISM_REPRODUCTION_20261024"
    )
    artifacts = report / "artifacts"
    checksums = json.loads((artifacts / "sha256sums.json").read_text(encoding="utf-8"))
    for name, expected in checksums.items():
        target = artifacts / name
        if target.resolve().parent != artifacts.resolve():
            raise ValueError(f"Invalid artifact path: {name}")
        if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Reproduction artifact changed: {name}")
    freeze = json.loads((artifacts / "freeze.json").read_text(encoding="utf-8"))
    actual = hashlib.sha256((report / "reproduce.py").read_bytes()).hexdigest()
    if actual != freeze["harness_sha256"]:
        raise ValueError("Executed reproduction harness changed")
    print(f"PASS: {len(checksums)} immutable artifacts and executed harness")


if __name__ == "__main__":
    main()
