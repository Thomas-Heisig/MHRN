#!/usr/bin/env python3
"""Safely fast-forward a local checkout to canonical origin/main."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def _run(args: list[str], cwd: Path) -> str:
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-path", action="append", default=[])
    args = parser.parse_args()

    root = Path(_run(["git", "rev-parse", "--show-toplevel"], Path.cwd())).resolve()
    status = _run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        root,
    )
    if status:
        raise RuntimeError(
            "safe sync refuses to overwrite local changes:\n" + status
        )

    subprocess.run(["git", "fetch", "origin", "main"], cwd=root, check=True)
    branch = _run(["git", "branch", "--show-current"], root)
    if branch != "main":
        subprocess.run(["git", "switch", "main"], cwd=root, check=True)
    subprocess.run(
        ["git", "pull", "--ff-only", "origin", "main"],
        cwd=root,
        check=True,
    )

    head = _run(["git", "rev-parse", "HEAD"], root)
    origin_main = _run(["git", "rev-parse", "origin/main"], root)
    if head != origin_main:
        raise RuntimeError(f"HEAD {head} != origin/main {origin_main}")

    missing = [p for p in args.verify_path if not (root / p).exists()]
    if missing:
        raise RuntimeError(
            "sync reached origin/main but paths are missing: " + ", ".join(missing)
        )

    print(
        json.dumps(
            {
                "branch": "main",
                "head": head,
                "origin_main": origin_main,
                "clean_tree": True,
                "verified_paths": args.verify_path,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
