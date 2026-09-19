# REC-002 clean R2 execution audit

Date: 2026-09-19

Experiment: `EXP-REC-002-CLEAN-R2-20260919`  
Research question: `RQ-REC-002`  
Hypothesis: `H-REC-002-A`

## Execution

The preregistered run executed on source freeze
`947e64c757540ca12bbc5eaad012d5a800f05672`.

Before execution, the branch scientific source-tree digest was compared with the
currently verified gate digest. Both were identical:

`aff077317cab9fed4bd3883d0dc7c6f7e54fe8bf612597f316ff01edb34ffd37`

The branch did not modify `src/`, `configs/`, `tests/`,
`research/schemas/` or `pyproject.toml`.

Pre-execution gate/source/registry/recurrence regression suite:
**52 passed, 0 failed**.

The experiment completed all 80 registered runs and the independent artifact
verifier passed.

## Result

Result status: `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`.

Registered primary signatures were:

- loop_delay_1: last-response 62, recurrent-events 10, depth 61
- loop_delay_2: last-response 252, recurrent-events 33, depth 251
- loop_delay_4: last-response 251, recurrent-events 28, depth 250
- loop_delay_8: last-response 245, recurrent-events 20, depth 244

All preregistered primary gates passed:

- full four-delay grid for every seed;
- each treatment delay differs from delay 1;
- treatment delays are not all identical.

## Governance

The experiment remains DATA only:

- `scientific_evidence: false`
- `human_review_status: PENDING`
- `automatic_evidence_promotion: false`
- `independent_replication: false`

The workflow-created DATA commit was
`df8da50f126f12bdaa9b6d943a6cc68268a42fba`.

GitHub classified workflows automatically retriggered by the workflow-token push
as `action_required`; this is a CI-trigger authorization state, not a scientific
or test failure. This audit commit intentionally retriggers the normal PR checks
on the canonical persisted DATA head. No scientific source-digest path is
changed by this record.
