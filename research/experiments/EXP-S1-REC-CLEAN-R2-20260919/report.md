# EXP-S1-REC-CLEAN-R2-20260919: clean-tree recurrence map R2

Stage 1 small-SNN recurrence control / Stage-2 bridge.

Research question: RQ-REC-001  
Hypothesis: H-REC-001-A  
Source freeze: e3e2d63ff2ee1b73fbf37f77aebda2993e6b8fa5  
Clean before execution: true  
Runs: 300  
Data role: DATA only; no automatic EVID promotion.

## Reason for R2

Earlier direct-match REC-001 runs were scientifically useful DATA but Evidence Readiness was blocked by a dirty source tree. R2 repeats the complete registered weight x delay grid prospectively on a clean freeze with fresh seeds. Historical artifacts are not rewritten.

## Result

**Status: SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL**

Primary gates:

{
  "delay_effect_present_every_seed": true,
  "full_grid_every_seed": true,
  "persistent_class_present_every_seed": true,
  "recurrence_extends_response_every_seed": true,
  "transient_class_present_every_seed": true,
  "weight_effect_present_every_seed": true,
  "zero_recurrence_controls_immediate": true
}

Observed persistence classes: immediate_decay, persistent_to_window, transient

## Inference boundary

No p-values or sampling-based confidence intervals are used. The runner is deterministic and the seeds are not assumed to be independent stochastic samples.

## Claim boundary

This experiment tests a small three-neuron SNN under the registered recurrence-weight and delay interventions and can support only the scoped claim that recurrence parameters change persistence/propagation classes in this deterministic operating envelope. It does not establish cognition, memory, biological equivalence, scaling, a 5D advantage, general recurrent-computation superiority, human-reviewed EVID, or independent replication.

## Governance

Human review remains PENDING. This run is not independently authored replication and does not create EVID automatically.
