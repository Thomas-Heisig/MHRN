#!/usr/bin/env python3
"""Code-backed audit of mechanisms affecting the canonical Stage-1 topology runner."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs" / "learning_experiment.yaml"
NEURON = ROOT / "src" / "core" / "neuron.py"
MODELS = ROOT / "src" / "core" / "neuron_models.py"
NETWORK = ROOT / "src" / "core" / "network.py"
RUNNER = ROOT / "scripts" / "run_stage1_topology_v2.py"
OUT = ROOT / "research" / "audits" / "STAGE1_TOPOLOGY_REFERENCE_MECHANISM_AUDIT_20260927.json"


def main() -> int:
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    neuron_text = NEURON.read_text(encoding="utf-8")
    model_text = MODELS.read_text(encoding="utf-8")
    network_text = NETWORK.read_text(encoding="utf-8")
    runner_text = RUNNER.read_text(encoding="utf-8")

    checks = {
        "runner_uses_normal_neural_network_config": (
            "network = NeuralNetwork(values, random.Random(seed))" in runner_text
            and "isolated_reference" not in runner_text
        ),
        "two_half_euler_present": (
            "half_dt = 0.5 * dt_ms" in model_text
            and model_text.count("v += half_dt") >= 2
        ),
        "threshold_adaptation_enabled_by_default": (
            "enable_threshold_adaptation: bool = True" in neuron_text
        ),
        "homeostasis_enabled_by_default": (
            "enable_homeostasis: bool = True" in neuron_text
        ),
        "threshold_reads_adaptation": (
            "base + self.threshold_adaptation" in neuron_text
        ),
        "homeostasis_changes_threshold": (
            "self.threshold_adaptation += self.config.homeostasis_learning_rate * error"
            in neuron_text
        ),
        "energy_not_read_by_membrane_integrator": (
            "energy" not in model_text.split("def integrate_membrane", 1)[1].split(
                "def spike_threshold", 1
            )[0]
        ),
        "network_step_does_not_apply_stdp": all(
            token not in network_text.split("def step(self)", 1)[1].split(
                "def step_batch", 1
            )[0]
            for token in ("compute_stdp_update", "apply_stdp_update", "update_eligibility")
        ),
        "config_energy_affects_firing_false": (
            config.get("energy", {}).get("affects_firing") is False
        ),
        "config_stdp_enabled_false": (
            config.get("stdp", {}).get("enabled") is False
        ),
    }

    payload = {
        "schema_version": 1,
        "audit_id": "STAGE1-TOPOLOGY-REFERENCE-MECHANISM-AUDIT-20260927",
        "source_files": [
            str(path.relative_to(ROOT))
            for path in (CONFIG, NEURON, MODELS, NETWORK, RUNNER)
        ],
        "checks": checks,
        "pass": all(checks.values()),
        "classification": {
            "threshold_adaptation": "ACTIVE_AND_SPIKE_TIMING_RELEVANT",
            "homeostasis": "ACTIVE_AND_SPIKE_TIMING_RELEVANT",
            "energy": "STATE_UPDATED_BUT_SPIKE_TIMING_INERT_IN_CANONICAL_CORE",
            "traces": "STATE_UPDATED_BUT_SPIKE_TIMING_INERT_IN_CANONICAL_CORE",
            "synaptic_plasticity": "NOT_APPLIED_BY_CANONICAL_NETWORK_STEP",
            "refractory": "INACTIVE_DEFAULT_ZERO_TICKS",
        },
        "reference_translation_required": [
            "two-half-Euler v update",
            "u Euler update after the second v half-step",
            "adaptive threshold increment on spike",
            "threshold-adaptation decay",
            "firing-rate low-pass update",
            "homeostatic threshold update and clamp",
            "fixed-weight one-tick synaptic event delivery",
        ],
        "omittable_with_audit": [
            "energy state",
            "pre/post traces",
            "STDP/reward eligibility",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS" if payload["pass"] else "FAIL", "checks": checks}))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
