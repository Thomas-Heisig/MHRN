# EVID Review — EXP-S6-SEM-CL-002

**Review date:** 2026-09-15  
**Status:** human-reviewed project EVID interpretation  
**Underlying DATA:** `research/experiments/EXP-S6-SEM-CL-002/results/results.json`  
**Frozen preregistration:** `research/preregistrations/operational/EXP-S6-SEM-CL-002.json` + amendment A1  

## Decision

The preregistered hypothesis **H1 is falsified under the EXP-S6-SEM-CL-002 protocol**.

The experiment does **not** provide confirmatory evidence that MHRN semantic prototype consolidation is superior to matched raw-experience replay for catastrophic-forgetting reduction on this Split-MNIST protocol.

This negative result is retained as evidence. It is not discarded, retuned or reclassified as a positive result.

## Preregistered contrasts

| Contrast | Observed mean | Preregistered minimum | 95% paired bootstrap CI | Exact paired sign-flip | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| B3 − B2 final average accuracy | -0.000056 | +0.030000 | [-0.002224, +0.001722] | p = 1.000000 | fail |
| B2 − B3 mean forgetting | -0.000278 | +0.050000 | [-0.002986, +0.001944] | p = 1.000000 | fail |
| B3 − B4 final average accuracy | +0.001778 | +0.030000 | [+0.000833, +0.002944] | p = 0.015625 | fail: statistically positive but below the preregistered minimum effect |

All nine paired seeds completed; there was no missing-seed qualification of the result.

## What the result means

1. **No semantic-specific advantage over raw replay was demonstrated.** B3 and B2 are effectively indistinguishable on the two primary semantic-vs-raw endpoints; the point estimates slightly favor raw replay, but the differences are tiny and statistically non-significant.
2. **B3 does outperform the random-pattern control by a small amount in final accuracy**, and that paired difference has a positive bootstrap interval and p < 0.05. However, the effect is only about **0.18 percentage points**, far below the preregistered +3 percentage-point minimum. It therefore cannot be promoted as confirmation of H1.
3. The preregistered conjunctive success rule fails. The project must therefore treat CL-002 as **negative evidence for the claimed prototype advantage in this regime**.

## Relation to EXP-S6-SEM-CL-001

EXP-S6-SEM-CL-001 remains a valid positive result **under its own frozen protocol**: semantic consolidation plus bounded replay improved final accuracy and forgetting relative to a naive online baseline.

CL-002 narrows the interpretation of that earlier result. It shows that, under the CL-002 matched replay regime, the benefit cannot be attributed to a demonstrated superiority of semantic prototypes over raw replay.

It would be too strong to conclude that CL-001 was *proved* to be “only a replay effect”. The two experiments use materially different replay/update regimes. In particular, CL-001 used a much larger replacement-style replay exposure, whereas CL-002 fixes 100 additional replay updates per task transition (maximum 400) and realizes only a small number of mature semantic objects per task. Therefore CL-002 falsifies the specific CL-002 H1 claim, but does not retrospectively decompose every causal component of CL-001.

## Mechanistic lesson

The current implementation produces only a small number of mature semantic concepts per task (typically a few objects rather than the nominal capacity ceiling of 50). With only 100 replay updates per transition, neither raw nor semantic replay materially protects earlier tasks. This is a scientifically useful regime result:

- semantic compression does not automatically confer continual-learning advantage;
- replay dose and memory realization matter;
- a statistically detectable semantic-vs-random signal can still be practically too small to satisfy a meaningful-effect criterion;
- future tests must separate **representation quality**, **replay exposure**, and **memory budget definition** rather than treating “replay” as one variable.

These observations are interpretations of the frozen result, not post-hoc changes to its confirmatory decision rule.

## Claims allowed after CL-002

A defensible combined statement is:

> EXP-S6-SEM-CL-001 showed that MHRN semantic consolidation with bounded replay can improve Split-MNIST retention relative to a naive no-replay online baseline under its frozen protocol. EXP-S6-SEM-CL-002 did not confirm a semantic-prototype advantage over equally object- and update-budgeted raw replay; its preregistered H1 was falsified.

## Claims not allowed

CL-002 does **not** establish:

- that semantic memory is generally useless;
- that raw replay is generally superior;
- that the CL-001 result was definitively caused only by replay;
- that the complete recurrent MHRN SNN is inferior or superior to a standard SNN;
- transfer to other datasets, replay budgets or memory-capacity definitions;
- biological correctness of the semantic mechanism.

## Next confirmatory question

The next experiment must use a **new identifier**. A scientifically useful follow-up is to test whether the CL-002 null/negative result is caused by replay exposure being too weak to express representation differences. That follow-up should, before execution, preregister a replay-dose axis while keeping semantic-vs-raw memory matching intact. It must not alter or rerun CL-002.

## Governance

- DATA remain immutable.
- This file is a human-reviewed project interpretation, not an independent external replication.
- No automatic evidence promotion was used.
- Negative evidence is retained in the repository and should be reflected in future publications and scientific-progress reporting.
