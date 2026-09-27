# CUDA-PAN implementation status (Playground -> MHRN boundary)

**Branch:** `develop`  
**Classification:** engineering / Playground  
**Scientific evidence:** false

This document tracks which CUDA-PAN functions exist in the Playground, which are
executed, and which may later be promoted into the canonical MHRN CUDA backend.

## Current layer status

| Layer | Current status | Notes |
|---|---|---|
| 1 Compiler | implemented | Config -> Gate IR -> PTX + CUDA C++ scaffold, ptxas resource parsing |
| 2 GPU runtime | CUDA-1.2 implementation | Driver load, context/module/function, occupancy, VRAM allocation, H2D/D2H, `cuLaunchKernel`, synchronize |
| 3 Gate execution | bounded single-tick kernel available | A/B/C/D gate program only; not yet full SNN neuron/synapse state |
| 4 Network dynamics | CPU Playground only / CUDA pending | recurrent synapse propagation, deterministic delay buffers and full state evolution are not yet CUDA-backed |
| 5 Closed loop | CPU Playground implemented | action selection, target/action/reward loop exists; CUDA integration pending |
| 6 Learning | CPU Playground partial | credit/reward mechanisms exist; full CUDA STDP/reward update pending |
| 7 Stick figure application | CPU Playground implemented | deterministic point-mass/spring sandbox, sensors, actuators, posture and reward trigger |
| 8 Parity | contracts + CPU reference implemented | D1/D2/D3 contracts and freeze mode exist; actual CPU<->CUDA full-state parity pending |
| 9 Infrastructure | partial | compiler manifests, validation, logging/persistence elsewhere; tiered CUDA storage remains pending |

## CUDA-1.2 executable gate ABI

The generated PTX manifest now declares the `pan_gate_kernel` ABI explicitly.
The runtime validates all host-buffer dimensions before any device allocation.

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

A deterministic smoke-input builder exists for hardware validation. A successful
single-tick launch proves only that the bounded Playground gate kernel executed.
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

1. Execute `pan_gate_kernel` on the target RTX 3060 and persist a technical
   smoke report.
2. Add a CPU implementation of the exact gate ABI and compare all current/action
   outputs for one tick (D2 gate parity).
3. Extend the executable kernel ABI with membrane/adaptation/refractory state.
4. Add deterministic recurrent synapse gather and delay-ring state.
5. Run 10 then 100 ticks without plasticity.
6. Add eligibility/STDP/reward-modulated weight state.
7. Couple the CUDA network step to the already existing CPU sandbox.
8. Only after those gates pass, evaluate which runtime pieces become canonical
   MHRN CUDA code.
