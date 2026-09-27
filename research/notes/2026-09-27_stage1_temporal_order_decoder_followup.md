# Methodological follow-up — Temporal-Order decoder stress test

**Date:** 2026-09-27  
**Source experiment:** `EXP-S1-TEMP-PROMO-R1-20260927`  
**Status:** exploratory follow-up required  
**Evidence role:** none; does not modify the present Human Review or future EVID registration

## Resolved point

The preregistered simultaneous condition is not part of the forward/reverse order-accuracy endpoint. It is a separate non-inferential task-adequacy control.

The frozen decoder defines:
- forward: output A first;
- reverse: output B first;
- simultaneous: first A and B output spikes on the same tick.

The promotion DATA show simultaneous output at equal first-output ticks in the intact arm, so `intact_simultaneous_success_fraction = 1.0` is correct under the preregistered decoder. It is not a chance-level order-decoding score.

## Remaining methodological concern

The task saturates:
- intact forward/reverse accuracy = 1.0;
- identity-destroyed accuracy = 0.0;
- simultaneous-control success = 1.0;
- paired delta = 1.0 for all 20 seeds.

This strongly supports the bounded frozen task, but provides little resolution on robustness margin or whether a simpler deterministic shortcut could also solve the task.

## Prospective follow-up candidates

A future preregistered stress test should consider:
1. several nonzero order gaps, including near-simultaneous gaps;
2. physical A/B channel-label swaps after network construction;
3. balanced amplitude/current perturbations independent of logical order;
4. held-out or blinded decoder mapping where feasible;
5. increased path asymmetry controls;
6. evaluation of whether performance degrades smoothly as the order gap approaches zero;
7. an independently implemented decoder family (for example a separately specified threshold/readout rule) to test whether the result depends on the frozen decoder implementation;
8. a counterfactual channel-identity condition in which A and B use identical stimulus profiles and differ only in physical channel position, to separate channel identity from amplitude/profile cues.

These are prospective method-development ideas only. They are not grounds for retroactively changing the current DATA or Human Review unless a later preregistered study produces contradictory evidence.

## Claim boundary

The present Temporal-Order line remains restricted to a six-neuron, four-synapse, two-channel acyclic task. No learning, memory, cognition, general temporal reasoning, biological equivalence or scaling claim follows from it.
