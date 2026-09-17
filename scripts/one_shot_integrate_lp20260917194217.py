#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ED = ROOT / "research/publications/2026-09-17_recursive-epistemics_v1.8"


def append_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8")
    if marker not in current:
        path.write_text(current.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


# Explicitly classify the preparation artifacts. Approval remains proposal authority;
# neither file is execution DATA or scientific EVID.
overrides_path = ROOT / "research/document_governance_overrides.json"
governance = json.loads(overrides_path.read_text(encoding="utf-8"))
overrides = governance["overrides"]
proposal_overrides = {
    "research/learning/preparations/LP-20260917194217.json": {
        "kind": "learning_proposal",
        "status": "current",
        "authority": "proposal_only",
        "mutability": "versioned_replacement_only",
        "citation": "cite_plan_id_and_revision_as_proposal",
        "evidence_role": "proposal_not_evidence",
        "rationale": "Human-origin Stage-6 compression proposal; executed=false and therefore neither DATA nor EVID."
    },
    "research/learning/preparations/LP-20260917194217-approved.json": {
        "kind": "approved_learning_proposal",
        "status": "current",
        "authority": "approved_proposal_only",
        "mutability": "versioned_replacement_only",
        "citation": "cite_plan_id_approval_and_revision_as_proposal",
        "evidence_role": "approval_not_execution_or_evidence",
        "rationale": "Human approval records permission to proceed with preparation; runtime_authority=none and executed=false preserve the non-evidence boundary."
    }
}
governance_changed = False
for path, entry in proposal_overrides.items():
    if overrides.get(path) != entry:
        overrides[path] = entry
        governance_changed = True
if governance_changed:
    overrides_path.write_text(json.dumps(governance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

ledger_path = ED / "sources/content_integration.json"
ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
if not any(x.get("id") == "CORPUS-LP-20260917194217" for x in ledger["entries"]):
    ledger["entries"].append({
        "id": "CORPUS-LP-20260917194217",
        "title": "Approved Stage-6 compression learning proposal LP-20260917194217",
        "source_paths": [
            "research/learning/preparations/LP-20260917194217.json",
            "research/learning/preparations/LP-20260917194217-approved.json"
        ],
        "source_role": "approved human-origin proposal; not executed",
        "manuscript_parts": ["IV", "X", "XI"],
        "integration_status": "semantically_integrated_as_proposal_only",
        "integration_mode": "prospective_stage6_compression_hypothesis_and_controls",
        "boundaries": "authority=proposal_only, executed=false, runtime_authority=none; approval is not execution, DATA or EVID."
    })
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

append_once(
    ED / "parts/04_empirical_programme.md",
    "## 19.9 Genehmigter Stage-6-Kompressionsvorschlag",
    r'''
## 19.9 Genehmigter Stage-6-Kompressionsvorschlag

Mit `LP-20260917194217` liegt ein **genehmigter, aber nicht ausgeführter** human-origin Lernvorschlag vor. Die Forschungsfrage ist enger als der bisherige CL-003-Vergleich: Kann semantische Prototypkonsolidierung bei **10 % des Raw-Replay-Speicherbudgets** mindestens 95 % der Retention eines Raw-Replay-Baselines mit vollem Speicherbudget erreichen?

Der Vorschlag bindet `semantic_prototype_replay_10pct_budget` gegen `raw_replay_full_budget` und nennt als Kontrollen `no_replay`, `random_prototype_10pct` und `learning_off`. Die Evaluation soll auf Holdout-Daten nach sequentiellen Tasks erfolgen. Die Erfolgsmetrik ist `retention_ratio_at_1_10_storage >= 0.95` der Raw-Replay-Retention.

Der aktuelle Status ist strikt prospektiv: `authority=proposal_only`, `executed=false`, `runtime_authority=none`. Die menschliche Genehmigung autorisiert daher weder eine Ergebnisbehauptung noch DATA/EVID. Vor einer wissenschaftlich tragfähigen Ausführung müssen die referenzierten CL-002-/CL-003-Quellen digestscharf gebunden, die noch als `UNKNOWN` markierte Source-Trust-Einstufung geklärt und der Ausführungs-/Freeze-Vertrag entsprechend dem Research-Driven-Development-Prozess fixiert werden.
''',
)

append_once(
    ED / "parts/10_synthesis.md",
    "## 47.10 Neue Richtung nach CL-003: Kompression statt bloßer Gleichheit",
    r'''
## 47.10 Neue Richtung nach CL-003: Kompression statt bloßer Gleichheit

Der genehmigte Vorschlag `LP-20260917194217` zeigt eine methodisch sinnvollere Anschlussfrage an CL-003. Nachdem SemanticMemory im bisherigen matched-budget-Vergleich keinen bestätigten additiven Vorteil gegenüber Raw Replay gezeigt hat, verschiebt sich die nächste prüfbare These von „ist semantisches Replay generell besser?“ zu einer **Ressourcen-/Kompressionsfrage**: Kann eine semantisch verdichtete Repräsentation bei einem Zehntel des Speicherbudgets nahezu dieselbe Retention erreichen?

Das ist derzeit keine Erkenntnis, sondern eine genehmigte Forschungsrichtung. Ihr Wert liegt gerade darin, dass sie eine mögliche Stärke von semantischer Verdichtung dort prüft, wo sie theoretisch plausibler wäre: nicht als pauschaler Leistungsbonus bei gleichem Budget, sondern als Trade-off zwischen Retention und Speicherbedarf.
''',
)

append_once(
    ED / "parts/11_open_landscape.md",
    "## 58.3 LP-20260917194217: offene Kompressionsprüfung",
    r'''
## 58.3 LP-20260917194217: offene Kompressionsprüfung

`LP-20260917194217` ist als nächster möglicher Stage-6-Zyklus vorbereitet und genehmigt, aber **noch nicht ausgeführt**. Der geplante Primärvergleich ist `semantic_prototype_replay_10pct_budget` gegen `raw_replay_full_budget`; die Erfolgsgrenze liegt bei mindestens 95 % der Raw-Replay-Retention bei Faktor-10-Speicherreduktion. `no_replay`, `random_prototype_10pct` und `learning_off` dienen als Kontrollen.

Vor Ausführung sind Source-Digests, Trust-Status, Freeze, Seed-/Taskplan und Analysevertrag zu vervollständigen. Bis dahin bleibt der Eintrag Forschungsplanung und darf im Viewer nicht wie ein Ergebnis oder laufendes Experiment erscheinen.
''',
)

print("LP-20260917194217 integrated as proposal-only")
