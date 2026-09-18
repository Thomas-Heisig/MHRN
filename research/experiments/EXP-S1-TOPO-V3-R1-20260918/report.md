# EXP-S1-TOPO-V3-R1-20260918: topology_propagation_v3_r1_time_resolved_replication

Stage 1 - Kleines SNN
Research question: RQ-SNN-003
Hypothesis: H-SNN-003-B
Source freeze: 47d348010bdbfe18ee234132fe567552486b062b
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
| 3d | 20 | 28.0078 | 4 | 6 | 1 |
| 5d | 20 | 25.3281 | 4 | 5 | 0.882812 |
| 5d_shuffled | 20 | 21.0781 | 4 | 2 | 0.726562 |
| random_graph | 20 | 21.5078 | 4 | 2 | 0.734375 |

## Primary time-resolved contrasts

| endpoint | contrast | median delta | CI95 | Holm-p | significant |
| --- | --- | ---: | --- | ---: | :---: |
| activation_auc_0_32 | 1d -> 2d | 4.41406 | [4.36719, 4.42969] | 1.90735e-05 | yes |
| activation_auc_0_32 | 2d -> 3d | 1.46094 | [1.36719, 1.49219] | 1.90735e-05 | yes |
| activation_auc_0_32 | 3d -> 5d | -2.75 | [-3.02344, -2.25] | 1.90735e-05 | yes |
| activation_auc_0_32 | 5d -> 5d_shuffled | -4.41406 | [-5.36719, -3.33594] | 0.000160217 | yes |
| activation_auc_0_32 | 5d -> random_graph | -3.44531 | [-4.78906, -2.55469] | 1.90735e-05 | yes |
| half_activation_latency_censored | 1d -> 2d | -4 | [-4, -4] | 1.90735e-05 | yes |
| half_activation_latency_censored | 2d -> 3d | -2 | [-2, -2] | 1.90735e-05 | yes |
| half_activation_latency_censored | 3d -> 5d | 0 | [0, 0] | 1 | no |
| half_activation_latency_censored | 5d -> 5d_shuffled | 0 | [0, 0] | 0.1875 | no |
| half_activation_latency_censored | 5d -> random_graph | 0 | [-0.5, 0] | 0.25 | no |

## V2 first-output latency replication

| contrast | median delta | CI95 | Holm-p | significant |
| --- | ---: | --- | ---: | :---: |
| 1d -> 2d | -10 | [-10, -10] | 9.53674e-06 | yes |
| 2d -> 3d | -3 | [-3, -3] | 9.53674e-06 | yes |
| 3d -> 5d | -1 | [-1, -1] | 9.53674e-06 | yes |
| 5d -> 5d_shuffled | -3 | [-3, -2] | 9.53674e-06 | yes |
| 5d -> random_graph | -3 | [-3, -2] | 9.53674e-06 | yes |

Ceiling-resolution criterion: PASS
V2 latency replication criterion: PASS
Design integrity: PASS

## Claim boundary

This R1 protocol corrects the V3 primary multiple-testing implementation and is an internal preregistered Stage-1 replication/robustness test of RQ-SNN-003/H-SNN-003-B. It does not constitute independent external replication, does not test a 5D advantage, does not establish scaling, cognition or biological equivalence, and creates DATA rather than EVID.

## Local review after pull

Run:
python scripts/verify_stage1_topology_v3_r1.py

Raw data: data/evaluation.json.
Statistics: analysis/statistics.json.
