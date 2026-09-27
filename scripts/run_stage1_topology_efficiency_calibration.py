#!/usr/bin/env python3
"""Calibration-only runner for Stage-1 topology efficiency R1.

This is method-development/calibration DATA, not confirmatory evaluation and not EVID.
It may run while the efficiency preregistration is DRAFT, but it must never read or
execute the evaluation seed block.
"""

from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path
from typing import Any

from run_stage1_topology_v2 import build_network, load_config

from src.research.canonical_state import canonical_state_digest

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research" / "preregistrations" / "PREREG-S1-TOPO-EFFICIENCY-R1.json"
OUT = ROOT / "research" / "calibrations" / "CAL-S1-TOPO-EFFICIENCY-R1-20260927"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _topology_prereg(prereg: dict[str, Any]) -> dict[str, Any]:
    adapted = dict(prereg)
    adapted["conditions"] = {
        "3d": prereg["conditions"]["3d_reference"]["shape"],
        "5d": prereg["conditions"]["5d_reference"]["shape"],
        "5d_shuffled": prereg["conditions"]["5d_shuffled"]["shape"],
        "random_graph": prereg["conditions"]["random_graph"]["shape"],
    }
    matched = dict(prereg["matched_budgets"])
    matched["stimulus_current"] = float(
        prereg["calibration"]["reference_stimulus_current"]
    )
    adapted["matched_budgets"] = matched
    return adapted


def simulate(
    config: dict[str, Any],
    prereg: dict[str, Any],
    graph_condition: str,
    seed: int,
    stimulus_current: float,
) -> dict[str, Any]:
    weight = float(prereg["matched_budgets"]["synaptic_weight"])
    network, neuron_ids, coords, edges = build_network(
        config, _topology_prereg(prereg), graph_condition, seed, weight
    )
    before = canonical_state_digest(network)
    ticks = int(prereg["matched_budgets"]["evaluation_ticks"])
    stimulus_ticks = int(prereg["matched_budgets"]["stimulus_ticks"])
    input_labels = [int(v) for v in prereg["matched_budgets"]["stimulus_input_labels"]]
    output_labels = [int(v) for v in prereg["matched_budgets"]["output_labels"]]
    input_ids = [neuron_ids[label] for label in input_labels]
    output_ids = {neuron_ids[label] for label in output_labels}

    active: set[int] = set()
    active_outputs: set[int] = set()
    total_spikes = 0
    delivered_events = 0
    for tick in range(ticks):
        if tick < stimulus_ticks:
            network.inject_current_batch(
                {neuron_id: stimulus_current for neuron_id in input_ids}
            )
        result = network.step()
        spikes = {int(v) for v in result.spike_ids}
        total_spikes += int(result.spikes_this_tick)
        delivered_events += int(result.delivered_events)
        active.update(spikes)
        active_outputs.update(spikes & output_ids)

    return {
        "graph_condition": graph_condition,
        "seed": seed,
        "stimulus_current": stimulus_current,
        "node_count": len(neuron_ids),
        "edge_count": len(edges),
        "final_active_fraction": len(active) / float(len(neuron_ids)),
        "output_reach_fraction": len(active_outputs) / float(len(output_ids)),
        "total_spikes": total_spikes,
        "delivered_events": delivered_events,
        "state_digest_before": before,
        "state_digest_after": canonical_state_digest(network),
        "edge_digest": hashlib.sha256(json.dumps(edges).encode()).hexdigest(),
        "coordinate_digest": hashlib.sha256(json.dumps(coords).encode()).hexdigest(),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, float]:
    return {
        "n": len(rows),
        "final_active_fraction_median": float(
            statistics.median(float(row["final_active_fraction"]) for row in rows)
        ),
        "output_reach_fraction_median": float(
            statistics.median(float(row["output_reach_fraction"]) for row in rows)
        ),
        "delivered_events_median": float(
            statistics.median(float(row["delivered_events"]) for row in rows)
        ),
        "total_spikes_median": float(
            statistics.median(float(row["total_spikes"]) for row in rows)
        ),
    }


def choose_3d(summary: dict[str, dict[str, float]]) -> float | None:
    for current in sorted(map(float, summary)):
        row = summary[str(current)]
        if (
            0.84 <= row["final_active_fraction_median"] <= 0.90
            and row["output_reach_fraction_median"] >= 0.95
            and row["delivered_events_median"] >= 32
        ):
            return current
    return None


def choose_5d(summary: dict[str, dict[str, float]]) -> float | None:
    for current in sorted(map(float, summary)):
        row = summary[str(current)]
        if (
            row["final_active_fraction_median"] >= 0.98
            and row["output_reach_fraction_median"] >= 0.95
            and row["delivered_events_median"] >= 32
        ):
            return current
    return None


def main() -> int:
    prereg = read_json(PREREG)
    if prereg.get("status") != "DRAFT_BEFORE_FREEZE":
        raise RuntimeError("calibration is allowed only while preregistration is DRAFT")
    if prereg.get("execution_authorized") is not False:
        raise RuntimeError(
            "confirmatory execution must remain unauthorized during calibration"
        )
    if OUT.exists():
        raise FileExistsError(f"Refusing to overwrite calibration: {OUT}")

    calibration_seeds = list(map(int, prereg["calibration"]["seeds"]))
    evaluation_seeds = set(map(int, prereg["evaluation"]["seeds"]))
    if set(calibration_seeds) & evaluation_seeds:
        raise RuntimeError("calibration and evaluation seeds overlap")

    currents = list(map(float, prereg["calibration"]["candidate_stimulus_currents"]))
    config = load_config()
    rows: list[dict[str, Any]] = []
    for graph_condition in ("3d", "5d"):
        for current in currents:
            for seed in calibration_seeds:
                rows.append(simulate(config, prereg, graph_condition, seed, current))

    by_graph: dict[str, dict[str, dict[str, float]]] = {"3d": {}, "5d": {}}
    for graph_condition in ("3d", "5d"):
        for current in currents:
            selected = [
                row
                for row in rows
                if row["graph_condition"] == graph_condition
                and float(row["stimulus_current"]) == current
            ]
            by_graph[graph_condition][str(current)] = summarize(selected)

    selected_3d = choose_3d(by_graph["3d"])
    selected_5d = choose_5d(by_graph["5d"])
    result = {
        "schema_version": 1,
        "calibration_id": "CAL-S1-TOPO-EFFICIENCY-R1-20260927",
        "preregistration_id": prereg["preregistration_id"],
        "role": "pre-freeze calibration only; not confirmatory DATA and not EVID",
        "calibration_seeds": calibration_seeds,
        "evaluation_seeds_read_or_executed": False,
        "candidate_stimulus_currents": currents,
        "summaries": by_graph,
        "selection": {
            "3d_recruitment_matched_stimulus_current": selected_3d,
            "5d_high_recruitment_stimulus_current": selected_5d,
            "3d_recruitment_matched_gate_passed": selected_3d is not None,
            "5d_high_recruitment_gate_passed": selected_5d is not None,
        },
        "selection_inputs_excluded": prereg["calibration"][
            "forbidden_selection_inputs"
        ],
        "preregistration_sha256": sha256(PREREG),
    }

    write_json(OUT / "data" / "calibration.json", rows)
    write_json(OUT / "result.json", result)
    print(json.dumps(result["selection"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
