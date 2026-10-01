# Resident CUDA neuron traces

The actual cuda_pan Builder now owns pre/post traces and last-spike ticks in device memory throughout a run. A begin phase applies the original 0.95 decay before edge plasticity. The commit phase adds spikes and updates last-spike times after emission. The per-edge CUDA rules still reconstruct ascending-neuron event order for simultaneous spikes; moving trace storage must not change that ordering.

The driver requires monotonically increasing uint32 ticks and exactly one begin/commit pair. Invalid indices, duplicate spikes and incorrect phases are rejected before transfer. Initial buffers are uploaded once; later HtoD copies carry only the spike mask. Host readback remains necessary for existing edge descriptors, diagnostics and host-owned algorithms. This is device ownership of trace evolution, not a complete persistent kernel or speedup claim.

Lifecycle follows the shared CUDA context with reverse cleanup, including allocation failure. The Run component table, GPU preset description, diagnostics and D3 execution counts reflect trace ownership. The main CI assembles the kernel with ptxas.

Validation includes a partial block of 129 neurons over 150 ticks with exact CPU trace/timestamp comparisons in both phases, and verifies no trace-state uploads occur after initialization. Actual Builder tests cover seven plasticity modes, full PAN D3 and event-to-tick transitions. ptxas uses 16 registers, zero stack and zero spills. Complete session snapshots/restore, source-history/population ownership and canonical RuntimeController integration remain separate roadmap work.
