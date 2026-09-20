# Provenance-Separated Reporting for AI-Assisted Research: A Protocol for Testing Epistemic Misclassification

**Thomas Heisig · Methods / protocol paper v0.1 · 20 September 2026**  
**Research strand:** research integrity / recursive epistemics  
**Primary question:** `RQ-EPIST-002` / `H-EPIST-002-A`  
**Related programme:** `RQ-ETH-001` / `H-ETH-001-B/C/D/E`  
**Status:** methods and protocol paper; confirmatory study not yet executed

## Abstract

Rapid AI-assisted research can compress the path from question formation to code, analysis, review, and publication, increasing the risk that distinct epistemic states are conflated. We introduce a testable research-governance framework that explicitly separates source, decision, execution, DATA, review, accepted evidence, claim scope, and replication status. Rather than treating this framework as self-validating, we specify a controlled reviewer study to test whether provenance-separated claim packets reduce predefined epistemic classification errors relative to information-equivalent flattened narrative summaries. The primary outcome is epistemic misclassification rate; secondary outcomes include review time, inter-rater agreement, unsupported claim extension, clarification requests, and confidence calibration. The protocol also defines a claim-episode model for distinguishing material contributions, canonization decisions, formal authorship, and responsibility in Human–AI-assisted research. No confirmatory results are reported because the study has not yet been preregistered or executed. The contribution of this paper is therefore methodological: an auditable framework and falsifiable evaluation design for testing whether explicit evidence-state separation improves scientific review under AI-assisted research conditions.

## 1. Motivation

Generative AI can contribute to literature discovery, methodological criticism, code, analysis, and scientific writing. This speed creates a governance problem that is not resolved by generic disclosure alone.

A research workflow may contain at least the following distinct objects:

```text
source
decision
execution
DATA
analysis / projection
human review
EVID decision
claim
replication
```

When these are collapsed into a fluent narrative, reviewers may incorrectly infer that:

- completed execution implies scientific support;
- technical reproducibility implies hypothesis confirmation;
- Human Review implies independent replication;
- AI synthesis is an independent source;
- retrospective reconstruction is contemporaneous primary evidence;
- a registered DOI implies peer review.

The proposed framework calls this class of errors **epistemic misclassification**.

## 2. Recursive epistemics as an operational research programme

“Recursive epistemics” is used here for a research process in which the production, transformation, validation, selection, and publication of claims are themselves represented as auditable research objects.

The framework distinguishes object-level scientific claims from process-level claims. A provenance system may improve auditability without making the underlying neuroscience claim true.

This distinction is central:

> Better research governance is not additional evidence for the substantive hypothesis being governed.

## 3. Primary research question

`RQ-EPIST-002` asks:

> Under which conditions does explicit separation of source, decision, execution, DATA, review, EVID and claim reduce epistemic misclassification in rapidly iterating, AI-assisted research?

`H-EPIST-002-A` predicts that reviewers receiving a status- and provenance-separated claim packet will make fewer predefined epistemic classification errors than reviewers receiving an information-equivalent flattened summary packet.

This is currently a hypothesis, not a result.

## 4. Experimental design

### 4.1 Unit of analysis

The primary unit is a **claim episode**: the bounded sequence from first relevant observation or claim appearance to the last documented decision in a frozen sampling window.

Candidate episodes require:

- source-bound primary artefacts;
- at least one transformation or interpretation layer;
- a documented review, correction, or status decision;
- sufficient information to construct two matched presentation conditions.

### 4.2 Conditions

#### Provenance-separated packet

The reviewer receives explicit fields for:

- source/provenance;
- execution status;
- DATA;
- report or projection;
- Human Review;
- EVID status;
- replication status;
- claim boundary;
- known limitations.

#### Flattened summary

The reviewer receives the same substantive information in conventional prose without explicit state-axis separation.

The experiment must freeze an information-equivalence rule before execution.

### 4.3 Reviewer design

Preferred designs include randomized parallel assignment or a counterbalanced crossover. Reviewers should be blinded to the study hypothesis where feasible. No participant should adjudicate an episode they authored.

At least one later replication should use reviewers external to the MHRN project.

## 5. Primary and secondary outcomes

### Primary outcome

**Epistemic misclassification rate per review decision.**

Predefined error classes include:

1. DATA classified as accepted EVID;
2. report projection classified as raw DATA;
3. technical reproducibility classified as hypothesis confirmation;
4. Human Review classified as independent replication;
5. retrospective reconstruction classified as contemporaneous primary source;
6. AI synthesis classified as independent external source;
7. claim scope extended beyond its documented boundary.

### Secondary outcomes

- time to decision;
- inter-rater agreement;
- unsupported claim extensions;
- clarification requests;
- confidence calibration;
- correction latency.

Repeated reviewer and episode measurements require an analysis model that respects dependence; a simple pooled proportion comparison is not sufficient.

## 6. Adjudication

The reference answer for each episode must be reconstructed from source-bound primary artefacts and frozen before reviewer responses are inspected.

The adjudication record must distinguish:

- object existence;
- interpretation;
- evidence authority;
- claim scope;
- unresolved ambiguity.

Disagreement between adjudicators is recorded rather than silently collapsed.

## 7. Contribution, canonization, and responsibility

The related `RQ-ETH-001` programme introduces a Contribution and Accountability Matrix. Each provenance event can encode:

- actor type;
- actor/version;
- contribution role;
- input and output artefacts;
- materiality;
- decision authority;
- disposition;
- evidence reference;
- responsible natural person;
- timestamp and optional provenance digest.

This enables empirical questions about whether independent coders can distinguish generation, analysis, validation, selection, and canonization.

It also separates **material contribution** from **formal authorship**. A model may materially influence a scientific decision without becoming a formal author or accountable natural person.

## 8. Falsification and revision criteria

The framework must be narrowed or rejected if:

- information-equivalent packet construction cannot be achieved;
- the adjudication standard is not reproducible;
- provenance-separated presentation does not reduce the preregistered primary error rate;
- any benefit is explained entirely by materially longer review time under the frozen utility rule;
- effects disappear after reviewer/episode dependence is modeled;
- contribution roles cannot be coded with adequate reliability;
- canonization cannot be distinguished from generation.

## 9. Historical witnesses, not confirmatory evidence

MHRN contains several historical cases that motivate the error taxonomy, including:

- inadequate topology tests that were initially easy to overinterpret;
- DATA/report distinctions;
- progressively stronger controls narrowing semantization claims;
- separation of model-conformance, Human Review, EVID, and independent replication.

These cases may inform packet design. They are **not** confirmatory observations for `H-EPIST-002-A`.

## 10. AI-use transparency

The research programme itself is AI-assisted. AI systems can generate candidate questions, critiques, code, analyses, and manuscript text. The protocol therefore treats AI activity as provenance rather than hiding it.

Thomas Heisig remains the formal human author and publication authority for this manuscript. The empirical question is not whether AI “deserves” authorship, but whether contributions, decisions, and accountability can be represented and reviewed more reliably.

## 11. Relation to open science

The proposed framework is compatible with:

- preregistration;
- immutable source freezes;
- open DATA;
- explicit negative/null results;
- versioned manuscripts;
- DOI-separated software/publication/dataset objects;
- transparent AI-use disclosure.

Open artefacts do not guarantee epistemic correctness; they make more of the reasoning chain inspectable.

## 12. Current status and next gate

This paper reports a **methodological framework and protocol design**, not confirmatory results.

Before any result claim is permissible, the project must:

1. freeze a claim-episode sampling rule;
2. freeze reviewer inclusion/exclusion;
3. construct and validate information-equivalent packet pairs;
4. define adjudication and inter-rater criteria;
5. preregister sample size/stopping and statistical analysis;
6. authorize execution;
7. conduct the study;
8. complete Human Review;
9. seek external replication.

## 13. Claim boundary

A future positive study could support only the scoped claim that provenance-separated presentation reduced predefined classification errors in the sampled tasks and reviewer population.

It would not establish universal superiority of MHRN governance, objective truth of every adjudicated claim, validity of MHRN's neuroscience hypotheses, or superiority over all research-integrity frameworks.

## 14. Availability

Canonical repository: https://github.com/Thomas-Heisig/MHRN  
Author ORCID: https://orcid.org/0009-0002-9589-1872  
Primary protocol: `research/protocols/RQ_EPIST_002_PROCESS_GOVERNANCE_STUDY.md`  
Related provenance protocol: `research/protocols/RQ_ETH_001_PROVENANCE_STUDY.md`
