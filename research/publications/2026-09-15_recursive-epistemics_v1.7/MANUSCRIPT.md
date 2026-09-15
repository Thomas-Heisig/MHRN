# Rekursive Epistemik in verkörperten spikenden neuronalen Architekturen

## Recursive Epistemics in Embodied Spiking Neural Architectures

**Thomas Heisig · MHRN · Fassung 1.7 · fortgeschriebene Arbeitsfassung · 15. September 2026**

> **Versionshinweis.** Dies ist die aktuell fortgeschriebene `work in progress`-Fassung. Unmittelbare Vorgängerfassung ist [1.6](../2026-09-15_recursive-epistemics_v1.6/README.md). Die empirische Publikationsbasis [1.5](../FROZEN_V1.5.md) bleibt eingefroren und wird durch diese Revision nicht rückwirkend verändert.

> **Wissenschaftliche Grenze.** Diese Arbeit dokumentiert ein Forschungsframework, seine Implementierung, Experimente, negative Befunde, offene Hypothesen und Interpretationen. Sie behauptet weder AGI noch Bewusstsein/Sentienz, biologische Volläquivalenz, eine Überlegenheit des 5D-Adressraums noch einen wissenschaftlichen Durchbruch. Technische Implementierung und wissenschaftliche Evidenz werden getrennt bewertet.

---

# 1. Gegenstand und Ziel der Arbeit

MHRN — **Multi-Scale Homeostatic Recurrence Network** — ist ein Forschungs- und Engineeringframework für spikende neuronale Systeme, in dem neuronale Dynamik, Plastizität, spezialisierte sensorische/digitale Pfade, Embodiment, Gedächtnis, Vorhersage, technische Identität und spätere kognitive Forschungsfragen in einer gemeinsamen, reproduzierbaren Architektur untersucht werden sollen.

Die zentrale methodische Entscheidung dieser Fassung ist die Trennung von drei Ebenen:

1. **Mechanismus:** Was ist tatsächlich im System implementiert?
2. **Verifikation:** Welche technische Eigenschaft wurde reproduzierbar getestet?
3. **wissenschaftliche Evidenz:** Welche Forschungsfrage wurde mit geeignetem Protokoll, Kontrollen, DATA, Review und gegebenenfalls unabhängiger Replikation untersucht?

Damit wird die häufige Gleichsetzung von „Code existiert“, „Test ist grün“ und „Hypothese ist bestätigt“ ausdrücklich verworfen.

Die Arbeit verfolgt zwei miteinander verbundene Ziele. Erstens soll MHRN als technisch kontrollierbare Plattform für langfristige SNN-Forschung dienen. Zweitens soll die Dokumentation selbst so strukturiert sein, dass externe Kritik, Replikation, negative Befunde und historische Entwicklung nachvollziehbar bleiben.

---

# 2. Editions- und Provenienzvertrag

Fassung 1.7 ist keine still geänderte 1.5 und keine Überschreibung früherer Forschungsstände.

Die Editionslinie lautet:

- **1.5, 13.09.2026:** eingefrorene empirische Basis mit vollständiger damaliger Kampagnen- und Manuskriptprovenienz;
- **1.6, 15.09.2026:** integrative Revision mit separater Scientific-Maturity-Achse, Integritäts-/Attributionsregeln und verschärften Stage-6-Claim-Grenzen;
- **1.7, 15.09.2026:** fortgeschriebene Gesamtarbeitsfassung, die Haupt- und Nebenarbeiten, Governance, Neuheitsunsicherheit, Dokumentenordnung und laufende WIP-Änderungen in einem aktuellen Leserstand zusammenführt.

Historische DATA und EVID werden nicht auf den heutigen Codezustand umgedeutet. Eine ältere Messung bleibt eine Messung des damaligen Quellstands. Neue Instrumentierung rechtfertigt ein neues Experiment, nicht das Umschreiben alter Ergebnisse.

---

# 3. Wissenschaft als kumulativer Prozess

Die Arbeit folgt der Position, dass Wissenschaft grundsätzlich kumulativ ist. Kein Modell entsteht ohne übernommene Begriffe, Methoden, mathematische Werkzeuge, Softwaretechniken oder vorangegangene Beobachtungen. Daraus folgt jedoch **nicht**, dass akademische Attribution entbehrlich wäre.

MHRN unterscheidet deshalb zwei Bedeutungen, die in populären Aussagen über „Plagiat“ leicht vermischt werden:

- **epistemische Kumulativität:** Erkenntnisse bauen auf anderem Wissen auf;
- **institutionelles Plagiat:** zurechenbare fremde Texte, Daten, Code oder Ideen werden ohne angemessene Herkunftsangabe als eigene Leistung dargestellt.

Die zweite Form ist für dieses Projekt unzulässig, weil sie die Nachvollziehbarkeit der Wissensproduktion beschädigt. Freier Wissenstransfer verlangt in dieser Arbeit **mehr**, nicht weniger Provenienz.

Die vollständige Autorposition ist als [Worte des Autors](AUTHOR_POSITION.md) dokumentiert. Sie enthält auch die explizite Bereitschaft, die eigene Arbeit weiterverwenden zu lassen, sofern Herkunft, Veränderungen und Unsicherheiten nachvollziehbar bleiben.

---

# 4. Forschungsintegrität und Quellenklassen

Jede wissenschaftlich relevante Aussage soll einer Quellenklasse zugeordnet werden:

1. **MHRN observation:** direkt aus einem dokumentierten Run oder Artefakt;
2. **MHRN interpretation:** Interpretation eigener DATA, nicht identisch mit den DATA;
3. **external theory/method:** Theorie oder Methode aus externer Literatur;
4. **MHRN prior work:** eigene frühere Fassung, Experiment oder Dokument;
5. **AI-assisted wording/synthesis:** sprachliche oder synthetische Unterstützung, die keine Quellenautorität erzeugt.

Bibliografische Einträge aus automatisierter Recherche werden nicht allein aufgrund plausibler Titel akzeptiert. Unbestätigte Quellen verbleiben in **Quellenquarantäne**. Frühere Hinweise wie `ArithSpec` als angeblich normativer Standard oder `NeuroEval` als vermeintlich etablierte Community-Norm dürfen nicht als wissenschaftliche Grundlage erscheinen, solange diese Rolle nicht belastbar verifiziert ist.

Ein internes Similarity-/Attributionssystem kann Risiken reduzieren. Es kann keine „Plagiatsfreiheit“ beweisen. Vor einer formalen externen Einreichung bleiben menschliche Quellenprüfung und, abhängig von Institution/Zielorgan, externe Text- und Code-Similarity-Prüfungen notwendig.

---

# 5. Dokument- und Forschungsgovernance

Eine zentrale Schwäche des bisherigen Repositories war die Vermischung von aktuellen Dokumenten, historischen Fassungen, generierten Reports, Experimentartefakten und Forschungsnotizen. Fassung 1.7 führt deshalb eine repositoryweite Governance für `docs/**` und `research/**` ein.

Jede Datei erhält eine deklarierte Rolle mit mindestens:

- Pfad und Domäne,
- Dokumenttyp,
- Status (`current`, `current_wip`, `frozen`, `historical`, `generated`, `experimental`, `superseded`, `archive`),
- Autoritätsklasse,
- Mutabilität,
- Zitierregel,
- Evidenzrolle,
- Begründung und Klassifikationsregel.

Der Audit ist fail-closed gegenüber ungültigen Statuswerten und fehlenden Pflichtfeldern. Historische Experimente werden nicht aus ästhetischen Gründen verschoben, wenn dadurch Digests, Referenzen oder Reproduzierbarkeit gefährdet würden. Aufräumen bedeutet daher zuerst **semantische Ordnung**, dann gegebenenfalls kontrollierte physische Migration.

---

# 6. Technische Grundarchitektur

MHRN verwendet einen spikenden neuronalen Kern mit versionierten Neuron-/Synapsenmodellen, deterministischen Referenzpfaden und expliziten Persistenzgrenzen. Der Kern soll nicht durch ein Sprachmodell überschrieben werden; LLM-/AI-Komponenten bleiben Übersetzungs-, Analyse- oder Monitoringkomponenten außerhalb der kausal autoritativen SNN-Lernschleife, sofern ein Experiment nicht ausdrücklich etwas anderes definiert.

## 6.1 Vier Ordnungsbegriffe

Für Determinismus und spätere Beschleuniger wird zwischen vier Ebenen unterschieden:

- **Logical Identity** — Identität eines logischen Objekts;
- **Physical Slot** — konkrete Speicherposition;
- **Synaptic Reduction** — wohldefinierte Zusammenführung paralleler synaptischer Beiträge;
- **Execution Scheduling** — zeitliche/backendbezogene Ausführung.

Die Trennung soll verhindern, dass eine Performanceoptimierung still die wissenschaftliche Semantik ändert. Sie ist ein potenzieller methodischer MHRN-Beitrag; die externe Neuheit dieser Viererteilung ist noch nicht nachgewiesen.

## 6.2 Alternative neuronale Modelle

Izhikevich- und LIF-artige Modelle werden als austauschbare Modellvarianten behandelt. Biologisch detailliertere Modelle — etwa HH-artige Kanaldynamik, Multi-Compartment-Dendriten oder NMDA-Plateaus — sollen nicht ungeprüft als zusätzliche Felder in denselben primitiven Zustand gestapelt werden, sondern als kontrollierbare Modellvarianten/Ablationen mit eigener Integrations- und Reproduzierbarkeitsprüfung.

## 6.3 Determinismus und Beschleunigung

CPU- und GPU-Pfade müssen ihre Determinismusklasse explizit deklarieren. Floating-Point-Beschleunigung darf nicht pauschal mit Bytegleichheit verwechselt werden. Wissenschaftlich maßgeblich sind definierte Toleranzen, Reduktionsreihenfolgen, Seed-/State-Provenienz und die Frage, welche Ergebnisidentität ein Experiment tatsächlich voraussetzt.

---

# 7. Stage-Modell 0–10: zwei getrennte Fortschrittsachsen

Die Entwicklung wird in elf Stufen (0 bis 10) beschrieben. Die Zählung ist historisch so etabliert und wird aus Kompatibilitätsgründen beibehalten.

Die **Engineering-Achse** fragt nach Implementierung, Integration, technischer Verifikation und Persistenz. Die **Scientific-Maturity-Achse** gewichtet Forschungsfrage, Protokoll, DATA, reviewte EVID, unabhängige Replikation und Attribution. Der wissenschaftliche Score ist ein Governanceinstrument, **keine Kognitions-, Intelligenz- oder Bewusstseinskennzahl**.

Aktueller konservativer Scientific-Maturity-Snapshot dieser Edition:

| Stage | Gegenstand | wissenschaftliche Reife | wichtigste Grenze |
|---:|---|---:|---|
| 0 | einzelne Nervenzelle | 50 % | externe Replikation und breitere Parameter-/Modellablationen offen |
| 1 | kleine Netze / Signalweitergabe | 30 % | systematische kontrollierte Evidenzbasis noch begrenzt |
| 2 | stabiles rekurrentes SNN | 65 % | Zielskalierung und unabhängige Replikation getrennt vom Mechanismusabschluss |
| 3 | plastisches Nervengewebe | 55 % | held-out Learning-EVID und unabhängige Replikation offen |
| 4 | spezialisierte neuronale Areale | 55 % | modality-specific DATA vorhanden, wissenschaftliche Mehrleistung noch nicht breit belegt |
| 5 | integriertes künstliches Nervensystem | 55 % | Real-Device-/Closed-loop-EVID und Läsionskontrollen offen |
| 6 | Gedächtnis und Weltmodell | 40 % | keine abgeschlossene Semantization, kein hierarchisches Predictive Coding, kein vollständiges generatives Weltmodell |
| 7 | technische Identität / Selbstmodellgrundlagen | 28 % | Identitätsverwaltung ist kein kausales Selbstmodell |
| 8 | höhere Kognition | 23 % | überwiegend Forschungsprogramm |
| 9 | metakognitive / soziale Frontier | 15 % | Implementierung/Evidenz nicht ausreichend |
| 10 | Bewusstseinsforschung / Grenzfragen | 13 % | keine Bewusstseinsbehauptung; Definitions-/Messproblem zentral |

Diese Werte dürfen nur zusammen mit ihren Kriterien gelesen werden. Ein einzelner Prozentwert darf nicht als Ergebnis veröffentlicht werden.

---

# 8. Stage 0 — einzelne Nervenzelle

Die Stage-0-Forschung konzentriert sich auf deterministische Membrandynamik, Spikebildung, Refraktärverhalten, Modellparameter und Referenzvergleich. Die technische Primitive unterstützt unterschiedliche neuronale Modellpfade und Provenienz von Modellwechseln.

Die wissenschaftliche Aufgabe besteht nicht darin, zu zeigen, dass eine bekannte Differentialgleichung in Python ausgeführt werden kann. Relevant sind vielmehr:

- numerische Stabilität,
- Parametergrenzen,
- Übereinstimmung mit definierten Referenzen,
- Empfindlichkeit gegenüber Zeitschritt/Integrator,
- Reproduzierbarkeit über Umgebungen,
- Abgrenzung zwischen biologischer Inspiration und biologischer Simulation.

Offen bleiben breit angelegte Modellablationen und unabhängige externe Replikation.

---

# 9. Stage 1 und 2 — Netzwerkbildung und stabile Rekurrenz

Die rekurrente Netzwerkstufe untersucht, ob aus verbundenen spikenden Einheiten über lange Läufe eine technisch stabile, reproduzierbare Dynamik entsteht. Der Stage-2-Engineeringvertrag wurde in der bisherigen Entwicklung nach deterministischen Langläufen, Replay und Restart/Restore als erreicht behandelt.

Wissenschaftlich wichtiger als das Label „stabil“ ist die Operationalisierung: Stabilität bedeutet nicht automatisch kritische Dynamik, biologisch plausible Aktivitätsverteilungen oder nützliche Repräsentation. Entsprechend bleiben Netzwerkgröße, Aktivitätsregime, Topologie, Störungsrobustheit und unabhängige Replikation eigenständige Fragen.

Historische Langlaufdaten werden nicht rückwirkend als Nachweis einer heute erweiterten Architektur interpretiert.

---

# 10. Stage 3 — plastisches Nervengewebe

Stage 3 integriert STDP, Eligibility, verzögerte Drei-Faktor-Modulation, Homeostase, strukturelle Plastizität und Ressourcen-/Zustandsgrenzen. Entscheidend ist die Trennung zwischen einem technisch funktionierenden Plastizitätsmechanismus und dem wissenschaftlichen Nachweis, dass dieser Mechanismus unter kontrollierten Bedingungen nützlich, stabil und erklärungskräftig ist.

Ein besonderer Engineeringvertrag ist:

`Proposal → Approval → Mutation → Journal → Undo`

Strukturelle Änderungsvorschläge können damit von ihrer Freigabe, tatsächlichen Mutation, Journalisierung und gegebenenfalls Rücknahme getrennt werden. Das verbessert Auditierbarkeit und Reproduzierbarkeit. Die Priorität/Neuheit dieses Musters gegenüber anderen Frameworks ist offen und wird nicht aus der Implementierung abgeleitet.

Notwendige wissenschaftliche Kontrollen umfassen mindestens learning-on/off, Frozen-/Sham-/Shuffle-Bedingungen, mehrere Seeds, held-out Evaluation und Langzeitstabilität.

---

# 11. Stage 4 — spezialisierte neuronale Areale

Stage 4 behandelt auditive, visuelle und digitale Pfade als unterschiedliche Modalitäten mit eigenen Adapter-, Kodierungs- und Plastizitätsregeln. Die E01–E05-Arbeiten und zugehörigen Referenz-/Experimentartefakte bilden eine DATA- und Engineeringgrundlage, aber keine pauschale Evidenz für funktionale Überlegenheit spezialisierter Areale.

Die wissenschaftliche Kernfrage lautet, ob modality-specific pathways gegenüber gematchten allgemeinen Pfaden einen reproduzierbaren Vorteil unter kontrollierten Bedingungen liefern und welcher Mechanismus diesen Unterschied verursacht.

Dafür sind Frozen-, Random-, Shuffle-, Information-Destroyed- und Läsionskontrollen sowie mehrere Seeds erforderlich. Aggregierte Topologiegrößen dürfen nicht als dynamisch ausgeführte Großskalierungsläufe dargestellt werden.

---

# 12. Stage 5 — integriertes künstliches Nervensystem

Stage 5 verbindet Sensorik, digitale Interozeption, autorisierte Aktorik, Feedbackschleifen, Ressourcenhaushalt und fail-closed Grenzen. Technisch ist ein durchgängiger Full-Stack-/E2E-Vertrag ein wichtiger Schritt. Wissenschaftlich ist damit jedoch noch nicht gezeigt, dass das System robuste adaptive closed-loop Kontrolle entwickelt.

Reale Geräte, Sensorausfälle, Aktor-No-Effect-Bedingungen, Replay/Open-Loop-Vergleiche und längerfristige Störungen müssen separat geprüft werden. Discovery eines Sensors ist keine Aktivierung; Pipeline-Erreichbarkeit ist kein erlerntes Tool Use.

---

# 13. Stage 6 — Gedächtnis und Weltmodell

Stage 6 ist aktuell der wichtigste wissenschaftliche Übergang von Signalverarbeitung und Plastizität zu zeitlicher Repräsentation, Vorhersage und möglicher Wissensbildung.

## 13.1 Implementierte Grundlage

Die aktuelle Entwicklung enthält beziehungsweise untersucht:

- begrenztes Working Memory,
- episodische Speicherpfade,
- semantische Prototyp-/Registry-Ansätze,
- Replay-/Ablationsverträge,
- Übergangsstatistik und Vorhersage,
- Prediction-Error-Infrastruktur getrennt von Rewardpfaden,
- action-conditioned bzw. mehrschrittige World-Model-Kandidaten,
- Persistenz-/Checkpointfragen für gekoppelten Kognitionszustand.

## 13.2 Claim-Grenze

Diese Komponenten sind **nicht gleichbedeutend** mit:

- vollständiger Episoden→Semantik-Konsolidierung,
- hierarchischem Predictive Coding,
- neuronaler dendritischer Fehlerrechnung,
- einem validierten generativen Weltmodell,
- planungsfähiger Modellnutzung,
- oder menschenähnlichem Gedächtnis.

Die stärkste derzeit zulässige Formulierung lautet: MHRN besitzt eine experimentierbare Gedächtnis-/Vorhersageinfrastruktur und mehrere Mechanismuskandidaten, deren wissenschaftliche Reichweite noch durch gezielte Interventionen bestimmt werden muss.

## 13.3 Semantization

Die relevante Hypothese ist, dass wiederholte episodische Erfahrung, Replay und Konsolidierung zu einer gegenüber Einzelepisoden abstrakteren Repräsentation führen können. Ein semantischer Store als Datenstruktur reicht dafür nicht aus. Nötig sind Operationalisierungen von Generalisierung, episodischer Abhängigkeit und Transfer, dazu Replay-off, shuffled-replay und matched-exposure Kontrollen.

## 13.4 Predictive Coding

Eine Vorhersage und eine numerische Abweichung zwischen Prediction und Observation bilden noch kein Predictive-Coding-Netz. Erforderlich ist ein neuronaler Mechanismus, in dem Prediction Error kausal die Aktivitäts-/Lerndynamik beeinflusst und gegen alternative Feedforward-/Residual-Erklärungen abliert werden kann.

## 13.5 World Model

Ein statistischer One-Step-Predictor ist eine wertvolle Referenz, aber kein vollständiges Weltmodell. Stärkere Claims benötigen rekursive Mehrschrittrollouts, action conditioning, Unsicherheitskalibrierung, out-of-distribution Tests sowie Nachweis eines Entscheidungsnutzens gegenüber reactive, no-model und corrupted-model Kontrollen.

---

# 14. Stage 7 — technische Identität, Verhalten und Selbstmodellgrenze

MHRN besitzt versionierte technische Profile, Digest-/Revision-/Lineage-Metadaten, Snapshot-Bindungen und einen operationalen Behavior Profile-Zustand. Diese Funktionen erlauben reproduzierbare technische Identität und kontrollierte Verhaltensparameter.

Sie sind **kein psychologisches Selbst**, kein Nachweis von Selbstbewusstsein und keine kausale Selbst/Andere-Repräsentation. Ein späteres Selbstmodell müsste unter Intervention zeigen, dass intern repräsentierte eigene Zustände oder Handlungen Vorhersagen/Entscheidungen kausal verbessern und von Fremdzuständen unterschieden werden.

---

# 15. Stages 8–10 — Frontier statt Ergebnisbehauptung

Die höheren Stufen sind bewusst als Forschungsfrontier geführt. Planung, Literatur, Fragenkataloge oder UI-Platzhalter dürfen keine Implementierungsreife vortäuschen.

Stage 8 betrifft höhere kognitive Integration, flexible Aufgaben- und Wissensnutzung. Stage 9 betrifft metakognitive, soziale oder höherstufige Modellierung. Stage 10 betrifft Grenzfragen, zu denen auch Bewusstseinsforschung gehören kann.

Für Stage 10 ist die Definitions-/Messproblematik selbst Teil der Methodik. Es existiert kein zulässiger Pfad von einem technischen Stage-Score zu der Aussage „bewusst“. Theorien, Indikatoren oder Verhaltensmaße können Forschungsobjekte sein, nicht automatische Bewusstseinsdetektoren.

Ethik, Wohlfahrt, Abbruchkriterien, externe Kontrolle und Verantwortlichkeiten müssen vor jeder stärkeren Forschung an potenziell leidens- oder autonomierelevanten Zuständen explizit definiert werden.

---

# 16. Gateway-Architektur: Inhalt und Berechnung trennen

MHRN unterscheidet **Content Gateway** und **Compute Backend**.

Das Content Gateway beschreibt, welche Information eine Systemgrenze überschreiten darf, wie sie kodiert wird und welche Provenienz/Kausalität erhalten bleibt. Das Compute Backend beschreibt, wo eine Berechnung ausgeführt wird — etwa CPU, GPU oder ein externer Dienst.

Diese Trennung verhindert, dass die Nutzung eines Beschleunigers oder externen Modells automatisch als semantische Informationsquelle interpretiert wird. Umgekehrt ist eine erlaubte Informationsquelle nicht automatisch berechtigt, den kausalen Kernzustand zu verändern.

Die konzeptionelle Trennung ist ein Kandidat für einen MHRN-Beitrag; ihre Neuheit gegenüber existierender Literatur bleibt zu prüfen.

---

# 17. Forschungssystem: RQ → H → EXP → DATA → Review → EVID → Claim

Der wissenschaftliche Lebenszyklus lautet:

```text
Research Question
    ↓
Hypothesis
    ↓
frozen / preregistered protocol
    ↓
Experiment execution
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

Softwaretests können einen Experimentrunner verifizieren, aber nicht dessen Hypothese bestätigen. DATA dürfen negative oder fehlgeschlagene Ergebnisse enthalten. EVID ist eine Reviewentscheidung mit Provenienz und darf nicht durch einen Dashboardstatus oder einen AI-Report erzeugt werden.

---

# 18. Negative Befunde und offene Ergebnisse

MHRN betrachtet negative Ergebnisse als wissenschaftlich wertvoll. Beispiele früherer Arbeit umfassen Läufe, deren Instrumentierung keine erwartete sichtbare Aktivität erfasste, Grenzaudits, die keine inhaltliche Hypothese testen konnten, sowie Skalierungs-/Ausführungsfehler, die als Fehlversuche erhalten blieben.

Die korrekte Reaktion auf verbesserte Instrumentierung ist ein neuer, quellengebundener Lauf. Historische DATA werden nicht „repariert“, um zu einer späteren Erwartung zu passen.

Auch das Fehlen von unabhängiger Replikation ist ein Ergebnis über den Reifegrad der Evidenz und darf nicht durch interne Wiederholung semantisch ersetzt werden.

---

# 19. Skalierung und 5D-Hypothese

Der mehrdimensionale Adressraum ist eine technische Repräsentation und zugleich eine offene Forschungshypothese. Der Name oder die Existenz von fünf Koordinaten belegt weder biologische Plausibilität noch funktionale Überlegenheit.

Notwendig sind topologie- und ressourcengematchte Ablationen, mindestens zwischen niedrigeren, gleichen und höheren Dimensionszahlen, bei denen Konnektivität, Parameterzahl, Laufzeitbudget und Auswertungsverfahren soweit möglich kontrolliert werden.

Skalierung muss ebenfalls getrennt werden in:

- Zahl der Neuronen/Synapsen,
- tatsächlich simulierte Ticks,
- reale Laufzeit und Speicherbedarf,
- numerische Stabilität,
- deterministische/reproduzierbare Identität,
- und wissenschaftliche Funktion.

Ein großer Graph ist noch kein wissenschaftlich informativer Großskalierungslauf.

---

# 20. Reproduzierbarkeit und technische Zustandsgrenzen

Reproduzierbarkeit verlangt mehr als einen Seed. Relevante Zustände umfassen je nach Experiment:

- RNG- und Backendzustände,
- Neuron-/Synapsenzustand,
- Delays/Queues,
- Plastizitätstraces und Eligibility,
- strukturelle Journale,
- Homeostase/Ressourcen,
- Gedächtnis/World-Model-Zustand,
- Gateway-/Adapterzustand,
- Profil-/Behavior-Zustand,
- Sensor-/Aktorinputs,
- Code-/Konfigurationsdigest.

Pause/Resume-Äquivalenz ist erst dann belegt, wenn alle hypothesenrelevanten Zustände Teil der kanonischen Checkpointgrenze sind.

---

# 21. Frontend als wissenschaftliches Instrument

Das Dashboard ist nicht nur Bedienoberfläche. Es muss den epistemischen Status sichtbar machen.

Deshalb besitzt der Release-Bereich getrennte Ansichten für:

- Engineering-/Entwicklungsreife,
- wissenschaftliche Reife,
- Releases/Gates,
- Roadmap und Dokumentation.

Der Publication Viewer lädt immer die im Publikationskatalog deklarierte aktuelle Fassung. Ab 1.7 ist der Reader-Einstieg das aktuelle `MANUSCRIPT.md`; Vorgänger und Frozen 1.5 bleiben verlinkt. Formeln, Quellen, Dateiverweise und wissenschaftliche Hinweise müssen im zentralen Viewer lesbar bleiben.

Eine Benutzeroberfläche darf keine stärkeren Claims erzeugen als die zugrundeliegenden Artefakte.

---

# 22. Potenzielle eigene Beiträge

Fassung 1.7 behandelt die folgenden Punkte als **Kandidaten**, nicht als bereits bewiesene wissenschaftliche Neuheit:

1. explizite Trennung von Logical Identity, Physical Slot, Synaptic Reduction und Execution Scheduling;
2. Proposal → Approval → Mutation → Journal → Undo für auditierbare strukturelle Plastizität;
3. Trennung von Content Gateway und Compute Backend;
4. source-bound DATA/EVID-Grenzen im kombinierten Forschungs-/Engineeringworkflow;
5. duale Engineering-/Scientific-Maturity-Timeline als projektspezifische Operationalisierung.

Die vollständige [Beitrags- und Neuheitsmatrix](CONTRIBUTION_MAP.md) nennt zu jedem Kandidaten Nachbarschaft, Neuheitsstatus und nächsten Nachweis.

---

# 23. Literaturprogramm und Related Work

Für Stage 6 sind unter anderem Forschungsrichtungen zu Complementary Learning Systems, episodisch-semantischer Konsolidierung, Replay, Predictive Coding in SNNs und spikenden World Models relevant. Die aktuelle Quellenarbeit trennt verifizierte Publikationen von Kandidaten und Quarantänequellen.

Eine Quelle wird nicht deshalb relevant, weil ihr Titel zu MHRN passt. In die finale Argumentation gehört nur Literatur, deren Identität, Publikationsort, DOI/URL und tatsächlicher Inhalt überprüft wurden.

Besonders wichtig ist die Unterscheidung zwischen:

- Literatur, die einen Mechanismus beschreibt,
- Literatur, die eine ähnliche Implementierung zeigt,
- Literatur, die einen empirischen Effekt berichtet,
- und Literatur, die tatsächlich eine Prior-Art-/Neuheitsfrage berührt.

---

# 24. Externe Review- und Ethikstruktur

Das Projekt besitzt standardisierte Fragenkataloge und Rollenprüfungen für technische, biologische, sicherheitsbezogene, Backend- und ethische Perspektiven. Solche Gremien ersetzen kein Peer Review; sie dienen der strukturierten Kritik und der Erfassung wiederkehrender Schwachstellen.

Für Publikationsreife sind je nach Claim zusätzliche Kompetenzen erforderlich, insbesondere Neurowissenschaft, Statistik, Ethik, Recht und externe methodische Replikation.

Ein Review muss negative Bewertungen bewahren. Die Aufgabe eines Reviews ist nicht, Kritik „auszuräumen“, indem sie verschwindet, sondern offene Kritik in überprüfbare Fragen, Experimente, Grenzen oder begründete Gegenargumente zu überführen.

---

# 25. Offenes Forschungsprogramm

Die nächsten wissenschaftlich priorisierten Arbeiten sind:

1. **Stage 0:** Modell-/Integratorablationen und externe Referenzreplikation.
2. **Stage 2:** unabhängige Replikation, Zielskalierung und Störungsrobustheit.
3. **Stage 3:** held-out Multi-Seed-Plastizitätsexperimente, Langzeitstabilität und Ressourceninteraktion.
4. **Stage 4:** modality-specific vs. general matched controls, Läsion/Shuffle/Frozen.
5. **Stage 5:** echte closed-loop Real-Device-/No-Effect-/Sensor-Loss-Studien.
6. **Stage 6:** Replay/Konsolidierung→Semantization, kausaler neuronaler Prediction Error, Mehrschritt-/aktionskonditioniertes World Model und decision benefit.
7. **Stage 7:** kausale self/other Unterscheidung und vollständige Checkpointäquivalenz.
8. **Stages 8–10:** erst Operationalisierung/Definitionsarbeit, dann Implementierung; keine Fortschrittsbehauptung aus Planung.
9. **Neuheitsprüfung:** Prior-Art-Recherche für die drei benannten Architektur-/Prozesskandidaten.
10. **Integrität:** externer Text-/Code-Similarity- und Quellen-Audit vor formaler Einreichung.

---

# 26. Schlussfolgerung

MHRN ist im aktuellen Stand am überzeugendsten nicht als fertige künstliche Kognition, sondern als **zunehmend streng instrumentiertes Forschungsframework** zu beschreiben. Der technische Fortschritt ist real und in mehreren Stufen weit fortgeschritten; die wissenschaftliche Reife liegt absichtlich dahinter, weil stärkere Aussagen Kontrollen, Replikation und Review benötigen.

Die wichtigste methodische Verbesserung der Fassung 1.7 besteht daher nicht in einer neuen großen Behauptung, sondern in einer strengeren Ordnung:

- historische und aktuelle Fassungen werden nicht vermischt;
- jede Datei in `docs/` und `research/` erhält eine deklarierte Rolle;
- Engineering und Evidenz bleiben getrennt;
- übernommene und eigene Ideen werden getrennt;
- potenzielle Beiträge werden von bewiesener Neuheit getrennt;
- negative Befunde bleiben erhalten;
- und die aktuelle Arbeitsfassung ist im Publication Viewer direkt sichtbar, während die empirische 1.5 eingefroren zitierbar bleibt.

Damit wird die Arbeit nicht „kritikfrei“. Sie wird **kritikfähig**: Ein externer Leser soll erkennen können, was MHRN behauptet, worauf diese Aussage beruht, was noch offen ist und wo eine Widerlegung oder Replikation ansetzen kann.

---

# Anhang A — stabile Einstiege

- [Aktuelle Edition 1.7](README.md)
- [Worte des Autors](AUTHOR_POSITION.md)
- [Beitrags- und Neuheitsmatrix](CONTRIBUTION_MAP.md)
- [Current-Pointer](../CURRENT.md)
- [Frozen 1.5](../FROZEN_V1.5.md)
- [Vorgänger 1.6](../2026-09-15_recursive-epistemics_v1.6/README.md)
- [Repositoryweite Integritätsrichtlinie](../../INTEGRITY_AND_ATTRIBUTION.md)
- [Related Work](../../RELATED_WORK.md)
- [Aktueller wissenschaftlicher Zustand](../../CURRENT_SCIENTIFIC_STATE.md)
- [Dokumentgovernance](../../../docs/00-governance/DOCUMENT_GOVERNANCE.md)

# Anhang B — Status dieser Fassung

`1.7` ist eine **lebende Arbeitsfassung**. Neue WIP-Erkenntnisse dürfen in diese Edition integriert werden, sofern ihre Provenienz dokumentiert bleibt. Sobald 1.7 eingefroren wird, muss eine nachfolgende 1.8 oder spätere Edition für weitere inhaltliche Änderungen eröffnet werden.
