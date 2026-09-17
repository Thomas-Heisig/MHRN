"""Deterministic semantic contracts for experiment-to-RQ alignment.

This module is deliberately model-free. It classifies whether observed protocol
conditions match the registered research-question contract. The result gates
scientific evidence readiness and AI-report confidence, but never promotes an
experiment to scientific evidence by itself.
"""

from __future__ import annotations

_SUITE_REQUIRED_GROUPS = {
    "ping",
    "temporal",
    "stdp",
    "learning",
    "time",
    "5d",
    "regulation",
}


def classify_design_adequacy(question_id: str, protocol: str) -> tuple[str, str]:
    """Classify known protocol-level adequacy limits independently of semantics.

    A semantic match only says that the intended registered conditions are
    present. It does not imply that the implemented design has enough structure,
    activity or causal coupling to test the hypothesis.
    """
    if question_id == "RQ-SNN-003" and protocol == "topology_propagation_v1":
        return (
            "INADEQUATE_TO_TEST_HYPOTHESIS",
            "topology_propagation_v1 verwendet eine feste Drei-Neuronen-Kette mit zwei Synapsen. Die Dimensionskoordinaten werden variiert, aber die wesentlichen Kanten, Gewichte und Delays sind fest vorgegeben. Das Design ist daher nicht hinreichend sensitiv, um H-SNN-003-B als Topologie-/Geometriehypothese zu testen; identische Ausgaben sind kein Nullbefund gegen einen Topologieeffekt.",
        )
    if question_id == "RQ-SNN-003":
        return (
            "REQUIRES_EXPLICIT_REVIEW",
            "Für RQ-SNN-003 muss die Testadäquanz separat von der Condition-Semantik geprüft werden. Erforderlich sind insbesondere ausreichend große Netzwerke, gematchte Dichte/Größe, ein expliziter geometrischer Kopplungsmechanismus, regionale Stimulation und verteilungsbasierte Propagationsmetriken.",
        )
    return (
        "NOT_ASSESSED",
        "Für diese Forschungsfrage ist keine automatische Designadäquanz-Regel registriert.",
    )


def classify_semantic_status(
    question_id: str, protocol: str, conditions: set[str]
) -> tuple[str, str]:
    """Classify direct RQ tests separately from matching substudies in a suite."""
    plain = {item.split(":", 1)[-1] for item in conditions}

    def classify(found: bool, note: str) -> tuple[str, str]:
        if not found:
            return "MISMATCH", note
        if protocol == "science_all_v1":
            return (
                "CONTAINS_MATCH",
                note + " Die relevante Teilstudie ist in science_all_v1 enthalten; "
                "nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten.",
            )
        return "DIRECT_MATCH", note

    if question_id == "RQ-REC-001":
        return classify(
            any(item.startswith("w0_") for item in plain)
            and any(
                item.startswith("w100_") or item.startswith("w125_") for item in plain
            ),
            "REC-001 erwartet eine registrierte Rekurrenz-Gewicht/Delay-Karte mit Nullkontrolle.",
        )
    if question_id == "RQ-REC-002":
        return classify(
            {"loop_delay_1", "loop_delay_2", "loop_delay_4", "loop_delay_8"}.issubset(
                plain
            ),
            "REC-002 erwartet die registrierte Loop-Delay-Leiter.",
        )
    if question_id == "RQ-GEN-001":
        return classify(
            any(item.startswith("learning_on_drive_") for item in plain)
            and any(item.startswith("learning_off_drive_") for item in plain)
            and any(item.startswith("sham_replay_drive_") for item in plain),
            "GEN-001 erwartet Learning-on, Learning-off und Sham-Replay über registrierte Perturbationsproben.",
        )
    if question_id == "RQ-REPL-001":
        return classify(
            {"recurrence_off", "recurrence_on"}.issubset(plain),
            "REPL-001 erwartet beide Rekurrenzarme mit unabhängiger Seedstrategie.",
        )
    if question_id == "RQ-5D-005":
        return classify(
            {"1d", "2d", "3d", "5d"}.issubset(plain),
            "5D-005 erwartet topology-matched 1D/2D/3D/5D-Einbettungen.",
        )
    if question_id == "RQ-REG-002":
        return classify(
            {"regulation_off", "regulation_on"}.issubset(plain),
            "REG-002 erwartet Regulation-off und Regulation-on unter gleichem Perturbationsplan.",
        )
    if question_id == "RQ-TEMP-002":
        return classify(
            {"forward", "reverse", "simultaneous"}.issubset(plain),
            "TEMP-002 erwartet Forward-, Reverse- und Simultankontrolle.",
        )
    if question_id == "RQ-PERF-001":
        return classify(
            "subsystem_profile" in plain,
            "PERF-001 erwartet subsystemaufgelöste Runtime-Messungen.",
        )
    if question_id == "RQ-LIFE-001":
        return classify(
            "sequential_three_task_screen" in plain,
            "LEARN-INTERF-001 v1 ist ein explizit als Vorläufer markierter Interferenz-Screen.",
        )
    if question_id.startswith("RQ-PING-"):
        return classify(
            {"recurrence_off", "recurrence_on"}.issubset(plain),
            "PING erwartet recurrence_off und recurrence_on.",
        )
    if question_id.startswith("RQ-TEMP-"):
        return classify(
            "fast_medium_slow" in plain,
            "TEMP erwartet fast_medium_slow mit FAST/MEDIUM/SLOW-Horizonten.",
        )
    if question_id.startswith("RQ-TIME-"):
        time_conditions = {
            item.split(":", 1)[1]
            for item in conditions
            if item.startswith("time:") and ":" in item
        }
        direct_conditions = {item for item in conditions if ":" not in item}
        candidates = time_conditions or direct_conditions
        return classify(
            bool(candidates) and all(item.isdigit() for item in candidates),
            "TIME erwartet numerische Tick-Leiter-Bedingungen.",
        )
    if question_id.startswith("RQ-5D-"):
        return classify(
            {"1d", "2d", "3d", "5d", "random_graph"}.issubset(plain),
            "5D erwartet die registrierten Dimensions-/Topologiebedingungen.",
        )
    if question_id == "RQ-SUITE-001":
        present_groups = {item.split(":", 1)[0] for item in conditions if ":" in item}
        found = (
            _SUITE_REQUIRED_GROUPS.issubset(present_groups)
            and protocol == "science_all_v1"
        )
        return (
            "DIRECT_MATCH" if found else "MISMATCH",
            "SUITE erwartet science_all_v1 und PING, TEMP, STDP, Learning, TIME, 5D sowie Regulation unter gemeinsamer Provenienz.",
        )
    if question_id == "RQ-DET-001":
        tonic_replica_pair = "same_seed_tonic_replica_pair" in plain
        recurrence_replica_pair = {
            "recurrence_off_replica_a",
            "recurrence_off_replica_b",
            "recurrence_on_replica_a",
            "recurrence_on_replica_b",
        }.issubset(plain)
        return classify(
            tonic_replica_pair or recurrence_replica_pair,
            "RQ-DET-001 erwartet gepaarte Replikate mit identischem Seed, Input und Ausgangszustand. Zulässig sind die isolierte Tonic-Replikapaar-Bedingung oder explizite A/B-Replikate beider Rekurrenzarme.",
        )
    if question_id == "RQ-SNN-003":
        return classify(
            {
                "1d",
                "2d",
                "3d",
                "5d",
                "5d_shuffled",
                "random_graph",
            }.issubset(plain),
            "RQ-SNN-003 erwartet 1d, 2d, 3d, 5d, 5d_shuffled und random_graph unter gematchter Versuchsführung. Diese Regel prüft ausschließlich die semantische Condition-Zuordnung; die Testadäquanz des konkreten Protokolls wird separat bewertet.",
        )
    if question_id == "RQ-SNN-002":
        return classify(
            {"recurrence_off", "recurrence_on"}.issubset(plain),
            "RQ-SNN-002 erwartet nach aktuellem Registry-Vertrag einen kontrollierten Impulsantwort-Vergleich mit recurrence_off und recurrence_on. same_seed_tonic_replica_pair ist ein Determinismus-Diagnostikum für RQ-DET-001 und wird nicht post-hoc als Evidenz für RQ-SNN-002 umetikettiert.",
        )
    if question_id == "RQ-SNN-001":
        if protocol == "sustained_activity_stability_v1":
            return (
                "DIRECT_MATCH",
                "RQ-SNN-001 verwendet das dedizierte Sustained-Activity-Protokoll mit Kontroll- und Tonic-Drive-Bedingung.",
            )
        return (
            "MISMATCH",
            "RQ-SNN-001 fordert langfristig stabile Spike-Dynamik unter fortlaufender Aktivitaet. science_suite_v1/science_all_v1 bleiben dafuer diagnostisch; eine Primaerpruefung erfordert weiterhin ein dediziertes Sustained-Activity-Protokoll.",
        )
    return (
        "NOT_AUTOMATICALLY_CLASSIFIED",
        "Keine automatische semantische Regel fuer diese RQ-Familie registriert.",
    )
