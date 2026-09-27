#!/usr/bin/env python3
"""Two-neuron fixed-delay parity calibration for Stage-1 Brian2 reference."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import sys
from pathlib import Path

import brian2

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reference.stage1_topology_brian2.synapse_probe import run_two_neuron_delay_probe
from src.core.network import Brain5DConfig, NeuralNetwork, SimulationConfig
from src.core.neuron import NeuronConfig
from src.core.synapse import SynapseConfig

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "calibrations" / "CAL-S1-TOPO-REFERENCE-SYNAPSE-R1"
PROBE = ROOT / "reference" / "stage1_topology_brian2" / "synapse_probe.py"
NETWORK = ROOT / "src" / "core" / "network.py"
NEURON = ROOT / "src" / "core" / "neuron.py"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def neuron_config() -> NeuronConfig:
    return NeuronConfig(
        model="izhikevich-2003",
        dt_ms=1.0,
        a=0.02,
        b=0.2,
        c=-65.0,
        d=8.0,
        initial_v=-65.0,
        initial_u=-13.0,
        izhikevich_threshold=30.0,
        refractory_ticks=0,
        threshold_adaptation_rate=0.01,
        threshold_adaptation_decay=0.999,
        target_rate_hz=10.0,
        firing_rate_tau_ms=1000.0,
        homeostasis_learning_rate=0.001,
        enable_threshold_adaptation=True,
        enable_energy_dynamics=True,
        enable_traces=True,
        enable_homeostasis=True,
    )


def run_mhrn() -> list[dict[str, object]]:
    cfg = Brain5DConfig(
        dimensions=(2, 1, 1, 1, 1),
        simulation=SimulationConfig(dt_ms=1.0, max_delay=1),
        neuron=neuron_config(),
        synapse=SynapseConfig(w_min=0.0, w_max=200.0),
    )
    net = NeuralNetwork(cfg, random.Random(1))
    source = net.add_neuron((0, 0, 0, 0, 0))
    target = net.add_neuron((1, 0, 0, 0, 0))
    net.connect(source, target, weight=55.0, delay=1)

    rows: list[dict[str, object]] = []
    for tick in range(3):
        if tick == 0:
            net.inject_current(source, 100.0)
        result = net.step()
        rows.append(
            {
                "tick": tick,
                "source_spiked": source in result.spike_ids,
                "target_spiked": target in result.spike_ids,
                "delivered_events": result.delivered_events,
                "target_v": net.neurons[target].v,
                "target_u": net.neurons[target].u,
                "target_threshold_adaptation": net.neurons[target].threshold_adaptation,
                "target_firing_rate_estimate": net.neurons[target].firing_rate_estimate,
            }
        )
    return rows


def main() -> int:
    tolerance = 1e-12
    mhrn = run_mhrn()
    reference = [row.to_dict() for row in run_two_neuron_delay_probe()]

    checks: list[dict[str, object]] = []
    passed = True
    for tick in range(3):
        left = mhrn[tick]
        right = reference[tick]
        target = right["target"]
        diffs = {
            "target_v": abs(float(left["target_v"]) - float(target["v"])),
            "target_u": abs(float(left["target_u"]) - float(target["u"])),
            "target_threshold_adaptation": abs(
                float(left["target_threshold_adaptation"])
                - float(target["threshold_adaptation"])
            ),
            "target_firing_rate_estimate": abs(
                float(left["target_firing_rate_estimate"])
                - float(target["firing_rate_estimate"])
            ),
        }
        tick_pass = (
            bool(left["source_spiked"]) == bool(right["source"]["spiked"])
            and bool(left["target_spiked"]) == bool(target["spiked"])
            and int(left["delivered_events"]) == int(right["delivered_events"])
            and all(
                math.isclose(value, 0.0, rel_tol=0.0, abs_tol=tolerance)
                for value in diffs.values()
            )
        )
        passed = passed and tick_pass
        checks.append(
            {
                "tick": tick,
                "mhrn": left,
                "brian2_reference": right,
                "absolute_differences": diffs,
                "pass": tick_pass,
            }
        )

    semantics = {
        "source_spikes_tick_0": bool(mhrn[0]["source_spiked"]),
        "no_delivery_tick_0": int(mhrn[0]["delivered_events"]) == 0,
        "one_delivery_tick_1": int(mhrn[1]["delivered_events"]) == 1,
        "reference_current_tick_1_is_55": math.isclose(
            float(reference[1]["target_synaptic_current"]),
            55.0,
            rel_tol=0.0,
            abs_tol=tolerance,
        ),
    }
    passed = passed and all(semantics.values())

    payload = {
        "schema_version": 1,
        "calibration_id": "CAL-S1-TOPO-REFERENCE-SYNAPSE-R1",
        "role": "pre-freeze method calibration; not confirmatory DATA and not EVID",
        "weight": 55.0,
        "delay_ticks": 1,
        "tolerance_abs": tolerance,
        "cases": checks,
        "event_semantics": semantics,
        "provenance": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "brian2_version": brian2.__version__,
            "reference_probe_sha256": sha256_file(PROBE),
            "mhrn_network_source_sha256": sha256_file(NETWORK),
            "mhrn_neuron_source_sha256": sha256_file(NEURON),
        },
        "pass": passed,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "result.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "PASS" if passed else "FAIL"}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
