# RQ-ETH-001 — Provenance and Contribution Study

**Status:** protocol design / not preregistered  
**Execution authorized:** no  
**Research question:** `RQ-ETH-001`  
**Hypotheses:** `H-ETH-001-B`, `H-ETH-001-C`, `H-ETH-001-D`, `H-ETH-001-E`  
**Evidence mode:** empirical-methodological plus institutional-normative  
**Primary unit:** claim episode

## 1. Purpose

This protocol operationalizes the consolidated authorship research programme without treating generic runtime activity as evidence about authorship. It tests whether Human–AI-assisted MHRN knowledge production can be reconstructed as distinct contribution, decision and responsibility events.

`H-ETH-001-A` is retained as a historical umbrella hypothesis. Existing exploratory and boundary-audit artifacts tied to that identifier are not reinterpreted as direct tests of the refined subhypotheses.

## 2. Unit of analysis

A **claim episode** is the reconstructable path of one research-relevant claim from first appearance through revision, validation, acceptance, rejection or publication.

Eligible episode types include:

- research-question or hypothesis formation,
- experiment design,
- implementation/code change with scientific consequence,
- experiment interpretation,
- literature integration,
- evidence-status decision,
- manuscript claim revision.

## 3. Contribution and Accountability Matrix

Each event should capture:

| Field | Meaning |
|---|---|
| `claim_id` | Claim or research object under analysis |
| `event_id` | Single provenance event |
| `actor_type` | human / model / software / workflow / external |
| `actor_version` | Person/role, model version or software version |
| `role` | conceptualization / generation / analysis / validation / selection |
| `input_ref` | Input artifact |
| `output_ref` | Resulting artifact |
| `material_contribution` | material / non-material / unresolved |
| `decision_authority` | Actor or rule allowed to accept/reject/revise |
| `disposition` | accepted / revised / rejected / pending |
| `evidence_ref` | Commit, log, review, source or experiment reference |
| `responsibility` | Responsible natural person or institutional role |
| `timestamp` | Event time |
| `provenance_digest` | Optional integrity digest |

## 4. Material contribution codebook

A contribution is material if it changes at least one of:

1. research question or hypothesis,
2. method or protocol,
3. implementation relevant to the scientific result,
4. formal analysis,
5. interpretation,
6. evidence assessment,
7. bounded conclusion.

Spelling, formatting and meaning-preserving surface rewrites are non-material unless they alter scientific meaning.

## 5. Study phases

### Phase A — codebook pilot

Select heterogeneous claim episodes with complete enough provenance to test the coding vocabulary. Two independent coding passes should be performed without resolving disagreements in advance.

Outputs:

- disagreement catalogue,
- revised codebook,
- unresolved role classes,
- explicit exclusions,
- proposed quantitative thresholds for preregistration.

No confirmatory support claim is permitted from Phase A.

### Phase B — preregistered comparative study

Before execution, freeze:

- episode sampling rule,
- minimum provenance completeness,
- coder independence requirements,
- primary completeness metric,
- inter-rater agreement metric,
- binary Author/Tool baseline,
- matrix scoring rule,
- missing-data handling,
- success/failure thresholds,
- analysis code hash.

This phase directly tests `H-ETH-001-B`, `H-ETH-001-C` and `H-ETH-001-E`.

### Phase C — institutional standards mapping

Map the observed workflow against current formal authorship/accountability guidance. This is a standards analysis, not a runtime experiment. It informs `H-ETH-001-D` and must record the exact version/date of each external guideline.

## 6. Failure and revision criteria

The model requires revision if:

- relevant claim episodes cannot be reconstructed despite adequate project logging;
- independent coders cannot distinguish contribution roles with preregistered reliability;
- material contribution cannot be separated non-tautologically from surface transformation;
- canonization cannot be distinguished from generation in the recorded workflow;
- the multidimensional matrix provides no additional auditable information over the binary baseline;
- a canonized claim has no identifiable responsible natural person or governance role.

## 7. Claim boundary

The study can support statements about provenance, contribution roles, decision authority, auditability and formal responsibility. It cannot establish machine consciousness, moral status, legal personhood, copyright authorship or autonomous scientific responsibility.

## 8. Required external context

At minimum, the preregistered standards-mapping phase should review the then-current versions of:

- ICMJE authorship and AI-use guidance,
- CRediT / ANSI-NISO Z39.104,
- DFG guidance on generative models and research integrity,
- ALLEA European Code of Conduct for Research Integrity.

## 9. Next gate

The next scientific action is **not execution**. First freeze the codebook pilot design and define the sampling/provenance-completeness rule. Only a later preregistration may authorize a confirmatory run.
