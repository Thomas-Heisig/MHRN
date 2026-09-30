# MHRN simulator capability gaps and canonical integration programme

**Status:** active roadmap / research-design input  
**Date:** 2026-09-28  
**Scientific evidence:** none created by this document

## Purpose

This document separates three different questions that must not be conflated:

1. Which Playground/CUDA/PAN mechanisms are mature enough to become canonical MHRN infrastructure?
2. Which simulator capabilities are still missing compared with established systems such as Brian 2 and its external devices?
3. Which of those gaps are engineering backlog items and which require new preregistered scientific questions?

Existing Playground runs and RTX 3060 verification remain **engineering verification**. They motivate new canonical research but are not promoted retroactively to DATA or EVID.

## Architecture decision: do not promote the whole Playground

The Playground must not become the new MHRN core or a second canonical runtime as one monolithic package.

Target rule:

```text
Playground uses MHRN.
MHRN does not depend on Playground.
```

The reusable execution pieces are promoted behind canonical contracts:

```text
Dashboard / Research / Playground
            |
      canonical Runtime
            |
      ExecutionBackend
       /           \
   CPU backend   CUDA backend
       \           /
       parity contracts
            |
 canonical Network / Learning / Storage / Self-Organization
```

The Playground remains the composition, preset, exploratory and reference-policy workspace. Its duplicate session runtime, JSON persistence and direct structural mutation must not become authoritative.

## Corrected current CUDA/PAN boundary

As of 2026-09-28:

- Gate IR -> PTX/CUDA compilation and executable gate ABI exist.
- CUDA Driver API, H2D/D2H, allocation cleanup, cooperative launch and NVRTC paths exist.
- CUDA-1.4 recurrent LIF/AdEx/PAN-AdEx membrane execution with static recurrent synapses and delays has physical RTX 3060 verification.
- CUDA-1.5 frozen-reward STP/STDP/eligibility/weight-update reference execution has physical RTX 3060 verification.
- The complete PAN hyperstate (health, energy, consolidation, apoptosis, growth), governed structural mutation and the full embodied closed loop are **not** yet a canonical CUDA backend.
- D1/D2 engineering parity exists for the bounded recurrent/plasticity reference. Full D3 live causal trajectory parity remains open.

## Capability gap matrix

| Capability | Brian 2 / related ecosystem | MHRN current state | Integration class |
| --- | --- | --- | --- |
| Equation-defined neuron dynamics | Brian 2 defines models from equations | LIF/AdEx/PAN-AdEx are code-defined | SHOULD: model-contract/DSL feasibility |
| Physical units | Brian 2 checks dimensional consistency | runtime values are predominantly raw numeric values | SHOULD: boundary/config unit schema before broad DSL |
| Multicompartment neurons | Brian 2 provides `SpatialNeuron` | point-neuron core | OPTIONAL research/modeling track |
| Gap junctions | expressible through Brian 2 synapse equations; official example exists | no canonical electrical-synapse type | OPTIONAL after synapse contract |
| User-defined synapse equations/rules | Brian 2 `Synapses` supports model/on_pre/on_post code | canonical learning rules are implemented in code | SHOULD: versioned synapse-rule contract; do not weaken governance |
| SDE/noise model specification | Brian equations support stochastic terms for supported solvers | noise exists only in selected fixed mechanisms | SHOULD where required by a registered protocol |
| Recurrent CUDA backend | Brian2CUDA / Brian2GeNN provide external GPU paths | bounded native recurrent CUDA reference now exists | MUST canonicalize backend boundary |
| Structural plasticity on GPU | contemporary GeNN research demonstrates GPU structural-plasticity workflows | canonical CPU structural pipeline exists; GPU barrier integration pending | MUST research structural-barrier contract |
| Cross-backend bitwise reproducibility | Brian 2 explicitly does not guarantee universal bitwise reproducibility | MHRN has explicit D1/D2/D3 and execution-fingerprint direction | MUST preserve and validate |
| Standardized benchmark suite | Brian ecosystem has dedicated benchmark repositories and model workloads | MHRN has performance tests but no stable simulator-comparison suite | SHOULD |
| Neuromorphic adapters | Brian ecosystem includes external GeNN/Lava integrations | no Loihi/SpiNNaker backend | OPTIONAL interoperability, not core requirement |
| Community/published model library | mature external ecosystem | early MHRN ecosystem | ORGANIC / publication and replication work |

Sources are registered in `research/registry/sources.acceleration.yaml`. The comparison is descriptive; it is not an overall simulator ranking.

## Mandatory canonicalization gaps

Before Playground execution can be treated as a normal MHRN backend, the following are mandatory:

1. **ExecutionBackend contract** separating runtime control from execution implementation.
2. **Canonical neuron/synapse state contract** with stable neuron and edge identities.
3. **Canonical Learning/Synapse contract** defining STDP/STP/eligibility/reward timing, update ordering, clamping and delayed-emission semantics.
4. **Canonical parity framework** for D1 events, D2 state and D3 causal closed-loop trajectory.
5. **Early benchmark/reference suite** using frozen MHRN workloads plus an explicit restricted Brian 2 reference subset; this validates parity infrastructure before live CUDA-1.6 rather than after PAN-GPU.
6. **Canonical checkpoint/storage contract** including neuron/synapse state, pending events/delays/rewards, PAN/tissue sidecars, RNG, topology generation, environment state and execution fingerprint.
7. **Canonical Neural-I/O contract** using the existing `BoundaryFrame`, `CodecContract`, `PopulationLayout`, `SpikeFrame`, `DecodeResult` and `CodecStreamState` design.
8. **Frozen-Environment contract** — executable FE-1 integrity, FE-2 repeated replay, CPU/self FE-3 control and a canonical live-input ExecutionBackend adapter are implemented. A versioned FE-3 manifest is frozen; physical CPU-vs-CUDA FE-3 remains pending the RTX-class hardware acceptance run.
9. **Canonical structural approval/barrier contract** routing Growth/Pruning/Apoptosis through Proposal -> Coordinator Approval -> StructuralPlasticityEngine -> Journal/Undo.
10. **Truthful execution provenance**: CPU fallback, CUDA reference, hardware smoke and scientific run must never share ambiguous labels.

## Simulator capability work packages

### WP-MODEL-1 — versioned model description contract
Investigate a restricted equation/model representation before attempting a general Brian-compatible DSL. A model artifact must be versioned, hashed and validated before execution.

### WP-UNITS-1 — dimensional boundary
Introduce explicit physical-unit metadata and dimensional validation at configuration/model boundaries. Internal kernel storage can remain canonical base units; units are not required in the hot path.

### WP-SYN-1 — generalized synapse rule contract
Define a versioned rule interface that can express current canonical STDP/STP/eligibility behavior first. Arbitrary user code must not bypass determinism, resource or research governance.

### WP-COMPARTMENT-1 — multicompartment feasibility
Treat dendritic/multicompartment neurons as a separate optional model family, not as a prerequisite for the current point-neuron research programme.

### WP-ELECTRICAL-1 — gap-junction feasibility
Add only after bidirectional/current-coupled edge semantics are formally separated from spike-event synapses.

### WP-BENCH-1 — simulator benchmark suite
Create stable workloads with frozen versions and manifests: point-neuron baseline, recurrent delay network, plastic network, sparse scaling workload and external-reference subset. Measure build/codegen, initialization, simulation, memory and result parity separately.

### WP-INTEROP-1 — Brian 2 reference adapter
Do not use Brian 2 as a hidden implementation backend for MHRN. Build a restricted explicit adapter for preregistered reference comparisons. Map equations/parameters/units/integrator/delays/RNG and record both artifacts.

### WP-NEUROMORPHIC-1 — external hardware adapters
Loihi 2, Lava, SpiNNaker or similar targets remain optional adapters after canonical MHRN semantics are stable. External backend limitations become part of the execution fingerprint.

## Research programme

Canonical questions and untested hypotheses are stored in:

- `research/registry/questions.acceleration.yaml`
- `research/registry/hypotheses.acceleration.yaml`
- `research/registry/sources.acceleration.yaml`

The initial research families are:

- `RQ-CUDA-DET-001` — deterministic accelerated execution
- `RQ-CUDA-PAR-001` — CPU/CUDA backend parity
- `RQ-CUDA-SCALE-001` — computational scaling
- `RQ-GATE-IR-001` — executable Gate-IR semantics
- `RQ-PAN-SEM-001` — PAN semantic/state contract
- `RQ-PAN-GPU-001` — PAN cross-backend execution
- `RQ-CUDA-STRUCT-001` — structural mutation across host/GPU barriers
- `RQ-CUDA-CL-001` — causal closed-loop backend parity
- `RQ-FE-001` — Frozen-Environment verification methodology
- `RQ-SIM-INTEROP-001` — external simulator interoperability

No CLAIM entry is created by registration alone.

## Evidence ladder

```text
ENGINEERING
  hardware smoke / analytic unit tests
        |
        v
BACKEND VERIFICATION
  frozen reference + fail-closed parity
        |
        v
PREREGISTERED DATA
  fresh source freeze + controls + independent seeds
        |
        v
HUMAN REVIEW
        |
        v
EVID / bounded claim
```

## Priority

**MUST now:** canonical ExecutionBackend, learning/synapse contract, parity framework, early benchmark/reference suite, complete checkpoint/state integration, canonical Neural I/O types, Frozen-Environment contract, then CUDA-1.6 frozen and live closed-loop bridge.

**SHOULD next:** model/unit contract, generalized synapse-rule interface and broader Brian 2 interoperability beyond the early restricted reference subset.

**OPTIONAL after core closure:** multicompartment neurons, gap junctions, broad SDE model language, Loihi/SpiNNaker adapters, multi-GPU.

This ordering prevents feature parity with another simulator from displacing MHRN's primary scientific requirement: explicit semantics, provenance and reproducible evidence.


## Wave 3 status — execution and verification plane (2026-09-29)

Wave 3 closes two previously mandatory **engineering** gaps:

1. the backend-neutral ExecutionBackend contract now exists;
2. D1/D2/D3 parity, stable execution fingerprints and deterministic RNG/order/delay primitives now have canonical MHRN ownership.

The Playground is no longer the authority for Builder parity or stochastic release semantics. It imports the canonical contracts while preserving its historical public import paths.

This does **not** close RQ-CUDA-PAR-001. There is still no canonical CUDABackend implementing ExecutionBackend, and therefore no new preregistered CPU/CUDA DATA line produced by Wave 3.

The immediate remaining acceleration gap is Wave 4:

- extract CUDA Driver/NVRTC/ABI infrastructure to src/acceleration/cuda;
- implement CUDABackend against ExecutionBackend;
- preserve exact backend provenance and no-fallback labeling;
- run the first canonical backend comparison through src/verification/parity.

Learning, full PAN hyperstate, structural mutation and live closed-loop parity remain separately gated by their existing semantic contracts.


## Frozen-Environment acceptance status — 2026-09-30

The Frozen-Environment programme now has an executable verification layer
rather than documentation alone. Manifest artifacts use canonical JSON and
self-declared SHA-256 verification; FE-1 validates exact BoundaryFrame replay;
FE-2 verifies repeated deterministic trajectories; and FE-3 has a CPU/self D3c
control wired to the canonical parity framework.

This closes the **verification-instrument gap**, not the scientific
CPU/CUDA-equivalence question. Physical CUDA D3 remains pending, and no FE
acceptance result is DATA or EVID by itself.


## Hardware D3 bridge status — 2026-09-30

The physical CUDA acceptance runner now groups three distinct engineering
surfaces without conflating them:

- canonical Wave-4 CPU/CUDA D1/D2;
- optional recurrent/plasticity hardware reruns;
- a live Builder CPU/CUDA D3c bridge over the existing CPU world.

The third item remains a useful historical bridge because it exercises live
causal actions and full body trajectory equality. The canonical
Frozen-Environment path now also has a backend-neutral live-input adapter:
each tick converts the current frozen world state into a canonical
BoundaryFrame and external-current row, advances CPUReferenceBackend or
CUDABackend through the same continuation API, decodes an ActionCommand and
returns it to `FrozenWorldSession`.

The first versioned FE-3 manifest is
`research/verification/frozen_environment/FE3_DETERMINISTIC_TARGET_V1.json`.
Hosted CI verifies the adapter and CPU/self parity. Physical CPU-vs-CUDA FE-3
remains `HARDWARE_ACCEPTANCE_PENDING` until the dedicated RTX-class run
passes. No DATA/EVID is produced by either bridge or hardware acceptance.
