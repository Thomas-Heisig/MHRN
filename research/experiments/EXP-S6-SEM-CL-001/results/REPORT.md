# EXP-S6-SEM-CL-001 — Split-MNIST Semantization Ablation

**Result classification:** `preregistered_positive_result`

This report is DATA ONLY. Human review is required before any claim is promoted.

## Primary comparison

- Baseline final average accuracy: 0.1883
- Semantic final average accuracy: 0.4093
- Accuracy delta: +0.2210 (95% bootstrap CI +0.2076 to +0.2338; sign-flip p=0.001953)
- Baseline mean forgetting: 0.9764
- Semantic mean forgetting: 0.6975
- Forgetting reduction: +0.2789 (95% bootstrap CI +0.2621 to +0.2947; sign-flip p=0.001953)

## Preregistered decision rule

Positive result requires accuracy delta >= 0.03, forgetting reduction >= 0.05, positive 95% paired bootstrap lower bounds, and two-sided paired sign-flip p < 0.05 for both endpoints.

**Primary rule passed:** True

## Governance

- automatic evidence promotion: disabled
- human review: required
- scope: one mechanism, one benchmark, one simple baseline
