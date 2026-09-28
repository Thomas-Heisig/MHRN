# CUDA-1.6 integration: real hybrid Builder execution

`neuron_backend=cuda_membrane` executes LIF, AdEx or PAN-AdEx membrane updates on the GPU inside the actual Builder loop. A context, module and device allocations are reused across the bounded run. Per-neuron parameters, active/dead/refractory masks, CPU-delivered synaptic current and current PAN/environment feedback are honored each tick. Outputs return to the existing PAN, plasticity, structural-growth, action and body logic.

This is an explicit **hybrid integration**, not full GPU PAN. Synapses, eligibility, policy learning, hyperstate, dynamic topology and body physics remain on the CPU in this execution path. The separate CUDA-1.5 plasticity kernel remains a bounded reference. There is no speedup claim for a path that transfers state each tick. Persistent GPU state, live-session GPU execution, full GPU plasticity/world integration and multi-GPU work remain roadmap stages.

The Builder selector and exports preserve the backend choice. Unsupported models fail validation. CUDA absence/compile/launch failures propagate; no CPU fallback reports GPU success. Live sessions explicitly reject this Builder-only option. The existing shared API worker/rate bounds cover Builder runs and their D3 comparison endpoint.

## D3 acceptance

`POST /api/playground/cuda/builder-parity` runs matched CPU and CUDA-membrane Builders (at most 256 neurons and 4096 edges). It compares full spike-stream digests, sampled voltage errors, complete action/target/reward sequences and a digest of every physical body frame, including frames older than the 128-frame UI replay limit. Missing actions or invalid/non-finite state cannot pass. The result names the hybrid scope and `full_gpu_pan=false`.

Three RTX 3060 seeds (12345, 42, 777), each with the 256-neuron / 2048-edge default and 2000 ticks, passed actual Builder behavioral parity. Actions, target rewards and complete physical body trajectories were exact. The hardware test matrix plus initial three non-hardware checks passed in 71.99 seconds. Additional failure-injection tests cover allocation cleanup on copy/launch/synchronization errors; no-GPU CI skips only physical GPU tests.

The membrane kernel assembles with 37 registers, zero spill stores/loads and no stack. CI assembles it alongside the gate, recurrent and plasticity kernels. Eight Chromium workspace scenarios passed, including explicit backend selection, GPU failure display and D3 endpoint wiring.
