# Exploratory note — Stage-1 topology efficiency observation

**Date:** 2026-09-27  
**Source experiment:** `EXP-S1-TOPO-PROMO-R1-20260927`  
**Authority:** exploratory / hypothesis-generating only  
**EVID status:** none  
**Claim:** does not modify `EVID-2026-19`

## Observation

The preregistered Stage-1 topology promotion run supported only the bounded topology-sensitive propagation claim `CLAIM-S1-TOPO-001`. After completion, additional ratios were calculated from the already observed condition medians. These ratios were **not preregistered endpoints** and therefore cannot be used as confirmatory evidence.

From the persisted medians:

| condition | activation_auc_0_32 | total_spikes | delivered_events | AUC/spike | AUC/event |
| --- | ---: | ---: | ---: | ---: | ---: |
| 3d | 27.953125 | 281.0 | 1036.0 | 0.0994773 | 0.0269818 |
| 5d | 24.828125 | 177.5 | 631.0 | 0.1398768 | 0.0393473 |
| 5d_shuffled | 21.1171875 | 166.0 | 560.0 | 0.1272120 | 0.0377093 |
| random_graph | 22.609375 | 171.0 | 587.0 | 0.1322186 | 0.0385168 |

Relative to 3d, the median-ratio calculation is approximately:
- 5d AUC/spike: +40.6%
- 5d AUC/delivered-event: +45.8%

These values are descriptive post-hoc observations only.

## Important correction: occupancy versus dynamic recruitment

The registered `5d` condition uses shape `4 x 2 x 2 x 2 x 2 = 64` and the runner constructs all 64 coordinates. Therefore the Stage-1 5d condition does **not** occupy only ~6% of its declared coordinate lattice. All 64 coordinate positions are materialized.

The lower `final_active_fraction` of the 5d condition (~0.867 median) is therefore a difference in **dynamic recruitment during the run**, not a difference in structural address-space occupancy.

Consequently, a prospective efficiency experiment must control dynamic recruitment/activation ceiling rather than treating address-space sparsity as an established explanation.

## Why this is not evidence

The ratios `activation_auc_0_32 / total_spikes` and `activation_auc_0_32 / delivered_events` were not preregistered primary or secondary inferential endpoints in the promotion run. They were calculated after the topology result was known.

They may motivate a new hypothesis but must not be attached to `EVID-2026-19` as confirmatory support.

## Prospective hypothesis generated

`H-SNN-003-C` / `CLAIM-S1-EFFICIENCY-001` now capture the bounded question prospectively.

The intended study must:
1. predefine AUC/spike and AUC/event before execution;
2. keep neuron count, edge budget, neuron model, weights/delays and stimulus accounting explicit;
3. include controls that separate coordinate organization from dynamic-recruitment effects;
4. use a disjoint calibration partition for any activation-matching procedure;
5. use fresh evaluation seeds not present in the repository;
6. freeze all endpoint, multiplicity and decision rules before execution;
7. remain DATA until separate human review and EvidenceEngine promotion.

## Claim boundary

Even a positive prospective result would support only a scoped propagation-efficiency mechanism in the tested Small-SNN envelope. It would not establish memory-capacity gain, bit-level storage reduction, general information capacity, cognition, biological equivalence, scaling, or universal 5D superiority.
