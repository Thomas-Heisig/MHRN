# Playground Presets

**Classification:** exploratory Playground only. Presets are configuration hypotheses, not DATA or EVID.

The Builder exposes these presets through **16 · Closed-Loop Presets**. The
Preset Lab additionally provides the two frequently used starting profiles:
`Izhikevich · Referenz` and `PAN · Explorationsprofil`. User-created presets are
stored locally in the browser only.

## Controls and baselines

- `open_loop_baseline`: no action or reward loop; control condition.
- `baseline_heterogeneous`: E/I balance and neuron heterogeneity without a loop.

## Stabilization and channel fixes

- `fix_weight_explosion`: `weight=4`, `weight_decay=0.01`,
  `weight_max_clamp=10`.
- `fix_channel_separation`: separate target, reward, and action channels.
- `fix_weight_and_channels`: combines both corrections.

## Hypothesis experiments

- `feedback_gain_sweep`
- `input_differentiation`
- `credit_assignment_trace`
- `reward_shaping_dense`

## Progressive complexity

- `d1_minimal_closed_loop`
- `d2_full_embodiment_v2`
- `d3_spatial_embodiment_only`

## Diagnostics and robustness

- `e1_diagnose_silence`
- `e2_diagnose_synchrony`
- `e3_diagnose_context_policy`
- `f1_robustness_seed_sweep`
- `f2_robustness_scale_up`
- `f3_robustness_ablation`

## Sanity and special experiments

- `g1_two_action_simple`
- `g2_one_action_trivial`
- `g3_gaba_sweep`
- `g4_feedback_nonlinearity`

## Recommended order

1. `g2_one_action_trivial`
2. `g1_two_action_simple`
3. `fix_weight_explosion`
4. `fix_channel_separation`
5. `fix_weight_and_channels`
6. `d1_minimal_closed_loop`
7. `e3_diagnose_context_policy`
8. `input_differentiation`
9. `credit_assignment_trace`
10. `d2_full_embodiment_v2`

Preset expectations are hypotheses only. A result never promotes itself into the
Research Registry or Scientific Maturity.
