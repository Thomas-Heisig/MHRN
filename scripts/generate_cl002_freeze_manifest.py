#!/usr/bin/env python3
"""Generate the pre-execution SHA-256 manifest for EXP-S6-SEM-CL-002."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT / "research" / "preregistrations" / "frozen" / "EXP-S6-SEM-CL-002-FREEZE.json"
)
BOUND_FILES = (
    "src/research/continual_semantization_controls.py",
    "src/research/continual_semantization.py",
    "src/memory/semantic.py",
    "src/memory/neural_episodic.py",
    "scripts/run_semantization_split_mnist_cl002.py",
    "research/preregistrations/operational/EXP-S6-SEM-CL-002.json",
    "research/preregistrations/amendments/EXP-S6-SEM-CL-002-A1.json",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    hashes = {relative: sha256(ROOT / relative) for relative in BOUND_FILES}
    payload = {
        "schema_version": 1,
        "experiment_id": "EXP-S6-SEM-CL-002",
        "status": "pre_execution_source_freeze",
        "generated_before_empirical_run": True,
        "execution_authorized": False,
        "hash_algorithm": "SHA-256",
        "sha256": hashes,
        "automatic_evidence_promotion": False,
        "human_review_required": True,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUTPUT.relative_to(ROOT))
    for relative, digest in hashes.items():
        print(f"{digest}  {relative}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
