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
    ]
