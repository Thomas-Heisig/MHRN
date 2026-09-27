# Stage-1 topology reference pre-freeze mechanism audit

**Date:** 2026-09-27  
**Target:** `PREREG-S1-TOPO-REFERENCE-R1`  
**Status:** pre-freeze audit; reference execution remains unauthorized

## Canonical source path

The canonical Stage-1 topology runner loads `configs/learning_experiment.yaml`, replaces only dimensions/initial-neuron/max-delay fields, and then constructs `NeuralNetwork(values, random.Random(seed))`. It does not replace the neuron secondary-mechanism defaults.

The effective neuron configuration therefore combines the YAML Izhikevich parameters with the default values in `src/core/neuron.py::NeuronConfig`.

## Effective membrane model

| parameter | effective value |
| --- | ---: |
| model | izhikevich-2003 |
| dt_ms | 1.0 |
| a | 0.02 |
| b | 0.2 |
| c | -65.0 |
| d | 8.0 |
| initial_v | -65.0 |
| initial_u | -13.0 |
| spike threshold | 30.0 |

The integration rule is the canonical MHRN two-half-Euler update for `v`, followed by one Euler update for `u`. Spike detection occurs after integration; reset is `v=c; u=u+d`.

## Secondary mechanisms

### Threshold adaptation — ACTIVE AND TIMING-RELEVANT

Defaults:
- `enable_threshold_adaptation = true`
- rate = `0.01` per spike
- decay = `0.999` per tick

The current threshold is `30 + threshold_adaptation`. A spike increments adaptation before end-of-tick decay. This can affect later spike timing and **must be translated into the reference implementation**.

### Homeostasis — ACTIVE AND TIMING-RELEVANT

Defaults:
- `enable_homeostasis = true`
- target rate = `10 Hz`
- firing-rate tau = `1000 ms`
- homeostasis learning rate = `0.001`

Every tick updates the low-pass firing-rate estimate, then modifies `threshold_adaptation` by `0.001 * (firing_rate_estimate - 10)`, clamped to [-10, 10], before the final adaptation decay of the next applicable update order defined by the canonical neuron step. Because the modified adaptation enters the future spike threshold, this mechanism **must be translated**.

### Energy — ACTIVE STATE, NOT FIRING-COUPLED IN THIS RUN

Defaults/YAML:
- initial energy = 1.0
- spike cost = 0.001
- recovery = 0.0001 per tick
- YAML declares `energy.affects_firing: false`

The neuron implementation deducts/replenishes energy but does not use energy in membrane integration, threshold calculation, refractory state, or spike gating. Energy is therefore provenance-bearing state but is observationally inert for the registered propagation endpoints. The reference implementation may omit energy from its causal dynamics, but the omission must be recorded explicitly.

### Traces — ACTIVE STATE, INERT FOR PROPAGATION DYNAMICS

Defaults:
- traces enabled
- decay = 0.95
- increment = 1.0 on a spike

The Stage-1 topology run has no STDP/plasticity update consuming the traces. Trace state does not enter membrane integration or threshold. It is therefore inert for registered propagation endpoints and may be omitted from the causal reference dynamics with an explicit provenance note.

### Refractory mechanism — CONFIGURED AS ZERO

`refractory_ticks = 0`; no refractory suppression is applied.

## Reference translation consequence

A valid cross-implementation runner must therefore reproduce:
1. two-half-Euler Izhikevich membrane integration;
2. spike threshold/reset;
3. threshold-adaptation increment/decay;
4. low-pass firing-rate update;
5. homeostatic threshold-adaptation update/clamp;
6. one-tick synaptic event semantics.

Energy and traces may be omitted from causal simulation only because the source audit shows they do not feed back into the registered spike dynamics.

## Freeze gate

Reference freeze is prohibited until:
- a one-neuron one-tick integrator-parity test passes at machine precision for several preregistered subthreshold inputs;
- a multi-tick parity test including at least one spike passes for `v`, `u`, spike decision, threshold-adaptation and firing-rate estimate under the frozen reference translation;
- the reference package contains no MHRN runtime imports;
- the audit findings are bound into the frozen preregistration.

A failure of either parity test requires a translation correction **before** freeze. It may not be waived as a harmless framework difference.
