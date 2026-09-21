## Purpose

<!-- What changes and why? -->

## Target branch

- [ ] Normal work targets `develop`
- [ ] This is a release PR from `release/*` to `main`

## Validation

- [ ] Tests added/updated where applicable
- [ ] Documentation updated where applicable
- [ ] `git diff --check` passes
- [ ] No generated/local scratch files are included
- [ ] CI / required checks are green before merge

## Scientific boundary

- [ ] This change does not silently promote DATA to EVID
- [ ] Human Review / independent replication status is preserved
- [ ] Claim boundaries remain consistent with the underlying experiments

## Release-only checks

Complete only for PRs to `main`:

- [ ] Head branch is `release/*`
- [ ] Release metadata is current
- [ ] Release notes match the source freeze
- [ ] Clean tracked tree
- [ ] CI and applicable integrity gates are green
