# EXP-S6-SEM-CL-003 - Human Review Candidate

**Status:** `PENDING`

This document is a review candidate. It is not a human decision and does not promote DATA to EVID.

## Review target

- Experiment: `EXP-S6-SEM-CL-003`
- Research question: `RQ-S6-SEM-003`
- Protocol: `Replay dose x representation at constant total update budget on Split-MNIST`
- Seeds: `301-312`
- Conditions: `R05`, `S05`, `R20`, `S20`, `X20`, `R40`, `S40`
- Complete paired seeds: `12`
- Source DATA: `results/results.json`
- Machine report: `results/REPORT.md`
- Preregistration: `research/preregistrations/operational/EXP-S6-SEM-CL-003.json`

## Observed decision outputs

- Result classification: `H1_negative_H2_negative`
- C1 (`S20 - R20` accuracy): failed preregistered minimum effect and p-value rule.
- C2 (`R20 - S20` forgetting): failed preregistered minimum effect and p-value rule.
- C3 (`S20 - X20` accuracy): passed its preregistered rule.
- C4 (dose interaction): failed its preregistered minimum effect and p-value rule.

The conjunctive H1 rule therefore fails. H2 also fails. The negative and null outcomes must be retained.

## Human review scope

The reviewer should verify:

1. The frozen protocol, source hashes, seed set and all seven conditions were preserved.
2. The 12 seed-condition pairs are complete and no missing-data rule was bypassed.
3. C1-C4 use the preregistered endpoints, thresholds, bootstrap intervals and exact sign-flip tests.
4. C3 is not reinterpreted as a semantic advantage over raw replay.
5. The total update budget and raw/semantic/random object matching are correctly represented.
6. The result remains DATA-only and is not an independent external replication.

## Allowed interpretation

Under this frozen Split-MNIST regime, CL-003 does not confirm a semantic-prototype advantage over matched raw replay and does not confirm a replay-dose interaction. The positive C3 result is limited to the preregistered comparison against the random matched control and does not rescue H1.

## Prohibited interpretation

The result must not be used to claim that semantic memory is generally useless, that raw replay is generally superior, that CL-001 was explained completely, or that the result generalizes beyond the declared dataset, budgets and protocol.

## Required decision

A human reviewer must record either `accepted_as_interpretation` or `rejected` with reviewer identity and comments. Automatic DATA-to-EVID promotion remains disabled.
