#!/usr/bin/env python3
"""Reject MHRN/result leakage into the independent Brian2 reference package."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "reference" / "stage1_topology_brian2"
FORBIDDEN_TEXT = (
    "canonical MHRN effect",
    "equivalence bound",
    "replication classification",
    "EVID-2026-19",
    "EXP-S1-TOPO-PROMO-R1-20260927",
    "canonical_targets",
    "frozen_bounds",
    "equivalence_bounds",
    "research/experiments",
    "research/registry/evidence",
)
FORBIDDEN_IMPORT_PREFIXES = ("src", "scripts", "research")


def main() -> int:
    violations: list[str] = []
    protocol_path = PACKAGE / "reference_protocol.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    serialized = json.dumps(protocol, sort_keys=True).lower()
    for forbidden in (
        "canonical_targets",
        "frozen_bounds",
        "evid-2026-19",
        "exp-s1-topo-promo-r1-20260927",
        "equivalence_bounds",
    ):
        if forbidden in serialized:
            violations.append(f"reference_protocol.json: leaked {forbidden}")
    for path in sorted(PACKAGE.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_TEXT:
            if token in text:
                violations.append(f"{path.name}: forbidden text {token}")
        tree = ast.parse(text, filename=str(path))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                if name.startswith(FORBIDDEN_IMPORT_PREFIXES):
                    violations.append(f"{path.name}: forbidden import {name}")
    # Reject code that attempts to traverse into research artifacts or to encode
    # the complete canonical latency target vector directly.
    target_vector_signatures = (
        "-10.0,-3.0,-1.0,-3.0,-2.5",
        "[-10.0, -3.0, -1.0, -3.0, -2.5]",
    )
    for path in sorted(PACKAGE.glob("*.py")):
        compact = path.read_text(encoding="utf-8").replace(" ", "")
        for signature in target_vector_signatures:
            if signature.replace(" ", "") in compact:
                violations.append(f"{path.name}: leaked canonical target vector")

    payload = {
        "package": str(PACKAGE.relative_to(ROOT)),
        "violations": violations,
        "pass": not violations,
    }
    print(json.dumps(payload, indent=2))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
