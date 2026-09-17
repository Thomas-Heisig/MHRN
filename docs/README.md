<!-- publication-current-1.8 -->
> Aktuelle wissenschaftliche Arbeitsfassung: [Edition 1.8](../research/publications/2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md). Aeltere Editionsangaben dokumentieren ihren damaligen Stand.

# MHRN Documentation — kanonischer Einstieg

**Stand:** 15. September 2026  
**Kanonischer Codezweig:** `main`  
**Aktuelle wissenschaftliche Arbeitsfassung:** Recursive Epistemics **1.7 WIP**  
**Dokumentgovernance:** [`00-governance/DOCUMENT_GOVERNANCE.md`](00-governance/DOCUMENT_GOVERNANCE.md)

Dieses README ist ausschließlich ein **aktueller Navigations- und Autoritätsindex**. Historische Testzahlen, Commitstände, Sprintberichte und frühere Publikationsstände gehören in versionierte/historische Dateien und werden hier nicht mehr als „current state“ wiederholt.

## Autorität und Lesereihenfolge

Wenn Dokumente widersprechen, gilt:

1. Code, Schemas und maschinenlesbare Verträge auf `main`;
2. aktuelle CI-/Verifikationsartefakte;
3. source-bound Experiment-DATA und ausdrücklich akzeptierte EVID;
4. kanonische Quality-/Architektur-/Methodendokumente;
5. aktuelle WIP-Publikation;
6. generierte Projektionen;
7. historische, superseded und archivierte Dokumente.

`test passed != experiment DATA != accepted EVID != interpretation`.

## Aktuelle wissenschaftliche Fassung

- [Publication Current Pointer](../research/publications/CURRENT.md)
- [Vollmanuskript 1.7](../research/publications/2026-09-15_recursive-epistemics_v1.7/MANUSCRIPT.md)
- [Forschungsbericht 1.7](../research/publications/2026-09-15_recursive-epistemics_v1.7/FORSCHUNGSBERICHT.md)
- [Vorgänger 1.6](../research/publications/2026-09-15_recursive-epistemics_v1.6/README.md)
- [Frozen empirical baseline 1.5](../research/publications/FROZEN_V1.5.md)

Der Publication Viewer folgt dem maschinenlesbaren `research/publications/catalog.json` und soll stets die aktuelle WIP-Fassung öffnen. Frozen/historical Editions bleiben separat zitierbar.

## Dokumentbereiche

| Bereich | Rolle | typische Autorität |
|---|---|---|
| `00-governance/` | Dokument- und Informationsgovernance | normativ für Dokumentstatus |
| `01-guides/` | Anleitungen | operativ, nicht wissenschaftliche Evidenz |
| `02-architecture/` | Architektur-/Subsystemverträge | technischer Design-/Vertragsstand |
| `03-dashboard/` | Dashboard, API, UI | technischer Interfacevertrag |
| `04-integration/` | Integrationsnotizen | kontext-/versionsabhängig |
| `05-quality/` | Quality, Integrity, Gates | normative Qualitätsregeln |
| `06-research/` | Forschungspositionierung | Interpretation/Methodik |
| `07-changelog/` | datierte Änderungen | historische Entwicklungsprovenienz |
| `08-roadmap/` | Roadmap/TODO | Planung, niemals Ergebnisnachweis |
| `09-sprints/` | Sprintstände | historisch/zeitgebunden |
| `10-releases/` | Releaseakten | releasebezogene Provenienz |
| `11-readme/` | frühere README-Blöcke | historisch |
| `12-updates/` | Integrations-/Update-Snapshots | zeitgebunden |
| `99-archive/` | Altmaterial | archiviert/historisch |

Jede einzelne Datei wird zusätzlich durch `scripts/audit_document_governance.py` maschinenlesbar klassifiziert.

## Kanonische aktuelle Dokumente

### Governance / Qualität

- [Document Governance](00-governance/DOCUMENT_GOVERNANCE.md)
- [Research Integrity Gate](05-quality/RESEARCH_INTEGRITY_GATE.md)
- [Quality Gate](05-quality/QUALITY_GATE.md)

### Architektur

- [Architecture](02-architecture/ARCHITECTURE.md)
- [Scientific Contracts Alpha.3](02-architecture/SCIENTIFIC_CONTRACTS_ALPHA3.md) — versionsgebundener Vertrag, nicht alleinige Current-Übersicht
- [Adaptive Wesen Body](02-architecture/WESEN_ADAPTIVE_BODY.md)
- [Neural Symbiosis](02-architecture/NEURAL_SYMBIOSIS.md)
- [MSBA](02-architecture/MSBA.md)
- [Profile & Identity](02-architecture/PROFILE_IDENTITY.md)
- [Real-body Embodiment](02-architecture/EMBODIMENT_REAL_BODY.md)
- [Connectome-informed Embodiment](02-architecture/CONNECTOME_EMBODIMENT.md)
- [Storage / B5D Format](02-architecture/B5D_FORMAT.md)

### Roadmap

- [Development Roadmap](08-roadmap/ROADMAP.md)
- [Scientific Maturity Roadmap](08-roadmap/SCIENTIFIC_MATURITY_ROADMAP.md)
- [Research Roadmap](08-roadmap/RESEARCH_ROADMAP.md)
- [TODO](08-roadmap/TODO.md)
- [v0.6 Acceptance](08-roadmap/V06_ACCEPTANCE.md)

### Research

- [Research canonical index](../research/README.md)
- [Current Scientific State](../research/CURRENT_SCIENTIFIC_STATE.md)
- [Integrity & Attribution](../research/INTEGRITY_AND_ATTRIBUTION.md)
- [Related Work](../research/RELATED_WORK.md)
- [Research Registry](../research/registry/)
- [Research Schemas](../research/schemas/)
- [Experiments](../research/experiments/)

## Wissenschaftliche Grenzen

- Engineering-Reife und Scientific Maturity sind getrennte Achsen.
- Der 5D-Adressraum ist keine bewiesene Überlegenheitsbehauptung.
- Gateway-/Pipeline-Erreichbarkeit ist kein erlerntes Tool Use.
- technische Identität/Behavior Profile ist kein psychologisches Selbst.
- Stage 6 besitzt Mechanismen und Kandidaten, aber noch keine abgeschlossene Semantization, kein etabliertes hierarchisches Predictive Coding und kein vollständig validiertes generatives Weltmodell.
- Stage 10 erzeugt keinen Bewusstseinsclaim.
- AI-generierte oder unbestätigte Quellen dürfen nicht als Autorität behandelt werden.

## Historische Dokumente

Historische Dokumente bleiben absichtlich im Repository, wenn sie für Provenienz, Digests, alte Links oder Reproduzierbarkeit benötigt werden. Ihr Vorhandensein bedeutet **nicht**, dass ihr Inhalt aktuell ist. Der Governance-Audit weist ihnen eine entsprechende Statusklasse zu.

Insbesondere gelten alte feste Testzahlen, frühere Branch-/Commitangaben, Alpha-/Sprint-Snapshots und ältere Publikationsversionen ausschließlich für ihren dokumentierten Zeitpunkt.

## Pflege

Neue Dokumente unter `docs/` oder `research/` müssen durch die Governance-Regeln klassifizierbar sein. Änderungen triggern `Publication Integrity`. Wenn eine Datei wissenschaftlich autoritativ sein soll, muss ihre Rolle explizit im Governance-/Registry-System verankert werden; bloße Platzierung in einem prominenten Ordner reicht nicht.
