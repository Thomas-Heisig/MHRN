# Implementation audit — EXP-GEN-0041

**Date:** 2026-09-16  
**Type:** post-hoc implementation audit  
**Historical DATA:** unchanged  
**Evidence promotion:** blocked pending rerun under corrected firing-rate semantics and Human Review

## Finding

A post-execution code review identified a defect in `src/core/neuron.py` as used by the frozen EXP-GEN-0041 execution. The historical firing-rate estimator updated only on spikes, derived `dt` from `_last_update_tick`, and `_last_update_tick` was advanced on every simulated tick. Under ordinary consecutive ticks this made `dt` effectively 1 while `_spike_count_window` accumulated. The resulting `firing_rate_estimate` therefore did not represent a firing rate in Hz.

`_apply_homeostasis()` compares this estimator directly with `target_rate_hz`. The experiment configuration did not explicitly disable homeostasis, so the canonical `NeuronConfig` default (`enable_homeostasis=True`) applied. Consequently, the defect could affect membrane trajectories in active conditions through threshold adaptation.

## Scientific consequence

The original raw observations, manifest, preregistration, hashes, and automated criteria evaluation remain historical records and MUST NOT be rewritten. However, EXP-GEN-0041 must not be promoted as clean confirmatory evidence for H-SNN-006-A without a new preregistered execution using the corrected implementation.

The previously observed facts remain facts about the historical implementation: the run completed, states remained finite, topology remained unchanged, and the recorded stability criteria were satisfied under that implementation. What is no longer justified is treating those trajectories as evidence from a correctly unit-calibrated homeostatic firing-rate mechanism.

## Required follow-up

1. Merge the firing-rate implementation fix with regression tests.
2. Preserve EXP-GEN-0041 unchanged.
3. Create a new experiment ID for the corrected-code replication; do not overwrite or silently replace EXP-GEN-0041.
4. Use a new preregistration/version or an explicit implementation-correction replication contract that records the changed neuron semantics.
5. Compare the corrected replication with EXP-GEN-0041 and report whether the stability conclusion is robust to the defect fix.
6. Keep evidence status at `HUMAN_REVIEW_REQUIRED` until the corrected replication and Human Review are complete.
