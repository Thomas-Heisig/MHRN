# Canonical CUDA Backend Contract

Status: canonical engineering contract, Wave 4  
Date: 2026-09-29  
Scientific evidence: none created by this document  
Implementation: `src/acceleration/cuda/`

## Scope

Wave 4 moves the hardware-tested CUDA execution infrastructure out of
Playground ownership and behind the Wave-3 `ExecutionBackend` contract.

Canonical ownership now covers:

- CUDA Driver API wrapper, allocation/copy guards, NVRTC and ptxas/preflight;
- bounded recurrent LIF/AdEx/PAN-AdEx membrane execution;
- static recurrent delays and the existing CUDA-1.4 reference kernel;
- the existing CUDA-1.5 STP/STDP/eligibility/frozen-reward engineering kernels;
- a backend-neutral `CUDABackend` facade;
- an explicit CPU scalar reference backend for D1/D2 acceptance;
- Playground compatibility shims that import canonical acceleration code.

The dependency direction is normative:

```text
Playground -> src.acceleration.cuda
src.acceleration.cuda -X-> src.playground
```

## Kernel freeze

Wave 4 is an ownership/interface extraction, not a kernel rewrite.

The canonical recurrent kernel is byte-identical to the previously verified
`src/playground/cuda/recurrent.cu`. The canonical plasticity kernel is
byte-identical to `src/playground/cuda/builder_synapses.cu`.

CI executes a kernel-freeze gate and fails if either pair diverges.

Any future semantic kernel change requires a new engineering verification
baseline and cannot inherit the old RTX-3060 parity observations unchanged.

## Execution mode

The first canonical facade declares:

```text
execution_mode = BOUNDED_REPLAY_REFERENCE
```

Its snapshot is backend-neutral and contains canonical configuration, seed,
continuation tick and digest data only. It contains no CUDA pointer, context,
module, stream or kernel handle.

The facade currently reconstructs continuation by deterministic prefix replay.
This satisfies the data-only state boundary for the bounded reference scope but
is not claimed to be the final resident high-performance checkpoint design.

A later wave must promote continuation-critical resident delay/plasticity/PAN
state into the canonical RuntimeCheckpoint contract.

## Capabilities

Wave-4 capabilities are bounded declarations:

- recurrent: supported;
- technical plasticity kernels: available;
- PAN hyperstate: not supported by the canonical backend;
- structural plasticity: not supported by the canonical backend;
- max neurons: 4096;
- max ticks: 2000;
- max edges: 65536;
- deterministic under the declared bounded reference contract.

Capability declarations are engineering metadata, not scientific validation.

## Plasticity semantic boundary

The CUDA plasticity implementation is physically canonicalized as reusable
acceleration infrastructure but its scientific/learning semantics remain:

```text
plasticity_semantics = NON_CANONICAL_DRAFT
learning_contract_id = mhrn-learning-synapse-v1
learning_contract_status = ALIGNMENT_PENDING
```

This is required because the canonical CPU LearningEngine and the CUDA-1.5
reference are not yet semantically identical for every STDP/STP/eligibility/
reward rule. `supports_plasticity=True` means the technical kernel path exists;
it does not mean the canonical Learning/Synapse contract has been satisfied.

## Parity acceptance

Wave 4 adds an explicit CPU-reference-vs-CUDA D1/D2 hardware acceptance test:

- D1: exact ordered spike/event parity;
- D2: continuous state within the registered 1e-4 compatibility tolerance.

The hardware test remains opt-in through `MHRN_TEST_CUDA_HARDWARE=1`.

D3 is **not** declared complete by Wave 4. D3b/D3c require the Frozen
Environment contract and causal live environment trajectory comparison.

Execution fingerprints are intentionally backend-specific because backend name
and version are fingerprint inputs. Cross-backend equivalence is therefore
tested with D1/D2/D3, while the canonical configuration fingerprint remains the
shared configuration identity.

## Fail-closed CI gates

Wave 4 adds four durable gates:

1. canonical acceleration/verification code may not import Playground;
2. extracted CUDA kernel bytes must match their frozen Playground reference;
3. plasticity capability must expose its non-canonical draft semantics;
4. CPU-vs-CUDA D1/D2 parity is a named standalone hardware acceptance test.

## Evidence boundary

Wave 4 is Engineering Verification and architecture integration. It creates no
DATA, EVID, CPU/CUDA scientific-equivalence claim, performance-superiority
claim, PAN-validity claim or learning-validity claim.
