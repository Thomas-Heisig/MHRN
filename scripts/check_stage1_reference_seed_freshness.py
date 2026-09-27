#!/usr/bin/env python3
"""Freeze-gate seed freshness check for Stage-1 reference replication."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-REFERENCE-R1.json"
ALLOWED = PREREG.relative_to(ROOT).as_posix()


def main() -> int:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    seeds = [str(int(v)) for v in prereg["evaluation"]["seeds"]]
    files = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    collisions: dict[str, list[str]] = {}
    for seed in seeds:
        found: list[str] = []
        for name in files:
            if not name or name == ALLOWED:
                continue
            path = ROOT / name
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if re.search(rf"(?<!\\d){re.escape(seed)}(?!\\d)", content):
                found.append(name)
        if found:
            collisions[seed] = sorted(found)
    payload = {
        "preregistration_id": prereg["preregistration_id"],
        "checked_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "seeds": prereg["evaluation"]["seeds"],
        "collisions": collisions,
        "collision_free": not collisions,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["collision_free"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
