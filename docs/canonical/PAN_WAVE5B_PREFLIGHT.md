# PAN Wave 5B Preflight

**Status:** engineering preflight ready; execution blocked  
**Scientific evidence:** none created by this document  
**Integration claim:** none

## Purpose

Wave 5B prepares the first canonical PAN CPU/CUDA equivalence gate without
promoting the existing Playground PAN implementation. The preflight is
deliberately executable only as validation of contracts and manifests; it does
not execute CUDA.

The authoritative preflight artifact is:

`research/verification/pan/PAN_WAVE5B_PREFLIGHT_V1.json`

The corresponding pure comparison semantics live in:

- `src/homeostasis/pan_contract.py` — current PAN semantic draft;
- `src/homeostasis/pan_parity_contract.py` — backend-neutral D2 comparison;
- `src/homeostasis/pan_wave5b_preflight.py` — fail-closed readiness projection.

## Current gate state

At the Wave-5B preflight revision:

- PAN semantic contract: `DRAFT_NOT_FROZEN`;
- PAN parity contract: `DRAFT_PREFLIGHT`;
- FE-3 software manifest: versioned and self-verifying;
- physical RTX-3060 FE-3 acceptance: required and not inferred from CI;
- explicit Wave-5B execution authorization: required and absent;
- PAN canonical integration: **not claimed**;
- DATA / EVID / CLAIM: **not created**.

A valid preflight therefore may report `preflight_ready=true` while
`ready_for_execution=false`. This distinction is intentional.

## D2 comparison surface

The draft PAN parity contract compares continuation-critical PAN state:

- exact: `pan_alive`, `pan_neuron_id`;
- numeric: health, amplitude, energy, activity EMA, consolidation,
  information proxy and the hyperstate vector;
- engineering absolute tolerance: `1e-12`;
- any non-finite state fails closed.

The tolerance is an engineering acceptance value derived from the current
reference tests. It is not a scientific equivalence margin and does not
constitute preregistration.

## D3c requirement

Wave 5B also requires exact causal Frozen-Environment trajectory parity after
canonical PAN CUDA integration. The existing FE-3 contract remains the
environment authority; Wave 5B does not introduce a second world model or a
second closed-loop semantics.

## Required gates before execution

Execution may only be authorized when all of the following are true:

1. the PAN semantic contract is explicitly reviewed and frozen;
2. the reviewed physical hardware report is from an RTX-3060-class reference
   host and has `passed=true` and `full_fe3_accepted=true`;
3. the FE-3 manifest hash matches the preflight manifest;
4. an explicit source-bound `PAN_WAVE5B_AUTHORIZATION.json` authorizes the
   exact preflight manifest digest.

A physical FE-3 pass alone does **not** bypass the PAN contract freeze.

## Existing Playground CUDA PAN path

The repository already contains exploratory Playground CUDA PAN state,
feedback and hardware-opt-in parity tests. They are valuable implementation
references, but they are not automatically canonical MHRN PAN semantics.
Wave 5B must consume the frozen canonical contract rather than promoting the
Playground implementation by location or historical success.

## Dependency boundary

Canonical Wave-5B modules must not import `src.playground`. The direction
remains:

```text
Playground -> canonical MHRN contracts
canonical MHRN -/-> Playground
```

## What can proceed in parallel

The physical RTX run is the next execution blocker for FE-3/PAN integration,
not the only remaining project task. Wave-6 structural-barrier design and the
Wave-7 learning/synapse contract may be prepared independently, provided they
make no CUDA/PAN integration claim before their own gates are satisfied.

## Interpretation boundary

Passing the future Wave-5B engineering parity gate would establish only a
bounded CPU/CUDA implementation-equivalence result for the frozen PAN
contract. It would not establish biological validity, cognitive capability,
scientific DATA/EVID, superiority, or a speedup claim.
