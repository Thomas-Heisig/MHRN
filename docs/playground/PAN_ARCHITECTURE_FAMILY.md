# PAN — Persistent Adaptive Neural

PAN names this project's architecture family, with three projections: Persistent Adaptive Neuron, Persistent Adaptive Synapse and Persistent Adaptive Network. This is a naming/design convention, not a claim of scientific novelty, cognition or complete implementation.

| Invariant | Neuron | Synapse | Network |
| --- | --- | --- | --- |
| Persistent | Membrane/adaptation, health, energy and hyperstate retain defined state between ticks | Weights, delay, eligibility and STP survive the specified update boundary | Topology, feedback, RNG, pending events and world state have explicit lifetime/restore contracts |
| Adaptive | Excitability and bounded lifecycle state respond to activity | Configured plasticity responds to pre/post events and reward | Configured structural rules change connectivity at controlled barriers |
| Neural | A specified spiking cell and state representation | Causal delayed transmission between cells | Recurrent neural dynamics coupled to declared input/output |

Persistence across ticks, kernel calls, episodes, saved runs and hardware changes are separate guarantees. Current CUDA Builder buffers live for one run; the synaptic transfer snapshot deliberately resets other state. A complete cross-backend checkpoint is still a roadmap item. A persistent CUDA kernel is one execution strategy, not the definition of persistence.

The proposed neuron tuple `(V, adaptation, health, amplitude, hyperstate, geometry)` and synapse tuple `(weight, delay, facilitation, resources, eligibility)` describe intended contracts. Actual supported variables and rules must be read from versioned implementations; the Playground does not implement every proposed synaptic mechanism. Hyperstate axes beyond the documented proxies remain unassigned exploratory dimensions. No semantic understanding follows from naming an axis.

Acceptance requires state-lifetime tests, finite/bounded updates, causal event order, checkpoint compatibility and CPU/GPU conformance. Network-level behavior additionally needs controls separating explicit context policies from neural information use. See the [complete work programme](PAN_GPU_ROADMAP.md).
