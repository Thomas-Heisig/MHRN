#!/usr/bin/env python3
"""Preregistered Stage-1 two-channel temporal-order task."""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import random
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from src.core import NeuralNetwork
from src.core.synapse import SynapseConfig
from src.research.canonical_state import canonical_state_digest

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "research/preregistrations/PREREG-S1-TEMP-ORDER-V2.json"
CONFIG = ROOT / "configs/learning_experiment.yaml"
HISTORICAL = ROOT / "research/preregistrations/PREREG-TEMP-002.json"
EXP_ID = "EXP-S1-TEMP-ORDER-V2-20260919"
OUT = ROOT / "research/experiments" / EXP_ID
ARMS = ("intact", "identity_destroyed")
ORDERS = ("forward", "reverse", "simultaneous")
ORDER_TRIALS = ("forward", "reverse")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = p * (len(ordered) - 1)
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    f = pos - lo
    return ordered[lo] * (1.0 - f) + ordered[hi] * f


def bootstrap_ci(values: list[float]) -> list[float]:
    rng = random.Random(int(hashlib.sha256(EXP_ID.encode()).hexdigest()[:12], 16))
    medians = [
        statistics.median([values[rng.randrange(len(values))] for _ in values])
        for _ in range(5000)
    ]
    return [percentile(medians, 0.025), percentile(medians, 0.975)]


def sign_test_p(values: list[float]) -> float:
    nonzero = [v for v in values if abs(v) > 1e-12]
    if not nonzero:
        return 1.0
    positives = sum(v > 0 for v in nonzero)
    tail = min(positives, len(nonzero) - positives)
    return min(
        1.0,
        2.0
        * sum(math.comb(len(nonzero), k) for k in range(tail + 1))
        / (2 ** len(nonzero)),
    )


def parameters(prereg: dict[str, Any], seed: int) -> tuple[float, float]:
    spec = prereg["seed_bound_nuisance_realizations"]
    rng = random.Random(seed ^ int(spec["xor_salt"]))
    w0, w1 = map(float, spec["synaptic_weight_uniform"])
    c0, c1 = map(float, spec["stimulus_current_uniform"])
    return rng.uniform(w0, w1), rng.uniform(c0, c1)


def network(
    config: dict[str, Any], seed: int, weight: float
) -> tuple[NeuralNetwork, dict[str, int]]:
    values = dict(config)
    values["dimensions"] = [6, 1, 1, 1, 1]
    values["initial_neurons"] = 0
    simulation = dict(values.get("simulation", {}))
    simulation["max_delay"] = max(4, int(simulation.get("max_delay", 4)))
    values["simulation"] = simulation
    net = NeuralNetwork(values, random.Random(seed))
    ids = {
        name: net.add_neuron((i, 0, 0, 0, 0))
        for i, name in enumerate(
            ("input_A", "hidden_A", "output_A", "input_B", "hidden_B", "output_B")
        )
    }
    net.input_cells.update((ids["input_A"], ids["input_B"]))
    net.output_cells.update((ids["output_A"], ids["output_B"]))
    syn = SynapseConfig(w_max=200.0)
    for source, target in (
        ("input_A", "hidden_A"),
        ("hidden_A", "output_A"),
        ("input_B", "hidden_B"),
        ("hidden_B", "output_B"),
    ):
        net.connect(ids[source], ids[target], weight, 1, config=syn)
    return net, ids


def schedule(order: str, gap: int) -> list[tuple[int, str]]:
    return {
        "forward": [(0, "A"), (gap, "B")],
        "reverse": [(0, "B"), (gap, "A")],
        "simultaneous": [(0, "A"), (0, "B")],
    }[order]


def decode(first: dict[str, int | None]) -> str:
    a, b = first["A"], first["B"]
    if a is None and b is None:
        return "no_output"
    if a is None:
        return "B_only"
    if b is None:
        return "A_only"
    if a == b:
        return "simultaneous"
    return "forward" if a < b else "reverse"


def simulate(
    config: dict[str, Any], prereg: dict[str, Any], seed: int, arm: str, order: str
) -> dict[str, Any]:
    weight, current = parameters(prereg, seed)
    net, ids = network(config, seed, weight)
    before = canonical_state_digest(net)
    logical = schedule(order, int(prereg["task"]["order_gap_ticks"]))
    actual = [(tick, channel if arm == "intact" else "A") for tick, channel in logical]
    first: dict[str, int | None] = {"A": None, "B": None}
    output_sequence: list[dict[str, Any]] = []
    spikes = events = 0
    for tick in range(int(prereg["task"]["evaluation_ticks"])):
        currents: dict[int, float] = {}
        for event_tick, channel in actual:
            if event_tick == tick:
                nid = ids[f"input_{channel}"]
                currents[nid] = currents.get(nid, 0.0) + current
        if currents:
            net.inject_current_batch(currents)
        result = net.step()
        spikes += int(result.spikes_this_tick)
        events += int(result.delivered_events)
        spiked = set(map(int, result.spike_ids))
        for channel in ("A", "B"):
            if ids[f"output_{channel}"] in spiked:
                output_sequence.append({"tick": tick, "channel": channel})
                if first[channel] is None:
                    first[channel] = tick
    decoded = decode(first)
    return {
        "seed": seed,
        "arm": arm,
        "order": order,
        "node_count": net.neuron_count,
        "edge_count": net.synapse_count,
        "synaptic_weight": weight,
        "stimulus_current": current,
        "logical_schedule": logical,
        "actual_schedule": actual,
        "total_injected_charge": 2.0 * current,
        "first_output_tick": first,
        "decoded_order": decoded,
        "task_success": decoded == order,
        "output_sequence": output_sequence,
        "total_spikes": spikes,
        "delivered_events": events,
        "state_digest_before": before,
        "state_digest_after": canonical_state_digest(net),
    }


def analyze(runs: list[dict[str, Any]], prereg: dict[str, Any]) -> dict[str, Any]:
    seeds = list(map(int, prereg["evaluation"]["seeds"]))
    lookup = {(r["seed"], r["arm"], r["order"]): r for r in runs}
    rows = []
    for seed in seeds:
        intact = statistics.fmean(
            float(lookup[(seed, "intact", o)]["task_success"]) for o in ORDER_TRIALS
        )
        destroyed = statistics.fmean(
            float(lookup[(seed, "identity_destroyed", o)]["task_success"])
            for o in ORDER_TRIALS
        )
        rows.append(
            {
                "seed": seed,
                "intact_order_accuracy": intact,
                "identity_destroyed_order_accuracy": destroyed,
                "paired_accuracy_delta": intact - destroyed,
                "intact_simultaneous_success": bool(
                    lookup[(seed, "intact", "simultaneous")]["task_success"]
                ),
            }
        )
    deltas = [float(r["paired_accuracy_delta"]) for r in rows]
    intact = [float(r["intact_order_accuracy"]) for r in rows]
    destroyed = [float(r["identity_destroyed_order_accuracy"]) for r in rows]
    summary = {
        "intact_order_accuracy_median": float(statistics.median(intact)),
        "identity_destroyed_order_accuracy_median": float(statistics.median(destroyed)),
        "intact_simultaneous_success_fraction": statistics.fmean(
            float(r["intact_simultaneous_success"]) for r in rows
        ),
        "paired_accuracy_delta_median": float(statistics.median(deltas)),
        "paired_accuracy_delta_bootstrap_ci95": bootstrap_ci(deltas),
        "paired_sign_test_p": sign_test_p(deltas),
    }
    rule = prereg["decision_rule"]
    gates = {
        "intact_order_accuracy": summary["intact_order_accuracy_median"]
        >= float(rule["minimum_intact_order_accuracy"]),
        "identity_destroyed_ceiling": summary[
            "identity_destroyed_order_accuracy_median"
        ]
        <= float(rule["maximum_identity_destroyed_order_accuracy"]),
        "simultaneous_control": summary["intact_simultaneous_success_fraction"]
        >= float(rule["minimum_intact_simultaneous_success_fraction"]),
        "paired_delta": summary["paired_accuracy_delta_median"]
        >= float(rule["minimum_paired_accuracy_delta"]),
        "paired_sign_test": summary["paired_sign_test_p"]
        < float(prereg["analysis"]["alpha"]),
        "bootstrap_ci_excludes_zero": summary["paired_accuracy_delta_bootstrap_ci95"][0]
        > 0.0,
    }
    return {
        "per_seed": rows,
        "summary": summary,
        "gates": gates,
        "status": (
            "SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL"
            if all(gates.values())
            else "NO_PREDEFINED_SUPPORT_DETECTED"
        ),
    }


def main() -> int:
    prereg = read_json(PREREG)
    if (
        prereg["protocol"] != "stage1_two_channel_temporal_order_v2"
        or prereg["execution_authorized"] is not True
    ):
        raise RuntimeError("invalid or unauthorized preregistration")
    if OUT.exists():
        raise RuntimeError("experiment output already exists")
    source = {
        "commit": git("rev-parse", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "dirty_before_execution": bool(git("status", "--porcelain")),
    }
    if source["dirty_before_execution"]:
        raise RuntimeError("source tree must be clean before execution")
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    runs = [
        simulate(config, prereg, int(seed), arm, order)
        for seed in prereg["evaluation"]["seeds"]
        for arm in ARMS
        for order in ORDERS
    ]
    seeds = list(map(int, prereg["evaluation"]["seeds"]))
    integrity_checks = {
        "run_count": len(runs) == len(seeds) * 6,
        "coverage": all(
            sum(r["seed"] == s and r["arm"] == a and r["order"] == o for r in runs) == 1
            for s in seeds
            for a in ARMS
            for o in ORDERS
        ),
        "network_budget": all(
            r["node_count"] == 6 and r["edge_count"] == 4 for r in runs
        ),
        "paired_parameters": all(
            len(
                {
                    (
                        round(r["synaptic_weight"], 12),
                        round(r["stimulus_current"], 12),
                        round(r["total_injected_charge"], 12),
                    )
                    for r in runs
                    if r["seed"] == s
                }
            )
            == 1
            for s in seeds
        ),
        "fresh_seeds": set(seeds).isdisjoint(range(101, 121))
        and set(seeds).isdisjoint(range(2101, 2121))
        and set(seeds).isdisjoint(range(6201, 6221)),
    }
    integrity = {"checks": integrity_checks, "pass": all(integrity_checks.values())}
    analysis = analyze(runs, prereg)
    if not integrity["pass"]:
        analysis["status"] = "NOT_TESTED_INTEGRITY_FAILURE"
    data = OUT / "data/evaluation.json"
    stats = OUT / "analysis/statistics.json"
    write_json(data, runs)
    write_json(
        stats,
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "analysis": analysis,
            "integrity": integrity,
            "claim_boundary": prereg["claim_boundary"],
        },
    )
    manifest = {
        "schema_version": 1,
        "experiment_id": EXP_ID,
        "stage": 1,
        "research_question": "RQ-TEMP-002",
        "hypothesis": "H-TEMP-002-A",
        "protocol": prereg["protocol"],
        "experiment_status": "completed" if integrity["pass"] else "not_tested",
        "result_status": analysis["status"],
        "scientific_evidence": False,
        "automatic_evidence_promotion": False,
        "human_review_status": "PENDING",
        "independent_replication": False,
        "source_freeze": source,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "os_name": os.name,
        },
        "design": {
            "seed_count": len(seeds),
            "run_count": len(runs),
            "arms": list(ARMS),
            "orders": list(ORDERS),
            "node_count": 6,
            "edge_count": 4,
        },
        "results": analysis["summary"],
        "integrity": integrity,
        "artifacts_sha256": {
            "preregistration": sha256(PREREG),
            "historical_v1_preregistration": sha256(HISTORICAL),
            "config": sha256(CONFIG),
            "runner_source": sha256(Path(__file__).resolve()),
            "evaluation_data": sha256(data),
            "statistics": sha256(stats),
        },
        "claim_boundary": prereg["claim_boundary"],
    }
    write_json(OUT / "manifest.json", manifest)
    write_json(
        OUT / "review_request.json",
        {
            "schema_version": 1,
            "experiment_id": EXP_ID,
            "reviewer_type_required": "human",
            "human_review_status": "PENDING",
            "scientific_evidence": False,
            "automatic_evidence_promotion": False,
            "independent_replication": False,
            "ai_review_does_not_satisfy_human_gate": True,
            "questions": [
                "Does V2 genuinely distinguish forward, reverse and simultaneous order without the V1 schedule-collapse defect?",
                "Is the identity-destroyed control sufficiently matched to isolate channel identity?",
                "Are the paired nuisance realizations and inferential test appropriate for the scoped Stage-1 claim?",
                "Does interpretation remain inside the registered claim boundary?",
            ],
        },
    )
    s = analysis["summary"]
    ci = s["paired_accuracy_delta_bootstrap_ci95"]
    report = f"""# {EXP_ID}: two-channel temporal-order task

Stage 1 - Kleines SNN

Research question: RQ-TEMP-002  
Hypothesis: H-TEMP-002-A  
Source freeze: {source["commit"]}  
Clean before execution: true  
Data role: DATA only; no automatic EVID promotion.

## Protocol correction

The historical V1 runner represented forward as (0,4) and reverse as (4,0), but executed both with membership testing. Both therefore collapsed to the same stimulation ticks. V2 preserves historical bytes and uses two distinguishable input channels plus an information-destroyed matched control.

## Result

**Status: {analysis["status"]}**

| endpoint | result |
| --- | ---: |
| intact order accuracy, median | {s["intact_order_accuracy_median"]:.4f} |
| identity-destroyed order accuracy, median | {s["identity_destroyed_order_accuracy_median"]:.4f} |
| intact simultaneous success fraction | {s["intact_simultaneous_success_fraction"]:.4f} |
| paired accuracy delta, median | {s["paired_accuracy_delta_median"]:.4f} |
| paired delta CI95 | [{ci[0]:.4f}, {ci[1]:.4f}] |
| exact paired sign-test p | {s["paired_sign_test_p"]:.8g} |

Design integrity: {"PASS" if integrity["pass"] else "FAIL"}

## Claim boundary

{prereg["claim_boundary"]}

## Governance

Human review remains required before EVID promotion. AI review does not satisfy that gate. This run is not an independent replication.
"""
    (OUT / "report.md").write_text(report, encoding="utf-8")
    checks = {
        "analysis/statistics.json": sha256(stats),
        "data/evaluation.json": sha256(data),
        "manifest.json": sha256(OUT / "manifest.json"),
        "report.md": sha256(OUT / "report.md"),
        "review_request.json": sha256(OUT / "review_request.json"),
    }
    (OUT / "checksums.sha256").write_text(
        "".join(f"{d}  {p}\n" for p, d in sorted(checks.items())), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "experiment_id": EXP_ID,
                "status": analysis["status"],
                "integrity": integrity["pass"],
                "runs": len(runs),
                **s,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
