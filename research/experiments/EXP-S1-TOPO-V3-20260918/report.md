# EXP-S1-TOPO-V3-20260918: topology_propagation_v3_time_resolved_replication

Stage 1 - Kleines SNN
Research question: RQ-SNN-003
Hypothesis: H-SNN-003-B
Source freeze: 4bd92e6d9d1e830292f9e4fbbbebdcb8e54493b3
Clean before execution: True
Data role: DATA; no automatic EVID promotion.

## Fixed design

- neurons per condition: 64
- edges per condition: 246
- synaptic weight: 55
- evaluation seeds: 20
- V2 evaluation seeds are not reused.

## Status: SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL

## Condition summaries

| condition | n | activation AUC 0-32 | half-active latency | first-output latency | final active fraction |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1d | 20 | 22.1562 | 10 | 19 | 1 |
| 2d | 20 | 26.5703 | 6 | 9 | 1 |
| 3d | 20 | 27.9922 | 4 | 6 | 1 |
| 5d | 20 | 25.5 | 4 | 5 | 0.890625 |
| 5d_shuffled | 20 | 20.8359 | 4 | 2 | 0.71875 |
| random_graph | 20 | 21.7734 | 3.5 | 2 | 0.75 |

## Primary time-resolved contrasts

| endpoint | contrast | median delta | CI95 | Holm-p | significant |
| --- | --- | ---: | --- | ---: | :---: |
| activation_auc_0_32 | 1d -> 2d | 4.41406 | [4.35938, 4.44531] | 9.53674e-06 | yes |
| activation_auc_0_32 | 2d -> 3d | 1.4375 | [1.38281, 1.47656] | 9.53674e-06 | yes |
| activation_auc_0_32 | 3d -> 5d | -2.32031 | [-3.625, -1.59375] | 9.53674e-06 | yes |
| activation_auc_0_32 | 5d -> 5d_shuffled | -4.54688 | [-5.85938, -2.92188] | 9.53674e-06 | yes |
| activation_auc_0_32 | 5d -> random_graph | -2.86719 | [-5.07031, -2.3125] | 9.53674e-06 | yes |
| half_activation_latency_censored | 1d -> 2d | -4 | [-4, -4] | 9.53674e-06 | yes |
| half_activation_latency_censored | 2d -> 3d | -2 | [-2, -2] | 9.53674e-06 | yes |
| half_activation_latency_censored | 3d -> 5d | 0 | [0, 0] | 0.90625 | no |
| half_activation_latency_censored | 5d -> 5d_shuffled | 0 | [0, 0] | 0.90625 | no |
| half_activation_latency_censored | 5d -> random_graph | -0.5 | [-1, 0] | 0.00585938 | no |

## V2 first-output latency replication

| contrast | median delta | CI95 | Holm-p | significant |
| --- | ---: | --- | ---: | :---: |
| 1d -> 2d | -10 | [-10, -10] | 9.53674e-06 | yes |
| 2d -> 3d | -3 | [-3, -2.5] | 9.53674e-06 | yes |
| 3d -> 5d | -1 | [-1, -1] | 9.53674e-06 | yes |
| 5d -> 5d_shuffled | -3 | [-3, -2] | 9.53674e-06 | yes |
| 5d -> random_graph | -3 | [-3, -2] | 9.53674e-06 | yes |

Ceiling-resolution criterion: PASS
V2 latency replication criterion: PASS
Design integrity: PASS

## Claim boundary

This protocol is an internal preregistered Stage-1 replication/robustness test of RQ-SNN-003/H-SNN-003-B. It does not constitute independent external replication, does not test a 5D advantage, does not establish scaling, cognition or biological equivalence, and creates DATA rather than EVID.

## Local review after pull

Run:
python scripts/verify_stage1_topology_v3.py

Raw data: data/evaluation.json.
Statistics: analysis/statistics.json.
