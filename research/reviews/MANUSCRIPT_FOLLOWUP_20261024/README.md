# Manuscript-review follow-up — 2026-10-24

This work follows the five remaining items of the 2026-10-17 TODO. It is
recorded on a local branch; publication and independent review are not implied.

| Item | Delivered | Remaining boundary |
| --- | --- | --- |
| 10% memory compression | [R1 protocol](../../preregistrations/PREREG-MEM-COMPRESSION-R1.md): complete accounting categories, matched-byte controls, 95% retention/non-inferiority rule, stop and architecture decision rules | REVIEW_READY_NOT_FROZEN: canonical RQ/H admission, byte-accounting/restore implementation tests, dataset/source freeze and R1 human approval remain. No experiment executed. |
| H-EMB-001-B | [V4 report](../../experiments/EXP-EMB001B-UNSEEN-V4-20261024/report.md): 120 runs, disturbance unknown to donor tape, matched causal controls, all integrity checks passed | Exploratory synthetic DATA only; human scientific review and EVID promotion pending. |
| 5D ablation | [R2 design](../../preregistrations/PREREG-5D-MATCHED-R2.md) and [hash freeze](../../preregistrations/PREREG-5D-MATCHED-R2.freeze.json) | Design frozen before evaluation; dedicated executable R2 runner, preflight and authorization still required. Does not bypass blocked efficiency R1. |
| Prior art | [Source-based assessment](../PRIOR_ART_REVIEW_20261024.md), explicit antecedents and bounded novelty wording | Independent external reviewer has not reviewed it; the independence TODO remains open. |
| Maturity percentages | [Method](../../../docs/05-quality/SCIENTIFIC_MATURITY_METHOD.md), arithmetic audit, corrected dashboard and enforcing checker | Status labels remain judgment-based; no evidence promotion and no probability interpretation. Historical editions unchanged. |

The memorandum is an addendum to edition 1.8, not a silent rewriting of its
published historical results. New DATA should enter a future publication only
with the scoped limitations and review status above. Source-bound experiment
details live in its own freeze record, not in the later documentation commit.

The memory R1 plan is concrete enough for methodological review but cannot be
called a full freeze merely because its prose is finished. The implementation
work listed there is required before an execution request. No result-dependent
choice, favorable outcome or automatic score change substitutes for review.

Validation: 43 focused tests passed (embodiment compatibility/controls,
publication maturity contracts and deliberate score-corruption cases).
Ruff, JavaScript syntax, documentation consistency and scientific-maturity
integrity checks passed. `verify_emb001b_unseen_v4.py` independently recomputes
the primary outcome from all 120 stored traces and checks archived hashes,
causal sentinels and source hashes against the pre-execution Git commit.
This second computation is an internal verifier, not independent peer review.
