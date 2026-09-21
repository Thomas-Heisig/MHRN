# MHRN Git Workflow

**Effective:** 21 September 2026  
**Repository:** `Thomas-Heisig/MHRN`

MHRN uses a release-oriented branch model. The public `main` branch is not a general development branch.

## Branch model

```text
feature/*  fix/*  research/*  chore/*
                  ↓
               develop
                  ↓
              release/*
                  ↓
                 main
```

- `develop` is the active integration branch.
- Normal engineering, research, documentation and publication work targets `develop`.
- `main` contains only release-ready public states.
- Only `release/*` pull requests may target `main`.
- Direct pushes, force-pushes and history rewrites of `main` are outside project policy.

## Start normal work

```bash
git fetch origin
git switch develop
git pull --ff-only origin develop
git switch -c feature/short-description
```

Use a more specific prefix when appropriate:

```text
feature/
fix/
research/
chore/
docs/
```

## Commit and publish the working branch

```bash
git status
git diff
git add -A
git diff --staged
git commit -m "feat: describe the change"
git push -u origin feature/short-description
```

Open a Pull Request to **`develop`**.

Before merge:

- CI must be green;
- Repository Health / clean-tree must be green;
- applicable scientific or publication integrity checks must be green;
- unresolved review conversations must be resolved;
- no local scratch, generated drift or secrets may be committed.

## Keep a working branch current

```bash
git fetch origin
git rebase origin/develop
```

If the branch is already public and rebasing would rewrite shared history, prefer merging `origin/develop` or open a fresh branch. Do not rewrite `main`.

## Release preparation

A public release starts only from a green `develop` commit:

```bash
git fetch origin
git switch develop
git pull --ff-only origin develop
git switch -c release/vX.Y.Z
```

The release branch may contain only release preparation, such as:

- version metadata;
- release notes;
- citation metadata;
- Zenodo/software archive metadata;
- final compatibility fixes required for that release.

Open:

```text
release/vX.Y.Z -> main
```

The Release Policy workflow rejects ordinary branches targeting `main`.

Follow the canonical checklist:

[Release checklist](../10-releases/RELEASE_CHECKLIST.md)

## Release gate

A release PR may merge only when:

1. full CI is green;
2. `ci-status` is green;
3. Release Policy is green;
4. Repository Health / clean tree is green;
5. applicable scientific/publication integrity checks are green;
6. release metadata and release notes match the exact source state;
7. DATA/EVID, Human Review and replication status remain scientifically correct.

A software release, DOI or green CI is not an EVID promotion.

## Hotfixes

Start from the released state when diagnosing a release problem, but integrate the fix back through `develop` first.

Preferred path:

```text
main
  ↓
fix/hotfix-...
  ↓
develop
  ↓
release/<next-patch-or-alpha>
  ↓
main
```

This keeps `develop` from losing release-history fixes.

## Reverting a released change

Do not rewrite released history. Use a new revert/fix branch:

```bash
git switch -c fix/revert-description origin/develop
git revert <commit>
git push -u origin fix/revert-description
```

Then follow the normal PR and release path.

## Tags

Published `v*` tags are immutable release identifiers.

Do not:

```bash
git tag -f ...
git push --force ...
git push origin --delete v...
```

If a release is wrong, publish a corrected subsequent release instead of moving the published tag.

## Local safety checks

Useful checks before pushing:

```bash
git status
git diff --check
python -m pytest -m "not slow"
python -m mypy src/
python -m pyright
python -m black --check src tests scripts
python -m ruff check src tests scripts
```

CI remains authoritative for the repository-wide release gate.

## Repository authority

- Source/research integration: `develop`
- Public release line: `main`
- Release metadata: `releases/current.json`
- Branch policy: `docs/00-governance/BRANCHING_AND_RELEASE_POLICY.md`
- Release checklist: `docs/10-releases/RELEASE_CHECKLIST.md`
- Scientific state: `research/CURRENT_SCIENTIFIC_STATE.md`

Historical Git instructions remain recoverable from repository history but are no longer active project guidance.
