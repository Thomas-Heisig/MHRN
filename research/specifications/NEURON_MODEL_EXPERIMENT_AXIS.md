# Neuron model as an experimental axis

**Status:** current research specification  
**Default:** `izhikevich-2003`  
**Optional validated alternative:** `lif-current-v1`

## Purpose

The selectable neuron model is a treatment axis, not an implementation detail. Izhikevich remains the canonical MHRN default. LIF may be enabled in experiments for which the scientific question remains meaningful under both membrane models.

## Eligibility rule

An experiment may activate the model axis when its outcome is not definitionally tied to one membrane model. Examples include propagation, topology, learning, memory, robustness, scaling and ablation experiments where membrane dynamics can be held as a declared treatment factor.

An experiment must not silently switch models. If `neuron.model` differs from the canonical default, the manifest/execution contract must record:

- `neuron.model`
- complete `NeuronConfig`
- model provenance/version
- `dt_ms`
- `refractory_ticks`
- whether the model comparison is primary, secondary or diagnostic
- the model-specific hypothesis ID when inferential comparison is intended

## Hypothesis rule

The existing primary hypothesis remains the primary hypothesis unless its preregistration explicitly says otherwise. A model comparison is represented by an additional hypothesis/contrast, not by rewriting the original hypothesis after data are observed.

For Stage-0 reference conformance the registered model-specific hypotheses are:

- `H-EVAL-006-A`: Izhikevich one-step transition/spike/reset conformance.
- `H-EVAL-006-B`: LIF default (`refractory_ticks=0`) trajectory/spike conformance.
- `H-EVAL-006-C`: optional nonzero-LIF-refractory semantic mapping.

## Reference semantics

### Izhikevich

The conformance contract compares one declared 1-ms transition at identical initial `(v, u, I)` state. It checks both sides of the threshold/reset boundary:

1. split-Euler membrane update,
2. threshold decision,
3. reset to `v=c`,
4. recovery update `u += d`.

Long free-running trajectories are a separate robustness question because sub-nanoscopic floating-point differences can be amplified by nonlinear state evolution. The historical V1 1000-tick negative is preserved.

### LIF

The reference uses forward Euler with identical `dt_ms`, resting potential, resistance, time constant, threshold and reset.

At `dt_ms=1.0`, diagnostic mapping for the optional refractory extension is:

| MHRN `refractory_ticks` | Brian2 refractory |
| ---: | ---: |
| 0 | 0 ms (canonical comparison) |
| 1 | 2 ms |
| 2 | 3 ms |
| 3 | 4 ms |

The nonzero mapping remains subject to the frozen confirmatory protocol `PREREG-RQ-EVAL-006-V2`.

## Evidence boundary

A green Brian2 comparison validates external-reference conformance for the declared numerical contract. It is not independent authorship replication and must not be promoted automatically from DATA to EVID. Human evidence review remains required.

## Homeostasis

The current LIF diagnostic operating envelope is configuration-specific: target 10 Hz was reached without actuator saturation for currents 16, 18, 20, 22 and 25 under the declared Stage-0 diagnostic configuration. At current 30 the +10 mV threshold-offset bound saturated. This must be described as an operating envelope, not as a universal biological or cross-model current boundary.
