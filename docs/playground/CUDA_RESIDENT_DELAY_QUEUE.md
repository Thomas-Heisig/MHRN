# Resident CUDA delay queue

The actual `cuda_pan` Builder keeps its 65-slot pending-current ring on the device throughout a run. A consume kernel returns and clears the current slot. An enqueue kernel gives each target neuron one writer that visits the supplied emission sequence in original order. No floating-point atomics reorder additions. Stored values are emitted amplitudes; later weight changes cannot modify them.

All delays remain 1–64. The slot formula reduces the uint32 tick before adding delay, avoiding overflow near the maximum tick. Invalid shapes, indices, delays, non-finite values and accumulation overflow fail closed. Fixed buffers are reused and cleaned with the shared context. Each normal tick transfers the current input vector and new events, not the full ring.

Full snapshots are read only for execution-policy transition bookkeeping and final diagnostics. The queue has explicit validated snapshot/restore of all 65 slots; the caller must restore at the same external simulation tick. This is **queue state only**, not a full canonical checkpoint or persistence across complete sessions. Membrane/PAN/synaptic host mirrors and other host-owned state still have per-tick transfers. CUDA-2 is therefore not claimed complete.

Validation covers partial blocks (129 neurons), repeated delay-64 wrap, mixed positive/negative same-target emissions, exact insertion order, snapshot/reset/restore continuation, uint32 boundary slot calculation, malformed input, accumulation overflow and partial-allocation cleanup. Actual full PAN D3 compares the complete final ring and requires GPU queue consumption for every membrane tick. Body, policy, RNG, neuron traces and structural mutation remain CPU-owned.

## Measured validation (RTX 3060)

The resident-queue/PAN run passed 16 physical-GPU and software tests, including three complete 256-neuron, 2048-edge, 2000-tick D3 seeds. An additional real Builder event-to-tick transition regression passed, retaining pending-current parity and transition integrity. After integrating current develop, the focused software suite passed 123 tests (19 explicitly opt-in GPU cases skipped in that software-only invocation); 12 browser tests passed. The real HTTP D3 check consumed 128 GPU queue ticks with exact spikes, actions, body trajectory, RNG and final currents. PAN maximum error was 2.78e-17.

Black, Ruff and strict Pyright for the new driver pass. CUDA 13 ptxas reports 10 registers for consume and 22 for enqueue, with no stack or spills. These are correctness and resource measurements, not a throughput speedup claim.
