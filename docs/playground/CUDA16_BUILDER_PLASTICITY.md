# Actual Builder CUDA plasticity rules

The `cuda_pan` path now executes pair-STDP, triplet-STDP, eligibility decay/updates/timestamps, three-factor and eligibility modulators, and homeostatic weight scaling on CUDA, in addition to emission/STP/recovery/decay and live target/posture reward updates. This ports the actual Builder rules; it does not replace them with the earlier simplified frozen-reward reference.

Each edge is processed independently but reproduces the original ascending-neuron event order. When both source and target spike in one tick, the source/target IDs determine whether depression or potentiation happens first. Clamps apply after the same sub-operations as the CPU. Triplet updates include a prior same-tick trace increment only when that neuron has already been processed. Tests explicitly cover the simultaneous-spike cases, 0/1/20/21 tick windows and near-bound weights.

Host ownership remains explicit: neuron pre/post traces, global rate/modulator calculation, traversal RNG, topology/growth, ordered delay queues, PAN source history/population reduction, policy, body, sensors and episode management. GPU kernels compute the per-edge updates. Persistent device state across runs, canonical storage/controller integration and a complete CUDA-MHRN backend are not implied.

D3 additionally compares all neuron traces and last-spike timestamps. The existing full checks include weights, STP/eligibility state, pending currents, complete RNG state, PAN state, spikes and body/action/reward trajectories. The new kernel uses the same bounded buffers/context, with finite/shape validation and failure cleanup.

Validation covers all eight pair/triplet/eligibility flag combinations on 129 edges, exact event ordering/clamps, seven actual Builder plasticity modes (stdp, triplet_stdp, metaplasticity, three_factor, eligibility_trace, homeostatic, none) and three full default PAN D3 seeds. Main CI assembles the expanded synaptic source.


All 26 physical-GPU/PAN tests passed, including the full default D3 seeds. After adding the remaining per-edge three-factor/eligibility/homeostatic modifiers, the 12 synaptic hardware tests were rerun and passed. Plasticity uses 33 registers and scaling 14, both with zero stack/spills. The combined software selection passed 127 tests; GPU tests are opt-in in CI. These are bounded execution checks, not a scientific learning-advantage claim.
