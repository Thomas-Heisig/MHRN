#!/usr/bin/env python3
"""Pre-freeze one-neuron parity calibration between MHRN and Brian2 reference."""

from __future__ import annotations

import json
import math
from pathlib import Path

from reference.stage1_topology_brian2.integrator_probe import run_one_tick
from src.core.neuron import NeuronConfig, create_neuron

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "calibrations" / "CAL-S1-TOPO-REFERENCE-INTEGRATOR-R1"


def run_mhrn_one_tick(current: float) -> dict[str, float | bool]:
    config = NeuronConfig(
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
    neuron = create_neuron(1, config=config)
    spiked = neuron.step(float(current), 0)
    return {
        "v": neuron.v,
        "u": neuron.u,
        "threshold_adaptation": neuron.threshold_adaptation,
        "firing_rate_estimate": neuron.firing_rate_estimate,
        "spiked": spiked,
    }


def main() -> int:
    tolerance = 1e-12
    cases = []
    passed = True
    for current in (0.0, 100.0):
        mhrn = run_mhrn_one_tick(current)
        reference = run_one_tick(current).to_dict()
        diffs: dict[str, float] = {}
        case_pass = bool(mhrn["spiked"] == reference["spiked"])
        for key in ("v", "u", "threshold_adaptation", "firing_rate_estimate"):
            diff = abs(float(mhrn[key]) - float(reference[key]))
            diffs[key] = diff
            case_pass = case_pass and math.isclose(
                float(mhrn[key]), float(reference[key]), rel_tol=0.0, abs_tol=tolerance
            )
        passed = passed and case_pass
        cases.append(
            {
                "input_current": current,
                "mhrn": mhrn,
                "brian2_reference": reference,
                "absolute_differences": diffs,
                "pass": case_pass,
            }
        )
    payload = {
        "schema_version": 1,
        "calibration_id": "CAL-S1-TOPO-REFERENCE-INTEGRATOR-R1",
        "role": "pre-freeze method calibration; not confirmatory DATA and not EVID",
        "tolerance_abs": tolerance,
        "cases": cases,
        "pass": passed,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "result.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS" if passed else "FAIL", "cases": cases}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
