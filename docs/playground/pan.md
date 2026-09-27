# PAN in the MHRN Playground

**Classification: PLAYGROUND_PAN — exploratory only.**

PAN is implemented as an optional exploratory state layer on top of the
existing bounded Playground simulator. It does not create a second canonical
MHRN engine and it does not write into the scientific registry.

## Hyperstate

PAN uses a configurable hyperstate with 5..32 dimensions. The first ten
descriptive axes are:

1. intrinsic simulation time
2. excitability proxy
3. plasticity activity
4. local information proxy
5. health
6. neuromodulation proxy
7. energy budget
8. embodied-position projection
9. consolidation proxy
10. network-coupling proxy

Dimensions above ten are intentionally unassigned latent axes.

### Important information-boundary note

Dimension 4 is **not PID**. The current Playground implementation uses a local
surprise proxy and reports:

- `information_axis: local_surprise_proxy_not_PID`
- `pid_status: NOT_IMPLEMENTED`

A scientific PID claim requires an explicit definition of sources/target,
estimator validation, bias analysis and a new preregistered canonical run.

## PAN runtime

The optional PAN layer adds bounded exploratory state variables per neuron:

- health
- spike amplitude
- energy
- activity EMA
- consolidation
- alive/apoptotic state
- hyperstate vector

The simulator can project the previous population hyperstate back into neuron
input through a seeded feedback matrix. This is a Playground closed loop only;
it is not a validated MHRN world model.

## PAN building blocks

Neuron:

- `pan_adex_5d`: AdEx membrane dynamics with the PAN hyperstate layer.

Synapse:

- `pan_stp_stdp`: exploratory release-state depression/recovery plus pair
  STDP.

The same PAN layer can also be enabled with other existing Playground neuron
models via `pan_enabled=true`.

## Research candidates

The Playground exposes PAN observations only as
`DRAFT_IDEA_NOT_PREREGISTERED` candidates. Current candidates include:

- health-modulated homeostatic recovery after perturbation
- hyperstate feedback versus matched no-feedback recurrence
- replacement of the surprise proxy by a formally specified information/PID
  measure
- health/energy/apoptosis transition dynamics under matched stress

These are **not hypotheses in the MHRN Research Registry**.

The only allowed route into science is:

```text
Playground observation
-> research candidate
-> new hypothesis
-> new preregistration
-> freeze
-> new canonical DATA run
-> Human Review
-> optional EVID
```

No Playground result is promoted, copied or counted automatically.


## Generative gate runtime

The Playground can now translate validated PAN/geometry/clock settings into a
descriptive `GateSchematic`. The mapping is explicit and inspectable; it does
not claim that Python objects are physical logic gates or CUDA cores.

Implemented reference primitives include:

- apoptosis / aging threshold gates
- feedback-gain gate
- geometry sigma, probability, radius and conduction-delay gates
- base-clock, continuous-step and event-batch timers
- neurogenesis, synaptogenesis, path-formation and pruning triggers

Every schematic reports `classification: PLAYGROUND_GATE_SCHEMATIC`,
`scientific_evidence: false`, `generation: SETTINGS_DERIVED` and
`hardware_execution: PYTHON_REFERENCE_ONLY`.

## Dual event + continuous clock

`clock_mode=dual` adds a deterministic interleaved scheduler around the
existing Playground continuous tick engine. Spikes are queued as events and
drained at explicit synchronization barriers. This is a reference execution
model, not actual simultaneous CPU/GPU concurrency. Results report
`execution_semantics: DETERMINISTIC_INTERLEAVED_REFERENCE`.

Generative growth requires dual mode so that structural mutation occurs only
at defined barriers.

## Event-driven generative growth

With `growth_enabled=true`, barrier events can drive bounded structural
changes: repeated coactivation can trigger synaptogenesis, high
information-proxy nodes can trigger path formation, weak edges can be pruned,
and sufficient activity can reactivate an apoptotic slot.

The current neurogenesis implementation is deliberately conservative:
population storage is fixed at `n_neurons`. Neurogenesis means reactivating an
existing apoptotic slot; it does not dynamically reallocate the population.
Results report `REACTIVATE_APOPTOTIC_SLOT_NO_REALLOCATION`.

## CUDA budget and SSD offload

`cuda_budget_mb` provides a memory-layout estimate for a hypothetical compact
CUDA implementation. The current Python reference backend does not allocate
CUDA tensors from this pool. It reports `REFERENCE_ESTIMATE_ONLY` and
`NOT_IMPLEMENTED_IN_PYTHON_REFERENCE_BACKEND`.

Optional SSD offload writes compressed event batches and lightweight snapshots
only below `playground_sessions/pan_offload/`, through the same Playground
isolation guard that blocks canonical research paths. The reference writer is
synchronous; asynchronous CUDA streams, pinned-memory transfer and GPU-to-SSD
pipelines remain unimplemented.

## CUDA hardware boundary

| Capability | Current Playground status |
|---|---|
| settings -> gate schematic | implemented reference |
| dual event + continuous scheduler | implemented reference |
| bounded event-driven growth | implemented fixed-capacity reference |
| 2 GiB CUDA memory planning | estimate only |
| compressed SSD offload | implemented synchronous reference |
| persistent CUDA gate kernels | not implemented |
| CUDA Dynamic Parallelism growth | not implemented |
| SM topology as PAN geometry | exploratory idea only |
| thermal state as health feedback | exploratory idea only |

No claim is made that a gate is a CUDA core or that GPU thermal behavior is a
biological analogue.


## Cognitive learning extension

PAN Playground now includes three executable reference components:

1. **ThalamicGating** — bounded relay/attention/inhibition gains. This is a
   functional abstraction, not a biological thalamus model.
2. **CorticalOrganization** — conditioned layer labels (default six) with
   optional reward-modulated layer-gain plasticity.
3. **BehavioralLearningEngine** — bounded reward-modulated policy learning that
   stores policy parameters/traces rather than exact external payloads.

The learned policy is fed back into the output population as bounded current,
so a single Playground session can execute, update the policy, and continue
under the updated policy.

The external boundary is not duplicated. PAN reuses the project's existing
`NetworkAreaAdapter`, Gateway Runtime, MSBA audio/vision/digital modalities
and Neural I/O codec/lifecycle contracts.

The Dashboard exposes these settings directly under **Lernen & kognitive
Organisation**.

### Hardware profile

`cuda_8gb_balanced_plan` records the 8-GB architecture estimates (including
12,288 active-neuron and 50-million-synapse planning targets), but reports
register-native kernels, PTX gates and Dynamic Parallelism as NOT IMPLEMENTED.
The runnable backend remains the Python reference implementation.

Full status matrix: `docs/playground/PAN_COMPLETE_ARCHITECTURE.md`.
