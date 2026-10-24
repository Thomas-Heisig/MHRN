# Clean-source determinism reproduction — 2026-10-24

The manuscript finding in edition 1.8, section 19.8, is reproduced on
`556dd5e06ac1c3d71c9c00d4c66aa230c72c6007` (tree
`0cca9976a37a82b31109c82d9a212dc13be0249e`). This is a new technical
reproduction of `RQ-DET-001 / H-SNN-003-A`, not a repair of the historical
dirty-tree provenance or an automatic EVID promotion.

## Protocol and result

The unmodified `src.research.experiment_suite.run_ping_v2` ran
`deterministic_replica_v1`: seeds 101, 102, 103; recurrence off/on;
replicas A/B; 256 ticks. Three fresh Python processes used
`PYTHONHASHSEED=0,1,42`, giving 36 runs and 18 A/B pairs.

All A/B pairs had equal complete metrics, spike sequences and initial/final
state digests. Every run completed 256 ticks without a runtime error.
The three complete serialized process outputs were byte-identical.

| Arm | Spikes | Delivered synaptic events | Recurrent events | Propagation depth |
| --- | ---: | ---: | ---: | ---: |
| Recurrence off | 3 | 2 | 0 | 1 |
| Recurrence on | 33 | 33 | 10 | 61 |

These totals match both the manuscript and the immutable raw outputs of
`EXP-BATCH-20260914074039-03`. The configuration SHA-256 is exactly the
historically recorded `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`.
The historical dirty working tree cannot be reconstructed from its commit
alone; the new run deliberately identifies its own exact source commit.

## Provenance and repeat command

The checkout was clean before and after execution. Before running, the
harness compared every tracked file under `src/` and `configs/` byte-for-byte
by Git blob hash and recorded SHA-256 hashes. Windows checkout newline
conversion initially failed this preflight (no experiment ran). Ten affected
files were restored directly from their committed blobs, and Git's index
stat cache was refreshed without changing the index tree. A second preflight
stopped on that stale status before the refresh. The successful invocation
and all worker commands are recorded in the artifacts.

Environment: Windows, CPython 3.13.14; the existing isolated
`reference-r2-env` was used. Exact OS/interpreter details and all installed
package versions are recorded, rather than assuming an empty environment.
Outputs were written outside the tested checkout. This report and the TODO
change were added only after the successful clean-tree run.

To repeat, create a separate checkout of the source commit above, ensure
source/config bytes match its Git blobs, and invoke the archived harness
from outside that checkout, with a new output directory:

```powershell
& <python-3.13-environment>/Scripts/python.exe -B <report>/reproduce.py <clean-checkout> <new-output-directory>
```

Use the package versions in `artifacts/pip-freeze.txt`. The harness refuses
a dirty tree, differing source bytes, a changed historical configuration,
or an existing output directory. It freezes metadata before worker execution.
No repository runtime code was modified for the measurement.

## Artifacts and limits

- `reproduce.py`: exact executed harness, bound by SHA-256 in the freeze.
- `artifacts/freeze.json`: source commit/tree, source/config hashes,
  pre-execution timestamp, command and interpreter/platform details.
- `artifacts/pip-freeze.txt`: environment package versions.
- `artifacts/processes.json`: exact worker commands, hash seeds and exit codes.
- `artifacts/runs-hashseed-*.json`: all 36 raw results.
- `artifacts/stdout-*.txt`, `stderr-*.txt`: worker logs, empty on success.
- `artifacts/result.json`: six pair comparisons for the first process,
  full-output equality across all three processes, and clean post-run status.
- `artifacts/sha256sums.json`: checksums of the recorded result files.

This is a same-machine, same-toolchain reproduction of a small fixed
protocol. Three seeds are not evidence of independent randomized network
realizations. Cross-platform determinism, arbitrary network sizes/time
horizons, independent scientific replication and formal human EVID review
are not established. Historical DATA, registry evidence status and the
published manuscript remain unchanged.
