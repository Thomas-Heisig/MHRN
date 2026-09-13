# Stage 2 — Stable Recurrent SNN Contract

## Purpose

Stage 2 verifies the engineering mechanics required for a deterministic recurrent spiking network: explicit feedback connectivity, sustained bounded spike/event propagation, long deterministic replay, and restart/restore continuity.

This stage is an **engineering verification boundary**, not a scientific evidence promotion. Passing it does not imply cognition, consciousness, biological equivalence, or stability for arbitrary recurrent systems.

## Deterministic reference topology

The scoped software reference is a four-cell directed ring:

`A -> B -> C -> D -> A`

Reference parameters:

- neuron model: `izhikevich-2003`
- isolated reference neuron configuration; adaptive secondary mechanisms disabled
- four neurons / four synapses
- synaptic delay: `1` tick
- reference weight: `200.0`
- deterministic seed: `23`
- long-run verification: `20,000` ticks
- initial condition: cell A starts at the spike threshold

The deliberately strong weight belongs only to the reference contract and does not modify production defaults.

## Required proofs

The Stage-2 reference test must establish all of the following:

1. The topology is an explicit closed recurrent ring.
2. Exactly one reference spike is propagated per tick after priming.
3. Event-queue depth remains bounded at one event.
4. Membrane summary values stay finite and within the contract's broad numerical guardrails.
5. A 20,000-tick run completes without queue drift or numerical failure.
6. A second independently constructed network produces the same deterministic tick projection and identical serialized state.
7. Existing restart/restore verification remains independently represented by `restore_determinism.json`.

## Relationship to RQ-SNN-001

`RQ-SNN-001` already has a registered experiment (`EXP-BATCH-20260908200906-01`) with 20 runs of 100,000 ticks under control/treatment conditions. That experiment provides DATA and deterministic statistics for scientific analysis.

The Stage-2 reference contract serves a different purpose: it closes the software-verification gap that previously left the development timeline at 94%. It must not automatically promote the experimental DATA to scientific EVID.

## Limits

- The reference network is intentionally tiny relative to the Stage-2 target scale of 1,000–10,000 neurons.
- Stability of this ring does not establish stability for arbitrary topology, delay, weight, model, plasticity, or external drive.
- Target-scale runtime performance remains a separate benchmark question.
- Deterministic sustained activity is not evidence of cognition.

## Completion rule

Stage 2 is technically complete when the repository contains the contract test, the scoped verification artifact, restart/restore verification, a registered long-run protocol, and the Release timeline resolves every Stage-2 criterion as implemented/verified. Scientific readiness remains separately scored.
