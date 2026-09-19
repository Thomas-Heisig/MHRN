# EXP-REC-002-CLEAN-R2-20260919: REC-002 clean-tree R2

Research question: RQ-REC-002  
Hypothesis: H-REC-002-A  
Source freeze: 947e64c757540ca12bbc5eaad012d5a800f05672  
Clean before execution: true  
Runs: 80  
Data role: DATA only; no automatic EVID promotion.

## Reason for R2

The registered REC-002 delay ladder is a semantic DIRECT_MATCH, but the latest 20-seed confirmatory run was provenance-blocked by a dirty source tree. R2 repeats the same registered intervention on the current green source freeze using fresh seeds. Historical DATA are unchanged.

## Result

**Status: SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL**

Primary gates:

{
  "every_treatment_differs_from_delay1": true,
  "full_grid_every_seed": true,
  "treatment_delays_not_all_identical": true
}

Condition signatures:

{
  "loop_delay_1": [
    [
      62,
      10,
      61
    ]
  ],
  "loop_delay_2": [
    [
      252,
      33,
      251
    ]
  ],
  "loop_delay_4": [
    [
      251,
      28,
      250
    ]
  ],
  "loop_delay_8": [
    [
      245,
      20,
      244
    ]
  ]
}

## Inference boundary

No p-values or sampling-based confidence intervals are used. Support is decided by preregistered deterministic within-seed contrasts.

## Claim boundary

This experiment can support only the scoped claim that loop delay changes persistence/propagation metrics in the registered small deterministic recurrent SNN at recurrent weight 100 and a 256-tick observation window. It does not establish memory, cognition, biological equivalence, scaling, a 5D advantage, monotonic superiority of larger delays, human-reviewed EVID or independent replication.

## Gate protection

This experiment branch does not modify src/, configs/, tests/, research/schemas/ or pyproject.toml. Merge is permitted only after experiment verification and pull-request CI are green.

## Governance

Human review remains PENDING. This is not independently authored replication and does not create EVID automatically.
