# Stage-1 TEMP-ORDER V2 execution-recovery record

**Date:** 2026-09-19  
**Experiment:** `EXP-S1-TEMP-ORDER-V2-20260919`

## First verified execution

The first GitHub Actions execution used source freeze `e711d5b4cf13df13915f3fcebf31db7611b5c591`.

The following gates completed successfully before persistence:

- existing Small-SNN contract regressions: **8 passed**;
- clean-tree source-freeze check: **PASS**;
- preregistered experiment execution: **PASS**;
- persisted-artifact verifier against the generated working-tree DATA: **PASS**.

The scientific output printed by the runner was:

- runs: **120**;
- status: `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`;
- intact order-accuracy median: **1.0**;
- identity-destroyed order-accuracy median: **0.0**;
- intact simultaneous-control success fraction: **1.0**;
- paired accuracy-delta median: **1.0**;
- bootstrap 95% CI: **[1.0, 1.0]**;
- exact paired sign-test: **p = 1.9073486328125e-06**;
- design integrity: **true**.

The workflow then created local DATA commit `3ac68917`, but its push was rejected as non-fast-forward because the remote branch had received a later workflow-definition commit while the run was executing. Therefore `3ac68917` was never the canonical remote DATA commit.

## Persistence-recovery execution

The pull-request execution then ran the unchanged registered scientific runner on source freeze `23549a0b75f7019a6146f8513bf6628505acb079`. The only intervening repository change relevant to the branch was CI trigger/persistence wiring; the preregistration and scientific runner were unchanged.

The second execution again passed the same regression, clean-tree, experiment and verifier gates and reproduced the same numerical result. Its DATA were persisted as commit:

`aed8e70f9cf227ac07bcec900fc916dcae3a243e`

This persisted execution is the canonical DATA instance for the experiment.

## Epistemic classification

The recovery execution is **not** counted as an independently authored replication and does not satisfy the independent-replication criterion. It is a same-code, same-protocol persistence recovery caused by a Git non-fast-forward race.

Human review remains `PENDING`. No EVID promotion is implied by either execution.
