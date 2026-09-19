# EXP-S1-TEMP-ORDER-V2-20260919: two-channel temporal-order task

Stage 1 - Kleines SNN

Research question: RQ-TEMP-002  
Hypothesis: H-TEMP-002-A  
Source freeze: 23549a0b75f7019a6146f8513bf6628505acb079  
Clean before execution: true  
Data role: DATA only; no automatic EVID promotion.

## Protocol correction

The historical V1 runner represented forward as (0,4) and reverse as (4,0), but executed both with membership testing. Both therefore collapsed to the same stimulation ticks. V2 preserves historical bytes and uses two distinguishable input channels plus an information-destroyed matched control.

## Result

**Status: SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL**

| endpoint | result |
| --- | ---: |
| intact order accuracy, median | 1.0000 |
| identity-destroyed order accuracy, median | 0.0000 |
| intact simultaneous success fraction | 1.0000 |
| paired accuracy delta, median | 1.0000 |
| paired delta CI95 | [1.0000, 1.0000] |
| exact paired sign-test p | 1.9073486e-06 |

Design integrity: PASS

## Claim boundary

This Stage-1 task tests whether a small, acyclic six-neuron SNN preserves the temporal order of two distinguishable input channels at designated outputs and whether deliberately destroying channel identity removes that fixed decoding signal. It demonstrates at most scoped technical task function under the registered parameter range. It does not establish learning, memory, cognition, biological equivalence, scaling, 5D superiority, general temporal reasoning, human-reviewed EVID or independent replication.

## Governance

Human review remains required before EVID promotion. AI review does not satisfy that gate. This run is not an independent replication.
