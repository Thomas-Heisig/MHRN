# Governance Decision: Wave 6 first governed structural run

**Decision ID:** `DEC-WAVE6-FIRST-RUN-MANUAL-20261001`  
**Date:** 2026-10-01  
**Status:** accepted governance selection; execution not authorized  
**Contract:** `mhrn-structural-approval-v0.1`

## Decision

The first future governed structural-plasticity run will use `ApprovalMode.MANUAL_ONLY`.

The system default remains `DISABLED`. This decision does not enable structural mutation and does not satisfy the independent hard gates by itself.

## Rationale

`MANUAL_ONLY` is selected for the first governed run because it permits direct inspection of proposals and journal/undo behavior without introducing an unreviewed automatic approval policy.

`POLICY_AUTO` remains deferred until the policy has its own validation. `PREREGISTERED_AUTO` remains deferred until an exact policy artifact is frozen inside a preregistered structural study.

## Preconditions before execution authorization

1. exact structural config is frozen;
2. policy artifact hash is recorded;
3. manual authorization is explicitly recorded;
4. topology changes are permitted by the study/protocol;
5. structural barrier is available;
6. journal and undo path are healthy;
7. scientific freeze permits the mutation;
8. normal safety/resource/cooldown/kind checks pass.

No CUDA in-kernel structural mutation is authorized by this decision.

## Separation from first CPU preregistration

`PREREG-CPU-PAR-001` is intentionally executed with structural approval `DISABLED`. The self-parity study must not conflate CPU determinism with topology adaptation.

## Evidence boundary

This is a governance/method decision, not DATA, EVID or a structural-plasticity effect claim.
