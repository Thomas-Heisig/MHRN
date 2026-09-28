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

An activity-only held-out decoder and shuffled-label baseline are integrated into run results. Policy feedback is flagged. The integrated six-condition suite now covers randomized input-cue interventions and pair-STDP/frozen-weight comparisons. Synaptic transfer probe calibration curves are integrated; task-learning transfer remains open. No all-GPU PAN or neural-learning advantage is claimed.


## CUDA-1.6 hybrid integration acceptance

The actual Builder can now run membrane updates on CUDA with the complete existing CPU PAN/Strichmann loop. Three full RTX 3060 seed pairs passed D3 for actions, rewards and all body frames. [Scope and validation](CUDA16_BUILDER_HYBRID.md). This is not completion of all-GPU CUDA-1.6: synaptic/world/structural state and live sessions remain CPU in this integration path.


## Cue interventions

Actual independent randomized/absent input cues and a six-condition pair-STDP control suite are integrated into the Builder and research controls. The matched 3-seed sample decodes aligned cues equally well with frozen and plastic weights, so no neural-learning advantage is claimed. [Protocol and results](CUE_CONTROL_EXPERIMENTS.md). A [synaptic transfer probe](SYNAPTIC_TRANSFER.md) transfers validated weights/delays to new cue channels with fresh-state controls. Full checkpoint resumption and faster neural task learning remain unproven.


## Integrated PAN work programme (2026-09-28)

PAN is the project architecture-family name **Persistent Adaptive Neural**, with neuron, synapse and network projections. Persistence and adaptation are acceptance obligations at each level, not claims that all state already survives every backend or hardware transition. [Definition and invariants](PAN_ARCHITECTURE_FAMILY.md).

Status below distinguishes the non-canonical Playground from canonical MHRN. A feature in the Playground does not automatically establish a canonical RuntimeController backend. The CUDA-1.4/1.5 reference is accurately described as **recurrent CUDA SNN + frozen-reward synaptic-plasticity reference backend**. The Builder has a separate hybrid implementation.

| Work package | Current execution | Required acceptance before completion |
| --- | --- | --- |
| Membrane and spike detection | CPU or actual CUDA Builder | D1 full spikes, finite D2, threshold/refractory boundaries |
| PAN Hyperstate (5–32 axes) | New optional CUDA PAN state stage | Per-tick full-state parity, dead-state retention and dimensions 5/10/32 |
| PAN Health / Energy | New optional CUDA PAN state stage | Bounds, finite checks, stress/recovery and death-threshold cases |
| Information Proxy | New optional CUDA PAN state stage | Local-surprise parity; no substitution for PID/information theory validation |
| Consolidation | New optional CUDA PAN state stage | Activity-history parity; not established cognitive memory |
| Apoptosis | CUDA decision, host event bookkeeping | Identical death tick/id, dead neurons stop spiking, buffers remain valid |
| Feedback projection / population reduction | Weighted projection/shape on CUDA; source history and ordered population reduction on CPU | 96-mode projection parity plus full D3; GPU population/history ownership remains open |
| Synaptic propagation / STDP / eligibility | CUDA Builder emission/STP/recovery/live reward plus pair/triplet/eligibility/modulation; resident neuron traces | Full synaptic-state/RNG D3 and seven rule modes; resident delay queue integrated; neuron trace decay/commit is device-owned; other persistent state remains open |
| Inhibitory integration | Actual Builder GPU emission implemented; older frozen-reward reference restriction remains | Signed/GABA and threshold controls pass; keep reference/backend scope explicit |
| Full Builder RNG semantics | Preserved host traversal draws supplied to CUDA emission; reference counter RNG differs | Exact complete RNG-state/STP/D3 checks pass; device RNG ownership remains separate |
| Growth / dynamic synaptogenesis / structural mutation | CPU barriers | Deterministic additions/removals, stable IDs, capacity and pending-event migration |
| Live Environment Reward | World reward on CPU, actual live reward weight update on CUDA | Sign/zero/window controls and full D3 pass; GPU world/reward generation remains open |
| Stick Figure / Posture | CPU shared physical world, real Builder coupling | GPU or explicitly supported host adapter, full trajectory/reward parity |
| Sensors / actuators / Neural I/O | CPU real Builder path | Complete codec/projection/action contract and causal sensor/action perturbations |
| Complete closed-loop execution | Hybrid Builder verified; GPU live sessions rejected | All declared backend components executed, no silent fallback; live lifecycle tests |
| Canonical MHRN self-organization | Separate canonical mechanisms | Map actual canonical state/rules; conformance to canonical CPU, not Playground proxies |
| Canonical storage/checkpoint | Existing canonical path separate; synaptic probe is not full checkpoint | Versioned full state including RNG, queues, topology, time, body, policy; exact resume |
| RuntimeController integration | Not a productive full CUDA backend | Backend capability routing, cancellation, errors, storage and rollback tests |
| CUDA-2 persistent execution | Resident device delay ring with queue snapshot/restore; other host mirrors/transfers remain | Device-resident state, bounded stop/checkpoint, occupancy-safe launches, measured throughput |
| CUDA-3 neurogenesis | CPU exploratory growth only | Neuron creation/death/remapping and restored pending events with reference equivalence |
| Adaptive delays / SSD offload | Partial host facilities | Preserve emitted amplitude and arrival time during delay changes/spill/restore |
| Multi-GPU / clusters | Open | Explicit partition/RNG/checkpoint protocol, cross-device delays, failure recovery and hardware scaling |

### Ordered next stages

1. Integrate and validate the new PAN state CUDA stage in Builder, D3 endpoint, visible component table and main CI.
2. PAN feedback projection is implemented as the next validated stage. Builder inhibitory emission, exact host traversal-RNG supply and per-edge plasticity rules are integrated. Resident delay-queue and neuron-trace ownership are integrated. Port source history/population reduction and complete persistent-session state next. Preserve ordered reductions and emission-time amplitude. Keep the frozen-reward reference as a separate oracle.
3. Add persistent live-session integration, bounded cancellation and complete versioned checkpoints before advertising persistence across runs/backends.
4. Connect canonical self-organization and RuntimeController through explicit state/conformance adapters. Do not relabel exploratory health/energy/information proxies as canonical mechanisms.
5. Move structural mutation/neurogenesis and event migration through validated barriers; then resident execution, measured optimization and multi-GPU/distributed tests.

Research runs alongside engineering: aligned/randomized/absent cues and policy-current ablation are integrated. Synaptic-transfer calibration is integrated but shows no consistent advantage. Remaining tests include cue removal after a training/delay phase, activity-driven policy with a causal decoder ablation, genuinely new-task reward learning, larger paired seed samples and predeclared held-out evaluation. A negative result is a completed experiment, not a reason to change acceptance thresholds. Decodability, causal neural use and learned generalization remain different claims.

The attachments motivate this programme but do not supply measured evidence. For example, high neuron count alone does not imply occupancy failure, FP64 alone does not guarantee exact execution, and matching one success rate is not sufficient D3. Occupancy is queried from the actual compiled kernel; parity states precisely which quantities and trajectories were compared.


### Canonical integration locations

The existing canonical bridge is `src/self_organization/runtime_adapter.py`: it publishes homeostasis-derived proposals; structural mutations still pass through coordinator/approval/engine/manipulator. A CUDA adapter must preserve this separation and the existing policy, rather than silently executing Playground growth as canonical self-organization.

`src/storage/checkpoint.py` already specifies RNG, current tick, pending currents, event slots, neurons and synapses. GPU checkpoint work must extend/implement that versioned contract and prove interrupted/resumed equivalence; the research-only synaptic snapshot cannot replace it.

Two control surfaces exist: `src/controller/runtime.py` (network/homeostasis, hooks and safe snapshots) and `src/runtime/control.py` (single worker callback queue). Integration must identify the active production composition and preserve single-owner stepping, safe boundaries and structured failures. Merely adding a CUDA selector to the Playground does not attach either productive controller.


[Builder synaptic integration](CUDA16_BUILDER_SYNAPSES.md) is the next concrete CUDA-1.6 stage: actual inhibitory emissions, STP with preserved Builder RNG, recovery/decay and live reward updates. Its explicit GPU preset inherits the existing balanced PAN parameters. It does not claim the host delay queue, STDP/eligibility evolution or body have moved to GPU.


[Actual Builder plasticity](CUDA16_BUILDER_PLASTICITY.md) adds per-edge learning-rule execution with original same-tick ordering, rather than treating the frozen-reward reference as a drop-in backend. Global modulators are still host-calculated; per-edge application is CUDA.


[Resident delay queue](CUDA_RESIDENT_DELAY_QUEUE.md) is an initial CUDA-2 state-ownership step integrated into the real Builder, with exact ordered current accumulation and raw queue restore. It does not close complete session checkpoint/resume, cancellation or productive controller integration.


[Resident neuron traces](CUDA_RESIDENT_NEURON_TRACES.md) preserves the original pre-plasticity decay and post-emission last-spike commit. The device owns trace evolution between ticks; host mirrors still feed edge descriptors and diagnostics.
