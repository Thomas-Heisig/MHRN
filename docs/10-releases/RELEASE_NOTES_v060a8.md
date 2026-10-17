# MHRN v0.6.0-alpha.8

**Status:** release candidate; not published until the release PR and exact
post-merge `main` CI/source-freeze gates are green.

Alpha.8 is an integration and maintenance pre-release. It publishes the green
`develop` state accumulated after alpha.7. It is a software pre-release, not a
claim that the scientific programme is complete.

> Naming note: the legacy "Alpha.8" label in
> `TODO_ALPHA8_RECURSIVE_LOOPBACKS.md` comes from the v0.5 line and refers to
> the recursive causal loopback programme. That programme is **not** part of
> this release and remains unimplemented.

## Included

- Plastic-gateway activation validation: activation requires a `protocol_id`
  and an explicit `research_source`; gateway-registry guard documentation.
- Bounded cognition raw-run viewer in the File Viewer: at most 100 indexed
  runs, previews only for matching SHA-256 entries, backend decompression
  capped at 256 KiB. Raw runs stay read-only DATA.
- Stage-3 plastic-network benchmark provenance: source SHA-256 digests,
  mechanism details and a functional-stability assessment. Results remain
  engineering observations.
- Dependency refresh (`fastapi>=0.143`, `uvicorn>=0.54`, dev dependency
  groups) and the Python 3.13 full-suite CI matrix.
- Restored strict pyright compliance on `develop` (raw-run index typing) and
  black/lint fixes.
- `OPEN_SCIENCE.md` aligned with the verified alpha.7 Zenodo archive.
- Manuscript-review follow-up tasks (17 October 2026) recorded as open TODOs:
  clean-tree determinism replication, memory-compression decision rule,
  yoked `H-EMB-001-B` comparison, matched 5D ablation, independent prior-art
  review and an explanation of maturity percentages.

## Evidence and release boundaries

- No DATA, Human Review, EVID, scientific-maturity or replication state is
  changed by this release. No evidence is automatically promoted.
- Implementation, passing CI, DATA, Human Review, accepted EVID and independent
  replication remain distinct states.
- Alpha.7 (`10.5281/zenodo.23138847`) is the latest published and verified
  archive at preparation time. Alpha.8 archival and DOI are pending the actual
  GitHub release and external archive verification.

## Connected publication routes

- GitHub `main` is canonical. Hugging Face mirrors update through the
  configured `sync-huggingface.yml` workflow after `main` updates.
- Zenodo is connected to GitHub software releases (concept DOI
  `10.5281/zenodo.22860682`).
- OSF and ORCID are linked identity routes without automatic release-update
  workflows. No institution-specific endpoint is registered.

## Provenance

- Integration PR: #282, merged to `develop` at
  `343d1634e24a30b34dc0fdf5cdca10186a9dba0c` with all checks green.
- Named release branch: `release/v0.6.0-alpha.8`.
- Source-freeze commit, tag, GitHub release URL and Zenodo DOI remain unset
  until their respective gates complete.

AI systems materially assisted with software, tests, debugging and release
preparation. Thomas Heisig remains the human author and release authority.
