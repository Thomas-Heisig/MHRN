"""Print a descriptive analysis for a PAN Playground night run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.playground.night_run import analyze_run


def latest_run(root: Path) -> Path:
    candidates = sorted(
        (path for path in root.glob("PGNIGHT-*") if path.is_dir()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(f"no night runs under {root}")
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--session",
        default="last",
        help="Night-run directory, run ID, or 'last'.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("playground_sessions/night_runs"),
    )
    args = parser.parse_args()
    if args.session == "last":
        run_dir = latest_run(args.root)
    else:
        candidate = Path(args.session)
        run_dir = candidate if candidate.is_dir() else args.root / args.session
    result = analyze_run(run_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
