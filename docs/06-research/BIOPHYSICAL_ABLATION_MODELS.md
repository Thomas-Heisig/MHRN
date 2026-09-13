# Biophysical ablation model architecture

Status: experimental research branch

This layer deliberately does **not** redefine the canonical MHRN point-neuron or chemical-synapse schemas. It introduces explicit alternative bodies and sidecar subsystems so ablations are reproducible and mechanism ownership remains visible.

## Separation rules

### Alternative model bodies

- `HodgkinHuxleyNeuron`: deterministic Na/K/Ca conductance model with explicit gating state.
- `CompartmentNeuron`: soma plus explicit dendritic compartments.
- `QuantalSTPSynapse`: seeded quantal release and STP in one coherent vesicle model.

These are replacements for their canonical primitive, not hidden flags inside `Neuron` or `Synapse`.

### Orthogonal dendritic axes

Multi-compartment morphology and NMDA-like plateau nonlinearity are separate treatments. A multi-compartment experiment may run with a linear dendrite, and an NMDA-plateau treatment must be declared explicitly through `DendriticNonlinearity.NMDA_PLATEAU` plus `enable_nmda_plateau=True`.

### Sidecars

- `AstrocyteField`: plasticity-timescale extracellular modulation.
- `MicrogliaField`: development-timescale structural proposals only.
- `SlowConsolidation`: consolidation-timescale tag -> finite capture window -> consolidation.
- `ReceptorTrafficking`: plasticity-timescale receptor availability; it never changes canonical `weight`.
- `GapJunction`: tick-timescale bidirectional ohmic coupling; never represented as a chemical `Synapse`.

## Timescale API

Every mechanism has one owner scale:

| API | Intended scale | Examples |
| --- | --- | --- |
| `step()` | tick | HH, compartment dynamics, quantal release, gap junction current |
| `plasticity_update()` | plasticity | astrocyte modulation, receptor trafficking |
| `consolidate()` | consolidation | protein synthesis / tag capture |
| `develop()` | development | microglia structural proposals |

No slow mechanism is run implicitly from the 1 ms point-neuron tick loop.

## Ablation rule

Ablation uses the same mechanism class and pipeline with one mechanism parameter disabled. Examples:

- HH full vs. HH `enable_na=False`
- multi-compartment linear vs. multi-compartment NMDA plateau
- astrocyte `enabled=True` vs. `enabled=False`
- protein synthesis with the same capture window and `enabled=False`

The old canonical path is therefore not used as a substitute control for a new model.

## Provenance

Each experimental mechanism exposes `provenance_tag` containing:

- stable model identifier
- implementation version
- owning timescale
- enabled/ablated state
- full parameter payload
- explicit stochastic seed where relevant

Quantal release owns a private `random.Random(seed)` instance and never reads module-global RNG state.

## Structural safety

Microglia returns a `MicrogliaProposal`. It does not delete synapses. Approval, application and undo remain the responsibility of the existing structural manipulation/journal path. This prevents biological sidecars from bypassing auditability.

## Protein synthesis

Tags expire after `capture_window_ticks`. Outside the capture window the tag is cleared and cannot capture newly synthesized protein. This prevents the mechanism from degenerating into a persistent global learning-rate multiplier.

## Receptor trafficking

`transmission = weight * availability`.

`weight` remains the consolidated connection parameter. Trafficking only changes the sidecar `availability` value.

## Performance budgets

The following are engineering expectations to be benchmarked, not measured claims:

| Model | Expected relative cost vs. Izhikevich point neuron | Use |
| --- | ---: | --- |
| Izhikevich | 1x baseline | large recurrent experiments |
| LIF | ~1x or lower | controls / scaling |
| Multi-compartment | roughly O(number of compartments) | targeted morphology experiments |
| HH Na/K/Ca | commonly tens to hundreds of operations per small point-cell step and normally requires a smaller `dt_ms` | small mechanistic experiments |

No Stage-3 or other established baseline is to be silently recalibrated from Izhikevich to HH or multi-compartment. Every such experiment must declare the treatment and performance budget.

## Current integration boundary

`BiophysicalNeuronConfig` and `create_biophysical_neuron()` are the explicit experimental construction boundary. The canonical `NeuralNetwork` still stores canonical point neurons, so HH and multi-compartment populations are **not yet silently inserted into existing large-network runs**. A future heterogeneous-network adapter must first define common current/spike/state contracts and storage migration.

This boundary is intentional: selecting a biophysical treatment must not mutate the meaning of previously validated recurrent-SNN experiments.
