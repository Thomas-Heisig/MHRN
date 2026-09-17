#!/usr/bin/env python3
"""Integrate current accepted scientific-method decisions into Edition 1.8.

This one-shot helper updates only the current synthesis/governance layer. Historical
experiment DATA, manifests, AIRR/AIAR records and EVID remain untouched.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ED = ROOT / "research/publications/2026-09-17_recursive-epistemics_v1.8"


def append_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8")
    if marker in current:
        return
    path.write_text(current.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


# The two decision documents are high-authority methodological interpretations,
# not DATA/EVID. Declare them explicitly so document governance is deterministic.
overrides_path = ROOT / "research/document_governance_overrides.json"
payload = json.loads(overrides_path.read_text(encoding="utf-8"))
overrides = payload["overrides"]
entries = {
    "research/decisions/2026-09-17_determinism_registry_airr_alignment.md": {
        "kind": "scientific_method_decision",
        "status": "current",
        "authority": "accepted_implementation_and_method_decision",
        "mutability": "versioned_replacement_only",
        "citation": "cite_decision_path_and_revision_with_underlying_experiment",
        "evidence_role": "methodological_interpretation_not_evidence_by_itself",
        "rationale": "Accepted decision preserving historical provenance while aligning determinism registry semantics and AIRR confidence gating."
    },
    "research/decisions/2026-09-17_snn003_topology_propagation_v1_adequacy.md": {
        "kind": "scientific_method_decision",
        "status": "current",
        "authority": "accepted_scientific_method_decision",
        "mutability": "versioned_replacement_only",
        "citation": "cite_decision_path_and_EXP-GEN-0047",
        "evidence_role": "adequacy_interpretation_not_evidence_by_itself",
        "rationale": "Accepted adequacy decision: EXP-GEN-0047 is technically valid and semantically matched but inadequate to test H-SNN-003-B; defines prospective v2 requirements."
    },
}
changed = False
for key, value in entries.items():
    if overrides.get(key) != value:
        overrides[key] = value
        changed = True
if changed:
    overrides_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Add these decisions to the semantic corpus ledger.
ledger_path = ED / "sources/content_integration.json"
ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
if not any(x.get("id") == "CORPUS-SCIENTIFIC-DECISIONS" for x in ledger["entries"]):
    ledger["entries"].append(
        {
            "id": "CORPUS-SCIENTIFIC-DECISIONS",
            "title": "Accepted scientific-method decisions and adequacy rulings",
            "source_paths": [
                "research/decisions/2026-09-17_determinism_registry_airr_alignment.md",
                "research/decisions/2026-09-17_snn003_topology_propagation_v1_adequacy.md"
            ],
            "source_role": "accepted methodological interpretation and prospective design constraint",
            "manuscript_parts": ["IV", "VI", "X", "XI"],
            "integration_status": "semantically_integrated_without_evidence_promotion",
            "integration_mode": "registry_semantics_adequacy_and_prospective_design_synthesis",
            "boundaries": "Historical DATA/manifests remain immutable; semantic alignment does not erase provenance blocks, and test inadequacy is neither confirmation nor refutation of the target hypothesis."
        }
    )
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

append_once(
    ED / "parts/04_empirical_programme.md",
    "## 19.8 Determinismus-Registry, AIRR und Testadäquanz",
    r'''
## 19.8 Determinismus-Registry, AIRR und Testadäquanz

Zwei Entscheidungen vom 17. September 2026 präzisieren die Verwendung der jüngsten SNN-DATA. Erstens bleibt der historische Lauf `EXP-BATCH-20260914074039-02` unverändert `RQ-SNN-002` zugeordnet. Seine beobachtete Condition `same_seed_tonic_replica_pair` ist für diese historische Registrierung ein semantischer Mismatch und darf nicht post hoc umetikettiert werden. Der technische Befund kann als Determinismusdiagnostik zitiert werden, aber nur gemeinsam mit dieser Provenienzgrenze.

`RQ-DET-001` besitzt nun einen expliziten Determinismusvertrag: entweder isolierte Same-Seed/Same-Input-Tonic-Replikapaare oder die expliziten `recurrence_off/on_replica_a/b`-Bedingungen. `RQ-SNN-002` behält dagegen seinen Recurrence-off/on-Vertrag; der bestehende saubere Lauf `EXP-SNN-002-R2` erfüllt diesen mit zehn Seeds. Ein neuer Lauf wird nicht allein erzeugt, um einen Registry-/Pipelinefehler kosmetisch zu reparieren.

AIRR bleibt Interpretation-only. Bei semantischem `MISMATCH` wird die öffentliche/reportseitige `ai_confidence` deterministisch auf `0.0` gesetzt; die ursprüngliche Modellselbsteinschätzung bleibt nur im append-only AIAR-Auditdatensatz. Ein isolierter Tonic-Test ist außerdem ausdrücklich **kein Netzwerkbefund** und seine Laufzeit darf nicht als Netzwerkperformance interpretiert werden.

Die zweite Entscheidung betrifft `EXP-GEN-0047` und `H-SNN-003-B`. Die sechs Conditions `1d`, `2d`, `3d`, `5d`, `5d_shuffled` und `random_graph` sind semantisch korrekt und der Lauf ist technisch reproduzierbar. Dennoch ist `topology_propagation_v1` **INADEQUATE_TO_TEST_HYPOTHESIS**: Nur drei Neuronen und zwei feed-forward Synapsen tragen die Dynamik; bei den nicht-randomisierten Bedingungen verändert sich die Koordinate, aber nicht ausreichend der kausale Übertragungsmechanismus. Daher sind identische Ergebnisse über 1D/2D/3D/5D weder ein Topologie-Nullbefund noch eine Widerlegung eines 5D-Effekts.

Die einzige deskriptive Abweichung des v1-Laufs — eine um einen Tick frühere First-Response-Latency im `random_graph` — ist konfundiert mit einer geänderten Kantenanordnung und darf nicht zum Dimensionseffekt hochgestuft werden. Auch `stopped_on_quiescence=false` ist kein Fehler: Der Runner setzt `min_ticks=max_ticks` und erzwingt damit das vollständige Beobachtungsfenster.

Für `topology_propagation_v2` gilt deshalb ein stärkerer prospektiver Vertrag: mindestens 1.000 Neuronen pro Condition, im Mittel mindestens zehn eingehende Synapsen, gematchte globale Struktur/Parameter/Stimulusenergie, explizite Kopplung von Geometriedistanz an Konnektivitätswahrscheinlichkeit und/oder Delay, die sechs genannten Kontrollen einschließlich degree-/density-matched Random Graph, multi-neuronaler Input, First-Arrival-/Reach-Verteilungen als Primärgrößen, Activity-Adequacy-Gate, mehrere unabhängige Seeds, vorab eingefrorene Inferenzregel und clean-tree Provenienz. Diese Werte sind Mindestschwellen für die nächste Testgeneration, keine Behauptung allgemeiner Suffizienz.
''',
)

append_once(
    ED / "parts/10_synthesis.md",
    "## 47.9 Neue methodische Erkenntnis: semantischer Match ist nicht Testadäquanz",
    r'''
## 47.9 Neue methodische Erkenntnis: semantischer Match ist nicht Testadäquanz

Die jüngsten Determinismus- und Topologieentscheidungen schärfen eine zentrale Lehre von MHRN: **Semantische Zuordnung, technische Reproduzierbarkeit und Hypothesentestadäquanz sind drei verschiedene Prüfungen.** Ein Experiment kann die richtigen registrierten Conditions besitzen und byte-/metrisch reproduzierbar laufen, während sein Mechanismus dennoch nicht sensitiv genug ist, die Zielhypothese zu beantworten.

`EXP-GEN-0047` ist dafür das Referenzbeispiel. Die korrekte Schlussfolgerung lautet nicht „Topologie hat keinen Effekt“, sondern „dieser v1-Aufbau macht Topologie nicht ausreichend kausal wirksam, um den Effekt zu testen“. Damit wird ein scheinbarer Nullbefund in eine Designkorrektur überführt, ohne DATA umzuschreiben.

Analog zeigt die Determinismus-Registry-Korrektur, dass ein technisch passender Befund durch falsche historische RQ-Zuordnung nicht nachträglich zu EVID umetikettiert werden darf. Die wissenschaftlich stärkere Lösung ist, historische Provenienz zu erhalten und den prospektiven Vertrag zu reparieren.
''',
)

append_once(
    ED / "parts/11_open_landscape.md",
    "## 58.2 Topologie v2 und saubere Determinismus-Replikation",
    r'''
## 58.2 Topologie v2 und saubere Determinismus-Replikation

Aus den aktuellen Entscheidungen entstehen zwei klar begrenzte nächste Schritte. Für `RQ-DET-001` ist ein clean-tree-Replikationslauf erforderlich, bevor ein durch Dirty-Tree-Provenienz blockiertes Artefakt regulär in Richtung EVID geprüft werden kann. Eine semantische Reklassifikation allein entfernt den Provenienzblock nicht.

Für `H-SNN-003-B` muss `topology_propagation_v2` **vor Ausführung** präregistriert werden. Der neue Aufbau muss Topologie durch Konstruktion auf Dynamik wirken lassen und zunächst ein Activity-Adequacy-Gate bestehen. Scheitert dieses Gate, ist der Hypothesentest `NOT_TESTED`, nicht negativ. Erst danach dürfen vorab definierte Vergleiche zwischen 1D/2D/3D/5D, `5d_shuffled` und einem degree-/density-matched `random_graph` interpretiert werden. Dabei wird ausdrücklich kein 5D-Vorteil vorausgesetzt; die Hypothese verlangt zunächst nur einen belastbaren Unterschied zwischen mindestens zwei Topologiebedingungen.
''',
)

print("Scientific decisions integrated into Edition 1.8 and document governance")
