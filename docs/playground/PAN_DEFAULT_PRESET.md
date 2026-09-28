# PAN full starting profile

The Builder initially selects **PAN · Vollprofil (Standard)** (`pan_full_balanced`).
This complete preset resets supported parameters explicitly, including Neural I/O
payload, so values from a previously selected experiment do not leak into it.

It uses 256 PAN AdEx neurons, 2,048 edges, 2,000 ticks, STP/STDP and structural
plasticity, growth, cortical/thalamic processing, Neural I/O, behavioral learning,
and the stick-figure action/reward loop. Eight channels separate target (0), reward
(1), posture score (2), reward event (3), reward cue (5), and action feedback (6).
Weights start at 4, decay by 0.001 and clamp at 20; feedback uses tanh, gain 1.5
and saturation 20. The default CPU profile keeps offload disabled; this small
network is not a GPU-utilization benchmark. Sessions are saved by default.

## Measured checks, 2026-09-28

The measurements below describe the original global-policy baseline. See
[the context-policy follow-up](CONTEXT_POLICY.md) for the corrected learner and
paired measurements (64.5–74.2% on the same three seeds).

Three complete CPU runs, with persistence disabled for measurement:

| Seed | Wall time (s) | Mean rate (Hz) | Active neurons | Successful episodes |
| --- | ---: | ---: | ---: | ---: |
| 12345 | 20.84 | 46.65 | 256/256 | 7/31 (22.6%) |
| 42 | 22.58 | 49.52 | 256/256 | 8/31 (25.8%) |
| 777 | 23.57 | 47.78 | 256/256 | 7/31 (22.6%) |

All runs completed 31 policy and external-reward updates without insufficient
activity episodes. This verifies execution, not superior learning: success remains
near the four-action chance level. There is no evidence of globally optimal
parameters or scientific/biological validity. Tune and compare seeds for a chosen
task before drawing performance conclusions. Runtime depends on the host.

The existing smaller presets remain available for focused experiments. CUDA
compile, preflight, smoke and parity diagnostics remain separate controls.


## Explicit CUDA variant

`pan_cuda_hybrid` inherits this balanced profile and selects actual CUDA membrane/PAN/feedback plus supported synaptic emission and live reward updates. It requires NVIDIA Driver + NVRTC; body, policy and RNG remain CPU-owned; the delay ring and neuron traces are device-resident. The CPU default explicitly resets `neuron_backend=cpu`. See [backend scope](CUDA16_BUILDER_SYNAPSES.md).
