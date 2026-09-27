#!/usr/bin/env python3
"""Freeze-gate seed freshness check for Stage-1 topology efficiency R1."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-EFFICIENCY-R1.json"
ALLOWED_PATH = PREREG.relative_to(ROOT).as_posix()


def tracked_files() -> list[str]:
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [item for item in raw.decode().split("\0") if item]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> int:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    seeds = [
        *map(int, prereg["calibration"]["seeds"]),
        *map(int, prereg["evaluation"]["seeds"]),
    ]
    files = tracked_files()
    collisions: dict[str, list[str]] = {}

    for seed in seeds:
        token = str(seed)
        found: list[str] = []
        for name in files:
            path = ROOT / name
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if token in text and name != ALLOWED_PATH:
                found.append(name)
        if found:
            collisions[token] = sorted(found)

    result = {
        "schema_version": 1,
        "preregistration_id": prereg["preregistration_id"],
        "checked_commit": git("rev-parse", "HEAD"),
        "git_dirty": bool(git("status", "--porcelain")),
        "calibration_seeds": prereg["calibration"]["seeds"],
        "evaluation_seeds": prereg["evaluation"]["seeds"],
        "allowed_occurrence": ALLOWED_PATH,
        "collisions": collisions,
        "collision_free": not collisions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["collision_free"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
