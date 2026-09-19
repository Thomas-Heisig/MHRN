# RQ-EPIST-002 — Process Governance Misclassification Study

**Status:** protocol design only  
**Preregistration:** not yet created  
**Execution authorization:** none  
**Research question:** `RQ-EPIST-002`  
**Hypothesis:** `H-EPIST-002-A`

## 1. Research question

Under which conditions does an explicit separation of source, decision, execution, DATA, review, EVID and claim reduce epistemic misclassification in rapidly iterating, AI-assisted MHRN research?

## 2. Confirmatory target

`H-EPIST-002-A` predicts that reviewers receiving a status- and provenance-separated claim packet will make fewer predefined epistemic classification errors than reviewers receiving an information-equivalent flattened summary packet.

This document does not authorize execution and is not a preregistration.

## 3. Unit of analysis

The primary unit is a **claim episode**: the bounded sequence from the first relevant observation or claim appearance to the last documented decision inside a frozen sampling window.

Historical cases may be used to design the study, but they do not become confirmatory observations merely because they motivated the protocol.

## 4. Candidate material

Candidate episodes should be selected from cases that have:

- source-bound primary artifacts;
- at least one transformation or interpretation layer;
- a documented review, correction or status decision;
- enough information to construct two information-equivalent presentation conditions.

The design should include both easy and difficult episodes and should not sample only known failures.

## 5. Conditions

### 5.1 Separated packet

The reviewer receives explicit fields for:

- source / provenance;
- execution state;
- DATA;
- report or projection;
- review;
- EVID status;
- claim boundary;
- known limitations.

### 5.2 Flattened packet

The reviewer receives the same substantive information in a conventional narrative summary without explicit status-axis separation.

The two packets must be information-equivalent as far as practical. Any residual asymmetry must be documented before execution.

## 6. Reviewer design

Preferred design:

- randomized assignment or counterbalanced crossover;
- episode order randomized within declared constraints;
- reviewers blinded to the study hypothesis where feasible;
- no reviewer may adjudicate the same episode they authored;
- training examples fixed before confirmatory review begins.

Independent external reviewers are preferred for at least one replication phase.

## 7. Error taxonomy

At minimum, the preregistration must define scoring rules for:

1. DATA classified as accepted EVID;
2. report projection treated as raw DATA;
3. technical reproducibility treated as hypothesis confirmation;
4. Human Review treated as independent replication;
5. retrospective reconstruction treated as a contemporaneous primary source;
6. AI synthesis treated as an independent external source;
7. claim scope extended beyond its documented boundary.

Additional error classes may be added only before freeze.

## 8. Outcomes

### Primary outcome

Epistemic misclassification rate per review decision.

### Secondary outcomes

- time to decision;
- inter-rater agreement;
- number of unsupported claim extensions;
- number of clarification requests;
- confidence calibration;
- correction latency where a deliberate inconsistency is included.

No secondary outcome may replace the primary outcome after data inspection.

## 9. Adjudication reference

The scoring reference must be reconstructed from source-bound primary artifacts and frozen before reviewer responses are inspected.

Adjudication must distinguish:

- artifact existence;
- artifact interpretation;
- EVID authority;
- claim scope;
- unresolved ambiguity.

Disagreement between adjudicators is itself recorded. Majority vote alone is not treated as proof of truth.

## 10. Analysis contract

Before execution, the preregistration must freeze:

- sample size or stopping rule;
- episode inclusion/exclusion;
- reviewer inclusion/exclusion;
- error scoring rules;
- primary contrast;
- handling of repeated measures;
- missing-data rule;
- multiplicity policy for secondary outcomes;
- success/failure threshold.

A simple proportion difference is not sufficient if reviewer and episode repeated measures are present; the final statistical model must respect the sampling structure.

## 11. Failure / revision criteria

`H-EPIST-002-A` must be rejected or narrowed if:

- information equivalence cannot be achieved;
- adjudication is not sufficiently reproducible;
- separated presentation does not reduce the preregistered primary error rate;
- any apparent benefit is explained entirely by materially longer review time under the preregistered utility rule;
- the effect disappears when reviewer and episode dependence are modeled;
- or the reference standard cannot be reconstructed from source-bound artifacts.

## 12. Historical methodological witnesses

The following cases may motivate packet design but are not confirmatory evidence for `H-EPIST-002-A`:

- `EXP-GEN-0036`: report projection versus underlying DATA;
- `EXP-GEN-0047`: semantic match versus test adequacy;
- `EXP-S6-SEM-CL-001/002/003`: stronger controls narrowing a mechanism claim;
- Stage-0 model-conformance path: technical reference conformance, Human Review and independent replication as separate dimensions.

## 13. Relation to other questions

- `RQ-EPIST-001` concerns system knowledge versus researcher knowledge.
- `RQ-EPIST-002` concerns the performance of research-process governance.
- `RQ-ETH-001` concerns epistemic contribution, canonization, authorship and responsibility.

These questions may share provenance material but must not share evidence automatically.

## 14. Claim boundary

A positive result would support only the scoped claim that, under the sampled tasks and reviewer population, the separated packet reduced the predefined classification error rate relative to the flattened packet.

It would not establish:

- universal superiority of the MHRN governance system;
- objective correctness of every adjudicated claim;
- independent scientific validity of MHRN's substantive neuroscience claims;
- or superiority over all external research-governance methods.
