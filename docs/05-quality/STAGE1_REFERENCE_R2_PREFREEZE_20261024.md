# Stage-1 reference R2 — pre-freeze verification, 24 October 2026

Status: engineering/method validation only; no confirmatory reference DATA,
human evidence decision or independent replication is created by these checks.

## Source restoration

Commit `c6009b4e` reformatted the import in
`reference/stage1_topology_brian2/synapse_probe.py`. Its bytes consequently
ceased to match the historical R1 calibration. The probe was restored from
`28d07e67` only after verifying identical Python ASTs and the exact recorded
SHA-256 `d05bae8f00b97758cb96662acbb0f2e58cd7860776871b5edf6fd4ed09e576da`.
The original calibration and its recorded hash were not changed. A regression
test now guards this byte-preservation contract, including cosmetic edits.

The failed pre-restoration audit remains at
`research/calibrations/CAL-S1-TOPO-REFERENCE-DYNAMICS-REUSE-R2/failed-before-format-restoration-20261024.json`.
The current result is separate in that directory's `result.json`.

## Verified preparation

- Python 3.13.14 and Brian2 2.10.1 in an isolated Windows environment.
- Topology mapping: all 18 cases pass, using calibration seeds separate from evaluation.
- Immutable dynamics reuse: all nine recorded source hashes match; historical
  integrator, reset and synapse artifacts retain their original bytes.
- Independence scan: no forbidden imports or canonical target leakage detected.
- Seed freshness: no collisions at the checked baseline; this check must be
  repeated at the final clean freeze commit.
- R2 preregistration prose now distinguishes its active seed block from the
  earlier R1 block, without changing the registered seed list or decision bounds.

The mapping script supports direct invocation. The freeze script now uses
`sys.executable` for subprocesses and requires an explicit ISO `--freeze-date`,
preventing a new freeze from silently inheriting the draft's September date.

## Freeze and execution boundary

Use a clean, committed tree and Python 3.13 with Brian2 2.10.1. Run the R2
contract/preflight/freeze-CLI tests before:

```text
python scripts/freeze_stage1_topology_reference_r2.py --freeze-date YYYY-MM-DD
```

Supply the actual freeze date. The script refuses a dirty tree or existing
freeze. The freeze must bind the source commit, calibration artifacts, runner,
verifier and preregistered criteria. Its completion is not authorization to run
the reference evaluation: `execution_authorized` stays false. A subsequent
human execution-authorization record must bind the reviewed freeze and runner.
Project-side reference replication can earn partial replication credit only.
