# SNN-005 isolated execution audit

Experiment: `EXP-SNN005-HOLDOUT-R2-20260919`

## Execution isolation

The scientific run was executed in a detached temporary Git worktree rather
than in the primary checkout.

- source freeze: `71b90a4d95ed2e68385ac3f65cb36a39a1eea839`
- primary checkout clean before execution: **true**
- primary checkout clean after execution: **true**
- generated DATA confined to isolated worktree: **true**
- isolated worktree became dirty only because the experiment generated its DATA:
  **true**
- regression suite before execution: **53 passed**

The verified workflow artifact was persisted without re-executing the
simulation. The workflow artifact ID is `10590472981`.

## Registered result

Status: `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`

Mean held-out accuracy:

- `learning_on`: **0.7640625**
- `learning_off`: **0.5000000**
- `sham_replay`: **0.5000000**
- `weight_reset`: **0.5000000**
- `weight_shuffle`: **0.5000000**

Primary contrast `learning_on - learning_off`:

- mean difference: **0.2640625**
- paired bootstrap 95% CI: **[0.1953125, 0.3328125]**
- exact two-sided sign-flip p: **0.000030517578125**
- Holm-adjusted p: **0.0001220703125**

All preregistered scientific decision gates passed.

## Governance boundary

The result remains DATA only:

- `scientific_evidence: false`
- `human_review_status: PENDING`
- `automatic_evidence_promotion: false`
- `independent_replication: false`

This audit record does not modify the experiment DATA, the registered analysis,
or the source freeze. It provides a normal user-authored PR head so repository
CI can evaluate the canonical persisted DATA without another experiment run.
