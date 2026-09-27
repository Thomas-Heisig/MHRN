# Stage-1 scientific consolidation — Small SNN

**Date:** 2026-09-25  
**Authority:** current scientific-state decision / maturity interpretation  
**Scope:** Stage 1 only; no automatic EVID promotion

## Decision

Stage 1 is no longer represented by the historical 30% software-contract projection. The current repository supports a **85% scientific-maturity score** under the existing six-criterion weighting contract:

- registered RQ/H: **met** = 15%;
- frozen scientific protocols beyond the software contract: **met** = 20%;
- source-bound scientific DATA: **met** = 20%;
- human-reviewed evidence gate: **met** = 20% of 20%;
- independent replication: **open** = 0% of 15%;
- methods/model attribution: **met** = 10%.

The reviewed-evidence criterion is now complete for the central topology claim through the prospective promotion run `EXP-S1-TOPO-PROMO-R1-20260927`, canonical human review (`supports`) and explicit EvidenceEngine registration as `EVID-2026-19`. This remains separate from independent replication.

## Central Stage-1 baseline

The canonical scientific baseline is `RQ-SNN-003 / H-SNN-003-B`. Its bounded claim is that under matched neuron count, global edge budget, stimulation, weights/delays and the registered Small-SNN operating envelope, concrete network topology changes propagation dynamics; no 5D advantage is assumed or inferred.

`EXP-S1-TOPO-V2-20260918` and `EXP-S1-TOPO-V3-R1-20260918` are treated as one linked line, **STAGE1-TOPOLOGY-LINE-001**. V2 establishes the first preregistered 64-neuron/246-edge topology-sensitive result. R1 uses fresh seeds, corrects the V3 multiple-testing implementation, resolves the V2 terminal-endpoint ceiling with prospective time-resolved endpoints and internally replicates all five V2 first-output latency directions. `EXP-S1-TOPO-V3-20260918` remains audit-only because its primary Holm family was implemented incorrectly.

## Human reviews

The V2 review at `research/experiments/EXP-S1-TOPO-V2-20260918/review_request.json.review.json` and the V3-R1 review at `research/experiments/EXP-S1-TOPO-V3-R1-20260918/review_request.json.human-review.json` were completed by Thomas Heisig with `accepted_as_interpretation`.

These reviews satisfy the **human-review subgate** for Stage-1 maturity. They do not silently become an EvidenceEngine `supports` decision and do not rewrite source-bound experiment manifests.

## Separate EVID-promotion assessment

Current topology status: **COMPLETED as `EVID-2026-19`**.

The historical V2/R1 manifests remain immutable and were not retrofitted. Instead, `EXP-S1-TOPO-PROMO-R1-20260927` prospectively repeated the bounded topology claim with fresh seeds 6301–6320 under the current EvidenceEngine provenance contract. The run completed with clean Git state, valid execution, zero runtime/fatal errors, full provenance digests and source-freeze binding. The canonical Human Review by Thomas Heisig records `supports` while preserving the null findings and the explicit no-5D-superiority boundary. The subsequent explicit EvidenceEngine promotion created `EVID-2026-19`.

Automatic promotion remains disabled. The Temporal-Order line remains reviewed DATA and still requires its own prospective promotion path.

## Second Stage-1 functional line

**STAGE1-TEMPORAL-ORDER-LINE-002** is separate from the topology baseline: `RQ-TEMP-002 / H-TEMP-002-A`, experiment `EXP-S1-TEMP-ORDER-V2-20260919`. The design uses a six-neuron acyclic SNN, 20 seeds and 120 runs with intact versus identity-destroyed arms plus simultaneous control. Its status is `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`; the append-only Human Review at `research/experiments/EXP-S1-TEMP-ORDER-V2-20260919/review_request.json.review.json` was completed by Thomas Heisig with `accepted_as_interpretation`. Scientific EVID remains false and independent replication remains false.

This line is scientifically useful because it contains an information-destroying control and a fixed decoding task, but it is **independent only in functional question/task**. It is not an independent replication of the topology line and does not establish learning, memory, cognition, scaling or general temporal reasoning.

The central machine-readable synthesis is `research/registry/stage1_baseline.json` (`STAGE1-SCIENTIFIC-BASELINE-20260925`). It binds the 85% maturity derivation, the linked V2/V3-R1 topology DATA line, the reviewed Temporal-Order functional line, the separate EVID-promotion assessment and the unchanged independence boundary in one canonical record.

Deterministic publication projection for Edition 1.8 was regenerated after this consolidation so manuscript, research-object registry and publication manifest describe the same canonical state.

## Remaining Stage-1 work

1. execute the separate prospective EvidenceEngine-compatible promotion path for the Temporal-Order claim and complete canonical human review;
2. obtain independently implemented reference/cross-implementation replication for the central topology claim;
3. broaden task, perturbation and scaling regimes without conflating them with the existing baseline;
4. keep `RQ-5D-005 / H-5D-005-A` separate and open until its larger geometry-specific programme is executed.
