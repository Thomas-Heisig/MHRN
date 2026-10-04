# MHRN v0.6.0-alpha.7

**Status:** release candidate; not published until the release PR and exact
post-merge `main` CI/source-freeze gates are green.

Alpha.7 consolidates the governed Stage-0/Stage-1 evidence state, the current
research-software and manuscript infrastructure, and the experimental
Playground/PAN/CUDA preflight work. It is a software pre-release, not a claim
that the scientific programme is complete.

## Included

- v0.6 runtime, storage, determinism, migration, performance-budget and
  reproducibility contracts.
- Scoped Stage-0/Stage-1 records `EVID-2026-18`, `EVID-2026-19`, and
  `EVID-2026-20`, retaining their declared limits and separate replication
  requirements.
- Playground research tools, PAN and closed-loop experiments, and CUDA/PTX
  compilation/preflight/parity diagnostics. No completed equivalent CUDA SNN
  backend is claimed.
- Publication 1.8 as WIP, with the October findings synthesis, source-bound
  failed-run treatment, conceptual-audit boundaries and explicit unresolved
  human reviews.
- A Stage-3 plastic-network engineering benchmark with matched asymmetric,
  symmetric and learning-off profiles. Its lower/intermediate scale results
  are engineering observations; the 100k-neuron/10M-synapse upper point remains
  unmeasured.

## Evidence and release boundaries

- Implementation, passing CI, DATA, Human Review, accepted EVID and independent
  replication remain distinct states. No evidence is automatically promoted.
- The remaining `EXP-GEN-0041` and `EXP-S6-SEM-CL-003` human reviews,
  confirmatory R2 productive-learning evaluation, and independent replication
  are not closed by this software release.
- Alpha.7 remains a release candidate until the exact release PR, post-merge
  main CI, source-freeze record and tag are verified.
- Alpha.6 is the latest published software archive at preparation time.
  Alpha.7 Zenodo archival and DOI are pending the actual GitHub release and
  external archive verification.

## Connected publication routes

- GitHub `main` is canonical. Hugging Face source/Space/research-data mirrors
  update through the configured `sync-huggingface.yml` workflow after main
  updates.
- Zenodo is connected to GitHub software releases. Alpha.6 is the last
  verified archive; Alpha.7 is not yet archived.
- OSF and ORCID are linked project/researcher identity routes. The repository
  has no automatic OSF or ORCID release-update workflow.
- No institutional account or institution-specific update endpoint is
  registered. No institutional notification is implied by this candidate.

## Provenance

- Release integration PR: #269, merged to `main` at `4a6eb9887255ebb2ede0a5f2e13460c4b5878946`.
- Named release branch: `release/v0.6.0-alpha.7`.
- Source-freeze commit, tag, GitHub release URL and Zenodo DOI remain unset
  until their respective gates complete.

AI systems materially assisted with research leads, critique, software, tests,
debugging and manuscript preparation. Thomas Heisig remains the human author
and release authority.
