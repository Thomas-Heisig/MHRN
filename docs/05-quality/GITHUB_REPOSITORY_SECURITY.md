# GitHub Repository Security Baseline

**Repository:** `Thomas-Heisig/MHRN`  
**As of:** 20 September 2026  
**Purpose:** protect the canonical research repository from unauthorized or accidental history changes without locking out the single maintainer.

## Observed state

At the time this baseline was written:

- repository visibility: **public**;
- default branch: **`main`**;
- repository rulesets returned by GitHub: **none**;
- the connected automation cannot administer branch protection;
- release and research workflows exist that historically wrote metadata directly to `main`.

The GitHub-hosted merge commits inspected on 20 September 2026 are signed and verified, but ordinary API-created commits are not consistently signed. For that reason, **required signed commits are not part of the first protection step**.

## Required `main` ruleset

Create a repository ruleset named **Protect main** targeting `main` with:

- enforcement: **Active**;
- **Require a pull request before merging**;
- required approvals: **0** while Thomas Heisig is the sole maintainer;
- do **not** require Code Owner approval yet, because a sole author cannot approve their own pull request;
- **Require status checks to pass before merging**;
- required status checks for release PRs: **`ci-status`**, **`release-policy`**, and **`repository-health`**;
- require the branch to be up to date before merging;
- require conversation resolution before merging;
- **Block force pushes**;
- **Restrict deletions**.

Initially keep bypass limited to the repository administrator only. Do not grant a broad GitHub Actions bypass. Existing workflows that try to push directly to `main` should be treated as legacy writers and migrated to PR-based metadata updates before bypass is removed entirely.

## Release-tag protection

Create a second ruleset named **Protect release tags** targeting:

```text
v*
```

Enable:

- restrict updates;
- restrict deletions;
- block force pushes.

Published release tags are archival identifiers and should not silently move.

## Account security

Repository rules cannot protect against a compromised owner account. The maintainer account should therefore use:

- a passkey or strong two-factor authentication;
- offline recovery codes;
- periodic review of SSH keys;
- periodic review/removal of unused personal access tokens;
- periodic review of installed GitHub Apps and OAuth grants.

Do not store tokens or recovery data in the repository.

## Canonical change path

The protected workflow is:

```text
feature / fix / research branch
        ↓
Pull Request to develop
        ↓
CI + repository-health = green
        ↓
develop
        ↓
release/* branch
        ↓
Pull Request to main
        ↓
ci-status + release-policy + repository-health = green
        ↓
main
```

Direct pushes and force-pushes to `main` are not part of the protected workflow.

## Automation note

Historical workflows currently contain direct `main` writers, including release metadata and generated research-report jobs. The protection ruleset is expected to reject such direct writes unless explicitly bypassed. New automation must prefer:

```text
automation branch -> Pull Request -> required checks -> merge
```

rather than writing directly to `main`.

## CODEOWNERS

`.github/CODEOWNERS` identifies `@Thomas-Heisig` as the current human owner for the repository and sensitive research/publication paths. This provides ownership visibility now and allows Code Owner review to be enabled later if another independent maintainer/reviewer is added.

## Scientific reason for repository protection

MHRN uses commit hashes, source freezes, experiment provenance, release tags and publication manifests as parts of its scientific audit trail. Rewriting `main` or moving release tags can therefore damage scientific provenance even if the source code still runs.

Repository protection is consequently part of research integrity, not only software administration.
