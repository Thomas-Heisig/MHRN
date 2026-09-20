# MHRN: An Open Research Framework for Recurrent Spiking Neural Networks with Plasticity, Provenance, and Evidence-Aware Experimentation

**Thomas Heisig · Working paper v0.1 · 20 September 2026**  
**Target class:** research-software / methods paper  
**Candidate venues:** Journal of Open Source Software (JOSS), Journal of Open Research Software (JORS)  
**Status:** working draft; not submitted; target-specific eligibility and review requirements remain open

## Abstract

Research on recurrent spiking neural networks (SNNs) frequently combines simulation code, plasticity mechanisms, experiment scripts, analysis notebooks, and interpretive reports in a single evolving software environment. This creates a methodological risk: technical implementation, generated DATA, human review, accepted evidence, and independent replication can become conflated during rapid iteration. We present the Multi-Scale Homeostatic Recurrence Network (MHRN), an open research framework for recurrent SNN experiments with explicit contracts for recurrent dynamics, synaptic and structural plasticity, homeostatic regulation, persistent state, embodiment, experiment provenance, and evidence-aware research workflows. MHRN combines a Python simulation core with registered research questions and hypotheses, preregistration-oriented experiment execution, source-bound DATA artefacts, human-review boundaries, reproducible release freezes, and a local research dashboard. The software deliberately separates engineering maturity from scientific maturity and prevents software tests, dashboards, completed runs, or release identifiers from automatically becoming accepted scientific evidence. MHRN is released under the MIT License and is distributed through GitHub, Hugging Face, OSF, and Zenodo-oriented archival workflows. This paper describes the software architecture, research workflow, reproducibility mechanisms, and intended use as infrastructure for auditable SNN research. It does not claim that MHRN demonstrates AGI, consciousness, biological equivalence, or a general advantage of its multidimensional address representation.

## 1. Summary

MHRN is a research-software framework for building and evaluating recurrent spiking neural systems under explicit provenance and evidence boundaries. Its central design goal is not to hide scientific uncertainty behind a unified application, but to make the transitions between implementation, experiment execution, DATA, interpretation, review, EVID, and replication visible and auditable.

The framework contains:

- a sparse recurrent SNN core;
- Izhikevich and LIF neuron-model paths;
- delayed recurrent event propagation;
- STDP, eligibility traces, and delayed-reward / three-factor learning mechanisms;
- homeostatic regulation;
- structural plasticity with proposal, approval, mutation, journal, and recovery contracts;
- persistent snapshots and deterministic restore/continue infrastructure;
- typed sensor/actuator and embodiment interfaces;
- working, episodic, replay, prediction, and world-model research infrastructure;
- registered research questions, hypotheses, protocols, experiments, DATA, reviews, and evidence records;
- a browser-based operator and research dashboard;
- release, citation, DOI, ORCID, OSF, and Hugging Face publication infrastructure.

The canonical software repository is `Thomas-Heisig/MHRN`. The current public research-software release is `v0.6.0-alpha.6`.

## 2. Statement of need

SNN research software often needs to satisfy two different forms of correctness.

The first is **engineering correctness**: deterministic execution where required, stable interfaces, valid serialization, bounded resource use, reproducible configuration, and testable software contracts.

The second is **scientific correctness**: appropriate research questions, frozen protocols, suitable controls, source-bound observations, defensible statistics, explicit limitations, human review, and independent replication where claims require it.

These are related but not interchangeable. A unit test can show that a function behaves as implemented without showing that the scientific hypothesis is true. A successful experiment runner can generate DATA without making those DATA accepted evidence. A DOI can make an object citable without making it peer reviewed.

MHRN therefore treats research-state separation as a first-class software requirement:

```text
implementation / test
        !=
experiment DATA
        !=
human-reviewed EVID
        !=
independent replication
```

This is particularly important in AI-assisted research, where code, analysis, text, methodological criticism, and literature leads can be generated quickly. MHRN records AI assistance as provenance while retaining human responsibility for acceptance, interpretation, and publication.

## 3. Architecture

### 3.1 Recurrent spiking core

The simulation core represents neurons in a sparse multidimensional coordinate space and supports recurrent directed connectivity with explicit delays. The architecture is designed so that recurrence, neuron dynamics, plasticity, and structural changes can be tested independently rather than being fused into one opaque training loop.

The current implementation includes Izhikevich- and LIF-family paths, deterministic random-state handling, delayed event delivery, and bounded runtime control. Dimensional coordinates are treated as a representation choice rather than a biological claim.

### 3.2 Plasticity and regulation

MHRN includes mechanisms for:

- pair-based spike-timing-dependent plasticity;
- eligibility traces;
- delayed reward / three-factor learning;
- firing-rate and energy-related homeostatic regulation;
- structural plasticity and topology mutation.

Structural change is governed by an explicit path:

```text
proposal -> authorization -> bounded mutation -> journal -> recovery / undo
```

This enables experimental manipulation of topology without silently rewriting network state.

### 3.3 Persistence and reproducibility

Persistent state is handled through versioned snapshots, checkpoints, structural journals, and deterministic restore/continue contracts. Claim-relevant runs can record source-freeze commits, configuration references, seeds, provenance digests, validity state, and generated artefact paths.

The release process similarly uses exact source freezes: a release is attached to a concrete commit that has passed the required software and scientific-integrity checks.

### 3.4 Embodiment and bounded external systems

MHRN exposes typed sensor and actuator boundaries and supports bounded peripheral or virtual systems. External language models, retrieval systems, research assistants, and neural gateways are not implicitly treated as the learning core. Their authority is restricted by explicit interface and experimental-treatment contracts.

This is important for causal attribution. A successful external tool call does not demonstrate that the SNN learned to perform the same operation.

### 3.5 Research infrastructure

The research layer contains machine-readable registries for research questions, hypotheses, claims, evidence and experiments. Preregistration-oriented protocols can freeze:

- conditions;
- seeds;
- primary outcomes;
- statistical tests;
- multiple-testing rules;
- validity criteria;
- claim boundaries.

Experiment output remains DATA unless a separate evidence decision explicitly changes its status.

## 4. Research workflow

The canonical research flow is:

```text
Research Question
    -> Hypothesis
    -> frozen / preregistered protocol
    -> authorized experiment
    -> source-bound DATA
    -> analysis
    -> limitations
    -> human review
    -> EVID decision
    -> bounded claim
    -> independent replication where required
```

The dashboard projects this workflow for inspection and operation, but the browser interface is not itself the scientific authority. Canonical files and registries remain inspectable in the repository.

## 5. Reproducibility and open-science workflow

MHRN combines several public research routes:

- **GitHub** — canonical source and version history;
- **Zenodo** — software release archiving and DOI assignment;
- **OSF** — open-science and project/provenance route;
- **Hugging Face** — rolling source, Space, and research-data discovery mirrors;
- **ORCID** — author identity.

Software releases, scientific manuscripts, and research datasets are treated as separate citable research objects. This prevents a software DOI from being used as if it were the DOI of a scientific paper or frozen dataset.

## 6. Research impact and intended use

MHRN is intended for research questions that require controlled recurrent SNN experiments rather than only model training. Example uses include:

- topology-sensitive propagation studies;
- STDP and homeostatic interaction studies;
- structural-plasticity experiments;
- replay and continual-learning experiments;
- embodiment and closed-loop sensor/actuator studies;
- prediction-error and world-model experiments;
- provenance and research-governance studies.

The framework is currently alpha research software. Public availability and technical completeness should not be interpreted as evidence that every implemented mechanism has scientific support.

## 7. Relation to existing SNN research software

Established simulation environments such as NEST, Brian 2, PyNN, BindsNET, and Norse demonstrate different trade-offs between large-scale simulation, model expressiveness, interoperability, machine-learning integration, and event-driven computation. MHRN is not presented as a replacement for those systems.

Its narrower contribution is the combination of recurrent SNN experimentation with:

1. explicit evidence-state separation;
2. repository-native research governance;
3. source-bound experiment provenance;
4. operator authorization for structural changes;
5. integrated open-science publication routing.

A formal prior-art comparison remains required before journal submission.

## 8. AI-use disclosure

AI systems materially assisted the MHRN project with research leads, code generation, refactoring, debugging, tests, literature discovery, methodological criticism, and manuscript drafting. AI systems are not listed as authors. Thomas Heisig is responsible for selection, validation, interpretation, and publication.

The project treats this collaboration itself as a research object, but software functionality or AI assistance is not accepted as scientific evidence without the relevant experiment and review path.

## 9. Limitations

The current software release has several important limitations:

- MHRN remains alpha research software.
- Independent external replication is incomplete.
- Several scientific mechanisms are implemented but not yet supported by reviewed evidence.
- The multidimensional coordinate representation has not been shown to provide a general 5D advantage.
- Synthetic embodiment does not establish real-world autonomy.
- Scaling demonstrations do not establish biological equivalence.
- A green CI state demonstrates software-contract compliance, not scientific truth.
- The JOSS/JORS submission readiness of this paper depends on target-specific requirements, public-development history, documentation review, and demonstrated research use.

## 10. Availability

Canonical repository: https://github.com/Thomas-Heisig/MHRN  
Author ORCID: https://orcid.org/0009-0002-9589-1872  
OSF: https://osf.io/p34uq/  
Hugging Face: https://huggingface.co/ThomasHeisig/MHRN  
License: MIT

## 11. Citation boundary

Cite the MHRN software release when the implementation is the research object. Cite empirical papers separately when interpreting experiment results, and cite dataset records separately when relying on frozen research DATA.

This software paper does not promote any experiment from DATA to EVID.

## References

- Brette, R., et al. (2007). Simulation of networks of spiking neurons: a review of tools and strategies. *Journal of Computational Neuroscience*.
- Gewaltig, M.-O., & Diesmann, M. (2007). NEST (NEural Simulation Tool). *Scholarpedia*.
- Stimberg, M., Brette, R., & Goodman, D. F. M. (2019). Brian 2, an intuitive and efficient neural simulator. *eLife*.
- Hazan, H., et al. (2018). BindsNET: A machine learning-oriented spiking neural networks library in Python. *Frontiers in Neuroinformatics*.
- Pehle, C., & Pedersen, J. E. (2021). Norse — A deep learning library for spiking neural networks. Documentation/software publication.
- MHRN repository documentation and governed research artefacts, version 0.6.0-alpha.6.
