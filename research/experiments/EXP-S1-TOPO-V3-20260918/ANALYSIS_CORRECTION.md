# EXP-S1-TOPO-V3-20260918 — analysis correction notice

**Status:** superseded for confirmatory interpretation by `EXP-S1-TOPO-V3-R1-20260918`  
**DATA policy:** raw DATA, manifest, checksums and original statistics remain unchanged.

## Reason

The V3 execution and integrity checks completed successfully, but the analysis implementation applied Holm correction separately within each primary endpoint family (5 contrasts for `activation_auc_0_32` and 5 contrasts for `half_activation_latency_censored`).

The preregistration required **one Holm correction across all 10 primary time-resolved endpoint/contrast tests**.

This is an analysis-contract implementation error, not a simulation or raw-DATA failure.

## Consequence

- V3 raw DATA remain scientifically useful as an audit trail.
- V3 must not be used as the confirmatory result for the preregistered decision rule.
- No V3 DATA or original analysis artifact is rewritten post hoc.
- R1 uses fresh seeds and the corrected single Holm family across all 10 primary tests.
- The first-output-latency replication family remains a separate preregistered family of 5 tests.

No automatic EVID promotion is permitted.
