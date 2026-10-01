# CUDA-PAN implementation status (Playground -> MHRN boundary)

**Branch:** `develop`  
**Status date:** 2026-09-28  
**Classification:** engineering / Playground reference implementation  
**Scientific evidence:** false

This document tracks executable CUDA/PAN engineering and the promotion boundary into canonical MHRN. Engineering verification never auto-promotes to DATA or EVID.

## Current layer status

| Layer | Current status | Notes |
| --- | --- | --- |
| 1 Compiler | implemented | PlaygroundConfig -> Gate IR -> PTX/CUDA scaffold; ptxas resource parsing |
| 2 GPU runtime | implemented reference | CUDA Driver API load/context/module/function, occupancy, VRAM allocation, H2D/D2H, kernel/cooperative launch, synchronization and cleanup |
| 3 Gate execution | CUDA-1.3 hardware-verified reference | executable bounded gate ABI; fail-closed D2/RNG/cleanup checks |
| 4 Recurrent network dynamics | CUDA-1.4 implemented reference | LIF/AdEx/PAN-AdEx membrane state, incoming CSR, integer delays, delay ring, multi-block cooperative execution |
| 5 Closed loop | CPU implemented; CUDA-1.6 pending | sensors/body/posture/action/environment/reward are not yet a full CUDA causal loop |
| 6 Synaptic learning | CUDA-1.5 implemented reference | frozen-reward STP, pair STDP, eligibility, reward-modulated weight update, decay/clamp; canonical LearningEngine alignment remains open |
| 7 PAN hyperstate | partial / CPU-side exploratory | full Health/Energy/Consolidation/Apoptosis/Growth contract is not a canonical GPU implementation |
| 8 Structural plasticity | canonical CPU pipeline; CUDA integration pending | GPU execution must use governed host barriers and stable identity/repacking contracts |
| 9 Parity | D1/D2 reference implemented; D3 live causal parity pending | fail-closed NaN/Inf/empty/shape checks; recurrent/plasticity state parity exists in bounded engineering scope |
| 10 Infrastructure | partial | execution provenance, canonical storage/checkpoint, Backend interface and tiered scaling remain integration work |

## Physical RTX 3060 engineering verification

The repository records bounded hardware acceptance for CUDA-1.4 and CUDA-1.5 on 2026-09-28. The recurrent reference has been exercised across multiple tick counts, delays and block sizes with exact spike agreement in the tested fixtures and bounded continuous-state error. The plastic reference has exercised positive, zero and negative frozen rewards and compares weights, eligibility and STP availability in addition to membrane state.

These are engineering verification results only. They do not establish:

- complete PAN-GPU execution;
- structural-plasticity equivalence;
- free closed-loop behavioral equivalence;
- performance superiority;
- scientific validity of PAN mechanisms;
- EVID for any MHRN research claim.

## Promotion boundary

Candidates for canonical extraction now include:

- CUDA Driver/NVRTC infrastructure;
- explicit kernel ABI and fail-closed host validation;
- allocation/copy/cleanup contracts;
- cooperative-launch and occupancy preflight;
- deterministic RNG primitives;
- recurrent backend reference;
- D1/D2 parity infrastructure;
- frozen-action/frozen-reward replay;
- ptxas/resource provenance.

They must be re-homed behind canonical MHRN interfaces rather than making `src/playground` a dependency of the core.

Remain Playground/reference-specific unless separately promoted:

- preset/UI aliases;
- stick-figure implementation;
- exploratory posture/reward weights;
- current A/B/C/D gate grouping;
- BehavioralLearningEngine as a reference policy;
- Playground SessionDaemon;
- Playground JSON persistence;
- exploratory PAN/cortical/thalamic naming and hypotheses.

## Canonical next gates

1. Define `ExecutionBackend` and make CPU/CUDA implementations consume the same network/state contracts.
2. Freeze a canonical Learning/Synapse contract before treating CUDA-1.5 as a backend for canonical learning experiments.
3. Canonicalize D1/D2/D3 parity and execution fingerprints.
4. Integrate canonical checkpoint/storage and BoundaryFrame/Neural-I/O state.
5. Execute CUDA-1.6 first with frozen boundary/environment trajectories, then live deterministic closed-loop trajectories.
6. Freeze PAN semantic state before porting full Health/Energy/Consolidation/Apoptosis/Growth.
7. Route structural changes through deterministic host barriers and the canonical Self-Organization approval/journal/undo path.
8. Only then evaluate scaling, multi-GPU and optional external/neuromorphic adapters.

See also `docs/08-roadmap/MHRN_SIMULATOR_CAPABILITY_GAPS.md`.
