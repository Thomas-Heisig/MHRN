"""Print a source-bound Stage 0-6 inventory without promoting scientific evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.dashboard.development_timeline import build_development_timeline
from src.dashboard.verification import current_git_head, inspect_source_tree


def audit(root: Path) -> dict[str, Any]:
    """Expose existing criteria, declared limits and path presence; do not mutate."""
    root = root.resolve()
    timeline = build_development_timeline(root)
    source = inspect_source_tree(root)
    stages = [stage for stage in timeline["stages"] if 0 <= stage["stage"] <= 6]
    missing = sorted(
        {
            name
            for stage in stages
            for name in (*stage["relevant_modules"], *stage["relevant_tests"])
            if not (root / name).exists()
        }
    )
    return {
        "schema_version": 1,
        "kind": "repository_inventory_not_empirical_verification",
        "git_commit": current_git_head(root),
        "source_digest": source.digest,
        "working_tree_changes": list(source.mismatching_files),
        "stages": stages,
        "missing_declared_module_or_test_paths": missing,
        "scientific_evidence_promotion": False,
        "neural_memory_complete": False,
        "interpretation": "reached is a scoped engineering status; path existence is not verification",
    }


def main() -> None:
    """Output JSON only; redirect outside frozen scientific artifact directories."""
    print(
        json.dumps(
            audit(Path(__file__).resolve().parents[1]), indent=2, ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()
