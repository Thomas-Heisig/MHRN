# Unseen-disturbance closed-loop/yoked comparison

2026-10-24. **COMPLETED_EXPLORATORY_DATA; HUMAN_REVIEW_PENDING.**
RQ-EMB-001 / H-EMB-001-B; protocol PREREG-EMB001B-UNSEEN-V4.
Source frozen before execution: `fdfd0568f096b44e91ac16cf57299fcc823fca32`.
The clean-source check passed before and after execution. CPython 3.13.14,
Windows 11, PYTHONHASHSEED=0; complete environment/commands in `freeze.json`
and `pip-freeze.txt`. No historical DATA or EVID status was changed.

## Intervention and result

For each of 20 seeds, first record an unperturbed closed-loop sensor tape.
Replay receives that frozen tape; live feedback receives the actual current
body sensors. Both challenged bodies receive the same external torque,
±0.003 Nm over ticks 250–499 (ten seeds per sign). Six conditions and 1,000
ticks per condition produce 120 runs. The target, initial neural/body state,
graph, fixed receptor and decoder parameters are matched within seed.

Primary endpoint is tracking RMSE on ticks 250–999. Mean values in radians:

| Condition | RMSE |
| --- | ---: |
| Live closed-loop, challenged | 0.14611949 |
| Frozen yoked tape, challenged | 0.34670261 |
| Feedback absent, challenged | 0.52945445 |
| PD-only controller, challenged | 0.18385742 |
| Unperturbed donor | 0.14016236 |
| Unperturbed yoked sentinel | 0.14016236 |

Primary paired difference (yoked minus live) is positive for 20/20 seeds:
mean 0.20058312 rad, range 0.15286834–0.24810907. Sign-stratified means are
0.24449186 for positive and 0.15667437 for negative torque. These are
descriptive paired observations, not p-values or population-level confidence.

All integrity checks passed: 120 complete error-free runs; equal initial
states and graph; exact unperturbed donor/sentinel traces; challenged replay
observes the frozen donor tape and emits exactly the donor's motor commands;
its physical trajectory nevertheless changes under the disturbance. Feedback
absent receives zeros. The same explicit schedule is passed to each challenge
arm by the frozen runner. Per-tick traces are retained for audit.

This addresses the earlier exact-yoke equality: replay of a trajectory exposed
to the same disturbance can be observationally equivalent. Here the donor
does not contain the later challenge. Live feedback can depend on the
challenged body, while replay cannot. The result supports this bounded
feedback-contingency effect in the engineered fixture. It does not attribute
the effect to learning or an emergent body schema. The PD arm is an attribution
reference, not a matched neural or optimized-controller benchmark.

## Provenance, packaging and limitations

`outcomes.json`, `integrity.json`, `result.json` contain compact results.
`raw-traces.zip` stores all donor and six-arm per-seed traces without loss;
`archive-index.json` binds the ZIP and `sha256sums.json` binds its original
uncompressed members as well as the remaining execution artifacts. All
checksums were verified after packaging. The 80.8 MB original output remains
outside the repository; compression occurred only after measurement.

The resource/time ceiling was checked after each paired-seed block, not by
an OS-enforced interruption mid-run. No ceiling was exceeded. This exploratory
run uses a fixed synthetic six-neuron controller on one machine and does not
establish biological equivalence, real-device transfer, general robustness,
independent replication or confirmatory EVID. Human scientific review and
canonical evidence promotion remain pending.
