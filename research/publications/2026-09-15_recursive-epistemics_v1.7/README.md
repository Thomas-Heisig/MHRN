# Recursive Epistemics / Rekursive Epistemik — Fassung 1.7

**Status:** aktuelle fortgeschriebene Arbeitsfassung (`current_wip`)  
**Datum:** 15. September 2026  
**Autor:** Thomas Heisig  
**Softwarelinie:** MHRN 0.6.0-alpha.3  
**Evidenzautorität:** Interpretation und Forschungsprogramm; keine automatische EVID-Promotion

## Direkt lesen

- **[Aktuelles Vollmanuskript 1.7](MANUSCRIPT.md)** — kanonischer Publication-Viewer-Einstieg
- [Forschungsbericht 1.7](FORSCHUNGSBERICHT.md)
- [Forschungsgetriebener Entwicklungsmodus](../../RESEARCH_DRIVEN_DEVELOPMENT.md) — verbindlicher Experiment-für-Experiment-Zyklus ab Edition 1.7
- [Safety-Forschungsprogramm: Zielgenese, Korrigierbarkeit und Post-Objective Transition](SAFETY_AUTONOMY_RESEARCH.md)
- [Worte des Autors](AUTHOR_POSITION.md)
- [Autor und Schaffensart](AUTHOR_AND_CREATION_PRACTICE.md) — kanonische Selbstauskunft zu Hintergrund, Motivation, Arbeitsweise, KI-Assistenz, Bias-Risiken und Verantwortung
- [Beitrags- und Neuheitsmatrix](CONTRIBUTION_MAP.md)
- [Scientific Stage Matrix](SCIENTIFIC_STAGE_MATRIX.md)
- [Integrität und Attribution](INTEGRITY_AND_ATTRIBUTION.md)
- [Literatur- und Quellenstatus](REFERENCES.md)
- [Work in Progress](WORK_IN_PROGRESS.md)
- [Manifest](manifest.json)

## Editionskette

**Vorgänger:** [Fassung 1.6](../2026-09-15_recursive-epistemics_v1.6/README.md)  
**Frozen empirical baseline:** [Fassung 1.5](../FROZEN_V1.5.md)  
**Stabiler Current-Pointer:** [CURRENT.md](../CURRENT.md)

Fassung 1.7 führt die laufende Arbeit vollständig weiter, ohne frühere empirische Artefakte zu überschreiben. Neue technische und wissenschaftliche Erkenntnisse, Nebenarbeiten, Kritikpunkte und offene Hypothesen werden in 1.7 integriert, solange diese Edition `current_wip` ist. Beim späteren Freeze wird für weitere Änderungen eine neue Edition eröffnet.

## Verbindlicher Forschungsmodus ab Edition 1.7

MHRN wird ab dieser Edition nicht mehr primär featuregetrieben fortgeschrieben. Der kanonische Entwicklungszyklus beginnt mit einer expliziten Forschungsfrage und endet erst mit einer wissenschaftlichen Antwort oder einer dokumentierten weiterhin offenen Frage.

> **MHRN wird als wissenschaftsgetriebenes System entwickelt. Neue Mechanismen, Module und Fähigkeiten werden grundsätzlich aus expliziten Forschungsfragen, experimentellen Befunden, methodischen Erfordernissen oder nachgewiesenen technischen Grenzen abgeleitet. Die Softwarearchitektur wächst damit aus dem Forschungsprozess; sie ist nicht dessen nachträgliche Rechtfertigung.**

> **Ein negatives Experiment gilt nicht als Entwicklungsfehler. Es begrenzt den Hypothesenraum und kann unmittelbar die nächste Architekturentscheidung bestimmen.**

Der verbindliche Zyklus lautet:

`RQ → Hypothesen → benötigte Fähigkeit → minimale Implementierung → technische Validierung → Präregistrierung/Freeze → autorisierte Ausführung → DATA → präregistrierte Analyse → Human Review → EVID → RQ-Antwort → Publikationsupdate → Folgefrage`

Dabei bleiben RQ-Status, Hypothesenstatus, DATA, EVID und Claim-Status getrennte wissenschaftliche Ebenen. Ein Runner darf seine eigenen DATA niemals automatisch zu Evidenz erklären.

Stages bleiben als Orientierungsrahmen erhalten, gelten wissenschaftlich aber nicht aufgrund vorhandener Features oder eines Prozentwertes als abgeschlossen. Maßgeblich werden schrittweise definierte **Exit-RQs und Evidenzanforderungen**.

Die vollständige Arbeitsregel ist in [`research/RESEARCH_DRIVEN_DEVELOPMENT.md`](../../RESEARCH_DRIVEN_DEVELOPMENT.md) kanonisch festgehalten.

## Was 1.7 gegenüber 1.6 ergänzt

- verbindlichen forschungsgetriebenen Experiment-für-Experiment-Zyklus statt nachträglicher Feature-Begründung;
- getrennte wissenschaftliche Statusräume für RQ, Hypothese, DATA, EVID und Claim;
- Stage-Abschluss über Exit-RQs und Evidenzanforderungen statt Feature-Prozentwerte;
- repositoryweite Dokumentgovernance für jede Datei unter `docs/` und `research/`;
- stabile Current-/Frozen-Einstiege für Publikationen;
- direkte Viewer-Bindung an das aktuelle `MANUSCRIPT.md` statt an eine reine Indexseite;
- ausführlich integrierte Stage-0–10-Darstellung;
- Autorposition zu kumulativer Wissenschaft, freiem Wissenstransfer und Attribution;
- kanonische Selbstauskunft `AUTHOR_AND_CREATION_PRACTICE.md` zu beruflichem Hintergrund, Motivation, assistierter Einzelautorschaft, KI-Nutzung, Verantwortung und methodischen Bias-Risiken;
- explizite Neuheitsunsicherheit für potenzielle MHRN-Beiträge;
- klare Trennung von Quellenübernahme, Synthese, Eigenentwicklung und ungeklärter Prior Art;
- fortgeschriebene Stage-6-Grenzen für Semantization, Predictive Coding und World Models;
- Governance-Audit, der alle Dateien in `docs/` und `research/` klassifiziert;
- eigenständiges Safety-Forschungsprogramm für Zielprovenienz, Goal Misgeneralization, Corrigibility, Interruptibility, Specification Gaming, instrumentelle Optionsraumpräferenz, Zielvorschläge, Post-Objective Transition und Autorisierungskonflikte;
- Registrierung von `RQ-SAFE-001` bis `RQ-SAFE-009` und `H-SAFE-001-A` bis `H-SAFE-009-A` als offene/untested Forschungsobjekte;
- Safety-Experiment-Backlog mit `EXP-SAFE-*`-Familien, die bis zu eigener Preregistrierung, Runner-Bindung und Ausführungsfreigabe ausdrücklich `planned` bleiben;
- vorbereitende Migration zur neuen Gesamtgliederung ab Edition 2.0, ohne die 1.x-Editionsgeschichte nachträglich umzuschreiben.

## Safety als Querschnittsforschung

Safety wird ab 1.7 nicht ausschließlich als später Ethik-Anhang behandelt. Das Programm verbindet drei Ebenen:

1. **empirisch-technisch:** messbare Safety-RQs, Hypothesen, Kontrollen und Failure Criteria;
2. **Engineering/Governance:** Sandbox, Berechtigungsgrenzen, unabhängiger Stopppfad, Provenienz und Freigabegates;
3. **philosophisch-ethisch:** Verantwortung, Zielgenese, Korrigierbarkeit, Post-Objective Transition und mögliche Konflikte mit AI-Welfare-Vorsorge.

Der Ausgangspunkt bleibt konservativ: MHRN besitzt damit nicht plötzlich autonome Ziele oder Selbsterhaltung. Die neuen Einträge definieren Fragen, die **vor** einer späteren stärkeren Autonomie untersucht werden müssen.

## Übergang zu Edition 2.0

Die 1.7-Struktur bleibt für die laufende 1.x-Linie bestehen. Die neue Gesamtgliederung wird erst ab Version 2.0 kanonisch. Die schrittweise Migration ist in [`docs/08-roadmap/V2_PUBLICATION_STRUCTURE_MIGRATION.md`](../../../docs/08-roadmap/V2_PUBLICATION_STRUCTURE_MIGRATION.md) definiert.

Bis dahin werden neue Inhalte so klassifiziert, dass sie später entlang der folgenden Koordinaten überführt werden können:

`Aussage = Achse × Thema × Entwicklungsphase × Provenienz × Evidenzstatus`

Die drei gleichrangigen Forschungsachsen sind:

- empirisch-technisch,
- epistemologisch-methodisch,
- philosophisch-ethisch.

Sie sind strukturell gleichrangig, verwenden jedoch unterschiedliche, jeweils explizit zu deklarierende Evidenzregeln.

## Wissenschaftliche Grenze

Die Bezeichnung `current_wip` bedeutet **nicht**, dass alle Inhalte peer reviewed, extern repliziert oder als EVID akzeptiert sind. Der Viewer zeigt absichtlich den neuesten Arbeitsstand. Für zitierfähige historische Reproduzierbarkeit stehen frozen/snapshot Editions separat bereit.

Die neue 2.0-Gliederung, die neuen Safety-Fragen und ihre geplanten Experimente verändern für sich keinen Stage-Score und keine Evidenzautorität. Struktur und Forschungsplanung sind Voraussetzungen wissenschaftlicher Arbeit, aber keine empirischen Befunde.
