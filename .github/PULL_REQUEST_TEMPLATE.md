# Pull Request

## Purpose

Describe the change and its motivation.

Fixes # (issue, if applicable)

## Target branch

- [ ] Normal feature/fix/research/chore work targets `develop`
- [ ] This is a release PR from `release/*` to `main`

## Type

- [ ] Bug fix
- [ ] New feature
- [ ] Refactor
- [ ] Test
- [ ] Documentation
- [ ] Tooling / CI
- [ ] Research / experiment
- [ ] Publication
- [ ] Release
- [ ] Breaking change

## Architecture impact

Describe affected boundaries and compatibility considerations.

## Verification

List the exact commands run and results.

- [ ] `pytest -m "not slow"`
- [ ] `mypy src`
- [ ] `black --check src tests scripts`
- [ ] `ruff check src/ tests/ scripts/`
- [ ] `pyright`
- [ ] Pyright/Pylance clean for changed/new files
- [ ] Pylint quality threshold maintained
- [ ] `git diff --check`
- [ ] Slow tests run when relevant
- [ ] No generated/local scratch files are included
- [ ] CI / required checks are green before merge

## Persistence / safety checklist

- [ ] Restore determinism is unchanged or explicitly tested
- [ ] Structural changes still pass through controlled mutation boundaries
- [ ] Auto-approval defaults remain conservative
- [ ] No arbitrary shell command path was added to the dashboard
- [ ] No new broad type suppressions were introduced

## Scientific boundary

- [ ] This change does not silently promote DATA to EVID
- [ ] Human Review / independent replication status is preserved
- [ ] Claim boundaries remain consistent with the underlying experiments
- [ ] Negative/null results and historical provenance remain intact

## Documentation

- [ ] README updated if user-visible behavior changed
- [ ] User Guide updated if operator workflow changed
- [ ] Developer Guide / architecture docs updated if contracts changed

## Release-only checks

Complete only for PRs to `main`:

- [ ] Head branch is `release/*`
- [ ] Release metadata is current
- [ ] Release notes match the source freeze
- [ ] Repository Health / clean-tree gate is green
- [ ] `ci-status` is green
- [ ] Applicable scientific/publication integrity gates are green
