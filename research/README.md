# MHRN Research — kanonischer wissenschaftlicher Einstieg

**Stand:** 17. September 2026  
**Aktuelle wissenschaftliche Arbeitsfassung:** Recursive Epistemics **1.8 WIP**  
**Frozen empirical baseline:** Recursive Epistemics **1.5**  
**Grundregel:** `implementation test != DATA != reviewed EVID != interpretation`

Dieses README ist ein Navigations- und Autoritätsindex. Historische DATA, EVID-Entscheidungen, feste Testzahlen und frühere Publikationsstände bleiben erhalten und werden nicht rückwirkend an die aktuelle Interpretation angepasst.

## Aktuelle Publikation

- [CURRENT](publications/CURRENT.md)
- [Vollmanuskript 1.8](publications/2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md)
- [Elfteilige 1.8-Struktur](publications/2026-09-17_recursive-epistemics_v1.8/README.md)
- [Forschungsfragen/Hypothesen/Claims](publications/2026-09-17_recursive-epistemics_v1.8/RESEARCH_REGISTER.md)
- [Vorgängerforschung](publications/2026-09-17_recursive-epistemics_v1.8/PRIOR_WORK_MAP.md)
- [Quelleninventar](publications/2026-09-17_recursive-epistemics_v1.8/SOURCE_INDEX.md)
- [Literatur](publications/2026-09-17_recursive-epistemics_v1.8/REFERENCES.md)
- [Vorgänger 1.7](publications/2026-09-15_recursive-epistemics_v1.7/README.md)
- [Vorgänger 1.6](publications/2026-09-15_recursive-epistemics_v1.6/README.md)
- [Frozen 1.5](publications/FROZEN_V1.5.md)
- [Publikationskatalog](publications/catalog.json)

Der Publication Viewer folgt `publications/catalog.json`; das aktuelle Reader-Ziel ist Edition 1.8 `MANUSCRIPT.md`.

## Aktueller wissenschaftlicher Status

- [Current Scientific State](CURRENT_SCIENTIFIC_STATE.md)
- [Seed-Datenvertrag](specifications/SEED_DATA_CONTRACT.md) — Aufbau, Nutzung und Interpretation seed-gebundener DATA
- [Scientific-Maturity-Manifest](../src/dashboard/static/scientific-progress.json)
- [Scientific Maturity Roadmap](../docs/08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md)
- [Research Integrity Gate](../docs/05-quality/RESEARCH_INTEGRITY_GATE.md)
- [Integrity & Attribution](INTEGRITY_AND_ATTRIBUTION.md)
- [RQ-ETH-001 Provenance Study](protocols/RQ_ETH_001_PROVENANCE_STUDY.md) — Beitrags-/Verantwortungsmatrix; Designstatus, noch nicht präregistriert
- [RQ-EPIST-002 Process Governance Study](protocols/RQ_EPIST_002_PROCESS_GOVERNANCE_STUDY.md) — Vergleich getrennte Status-/Provenienzpakete vs. abgeflachte Summary; Designstatus, noch nicht präregistriert
- [Related Work](RELATED_WORK.md)
- [Open Science / Research Networks](../OPEN_SCIENCE.md) — DOI-, ORCID-, OSF-, Preprint- und Discovery-Routing
- [External Review Deployment](../docs/04-integration/EXTERNAL_REVIEW_DEPLOYMENT.md) — Pages, isolierter Collector und sicherer Aggregat-Export
- [Call for Independent Replication](../INDEPENDENT_REPLICATION.md) — öffentliche Replikationsziele und Anforderungen an Unabhängigkeit
- [Paper Offshoots — Kandidaten für eigenständige Fachbeiträge](paper_offshoots/README.md) — Planung, keine DATA/EVID
- [Wissenschaftliche Bilanz Edition 1.8](publications/2026-09-17_recursive-epistemics_v1.8/SCIENTIFIC_BALANCE.md) — Claim-Ledger, Vollständigkeitsgrenze und offene wissenschaftliche Bilanz

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
| `paper_offshoots/` | begrenzte Kandidaten für eigenständige Fachbeiträge | Planung; keine DATA/EVID oder automatische Neuheitsbehauptung |

Alle Dateien unter `research/` und `docs/` werden zusätzlich durch `scripts/audit_document_governance.py` klassifiziert.

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
6. Stage 6: Human Review von CL-003; danach begrenzte SemanticMemory-Entscheidung sowie kausaler Prediction Error, action-conditioned Mehrschritt-World-Model und Decision Benefit.
7. Spiegel-/Handlungsprädiktion als Stage-4/5/6-Querschnitt; Stage 7 erst bei kausaler Self/Other-Differenzierung.
8. Stage 7: self/other Interventionen und vollständige gekoppelte Checkpointäquivalenz.
9. Dimensionsforschung: gematchte 2D/3D/4D/5D/6D/8D-Ablationen.
10. Prior-Art-, Quellen-, Similarity- und externe Replikationsarbeit.

## Wissenschaftliche Grenzen

Working-/episodische Speichergrundlagen, semantische Kandidaten, Replay-Verträge und Prediction-/World-Model-Infrastruktur sind keine abgeschlossene Semantization, kein etabliertes hierarchisches Predictive Coding und kein validiertes generatives Weltmodell. Der 5D-Adressraum bleibt technische Repräsentation und offene Hypothese. Endpoint-/Pipeline-Erreichbarkeit ist kein erlerntes Tool Use. Historische DATA/EVID werden nicht an neue Instrumentierung umgeschrieben.

## Dokumentgovernance

Siehe [Dokument- und Forschungsgovernance](../docs/00-governance/DOCUMENT_GOVERNANCE.md). Neue Dateien benötigen eine nachvollziehbare Rolle; prominente Platzierung allein erzeugt keine wissenschaftliche Autorität.
