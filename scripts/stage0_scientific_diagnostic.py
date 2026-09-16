"""Bounded Stage-0 scientific-readiness diagnostic.

This script is deliberately diagnostic/exploratory. It does not promote DATA to EVID
and it does not change dashboard scores. It characterizes the current firing-rate,
homeostasis and Brian2 comparison paths so a confirmatory validation can be frozen
without post-hoc parameter selection.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.core.compartment_neuron import CompartmentNeuronConfig
from src.core.hh_neuron import HodgkinHuxleyConfig
from src.core.neuron import NeuronConfig, NeuronModel, available_neuron_models, create_neuron
from src.research.empirical_evaluation import run_brian2_conformance

OUT = Path("stage0-science-diagnostic.json")


def _homeostasis_probe(current: float, *, enabled: bool, ticks: int = 30_000) -> dict[str, Any]:
    config = NeuronConfig(
        model=NeuronModel.LEAKY_INTEGRATE_AND_FIRE,
        dt_ms=1.0,
        target_rate_hz=10.0,
        firing_rate_tau_ms=1000.0,
        homeostasis_learning_rate=0.001,
        threshold_adaptation_rate=0.0,
        threshold_adaptation_decay=1.0,
        enable_threshold_adaptation=True,
        enable_homeostasis=enabled,
        enable_energy_dynamics=False,
        enable_traces=False,
    )
    neuron = create_neuron(1, config=config)
    burn_in = ticks // 2
    measured_spikes = 0
    for tick in range(ticks):
        spiked = neuron.step(current, tick)
        if tick >= burn_in and spiked:
            measured_spikes += 1
    measured_seconds = (ticks - burn_in) * config.dt_ms / 1000.0
    return {
        "input_current": current,
        "homeostasis_enabled": enabled,
        "ticks": ticks,
        "burn_in_ticks": burn_in,
        "measured_spikes": measured_spikes,
        "measured_rate_hz": measured_spikes / measured_seconds,
        "ema_rate_hz": neuron.firing_rate_estimate,
        "threshold_adaptation": neuron.threshold_adaptation,
        "threshold_saturated": abs(neuron.threshold_adaptation) >= 9.999999,
    }


def main() -> None:
    currents = (16.0, 18.0, 20.0, 22.0, 25.0, 30.0)
    homeostasis = [
        _homeostasis_probe(current, enabled=enabled)
        for current in currents
        for enabled in (False, True)
    ]
    brian_runs = run_brian2_conformance({}, seeds=(20001, 20002, 20003))
    brian2 = [
        {
            "seed": run.seed,
            "condition": run.condition,
            "max_abs_voltage_error": run.metrics["max_abs_voltage_error"],
            "max_abs_recovery_error": run.metrics["max_abs_recovery_error"],
            "spike_events_equal": run.metrics["spike_events_equal"],
            "conformance_within_1e_8": run.metrics["conformance_within_1e_8"],
            "brian2_version": run.metrics["brian2_version"],
            "native_first_spikes": run.metrics["native_spikes"][:12],
            "brian2_first_spikes": run.metrics["brian2_spikes"][:12],
        }
        for run in brian_runs
    ]
    canonical_models = [item.model.value for item in available_neuron_models()]
    payload = {
        "status": "diagnostic_only_not_evidence",
        "stage": 0,
        "stage_name": "Einzelne Nervenzelle",
        "homeostasis_sweep": homeostasis,
        "brian2_conformance": brian2,
        "model_scope": {
            "canonical_stage0_models": canonical_models,
            "hh_default_enabled": HodgkinHuxleyConfig().enabled,
            "compartment_default_enabled": CompartmentNeuronConfig().enabled,
            "hh_and_compartment_classification": "stage0_plus_experimental_not_canonical_switch_contract",
        },
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
