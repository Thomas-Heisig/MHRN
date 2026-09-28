# MHRN Frozen Environment Contract v0.1

**Status:** canonical design contract  
**Required before:** CUDA-1.6 live closed-loop parity  
**Scientific evidence:** none created by this document

## Purpose

A "frozen environment" must identify exactly which causal inputs are replayed and which components are still allowed to evolve. Otherwise D3 can be satisfied by construction without testing the backend boundary.

## Contract id

```text
frozen_environment_contract_id = mhrn-frozen-environment-v1
```

## Environment layers

The closed loop is decomposed into:

```text
source/sensor state
  -> BoundaryFrame
  -> codec / SpikeFrame
  -> SNN backend
  -> DecodeResult / action
  -> actuator transform
  -> body/world transition
  -> next sensor state
  -> reward computation
```

Freezing is declared per layer.

## Required frozen artifacts

A frozen-environment manifest records:

- initial world/body state;
- environment implementation/version/artifact hash;
- environment parameter/config hash;
- world RNG algorithm/version/state or counter contract;
- sensor sampling schedule;
- canonical BoundaryFrame sequence when sensor replay is frozen;
- actuator/action schema;
- action-to-transition mapping version;
- reward-function version and parameter hash;
- episode start/stop/reset semantics;
- external disturbances and their ticks;
- all content hashes required for replay.

## Freeze modes

### FE-1: Boundary replay

Inputs are predetermined as canonical BoundaryFrames.

The neural backend cannot affect future observations.

Use for isolated encoder/network/decoder parity.

### FE-2: Frozen world with live actions

Initial state, dynamics, RNG and reward function are frozen, but actions are produced live by the tested backend and drive the world.

This is the first meaningful causal D3 test.

### FE-3: Full deterministic live loop

Sensors are generated from the evolving frozen world state; actions, body/world transitions, observations and rewards all emerge causally.

This is the target D3c trajectory-parity mode.

A frozen action sequence or frozen reward sequence is a diagnostic control only and is not FE-2/FE-3.

## World RNG

A seed alone is insufficient.

The manifest records either:

```text
algorithm + version + complete state
```

or a counter-based contract:

```text
(world_seed, episode, tick, stream, index)
```

The environment must not consume hidden scheduling-dependent random draws.

## Canonical trajectory record

For each environment tick:

```text
tick
pre_state_hash
boundary_frame_hashes
decoder/action hash
post_action_state_hash
reward record/hash
post_state_hash
world_rng_fingerprint
```

D3c compares the ordered trajectory records, not only aggregate success rate.

## Reset and episode boundaries

Reset is a first-class state transition.

The contract defines:

- whether network learning state resets;
- whether codec stream state resets;
- whether world RNG resets or advances;
- whether pending rewards/events cross the episode boundary;
- target/cue reset semantics.

No component may infer a reset from wall-clock/UI events.

## Fail-closed rules

Reject the run if:

- a required frozen artifact hash differs;
- a BoundaryFrame is missing, duplicated or reordered;
- action schema/version differs;
- environment RNG provenance is incomplete;
- reward function/config differs;
- hidden wall-clock or nondeterministic external input enters an FE-2/FE-3 run.

## CUDA-1.6 sequence

CUDA-1.6 proceeds in this order:

1. FE-1 boundary replay, learning off;
2. FE-1 boundary replay, canonical learning on;
3. FE-2 frozen world with live backend actions;
4. FE-3 full deterministic live loop;
5. only after parity, scientific behavioral experiments.
