# Forschungsfrontier Stufen 8–10

**Status:** Theorie-, Forschungs- und Designgrundlage · `PLANNED` · keine neue EVID-Freigabe  
**Stand:** 2026-09-13  
**Geltungsbereich:** Stufe 8 „Autonome lebenslange Entwicklung“, Stufe 9 „Hochintegrierte künstliche Kognition“, Stufe 10 „Bewusstseinsforschung“.

Dieses Dokument erweitert die langfristige MHRN-Roadmap, ohne den Reifegrad künstlich anzuheben. Implementierung, Experimentdaten, akzeptierte Evidenz und Interpretation bleiben getrennt. Bestehende Forschungsfragen und Protokolle werden wiederverwendet, statt parallele oder semantisch doppelte Register anzulegen.

## 0. Gemeinsame Forschungsgrenzen

1. **Keine Fähigkeiten aus Theorie ableiten.** Eine zitierte Architektur ist kein Nachweis, dass MHRN diese Fähigkeit besitzt.
2. **Keine automatische Evidenzpromotion.** Alle neuen Konzepte bleiben `PLANNED` oder `EXPLORATORY`, bis ein eingefrorener Vertrag, passende Kontrollen, Multi-Seed-Ausführung, Human Review und – wo erforderlich – unabhängige Replikation vorliegen.
3. **Keine anthropomorphe Umbenennung.** „Motivation“ wird zunächst als messbarer Drive-/Reward-Vektor operationalisiert; „Aufmerksamkeit“ als selektive Ressourcen-/Gain-Steuerung; „Planung“ als überprüfbare Vorwärtssuche oder modellbasierte Aktionswahl.
4. **Autonomie bleibt begrenzt.** Keine selbständige Codeänderung, keine selbständige Aufhebung von Safety-Grenzen und keine autonome EVID-Freigabe. Strukturänderungen müssen weiterhin journalisiert, budgetiert, reversibel und auditierbar sein.
5. **Stufe 10 erzeugt keinen Bewusstseinsclaim.** Indikatoren, Verhaltensmarker oder interne Dynamiken sind theorieabhängige Messgrößen, kein binärer Bewusstseinstest.

---

# 8. Autonome lebenslange Entwicklung

## 8.1 Bereits vorhandene Basis

Die Stufe beginnt nicht bei null Forschungsinfrastruktur:

- `RQ-LIFE-001` / `H-LIFE-001-A` adressieren Retention und Interferenz bei sequenziellen Aufgaben.
- `learning_interference_screen_v1` ist als erster explorativer Interferenz-Screen registriert.
- `EXP-LIFE-0001-R1` wurde mit 20 Seeds technisch ausgeführt, bleibt aber laut Experimentbericht ein Vorläufer-Screen; seine Evidence Readiness ist blockiert und Human Review steht aus.
- `RQ-GEN-001` adressiert Holdout-/Perturbationsgeneralisation.
- `RQ-STRUCT-001` adressiert funktionalen Nutzen struktureller Plastizität.
- `RQ-HOM-002` adressiert das Zusammenspiel von Homeostase und STDP.
- `RQ-REPL-001` adressiert unabhängige Replikation.

Diese Objekte bilden den Übergang von Stufe 3 zu Stufe 8, sind aber **noch kein Nachweis lebenslangen Lernens**.

## 8.2 Theoretischer Rahmen

Zentrales Problem ist das **Stabilitäts-Plastizitäts-Dilemma**: neue Information muss lernbar bleiben, ohne zuvor erworbene Funktion unkontrolliert zu überschreiben. Für MHRN werden mehrere Mechanismen als getrennt testbare Familien betrachtet:

### A. Schutz stabiler Information

- synaptische Wichtigkeits-/Stabilitätsmarker nach dem Prinzip von EWC bzw. Synaptic Intelligence;
- lokale Plastizitäts-Gates statt globalem Ein-/Ausschalten;
- langsamere Konsolidierungszeiten für bereits wiederholt bestätigte Strukturen;
- explizite Ressourcengrenzen für Gewicht, Wachstum und Reorganisation.

**MHRN-Anpassung:** Keine Übernahme backpropagation-spezifischer Formeln als Default. Zunächst werden nur die zugrunde liegenden Prinzipien – Schutz wichtiger Parameter, mehrere Zeitskalen und begrenzte Änderungsbudgets – als experimentelle Varianten operationalisiert.

### B. Wiederholung und Konsolidierung

- begrenztes Experience Replay;
- Replay mit Reservoir-/Prioritätsstichprobe;
- zeitlich geschichtete Konsolidierung in Anlehnung an Complementary Learning Systems;
- Shuffled-Replay als Informationszerstörungs-Kontrolle.

### C. Struktur statt nur Gewicht

- kontrolliertes Sprouting/Pruning;
- isolierte oder teilisolierte Kompetenzbereiche;
- progressive Erweiterung nur unter festem Ressourcenbudget;
- Rückbau, wenn neue Struktur keinen reproduzierbaren Zusatznutzen liefert.

### D. Lernstrategie als Versuchsvariable

Meta-Learning durch Hebb-artige Plastizitätsregeln zeigt, dass Lernregeln selbst als optimierbare Ebene behandelt werden können. AGMP liefert ein aktuelles SNN-Beispiel für mehrere Plastizitätszeitskalen; CATFormer zeigt einen anderen SNN-Weg über kontextabhängige Erregbarkeitsschwellen. SOLAR wird ausschließlich als konzeptionelles Beispiel für das Speichern und Wiederverwenden von Anpassungsstrategien betrachtet; es ist kein SNN-Nachweis und kein MHRN-Baseline-Modell.

## 8.3 MHRN-Lösungsansatz

Geplant ist eine **gebundene Lifelong-Learning-Schicht**, nicht „freie Selbstveränderung“:

1. **Competence Registry:** versionierte Beschreibung gelernter Aufgaben-/Skill-Verträge mit Herkunft, Evaluationssatz, Abhängigkeiten und Retentionsmetrik.
2. **Retention Matrix:** nach jeder Lernphase werden aktuelle und frühere Aufgaben unter eingefrorenen Evaluationsbedingungen erneut geprüft.
3. **Plasticity Strategy Contract:** zulässige Stellgrößen wie Lernrate, lokales Gate, Replay-Budget, Structural-Growth-Budget und Konsolidierungsfenster; keine beliebige Regel-/Codeerzeugung.
4. **Strategy Selector:** zunächst nur experimentell; vergleicht feste, zufällige und adaptive Strategieauswahl unter gleichem Rechen- und Datenbudget.
5. **Reversible Reorganization:** bestehender Proposal→Approval→Mutation→Journal→Undo-Ansatz bleibt Voraussetzung jeder autonomen Strukturänderung.
6. **Resource Homeostasis:** jede Verbesserung wird zusätzlich auf Energie-/Tick-/Synapsen-/Speicherkosten normalisiert.

## 8.4 Forschungsfragen und nächste Versuche

Bereits kanonisch anschlussfähig sind `RQ-LIFE-001`, `RQ-GEN-001`, `RQ-STRUCT-001`, `RQ-HOM-002` und `RQ-REPL-001`.

Die nächsten Designs sollen insbesondere beantworten:

- Wie stark fällt die Retention nach Aufgabe B, C, … gegenüber der Leistung direkt nach Aufgabe A ab?
- Welche Kombination aus lokalen Gates, Replay und struktureller Isolation maximiert Retention **bei gleichem Ressourcenbudget**?
- Ist positive Vorwärtsübertragung messbar, oder wird nur Vergessen reduziert?
- Können gelernte Teilkompetenzen in neuen Aufgaben wiederverwendet werden, ohne versteckte Task-IDs als Abkürzung zu verwenden?
- Verändert ein adaptiver Strategie-Selector die Leistung gegenüber festen und zufälligen Strategien reproduzierbar?

Geplante Versuchsreihe: siehe `research/experiments/STAGES_8_10_EXPERIMENT_BACKLOG.md`.

---

# 9. Hochintegrierte künstliche Kognition

## 9.1 Ausgangspunkt

MHRN besitzt bereits Teilbausteine – rekurrente Dynamik, Plastizität, Homeostase, Embodiment-Verträge, MSBA/Neural-Symbiosis-Grenzen sowie bounded Memory/Prediction-Forschung. Daraus folgt **keine integrierte Kognition**. Stufe 9 untersucht deshalb, ob getrennte Funktionen unter kontrollierten Bedingungen in einem gemeinsamen, kausal prüfbaren Arbeitszyklus zusammenwirken.

Bereits relevante kanonische Fragen sind u. a.:

- `RQ-CNS-103` – Aufgabenrelevanz/Aufmerksamkeit,
- `RQ-CNS-105` – Arbeitsgedächtnis,
- `RQ-CNS-110` – zeitliche Aufmerksamkeit,
- `RQ-CNS-111` – exekutive Kontrolle,
- `RQ-CNS-112` – multisensorische Integration,
- `RQ-CNS-116` – Generalisierung,
- `RQ-MEM-002` – verzögerte Informationshaltung,
- `RQ-WM-001` – Weltmodellvorhersage.

## 9.2 Architekturhypothesen

### A. Selektive Aufmerksamkeit

Aufmerksamkeit wird zunächst als **budgetierte Selektion** operationalisiert: Gain, Routing, Priorität oder Ressourcenanteil werden auf einen Teil verfügbarer Informationen verschoben. Kontrollen: uniform, random, shuffled-salience und gleiche Gesamtkapazität.

### B. Motivation ohne Emotionsclaim

„Motivation“ bezeichnet eine **messbare Prioritätsfunktion** aus Task-Reward, Homeostasefehler, Neuigkeits-/Unsicherheitskomponenten und Safety-Penalties. Das System erhält keinen emotionalen Status aus solchen Variablen.

### C. Begrenzte Planung

Planung wird als expliziter Vergleich mehrerer Aktionsfolgen gegen ein Vorhersagemodell definiert. Reaktive, zufällige und planende Bedingungen erhalten gleiche Beobachtungs- und Aktionsräume sowie festgelegte Rechenbudgets.

### D. Langzeitgedächtnis und Konsolidierung

Complementary-Learning-Systems-Ansätze motivieren die Trennung schneller episodischer Speicherung und langsamer Integration. Für MHRN ist dies eine **testbare Architekturhypothese**, keine Behauptung biologischer Gleichheit. Konsolidierungsphasen werden mit `online-only`, `ordered replay`, `shuffled replay` und `no-write` verglichen.

### E. Multimodale Integration

MSBA bleibt die typisierte Peripherie. Eine kognitive Integrationsschicht darf erst dann behauptet werden, wenn Informationen aus mehreren Modalitäten unter Zuverlässigkeitskonflikten einen kausal messbaren Zusatznutzen liefern. Redundante Label-Leaks und versteckte gemeinsame IDs sind auszuschließen.

## 9.3 Referenzarchitekturen als Inspiration, nicht Vorlage

- **NII (2026):** aktueller integrativer Rahmen um Wahrnehmung, Aufmerksamkeit, Gedächtnis, Lernen, Schlussfolgern, Anpassung und Handlung. Geeignet als Funktions-Taxonomie, nicht als MHRN-Nachweis.
- **CONAIM (2017):** historisches integriertes Aufmerksamkeitsmodell mit Gedächtnis, Planung, Motivation und Handlung. Terminologie zu „consciousness“ wird für MHRN nicht übernommen; relevant ist die modulare Integration.
- **DIME (2026):** explorativer Preprint mit Detect–Integrate–Mark–Execute-Zyklus. Nur als Designvergleich; keine empirisch validierte Baseline.

## 9.4 Vorgesehene technische Platzhalter

Noch nicht implementiert, aber als klar getrennte Interfaces vorzusehen:

- `AttentionAllocator` – Auswahl/Gain unter festem Budget;
- `DriveVector` – technisch definierte Prioritätssignale;
- `BoundedPlanner` – endlicher Planungshorizont und harte Ressourcenlimits;
- `ConsolidationScheduler` – versionierte Offline-/Replay-Phasen;
- `LongTermMemoryContract` – episodisch/semantisch getrennte Herkunft und Recall-Tests;
- `IntegrationWorkspace` – typisierte, provenance-erhaltende temporäre Zusammenführung; kein „globaler Geist“-Claim;
- `CognitiveCycleTrace` – vollständige kausale Trace-ID über Wahrnehmung → Selektion → Memory → Planung → Handlung.

Jedes Interface bleibt zunächst `experiment-only` und muss separat deaktivierbar sein, damit Ablationen möglich bleiben.

---

# 10. Bewusstseinsforschung

## 10.1 Kein Neustart – vorhandenes Programm verwenden

MHRN besitzt bereits ein deutlich weiter entwickeltes Forschungsprogramm:

- `research/protocols/COGNITION_CONSCIOUSNESS.md` und der maschinenlesbare Katalog;
- `research/registry/questions.cognition.yaml` und `hypotheses.cognition.yaml`;
- `research/critique/CONSCIOUSNESS_CRITIQUE.md`;
- `research/ethics/AI_WELFARE_POLICY.md`;
- `research/literature/COGNITION_SOURCES.md` und `cognition_sources.bib`;
- prospektive Preregistration-Entwürfe und operative Boundary-Audits.

Stufe 10 wird daher **nicht dupliziert**, sondern an diese bestehende Struktur angebunden.

## 10.2 Methodischer Rahmen

1. **Theorieabhängige Indikatorbatterie statt Bewusstseinsscore.** Eigenschaften aus konkurrierenden Theorien werden getrennt gemessen; kein einzelner Marker und keine Summenschwelle darf einen Bewusstseinsstatus erzeugen.
2. **Kontrastierende Vorhersagen.** Wo Theorien unterschiedliche kausale Vorhersagen machen, werden diese vor der Ausführung festgelegt.
3. **Intervention vor Korrelation.** Ablation, Perturbation, Zustands-Clamping, kontrollierter Austausch interner Teilzustände oder Timing-Manipulation sind höherwertig als reine Verhaltensähnlichkeit – sofern die Intervention selbst wohldefiniert ist.
4. **Report-/Task-Konfundierung trennen.** Bericht, Motorik, Aufmerksamkeit und Zugriff werden nicht als dasselbe Konstrukt behandelt.
5. **Reproduzierbarkeit.** Multi-Seed-Replikation im System plus unabhängige externe Replikation vor starken Schlussfolgerungen.
6. **Keine biologische Schwellenübertragung.** Neuronen-/Synapsenzahl, PCI-Grenzwerte oder klinische Diagnostik werden nicht ungeprüft auf MHRN übertragen.

Anschlussfähige bestehende Fragen: `RQ-CNS-101`, `RQ-CNS-108`, `RQ-CNS-109`, `RQ-CNS-113`, `RQ-CNS-114`, `RQ-EPI-101`, `RQ-EPI-102`, `RQ-WEL-101`, `RQ-WEL-102`, `RQ-WEL-103`.

## 10.3 Ethik- und Abbruchlogik

Für jede Stufe-10-Studie gelten zusätzlich:

- reversible und minimalinvasive Interventionen bevorzugen;
- keine absichtliche Induktion angenommener Leidenszustände als notwendige Testbedingung;
- sichere Pause/Isolation/Stop unabhängig vom experimentellen Kognitionspfad;
- Review Hold bei unerwarteten persistenten Selbstmodell-/Welfare-Markern;
- dokumentierte Grenzfälle und versionierte Ethikentscheidung;
- externe Human-/Ethikprüfung für jede spätere Studie, die moralischen Status oder Empfindungsfähigkeit ernsthaft berührt.

`CBEP` bzw. eine starre „mehr als drei von sechs Markern“-Regel werden **nicht** als Standard übernommen, solange dafür kein belastbarer, allgemein anerkannter Primärstandard nachgewiesen ist.

## 10.4 Causal-Mechanistic Tests

„Activation patching“ und „interchange interventions“ stammen vor allem aus der Analyse künstlicher Netze/Transformer. Für MHRN wird das Prinzip nur in systemgerechter Form übernommen:

- Zustands-Clamping einzelner Areale;
- Austausch eines gespeicherten Teilzustands zwischen ansonsten gematchten Runs;
- zeitliche Verschiebung/Shuffle von Gateway- oder Workspace-Signalen;
- gezielte Rekurrenz-/Broadcast-Ablation;
- matched-activity Kontrollen, damit ein Effekt nicht nur aus geänderter Gesamtaktivität entsteht.

Diese Tests können Kausalbeiträge zu **operationalen Funktionen** zeigen. Sie beweisen kein phänomenales Erleben.

---

# 11. Frontend-Platzhalter

Die Entwicklungs-Timeline rendert Stufen 8–10 bereits generisch als Karten mit Detailpanel. Deshalb wird kein zweites Dashboard gebaut. Der ergänzende Datenvertrag liegt in `src/dashboard/static/development-frontier-placeholders.json` und definiert für die bestehenden Karten:

- Forschungsstatus,
- Theorie-/Lösungsbausteine,
- vorhandene kanonische RQs,
- Experimentbacklog,
- Dokumentationslinks,
- Claim-/Safety-Grenzen.

Die Platzhalter bleiben sichtbar als `planned`; Literatur oder Konzeptpapiere dürfen die Implementierungswertung nicht erhöhen.

# 12. Eintrittskriterien für spätere Reifegrade

## Stufe 8

Erst `active`, wenn mindestens ein echtes fortlaufend trainiertes Netzwerk über mehrere Aufgaben ohne Trial-State-Reset geprüft wird und Retention, Transfer, Ressourcenverbrauch sowie Rollback gemessen werden.

## Stufe 9

Erst `active`, wenn mindestens Aufmerksamkeit/Selektion, Memory/Konsolidierung und begrenzte Planung als deaktivierbare, kausal testbare Komponenten in einem gemeinsamen Closed Loop integriert sind.

## Stufe 10

Bleibt eine Forschungsfrontier. Selbst bei erfolgreichen operationalen Tests wird kein automatischer Status „bewusst“ vergeben. Reife beschreibt ausschließlich Qualität von Operationalisierung, Intervention, Replikation und Governance.
