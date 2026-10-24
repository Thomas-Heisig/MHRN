# Matched 5D ablation R2 — design freeze

Date: 2026-10-24. **FROZEN_DESIGN_ONLY; execution_authorized=false.**
Binding: `RQ-5D-005 / H-5D-005-A`. This prospective design complements, and
does not overwrite, `PREREG-5D-005` or historical Stage-1 studies. It does
not unblock the failed recruitment-matching gate of efficiency R1.

## Frozen design

Six arms: 1d=(64,1,1,1,1), 2d=(8,8,1,1,1), 3d=(4,4,4,1,1),
5d=(4,2,2,2,2), 5d_shuffled, random_graph. Every arm has 64 neurons and
246 directed acyclic edges: each source i has min(4,63-i) outgoing edges.
Coordinates, normalized distances, deterministic seed-based tie breaking,
coordinate shuffle and random-target sampling use `all_coords`,
`canonical_coords`, `normalized_distance`, `edge_list` and `build_network`
from `scripts/run_stage1_topology_v2.py`, bound by hash in the design freeze.
Record realized edge lists and degree sequences. Edge count and out-degree
are matched; in-degree, path lengths and graph geometry may differ and are
the intervention, not hidden matching assumptions. This is a comparison of
specific graph construction rules, not a pure effect of abstract dimension.

All synapses weight 55, delay 1 tick; input labels 0–3, output labels 60–63;
one 100-current impulse at tick 0; 128 evaluation ticks; identical initial
neuron parameters from `configs/learning_experiment.yaml`. No learning,
structural plasticity, optimizer, warm-up training or hyperparameter search:
all have exactly zero updates/trials. Weight 55 was chosen historically;
it is not retuned against these new outcomes. Seeds 96001–96030, paired across
arms, each condition reconstructed independently. No calibration on these
seeds. Equal training/search effort means zero in every arm, not unknown.

Primary outcome: sum of cumulative active-neuron fractions for the first 32
ticks, using the time-resolved observation convention in
`run_stage1_topology_v3_r1.py` (range 0–32, not divided by window length).
Primary contrast: 5d minus 3d. Fixed directional claim of benefit requires a
positive paired mean and one-sided exact sign-test p<0.05 (ties excluded,
effective n reported). Thirty complete pairs mandatory; zero non-tied pairs
give p=1. No secondary contrast may rescue the primary. Report a 95% paired
bootstrap interval (20,000 resamples, RNG seed 20261024) descriptively.
All other arms, half-activation latency, first-output latency and total spikes
are secondary/descriptive. This endpoint measures early activation, not task
accuracy, intelligence or energy efficiency. A faster graph need not be better.

Resource ceilings: one CPU worker, float64 scalar simulation; no GPU;
2 GiB peak process RSS; 60 seconds/arm/seed; 3 CPU hours for all 180 runs;
2 GiB saved output. Record wall time/RSS at one-second intervals. Stop and
retain partial data on exceeded resources, NaN, invalid graph, count mismatch
or runtime failure. No replacement seeds, automatic reruns or parameter
adjustment. Invalid/incomplete runs imply NOT_TESTED, not no 5D effect.

Before evaluation a dedicated R2 runner must enforce this design, run only
synthetic integrity fixtures, verify evaluation-seed freshness, record all
source/config/environment hashes and obtain execution authorization. The
bound historical V3 runner must NOT be invoked directly: its hard-coded
seed plan and multiple-primary-endpoint analysis differ from this R2 plan.
Design freeze therefore does not claim executable freeze or completed DATA.

The freeze record binds this document and source dependencies before any R2
evaluation. Changes require a versioned amendment and new hashes. A technical
or scientific review may reject this design; freezing does not certify its
adequacy, power or independence.
