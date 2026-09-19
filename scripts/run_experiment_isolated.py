#!/usr/bin/env python3
"""Run a scientific experiment in an isolated Git worktree."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _run(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout


def _status(repo: Path) -> str:
    return _run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=repo,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--export-dir", required=True)
    args = parser.parse_args()

    primary = Path(_run(["git", "rev-parse", "--show-toplevel"], Path.cwd()).strip())
    primary = primary.resolve()
    before = _status(primary)
    if before:
        raise RuntimeError("primary checkout must be clean before isolated execution")

    head = _run(["git", "rev-parse", "HEAD"], primary).strip()
    worktree = Path(tempfile.mkdtemp(prefix="mhrn-exp-")).resolve()
    export_root = Path(args.export_dir).resolve()
    export_root.mkdir(parents=True, exist_ok=True)
    export_exp = export_root / args.experiment_id
    if export_exp.exists():
        raise RuntimeError(f"export target exists: {export_exp}")

    added = False
    dirty_after = ""
    try:
        _run(["git", "worktree", "add", "--detach", str(worktree), head], primary)
        added = True
        if _status(worktree):
            raise RuntimeError("isolated worktree is not clean before execution")

        env = os.environ.copy()
        env["PYTHONPATH"] = str(worktree)
        env["MHRN_ISOLATED_EXPERIMENT"] = "1"
        env["MHRN_SOURCE_FREEZE_COMMIT"] = head

        _run([sys.executable, args.runner], worktree, env)
        experiment_dir = worktree / "research" / "experiments" / args.experiment_id
        if not experiment_dir.is_dir():
            raise RuntimeError(f"missing generated experiment: {experiment_dir}")
        _run([sys.executable, args.verifier], worktree, env)

        dirty_after = _status(worktree)
        shutil.copytree(experiment_dir, export_exp)
    finally:
        if added:
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(worktree)],
                cwd=primary,
                check=False,
            )
            subprocess.run(["git", "worktree", "prune"], cwd=primary, check=False)
        else:
            shutil.rmtree(worktree, ignore_errors=True)

    after = _status(primary)
    if after != before:
        raise RuntimeError("primary checkout changed during isolated execution")

    audit = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "source_freeze_commit": head,
        "primary_checkout_clean_before": before == "",
        "primary_checkout_clean_after": after == "",
        "isolated_worktree_dirty_after_execution": bool(dirty_after),
        "generated_data_confined_to_isolated_worktree": True,
    }
    (export_root / "isolation_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
