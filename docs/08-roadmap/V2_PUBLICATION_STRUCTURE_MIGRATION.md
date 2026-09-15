# Migration zur Publikationsstruktur 2.0

**Status:** current planning document  
**Start:** 15. September 2026  
**Ziel:** Ab Edition 2.0 wird die neue Gesamtgliederung kanonisch. Edition 1.7 bleibt bis dahin die laufende 1.x-Arbeitsfassung und wird nicht nachträglich in eine 2.0-Struktur umbenannt.

## 1. Grundsatz

Die neue Gliederung wird **nicht als Big-Bang-Umbau** eingeführt. Neue Inhalte werden ab sofort so dokumentiert, dass sie später eindeutig in die 2.0-Struktur überführt werden können. Historische DATA, EVID, Preregistrierungen, Experimente und frozen Publikationen bleiben unverändert.

Die Migration trennt drei Dinge:

1. **Inhaltliche Weiterarbeit** — Forschung, Experimente, Architektur und Kritik laufen weiter.
2. **Semantische Klassifikation** — neue und bestehende Inhalte erhalten Zielkapitel, Forschungsachse, Thema, Entwicklungsphase und Provenienzklasse.
3. **Physische Neuordnung** — Dateien werden erst dann verschoben oder zusammengeführt, wenn Provenienz, Links, Digests und Reproduzierbarkeit dadurch nicht beschädigt werden.

## 2. Kanonische 2.0-Hauptgliederung

Ab Version 2.0 soll das Gesamtwerk folgende Hauptteile verwenden:

### Teil I — Nullpunkt, Autor und Entstehungsbedingungen

- Motivation und Ausgangsproblem
- Autorposition und Schaffensart
- Grenzen persönlicher Erfahrung als Evidenz
- frühe Brain-5D-Phase und rekonstruierte Vorgeschichte
- KI-Assistenz und externe Kognition als Bestandteil der Arbeitsumgebung

### Teil II — Schaffensgeschichte und Architekturgenese

- Brain-5D → MHRN
- Neuron/Synapse → Rekurrenz → Plastizität → spezialisierte Pfade → Nervensystem → Gedächtnis/Weltmodell
- wichtige Architekturentscheidungen, verworfene Wege und Revisionen
- Editionen, Releases, Experimente und Claim-Genealogie

### Teil III — Forschungsobjekt MHRN

- neuronale Primitive
- rekurrente Netze
- Plastizität und Homeostase
- Modalitäten und Gateways
- Embodiment
- Gedächtnis und Weltmodell
- Language Organ / Knowledge Intake
- technische Identität, spätere Kognition und Autonomiegrenzen

### Teil IV — Empirisches Forschungsprogramm

- Forschungsfragen und Hypothesen
- Preregistrierung
- Versuchsdesigns
- Kontrollbedingungen
- Statistik und Reproduzierbarkeit
- positive, negative und Nullbefunde
- Safety-Forschungsprogramm
- unabhängige Replikation

### Teil V — Wissenschaftliche Infrastruktur und Engineering

- Determinismus
- Persistenz/Restore
- CUDA/Scaling
- Runtime und Ressourcen
- Git/CI/Gates
- Dashboard
- Publication Viewer
- Research Catalog
- experimentelle Workflow-Infrastruktur

### Teil VI — Epistemologie und Methodik der Schaffensgeschichte

- drei gleichrangige Forschungsachsen mit unterschiedlichen Evidenzregeln
- Provenienzklassen
- Creation Event Register
- AI-assisted research provenance
- retrospektive Rekonstruktion vs. zeitgenössische Artefakte
- Falsifikation von Entstehungs-/Prioritätsaussagen

### Teil VII — Integrität, Autorschaft und kumulative Wissenschaft

- Attribution
- Quellenklassen
- Prior Art
- Similarity
- kumulative Wissenschaft vs. Plagiat
- Autorschaft und KI-Unterstützung
- Human Review und externe Kritik

### Teil VIII — Philosophie, Ethik und Sicherheit

- normative Prämissen
- Verantwortung
- Kontrollierbarkeit
- Zielgenese
- Corrigibility und Interruptibility
- Post-Objective Transition Safety
- mögliche künstliche Empfindungsfähigkeit und Welfare Precaution
- Bewusstseinsforschung und Claim-Grenzen

### Teil IX — Rekursive Epistemik

- Forschungsobjekt und Forschungsprozess als getrennte, aber vergleichbare Ebenen
- Objekt-Ebene: Umwelt → Gateway → neuronales System → Lernen → Output
- Meta-Ebene: Literatur/DATA/AI/Reviewer/Autor → epistemisches Gateway → Entscheidung → Experiment → Kritik → Revision
- methodisierte strukturelle Vergleiche ohne Gleichsetzung der Ebenen

### Teil X — Synthese

Jeder Syntheseclaim muss mindestens ausweisen:

- Forschungsachse,
- Thema,
- Entwicklungsphase,
- Provenienzklasse,
- Evidenzstatus,
- Interpretationsart (`confirmatory`, `methodological`, `argumentative`),
- Revisionskriterium.

### Teil XI — Offene Forschungslandschaft

- offene Claims
- geplante Experimente
- externe Replikation
- Stage-8–10-Frontier
- Safety-Gates
- Prior-Art-Fragen
- Grenzen und Abbruchkriterien

## 3. Mehrdimensionale Zuordnung statt nur Kapitelnummer

Ab sofort soll jeder neue größere Forschungsbaustein nach Möglichkeit anhand folgender Koordinaten klassifizierbar sein:

`Aussage = Achse × Thema × Entwicklungsphase × Provenienz × Evidenzstatus`

### Achse

- empirisch-technisch
- epistemologisch-methodisch
- philosophisch-ethisch

Die drei Achsen sind gleichrangig als Forschungsachsen, verwenden aber unterschiedliche Evidenzregeln.

### Thema

Beispiele:

- neuronale Dynamik
- Plastizität
- Modalität/Gateway
- Gedächtnis
- Weltmodell
- Language Organ
- Embodiment
- Autonomie/Safety
- Bewusstseinsforschung
- Forschungsprozess

### Entwicklungsphase

Mindestens:

- rekonstruierte Vorphase / Nullpunkt
- Brain-5D
- frühe MHRN-Integration
- evidenzorientierte MHRN-Phase
- aktuelle Edition
- zukünftige Frontier

### Provenienzklasse

- **S1:** harte/primäre Artefakte — Commits, Tags, PRs, frozen Preregistrierungen, DATA, Ergebnisse, Manifeste, Hashes
- **S2:** zeitgenössische Prozessartefakte — Issues, Reviews, Chats, AI-Interaktionen, Arbeitsnotizen, Changelogs, Diffs
- **S3:** zeitgenössische Selbstauskunft — Autorennotizen, Begründungen, Journale
- **S4:** retrospektive Rekonstruktion — heutige Erinnerung oder unvollständig belegte Vor-Repo-Geschichte

Bei Widerspruch zwischen retrospektiver Erinnerung und zeitgenössischem Artefakt hat das zeitgenössische Artefakt Vorrang. Fehlende Dokumentation wird als `nicht rekonstruierbar` gekennzeichnet und nicht durch erfundene Präzision ersetzt.

### Evidenzstatus

Beispiele:

- implemented
- technically_verified
- DATA
- candidate_evidence
- accepted_EVID
- null_result
- falsified_under_protocol
- methodological_claim
- argumentative_claim
- open

## 4. Migrationsphasen

### Phase A — ab 1.7: Vorstrukturierung

- neue größere Forschungsprogramme erhalten eine eindeutige 2.0-Zielzuordnung;
- neue RQs/Hypothesen bleiben in der bestehenden Registry, erhalten aber passende Domains;
- neue Publikationsbeilagen werden über die aktuelle 1.7-README verlinkt;
- Safety wird als eigener Forschungsstrang eingebaut;
- historische Dateien werden nicht umbenannt oder verschoben;
- neue WIP-Inhalte müssen ihre Claim-Grenzen und Evidenzrolle deklarieren.

### Phase B — 1.x: Register und Genealogien

Schrittweise aufzubauen:

- `Creation Event Register`
- `Claim Ledger`
- `Experiment Genealogy`
- `Edition Genealogy`
- `Provenance Register`

Diese Register sollen zunächst additive Projektionen sein. Sie dürfen bestehende Primärartefakte nicht ersetzen.

### Phase C — spätes 1.x: 2.0-Inhaltsmatrix

Vor Eröffnung von 2.0 wird eine Matrix erstellt, die jedes relevante Dokument und jeden zentralen Claim mindestens einem zukünftigen Hauptteil zuordnet. Mehrfachzuordnung über Querverweise ist zulässig; eine Datei muss nicht physisch dupliziert werden.

### Phase D — Eröffnung 2.0

Erst dann wird die neue Hauptgliederung kanonischer Publication-Viewer-Einstieg.

2.0 muss:

- auf 1.7/letzte 1.x als Vorgänger verweisen;
- frozen 1.5 unverändert erreichbar halten;
- historische Forschungsstände nicht rückwirkend umdeuten;
- alle relevanten Haupt- und Nebenarbeiten aus der Schaffenszeit integrieren;
- den Unterschied zwischen rekonstruierter Vorgeschichte und harter Repo-Provenienz sichtbar halten.

### Phase E — nach 2.0: kontrollierte physische Bereinigung

Erst nach stabiler semantischer Zuordnung dürfen redundante aktuelle Dokumente konsolidiert oder in Archive verschoben werden. Experimente, DATA, EVID, Freeze-Manifeste und zitierte historische Pfade werden nicht ohne expliziten Migrationsvertrag verschoben.

## 5. Safety-Forschungsstrang in 2.0

Das neue Safety-Programm wird in 2.0 nicht ausschließlich im Ethikteil geführt.

Es besitzt mindestens drei Projektionen:

- **Teil IV:** empirische Safety-RQs, Hypothesen und Experimente;
- **Teil V:** technische Safety-Gates, unabhängiger Stopppfad, Sandbox und Berechtigungsarchitektur;
- **Teil VIII:** normative Verantwortung, Corrigibility, Zielgenese, Post-Objective Transition und Welfare-Konflikte.

In Teil X wird nur synthetisiert, was in den jeweiligen Achsen zuvor methodisch ausgewiesen wurde.

## 6. Keine automatische Reife durch Strukturmigration

Die Umstellung auf 2.0 verändert keinen Stage-Score, keinen Claim-Status und keine EVID-Autorität. Eine bessere Gliederung ist wissenschaftliche Infrastruktur, aber kein empirischer Befund.

## 7. Definition of Done für die 2.0-Struktur

Die neue Gliederung gilt als etabliert, wenn:

- alle elf Hauptteile als kanonische Struktur existieren;
- alle zentralen Forschungsstränge aus Brain-5D und MHRN zugeordnet sind;
- Creation/Claim/Experiment/Edition/Provenance-Genealogien vorhanden sind;
- die drei Forschungsachsen ihre jeweils expliziten Evidenzregeln besitzen;
- Safety als Querschnitt zwischen empirischer Forschung, Engineering und Ethik integriert ist;
- Publication Viewer auf 2.0 zeigt, während historische Editionen erreichbar bleiben;
- kein historisches DATA/EVID durch die Migration verändert wurde;
- Dokumentgovernance und CI die neue Struktur validieren.
