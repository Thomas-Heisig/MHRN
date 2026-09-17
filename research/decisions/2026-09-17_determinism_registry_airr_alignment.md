# Determinism registry and AIRR semantic alignment

**Date:** 2026-09-17
**Status:** accepted implementation decision
**Scope:** `RQ-SNN-002`, `RQ-DET-001`, AIRR confidence gating

## Decision

Historical experiment provenance is immutable. `EXP-BATCH-20260914074039-02` therefore remains registered as `RQ-SNN-002`; its observed condition `same_seed_tonic_replica_pair` remains a semantic mismatch for that historical registration and is not post-hoc promoted. Its technical result can be cited as a determinism diagnostic only with the mismatch/provenance limitation attached.

`RQ-DET-001` now has an explicit deterministic semantic contract. It accepts either `same_seed_tonic_replica_pair` for isolated same-seed/same-input replica tests or the four explicit `recurrence_*_replica_a/b` conditions used by `deterministic_replica_v1`. This resolves the prior `NOT_AUTOMATICALLY_CLASSIFIED` state without rewriting old manifests.

`RQ-SNN-002` retains the current registry condition contract `recurrence_off` + `recurrence_on`. The clean existing run `EXP-SNN-002-R2` already satisfies this contract with ten seeds. No duplicate rerun is created merely to repair the registry/pipeline bug.

## AIRR rule

AIRR remains interpretation-only. In addition, the public/report-level `ai_confidence` is deterministically forced to `0.0` whenever semantic alignment is `MISMATCH`. The model's original self-confidence remains available only inside the append-only AIAR record for auditability. This prevents a high model self-rating from visually contradicting a hard semantic evidence block.

## Scope boundary

`tonic_spike_reproducibility_v1` is an isolated-neuron test. Summaries generated for this protocol explicitly state that the result is not a network-level finding. Runtime from such a run must not be used as network-performance evidence.

## Remaining scientific boundary

The existing `RQ-DET-001` batch artifact was produced from a dirty source tree. After semantic reclassification it may become a direct semantic match, but that does not remove the provenance block. A future clean-tree rerun is required before evidence promotion under the normal human-review/freeze rules.

The wording of `RQ-SNN-002` (constant-input neuron reproducibility) and its current recurrence-based operational contract are not perfectly isomorphic. This decision does not silently rewrite the research question. A future registry version may split isolated tonic reproducibility from network recurrence reproducibility explicitly; such a change must be preregistered rather than retrofitted to historical runs.
