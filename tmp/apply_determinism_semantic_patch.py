from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


SEMANTIC_CONTRACTS = '''"""Deterministic semantic contracts for experiment-to-RQ alignment.

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
'''


def patch_experiment_summary() -> None:
    path = ROOT / "src/research/experiment_summary.py"
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "from typing import Any\n",
        "from typing import Any\n\nfrom .semantic_contracts import classify_semantic_status\n",
        label="experiment_summary import",
    )

    start = text.index("def _semantic_status(")
    end = text.index("\ndef _fmt(", start)
    wrapper = '''def _semantic_status(\n    question_id: str, protocol: str, conditions: set[str]\n) -> tuple[str, str]:\n    \"\"\"Compatibility wrapper around the canonical deterministic classifier.\"\"\"\n    return classify_semantic_status(question_id, protocol, conditions)\n\n'''
    text = text[:start] + wrapper + text[end + 1 :]

    old_signature = '''def _render_airr_sections(\n    lines: list[str], experiment_dir: Path, ai_report: dict[str, object]\n) -> None:\n'''
    new_signature = '''def _render_airr_sections(\n    lines: list[str],\n    experiment_dir: Path,\n    ai_report: dict[str, object],\n    semantic_status: str,\n) -> None:\n'''
    text = replace_once(
        text, old_signature, new_signature, label="AIRR summary renderer signature"
    )

    text = replace_once(
        text,
        '''    if not isinstance(content, dict):\n        content = {}\n    lines.extend(\n''',
        '''    if not isinstance(content, dict):\n        content = {}\n    raw_ai_confidence = content.get("ai_confidence", 0.0)\n    visible_ai_confidence = (\n        0.0 if semantic_status == "MISMATCH" else raw_ai_confidence\n    )\n    confidence_gate_note = (\n        " Semantik-Gate: MISMATCH erzwingt 0.0; der rohe Modellwert bleibt nur im AIAR-Audittrail."\n        if semantic_status == "MISMATCH"\n        else ""\n    )\n    lines.extend(\n''',
        label="AIRR visible confidence gate",
    )
    text = replace_once(
        text,
        '''            f"KI-Konfidenz: `{content.get('ai_confidence', 0.0)}` — dies ist keine statistische Konfidenz.",\n''',
        '''            f"KI-Konfidenz: `{visible_ai_confidence}` — dies ist keine statistische Konfidenz.{confidence_gate_note}",\n''',
        label="AIRR summary confidence line",
    )
    text = replace_once(
        text,
        '''        f"- Netzwerkmodus: `{manifest.get('network_mode', 'unknown')}`",\n''',
        '''        f"- Netzwerkmodus: `{manifest.get('network_mode', 'unknown')}`",\n        *(\n            ["- Aussagebereich: `isoliertes Neuronenmodell; keine Netzwerkaussage`"]\n            if protocol == "tonic_spike_reproducibility_v1"\n            else []\n        ),\n''',
        label="tonic scope note",
    )
    text = replace_once(
        text,
        "    _render_airr_sections(lines, experiment_dir, ai_report)\n",
        "    _render_airr_sections(lines, experiment_dir, ai_report, semantic_status)\n",
        label="AIRR renderer call",
    )
    path.write_text(text, encoding="utf-8")


def patch_airr() -> None:
    path = ROOT / "src/research_assistant/airr.py"
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "from typing import Any, cast\n\nfrom .assistant import AnalysisBackend, ResearchAssistant\n",
        "from typing import Any, cast\n\nfrom src.research.semantic_contracts import classify_semantic_status\n\nfrom .assistant import AnalysisBackend, ResearchAssistant\n",
        label="airr semantic import",
    )

    helper = '''def _packet_semantic_status(packet: ResearchPacket) -> tuple[str, str]:\n    \"\"\"Resolve deterministic RQ/protocol/condition alignment from packet data.\"\"\"\n    question_id = str(packet.research_question.get("id", "NOT_AVAILABLE"))\n    protocol_payload = packet.protocol if isinstance(packet.protocol, dict) else {}\n    simulation = (\n        packet.manifest.get("simulation", {})\n        if isinstance(packet.manifest.get("simulation"), dict)\n        else {}\n    )\n    protocol = str(\n        protocol_payload.get("protocol")\n        or simulation.get("protocol")\n        or packet.manifest.get("protocol_id")\n        or "NOT_AVAILABLE"\n    )\n\n    conditions: set[str] = set()\n    data = packet.data if isinstance(packet.data, dict) else {}\n    statistics = data.get("statistics")\n    if isinstance(statistics, dict):\n        statistics_conditions = statistics.get("conditions")\n        if isinstance(statistics_conditions, dict):\n            conditions.update(str(name) for name in statistics_conditions)\n\n    for key in ("run_preview", "runs"):\n        values = data.get(key)\n        if not isinstance(values, list):\n            continue\n        for value in values:\n            if isinstance(value, dict) and value.get("condition") is not None:\n                conditions.add(str(value["condition"]))\n\n    return classify_semantic_status(question_id, protocol, conditions)\n\n\n'''
    marker = "def _build_report(\n"
    if helper in text:
        raise RuntimeError("airr semantic helper already present")
    text = replace_once(
        text, marker, helper + marker, label="airr semantic helper insertion"
    )

    text = replace_once(
        text,
        '''    manifest = packet.manifest\n    content = {\n''',
        '''    manifest = packet.manifest\n    semantic_status, semantic_note = _packet_semantic_status(packet)\n    raw_confidence = writer.output.get("confidence", 0.0)\n    model_confidence = (\n        float(raw_confidence)\n        if isinstance(raw_confidence, (int, float)) and not isinstance(raw_confidence, bool)\n        else 0.0\n    )\n    confidence_blocked = semantic_status == "MISMATCH"\n    reported_confidence = 0.0 if confidence_blocked else model_confidence\n    confidence_gate = (\n        "FORCED_ZERO_SEMANTIC_MISMATCH" if confidence_blocked else "PASSED"\n    )\n    content = {\n''',
        label="airr build semantic state",
    )
    text = replace_once(
        text,
        '''            "claim_support": "NOT_DETERMINED",\n            "rq_status": "IN_PROGRESS",\n        },\n        "ai_confidence": writer.output.get("confidence", 0.0),\n''',
        '''            "claim_support": "NOT_DETERMINED",\n            "rq_status": "IN_PROGRESS",\n            "semantic_alignment": semantic_status,\n            "semantic_note": semantic_note,\n            "confidence_gate": confidence_gate,\n        },\n        "ai_confidence": reported_confidence,\n''',
        label="airr epistemic confidence gate",
    )
    path.write_text(text, encoding="utf-8")


def write_tests() -> None:
    semantic_test = ROOT / "tests/test_determinism_semantic_contracts.py"
    semantic_test.write_text(
        '''from __future__ import annotations\n\nfrom src.research.semantic_contracts import classify_semantic_status\n\n\ndef test_det_001_accepts_same_seed_tonic_replica_pair() -> None:\n    status, note = classify_semantic_status(\n        "RQ-DET-001",\n        "tonic_spike_reproducibility_v1",\n        {"same_seed_tonic_replica_pair"},\n    )\n    assert status == "DIRECT_MATCH"\n    assert "identischem Seed" in note\n\n\ndef test_det_001_accepts_explicit_network_replica_pairs() -> None:\n    status, _ = classify_semantic_status(\n        "RQ-DET-001",\n        "deterministic_replica_v1",\n        {\n            "recurrence_off_replica_a",\n            "recurrence_off_replica_b",\n            "recurrence_on_replica_a",\n            "recurrence_on_replica_b",\n        },\n    )\n    assert status == "DIRECT_MATCH"\n\n\ndef test_snn_002_rejects_tonic_pair_and_points_to_det_001() -> None:\n    status, note = classify_semantic_status(\n        "RQ-SNN-002",\n        "tonic_spike_reproducibility_v1",\n        {"same_seed_tonic_replica_pair"},\n    )\n    assert status == "MISMATCH"\n    assert "RQ-DET-001" in note\n\n\ndef test_snn_002_keeps_registered_recurrence_contract() -> None:\n    status, _ = classify_semantic_status(\n        "RQ-SNN-002",\n        "science_suite_v1",\n        {"recurrence_off", "recurrence_on"},\n    )\n    assert status == "DIRECT_MATCH"\n''',
        encoding="utf-8",
    )

    airr_test = ROOT / "tests/test_airr_semantic_gating.py"
    airr_test.write_text(
        '''from __future__ import annotations\n\nimport json\nfrom pathlib import Path\nfrom typing import Any\n\nfrom src.research_assistant.airr import AIRRPipeline\n\n\ndef _backend(_prompt: str) -> tuple[dict[str, Any], dict[str, str | float]]:\n    return (\n        {\n            "assessment": "Technische Interpretation.",\n            "observations": [],\n            "effect_direction": "not_determined",\n            "methodological_concerns": [],\n            "alternative_explanations": [],\n            "recommended_experiments": [],\n            "requested_evidence": [],\n            "confidence": 0.95,\n        },\n        {"provider": "test", "model": "fixture", "model_digest": "fixture"},\n    )\n\n\ndef _fixture(root: Path, *, conditions: list[str], protocol: str) -> None:\n    experiment = root / "experiments" / "EXP-AIRR-SEM"\n    analysis = experiment / "analysis"\n    analysis.mkdir(parents=True)\n    (root / "registry" / "evidence").mkdir(parents=True)\n    (root / "registry" / "questions.yaml").write_text(\n        "- id: RQ-SNN-002\\n  question: Reproducible spike sequences?\\n",\n        encoding="utf-8",\n    )\n    (root / "registry" / "hypotheses.yaml").write_text(\n        "- id: H-SNN-002-A\\n  research_question: RQ-SNN-002\\n  hypothesis: Reproducible.\\n",\n        encoding="utf-8",\n    )\n    (root / "registry" / "claims.yaml").write_text("[]\\n", encoding="utf-8")\n    (experiment / "workflow.json").write_text(\n        json.dumps({"protocol": protocol}), encoding="utf-8"\n    )\n    (experiment / "manifest.json").write_text(\n        json.dumps(\n            {\n                "experiment_status": "completed",\n                "research_questions": ["RQ-SNN-002"],\n                "hypotheses": ["H-SNN-002-A"],\n                "artifacts": {"workflow": "workflow.json"},\n                "git": {"commit": "abc123", "dirty": False},\n            }\n        ),\n        encoding="utf-8",\n    )\n    runs = [\n        {"condition": condition, "seed": 101, "metrics": {}}\n        for condition in conditions\n    ]\n    (analysis / "ai_packet.json").write_text(\n        json.dumps({"run_preview": runs}), encoding="utf-8"\n    )\n    (analysis / "statistics.json").write_text(\n        json.dumps(\n            {\n                "generated_by": "deterministic_statistics_engine",\n                "conditions": {condition: {"run_count": 1} for condition in conditions},\n            }\n        ),\n        encoding="utf-8",\n    )\n\n\ndef test_airr_forces_reported_confidence_to_zero_on_semantic_mismatch(\n    tmp_path: Path,\n) -> None:\n    _fixture(\n        tmp_path,\n        conditions=["same_seed_tonic_replica_pair"],\n        protocol="tonic_spike_reproducibility_v1",\n    )\n    report = AIRRPipeline(tmp_path).analyze("EXP-AIRR-SEM", _backend)\n    assert report.content["ai_confidence"] == 0.0\n    epistemic = report.content["epistemic_status"]\n    assert epistemic["semantic_alignment"] == "MISMATCH"\n    assert epistemic["confidence_gate"] == "FORCED_ZERO_SEMANTIC_MISMATCH"\n    assert report.content["aiar"]["writer"]["output"]["confidence"] == 0.95\n\n\ndef test_airr_preserves_interpretive_confidence_for_direct_match(\n    tmp_path: Path,\n) -> None:\n    _fixture(\n        tmp_path,\n        conditions=["recurrence_off", "recurrence_on"],\n        protocol="science_suite_v1",\n    )\n    report = AIRRPipeline(tmp_path).analyze("EXP-AIRR-SEM", _backend)\n    assert report.content["ai_confidence"] == 0.95\n    epistemic = report.content["epistemic_status"]\n    assert epistemic["semantic_alignment"] == "DIRECT_MATCH"\n    assert epistemic["confidence_gate"] == "PASSED"\n''',
        encoding="utf-8",
    )


def write_decision_record() -> None:
    path = ROOT / "research/decisions/2026-09-17_determinism_registry_airr_alignment.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '''# Determinism registry and AIRR semantic alignment\n\n**Date:** 2026-09-17  \n**Status:** accepted implementation decision  \n**Scope:** `RQ-SNN-002`, `RQ-DET-001`, AIRR confidence gating\n\n## Decision\n\nHistorical experiment provenance is immutable. `EXP-BATCH-20260914074039-02` therefore remains registered as `RQ-SNN-002`; its observed condition `same_seed_tonic_replica_pair` remains a semantic mismatch for that historical registration and is not post-hoc promoted. Its technical result can be cited as a determinism diagnostic only with the mismatch/provenance limitation attached.\n\n`RQ-DET-001` now has an explicit deterministic semantic contract. It accepts either `same_seed_tonic_replica_pair` for isolated same-seed/same-input replica tests or the four explicit `recurrence_*_replica_a/b` conditions used by `deterministic_replica_v1`. This resolves the prior `NOT_AUTOMATICALLY_CLASSIFIED` state without rewriting old manifests.\n\n`RQ-SNN-002` retains the current registry condition contract `recurrence_off` + `recurrence_on`. The clean existing run `EXP-SNN-002-R2` already satisfies this contract with ten seeds. No duplicate rerun is created merely to repair the registry/pipeline bug.\n\n## AIRR rule\n\nAIRR remains interpretation-only. In addition, the public/report-level `ai_confidence` is deterministically forced to `0.0` whenever semantic alignment is `MISMATCH`. The model's original self-confidence remains available only inside the append-only AIAR record for auditability. This prevents a high model self-rating from visually contradicting a hard semantic evidence block.\n\n## Scope boundary\n\n`tonic_spike_reproducibility_v1` is an isolated-neuron test. Summaries generated for this protocol explicitly state that the result is not a network-level finding. Runtime from such a run must not be used as network-performance evidence.\n\n## Remaining scientific boundary\n\nThe existing `RQ-DET-001` batch artifact was produced from a dirty source tree. After semantic reclassification it may become a direct semantic match, but that does not remove the provenance block. A future clean-tree rerun is required before evidence promotion under the normal human-review/freeze rules.\n\nThe wording of `RQ-SNN-002` (constant-input neuron reproducibility) and its current recurrence-based operational contract are not perfectly isomorphic. This decision does not silently rewrite the research question. A future registry version may split isolated tonic reproducibility from network recurrence reproducibility explicitly; such a change must be preregistered rather than retrofitted to historical runs.\n''',
        encoding="utf-8",
    )


def main() -> None:
    semantic_path = ROOT / "src/research/semantic_contracts.py"
    semantic_path.write_text(SEMANTIC_CONTRACTS, encoding="utf-8")
    patch_experiment_summary()
    patch_airr()
    write_tests()
    write_decision_record()


if __name__ == "__main__":
    main()
