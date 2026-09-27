#!/usr/bin/env python3
"""Explicit reset/post-spike parity calibration for Stage-1 Brian2 reference."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import brian2

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reference.stage1_topology_brian2.integrator_probe import run_trajectory
from src.core.neuron import NeuronConfig, create_neuron

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "calibrations" / "CAL-S1-TOPO-REFERENCE-RESET-R1"
PROBE = ROOT / "reference" / "stage1_topology_brian2" / "integrator_probe.py"
NEURON = ROOT / "src" / "core" / "neuron.py"
MODELS = ROOT / "src" / "core" / "neuron_models.py"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def config() -> NeuronConfig:
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


def mhrn_trajectory(currents: list[float]) -> list[dict[str, float | bool]]:
    neuron = create_neuron(1, config=config())
    rows: list[dict[str, float | bool]] = []
    for tick, current in enumerate(currents):
        spiked = neuron.step(float(current), tick)
        rows.append(
            {
                "v": neuron.v,
                "u": neuron.u,
                "threshold_adaptation": neuron.threshold_adaptation,
                "firing_rate_estimate": neuron.firing_rate_estimate,
                "spiked": spiked,
            }
        )
    return rows


def main() -> int:
    tolerance = 1e-12
    currents = [100.0, 0.0]
    mhrn = mhrn_trajectory(currents)
    reference = [row.to_dict() for row in run_trajectory(currents)]

    checks: list[dict[str, object]] = []
    passed = True
    for tick, (left, right) in enumerate(zip(mhrn, reference, strict=True)):
        diffs: dict[str, float] = {}
        tick_pass = bool(left["spiked"] == right["spiked"])
        for key in ("v", "u", "threshold_adaptation", "firing_rate_estimate"):
            diff = abs(float(left[key]) - float(right[key]))
            diffs[key] = diff
            tick_pass = tick_pass and math.isclose(
                float(left[key]), float(right[key]), rel_tol=0.0, abs_tol=tolerance
            )
        passed = passed and tick_pass
        checks.append(
            {
                "tick": tick,
                "input_current": currents[tick],
                "mhrn": left,
                "brian2_reference": right,
                "absolute_differences": diffs,
                "pass": tick_pass,
            }
        )

    reset_semantics = {
        "spike_on_tick_0": bool(mhrn[0]["spiked"] and reference[0]["spiked"]),
        "reset_v_equals_c": bool(
            math.isclose(float(mhrn[0]["v"]), -65.0, abs_tol=tolerance)
            and math.isclose(float(reference[0]["v"]), -65.0, abs_tol=tolerance)
        ),
        "u_incremented_by_d_in_matching_state": bool(
            math.isclose(
                float(mhrn[0]["u"]), float(reference[0]["u"]), abs_tol=tolerance
            )
        ),
        "next_tick_state_matches": bool(checks[1]["pass"]),
    }
    passed = passed and all(reset_semantics.values())

    payload = {
        "schema_version": 1,
        "calibration_id": "CAL-S1-TOPO-REFERENCE-RESET-R1",
        "role": "pre-freeze method calibration; not confirmatory DATA and not EVID",
        "tolerance_abs": tolerance,
        "currents": currents,
        "cases": checks,
        "reset_semantics": reset_semantics,
        "provenance": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "brian2_version": brian2.__version__,
            "reference_probe_sha256": sha256_file(PROBE),
            "mhrn_neuron_source_sha256": sha256_file(NEURON),
            "mhrn_neuron_model_source_sha256": sha256_file(MODELS),
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
