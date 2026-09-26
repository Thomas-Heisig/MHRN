#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from src.research.meta_system import build_crosswalk, render

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    errors: list[str] = []
    cross = build_crosswalk()
    if len(cross["directions"]) != 11:
        errors.append("direction count is not 11")
    rows = {q["research_question"]: q for q in cross["questions"]}
    for qid in ("RQ-EPIST-002", "RQ-ETH-001", "RQ-META-001", "RQ-META-002", "RQ-META-003"):
        if qid not in rows:
            errors.append(f"missing meta question {qid}")
        elif rows[qid]["direction"] != "DIR-11":
            errors.append(f"{qid} is not mapped to DIR-11")
    for path in sorted((ROOT / "research/meta/studies").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("execution_authorized") is not False or data.get("scientific_evidence") is not False:
            errors.append(f"{path}: design artifact illegally authorizes execution/evidence")
    for name, expected in render().items():
        path = ROOT / "research/generated" / name
        if not path.is_file() or path.read_text(encoding="utf-8") != expected:
            errors.append(f"generated drift: {name}")
    if errors:
        print("\n".join("ERROR: " + e for e in errors))
        return 1
    print("Meta research system checks passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
