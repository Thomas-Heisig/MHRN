# Branching and Release Policy

**Effective:** 21 September 2026  
**Repository:** `Thomas-Heisig/MHRN`

## Purpose

MHRN uses `main` as a release line, not as a general development branch. This preserves a clean public state for visitors and keeps release commits, source freezes, publication metadata and scientific provenance easy to audit.

## Canonical branch model

```text
feature/*  fix/*  research/*  chore/*
                  ↓
               develop
                  ↓
              release/*
                  ↓
                 main
```

### `develop`

`develop` is the integration branch for ongoing work:

- engineering changes;
- research tooling;
- new experiments and protocols;
- documentation;
- publication drafts;
- frontend/dashboard changes;
- maintenance and cleanup.

Normal Pull Requests target `develop`.

### `release/*`

A `release/*` branch is cut from a green `develop` state when a public release is being prepared.

A release branch may contain only release preparation such as:

- version updates;
- release notes;
- citation and Zenodo metadata;
- final generated publication metadata;
- final compatibility fixes required for the release.

It must not become a parallel development branch.

### `main`

`main` is the public release line.

Only Pull Requests from `release/*` may target `main`.

Direct development on `main`, force pushes, history rewrites and unreviewed automation writes are outside project policy.

## Release readiness contract

A release may merge to `main` only when all applicable conditions are satisfied:

1. full Continuous Integration is green;
2. the aggregate `ci-status` job is green;
3. Release Policy is green;
4. scientific/publication integrity workflows relevant to the changed paths are green;
5. tracked working tree is clean;
6. no unresolved merge markers or generated drift;
7. release metadata is internally consistent;
8. release notes describe the actual source state;
9. DATA/EVID status is not promoted by release mechanics;
10. release tag and source-freeze commit are recorded after publication.

A release or DOI never substitutes for Human Review or independent replication.

## Emergency fixes

A production/release emergency starts from `main` on a branch such as:

```text
fix/hotfix-...
```

The fix is first merged into `develop`. A new `release/*` branch is then cut and follows the normal release gate back to `main`.

This prevents `develop` from silently missing hotfix history.

## Automation policy

Automation may generate artefacts or changes on `develop` or dedicated automation branches.

New automation must not write directly to `main`.

Preferred automation path:

```text
automation branch
       ↓
Pull Request to develop
       ↓
checks
       ↓
merge
```

Release automation may create tags/releases only after the exact source freeze has satisfied the release contract.

## Scientific provenance

MHRN uses source commits and release tags in experiment, publication and evidence provenance. Protecting `main` and release tags is therefore part of research integrity.

Historical experiment DATA, reviews and EVID artefacts are never rewritten merely to make a release cleaner.
