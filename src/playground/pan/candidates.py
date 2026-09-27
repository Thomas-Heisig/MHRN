"""Non-canonical research-question candidates derived from PAN exploration."""

from __future__ import annotations


def pan_research_candidates() -> list[dict[str, object]]:
    """Return ideas only; these are never registered hypotheses."""

    return [
        {
            "id": "PAN-CANDIDATE-HOMEOSTATIC-SURVIVAL",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Does health-modulated multi-scale homeostasis change recovery "
                "after matched perturbations in recurrent SNNs?"
            ),
            "required_controls": [
                "matched neuron and edge budgets",
                "fixed seeds",
                "homeostasis-disabled control",
                "lesion or perturbation control",
            ],
        },
        {
            "id": "PAN-CANDIDATE-HD-FEEDBACK",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Does bounded hyperstate feedback alter stability or recovery "
                "relative to a matched no-feedback recurrent network?"
            ),
            "required_controls": [
                "feedback gain zero",
                "coordinate shuffle",
                "matched recurrent topology",
                "seed-paired runs",
            ],
        },
        {
            "id": "PAN-CANDIDATE-INFO-AXIS",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Can a formally specified information measure replace the current "
                "local surprise proxy and support a preregistered PAN comparison?"
            ),
            "required_controls": [
                "define PID sources and target before implementation",
                "validate estimator bias",
                "compare against entropy/surprise baselines",
            ],
        },
        {
            "id": "PAN-CANDIDATE-AGING",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Do bounded health, energy and apoptosis dynamics produce "
                "reproducible network-level transitions under matched stress?"
            ),
            "required_controls": [
                "health decay zero",
                "apoptosis disabled",
                "matched input and topology",
                "predefined transition metric",
            ],
        },
        {
            "id": "PAN-CANDIDATE-GEOMETRIC-SCALING",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "How does candidate and realized out-degree scale with geometric "
                "dimension under explicitly matched density, radius and metric?"
            ),
            "required_controls": [
                "define lattice or point process before comparison",
                "hold N and connection rule fixed",
                "report metric and boundary conditions",
                "do not assume universal neighbour counts",
            ],
        },
        {
            "id": "PAN-CANDIDATE-TOPOLOGICAL-SHORTCUTS",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Do independent cyclic a/b axes create shortcut edges and alter "
                "path length or clustering relative to matched xyz-only graphs?"
            ),
            "required_controls": [
                "xyz-only control",
                "mixed-additive metric control",
                "shortcut-union control",
                "matched edge budget and seeds",
            ],
        },
        {
            "id": "PAN-CANDIDATE-ACTIVITY-POSITIONING",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Can a preregistered activity- or information-driven geometric "
                "position rule produce stable self-organized clustering?"
            ),
            "required_controls": [
                "positioning disabled control",
                "define movement objective before implementation",
                "use surprise proxy before any PID claim",
                "matched initialization and topology",
            ],
        },
        {
            "id": "PAN-CANDIDATE-GATE-EMERGENCE",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Do settings-derived gate schematics remain behaviorally stable "
                "under matched parameter sweeps and seeds?"
            ),
            "required_controls": [
                "fixed config-to-gate mapping",
                "seed-paired runs",
                "gate-disabled control",
            ],
        },
        {
            "id": "PAN-CANDIDATE-DUAL-MODE-CONSISTENCY",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Under what bounded conditions do dual event/continuous runs "
                "agree with continuous-only reference runs?"
            ),
            "required_controls": [
                "identical initial state",
                "matched dt and input",
                "predefined equivalence tolerance",
            ],
        },
        {
            "id": "PAN-CANDIDATE-GENERATIVE-GROWTH",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Does bounded event-driven growth produce reproducible topology "
                "changes under matched activity histories?"
            ),
            "required_controls": [
                "growth-disabled control",
                "fixed-capacity pool control",
                "matched edge budgets and seeds",
            ],
        },
        {
            "id": "PAN-CANDIDATE-MEMORY-SCALING",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "How does estimated hot-state memory scale with neuron count, "
                "edge count and PAN state dimension?"
            ),
            "required_controls": [
                "measured allocator validation before CUDA claims",
                "dtype and index-width reporting",
                "peak-memory rather than nominal-state comparison",
            ],
        },
        {
            "id": "PAN-CANDIDATE-HARDWARE-NATIVE-EMERGENCE",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Does a future measured register-native CUDA implementation alter "
                "runtime dynamics or resource scaling relative to the reference backend?"
            ),
            "required_controls": [
                "same model and seeds on reference and CUDA backends",
                "measured occupancy/register counts",
                "measured VRAM and bandwidth",
                "no PTX or hardware-native claim before implementation",
            ],
        },
        {
            "id": "PAN-CANDIDATE-BEHAVIORAL-EMERGENCE",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Does reward-modulated policy learning generalize behavior to "
                "new inputs without storing exact external payloads?"
            ),
            "required_controls": [
                "policy-frozen control",
                "novel-input transfer split",
                "matched reward schedule",
                "payload leakage audit",
            ],
        },
        {
            "id": "PAN-CANDIDATE-HYBRID-COGNITION",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Does coupling PAN to the existing Gateway/Neural-Symbiosis "
                "interfaces yield measurable task benefits over fixed routing?"
            ),
            "required_controls": [
                "fixed gateway routing",
                "random/shuffle gateway controls",
                "matched external model/tool outputs",
                "separate PAN and peripheral contribution analysis",
            ],
        },
        {
            "id": "PAN-CANDIDATE-LAYER-EMERGENCE",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Do plastic layer gains or connectivity develop reproducible "
                "functional specialization beyond the initial layer assignment?"
            ),
            "required_controls": [
                "fixed-layer non-plastic control",
                "shuffled layer labels",
                "matched topology and seeds",
                "predefined specialization metric",
            ],
        },
        {
            "id": "PAN-CANDIDATE-SPATIAL-LIFECYCLE",
            "status": "DRAFT_IDEA_NOT_PREREGISTERED",
            "question": (
                "Can apoptosis and separately implemented neurogenesis maintain "
                "spatial density under matched stress and replacement rules?"
            ),
            "required_controls": [
                "apoptosis-only control",
                "neurogenesis-only control",
                "fixed population control",
                "predefined density and turnover metrics",
            ],
        },
    ]
