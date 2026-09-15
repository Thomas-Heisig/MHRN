# Semantic Prototype Consolidation vs. Raw Experience Replay on Split-MNIST

## A preregistered negative result from EXP-S6-SEM-CL-002

**Date:** 2026-09-15  
**Status:** internal research publication / negative result  
**Experiment:** `EXP-S6-SEM-CL-002`  
**Stage:** 6 — Memory and World Model  

## Result in one sentence

Under the preregistered EXP-S6-SEM-CL-002 protocol, MHRN semantic-prototype replay did **not** achieve the required advantage over equally object- and update-budgeted raw-experience replay on Split-MNIST; the directed H1 is therefore falsified for this protocol.

## Primary preregistered results

| Contrast | Mean effect | Required effect | 95% paired bootstrap CI | Exact paired sign-flip | Confirmatory decision |
| --- | ---: | ---: | ---: | ---: | --- |
| Semantic − Raw final average accuracy | -0.000056 | +0.030000 | [-0.002224, +0.001722] | p = 1.000000 | fail |
| Raw − Semantic mean forgetting | -0.000278 | +0.050000 | [-0.002986, +0.001944] | p = 1.000000 | fail |
| Semantic − Random final average accuracy | +0.001778 | +0.030000 | [+0.000833, +0.002944] | p = 0.015625 | fail |

All nine preregistered paired seeds completed. The conjunctive success rule therefore failed on substantive effect criteria rather than because of missing data.

## Interpretation

The experiment provides **negative evidence for the specific claim that the current semantic prototype representation is superior to matched raw replay in the CL-002 regime**.

The semantic condition did show a small positive final-accuracy difference relative to matched random spike prototypes. That difference was statistically detectable, but its magnitude was only about 0.18 percentage points — far below the preregistered 3 percentage-point minimum effect. It is therefore not a positive confirmatory result.

The result does not establish that semantic memory is generally ineffective. It also does not establish that raw replay is generally superior. It identifies a bounded regime in which the proposed semantic compression failed to provide the preregistered practical advantage.

## Relation to EXP-S6-SEM-CL-001

`EXP-S6-SEM-CL-001` remains a positive preregistered result under its own protocol against a naive online no-replay comparator.

`EXP-S6-SEM-CL-002` narrows that result: the earlier improvement cannot currently be attributed to a demonstrated superiority of semantic prototypes over raw replay. The two experiments use different replay/update regimes, so CL-002 does not prove retrospectively that CL-001 was caused only by replay.

## Reproducibility chain

- base preregistration: `research/preregistrations/operational/EXP-S6-SEM-CL-002.json`
- pre-execution amendment: `research/preregistrations/amendments/EXP-S6-SEM-CL-002-A1.json`
- source freeze: `research/preregistrations/frozen/EXP-S6-SEM-CL-002-FREEZE.json`
- freeze attestation: `research/preregistrations/frozen/EXP-S6-SEM-CL-002-ATTESTATION.json`
- execution authorization: `research/preregistrations/authorizations/EXP-S6-SEM-CL-002.json`
- DATA: `research/experiments/EXP-S6-SEM-CL-002/results/results.json`
- generated DATA report: `research/experiments/EXP-S6-SEM-CL-002/results/REPORT.md`
- human project EVID review: `research/experiments/EXP-S6-SEM-CL-002/EVID.md`
- machine-readable EVID decision: `research/experiments/EXP-S6-SEM-CL-002/EVID.json`

## Governance

This negative publication is required by the preregistered publication rule. No outcome was hidden or converted into a post-hoc success claim. DATA and EVID remain separate, and no independent external replication is claimed.

See `MANUSCRIPT.md` for the compact scientific report and `METHODS_AND_DEVIATIONS.md` for protocol provenance and deviations.
