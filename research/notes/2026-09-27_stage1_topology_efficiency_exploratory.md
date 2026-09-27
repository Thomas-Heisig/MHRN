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

## Competing explanations to test prospectively

The post-hoc ratio pattern is compatible with several distinct explanations. None is privileged by the historical DATA:

1. **Specific coordinate-organization effect.** The registered 5D graph organization itself could change how much early activation is obtained per emitted spike or delivered synaptic event.
2. **Sparse-/efficient-coding-like activity pattern.** A lower-activity code could improve the descriptive ratios without the effect being specific to 5D geometry. This is an activity-pattern explanation, not structural address-space sparsity.
3. **Dynamic-recruitment artifact.** Because the 5D condition recruits a smaller final fraction of neurons than 1d–3d in the historical run, a smaller denominator could mechanically increase AUC/spike or AUC/event.
4. **Metric/window artifact.** `activation_auc_0_32` integrates activity over a fixed 32-tick window. Different onset, duration or recruitment trajectories can yield similar integrals, so a ratio based on this AUC need not identify a unique mechanism.

The prospective experiment must distinguish these explanations rather than assuming that a positive ratio is evidence for 5D geometry.

## Relation to the Temporal-Order line

The separate Temporal-Order methodological issue around perfect decoder scores does not enter this efficiency study: the efficiency endpoints use propagation AUC, spike counts and delivered synaptic events and require **no temporal-order decoder**. The two Stage-1 lines therefore remain methodologically separate.

## Sparse-coding literature boundary

Olshausen & Field (1996) is included only as related-work context for the general principle that sparse activity can participate in efficient coding. The MHRN 5D coordinate construction is **not** equivalent to sparse coding in the Olshausen–Field sense, and this prospective study does not reproduce or test their natural-image coding result.

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

Even a positive prospective result would support only a scoped propagation-efficiency mechanism in the tested Small-SNN envelope. It would not establish memory-capacity gain, bit-level storage reduction, parameter-count reduction, Shannon information capacity, general representational capacity, cognition, biological equivalence, scaling, or universal 5D superiority. AUC/spike and AUC/event are efficiency ratios, not information-capacity measures. All registered conditions materialize 64 neurons; this study does not test materialized-coordinate count or theoretical addressability.
