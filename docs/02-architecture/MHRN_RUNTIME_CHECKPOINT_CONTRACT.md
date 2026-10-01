# MHRN Canonical Runtime Checkpoint Contract v0.1

**Status:** canonical design contract extending the existing typed RuntimeCheckpoint/RuntimeBundle path  
**Scientific evidence:** none created by this document

## Purpose

Backend interchangeability requires more than serializing membrane voltages and weights. A checkpoint must preserve every continuation-critical state whose omission could change a future trajectory.

This document does not replace `src/storage/checkpoint.py` or `src/storage/runtime_bundle.py`; it defines the complete target surface they must expose before canonical CUDA execution.

## Contract id

```text
checkpoint_contract_id = mhrn-runtime-checkpoint-v5-target
```

The concrete schema version remains implementation-controlled until migration code and tests exist.

## Required state families

### Network/core

- current tick and counters;
- canonical neuron state;
- canonical synapse state;
- stable neuron and edge identities;
- input/output population membership;
- topology generation/version.

### Pending causal state

- pending synaptic events;
- delay ring/queue contents including already emitted amplitudes;
- pending external currents;
- pending reward records;
- pending action/decoder outputs where they can affect continuation.

### Learning

- last pre/post spike times;
- eligibility traces;
- STP resource/facilitation state when enabled;
- learning parameter/contract hash;
- learning RNG state/counter contract;
- any episode-local learning state required for exact continuation.

### PAN/tissue sidecars

- all continuation-critical PAN/tissue fields;
- sidecar schema versions;
- mapping from logical identities to packed physical slots/edge slots.

### Neural I/O

- active BoundaryFrame/SpikeFrame causal references as required;
- CodecStreamState;
- scheduler/refractory state;
- PopulationLayout and CodecContract hashes;
- active readout window state where continuation depends on it.

### Environment/embodiment

For closed-loop checkpoints:

- world/body state;
- environment contract/config hash;
- world RNG state/counter fingerprint;
- episode/reset state;
- reward-function identity/config.

### Execution provenance

- backend id/version;
- kernel/module artifact hash;
- precision profile;
- schedule/reduction versions;
- compiler/runtime/driver/device fingerprint where required by the determinism class;
- topology generation;
- canonical contract hashes.

## Round-trip invariants

A pack/unpack cycle without simulation must satisfy:

```text
canonical_state_hash_before == canonical_state_hash_after
```

for every state family in scope.

A continuation test must additionally satisfy:

```text
uninterrupted_run_suffix == restore_then_continue_suffix
```

under the declared determinism contract.

## Backend-neutral checkpoint

A canonical checkpoint is not a dump of raw CUDA addresses or implementation-specific buffers.

Packed GPU layouts may be stored as optional cache/acceleration artifacts, but the authoritative checkpoint must reconstruct a valid canonical state for another conforming backend.

## Migration

Every breaking schema change requires:

- explicit source schema;
- explicit target schema;
- migration artifact/version;
- migration provenance;
- tests for idempotence where applicable;
- no silent defaulting of continuation-critical state.

## CUDA promotion gate

CUDA cannot be considered a normal canonical ExecutionBackend until checkpoint/restore covers the recurrent, learning, Neural-I/O and environment state actually active in the experiment.
