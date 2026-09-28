# PAN execution roadmap and acceptance evidence

This roadmap separates runnable implementations from scaffolds. Stage completion
requires tests and measured execution, not filenames, parameter toggles or a
successful single-tick gate launch. Main remains outside this integration work.

| Stage | Deliverable | Acceptance |
| --- | --- | --- |
| CUDA-1.3 | Validated gate ABI, fail-closed parity, safe buffers/cleanup | Integrated in #232/#233; physical RTX 3060 smoke and RNG parity passed |
| Context policy | Cue-conditioned policy and action-time reward credit | Context regression tests and measurements in CONTEXT_POLICY.md |
| CUDA-1.4 | Multi-block recurrent execution and delay ring | Cross-block spikes; CPU/GPU state and spike comparison at 10/100/1000 ticks; ring wrap and non-divisible block sizes |
| CUDA-1.5 | STP/STDP, eligibility and reward modulation on GPU | Ordered update semantics; bounded weights; trace/weight parity and negative controls |
| CUDA-1.6 | Closed loop, sensors, posture and stick-figure dynamics | Frozen-action/reward parity first, then live behavior; reset/collision tests |
| CUDA-2 | Resident cooperative execution, reusable buffers and streams | Actual kernel occupancy bound; bounded stop/checkpoint; no allocation per tick; measured throughput |
| CUDA-3 | Structural mutation and neurogenesis at host barriers | Deterministic mutations, index remapping, checkpoint restoration and capacity checks |
| Adaptive delays/offload | Myelination and bounded SSD spill/restore | Pending-event migration, exact replay and backpressure tests |
| Scaling | Multi-GPU, external input interface and distributed execution | Explicit partition/protocol contracts, equivalence checks and measured scaling on available hardware |

GPU and cluster stages remain open until their acceptance evidence exists. CPU
fallback must be explicit; a selected GPU hardware profile alone does not execute
the network on a GPU. A persistent kernel is a performance design choice, not a
prerequisite for demonstrating learning. Grid dimensions derive from block size
and neuron count; 256 neurons do not inherently require four blocks.
