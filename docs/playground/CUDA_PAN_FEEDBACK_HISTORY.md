# Resident PAN feedback history and source selection

The real cuda_pan Builder now keeps the feedback population history in a 66-slot device ring. Population reduction writes its result into the next slot. A source kernel selects the current population or delayed retained entry and applies population/layer/subset/hypervector shaping before the existing projection kernel. Host source-vector computation is removed from the ordinary GPU path.

Availability follows the CPU's retained length, not just the ring capacity. Shrinking the configured delay discards old availability; increasing it cannot resurrect forgotten entries still physically present in ring memory. Delay 0 uses the current population; delays 1–64 use zero until a sufficiently old retained sample exists. Normal stepping uploads neither population nor history. Initial state and validated external edits synchronize both buffers explicitly; host mirrors remain available for diagnostics and existing APIs.

Shape, finite-value and strict integer-delay checks precede transfers. The shared context owns cleanup. D3 records source-kernel calls and requires them to match GPU projection calls; the Run component table and diagnostics declare source/history as GPU-owned. Disabled PAN feedback remains disabled.

Validation covers a 155-step ring wrap with 64→0→64 delay changes, all four source transforms, zero startup/forgotten history, no ordinary history uploads, synchronized external edits, malformed/NaN history and invalid delays. The 96-mode projection matrix and an actual Builder D3 with delay 64 plus hypervector source exercise integration. Full PAN D3 remains part of the hardware acceptance set. Complete session checkpoint/restore and canonical controller integration are separate work; no speedup or full CUDA-MHRN claim is made.

## Local hardware verification — 24 October 2026

On the local working tree based on `17ba8cc5`, an NVIDIA GeForce RTX 3060
(driver 610.88) passed all 51 tests in the feedback-history, PAN-state,
Builder, Builder-synapses, neuron-traces and delay-queue test modules with
`MHRN_TEST_CUDA_HARDWARE=1` (263.10 seconds; no skipped tests).
This verifies the scoped integration on this device. It is an uncommitted
engineering check, not a release freeze, performance comparison or scientific EVID.
