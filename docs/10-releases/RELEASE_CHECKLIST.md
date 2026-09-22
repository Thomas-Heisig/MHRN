# MHRN Release Checklist

Use this checklist only on a `release/*` branch created from a green `develop` commit.

## 1. Freeze candidate

- [ ] `develop` CI is green.
- [ ] Repository Health Gate is green.
- [ ] Working tree is clean.
- [ ] Candidate commit is recorded.
- [ ] No unresolved experimental output or local scratch files are included.

## 2. Version and metadata

- [ ] `pyproject.toml` version is correct.
- [ ] `src/version.py` is correct.
- [ ] root `CITATION.cff` identifies the software release correctly.
- [ ] `.zenodo.json` is correct for the software archive.
- [ ] `codemeta.json` is aligned.
- [ ] `releases/current.json` is a release candidate for the intended tag.
- [ ] release notes describe only work actually present in the candidate.

## 3. Scientific boundary

- [ ] No DATA status was silently promoted to EVID.
- [ ] Human Review state is unchanged unless a real human review artefact exists.
- [ ] Independent replication is not inferred from internal replication.
- [ ] DOI/release publication is not described as peer review or scientific validation.
- [ ] Negative and null results remain visible.

## 4. Release PR

Open:

```text
release/<version> -> main
```

Required before merge:

- [ ] Release Policy = green.
- [ ] Continuous Integration / `ci-status` = green.
- [ ] Repository Health Gate = green.
- [ ] Publication / scientific integrity checks relevant to the changed paths = green.
- [ ] conversations resolved.
- [ ] no force push or history rewrite.

## 5. Publish

After the exact release PR commit has merged to `main`:

- [ ] create immutable `v*` tag on the exact source-freeze commit;
- [ ] create GitHub Release;
- [ ] verify release assets and notes;
- [ ] verify Zenodo ingestion if enabled;
- [ ] record the concrete DOI only after it publicly resolves;
- [ ] update release metadata through the next normal development/release cycle if an external identifier arrives later.

## 6. Post-release

- [ ] `main` remains clean and contains no unreleased development.
- [ ] `develop` contains all release/hotfix history.
- [ ] no stale `release/*` branch is reused for future development.
- [ ] public README/release badges resolve correctly.

A green release is an engineering/publication state. It is not an automatic scientific EVID decision.
