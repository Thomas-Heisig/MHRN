# EXP-S6-SEM-CL-002 — Methods, provenance and deviations

## Frozen research chain

1. Base preregistration merged before runner implementation.
2. Amendment A1 resolved prototype construction, random-control matching, realized memory budget, replay accounting and aborted-seed policy before empirical execution.
3. Runner and analysis code were implemented and tested only on synthetic data.
4. Seven transitively relevant source/protocol files were bound by SHA-256.
5. A freeze attestation documented 19 passing synthetic tests, successful unauthorized-execution blocking, manifest generation, Black and Ruff checks.
6. A separate authorization allowed one empirical Split-MNIST run.
7. The empirical workflow verified the frozen hashes before loading MNIST.
8. All 36 seed×condition runs completed and DATA were persisted independent of outcome.
9. Human project EVID review occurred only after DATA had been merged to `main`.

## Dataset identity

Canonical MNIST files were recorded as:

- train images: `440fcabf73cc546fa21475e81ea370265605f56be210a4024d2ca8f203523609`
- train labels: `3552534a0a558bbed6aed32b30c495cca23d567ec52cac8be1a0730e8010255c`
- test images: `8d422c7b0a1c1c79245a5bcf07fe86e33eeafee792b84584aec276f5a2dbc4e6`
- test labels: `f7ae60f92e00ec6debd23a6088c31dbd2371eca3ffa0defaefb259924204aec6`

## Frozen sources

The execution manifest bound:

- operational preregistration,
- preregistration amendment A1,
- CL-002 runner entrypoint,
- CL-002 analysis/control implementation,
- inherited CL-001 encoding/readout implementation,
- `SemanticMemory`,
- neural episodic representation.

Exact hashes are stored in `research/preregistrations/frozen/EXP-S6-SEM-CL-002-FREEZE.json` and repeated in the authorization record.

## Protocol deviations

### Pre-execution amendment

The original preregistration contained underdetermined implementation details. These were not silently resolved in code. Amendment A1 was merged before runner implementation and before any empirical CL-002 data access. It clarified:

- the exact existing semantic-prototype construction;
- that N=50 is a per-task capacity ceiling rather than forced occupancy;
- realized object-count matching across B2/B3/B4;
- exact random-prototype matching and RNG derivation;
- exact interpretation of K=100 replay updates per transition;
- seed-abort handling.

This is a documented pre-execution clarification, not a post-hoc analytic deviation.

### Freeze-workflow git push race

During the pre-execution freeze workflow, all scientifically relevant checks passed: 19 synthetic tests, unauthorized-run blocking, freeze-manifest generation, Black and Ruff. The final workflow step that attempted to push the normalized sources/manifest encountered a non-fast-forward race because a parallel update had already committed those normalized files. The resulting committed branch contained the same frozen sources and manifest and was subsequently merged. This infrastructure race is recorded in `EXP-S6-SEM-CL-002-ATTESTATION.json`; it did not expose empirical data or alter protocol/statistical decisions.

## Empirical execution deviations

**None observed.**

- all nine seeds completed;
- all four conditions completed for every seed;
- no seed replacement occurred;
- no NaN/Inf abort occurred;
- no endpoint, threshold or test was changed after data access;
- no confirmatory rerun was performed;
- the first authorized empirical run was the reported run.

## Evidence boundary

The machine-generated report remained DATA-only. Human project EVID was created afterward and preserves the preregistered negative decision. This publication is not an independent external replication or peer review.
