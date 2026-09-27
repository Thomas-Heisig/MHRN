"""Verified literature context for exploratory PAN work.

This module is descriptive metadata only. It is not part of the MHRN scientific
registry and must not be interpreted as evidence for PAN or MHRN claims.
"""

from __future__ import annotations

PAN_LITERATURE: tuple[dict[str, object], ...] = (
    {
        "key": "orchard_spiking_phasors_2024",
        "topic": "hyperdimensional_spiking",
        "citation": (
            "Orchard, J.; Furlong, P. M.; Simone, K. (2024). "
            "Efficient Hyperdimensional Computing With Spiking Phasors. "
            "Neural Computation 36(9), 1886-1911."
        ),
        "doi": "10.1162/neco_a_01693",
        "peer_reviewed": True,
        "supports": (
            "Spiking implementation of FHRR in which hypervector phase is "
            "encoded by spike timing within a cycle."
        ),
        "does_not_establish": (
            "PAN semantic state axes, health/apoptosis coupling, PID coupling, "
            "or variable spike-amplitude PAN dynamics."
        ),
    },
    {
        "key": "olin_ammentorp_phase_ssm_2026",
        "topic": "hyperdimensional_spiking",
        "citation": (
            "Olin-Ammentorp, W. (2026). Phase State Space Models: Parallel, "
            "Surrogate-Free Training of Spiking Networks. arXiv:2608.07754."
        ),
        "arxiv": "2608.07754",
        "peer_reviewed": False,
        "supports": (
            "A resonate-and-fire state-space interpretation with explicit "
            "connections to hyperdimensional computing and recurrent memory."
        ),
        "does_not_establish": "The integrated PAN health/PID/apoptosis framework.",
    },
    {
        "key": "ahmed_temporal_hdc_2026",
        "topic": "hyperdimensional_neural_representation",
        "citation": (
            "Ahmed, H. F.; Samiei, T.; Nozari, E. (2026). On the optimal "
            "temporal resolution for information representation in neural "
            "activity: a theoretical analysis. Frontiers in Computational "
            "Neuroscience 20."
        ),
        "doi": "10.3389/fncom.2026.1885975",
        "peer_reviewed": True,
        "supports": (
            "Neural population activity represented with spatial and temporal "
            "hypervectors in a high-dimensional real vector space."
        ),
        "does_not_establish": "PAN semantic axes or PAN closed-loop dynamics.",
    },
    {
        "key": "makkeh_infomorphic_2025",
        "topic": "pid_learning",
        "citation": (
            "Makkeh, A. et al. (2025). A general framework for interpretable "
            "neural learning based on local information-theoretic goal "
            "functions. PNAS 122(10):e2408125122."
        ),
        "doi": "10.1073/pnas.2408125122",
        "peer_reviewed": True,
        "supports": (
            "Local learning objectives built from partial-information "
            "decomposition terms in infomorphic neural networks."
        ),
        "does_not_establish": (
            "A validated PID estimator inside PAN hypervectors, or coupling "
            "between PID, neuronal health and apoptosis."
        ),
    },
    {
        "key": "naude_homeostatic_intrinsic_2013",
        "topic": "homeostasis",
        "citation": (
            "Naude, J.; Cessac, B.; Berry, H.; Delord, B. (2013). Effects of "
            "cellular homeostatic intrinsic plasticity on dynamical and "
            "computational properties of biological recurrent neural networks. "
            "Journal of Neuroscience 33(38), 15032-15043."
        ),
        "doi": "10.1523/JNEUROSCI.0870-13.2013",
        "peer_reviewed": True,
        "supports": (
            "Homeostatic intrinsic plasticity in recurrent biological network "
            "models and its effects on network dynamics."
        ),
        "does_not_establish": "PAN health-state or hypervector integration.",
    },
    {
        "key": "gao_multiscale_homeostasis_2025",
        "topic": "homeostasis",
        "citation": (
            "Gao, S. et al. (2025). Multi-scale neural homeostasis mechanisms: "
            "Insights into neurodegenerative diseases and therapeutic "
            "approaches, including exercise. Advanced Exercise and Health "
            "Science 2(1), 1-15."
        ),
        "doi": "10.1016/j.aehs.2025.02.002",
        "peer_reviewed": True,
        "supports": (
            "A multi-scale view of neural homeostasis spanning molecular, "
            "cellular and circuit regulation."
        ),
        "does_not_establish": "The specific PAN timescale equations or parameters.",
    },
    {
        "key": "chow_neurogenesis_2012",
        "topic": "neurogenesis_apoptosis",
        "citation": (
            "Chow, S.-F.; Wick, S. D.; Riecke, H. (2012). Neurogenesis Drives "
            "Stimulus Decorrelation in a Model of the Olfactory Bulb. "
            "PLoS Computational Biology 8(3):e1002398."
        ),
        "doi": "10.1371/journal.pcbi.1002398",
        "peer_reviewed": True,
        "supports": (
            "Persistent addition of inhibitory interneurons plus "
            "activity-dependent survival/apoptosis can restructure a network "
            "and decorrelate similar stimulus representations."
        ),
        "does_not_establish": (
            "A continuous PAN health coordinate or integration with PID and "
            "hyperdimensional state."
        ),
    },
    {
        "key": "cao_aging_fhn_2026",
        "topic": "aging_transition",
        "citation": (
            "Cao, W. et al. (2026). Explosive aging transition in globally "
            "coupled FitzHugh-Nagumo neurons with higher-order interactions. "
            "Acta Physica Sinica 75(12):120002."
        ),
        "doi": "10.7498/aps.75.20260125",
        "peer_reviewed": True,
        "supports": (
            "Aging transitions, hysteresis and resilience effects in coupled "
            "FitzHugh-Nagumo neuronal networks with higher-order interactions."
        ),
        "does_not_establish": "PAN per-neuron health/apoptosis hyperstate dynamics.",
    },
    {
        "key": "mahata_spike_amplitude_2023",
        "topic": "spike_amplitude_plasticity",
        "citation": (
            "Mahata, C. et al. (2023). Uniform multilevel switching and "
            "synaptic properties in RF-sputtered InGaZnO-based memristor "
            "treated with oxygen plasma. Journal of Chemical Physics."
        ),
        "doi": "10.1063/5.0179314",
        "peer_reviewed": True,
        "supports": (
            "Neuromorphic device behavior including spike-amplitude-dependent "
            "plasticity."
        ),
        "does_not_establish": (
            "PAN variable spike amplitude as a biological neuron property or "
            "its coupling to PID/hypervectors."
        ),
    },
    {
        "key": "bej_spike_agreement_2026",
        "topic": "spike_agreement_plasticity",
        "citation": (
            "Bej, S. et al. (2026). Fast agreement-driven device-calibrated "
            "local learning paradigms for spiking neural networks. "
            "Neural Networks 200:108809."
        ),
        "doi": "10.1016/j.neunet.2026.108809",
        "peer_reviewed": True,
        "supports": (
            "Spike Agreement Dependent Plasticity using spike-train agreement "
            "rather than pairwise spike timing."
        ),
        "does_not_establish": (
            "Spike-amplitude-dependent plasticity; the acronym SADP is shared "
            "by two different concepts and must not be conflated."
        ),
    },
    {
        "key": "symthaea_software_2026",
        "topic": "software_reference",
        "citation": "Symthaea Core software documentation (2026).",
        "url": "https://docs.rs/symthaea-core/latest/symthaea_core/hdc/index.html",
        "peer_reviewed": False,
        "supports": (
            "A software implementation exposing 16,384D and larger "
            "hyperdimensional representations."
        ),
        "does_not_establish": (
            "Peer-reviewed scientific evidence for PAN or an equivalent "
            "integrated neuron model."
        ),
    },
)


def pan_literature_context() -> dict[str, object]:
    """Return literature metadata with a deliberately bounded novelty statement."""

    return {
        "classification": "PLAYGROUND_LITERATURE_CONTEXT",
        "scientific_evidence_for_pan": False,
        "novelty_status": (
            "TARGETED_SEARCH_NO_INTEGRATED_EQUIVALENT_IDENTIFIED_NOT_NOVELTY_PROOF"
        ),
        "novelty_note": (
            "The cited literature supports individual component families. "
            "A targeted search did not identify one source integrating all PAN "
            "components, but absence in a targeted search does not prove novelty."
        ),
        "mhrn_literature_status": (
            "Public experimental project; no independent peer-reviewed MHRN "
            "publication or citation was identified in the targeted search."
        ),
        "sources": [dict(item) for item in PAN_LITERATURE],
    }
