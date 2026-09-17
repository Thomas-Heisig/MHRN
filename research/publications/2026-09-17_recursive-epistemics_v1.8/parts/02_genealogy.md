# Teil II — Schaffensgeschichte und Architekturgenese

## 5. Entwicklungsbogen

Die Schaffensgeschichte wird als Folge von Problemverschiebungen beschrieben, nicht als lineare Erfolgsgeschichte. Der frühe neuronale Würfel adressierte Persistenz, Wachstum und räumliche Organisation. Brain-5D machte daraus eine explizite mehrdimensionale Adress- und Geometriehypothese, verband sie mit spikender Dynamik, Plastizität, Homöostase, strukturellem Wachstum, multimodaler Kopplung und einer externen Sprachschnittstelle. MHRN verschärfte anschließend die Trennung zwischen Architektur, Experiment, DATA, Review, EVID und Claim.

Die Umbenennung Brain-5D → MHRN ist daher keine neue Evidenz. Sie reagiert auf die Gefahr, dass „5D“ als Naturbehauptung missverstanden wird. Fünf Koordinaten bleiben eine prüfbare Repräsentationsentscheidung; der aktuelle Projektname betont stattdessen Rekurrenz, Homöostase und Mehrskaligkeit.

## 6. Architekturentscheidungen und Revisionen

Mehrere heute zentrale Verträge lassen sich als Antworten auf frühere Mehrdeutigkeiten lesen. Ein persistenter Datenbankeintrag wird nicht als neuronales Gedächtnis behandelt. Ein LLM darf keinen stillen Schreibkanal in synaptische Gewichte oder Topologie erhalten. Monitoring und Intervention werden getrennt. Strukturänderungen werden proposal-, approval-, mutation- und journalfähig. CPU-/GPU-Beschleunigung darf keine wissenschaftliche Semantik verändern, ohne ihre Determinismusklasse offenzulegen.

Eine weitere Revision betrifft die Entwicklungslogik selbst. Frühe Phasen waren featuregetrieben: Eine plausible Funktion wurde implementiert und danach wissenschaftlich eingeordnet. Die heutige Regel dreht die Reihenfolge um: Forschungsfrage → Hypothese → minimale benötigte Fähigkeit → technische Validierung → Präregistrierung → autorisierte Ausführung → DATA → Analyse → Review → EVID → begrenzter Claim. Ein negativer Befund darf Architektur reduzieren, statt durch immer neue Rollenannahmen kompensiert zu werden.

## 7. Wissenschaftliche Verengung als Fortschritt

Die CL-001–CL-003-Linie ist ein wichtiges Beispiel. Ein kombinierter Semantic+Replay-Ansatz war gegenüber einer No-Replay-Baseline nützlich. Spätere, strengere Kontrollen zeigten jedoch keinen präregistriert bestätigten Zusatznutzen semantischer Verdichtung gegenüber gematchtem Raw-Replay; zugleich trug die semantische Repräsentation gegenüber einem Random-Prototype-Control relevante Struktur. Die Folge ist keine rhetorische Rettung, sondern eine engere Architekturposition: Replay bleibt Referenz, SemanticMemory ist ein Mechanismuskandidat mit begrenzter Rechtfertigung, bis Review und weitere explizit begründete Forschung etwas anderes tragen.

## 8. Nebenarbeiten als Genealogie, nicht als Ablage

Publikationen, Supplements, Frontend-/Viewer-Arbeiten, Safety-Programme, Spiegelmechanismen, Connectome-/Embodiment-Studien, biophysikalische Ablationsmodelle, Gedächtnis- und World-Model-Planung sowie Werkzeuge für lokale KI-Assistenten werden nicht als themenfremde Dateien behandelt. Edition 1.8 ordnet sie in die elfteilige Struktur ein und hält zugleich ihre ursprünglichen Pfade fest.

Ein maschinell erzeugter Quellenindex erfasst jede am Basiscommit versionierte Datei und jede Markdown-Überschrift unter `docs/` und `research/`. Diese Vollständigkeit ist eine **Bestandsvollständigkeit**, keine Garantie, dass jede Idee bereits semantisch perfekt klassifiziert wurde. Nicht klassifizierte Artefakte bleiben deshalb sichtbar und werden nicht gelöscht.

## 8.1 Architekturgenese in sechs Wendepunkten

### Wendepunkt A — Persistenz wird von „Speichern“ zu Zustandsvertrag

In der Vorphase war Persistenz zunächst ein praktisches Ziel: Der neuronale Zustand sollte einen Neustart überleben. Später zeigte sich, dass „gespeichert“ allein wissenschaftlich zu schwach ist. Ein reproduzierbarer Zustand benötigt eine definierte Grenze aus RNG, Neuronen, Synapsen, Delays, Queues, Plastizitätstraces, Strukturjournal, Homeostase, Ressourcen, Gedächtnis, Profilen, Gateway-Zuständen und gegebenenfalls Sensor-/Aktorinformationen.

Damit verschob sich die Frage von Datenhaltung zu **wissenschaftlicher Zustandsidentität**. Pause/Resume-Äquivalenz wurde ein prüfbarer Vertrag; Datenbankwissen wurde explizit von neuronaler Retention getrennt.

### Wendepunkt B — 5D wird von Leitmetapher zu offener Geometriehypothese

Brain-5D gab dem Projekt eine starke räumliche Leitidee. Mit wachsender wissenschaftlicher Strenge wurde aber sichtbar, dass eine Koordinate allein keine Funktion erzeugt. `EXP-GEN-0036` machte dies besonders deutlich: Die damalige 5D-v1-Studie variierte Dimensionen, koppelte die eigentliche Dynamik aber nicht ausreichend an Geometrie. Der Human Review klassifizierte die Frage für einen echten Geometrieeffekt als **nicht getestet**.

Diese Korrektur verändert die Architektur: Dimension darf künftig nur über einen präregistrierten Mechanismus wirken — etwa Nachbarschaft, distanzabhängige Konnektivität, Delay oder Plastizität. Der Name 5D ist damit keine Erklärung mehr, sondern ein experimenteller Faktor.

### Wendepunkt C — Plastizität wird auditierbar

Mit STDP, Eligibility, Drei-Faktor-Modulation, Homeostase und struktureller Plastizität wuchs die Gefahr, dass ein lernendes Netzwerk seine eigene Struktur auf schwer nachvollziehbare Weise verändert. Daraus entstand der Vertrag `Proposal → Approval → Mutation → Journal → Undo`.

Diese Kette ist mehr als Softwareorganisation. Sie trennt Hypothese, Freigabe, tatsächliche Mutation und Reversibilität. Dadurch kann eine Strukturänderung im Experiment gezielt erlaubt, verweigert, protokolliert oder zurückgenommen werden.

### Wendepunkt D — Multimodalität wird von „alles kann hinein“ zu typisierten Pfaden

Stage 4 ersetzte eine diffuse Multimodalitätsidee durch getrennte Audio-, Vision- und Digitalpfade mit unterschiedlichen Adaptern, Routingregeln und Plastizitätskandidaten. E01–E05 zerlegten die Frage weiter in Kosten, Ressourcenallokation, ROI/Foveation, digitale Integrität und Modalitätsverlust.

Damit wurde eine zentrale Grenze sichtbar: technisch spezialisierte Pfade sind noch kein Nachweis **emergenter** Spezialisierung. Vorgegebene Architektur und emergente funktionale Organisation werden seitdem getrennt behandelt.

### Wendepunkt E — Embodiment wird von Gerätezugriff zu kontrollierter Kausalität

Stage 5 verband Sensoren, Interozeption, Aktorik und Feedback. Gleichzeitig wurde der Zugriff auf reale Wirkungspfade stärker begrenzt: Discovery ist keine Aktivierung, Autorisierung ist ein eigener Status, und ein Effekt benötigt Acceptance-/Effect-Receipts.

Die 360-Run-Referenzkampagne zeigte, dass eine synthetische Sensor–SNN–Aktor–Feedback-Kette kontrolliert untersucht werden kann. Sie zeigte aber auch, welche stärkere Frage noch offen bleibt: Verbessert echter Closed Loop unter identischer externer Störung die Leistung gegenüber yoked Replay oder unterbrochener Rückmeldung?

### Wendepunkt F — Gedächtnis wird durch negative Evidenz vereinfacht

Stage 6 war zunächst architektonisch reich: episodische Pfade, semantische Prototypen, Replay, Prediction Error und World-Model-Kandidaten. Die CL-Experimente reduzierten diese Vielfalt epistemisch. Nachdem Raw-Replay als faire Kontrolle eingeführt wurde, verschwand der angenommene bestätigte Zusatznutzen der semantischen Verdichtung.

Die Architektur lernte daraus eine neue Regel: **Ein Mechanismus darf aus dem Zentrum verschwinden, wenn die Daten seinen Zusatznutzen nicht tragen.** Das ist ein wichtiger Unterschied zur frühen featuregetriebenen Phase.

## 8.2 Von Feature-Roadmap zu experimentgetriebener Entwicklung

Die heutige Roadmap ist nicht mehr primär eine Liste geplanter Fähigkeiten. Jede neue Fähigkeit muss an eine Forschungsfrage gebunden sein. Daraus folgt eine neue Reihenfolge:

`Frage → konkurrierende Hypothesen → minimale Fähigkeit → Verifikation → Freeze → autorisierter Lauf → DATA → Review → Architekturentscheidung`.

Diese Reihenfolge soll verhindern, dass Implementierung die Hypothese nachträglich definiert. Besonders bei Stage 6 wurde deutlich, dass ein bereits gebauter Mechanismus psychologisch schwerer zu verwerfen ist. Präregistrierte Stop-Regeln und eine explizite Referenzarchitektur wirken diesem Sunk-Cost-Effekt entgegen.

## 8.3 Die Nebenarbeiten als tatsächliche Architekturquellen

Mehrere scheinbar periphere Arbeiten haben die Kernarchitektur verändert:

- Der Publication Viewer führte zur klareren Trennung von aktueller WIP-Fassung, Vorgängern und Frozen Baseline.
- Die Dokumentgovernance führte zu Typ, Status, Autorität, Mutabilität, Zitierregel und Evidenzrolle pro Dokument.
- Lokale Chat-/Assistentensysteme schärften die Unterscheidung zwischen Interface-Gedächtnis und neuronaler Retention.
- AI-Review-Fehler führten zu strengeren Schema- und Provenienzgrenzen für automatische wissenschaftliche Auswertung.
- Safety-Arbeiten verschoben externe Aktorik zu deny-by-default, Capability-Gates und unabhängigen Stopppfaden.
- Spiegelmechanismus-Recherche verband Stage 4, 5, 6 und 7 zu einem neuen Querschnitt aus Wahrnehmung, Eigenhandlung, Prediction und Self/Other-Differenzierung.

Die Schaffensgeschichte ist deshalb nicht nur die Geschichte eines SNN-Kerns. Sie ist die Entstehung eines **Forschungssystems**, in dem technische Architektur und wissenschaftliche Governance zunehmend gemeinsam entworfen werden.
