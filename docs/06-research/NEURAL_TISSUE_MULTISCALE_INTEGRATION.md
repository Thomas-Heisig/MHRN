# Neural tissue multi-timescale integration

Status: experimental integration branch

Branch: `feature/neural-tissue-multiscale-integration`

## Purpose

The canonical MHRN core currently executes membrane dynamics, spike emission, transmission and several adaptive mechanisms on the same simulation clock. That is appropriate for the verified reference core, but it becomes increasingly problematic once Stage 8-10 mechanisms are introduced. Fast spike dynamics, medium-speed plasticity, slow consolidation and developmental topology changes must not be treated as if they were the same process.

This integration therefore adds an explicit multi-timescale layer around the existing `Neuron`, `Synapse` and `NeuralNetwork` primitives without silently changing their established deterministic semantics.

## Clock separation

| Clock | Default cadence | Responsibility |
| --- | ---: | --- |
| Tick | 1 tick / 1 ms canonical core | membrane integration, spikes, queued synaptic transmission |
| Plasticity | 10 ticks | calcium bridge, short-term plasticity recovery, prediction error, BCM-like candidate plasticity |
| Consolidation | 1,000 ticks | tags, confidence, slow support state, freezing candidates |
| Development | 100,000 ticks | auditable structural growth/pruning proposals |

The values are engineering defaults and are experiment parameters, not biological claims.

## Neuron-side additions

`NeuronTissueState` adds slow sidecar state for:

- basal and apical context drives as a minimal compartment surrogate;
- bounded calcium state;
- second-messenger state;
- neuromodulator gain;
- prediction and prediction-error state;
- salience;
- intrinsic excitability;
- metabolic reserve;
- glial-support surrogate;
- activity memory across ticks.

These fields deliberately do not replace the canonical Izhikevich/LIF membrane state. A later dedicated compartmental neuron model can be compared against the reference primitive rather than retroactively changing the reference model.

## Synapse-side additions

`SynapseTissueState` adds:

- short-term depression and facilitation;
- ready-vesicle fraction;
- release probability;
- presynaptic calcium;
- explicit AMPA/NMDA/GABA-A/GABA-B gain fields;
- retrograde-signal surrogate;
- BCM-like sliding threshold;
- synaptic tagging and consolidation;
- context/attention modulation gain;
- confidence;
- bounded dynamic-delay offset;
- silent-synapse state;
- frozen/consolidated state;
- cumulative plasticity-energy cost;
- explicit functional connection role (`feedforward`, `feedback`, `lateral`, `modulatory`, `unknown`).

The release model is deterministic. Quantale stochastic release and ion-channel stochasticity remain separate experiment candidates so deterministic replication is preserved by default.

## Network-side additions

`NeuralTissueController` composes the canonical `NeuralNetwork` rather than replacing it. It:

1. synchronizes neuron and synapse sidecars to the current topology;
2. advances the canonical network by exactly one normal network tick;
3. bridges spikes into calcium/metabolic/activity-memory state;
4. runs the plasticity clock only when due;
5. runs consolidation only when due;
6. generates structural growth/pruning proposals only on the development clock;
7. keeps weight updates and structural mutation disabled by default.

This avoids hidden double-learning with `LearningEngine` and preserves the existing deterministic event queue.

## Stage mapping

### Stage 8 - plastic nervous tissue

Implemented or scaffolded in this integration:

- explicit multi-timescale separation;
- STP depression/facilitation;
- vesicle resource state;
- calcium bridge;
- metabolic cost of candidate plasticity;
- synaptic tagging and consolidation;
- frozen synapse state;
- confidence state;
- auditable structural-plasticity proposals;
- optional structural mutation behind an explicit flag.

Still separate work:

- replay/generative replay;
- task-boundary detection;
- meta-learned learning rates;
- experimentally validated growth/pruning rules;
- persistent sidecar checkpoint/recovery integration.

### Stage 9 - predictive/contextual integration

Implemented or scaffolded:

- neuronal prediction and prediction error;
- salience state;
- synaptic attention/context gain;
- neuromodulator gain;
- functional connection typing;
- basal/apical context coincidence surrogate;
- receptor-family gain fields;
- delay-adaptation state.

Still network/module work:

- explicit working-memory buffer;
- predictive forward model;
- top-down attention controller;
- theta/gamma or other oscillatory coupling;
- hierarchical binding;
- explicit value/utility system.

### Stage 10 - self-monitoring/access

This integration does not claim Stage 10. Existing self-monitoring work can consume the new prediction, confidence, metabolic and consolidation metrics, but global-workspace, metacognitive access, report mechanisms and any Phi-like metric remain independent research modules.

## Why sidecars instead of immediately inflating the primitives

The repository already has serialization, snapshot, recovery, storage codecs, dashboard contracts and scientific tests tied to the canonical `Neuron` and `Synapse` schemas. Adding every slow biological state directly to those dataclasses in one step would change persistence and recovery semantics across the repository and would make old experiments harder to reproduce.

The sidecar design therefore acts as the compatibility boundary for the integration branch. Once experiments demonstrate stable behavior, individual fields can be promoted into versioned primitive schemas deliberately, together with migration tests.

## Scientific limitations

The names calcium, AMPA, NMDA, GABA, glial support and second messenger describe the intended computational role. The current variables are low-dimensional surrogates and are not calibrated biochemical models. In particular, this branch does not yet implement Hodgkin-Huxley ion channels, detailed dendritic morphology, explicit astrocyte networks, microglial dynamics, gap junction currents, protein synthesis, receptor trafficking kinetics or stochastic quantal release.

Any experiment must distinguish between:

- mechanism-inspired engineering model;
- experimentally measured computational effect;
- biological interpretation.

Only the first is provided by this implementation until evidence is generated.

## Integration rule

Default behavior must remain backward compatible:

- creating a normal `NeuralNetwork` behaves exactly as before;
- `LearningEngine` remains the production plasticity path;
- neural-tissue weight changes require `enable_weight_updates=True`;
- structural mutation requires `enable_structural_mutation=True`;
- research reports must record these flags and all four timescale cadences.
