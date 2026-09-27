#!/usr/bin/env python3
"""Verify pre-freeze Stage-1 topology efficiency calibration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from run_stage1_topology_efficiency_calibration import (
    OUT,
    PREREG,
    choose_3d,
    choose_5d,
    read_json,
    summarize,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []
    result_path = OUT / "result.json"
    data_path = OUT / "data" / "calibration.json"
    for path in (result_path, data_path):
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(ROOT)}")
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1

    prereg = read_json(PREREG)
    result = read_json(result_path)
    rows_raw: Any = json.loads(data_path.read_text(encoding="utf-8"))
    rows = [dict(row) for row in rows_raw if isinstance(row, dict)]

    seeds = list(map(int, prereg["calibration"]["seeds"]))
    currents = list(map(float, prereg["calibration"]["candidate_stimulus_currents"]))
    expected_runs = 2 * len(seeds) * len(currents)
    if len(rows) != expected_runs:
        errors.append(f"expected {expected_runs} calibration runs, got {len(rows)}")

    if any(int(row["seed"]) in set(map(int, prereg["evaluation"]["seeds"])) for row in rows):
        errors.append("evaluation seed appeared in calibration DATA")

    for graph_condition in ("3d", "5d"):
        for current in currents:
            count = sum(
                row["graph_condition"] == graph_condition
                and float(row["stimulus_current"]) == current
                for row in rows
            )
            if count != len(seeds):
                errors.append(
                    f"coverage mismatch for {graph_condition} current={current}: {count}"
                )

    if any(int(row["node_count"]) != 64 for row in rows):
        errors.append("calibration node_count mismatch")
    if any(int(row["edge_count"]) != 246 for row in rows):
        errors.append("calibration edge_count mismatch")

    recomputed: dict[str, dict[str, dict[str, float]]] = {"3d": {}, "5d": {}}
    for graph_condition in ("3d", "5d"):
        for current in currents:
            selected = [
                row
                for row in rows
                if row["graph_condition"] == graph_condition
                and float(row["stimulus_current"]) == current
            ]
            recomputed[graph_condition][str(current)] = summarize(selected)

    if result.get("summaries") != recomputed:
        errors.append("calibration summaries differ from deterministic recomputation")

    selected_3d = choose_3d(recomputed["3d"])
    selected_5d = choose_5d(recomputed["5d"])
    selection = result.get("selection", {})
    if selection.get("3d_recruitment_matched_stimulus_current") != selected_3d:
        errors.append("3d recruitment-matched selection mismatch")
    if selection.get("5d_high_recruitment_stimulus_current") != selected_5d:
        errors.append("5d high-recruitment selection mismatch")

    payload = {
        "status": "PASS" if not errors else "FAIL",
        "calibration_id": result.get("calibration_id"),
        "runs": len(rows),
        "selection": selection,
        "errors": errors,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
