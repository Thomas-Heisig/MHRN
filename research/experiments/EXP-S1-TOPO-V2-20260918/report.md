# EXP-S1-TOPO-V2-20260918: topology_propagation_v2

Stage 1 - Kleines SNN
Research question: RQ-SNN-003
Hypothesis: H-SNN-003-B
Source freeze: 2f81bce18e57e2ec835d387a470ce1ca4e5b38c2
Clean before execution: True
Data role: DATA; no automatic EVID promotion.

## Activity calibration

| weight | gate |
| ---: | :---: |
| 55.0 | PASS |

Chosen weight: 55.0

## Status: SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL

| condition | n | active fraction | output reach | first output latency | spikes | delivered events |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1d | 20 | 1.0000 | 1.0000 | 19.00 | 401.00 | 1536.00 |
| 2d | 20 | 1.0000 | 1.0000 | 9.00 | 363.00 | 1358.00 |
| 3d | 20 | 1.0000 | 1.0000 | 6.00 | 281.00 | 1036.00 |
| 5d | 20 | 0.8750 | 1.0000 | 5.00 | 181.00 | 649.50 |
| 5d_shuffled | 20 | 0.7734 | 1.0000 | 2.00 | 179.50 | 617.00 |
| random_graph | 20 | 0.7188 | 1.0000 | 2.00 | 165.50 | 563.00 |

## Preregistered primary contrasts

| endpoint | contrast | median delta | CI95 | Holm-p | significant |
| --- | --- | ---: | --- | ---: | :---: |
| active_fraction | 1d -> 2d | 0 | [0, 0] | 1 | no |
| active_fraction | 2d -> 3d | 0 | [0, 0] | 1 | no |
| active_fraction | 3d -> 5d | -0.125 | [-0.15625, -0.101562] | 1.90735e-05 | yes |
| active_fraction | 5d -> 5d_shuffled | -0.117188 | [-0.140625, -0.101562] | 0.00120735 | yes |
| active_fraction | 5d -> random_graph | -0.148438 | [-0.195312, -0.109375] | 1.90735e-05 | yes |
| first_output_latency_censored | 1d -> 2d | -10 | [-10, -10] | 1.90735e-05 | yes |
| first_output_latency_censored | 2d -> 3d | -3 | [-3, -3] | 1.90735e-05 | yes |
| first_output_latency_censored | 3d -> 5d | -1 | [-1, -1] | 1.90735e-05 | yes |
| first_output_latency_censored | 5d -> 5d_shuffled | -3 | [-3, -3] | 1.90735e-05 | yes |
| first_output_latency_censored | 5d -> random_graph | -3 | [-3, -2] | 1.90735e-05 | yes |

A significant topology difference is not a claim that 5D is superior.

## Integrity

Design checks: PASS
Expected edges per evaluation run: 246

## Local review after pull

Run:
python scripts/verify_stage1_topology_v2.py

Raw data: data/calibration.json and data/evaluation.json.
Statistics: analysis/statistics.json.

## Claim boundary

This protocol tests RQ-SNN-003/H-SNN-003-B for a 64-neuron Stage-1 topology-sensitive propagation regime. It is not evidence for RQ-5D-005/H-5D-005-A, does not test a 5D advantage, does not establish scaling, cognition, biological equivalence or independent replication, and creates DATA rather than EVID.
