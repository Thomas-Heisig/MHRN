# MHRN CUDA / D3 Hardware Acceptance — 2026-09-30

**Status:** executable engineering acceptance plan  
**Scientific evidence:** none created by this document  
**Target reference host:** physical NVIDIA RTX 3060 class system

## Purpose

This acceptance combines the two hardware checks that are currently executable
without changing the hardware-verified CUDA kernel:

1. **Wave-4 canonical CPU/CUDA D1/D2** through `CUDABackend`.
2. **Live Builder CPU/CUDA D3c bridge** with a CPU-resident world and CUDA
   neural execution.

The second check is deliberately called a **Builder D3c bridge**. It is not the
canonical Frozen-Environment FE-3 acceptance because the Wave-4
`CUDABackend` is a bounded replay backend and does not yet expose a live
per-tick sensor-input/decoder-action adapter.

## Command

```bash
MHRN_TEST_CUDA_HARDWARE=1 python scripts/run_cuda_hardware_acceptance.py \
  --require-gpu "RTX 3060" \
  --full \
  --include-fe3
```

The runner itself sets `MHRN_TEST_CUDA_HARDWARE=1`; the explicit environment
variable is therefore optional but useful in reproducibility logs.

## Acceptance groups

### WAVE4_D1_D2

Runs the canonical physical cross-backend test:

```text
tests/test_cuda_wave4_backend.py::
  test_physical_cpu_cuda_cross_backend_d1_d2_parity
```

Requirements:

- real CUDA execution;
- exact D1 spike-event parity;
- D2 voltage error within the canonical tolerance;
- no CPU fallback labelled as GPU;
- backend-specific execution fingerprints remain distinct provenance.

### WAVE4_RECURRENT_PLASTICITY_FULL

Enabled by `--full`.

Re-runs the physical recurrent and technical-plasticity acceptance cases. These
remain Engineering Verification. Plasticity semantics are still governed by
the separate learning-contract status.

### BUILDER_D3C_BRIDGE

Enabled by `--include-fe3`.

Runs all seeded variants of:

```text
tests/test_playground_cuda_builder.py::
  test_full_pan_builder_hardware_d3
```

This path uses the existing live Builder loop:

```text
CPU world/body
  -> sensor state
  -> CPU or CUDA neural path
  -> live action
  -> world transition
  -> reward / next sensor state
```

The canonical parity framework compares spikes/state and exact
action/target/reward/body-trajectory outcomes.

A passing bridge demonstrates that the existing live Builder path can produce
matching CPU/CUDA causal behavior on the tested hardware/configuration.

It **does not** demonstrate canonical Frozen-Environment FE-3 because that
specific path does not yet execute from a
`FrozenEnvironmentManifest -> live backend adapter -> DecodeResult ->
ActionCommand` chain.

## Fail-closed FE-3 boundary

The hardware report always emits:

```json
{
  "builder_d3c_bridge": "PASS|FAIL|NOT_REQUESTED",
  "frozen_environment_fe3": "PENDING_LIVE_BACKEND_ADAPTER",
  "full_fe3_accepted": false,
  "scientific_evidence": false
}
```

until the missing live adapter is implemented and tested.

The standalone FE CLI preserves the same boundary:

```bash
python scripts/run_fe_acceptance.py --manifest <fe3.json> --require-cuda
```

must fail while the canonical live adapter is unavailable.

## Missing canonical adapter

The next implementation gate is a backend-neutral live adapter with the
causal surface:

```text
FrozenEnvironment observation
  -> canonical sensor/BoundaryFrame encoding
  -> backend step
  -> canonical readout / DecodeResult
  -> ActionCommand
  -> FrozenWorldSession.step
```

Requirements:

- no precomputed future sensor sequence for FE-3;
- no backend reset between ticks;
- continuation state survives every tick;
- same manifest/config/seed for CPU and CUDA;
- exact D3c trajectory comparison through
  `exact_frozen_environment_parity`;
- no Playground import from canonical runtime/verification code.

## Evidence boundary

A green hardware acceptance is a stronger **Engineering Verification** artifact.
It does not create DATA or EVID and does not establish PAN validity, learning
validity, biological equivalence, autonomy, or behavioral superiority.
