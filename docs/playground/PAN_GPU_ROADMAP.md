# PAN execution roadmap and acceptance evidence

This roadmap separates runnable implementations from scaffolds. Stage completion
requires tests and measured execution, not filenames, parameter toggles or a
successful single-tick gate launch. Main remains outside this integration work.

| Stage | Deliverable | Acceptance |
| --- | --- | --- |
| CUDA-1.3 | Validated gate ABI, fail-closed parity, safe buffers/cleanup | Integrated in #232/#233; physical RTX 3060 smoke and RNG parity passed |
| Context policy | Cue-conditioned policy and action-time reward credit | Context regression tests and measurements in CONTEXT_POLICY.md |
| CUDA-1.4 | Multi-block recurrent execution and delay ring | Implemented in #236: RTX 3060 parity at 10/100/1000/2000 ticks, delay-64 ring wrap and partial blocks; see CUDA14_RECURRENT.md |
| CUDA-1.5 | STP/STDP, eligibility and reward modulation on GPU | Frozen-reward reference implemented; RTX 3060 trace/weight parity and signed/zero-reward controls pass; see CUDA15_PLASTICITY.md |
| CUDA-1.6 | Closed loop, sensors, posture and stick-figure dynamics | Hybrid Builder D3 passed on RTX 3060; full GPU synapses/world and live-session execution remain open |
| CUDA-2 | Resident cooperative execution, reusable buffers and streams | Actual kernel occupancy bound; bounded stop/checkpoint; no allocation per tick; measured throughput |
| CUDA-3 | Structural mutation and neurogenesis at host barriers | Deterministic mutations, index remapping, checkpoint restoration and capacity checks |
| Adaptive delays/offload | Myelination and bounded SSD spill/restore | Pending-event migration, exact replay and backpressure tests |
| Scaling | Multi-GPU, external input interface and distributed execution | Explicit partition/protocol contracts, equivalence checks and measured scaling on available hardware |

GPU and cluster stages remain open until their acceptance evidence exists. CPU
fallback must be explicit; a selected GPU hardware profile alone does not execute
the network on a GPU. A persistent kernel is a performance design choice, not a
prerequisite for demonstrating learning. Grid dimensions derive from block size
and neuron count; 256 neurons do not inherently require four blocks.


## Builder integration and cue research

The actual CPU Builder now shares the live stick-figure world, receives physical sensor inputs, drives muscles from actions and applies enabled posture rewards to synaptic eligibility. The Run page includes body frame replay. See [PAN embodiment integration](PAN_EMBODIED_INTEGRATION.md).

An activity-only held-out decoder and shuffled-label baseline are integrated into run results. Policy feedback is flagged. The integrated six-condition suite now covers randomized input-cue interventions and pair-STDP/frozen-weight comparisons. Transfer learning curves remain open. No all-GPU PAN or neural-learning advantage is claimed.


## CUDA-1.6 hybrid integration acceptance

The actual Builder can now run membrane updates on CUDA with the complete existing CPU PAN/Strichmann loop. Three full RTX 3060 seed pairs passed D3 for actions, rewards and all body frames. [Scope and validation](CUDA16_BUILDER_HYBRID.md). This is not completion of all-GPU CUDA-1.6: synaptic/world/structural state and live sessions remain CPU in this integration path.


## Cue interventions

Actual independent randomized/absent input cues and a six-condition pair-STDP control suite are integrated into the Builder and research controls. The matched 3-seed sample decodes aligned cues equally well with frozen and plastic weights, so no neural-learning advantage is claimed. [Protocol and results](CUE_CONTROL_EXPERIMENTS.md). Transfer from a trained neural checkpoint remains required.
