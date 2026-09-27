#!/usr/bin/env python3
"""Freeze-gate seed freshness check for Stage-1 reference replication."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-REFERENCE-R1.json"
ALLOWED_PATHS = {
    PREREG.relative_to(ROOT).as_posix(),
    "reference/stage1_topology_brian2/reference_protocol.json",
}


def main() -> int:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    seeds = [str(int(v)) for v in prereg["evaluation"]["seeds"]]
    files = (
        subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        .decode()
        .split("\0")
    )
    collisions: dict[str, list[str]] = {seed: [] for seed in seeds}
    token_pattern = re.compile(
        r"(?<!\\d)(" + "|".join(re.escape(seed) for seed in seeds) + r")(?!\\d)"
    )

    for name in files:
        if not name or name in ALLOWED_PATHS:
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in token_pattern.finditer(content):
            collisions[match.group(1)].append(name)

    collisions = {
        seed: sorted(set(paths))
        for seed, paths in collisions.items()
        if paths
    }
    payload = {
        "preregistration_id": prereg["preregistration_id"],
        "checked_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "seeds": prereg["evaluation"]["seeds"],
        "allowed_paths": sorted(ALLOWED_PATHS),
        "collisions": collisions,
        "collision_free": not collisions,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["collision_free"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
