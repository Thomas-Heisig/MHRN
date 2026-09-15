# MHRN Research — kanonischer wissenschaftlicher Einstieg

**Stand:** 15. September 2026  
**Aktuelle wissenschaftliche Arbeitsfassung:** Recursive Epistemics **1.7 WIP**  
**Frozen empirical baseline:** Recursive Epistemics **1.5**  
**Grundregel:** `implementation test != DATA != reviewed EVID != interpretation`

Dieses README ist ab Fassung 1.7 ein **Navigations- und Autoritätsindex**. Frühere Statusblöcke, feste Testzahlen, Branchstände und zeitgebundene Forschungszusammenfassungen bleiben in ihren historischen Dokumenten erhalten, werden hier aber nicht mehr als aktueller Stand wiederholt.

## Aktuelle Publikation

- [CURRENT](publications/CURRENT.md)
- [Vollmanuskript 1.7](publications/2026-09-15_recursive-epistemics_v1.7/MANUSCRIPT.md)
- [Forschungsbericht 1.7](publications/2026-09-15_recursive-epistemics_v1.7/FORSCHUNGSBERICHT.md)
- [Worte des Autors](publications/2026-09-15_recursive-epistemics_v1.7/AUTHOR_POSITION.md)
- [Beitrags-/Neuheitsmatrix](publications/2026-09-15_recursive-epistemics_v1.7/CONTRIBUTION_MAP.md)
- [Frozen 1.5](publications/FROZEN_V1.5.md)
- [Vorgänger 1.6](publications/2026-09-15_recursive-epistemics_v1.6/README.md)
- [Publikationskatalog](publications/catalog.json)

Der Publication Viewer folgt `publications/catalog.json`. Ab 1.7 ist das direkte Reader-Ziel das aktuelle `MANUSCRIPT.md`.

## Aktueller wissenschaftlicher Status

- [Current Scientific State](CURRENT_SCIENTIFIC_STATE.md)
- [Scientific-Maturity-Manifest](../src/dashboard/static/scientific-progress.json)
- [Scientific Maturity Roadmap](../docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md)
- [Research Integrity Gate](../docs/05-quality/RESEARCH_INTEGRITY_GATE.md)
- [Integrity & Attribution](INTEGRITY_AND_ATTRIBUTION.md)
- [Related Work](RELATED_WORK.md)

Engineering-Reife und wissenschaftliche Reife werden getrennt geführt. Kein Stage-Score ist eine Kognitions-, Intelligenz- oder Bewusstseinskennzahl.

## Kanonische Forschungsobjekte

| Bereich | Rolle | Autorität |
|---|---|---|
| `registry/` | RQ, Hypothesen, Claims und verwandte Register | normativ für Forschungsdefinitionen |
| `schemas/` | maschinenlesbare Forschungsverträge | normativ für Struktur/Validierung |
| `protocols/` | Methoden-/Protokollverträge | normativ für jeweilige Ausführung |
| `experiments/` | Ausführungsartefakte, DATA, Receipts, Reviews | experimentbezogen; nicht automatisch EVID |
| `literature/` | strukturierte Literatur und Quellenprovenienz | Quellenindex |
| `generated/` | generierte Reports/Projektionen | abgeleitet, nicht allein evidenztragend |
| `specifications/` | technische/wissenschaftliche Spezifikationen | Design-/Methodenvertrag |
| `ethics/` | Ethik-/Wohlfahrtsregeln | normative Forschungsgrenze |
| `critique/` | Kritik, Gegenargumente, Limits | kritische Interpretation |
| `external_review/` | externe/standardisierte Reviewstruktur | Reviewstatus, keine automatische EVID |
| `publications/` | versionierte wissenschaftliche Fassungen | Interpretation mit Editionsprovenienz |

Alle Dateien unter `research/` und `docs/` werden zusätzlich durch `scripts/audit_document_governance.py` klassifiziert. Hochautoritative Ausnahmen stehen in `document_governance_overrides.json`.

## Forschungsworkflow

```text
Research Question
    ↓
Hypothesis
    ↓
frozen / preregistered protocol
    ↓
Experiment
    ↓
DATA
    ↓
analysis + limitations
    ↓
human / independent review
    ↓
EVID decision
    ↓
bounded claim
```

Explorative oder technische Läufe dürfen DATA erzeugen, aber keine bestätigende Evidenz vortäuschen. Boundary Audits prüfen Grenzen/Verträge und sind nicht automatisch direkte Tests einer inhaltlichen Hypothese.

## Aktuelle priorisierte Forschung

1. Stage 0: Modell-/Integrator-/Parameterablationen.
2. Stage 2: unabhängige Replikation, Zielskalierung und Störungsrobustheit.
3. Stage 3: held-out Multi-Seed-Plastizität, Ressourcen-/Langzeitstabilität.
4. Stage 4: modality-specific vs. general matched controls, frozen/random/shuffle/lesion.
5. Stage 5: Real-Device-/Closed-loop-, Sensor-Loss- und Actuator-No-Effect-Studien.
6. Stage 6: Replay/Konsolidierung→Semantization, kausaler neuronaler Prediction Error, action-conditioned Mehrschritt-World-Model und Decision Benefit.
7. Stage 7: self/other Interventionen und vollständige gekoppelte Checkpointäquivalenz.
8. Dimensionsforschung: gematchte 2D/3D/4D/5D/6D/8D-Ablationen.
9. Prior-Art-Prüfung potenzieller MHRN-Beiträge.
10. externe Quellen-/Similarity-/Methodenprüfung vor formaler Einreichung.

## Stage-6-Grenze

Working-/episodische Speichergrundlagen, semantische Kandidaten, Replay-Verträge und Prediction-/World-Model-Infrastruktur sind **keine** abgeschlossene Semantization, **kein** etabliertes hierarchisches Predictive Coding und **kein** vollständig validiertes generatives Weltmodell. Diese stärkeren Aussagen benötigen mechanismusspezifische Interventionen und Replikation.

## 5D- und Skalierungsgrenze

Der 5D-Adressraum ist eine technische Repräsentation und offene Hypothese. Eine Überlegenheit ist nicht etabliert. Aggregierte Topologiegrößen sind nicht automatisch dynamische Großskalierungsexperimente. Dimensions- und Skalierungsclaims benötigen gematchte kontrollierte Läufe.

## Gateway-/Embodiment-Grenze

Endpoint- oder Pipeline-Erreichbarkeit ist kein erlerntes Tool Use. Sensor-Discovery ist keine Aktivierung. Content Gateway und Compute Backend werden getrennt behandelt, damit Informationsherkunft/Kausalität nicht mit Hardware-/Backendausführung vermischt wird.

## Forschungsintegrität

MHRN befürwortet kumulative, möglichst frei weiterverwendbare Wissenschaft. Daraus folgt eine strikte Herkunftspflicht: externe Methode, MHRN-Vorarbeit, eigene Transformation und ungeklärte Neuheit werden getrennt markiert. Unbestätigte Quellen bleiben quarantined. Interne Audits reduzieren Plagiats-/Attributionsrisiken, zertifizieren aber keine Plagiatsfreiheit.

## Historische Daten und Publikationen

Historische DATA, EVID-Entscheidungen, veröffentlichte Digests und frozen Publikationen werden nicht rückwirkend an neue Instrumentierung oder Interpretation angepasst. Verbesserte Messung führt zu einem neuen Experiment.

- [Frozen 1.5](publications/FROZEN_V1.5.md)
- [Publikationsarchiv](publications/README.md)
- [Experimente](experiments/)

## Dokumentgovernance

Siehe [Dokument- und Forschungsgovernance](../docs/00-governance/DOCUMENT_GOVERNANCE.md).

Neue Dateien müssen eine nachvollziehbare Rolle besitzen. Das Governance-Gate klassifiziert rekursiv jede reale Datei nach Status, Autorität, Mutabilität, Zitierregel und Evidenzrolle. Physische Verschiebungen historischer Artefakte erfolgen nur, wenn Provenienz und Referenzen erhalten bleiben.
