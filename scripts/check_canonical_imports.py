"""Fail-closed canonical import boundary gate for Wave 4."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    ROOT / "src" / "acceleration",
    ROOT / "src" / "verification",
)


def forbidden_imports() -> list[str]:
    failures: list[str] = []
    for root in TARGETS:
        for path in root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith("src.playground"):
                            failures.append(f"{path.relative_to(ROOT)}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    if module.startswith("src.playground"):
                        failures.append(
                            f"{path.relative_to(ROOT)}: from {module} import ..."
                        )
    return failures


def main() -> int:
    failures = forbidden_imports()
    if failures:
        raise SystemExit(
            "canonical acceleration/verification layers import Playground:\n"
            + "\n".join(failures)
        )
    print("canonical import boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
