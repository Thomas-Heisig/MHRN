# EXP-S6-SEM-CL-003 — Replay Dose × Representation

**Result classification:** `H1_negative_H2_negative`
**H1 passed:** False
**H2 passed:** False

This report is DATA ONLY. Human EVID review is required.

Complete paired seeds: 12

## C1_S20_minus_R20_accuracy
- mean: +0.021750
- minimum effect: +0.030000
- 95% bootstrap CI: +0.001916 to +0.042500
- paired sign-flip p: 0.072754
- passed: False

## C2_R20_minus_S20_forgetting
- mean: +0.027448
- minimum effect: +0.050000
- 95% bootstrap CI: +0.002500 to +0.053542
- paired sign-flip p: 0.070801
- passed: False

## C3_S20_minus_X20_accuracy
- mean: +0.148958
- minimum effect: +0.030000
- 95% bootstrap CI: +0.140208 to +0.157417
- paired sign-flip p: 0.000488
- passed: True

## C4_dose_interaction_accuracy
- mean: +0.007542
- minimum effect: +0.015000
- 95% bootstrap CI: -0.002875 to +0.018958
- paired sign-flip p: 0.238281
- passed: False

## Secondary: S40_minus_R40_accuracy
- mean: +0.029958
- 95% bootstrap CI: +0.006500 to +0.054625
- paired sign-flip p: 0.047852

## Secondary: R40_minus_S40_forgetting
- mean: +0.035990
- 95% bootstrap CI: +0.007240 to +0.066408
- paired sign-flip p: 0.053711

## Dose table

```json
{
  "05": {
    "raw_minus_semantic_forgetting_mean": 0.018020833333333347,
    "semantic_minus_raw_accuracy_mean": 0.014208333333333337
  },
  "20": {
    "raw_minus_semantic_forgetting_mean": 0.027447916666666655,
    "semantic_minus_raw_accuracy_mean": 0.021750000000000005
  },
  "40": {
    "raw_minus_semantic_forgetting_mean": 0.03598958333333333,
    "semantic_minus_raw_accuracy_mean": 0.029958333333333326
  }
}
```

## Governance
- automatic DATA→EVID promotion: disabled
- human review: required
- negative/null outcomes are retained
