# CUDA-1.4 recurrent membrane reference

The recurrent CUDA path executes LIF, AdEx and PAN-AdEx **membrane dynamics**
with static weighted synapses and integer delays from 1 to 64 ticks. PAN health,
hyperstate, plasticity, growth and embodied closed-loop execution are not yet
part of this backend. The ordinary Builder run remains the CPU implementation.

`recurrent.cu` is compiled through NVRTC, requiring CUDA toolkit headers/libraries
but no host C++ compiler. The CUDA driver launches a cooperative resident grid;
occupancy is measured for the actual compiled function before launch. Every lane
participates in `grid.sync()`, including unused lanes in partial blocks.

Incoming CSR edges are gathered in a fixed order without floating-point atomics.
A spike ring of `maximum_delay + 1` slots prevents a current write from overwriting
any slot still read in that tick. A grid barrier makes all spikes visible before
the next tick. Host/device buffers are allocated once per bounded run, outside
the tick loop, and cleaned up after success or failure.

State is explicitly **FP64**, with FMA disabled, to compare against existing Python
membrane functions. This is a correctness reference, not a float32 performance
claim. Limits: 4096 neurons, 2000 ticks, 65536 edges and 4 million history elements.
No CPU fallback is mislabeled as GPU execution.

## Entry points and verification

- Python: `RecurrentInputs`, `cpu_recurrent_reference`, `execute_recurrent` and
  `recurrent_parity` in `src.playground.cuda.recurrent`.
- Dashboard: `POST /api/playground/cuda/recurrent-parity`, using the shared
  diagnostic worker/rate limit. The Builder exposes a 129-neuron/100-tick test.
- CI: the ordinary pytest suite checks validation, causal delays, failed cleanup
  and fail-closed parity. `scripts/validate_playground_ptx.py` compiles this source
  through NVRTC and assembles it with ptxas in the existing CUDA CI container.
- Physical GPU: set `MHRN_TEST_CUDA_HARDWARE=1` and run
  `python -m pytest tests/test_playground_cuda_recurrent.py`.

RTX 3060 acceptance on 2026-09-28: LIF and PAN-AdEx, 129 neurons, three blocks,
10/100/1000/2000 ticks, exact spike parity and state tolerance 1e-4 passed. Delay-64
ring wraps and block sizes 32/128/256 also passed. An initial 1000-tick AdEx
measurement had maximum voltage error below 7e-13. ptxas reports 47 registers,
no spills on sm_86. These results concern membrane/static-synapse execution only.

Next: port STP/STDP and eligibility/reward updates with explicit update ordering;
then compare frozen-action/reward closed loops before enabling live GPU behavior.
