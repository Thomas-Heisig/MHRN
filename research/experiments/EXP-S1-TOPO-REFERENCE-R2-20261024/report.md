# Stage-1 Brian2 reference R2 — executed 24 October 2026

**Result: PARTIAL_REPLICATION at DATA-analysis level. Human scientific review: PENDING.**

All 120 registered runs (20 fresh seeds × six conditions, 128 ticks, 64 neurons,
246 edges) completed. The frozen verifier reports design integrity passed,
five of five primary criteria passed, no direction reversals, no confidence
interval outside or spanning the equivalence bounds, and five of five secondary
AUC directions reproduced. No replacement seeds, retuning or early stopping.

## Primary results

Differences are right minus left for censored first-output latency, in ticks
(registered dt = 1 ms). Negative values mean the right condition reaches the
output earlier. Tests are the frozen two-sided exact paired sign tests, with
Holm adjustment across the five contrasts. Intervals are the preregistered
5,000-resample paired median bootstrap intervals.

| Contrast | Median difference | 95% bootstrap CI | Frozen equivalence bound | Holm p |
| --- | ---: | --- | --- | ---: |
| 1d → 2d | -10 | [-10.0, -10.0] | [-15.0, -5.0] | 9.5367432e-06 |
| 2d → 3d | -3 | [-3.0, -3.0] | [-4.5, -1.5] | 9.5367432e-06 |
| 3d → 5d | -1 | [-1.0, -1.0] | [-1.5, -0.5] | 9.5367432e-06 |
| 5d → 5d_shuffled | -3 | [-3.0, -2.5] | [-4.5, -1.5] | 9.5367432e-06 |
| 5d → random_graph | -3 | [-3.0, -2.5] | [-3.75, -1.25] | 9.5367432e-06 |

## Interpretation and limits

5D reaches the output a median one tick earlier than 3D, but the shuffled-5D
and random-graph controls reach it a median three ticks earlier than 5D.
This result does **not** establish universal superiority of a 5D geometry.
The 3D→5D secondary early-activation AUC difference is **−3.4765625**: 5D has
lower early cumulative recruitment here despite its earlier first output.
This distinction must be retained when interpreting the separately planned
matched-5D study whose primary endpoint is activation AUC.

The degenerate bootstrap intervals reflect discrete outcomes and concentrated
paired differences, not absence of all uncertainty. The 3D→5D sign test has
19 non-tied pairs; the other four contrasts have 20. Seeds vary realizations
within this fixed 64-neuron construction; they do not sample arbitrary tasks,
network scales or biological systems. Brian2 is a separate implementation,
but authorship/project control are shared. Full independent external replication
is not established. EVID and maturity criteria have not been promoted.

## Provenance and verification

Executed source: `e5d2fe71bd755b2ace7f12c80ba4c4624913a610`, the exact source
bound by `PREREG-S1-TOPO-REFERENCE-R2.freeze.json` and preserved in main's history.
The main integration point before this campaign is `6bb97fb9`. A separate clean
checkout preserves the frozen test and runner bytes instead of silently replacing
them with subsequent formatting edits. Frozen-file hashes and the original
pre-status-update preregistration hash were checked before execution.

The user's instruction to begin experiments was recorded before execution;
the agent selected this ready protocol. That instruction is an execution
commission, not an assertion that the user performed a scientific review.
The immutable preregistration's historical authorization flag is unchanged;
the separate receipt binds this invocation to the frozen source and runner.

Python 3.13.14, Brian2 2.10.1, Windows. Exact environment, commands, UTC start/end,
eight passing contract tests, seed-freshness and independence checks are archived.
The raw runner completed in about 525 seconds. Its source tree remained clean.
No reference DATA existed before this execution. R1 remains aborted and unused.

The frozen verifier ran only after raw DATA were persisted. A separate arithmetic
audit reconstructed cumulative activation, latency and spike counts from all 120
spike traces and recomputed all sign tests and Holm corrections successfully.
This is an internal consistency audit, not independent scientific peer review.

`raw-data-and-provenance.zip` preserves the exact original bytes, including the
1,118,043-byte raw JSON, environment receipt, executed driver, audit script and
frozen protocol record. `archive-index.json` binds every archive member by size
and SHA-256. The adjacent JSON files are UTF-8/LF presentation copies; the archive
is the authority for byte-exact reproduction. Extract it outside a checkout,
restore the recorded source commit and environment, and use the recorded commands.
Do not overwrite this run or reuse its evaluation seeds as fresh seeds.

## Next experimental work

1. Implement and validate the dedicated runner for the already frozen matched-5D
   design, preserving its AUC primary outcome and all 30 registered seeds.
2. Finish the executable CPU self-parity construction/config freeze before its
   20 paired runs; preserve its separate scope from CPU/CUDA equivalence.
3. Complete byte accounting, restore tests and canonical RQ/H admission for the
   10% memory-compression protocol before its prospective evaluation.
