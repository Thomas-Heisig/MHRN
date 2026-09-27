#!/usr/bin/env python3
"""Pre-freeze one-neuron parity calibration between MHRN and Brian2 reference."""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import brian2

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reference.stage1_topology_brian2.integrator_probe import (
    run_one_tick,
    run_trajectory,
)
from src.core.neuron import NeuronConfig, create_neuron

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "calibrations" / "CAL-S1-TOPO-REFERENCE-INTEGRATOR-R1"
REFERENCE_PROBE = ROOT / "reference" / "stage1_topology_brian2" / "integrator_probe.py"
NEURON_SOURCE = ROOT / "src" / "core" / "neuron.py"
MODEL_SOURCE = ROOT / "src" / "core" / "neuron_models.py"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def run_mhrn_trajectory(currents: list[float]) -> list[dict[str, float | bool]]:
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
    trajectory_currents = [100.0, 0.0, 0.0, 100.0, 0.0, 0.0, 0.0, 0.0]
    mhrn_trajectory = run_mhrn_trajectory(trajectory_currents)
    brian2_trajectory = [row.to_dict() for row in run_trajectory(trajectory_currents)]
    trajectory_cases = []
    trajectory_pass = True
    for tick, (mhrn, reference) in enumerate(
        zip(mhrn_trajectory, brian2_trajectory, strict=True)
    ):
        diffs: dict[str, float] = {}
        tick_pass = bool(mhrn["spiked"] == reference["spiked"])
        for key in ("v", "u", "threshold_adaptation", "firing_rate_estimate"):
            diff = abs(float(mhrn[key]) - float(reference[key]))
            diffs[key] = diff
            tick_pass = tick_pass and math.isclose(
                float(mhrn[key]),
                float(reference[key]),
                rel_tol=0.0,
                abs_tol=tolerance,
            )
        trajectory_pass = trajectory_pass and tick_pass
        trajectory_cases.append(
            {
                "tick": tick,
                "input_current": trajectory_currents[tick],
                "mhrn": mhrn,
                "brian2_reference": reference,
                "absolute_differences": diffs,
                "pass": tick_pass,
            }
        )
    if not any(bool(row["mhrn"]["spiked"]) for row in trajectory_cases):
        trajectory_pass = False
    passed = passed and trajectory_pass

    payload = {
        "schema_version": 1,
        "calibration_id": "CAL-S1-TOPO-REFERENCE-INTEGRATOR-R1",
        "role": "pre-freeze method calibration; not confirmatory DATA and not EVID",
        "tolerance_abs": tolerance,
        "single_tick_cases": cases,
        "multi_tick": {
            "input_currents": trajectory_currents,
            "cases": trajectory_cases,
            "contains_spike": any(
                bool(row["mhrn"]["spiked"]) for row in trajectory_cases
            ),
            "pass": trajectory_pass,
        },
        "provenance": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "brian2_version": brian2.__version__,
            "reference_probe_sha256": sha256_file(REFERENCE_PROBE),
            "mhrn_neuron_source_sha256": sha256_file(NEURON_SOURCE),
            "mhrn_neuron_model_source_sha256": sha256_file(MODEL_SOURCE),
        },
        "cases": cases,
        "pass": passed,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "result.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "PASS" if passed else "FAIL", "cases": cases}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
