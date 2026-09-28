# Actual Builder GPU emission, STP and live reward

The `cuda_pan` Builder path now computes emitted amplitude, inhibitory/GABA scaling, PAN amplitude scaling, Bernoulli STP release/depletion, resource recovery, weight decay/clamp and live target/posture reward weight updates on CUDA. Kernels share the existing module/context and bounded reusable buffers (at most 20,000 edges).

The **Builder RNG remains the same host traversal stream**. A draw is consumed exactly once for each emitted edge when STP is active, in the original source/adjacency order. CUDA receives those draws; it does not substitute the independent counter RNG used by the separate CUDA-1.5 reference. No draw occurs for inactive STP. The strict comparison at the release threshold is preserved. Host code adds returned emission-time amplitudes to the existing delay ring in original order, so later weight changes do not retroactively change queued current.

Live reward updates retain the existing CPU contract: delayed delivered rewards and posture rewards respect the eligibility credit window, while the existing immediate reward branch updates all edges. Maximum clamps are retained per branch. This is a faithful port, not a change to the learning rule. STDP/triplet/eligibility evolution, topology, delay queue, body/reward computation and policy remain CPU-owned. The component table and diagnostics expose these boundaries; this is not full CUDA-MHRN.

D3 now checks complete Builder RNG state, STP resources, eligibility and eligibility timestamps, pending delay-ring currents, synaptic weights/delays/topology, full PAN end state, spikes, actions/rewards and full body trajectory. Numeric end-state bounds are 1e-12; sampled membrane bound is 1e-4. Missing/non-finite state fails closed.

## Validation

Seventeen tests passed with physical RTX 3060 enabled, including the three complete 256-neuron/2048-edge/2000-tick PAN D3 seeds, 129-event partial blocks, signed/inhibitory emissions, exact STP threshold and just-below-threshold cases, STP on/off, positive/zero/negative reward, credit-window boundary, recovery/decay clamps, frozen emitted values and malformed input. RNG state, actions and trajectories matched exactly; all numerical bounds passed. Resource-failure tests still cover shared-context cleanup. New kernels are assembled in main CI.

`pan_cuda_hybrid` inherits the complete balanced PAN profile and explicitly selects `cuda_pan`; it requires an available NVIDIA driver and NVRTC. `pan_full_balanced` explicitly selects CPU, so switching back never accidentally retains GPU execution. No universal optimum or speedup is claimed. The body remains available in the Run page in both profiles.
