#!/usr/bin/env python3
"""Independent Brian2 Stage-1 topology reference runner.

The runner consumes only the sanitized reference_protocol.json and does not
load project evidence, historical experiment statistics, or comparison targets.
Evaluation additionally requires an explicit environment authorization token.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import platform
import random
import sys
from pathlib import Path
from typing import Any

import brian2 as b2

HERE = Path(__file__).resolve().parent
PROTOCOL_PATH = HERE / "reference_protocol.json"
AUTH_ENV = "MHRN_STAGE1_REFERENCE_EXECUTION"
AUTH_VALUE = "AUTHORIZED_REFERENCE_R1"


def _digest(value: object) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_protocol() -> dict[str, Any]:
    value = json.loads(PROTOCOL_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("reference protocol must be a JSON object")
    if value.get("framework") != "Brian2":
        raise RuntimeError("unexpected reference framework")
    if str(value.get("framework_version")) != str(b2.__version__):
        raise RuntimeError(
            f"Brian2 version mismatch: protocol={value.get('framework_version')} "
            f"runtime={b2.__version__}"
        )
    return value


def _all_coords(shape: tuple[int, int, int, int, int]) -> list[tuple[int, ...]]:
    coords = list(itertools.product(*(range(size) for size in shape)))
    if len(coords) != 64:
        raise ValueError(f"shape must materialize 64 positions: {shape}")
    return [tuple(int(v) for v in coord) for coord in coords]


def _coordinate_score(coord: tuple[int, ...], shape: tuple[int, ...]) -> float:
    return sum(
        float(value) / float(max(size - 1, 1))
        for value, size in zip(coord, shape, strict=True)
    )


def _canonical_coords(shape: tuple[int, int, int, int, int]) -> list[tuple[int, ...]]:
    return sorted(_all_coords(shape), key=lambda c: (_coordinate_score(c, shape), c))


def _distance(
    left: tuple[int, ...], right: tuple[int, ...], shape: tuple[int, ...]
) -> float:
    return math.sqrt(
        sum(
            (float(a - b) / float(max(size - 1, 1))) ** 2
            for a, b, size in zip(left, right, shape, strict=True)
        )
    )


def _tie_key(seed: int, source: int, target: int) -> str:
    return hashlib.sha256(f"{seed}:{source}:{target}".encode()).hexdigest()


def _graph(
    condition: str,
    shape: tuple[int, int, int, int, int],
    seed: int,
    out_degree_cap: int,
) -> tuple[list[tuple[int, ...]], list[tuple[int, int]]]:
    coords = _canonical_coords(shape)
    if condition == "5d_shuffled":
        random.Random(seed ^ 0x5D5D5D).shuffle(coords)

    rng = random.Random(seed ^ 0x51A6E1)
    edges: list[tuple[int, int]] = []
    for source in range(len(coords) - 1):
        future = list(range(source + 1, len(coords)))
        degree = min(out_degree_cap, len(future))
        if condition == "random_graph":
            targets = sorted(rng.sample(future, degree))
        else:
            targets = sorted(
                future,
                key=lambda target: (
                    _distance(coords[source], coords[target], shape),
                    _tie_key(seed, source, target),
                    target,
                ),
            )[:degree]
        edges.extend((source, target) for target in targets)
    return coords, edges


def _population(count: int) -> tuple[b2.NeuronGroup, b2.Network]:
    b2.start_scope()
    b2.prefs.codegen.target = "numpy"
    b2.defaultclock.dt = 1 * b2.ms

    group = b2.NeuronGroup(
        count,
        model="""
        v : 1
        u : 1
        input_current : 1
        threshold_adaptation : 1
        firing_rate_estimate : 1
        spike_seen : integer
        """,
        threshold="v >= 30 + threshold_adaptation",
        reset="""
        v = -65
        u = u + 8
        threshold_adaptation = threshold_adaptation + 0.01
        spike_seen = 1
        """,
        dt=1 * b2.ms,
        name="reference_population",
    )
    group.v = -65.0
    group.u = -13.0
    group.input_current = 0.0
    group.threshold_adaptation = 0.0
    group.firing_rate_estimate = 0.0
    group.spike_seen = 0

    group.run_regularly(
        "spike_seen = 0",
        dt=1 * b2.ms,
        when="start",
        order=-10,
        name="reset_spike_flag",
    )
    group.run_regularly(
        """
        v = v + 0.5 * (0.04*v*v + 5*v + 140 - u + input_current)
        v = v + 0.5 * (0.04*v*v + 5*v + 140 - u + input_current)
        u = u + 0.02 * (0.2*v - u)
        """,
        dt=1 * b2.ms,
        when="groups",
        order=-1,
        name="two_half_euler",
    )
    group.run_regularly(
        """
        firing_rate_estimate = exp(-0.001)*firing_rate_estimate + spike_seen*(1-exp(-0.001))*1000
        threshold_adaptation = threshold_adaptation * 0.999
        threshold_adaptation = clip(threshold_adaptation + 0.001*(firing_rate_estimate - 10), -10, 10)
        """,
        dt=1 * b2.ms,
        when="after_resets",
        order=1,
        name="post_tick_adaptation",
    )
    return group, b2.Network(group, *group.contained_objects)


def _run_one(protocol: dict[str, Any], condition: str, seed: int) -> dict[str, Any]:
    shape_raw = protocol["conditions"][condition]
    shape = tuple(int(v) for v in shape_raw)
    if len(shape) != 5:
        raise ValueError(condition)

    network_cfg = protocol["network"]
    coords, edges = _graph(
        condition,
        shape,  # type: ignore[arg-type]
        int(seed),
        int(network_cfg["out_degree_cap"]),
    )
    if len(edges) != int(network_cfg["edge_count"]):
        raise RuntimeError(f"edge budget mismatch for {condition}: {len(edges)}")

    outgoing: dict[int, list[int]] = {index: [] for index in range(64)}
    for source, target in edges:
        outgoing[source].append(target)

    group, network = _population(64)
    input_labels = {int(v) for v in network_cfg["input_labels"]}
    output_labels = {int(v) for v in network_cfg["output_labels"]}
    weight = float(network_cfg["synaptic_weight"])
    delay = int(network_cfg["delay_ticks"])
    ticks = int(network_cfg["evaluation_ticks"])
    stimulus_ticks = int(network_cfg["stimulus_ticks"])
    stimulus_current = float(network_cfg["stimulus_current"])
    auc_window = int(network_cfg["auc_window_ticks"])

    queue: dict[int, list[tuple[int, float]]] = {}
    active: set[int] = set()
    first_output: int | None = None
    total_spikes = 0
    total_delivered = 0
    spike_times: dict[str, list[int]] = {str(i): [] for i in range(64)}
    delivered_per_tick: list[int] = []
    cumulative_active_per_tick: list[int] = []

    for tick in range(ticks):
        current = [0.0] * 64
        if tick < stimulus_ticks:
            for label in input_labels:
                current[label] += stimulus_current

        due = queue.pop(tick, [])
        for target, event_weight in due:
            current[target] += event_weight
        delivered_per_tick.append(len(due))
        total_delivered += len(due)

        group.input_current = current
        network.run(1 * b2.ms)
        spikes = [index for index in range(64) if int(group.spike_seen[index]) != 0]

        for source in spikes:
            spike_times[str(source)].append(tick)
            active.add(source)
            if source in output_labels and first_output is None:
                first_output = tick
            for target in outgoing[source]:
                queue.setdefault(tick + delay, []).append((target, weight))
        total_spikes += len(spikes)
        cumulative_active_per_tick.append(len(active))

    active_fraction_series = [count / 64.0 for count in cumulative_active_per_tick]
    auc = float(sum(active_fraction_series[:auc_window]))
    latency = first_output if first_output is not None else ticks + 1

    return {
        "condition": condition,
        "seed": int(seed),
        "node_count": 64,
        "edge_count": len(edges),
        "coordinate_digest": _digest(coords),
        "edge_digest": _digest(edges),
        "first_output_latency_censored": int(latency),
        "activation_auc_0_32": auc,
        "total_spikes": int(total_spikes),
        "delivered_events": int(total_delivered),
        "final_active_fraction": len(active) / 64.0,
        "spike_times_by_label": spike_times,
        "delivered_events_per_tick": delivered_per_tick,
        "cumulative_active_neurons_per_tick": cumulative_active_per_tick,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if os.environ.get(AUTH_ENV) != AUTH_VALUE:
        raise RuntimeError(
            f"reference evaluation is not authorized; set {AUTH_ENV} only from "
            "the separately approved execution workflow"
        )

    protocol = _load_protocol()
    output = Path(args.output)
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")

    conditions = list(protocol["conditions"])
    seeds = [int(v) for v in protocol["seeds"]]
    runs = [
        _run_one(protocol, condition, seed)
        for seed in seeds
        for condition in conditions
    ]

    payload = {
        "schema_version": 1,
        "protocol_id": protocol["protocol_id"],
        "framework": "Brian2",
        "framework_version": b2.__version__,
        "python_version": sys.version,
        "platform": platform.platform(),
        "protocol_sha256": _file_digest(PROTOCOL_PATH),
        "runner_sha256": _file_digest(Path(__file__)),
        "conditions": conditions,
        "seeds": seeds,
        "run_count": len(runs),
        "runs": runs,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "REFERENCE_DATA_WRITTEN",
                "run_count": len(runs),
                "output": str(output),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
