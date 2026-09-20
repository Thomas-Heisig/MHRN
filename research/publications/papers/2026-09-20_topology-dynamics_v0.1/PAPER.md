# Dimensional Embedding and Propagation Dynamics in Resource-Matched Recurrent Spiking Neural Networks

**Thomas Heisig · Working paper v0.1 · 20 September 2026**  
**Research strand:** topology / recurrent SNN dynamics  
**Primary question:** `RQ-SNN-003` / `H-SNN-003-B`  
**Status:** DATA-based working draft; human review and external replication incomplete

## Abstract

The geometry used to construct recurrent connectivity can alter signal propagation even when neuron count, edge budget, synaptic weight, delays, and stimulation are held fixed. We report two preregistered Stage-1 studies in the Multi-Scale Homeostatic Recurrence Network (MHRN) comparing six resource-matched topology conditions: 1D, 2D, 3D, 5D, shuffled-5D, and random-graph constructions. In the first study, 64 neurons and 246 edges were evaluated across 20 paired seeds after a separate calibration phase. First-output latency differed across all five preregistered adjacent/control contrasts after Holm correction, while terminal active fraction saturated at 1.0 for 1D–3D and therefore could not resolve those lower-dimensional differences. A prospectively corrected internal replication used new seeds and time-resolved endpoints. Activation AUC over ticks 0–32 separated 1D→2D, 2D→3D, 3D→5D, 5D→shuffled-5D, and 5D→random-graph contrasts, while all five first-output-latency directions from the original study replicated. These results support the narrow claim that concrete resource-matched topology influences propagation dynamics in this 64-neuron regime. They do not establish that a 5D embedding is generally superior, biologically privileged, more scalable, or cognitively advantageous.

## 1. Introduction

Recurrent spiking neural networks depend not only on neuron and synapse dynamics but also on how connectivity is arranged. A multidimensional coordinate system can be used to construct local or structured recurrent graphs, but dimensional labels alone do not imply functional advantage. A scientifically useful test must therefore separate geometric construction from confounds such as neuron count, edge density, weights, delays, stimulation, and seed choice.

MHRN originally contained broader hypotheses about multidimensional address spaces. Early exploratory tests were inadequate for strong dimensional claims because they did not causally couple geometry to a sufficiently expressive recurrent graph. The present work narrows the question to a simpler one:

> Under matched resource constraints, does the concrete topology used to construct a recurrent SNN alter propagation dynamics?

This paper focuses on `RQ-SNN-003 / H-SNN-003-B`, not on the stronger `H-5D-005-A` advantage hypothesis.

## 2. Methods

### 2.1 Network design

Both valid study lines use:

- 64 neurons per condition;
- 246 directed edges per condition;
- matched synaptic weight;
- matched delays and stimulation;
- paired evaluation seeds;
- separate calibration and evaluation stages where applicable.

The evaluated conditions are:

1. 1D structured topology;
2. 2D structured topology;
3. 3D structured topology;
4. 5D structured topology;
5. shuffled-5D control;
6. random-graph control.

The exact graph-construction rules and frozen protocol definitions are preserved in the preregistration and experiment artefacts.

### 2.2 V2 preregistered study

Experiment: `EXP-S1-TOPO-V2-20260918`  
Protocol: `topology_propagation_v2`

A four-seed calibration stage selected synaptic weight 55.0 through a preregistered activity-adequacy gate. The subsequent evaluation used 20 paired seeds and 120 total condition-runs.

Primary endpoints were:

- terminal active fraction;
- first-output latency.

The primary inferential procedure used exact paired two-sided sign tests with Holm correction across the preregistered contrast family. Deterministic bootstrap confidence intervals summarized paired median differences.

### 2.3 R1 time-resolved internal replication

Experiment: `EXP-S1-TOPO-V3-R1-20260918`  
Protocol: `topology_propagation_v3_r1_time_resolved_replication`

The replication used 20 new evaluation seeds and retained the 64-neuron, 246-edge, weight-55.0 design. It introduced time-resolved endpoints to resolve a known ceiling effect in terminal active fraction.

Primary endpoints were:

- activation AUC over ticks 0–32;
- half-activation latency.

A single Holm family covered all ten preregistered time-resolved tests. The original V2 first-output-latency contrasts were also repeated as a dedicated replication endpoint with their own Holm family.

### 2.4 Evidence status

Both lines are source-bound experiment DATA. They do not receive automatic EVID promotion. The R1 study is an internal preregistered replication/robustness test, not independent external replication.

## 3. Results

### 3.1 V2 condition summaries

| Condition | n | Active fraction median | First-output latency median | Total spikes median |
| --- | ---: | ---: | ---: | ---: |
| 1D | 20 | 1.0000 | 19 | 401.0 |
| 2D | 20 | 1.0000 | 9 | 363.0 |
| 3D | 20 | 1.0000 | 6 | 281.0 |
| 5D | 20 | 0.8750 | 5 | 181.0 |
| 5D shuffled | 20 | 0.7734 | 2 | 179.5 |
| Random graph | 20 | 0.7188 | 2 | 165.5 |

First-output latency differed in all five primary contrasts. Median right-minus-left differences were:

- 1D→2D: −10 ticks;
- 2D→3D: −3 ticks;
- 3D→5D: −1 tick;
- 5D→shuffled-5D: −3 ticks;
- 5D→random graph: −3 ticks.

Each had Holm-adjusted `p = 1.90735e-05`.

Terminal active fraction could not distinguish 1D→2D or 2D→3D because all three lower-dimensional conditions saturated at a median of 1.0. This is treated as a measurement-ceiling limitation rather than evidence of equality.

### 3.2 R1 time-resolved results

Median activation AUC over ticks 0–32 was:

| Condition | Median activation AUC |
| --- | ---: |
| 1D | 22.1562 |
| 2D | 26.5703 |
| 3D | 28.0078 |
| 5D | 25.3281 |
| 5D shuffled | 21.0781 |
| Random graph | 21.5078 |

The five preregistered activation-AUC contrasts were all significant after correction:

- 1D→2D: median Δ +4.4141, Holm `p = 1.90735e-05`;
- 2D→3D: +1.4609, Holm `p = 1.90735e-05`;
- 3D→5D: −2.7500, Holm `p = 1.90735e-05`;
- 5D→shuffled-5D: −4.4141, Holm `p = 0.000160217`;
- 5D→random graph: −3.4453, Holm `p = 1.90735e-05`.

Half-activation latency separated 1D→2D and 2D→3D but not the three later contrasts.

The dedicated V2 first-output-latency replication reproduced all five original contrast directions with Holm-adjusted `p = 9.53674e-06` for each contrast.

The preregistered ceiling-resolution criterion and latency-replication criterion both passed.

## 4. Interpretation

The combined DATA support a narrow topological conclusion:

> In the tested 64-neuron, 246-edge recurrent SNN regime, changing the matched graph-construction topology changes propagation dynamics.

The results also show why endpoint choice matters. Terminal active fraction saturated for 1D, 2D, and 3D in V2, whereas time-resolved activation AUC in R1 resolved systematic differences among those same conditions.

The observed ordering is not a monotonic dimensional-improvement result. In particular, 5D does not dominate 3D across the reported endpoints, and shuffled/random controls can produce earlier first outputs while lower activation AUC. Different propagation metrics therefore capture different graph-dynamical properties.

## 5. What this paper does not show

This study does **not** establish:

- a general 5D advantage;
- optimization of recurrent connectivity by dimensionality alone;
- biological correspondence between five coordinate axes and brain anatomy;
- scalability beyond the tested small-network regime;
- improved learning, memory, cognition, or task performance;
- independent external replication.

The stronger 5D-specific hypotheses require a separate >=1000-neuron, geometry-specific, resource-matched programme with preregistered functional endpoints.

## 6. Related work and biological context

Spatial embedding, wiring constraints, recurrent graph structure, small-world organization, modularity, and conduction delay are well-established concerns in computational neuroscience and network science. Biological nervous systems exhibit strong spatial and developmental constraints, but those facts do not imply that MHRN's 5D coordinate representation maps onto biological dimensions.

The appropriate biological comparison is therefore mechanistic and structural: whether controlled graph geometry produces measurable propagation effects and whether any future effect survives topology-, resource-, and scale-matched controls.

A formal prior-art review is still required before external submission.

## 7. Reproducibility

Canonical artefacts include:

- `research/preregistrations/PREREG-S1-TOPO-V2.json`;
- `research/experiments/EXP-S1-TOPO-V2-20260918/`;
- `research/experiments/EXP-S1-TOPO-V3-R1-20260918/`;
- verification scripts for V2 and R1;
- source-freeze hashes and raw evaluation DATA.

The invalid intermediate V3 run is preserved as an audit trail and excluded from confirmatory interpretation because its multiple-testing implementation did not match the preregistration.

## 8. Limitations and next experiments

The most important next steps are:

1. external replication by an independent team;
2. larger matched networks;
3. topology-preserving dimensional controls;
4. resource-cost measurement;
5. functional task endpoints beyond propagation;
6. explicit testing of `H-5D-005-A` rather than treating `H-SNN-003-B` as a proxy.

## 9. Data and code availability

Code: https://github.com/Thomas-Heisig/MHRN  
Author ORCID: https://orcid.org/0009-0002-9589-1872

All numerical claims in this working draft are tied to the V2 and V3-R1 source-bound DATA artefacts identified above.

## 10. Claim boundary

The current manuscript is a DATA-based working paper. It may report the results of the two valid preregistered internal study lines, but it must not use phrases such as “5D is superior”, “5D optimizes connectivity”, or “brain-like dimensionality” without new, appropriately controlled evidence.
