# CUDA-PAN implementation status (Playground -> MHRN boundary)

**Status reconciliation:** 24 October 2026, local `feature/cuda-pan-feedback-history` working tree; not a release freeze.
**Classification:** engineering / Playground  
**Scientific evidence:** false

This document tracks which CUDA-PAN functions exist in the Playground, which are
executed, and which may later be promoted into the canonical MHRN CUDA backend.

## Current layer status

| Layer | Current status | Notes |
|---|---|---|
| 1 Compiler | implemented | Config -> Gate IR -> PTX + CUDA C++ scaffold, ptxas resource parsing |
| 2 GPU runtime | CUDA-1.2 implementation | Driver load, context/module/function, occupancy, VRAM allocation, H2D/D2H, `cuLaunchKernel`, synchronize |
| 3 Gate execution | CUDA-1.3 hardware validation documented | Bounded gate ABI; see [roadmap](PAN_GPU_ROADMAP.md) for subsequent stages |
| 4 Network dynamics | CUDA recurrent and hybrid Builder paths implemented | [Recurrent reference](CUDA14_RECURRENT.md), [Builder synapses](CUDA16_BUILDER_SYNAPSES.md), [resident delay queue](CUDA_RESIDENT_DELAY_QUEUE.md), [neuron traces](CUDA_RESIDENT_NEURON_TRACES.md), [PAN population](CUDA_PAN_POPULATION.md); feedback history is local working-tree integration |
| 5 Closed loop | CPU world coupled to CUDA Builder | [Hybrid D3](CUDA16_BUILDER_HYBRID.md); body/sensors/action policy remain host-owned; GPU live sessions remain unsupported |
| 6 Learning | Bounded CUDA plasticity implemented | [Frozen-reward reference](CUDA15_PLASTICITY.md) and [actual Builder plasticity](CUDA16_BUILDER_PLASTICITY.md) have distinct contracts; global modulators remain host-calculated |
| 7 Stick figure application | CPU Playground implemented | deterministic point-mass/spring sandbox, sensors, actuators, posture and reward trigger |
| 8 Parity | Scoped CPU/CUDA and Builder D3 tests implemented | State, queue, traces, RNG and trajectories are compared within declared paths; this does not establish canonical full-MHRN parity |
| 9 Infrastructure | partial | compiler manifests, validation, logging/persistence elsewhere; tiered CUDA storage remains pending |

## CUDA-1.2 executable gate ABI

The generated PTX manifest now declares the `pan_gate_kernel` ABI explicitly.
The runtime validates all host-buffer dimensions, numeric finiteness, float32
range, uint32 scalar fields and uint64 channel masks before any device
allocation. H2D/DtoH copies check both host-buffer and device-allocation sizes.

The first executable path performs:

```text
compile_config
 -> ptxas
 -> cuInit
 -> cuDeviceGet
 -> cuCtxCreate
 -> cuModuleLoad
 -> cuModuleGetFunction
 -> cuMemAlloc
 -> cuMemcpyHtoD
 -> cuLaunchKernel
 -> cuCtxSynchronize
 -> cuMemcpyDtoH
 -> cleanup
```

A deterministic non-trivial CPU gate reference and hardware-smoke path exist for
validation. D2 comparison fails closed on NaN/Inf, empty evidence, action/current
length mismatches and invalid action types. The epsilon-greedy mapping uses the
upper 24 hash bits so its float32 uniform is guaranteed to remain in [0, 1).
The smoke path also records CUDA free/total memory before allocation and after
cleanup. A successful single-tick launch proves only that the bounded Playground
gate kernel executed.
It does **not** prove a complete MHRN SNN, STDP parity, behavioral equivalence,
or scientific acceleration.

## Promotion boundary: Playground -> canonical MHRN

Candidates for later transfer after validation:

- platform-neutral CUDA Driver API wrapper;
- explicit kernel ABI manifest;
- buffer-shape validation and fail-closed argument checking;
- deterministic seed/neuron/tick hash contract;
- ptxas resource report parsing;
- occupancy/cooperative-launch preflight;
- D1/D2/D3 parity helpers;
- freeze-action/freeze-reward replay contracts.

Remain Playground-specific unless separately promoted:

- stick-figure sandbox implementation;
- UI presets and Playground configuration aliases;
- exploratory posture reward weights/triggers;
- current A/B/C/D gate grouping;
- synthetic audio/visual proxies.

Canonical MHRN promotion must preserve the contracts already documented in
`docs/02-architecture/MHRN_CUDA.md`, especially stable neuron/edge identity,
canonical CSR ordering, deterministic reduction/scheduling, execution
provenance, and structural-barrier rules.

## Next CUDA steps

1. Validate and integrate the local [resident feedback history](CUDA_PAN_FEEDBACK_HISTORY.md) change, including dynamic delay retention, source transforms and Builder D3.
2. Implement persistent live-session lifecycle, bounded cancellation and complete versioned checkpoint/resume with interrupted-run equivalence.
3. Introduce explicit canonical state adapters and RuntimeController conformance before describing this as a productive MHRN CUDA backend.
4. Validate structural mutation, stable IDs and pending-event migration at host barriers.
5. Measure resident execution and scaling separately; remaining host mirrors and transfers prevent a full device-residency claim.

The [PAN GPU roadmap](PAN_GPU_ROADMAP.md) records stage-specific acceptance and historical hardware results. This overview is not a new scientific evidence decision.
