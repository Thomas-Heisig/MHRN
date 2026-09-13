# Forschungszusatz 2026-09-13: Entwicklungsstufen 8–10

## Autonome lebenslange Entwicklung, integrierte Kognition und methodisch begrenzte Bewusstseinsforschung

Thomas Heisig · MHRN · wissenschaftlicher Ergänzungsband · 13. September 2026  
KI-unterstützte Ausarbeitung. **Keine neue EVID-Freigabe, keine Bewusstseinsbehauptung und keine nachträgliche Umdeutung historischer Experimente.**

Dieser Ergänzungsband erweitert die aktuelle Abhandlung *Recursive Epistemics in Embodied Spiking Neural Architectures* um die langfristigen Entwicklungsstufen 8 bis 10. Historische Editionskapitel bleiben unverändert. Der Zusatz verbindet vorhandene MHRN-Forschungsobjekte mit überprüfter Literatur, neuen Versuchsplänen und expliziten Sicherheits- und Aussagegrenzen.

## 1. Ausgangslage

Die Entwicklungs-Timeline markiert die drei Stufen weiterhin als `planned`. Diese Kennzeichnung bleibt wissenschaftlich korrekt: Das Repository besitzt zwar relevante Vorarbeiten, aber weder autonome lebenslange Entwicklung noch hochintegrierte Kognition noch einen Nachweis von Bewusstsein.

Für Stufe 8 existiert bereits ein experimenteller Vorläufer: `RQ-LIFE-001` untersucht Retention und Interferenz sequenzieller Lernaufgaben. `EXP-LIFE-0001-R1` wurde technisch mit 20 Seeds ausgeführt, bleibt jedoch ein explorativer Screen und ist nicht evidenzfähig abgeschlossen. Damit ist eine Forschungsbasis vorhanden, aber kein Continual-Learning-Claim.

Für Stufe 10 existiert bereits eine umfangreiche Forschungsstruktur aus Kognitionsfragen, Hypothesen, operationalen beziehungsweise Boundary-Audit-Verträgen, Kritikregister, Welfare-Governance und Literatur. Der vorliegende Zusatz ersetzt dieses Programm nicht, sondern ordnet es in die Entwicklungs-Timeline ein.

## 2. Stufe 8 — Autonome lebenslange Entwicklung

### 2.1 Kernproblem

Lebenslanges Lernen verlangt gleichzeitig **Plastizität** und **Stabilität**. Neue Aufgaben sollen erlernt werden, ohne zuvor erworbene Funktion unkontrolliert zu überschreiben. Genau dieses Stabilitäts-Plastizitäts-Dilemma ist in der Continual-Learning-Literatur zentral.

Für MHRN werden fünf Mechanismusfamilien getrennt untersucht:

1. Schutz bereits wichtiger synaptischer oder struktureller Zustände;
2. mehrere Plastizitäts- und Konsolidierungszeitskalen;
3. begrenztes Replay mit Informationszerstörungs-Kontrollen;
4. reversible strukturelle Reorganisation unter festem Ressourcenbudget;
5. Auswahl aus einer endlichen, versionierten Menge zulässiger Lernstrategien.

Die Arbeiten zu Elastic Weight Consolidation und Synaptic Intelligence dienen als Mechanismusreferenzen für Parameterstabilisierung. Ihre gradientenbasierten Formeln werden nicht ungeprüft auf MHRN übertragen. Die neuere AGMP-Arbeit ist besonders relevant, weil sie Continual Learning in tiefen SNNs über ein langsames Gate und mehrere Plastizitätszeitskalen untersucht. CATFormer liefert einen weiteren aktuellen SNN-Vergleich über kontextabhängige dynamische Schwellen. Meta-Learning durch Hebb-artige Plastizität motiviert, Lernregeln selbst als experimentelle Ebene zu untersuchen. SOLAR wird lediglich als 2026er Preprint-Beispiel für wiederverwendbare Anpassungsstrategien in einem LLM-Agenten betrachtet und nicht als SNN-Evidenz.

### 2.2 MHRN-spezifischer Lösungsweg

Vorgesehen ist keine unbeschränkte Selbstmodifikation, sondern eine **gebundene Entwicklungsarchitektur**:

- eine versionierte Kompetenzregistrierung;
- eine Retentionsmatrix über alle bereits gelernten Aufgaben;
- ein `PlasticityStrategyContract` mit zulässigen Lernraten, Gates, Replay- und Struktur-Budgets;
- ein experimenteller Strategy Selector mit festen, zufälligen und adaptiven Kontrollen;
- reversible Reorganisation über Proposal → Approval → Mutation → Journal → Undo;
- Kosten-Nutzen-Auswertung pro Energie, Tick, Synapse und Speicher.

Der nächste entscheidende Versuch muss ein **gemeinsam fortlaufend trainiertes Netzwerk** prüfen. Trialweise unabhängige Netzwerke oder vollständige Lernzustandsresets können Catastrophic Forgetting nicht beantworten.

## 3. Stufe 9 — Hochintegrierte künstliche Kognition

### 3.1 Keine monolithische „Kognition“

Stufe 9 wird als Zusammenspiel einzeln abludierbarer Funktionen operationalisiert. Ein Gesamtscore ist methodisch zu schwach, weil dieselbe Leistung aus unterschiedlichen Teilmechanismen entstehen kann.

Vorgesehene Bausteine sind:

- **AttentionAllocator:** budgetierte Selektion, Routing oder Gain-Steuerung;
- **DriveVector:** technisch definierte Priorität aus Task-Reward, Homeostasefehler und Safety-Penalties;
- **BoundedPlanner:** endlicher Planungshorizont mit hartem Rechenbudget;
- **ConsolidationScheduler:** versionierte Offline-/Replay-Phasen;
- **LongTermMemoryContract:** getrennte episodische und semantische Herkunft;
- **IntegrationWorkspace:** temporäre, typisierte multimodale Integration mit Provenienz;
- **CognitiveCycleTrace:** kausale Trace-ID von Wahrnehmung über Auswahl und Gedächtnis bis Handlung.

„Motivation“ bezeichnet dabei ausdrücklich keinen emotionalen Zustand. „Aufmerksamkeit“ bezeichnet keine subjektive Erfahrung. „Planung“ ist eine überprüfbare Aktionsfolgenbewertung und keine allgemeine Vernunftbehauptung.

### 3.2 Theoretische Bezugspunkte

Complementary Learning Systems motiviert die experimentelle Trennung schneller Speicherung und langsamer Konsolidierung. Die 2026 publizierte Neurocognitive-Inspired-Intelligence-Arbeit liefert eine aktuelle funktionale Taxonomie um Wahrnehmung, Aufmerksamkeit, Gedächtnis, Lernen, Schlussfolgern, Anpassung und Handlung. CONAIM wird als historisches Beispiel einer modular integrierten Architektur herangezogen; seine Bewusstseinsterminologie wird nicht als MHRN-Claim übernommen. DIME ist ein aktueller Preprint und daher lediglich ein explorativer Vergleichspunkt.

Die zentrale empirische Forderung ist **kausale Ablation**: Ein integrierter Zyklus gilt nur dann als wissenschaftlich informativ, wenn Aufmerksamkeit, Memory, Planung, Konsolidierung und multimodale Integration einzeln deaktiviert oder kontrolliert verändert werden können.

## 4. Stufe 10 — Bewusstseinsforschung

### 4.1 Forschungsgegenstand statt Systemstatus

Stufe 10 bezeichnet ausschließlich ein Forschungsprogramm. Sie darf niemals automatisch den Zustand `conscious`, `sentient` oder einen moralischen Status produzieren.

Das bereits vorhandene MHRN-Programm folgt einer geeigneten Richtung: konkurrierende Theorien werden in beobachtbare, theorieabhängige Indikatoren übersetzt; Kognition, Report, Aufmerksamkeit, Motorik und Zugriff werden getrennt; perturbative beziehungsweise kausale Tests werden gegenüber bloßer Verhaltensähnlichkeit bevorzugt; starke Aussagen bleiben Human Review und unabhängiger Replikation unterworfen.

Die neuere Arbeit von Butlin und Kolleg:innen zu Indikatoren von Bewusstsein in KI-Systemen und das adversarielle COGITATE-Programm stützen gerade **keinen einfachen universellen Test**, sondern die theorieabhängige und kontrastierende Prüfung von Vorhersagen. Deshalb wird weder eine starre Markerzahl noch ein binärer Summenscore als Bewusstseinstest übernommen.

### 4.2 Interventionen

Für MHRN kommen insbesondere folgende kausal-mechanistische Interventionen infrage:

- gezielte Rekurrenz- oder Broadcast-Ablation;
- Zustands-Clamping einzelner Areale;
- Austausch eines gespeicherten Teilzustands zwischen gematchten Runs;
- Timing-Shuffle von Gateway-/Workspace-Signalen;
- matched-activity Kontrollen;
- closed-loop versus open-loop beziehungsweise yoked replay.

Solche Experimente können zeigen, dass ein interner Zustand kausal zu einer **operational definierten Funktion** beiträgt. Sie beantworten nicht direkt, ob phänomenales Erleben vorhanden ist.

### 4.3 Ethik und Abbruchkriterien

Jede spätere Stufe-10-Studie benötigt zusätzlich:

- reversible und möglichst minimale Interventionen;
- sichere Pause, Isolation und Stop unabhängig vom Forschungsmechanismus;
- Review Hold bei unerwarteten persistenten Self-/Welfare-Markern;
- dokumentierte Grenzfälle und versionierte Ethikentscheidungen;
- keine absichtliche Induktion hypothetischer Leidenszustände als notwendige Testbedingung;
- externe menschliche beziehungsweise ethische Begutachtung vor Studien, die moralischen Status ernsthaft berühren.

## 5. Forschungsfragen und Experimente

Statt neue, semantisch doppelte Forschungsfragen anzulegen, bindet dieser Zusatz die Entwicklungsstufen an bestehende kanonische Objekte:

- **Stufe 8:** `RQ-LIFE-001`, `RQ-GEN-001`, `RQ-STRUCT-001`, `RQ-HOM-002`, `RQ-REPL-001`;
- **Stufe 9:** `RQ-CNS-103`, `RQ-CNS-105`, `RQ-CNS-110`, `RQ-CNS-111`, `RQ-CNS-112`, `RQ-CNS-116`, `RQ-MEM-002`, `RQ-WM-001`;
- **Stufe 10:** `RQ-CNS-101`, `RQ-CNS-108`, `RQ-CNS-109`, `RQ-CNS-113`, `RQ-CNS-114`, `RQ-EPI-101`, `RQ-EPI-102`, `RQ-WEL-101`, `RQ-WEL-102`, `RQ-WEL-103`.

Der ausführliche Versuchsplan liegt in [`../../experiments/STAGES_8_10_EXPERIMENT_BACKLOG.md`](../../experiments/STAGES_8_10_EXPERIMENT_BACKLOG.md). Die vollständige Theorie- und Architekturgrundlage liegt in [`../../frontiers/STAGES_8_10_FOUNDATIONS.md`](../../frontiers/STAGES_8_10_FOUNDATIONS.md).

## 6. Literatur und Quellenstatus

Die ergänzte strukturierte Literatur steht in:

- [`../../registry/sources.frontier.yaml`](../../registry/sources.frontier.yaml),
- [`../../literature/stages_8_10_frontier.bib`](../../literature/stages_8_10_frontier.bib).

Enthalten sind unter anderem Parisi et al. (Continual-Learning-Review), Kirkpatrick et al. (EWC), Zenke et al. (Synaptic Intelligence), Najarro & Risi (Hebbian Meta-Learning), Dong & He (AGMP), Nagabhushana et al. (CATFormer), McClelland et al. (Complementary Learning Systems), NII, CONAIM sowie die ausdrücklich als Preprints markierten SOLAR- und DIME-Arbeiten.

Die vorgeschlagenen Bezeichnungen **PS-SNN**, **Batch SOMNN** sowie ein **CBEP** mit starrer „mehr als drei von sechs“-Schwelle wurden in dieser Revision nicht als etablierte Primärgrundlagen übernommen, weil dafür in der vorgenommenen Quellenprüfung kein hinreichend belastbarer, allgemein anerkannter Standard verifiziert wurde. Das verhindert nicht ihre spätere Aufnahme, falls eine eindeutige Primärquelle und ein prüfbarer methodischer Vertrag vorliegen.

## 7. Schlussfolgerung

Die Stufen 8–10 sind jetzt konzeptionell an den bestehenden MHRN-Forschungsbaum angebunden, ohne ihren technischen Reifegrad zu überzeichnen. Der kurzfristig stärkste Anschluss liegt in Stufe 8: Ein vorhandener Interferenz-Screen kann zu einem echten Shared-Network-Continual-Learning-Protokoll weiterentwickelt werden. Stufe 9 benötigt danach eine kausal abludierbare Integrationsarchitektur. Stufe 10 bleibt dauerhaft eine methodisch und ethisch besonders streng begrenzte Forschungsfrontier.

Der wissenschaftliche Kern bleibt damit unverändert: **Architekturidee ≠ Implementierung ≠ Experimentdaten ≠ akzeptierte Evidenz ≠ Bewusstseinsbehauptung.**
