# CUDA-1.5 frozen-reward synaptic reference

The cooperative recurrent backend can now execute pair STDP, quantal STP,
eligibility traces, a bounded reward-modulated weight update, weight decay and
clamping. `RecurrentInputs.synapses` selects a validated `SynapseConfig`;
`rewards` supplies one explicit frozen scalar per tick. An absent configuration
preserves the CUDA-1.4 static path.

The ordered scalar oracle uses the existing Python membrane model and an explicit
synapse implementation. Analytic tests independently check causal potentiation,
anticausal depression, resource recovery, signed reward updates and expired
credit. CPU/GPU agreement alone is not treated as proof that both are correct.

Within each tick:

1. Gather previously emitted amplitudes and update membrane states.
2. Synchronize all blocks; apply ordered pre/post pair updates and eligibility
   decay, then reward modulation within the credit window.
3. Emit the current weighted/released amplitude into the delay ring; recover STP
   resources and apply weight decay/clamp.
4. Synchronize before updating last-spike timestamps, then synchronize again.

The ring stores **emitted amplitudes per edge**, so learning after emission cannot
retroactively change a pending signal. Edge ownership follows incoming CSR rows;
there are no floating-point atomic updates. Same-tick pre/post operations follow
ascending-neuron ordering, matching the intended pair-rule ordering.

STP uses a specified uint32 counter hash `(seed, tick, edge)` and upper-24-bit
conversion to `[0,1)`. It does not reproduce the Builder's traversal-dependent
Python random stream. This reference therefore does not claim full Builder/PAN
trajectory equivalence. Inhibitory signs, PAN hyperstate, changing topology and
live behavioral/environment reward generation remain separate integration work.

## Evidence

On RTX 3060, 129 PAN-AdEx membrane neurons and three cooperative blocks pass
10/100/1000/2000-tick comparisons with positive, zero and negative frozen rewards.
Spikes match exactly; voltage, adaptation, final weights, eligibility and STP
availability all pass 1e-4 tolerance. One 1000-tick positive-reward run measured
zero error for weights/traces/resources and voltage error below 3e-13.

Run `MHRN_TEST_CUDA_HARDWARE=1 python -m pytest tests/test_playground_cuda_plasticity.py`
(set the environment variable using the platform shell). The ordinary CI runs the
analytic/validation tests; the CUDA CI compiles and assembles both static and
plastic variants. The Playground diagnostic uses `plasticity: true` on
`/api/playground/cuda/recurrent-parity`, with the existing shared worker limit.

This is FP64 engineering reference execution, not a speed or scientific-validity
claim. The ordinary complete PAN Builder run remains on CPU.
