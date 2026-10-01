# Canonical ExecutionBackend Contract

Status: canonical engineering contract, Wave 3  
Date: 2026-09-29  
Scientific evidence: none created by this document

## Purpose

MHRN separates runtime control from the mechanism that advances neural state. The canonical ExecutionBackend protocol is defined in src/runtime/backend.py. RuntimeController decides when bounded work is allowed; an ExecutionBackend decides how that work is executed.

Wave 3 defined semantics before a canonical CUDA backend existed. Wave 4 now provides a bounded canonical CUDA reference under `src/acceleration/cuda/` while preserving this contract. The first facade is explicitly `BOUNDED_REPLAY_REFERENCE`; resident continuation state remains a later step.

## Required interface

Every conforming backend provides:

- initialize(config, seed)
- step(tick)
- run(ticks)
- snapshot()
- restore(state)
- capabilities()

The canonical value types are BackendCapabilities, BackendState, StepResult and RunResult.

## BackendState invariant

BackendState is backend-neutral continuation state.

It may contain canonical data such as:

- logical neuron and edge identities;
- scalar and array-like numeric state represented as serializable data;
- pending events, rewards and delay state;
- topology generation identifiers;
- deterministic RNG state or counter contract references;
- contract and state digests.

It must not contain:

- CUDA device pointers;
- CUDA contexts, modules, streams or kernel handles;
- Python object identities;
- wall-clock timestamps used as continuation state;
- UI state;
- Playground-only session identifiers.

The current contract enforces canonical JSON serializability at the boundary. Later binary storage may optimize representation, but the authoritative logical state must remain reconstructable without backend-local pointers.

## Capability declaration

BackendCapabilities declares bounded support for:

- recurrence;
- plasticity;
- PAN hyperstate;
- structural plasticity;
- maximum neuron count;
- maximum tick count;
- determinism under the declared contract.

Capability flags are declarations, not scientific validation. Optional capability metadata includes `max_edges`, `plasticity_semantics` and `execution_mode`; these fields make bounded or draft support explicit rather than implying full canonical semantics.

## Runtime relationship

The intended dependency direction is:

~~~text
RuntimeController
      |
ExecutionBackend protocol
   /        \
CPU         CUDA
   \        /
canonical state / parity / checkpoint contracts
~~~

MHRN core and runtime must not import Playground to satisfy this interface.

## Wave 4 implementation

Wave 4 extracts CUDA infrastructure without weakening the state, determinism, checkpoint or parity contracts. The detailed bounded backend contract is defined in [CUDA_BACKEND.md](CUDA_BACKEND.md).

Acceptance for a canonical CUDA backend requires at minimum:

1. backend-neutral snapshot and restore;
2. declared bounded capabilities;
3. canonical execution fingerprint;
4. D1/D2 parity using the canonical verifier;
5. D3a before D3b/D3c closed-loop work;
6. no silent CPU fallback labeled as CUDA execution.

## Evidence boundary

A backend satisfying this protocol demonstrates software-contract conformance only. It does not establish performance superiority, scientific equivalence, PAN validity or EVID.
