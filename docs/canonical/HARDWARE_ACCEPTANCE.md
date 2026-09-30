# Canonical CUDA / Frozen-Environment Hardware Acceptance

**Status:** executable engineering acceptance contract  
**Scientific evidence:** none created by this document  
**Hardware target:** physical NVIDIA GPU; RTX 3060 is the current reference host

## Purpose

This contract separates three engineering checks that must not be conflated:

1. Wave-4 CPU/CUDA D1/D2 backend parity;
2. the historical Playground Builder D3c bridge;
3. canonical Frozen-Environment FE-3 CPU/CUDA D3c parity.

The third check is now wired through the same canonical CUDABackend and FrozenWorldSession contracts. No second CUDA closed-loop backend is introduced.

## Versioned FE-3 manifest

The first physical FE-3 acceptance uses:

`research/verification/frozen_environment/FE3_DETERMINISTIC_TARGET_V1.json`

The artifact is self-verifying and declares manifest SHA-256:

`e0356fcfafb5b9af37b080754ba00877f60c662243a262a3bc348e310c092e35`

The manifest freezes environment identity/configuration, initial world state, RNG provenance, sensor schedule, action schema, reward contract and episode policy. Sensor BoundaryFrames remain live causal outputs of the frozen world; they are deterministically reconstructed and hashed per tick.

## Live backend contract

CPUReferenceBackend and CUDABackend both implement the optional LiveInputExecutionBackend extension. Per tick:

1. FrozenWorldSession exposes the current exact world state.
2. The FE-3 adapter creates a canonical BoundaryFrame.
3. The state is encoded into one deterministic external-current row.
4. The backend advances exactly the current continuation tick.
5. The resulting spikes are decoded into ActionCommand.
6. FrozenWorldSession applies the action to the world and records reward/body state.
7. The next sensor state is therefore causally dependent on the backend action.

CUDABackend remains a bounded replay reference internally. Adding a live input row changes host-side canonical input data only; the hardware-verified recurrent CUDA kernel is not modified by this FE-3 integration.

## Acceptance command

```bash
MHRN_TEST_CUDA_HARDWARE=1 python scripts/run_cuda_hardware_acceptance.py \
  --require-gpu "RTX 3060" \
  --full \
  --include-fe3
```

`--include-fe3` adds the canonical FE-3 CPU/CUDA run and the historical Builder D3c bridge. It does not disable Wave-4 checks.

## Exact FE-3 acceptance conditions

Canonical FE-3 passes only when:

- the versioned manifest hash is identical;
- the live-input fingerprint is identical;
- canonical D3c FrozenEnvironment trajectory parity passes exactly;
- all invoked hardware acceptance selections pass.

CPU and CUDA **execution fingerprints are expected to differ**. The execution fingerprint includes backend identity/version by design. Cross-backend equality is expressed by shared configuration/input provenance and parity results, not by erasing backend identity.

## Output artifacts

A hardware run writes:

- `docs/canonical/HARDWARE_ACCEPTANCE_<date>.json`
- `docs/canonical/HARDWARE_ACCEPTANCE_<date>.md`

The generated Markdown explicitly records the interpretation boundary. A dated artifact is not committed automatically; it should be reviewed and committed only after a real physical run.

## Interpretation boundary

Passing this contract means Engineering Verification only.

It does **not** establish:

- scientific DATA or EVID;
- a speedup claim;
- PAN hyperstate equivalence;
- structural plasticity equivalence;
- canonical learning-rule equivalence;
- real-world autonomy or cognitive capability.

The Builder D3c bridge and canonical Frozen-Environment FE-3 remain separately named in reports so that one cannot silently stand in for the other.
