# MHRN Frozen Environment Contract v0.1

**Status:** executable canonical engineering contract; physical CPU/CUDA D3 pending  
**Required before:** scientific use of live cross-backend closed-loop parity  
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


## Executable implementation status — 2026-09-30

The canonical runtime contract is implemented in
`src/experience/frozen_environment.py`. Verification and artifact handling
live in `src/verification/frozen_environment/`; they import the runtime
contract and the canonical parity framework rather than defining a second
environment semantics.

The current executable ladder is:

1. **FE-1 / integrity:** exact BoundaryFrame payload/hash validation and ordered
   replay.
2. **FE-2 / repeated replay:** at least ten repetitions can be required to
   produce an identical canonical trajectory digest.
3. **FE-3 / CPU self-control:** two independently constructed deterministic
   world sessions are compared through
   `src.verification.parity.exact_frozen_environment_parity` as D3c.
4. **FE-3 / CPU vs CUDA:** remains **PENDING** until the canonical CUDA backend
   is connected to a physical closed-loop action adapter.

The CLI tools are:

```text
python scripts/build_frozen_environment.py --mode FE-1 --output /tmp/fe1.json
python scripts/run_fe_acceptance.py --manifest /tmp/fe1.json

python scripts/build_frozen_environment.py --mode FE-3 --output /tmp/fe3.json
python scripts/run_fe_acceptance.py --manifest /tmp/fe3.json --repeats 10
```

A dedicated `fe-contracts` CI job runs contract tests, artifact round trips,
FE-1 acceptance and FE-3 CPU/self acceptance. It is part of the global CI
summary.

### Claim boundary

These checks are **Engineering Verification**. A green FE-3 CPU/self control
shows that the frozen-environment and D3 comparison plumbing are internally
consistent; it does not show CPU/CUDA equivalence, PAN validity, learning
validity, behavioral superiority, or scientific support for a biological
claim. Physical CPU/CUDA D3 must be executed separately and a later scientific
experiment still requires its own preregistration, source freeze and review.


## Physical CUDA acceptance bridge — 2026-09-30

The canonical hardware runner now accepts `--include-fe3`. This adds the
existing physical live Builder CPU/CUDA D3c comparison to the same RTX-class
acceptance invocation used for Wave-4 D1/D2.

This is deliberately classified as a **Builder D3c bridge**, not as completed
Frozen-Environment FE-3. The Builder path has a live CPU world and compares
CPU/CUDA actions, targets, rewards and full body-trajectory digests through the
canonical parity framework, but it does not execute from a
`FrozenEnvironmentManifest` through a canonical per-tick backend adapter.

Therefore the authoritative status remains:

```text
Wave-4 physical D1/D2                  executable
Builder live CPU/CUDA D3c bridge       executable on physical CUDA
FrozenEnvironment FE-3 CPU/CUDA D3c    PENDING_LIVE_BACKEND_ADAPTER
```

The hardware command is:

```bash
python scripts/run_cuda_hardware_acceptance.py \
  --require-gpu "RTX 3060" \
  --full \
  --include-fe3
```

The resulting report always contains
`full_fe3_accepted=false` until the missing canonical live adapter exists.
