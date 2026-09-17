# RQ-SNN-003 / H-SNN-003-B — topology_propagation_v1 adequacy decision

**Date:** 2026-09-17  
**Status:** accepted scientific-method decision  
**Scope:** `RQ-SNN-003`, `H-SNN-003-B`, `topology_propagation_v1`, `EXP-GEN-0047`  
**Data policy:** archived DATA and manifests remain immutable

## Decision

`EXP-GEN-0047` is technically valid and reproducible for the executed program, and its six observed conditions are the intended semantic conditions for `RQ-SNN-003`:

- `1d`
- `2d`
- `3d`
- `5d`
- `5d_shuffled`
- `random_graph`

The semantic classifier therefore treats the condition set as `DIRECT_MATCH`.

This semantic match does **not** make the experiment adequate to test `H-SNN-003-B`. The implemented `topology_propagation_v1` design is classified as `INADEQUATE_TO_TEST_HYPOTHESIS`.

## Why the v1 design is not test-adequate

The current `run_5d()` implementation constructs only three neurons and two feed-forward synapses for each dimensional condition. The non-random conditions use the same explicit chain with fixed weights and delays. Coordinates change, but the mechanism that carries activity is not sufficiently coupled to geometric dimensionality.

For `EXP-GEN-0047` the deterministic statistics show the same core response for all six conditions:

- 3 spikes
- 2 delivered synaptic events
- 3 activated neurons
- 0 recurrent events
- propagation depth 1
- ISI 1

The only reported difference is `first_response_latency=1` for `random_graph` versus `2` for the other conditions. The random graph condition also changes the explicit edge arrangement, so this single-tick descriptive difference cannot be promoted to evidence for a dimensional or topology effect.

The result is therefore neither confirmation nor refutation of `H-SNN-003-B`. In particular, identical outcomes across 1D/2D/3D/5D must not be described as evidence that topology or dimensionality has no effect.

## AIRR interpretation rule

For a protocol deterministically classified as `INADEQUATE_TO_TEST_HYPOTHESIS`:

1. AIRR may describe the archived observations.
2. AIRR must not use inferential language unless a registered deterministic inferential analysis exists.
3. Uniform outcomes must not be converted into a topology-null conclusion.
4. An isolated latency difference must not be promoted to a topology effect.
5. Public/report-level AI confidence is forced to `0.0` for the hypothesis-level interpretation; the original model confidence remains only in the append-only AIAR audit record.

The earlier wording that topology "may not significantly affect propagation behavior" is methodologically too strong for this design. The correct conclusion is that the design is not sensitive enough to answer the registered topology question.

## Quiescence contract

`run_5d()` calls `NetworkImpulseProbe` with `min_ticks=ticks` and `max_ticks=ticks`. This deliberately disables early termination before the requested observation window has completed.

Therefore `stopped_on_quiescence=false` in all 18 runs is expected protocol behavior, not evidence of a missing quiescence trigger. Early-stop behavior is a separate mode and requires `min_ticks < max_ticks`.

## Requirements for topology_propagation_v2

The next hypothesis-bearing test must be preregistered before execution and must make topology capable of changing propagation by construction.

Minimum design requirements:

- **Network size:** at least 1,000 neurons per condition.
- **Degree/density:** target at least 10 incoming synapses per neuron on average, with the realized degree distribution archived and matched across comparison conditions.
- **Matched global structure:** identical neuron count, target edge count/density, neuron and synapse parameter distributions, seed policy, observation window and stimulus energy across topology conditions.
- **Geometry-to-dynamics coupling:** connectivity probability and/or synaptic delay must be an explicit preregistered function of distance in the represented dimensional space. Coordinates may not be metadata only.
- **Controls:** `1d`, `2d`, `3d`, `5d`, `5d_shuffled`, and degree/density-matched `random_graph`, with each control's purpose stated before execution.
- **Stimulus:** a matched input region containing multiple neurons, not a single isolated source neuron.
- **Primary outcomes:** distributions of first-arrival latency and propagation reach across target regions/neuron fractions; secondary outcomes may include activated-neuron fraction, event count, path/depth summaries and recurrence.
- **Activity adequacy gate:** before testing the hypothesis, the run must show that the stimulus generated enough network activity to expose topology. Failure of this gate is `NOT_TESTED`, not a null result.
- **Replication:** multiple independent seeds with topology generation varying according to a registered seed schedule; deterministic same-seed replicas remain a separate reproducibility check.
- **Inference:** the statistical comparison and effect-size rule must be frozen before data generation. `H-SNN-003-B` requires a difference between at least two topology conditions; no 5D advantage is assumed.
- **Provenance:** clean Git tree, frozen source/config hashes, complete topology-generation metadata, realized graph statistics and raw per-run outcomes.

The values `1,000 neurons` and `>=10 incoming synapses/neuron` are minimum operational thresholds for the next test generation, not claims that they are universally sufficient. A pilot may still fail the activity-adequacy gate and require a new preregistered design revision.

## Historical-data rule

No archived run, manifest, AIRR, review or digest from `EXP-GEN-0047` is rewritten to manufacture stronger evidence. The new semantic and adequacy classifiers describe how the immutable historical artifacts may be used prospectively in summaries and reviews.
