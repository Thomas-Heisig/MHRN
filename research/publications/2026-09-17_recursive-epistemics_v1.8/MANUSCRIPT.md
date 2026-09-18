# Rekursive Epistemik in verkörperten spikenden neuronalen Architekturen

**Thomas Heisig · Edition 1.8 · current_wip · 17. September 2026**

> Die elfteilige Zielstruktur 2.0 wird hier als Edition 1.8 umgesetzt. Kein Software-Release 2.0, kein Peer-Review-Siegel und keine neue Evidenzentscheidung.

Vorgänger: [1.7](../2026-09-15_recursive-epistemics_v1.7/README.md). Unveränderte empirische Basis: [Frozen 1.5](../FROZEN_V1.5.md). [Erweiterungsvertrag](EXTENDING.md).

## Inhaltsverzeichnis

- [Teil I — Nullpunkt, Autor und Entstehungsbedingungen](#part-i)
- [Teil II — Schaffensgeschichte und Architekturgenese](#part-ii)
- [Teil III — Forschungsobjekt MHRN](#part-iii)
- [Teil IV — Empirisches Forschungsprogramm](#part-iv)
- [Teil V — Wissenschaftliche Infrastruktur und Engineering](#part-v)
- [Teil VI — Epistemologie und Methodik der Schaffensgeschichte](#part-vi)
- [Teil VII — Integrität, Autorschaft und kumulative Wissenschaft](#part-vii)
- [Teil VIII — Philosophie, Ethik und Sicherheit](#part-viii)
- [Teil IX — Rekursive Epistemik](#part-ix)
- [Teil X — Synthese und revidierbare Beiträge](#part-x)
- [Teil XI — Offene Forschungslandschaft](#part-xi)

<a id="part-i"></a>

# Teil I — Nullpunkt, Autor und Entstehungsbedingungen

## 1. Forschungsgegenstand vor dem Repository

Die 1.8-Fassung setzt nicht mit einem vermeintlich fertigen MHRN an. Sie behandelt die Entstehung selbst als Forschungsgegenstand. Die frühesten in dieser Revision wiedergewonnenen Spuren stammen aus Gesprächen über einen persistenten neuronalen Würfel, dynamische Verbindungen, entwicklungsähnliche Schichten, Mutation, Speicherung über Neustarts hinweg und die Trennung zwischen einem lernenden Kern und nachladbaren Funktionen. Diese Spuren werden als **rekonstruierte Vorphase** geführt. Sie belegen weder, dass dies die erste Idee überhaupt war, noch dass die beschriebenen Mechanismen damals schon implementiert waren.

Der historische Wert liegt in der Problemkontinuität: Wie kann ein System Wissen behalten, ohne dass ein externes Sprachmodell oder eine Datenbank fälschlich als neuronales Gedächtnis gezählt wird? Wie lässt sich Wachstum zulassen, ohne die Kausalität zu verlieren? Wie kann ein technisches System zugleich offen erweiterbar und wissenschaftlich prüfbar bleiben? Diese Fragen erscheinen später in deutlich strengeren Formen wieder: als Persistenzvertrag, Retrieval-Isolation, strukturelle Plastizität, Capability-Gates, Experimentregister und Evidenzgrenzen.

## 2. Autorposition

Thomas Heisig wird in dieser Arbeit als Autor und Projektleiter geführt. KI-Systeme sind als Recherche-, Synthese-, Kritik-, Programmier- und Formulierungswerkzeuge dokumentiert, erhalten aber keine automatische Quellen- oder Autoritätsrolle. Entscheidend ist nicht, ob ein Satz mit menschlicher oder maschineller Hilfe formuliert wurde, sondern ob seine Herkunft, seine Prüfgrundlage und seine Entscheidungskette nachvollziehbar sind.

Die Selbstauskunft des Autors ist eine Primärquelle für Motivation und Arbeitsweise, jedoch keine empirische Evidenz über neuronale Mechanismen. Persönliche Intuition kann Forschungsfragen erzeugen; sie darf keine Hypothese bestätigen. Umgekehrt wird die ungewöhnlich enge Mensch-KI-Arbeit nicht versteckt. Sie ist selbst Teil der epistemologischen Fragestellung dieser Arbeit: Was bedeutet Autorschaft, wenn externe kognitive Werkzeuge permanent an Suche, Gegenargument, Implementierung und Text beteiligt sind?

## 3. Von Metaphern zu Operationen

Frühe Begriffe wie „DNA“, „Traum“, „Fantasie“, „Emotion“ oder „Gehirn“ werden historisch erhalten, aber nicht rückwirkend biologisch aufgeladen. In der heutigen Terminologie werden sie nur dann verwendet, wenn eine messbare technische Entsprechung definiert ist. Offline-Replay ist nicht Schlaf. Ein Aktivierungs- oder Salienzparameter ist kein Gefühl. Parametervererbung ist keine biologische Genetik. Eine adressierte 5D-Struktur ist kein anatomisches Gehirn.

Diese Entmetaphorisierung ist kein Verlust der ursprünglichen Ideen. Sie macht sie testbar. Der Weg von einer anschaulichen Analogie zu einer operationalisierten Variable wird als Teil der Schaffensgeschichte dokumentiert, damit spätere Leser unterscheiden können, was Inspiration, was Spezifikation, was Implementierung und was tatsächlich gemessener Befund war.

## 4. Nullpunkt als offene Grenze

Edition 1.8 behauptet keinen exakt datierten „ersten Gedanken“. Für Zeiträume außerhalb des Git-Verlaufs stehen teilweise nur Zusammenfassungen früherer Chats oder später wiedergefundene Dokumente zur Verfügung. Diese werden mit Provenienzklasse S4 gekennzeichnet. Wo Originalnachrichten oder Originaldateien fehlen, lautet die wissenschaftlich korrekte Aussage „rekonstruiert“ oder „nicht rekonstruierbar“, nicht eine erfundene Präzision.

Damit ist Teil I bewusst erweiterbar. Neue Primärartefakte können die Chronologie verdichten oder korrigieren. Sie dürfen aber nicht stillschweigend bestehende Versionen überschreiben. Jede neue historische Zuordnung braucht Quelle, Datum beziehungsweise Datumsunsicherheit und eine Aussage darüber, ob sie Autoranforderung, KI-Vorschlag, Implementierung, Messung oder spätere Interpretation dokumentiert.

## 4.1 Die ursprüngliche Problemfamilie

Die rekonstruierten Vorarbeiten zeigen keine einzelne „Ur-Idee“, sondern eine wiederkehrende Problemfamilie. Schon vor dem heutigen MHRN standen sechs Fragen nebeneinander:

1. Wie kann ein neuronales System **über Neustarts hinweg** einen wissenschaftlich definierten Zustand behalten?
2. Wie kann ein Netzwerk **wachsen, sich verbinden und verändern**, ohne dass der Veränderungspfad unprüfbar wird?
3. Wie lassen sich **räumliche oder funktionale Nachbarschaften** so repräsentieren, dass daraus später experimentierbare Geometrie entsteht?
4. Wie kann externe Software — Datenbank, Sprache, Plugin, Werkzeug — genutzt werden, ohne sie fälschlich als **intern gelerntes neuronales Wissen** auszugeben?
5. Wie können Offline-Phasen, Replay und Rekombination genutzt werden, ohne Metaphern wie „Traum“ oder „Fantasie“ als empirische Tatsachen zu behandeln?
6. Wie kann ein System modular erweiterbar bleiben, ohne dass jedes neue Modul automatisch Schreibrechte auf den kausalen Lernkern erhält?

Diese Kontinuität erklärt einen großen Teil der späteren Architektur. Die heutige Trennung von Content Gateway, Compute Backend, neuronaler Persistenz, Retrieval-Isolation, Capability-Gates und struktureller Mutation ist keine nachträgliche ästhetische Ordnung. Sie ist eine Antwort auf Mehrdeutigkeiten, die bereits in der Vorphase sichtbar waren.

## 4.2 Aus Brain-5D übernommene Forschungsräume

Das Brain-5D Scientific Framework v0.2 verdichtete die frühe Ideenlandschaft zu einem expliziteren wissenschaftlichen Programm. Darin tauchten bereits mehrere Forschungsräume auf, die bis heute fortwirken:

- mehrdimensionale Adress- und Geometriehypothesen;
- unterschiedliche Neuronmodelle und Zeitskalen;
- STDP, Eligibility, Drei-Faktor-Lernen, Homeostase und strukturelle Plastizität;
- Graphnullmodelle, Motive, Stabilität, Metastabilität und kritische Dynamik;
- Information, Decoding, Representational Similarity und temporale Generalisierung;
- Gedächtnis, Continual Learning, Replay, Vorhersage und Language Organ;
- Storage, digitaler Zustand, Embodiment, Safety und Ressourcenskalierung.

Edition 1.8 übernimmt diese Räume nicht als bereits bestätigte Theorie. Sie übernimmt sie als **Genealogie der Forschungsfragen**. Mehrere Begriffe wurden inzwischen eingeengt: „5D“ ist keine Naturbehauptung; „Digital Twin“ ist ohne physisches Gegenstück primär ein reproduzierbarer digitaler Zustand; „Language Organ“ ist kein autoritativer Lernkern; „Homeostase“ ist eine technische Regelklasse, solange biologische Homologie nicht gezeigt wurde.

## 4.3 Die Schaffensart als methodischer Risikofaktor

Die kanonische Selbstauskunft des Autors beschreibt einen stark parallelen, werkstattartigen Arbeitsmodus: Problem sichtbar machen, Randbedingungen benennen, Mechanismus isolieren, Eingriff definieren, ausführen, messen, Fehler dokumentieren, erst danach verallgemeinern. Dieser Modus hat die hohe Entwicklungsgeschwindigkeit ermöglicht, erzeugt aber ein spezifisches Risiko: **Struktur lässt sich schneller schließen als Empirie.**

Genau dieses Risiko ist in den Vorgängerarbeiten mehrfach sichtbar geworden. Ein technisch sauber gebautes Modul konnte im Frontend bereits vollständig erscheinen, obwohl seine wissenschaftliche Rolle erst teilweise geprüft war. Ein plausibles Semantikmodul konnte zentral wirken, bevor Raw-Replay als stärkere Kontrolle eingeführt wurde. Eine 5D-Bedingung konnte formal existieren, obwohl die Dynamik nicht ausreichend an die Geometrie gekoppelt war.

Aus diesen Erfahrungen entstand eine methodische Selbstkorrektur: Engineering-Fertigstellung und Scientific Readiness werden getrennt; negative Ergebnisse dürfen Architektur reduzieren; UI-Prozentwerte sind keine Fähigkeitsscores; und eine neue Funktion erhält keinen wissenschaftlichen Status allein durch Integration.

## 4.4 Mensch-KI-Zusammenarbeit als reale Entstehungsbedingung

MHRN ist in einer Arbeitsweise entstanden, in der menschliche Zielsetzung, mehrere KI-Assistenten, Literaturrecherche, Codegenerierung, Review, Tests und Git-Provenienz eng verschränkt sind. Diese Konstellation wird nicht geglättet. Für die Entstehungsgeschichte ist gerade wichtig, zwischen unterschiedlichen Beitragsarten zu unterscheiden:

- **Autoranforderung:** welche Richtung, Grenze oder Funktion der Mensch verlangt;
- **KI-Vorschlag:** welche Lösung, Formulierung oder Hypothese ein Assistenzsystem anbietet;
- **menschliche Entscheidung:** welche Variante angenommen, verändert oder verworfen wird;
- **Commit:** was tatsächlich implementiert und versioniert wurde;
- **Run/DATA:** was tatsächlich ausgeführt und gemessen wurde;
- **Review:** welche Interpretation anschließend akzeptiert, eingeschränkt oder verworfen wurde.

Diese Kette ist ein Teil der späteren Theorie rekursiver Epistemik. Die Arbeit untersucht nicht nur ein lernendes System; sie entsteht selbst in einem System aus Quellen, Werkzeugen, Reviews, Entscheidungen und Statusänderungen.

## 4.5 Persönliche Motivation und ihre wissenschaftliche Grenze

Die Vorgängerfassung dokumentiert die persönliche Motivation des Autors als Mischung aus technischer Praxis, starkem Ordnungs- und Abschlussdrang sowie langfristigem Interesse an kognitiven Systemen und deren Veränderungen. Diese Motivation ist epistemisch relevant, weil sie erklärt, warum bestimmte Fragen verfolgt werden. Sie besitzt jedoch keine Beweiskraft für deren Antwort.

Die verbindliche Regel lautet deshalb: **Nähe erzeugt Fragen, nicht Antworten.** Persönliche Erfahrung, handwerkliche Systemintuition oder interdisziplinäre Analogien dürfen einen Suchraum öffnen; sie ersetzen weder neurowissenschaftliche Fachliteratur noch Statistik, Replikation, Ethikprüfung oder Peer Review.

Gerade weil MHRN außerhalb institutioneller Forschungsstrukturen entstanden ist, muss die Arbeit ihre Grenzen expliziter machen: Was ist Selbstbeschreibung? Was ist externe Theorie? Was ist implementierter Mechanismus? Was ist DATA? Was wurde menschlich reviewt? Was ist noch offen? Diese Trennung ist nicht nur Dokumentationsstil, sondern ein Kompensationsmechanismus für fehlende institutionelle Selbstverständlichkeit.


---

<a id="part-ii"></a>

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


---

<a id="part-iii"></a>

# Teil III — Forschungsobjekt MHRN

## 9. Systemdefinition

MHRN ist ein Forschungsframework für rekurrente spikende Netzwerke mit explizitem Zeitverlauf, versionierten neuronalen und synaptischen Zuständen, Plastizitätsmechanismen, struktureller Veränderung, Homeostase, Persistenz, sensorischen/digitalen Gateways, Gedächtnis- und Vorhersagekandidaten sowie kontrollierten externen Werkzeugen. Das Framework untersucht nicht „Intelligenz“ als unteilbare Eigenschaft, sondern eine Folge operationalisierter Mechanismen und Funktionen.

Izhikevich-artige Neuronen sind eine recheneffiziente Modellfamilie mit unterschiedlichen Spike- und Burstregimen [Izhikevich, 2003](REFERENCES.md#ref-IZHIKEVICH2003). MHRN behandelt sie als austauschbare Dynamikklasse, nicht als biologisch vollständiges Neuron. LIF-, HH- oder Multi-Compartment-Varianten sind Ablations- oder Alternativmodelle; biologische Detailtreue wird nicht durch das bloße Hinzufügen von Kanalnamen erzeugt.

## 10. Rekurrenz, Plastizität und Homöostase

Rekurrenz ist ein Mechanismus, dessen funktionale Bedeutung kontrolliert werden muss. Dass eine rekurrente Bedingung mehr synaptische Ereignisse erzeugt als eine feedforward-nahe Kontrolle, ist zunächst ein Netzwerkbefund und noch kein Beleg für Gedächtnis, 5D-Vorteil oder höhere Kognition.

Für Plastizität trennt die Architektur lokale zeitabhängige Regeln, Eligibility und modulierte Drei-Faktor-Mechanismen. Drei-Faktor-Regeln sind theoretisch besonders relevant, wenn ein späteres modulatorisches Signal lokale Aktivität zeitlich überbrücken soll [Frémaux & Gerstner, 2016](REFERENCES.md#ref-FREMAUX2016). In MHRN wird ein solches Signal jedoch nicht automatisch „Dopamin“ genannt. Entscheidend ist die experimentell definierte Funktion.

## 11. Geometrie und 5D

Der fünfdimensionale Adressraum ist eine technische und wissenschaftliche Hypothese. Drei Dimensionen können räumliche/topologische Lokalität tragen, zwei weitere funktionale, modale, entwicklungsbezogene oder assoziative Nähe. Keine dieser Semantiken ist naturgegeben. Ein 5D-Effekt ist erst dann wissenschaftlich interessant, wenn Neuronen-, Synapsen-, Grad-, Delay-, Input- und Rechenbudgets gegenüber niedrigeren, gleichen und höheren Dimensionskontrollen hinreichend gematcht sind.

Edition 1.8 hält zusätzlich die frühere Idee lernbarer Metriken, dimensionsgekoppelter Distanz und sparse materialisierter Adressräume fest. Dabei wird klar zwischen Adressraum, materialisiertem Graphen und vollständigem dynamischen Zustandsraum unterschieden.

## 12. Gedächtnis, Replay und Weltmodell

Ein gespeicherter Zustand ist nicht automatisch Gedächtnis. Gedächtnis wird über Retention, cue-abhängigen Recall, Spezifität und Generalisierung operationalisiert. Complementary-Learning-Systems-Modelle motivieren unterschiedliche schnelle und langsame Lernprozesse sowie interleaved learning [McClelland et al., 1995](REFERENCES.md#ref-MCCLELLAND1995), doch MHRN übernimmt daraus keine fertige biologische Zuordnung.

Ein One-Step-Predictor ist ebenfalls kein vollständiges Weltmodell. Stärkere Claims erfordern action conditioning, Mehrschrittrollouts, Unsicherheitskalibrierung, Out-of-Distribution-Prüfung und einen kausalen Entscheidungsnutzen gegenüber reaktiven/no-model/corrupted-model Kontrollen. Prediction Error muss, wenn er als neuronaler Mechanismus beansprucht wird, nachweisbar in Aktivität oder Lernen eingreifen.

## 13. Sprache, Wissen und externe Intelligenz

Das Language Organ ist außerhalb des kausal autoritativen SNN-Lernkerns positioniert. Es kann übersetzen, strukturieren, erklären, recherchieren oder Vorschläge erzeugen. Ein Eingriff in den Kern benötigt einen expliziten, protokollierten Gateway- und Policy-Pfad. Damit bleibt die Frage testbar, welche Leistung aus SNN, Retrieval, Decoder, Sprachmodell oder menschlicher Entscheidung stammt.

Diese Grenze schließt leistungsfähige hybride Systeme nicht aus. Sie verhindert nur, dass ein externer symbolischer Dienst unbemerkt als Beweis für intern gelerntes neuronales Wissen verwendet wird.

## 13.1 Tatsächlich erreichter Stand der Stages 0–10

Die Vorgängerarbeiten enthalten wesentlich mehr als eine Architekturdefinition. Der Forschungsgegenstand ist bereits durch eine Reihe implementierter und teilweise experimentell untersuchter Stufen konkretisiert. Die folgende Zusammenfassung ersetzt nicht die jeweiligen Primärartefakte, integriert aber ihre belastbare Aussage in den Haupttext.

### Stage 0 — einzelne Nervenzelle

Die Einzelzellprimitive ist nicht mehr nur technisch vorhanden. Für den begrenzten, explizit definierten Konformitätsumfang wurde ein wissenschaftlicher Readiness-Vertrag abgeschlossen. In `EXP-STAGE0-20260916-MODEL-CONFORMANCE-V2` wurden vorab eingefrorene Endpunkte auf disjunkten Confirmatory-Seeds gegen Brian2 2.10.1 geprüft. Für die Izhikevich-2003-Transition stimmten alle 192 confirmatory samples in ihren Spike-Entscheidungen überein; der größte beobachtete Vor-Reset-Spannungsfehler lag bei etwa `6.82e-13` und damit weit unter der eingefrorenen Schwelle `1e-8`. Für `lif-current-v1` waren in drei 1000-Tick/5-Zell-Vergleichen die Spike-Ereignisse identisch; der maximale Membranfehler lag bei ungefähr `7.11e-15`.

Die Arbeit brachte zugleich eine wichtige negative Erkenntnis hervor: Der frühere freie 1000-Tick-Izhikevich-V1-Vergleich bleibt als negativer Befund erhalten, weil kleinste numerische Differenzen in einem nichtlinearen freien Verlauf später zu abweichenden Spike-Zeitpunkten führen können. Damit wurde die Forschungsfrage präzisiert: Referenzkonformität muss zwischen lokaler Übergangs-/Reset-Konformität und langfristiger Trajektorienidentität unterscheiden.

Auch die LIF-Refraktärsemantik wurde explizit geklärt. Bei `dt=1 ms` entsprechen `refractory_ticks=1/2/3` in der validierten Zuordnung Brian2-Refraktärzeiten von `2/3/4 ms`; gleiche numerische Werte bedeuten also nicht automatisch gleiche Semantik. Für den 10-Hz-Homeostasecontroller wurde ein konfigurationsgebundener Arbeitsbereich dokumentiert: Eingangsströme 16–25 erreichten das Ziel ohne Aktuator-Sättigung, bei 30 wurde die +10-mV-Grenze erreicht. Dies ist ein Operating-Envelope-Befund, kein biologisches Universalgesetz.

Der zugehörige maschinenlesbare Readiness-Status weist für den **scoped Stage-0 research-readiness contract 100 %** aus. Diese 100 % bedeuten ausschließlich: die dort definierten Prüfpunkte sind erfüllt. Menschlich reviewte EVID und unabhängig autorisierte Replikation bleiben getrennte Reifegates und sind damit nicht automatisch abgeschlossen.

### Stage 1 — kleines SNN

Stage 1 verfügt über einen technischen Small-SNN-Vertrag und Referenzartefakte zur Spike-Ausbreitung. Der wissenschaftliche Stand ist schwächer als die technische Reife: Die bisherigen Artefakte zeigen technische Funktion in kleinen Netzen, aber noch keine breite task-basierte Evidenz, Skalierbarkeit oder unabhängige Replikation. Der zentrale Übergang zu Stage 2 ist deshalb nicht „mehr Neuronen“, sondern die Frage, ob rekurrente Dynamik unter kontrollierten Interventionen einen kausal isolierbaren funktionalen Beitrag liefert.

### Stage 2 — stabile Rekurrenz

Die rekurrente Stufe besitzt Langlauf-, Determinismus-, Restart/Restore- und Netzwerkverträge. Ein wichtiger neuer Befund stammt aus `EXP-GEN-0036`: Die `PING`-Bedingungen zeigen einen klaren deskriptiven mechanistischen Unterschied zwischen `recurrence_off` und `recurrence_on`. Beide Bedingungen stammen aus derselben Basiskonstruktion; die Rekurrenzbedingung ergänzt gezielt eine Rückkante. Der Effekt ist damit innerhalb des kleinen simulierten Systems mechanistisch interpretierbar, aber noch keine breite Generalisierung. Die über Seeds identischen Trajektorien sind insbesondere keine zehn statistisch unabhängigen Replikate.

Diese Review korrigierte zugleich die Berichtsebene: Gedankenstriche in der universellen Summary-Tabelle bedeuteten nicht fehlende DATA. Trial-, STDP-, Lern-, TIME- und Regulationsprotokolle waren ausgeführt; ihre Metriken passten nur nicht in die zu enge SNN-Haupttabelle. Damit wurde ein echter Reporting-/AIRR-Fehler von einem Experimentfehler getrennt.

#### Aktuelle Reproduzierbarkeitslinie EXP-GEN-0045/0046

Nach der ersten 1.8-Strukturfassung kamen zwei weitere explorative DATA-Läufe hinzu. `EXP-GEN-0045` (`tonic_spike_reproducibility_v1`, RQ-SNN-002/H-SNN-002-A) führte drei Same-Seed-Tonic-Replikapaare für die Seeds 101, 102 und 103 aus. In allen drei Fällen war `spike_sequence_identical=true`. Der Befund dokumentiert für genau diesen Protokollumfang reproduzierbare Spike-Sequenzen bei gleichem Seed, Input und Anfangszustand; `scientific_evidence=false` und `automatic_evidence_promotion=false` bleiben ausdrücklich erhalten.

`EXP-GEN-0046` (`deterministic_replica_v1`, RQ-DET-001/H-SNN-003-A) erweitert die Prüfung auf zwölf 256-Tick-Läufe: `recurrence_off_replica_a/b` und `recurrence_on_replica_a/b` über dieselben drei Seeds. Innerhalb der jeweiligen Replica-Paare sind die gespeicherten Trajektorien deskriptiv identisch. Recurrence-off erzeugt pro Lauf 3 Spikes, 2 synaptische Ereignisse, 0 recurrent events und propagation depth 1; Recurrence-on erzeugt 33 Spikes, 33 synaptische Ereignisse, 10 recurrent events und propagation depth 61. Damit werden Reproduzierbarkeit und der bereits bekannte mechanistische Rekurrenzunterschied auf einer neuen DATA-Linie sichtbar.

Die wissenschaftliche Grenze ist wesentlich: `EXP-GEN-0046` ist als `EXPLORATORY` markiert, seine semantische Konsistenz steht auf `NOT_AUTOMATICALLY_CLASSIFIED`, die Evidence Readiness auf `BLOCKED_UNCLASSIFIED_SEMANTICS`, und der Human Review ist noch offen. Der AIRR ist Interpretation-only und besitzt trotz einer intern formulierten „supported“-Bewertung keine EVID-Autorität. Identische Ausgaben über Seeds beziehungsweise Replicapaare sind zudem keine automatisch unabhängigen Replikationen.

### Stage 3 — plastisches Nervengewebe

Stage 3 integriert STDP, Eligibility, verzögerte Drei-Faktor-Modulation, Homeostase, strukturelle Plastizität sowie Ressourcen- und Zustandsgrenzen. Der besondere Engineeringvertrag `Proposal → Approval → Mutation → Journal → Undo` trennt Änderungsvorschlag, Autorisierung, tatsächliche Strukturmutation, Journalisierung und Rücknahme. Dies macht Strukturplastizität auditierbar und experimentell abladierbar.

Der wissenschaftliche Stand bleibt jedoch enger: Implementierte Gewichtsänderung ist noch kein Nachweis nützlichen Lernens. Die noch ausstehenden starken Prüfungen betreffen held-out Generalisierung, learning-on/off, Frozen/Sham/Shuffle, Langzeitstabilität, Interaktion mit Homeostase und Ressourcen sowie unabhängige Replikation.

### Stage 4 — spezialisierte neuronale Areale

Stage 4 besitzt drei getrennte Referenzpfade: Audio (`stage4.audio.temporal`), Vision (`stage4.vision.spatial`) und Digital (`stage4.digital.symbolic`). Die Pfade unterscheiden sich in Adaptern, Routing und Plastizitätskandidaten. Der technische Topologievertrag beschreibt aggregiert 100.000 Neuronen und 10 Millionen gerichtete Kanten, aber **nicht** einen vollständig dynamisch materialisierten 100k/10M-Lauf; `dynamic_scale_execution_verified=false` bleibt Teil der Grenze.

Die E01–E05-Serien liefern konkrete DATA:

- `RQ-MSBA-E01`: gleiche mittlere Task-Accuracy der Referenzmodalitäten; modellierte Kosten im gespeicherten Datensatz Digital < Audio < Vision.
- `RQ-MSBA-E02`: adaptive Referenzallokation liegt in den gespeicherten DATA über fixer und zufälliger Allokation.
- `RQ-MSBA-E03`: adaptive visuelle ROI/Foveation erreicht im synthetischen Design dieselbe Task-Accuracy wie Full-Image bei geringerem modelliertem Energieverbrauch.
- `RQ-MSBA-E04`: im digitalen Integritätspfad traten keine gespeicherten Checksum- oder Exact-Payload-Mismatches auf.
- `RQ-MSBA-E05`: adaptive Referenzkompensation zeigte nach Modalitätsverlust eine höhere Task-Recovery als fixe Allokation.

Diese Befunde stützen technische Teilfunktionen in den jeweiligen synthetischen Designs, aber noch keinen allgemeinen Vorteil spezialisierter Areale, keine biologische Äquivalenz und keine physikalisch gemessene Energieeffizienz.

### Stage 5 — integriertes künstliches Nervensystem

Stage 5 verbindet typisierte Sensorgrenzen, digitale Interozeption, autorisierte Aktorik, die `ExperienceEngine`, Feedback und Ressourcenregulation. Der Referenzversuch `EXP-STAGE5-20260914-INTEGRATED-NERVOUS-SYSTEM` verwendet sechs Bedingungen — `authorized`, `unauthorized`, `actuator_failure`, `sensor_loss`, `open_loop_replay`, `sensor_reproducibility` — mit 20 unabhängigen Läufen × 3 Wiederholungen, insgesamt **360 kontrollierten Runs**.

Die DATA zeigen, dass die registrierte deterministische Sensor–SNN–Aktor–Feedback-Kette unter kontrollierten Bedingungen zielgerichtete Wirkungen erzeugen und unautorisierte bzw. fehlerhafte Wirkungspfade abgrenzen kann. Das ist DATA-Support für `H-EMB-001-A`, keine automatisch akzeptierte EVID und keine Generalisierung auf reale Geräte. `H-EMB-001-B` — der streng gematchte Vergleich von Closed Loop, yoked Replay und unterbrochener Rückmeldung unter identischer Störung — bleibt offen.

Interozeptionsgrößen wie `energy_reserve`, `resource_pressure` oder `thermal_threat` bleiben technische Kontrollvariablen. Sie sind weder Stoffwechselhomologien noch Hinweise auf subjektives Empfinden.

### Stage 6 — Gedächtnis und Weltmodell

Stage 6 umfasst Working-Memory-Grundlagen, episodische Speicherpfade, semantische Prototypen, Replay, Übergangsstatistik, Prediction-Error-Infrastruktur und World-Model-Kandidaten. Die stärkste bisherige empirische Erkenntnis entstand aus der CL-001–CL-003-Linie.

CL-001 zeigte einen Vorteil von Semantic+Replay gegenüber einer No-Replay-Baseline, trennte die Ursache aber nicht. CL-002 führte gematchtes Raw-Replay ein und bestätigte keinen konfirmatorischen Zusatznutzen semantischer Prototypen; die Projekt-EVID klassifizierte H1 für dieses Protokoll als falsifiziert. CL-003 prüfte die verbleibende Dosisalternative in 84 Runs = 12 Seeds × 7 Bedingungen. C1, C2 und C4 bestanden die präregistrierten Erfolgsregeln nicht. Der Semantic-minus-Raw-Unterschied stieg deskriptiv mit der Dosis, durfte aber wegen des negativen Interaktionstests C4 nicht als bestätigter Dosis-Effekt interpretiert werden. C3 (`S20 − X20`) war dagegen deutlich positiv: Semantic lag gegenüber Random Prototype um rund +14,9 Prozentpunkte höher.

Die derzeit zulässige DATA-only-Synthese lautet deshalb: **Replay ist unter den untersuchten Bedingungen der nachweisbare Hauptbeitrag; semantische Verdichtung trägt nicht-zufällige Struktur, zeigt aber keinen präregistriert bestätigten Zusatznutzen gegenüber gematchtem Raw-Replay.** CL-003 bleibt bis Human Review DATA, nicht EVID.

### Stage 7 — technische Identität und Selbstmodellgrenze

Versionierte technische Profile, Digests, Lineage, Snapshot-Bindung und Behavior State bilden eine reproduzierbare technische Identität. Sie sind kein psychologisches Selbstmodell. Ein stärkerer Stage-7-Claim erfordert kausale self/other-Interventionen, bei denen intern repräsentierte eigene Zustände oder Handlungen Vorhersagen oder Entscheidungen messbar verbessern und von Fremdzuständen unterschieden werden.

### Stages 8–10 — Frontier

Stage 8 enthält Continual-Learning- und Interferenzprogramme sowie Vorläufer-DATA, aber keine bestätigte autonome lebenslange Entwicklung. Stage 9 enthält Forschungsfragen zu hochintegrierter Kognition, jedoch keine confirmatory Stage-9-DATA. Stage 10 ist eine Governance- und Forschungsfrontier zu Bewusstseinsfragen; es existiert kein zulässiger Pfad von einem technischen Score zu Bewusstsein, Sentienz oder moralischem Status.

## 13.2 Eine zentrale Revision: 5D wurde bisher nicht adäquat getestet

`EXP-GEN-0036` liefert für die 5D-Frage keinen Nullbefund, sondern einen **Testadäquanzbefund**. Die damalige `run_5d()`-Implementierung variierte die Dimensionskoordinaten einer kontrollierten Drei-Neuronen-Kette, während die wesentliche Konnektivität, Gewichte und Delays explizit gesetzt blieben. Die Dynamik war damit konstruktiv kaum sensitiv für die Dimension.

Der Human Review klassifizierte `RQ-5D-005` deshalb für diesen Teilversuch als **NOT TESTED** hinsichtlich eines genuinen Geometrieeffekts. Künftige 5D-Prüfungen müssen vorab definieren, über welchen Mechanismus Dimension wirken darf — etwa Nachbarschaft, distanzabhängige Konnektivität, Delays oder Plastizität — und benötigen Aktivitäts-Adequanz, matched topology/degree, Shuffle- und Random-Graph-Kontrollen. Das ist ein wichtiger Erkenntnisfortschritt: Ein ungeeignetes Experiment darf nicht als Nullbefund gegen eine Hypothese interpretiert werden.

## 13.2 Periphere Netze, Neural Symbiosis und MSBA

Die kanonische Architektur enthält neben dem SNN-Kern eine explizite periphere Multi-Netz-Grenze. **Neural Symbiosis** bezeichnet dabei keine zweite Intelligenz im Kern, sondern eine Embodiment-Schicht, in der spezialisierte neuronale oder virtuelle Verarbeitungssysteme über deklarierte Gateways an den SNN angebunden werden können. Der offene Adaptervertrag kann unter anderem CNN-, Vision-Transformer-, Transformer-, RNN-/LSTM-/GRU-, GNN-, Reservoir-, Hopfield-, VAE-, Autoencoder-, multimodale und neuro-symbolische Komponenten beschreiben. Ebenso können Datenbanken, Wissensgraphen, Retrieval-, Logik- oder externe Speicherdienste als virtuelle Areale auftreten.

Diese Offenheit ist wissenschaftlich nur tragfähig, wenn **Erreichbarkeit von gelernter Nutzung getrennt** bleibt. Ein registrierter Adapter, ein erreichbarer Endpunkt oder eine erfolgreiche Inferenz beweist weder, dass das SNN den Pfad auswählt, noch dass es von ihm lernt oder einen kausalen Vorteil besitzt. Gateway-Plastizität ist deshalb standardmäßig gesperrt; Random-, Frozen-, Shuffle- und Plastic-Zustände gehören in experimentgebundene, persistierbare Laufkontexte. Externe Netze erhalten keine impliziten Schreibrechte auf kanonische Neuronen-, Synapsen-, Reward-, Gedächtnis- oder EVID-Zustände.

Unterhalb dieser Grenze konkretisiert **MSBA** die modalitätsspezifische Bahnarchitektur. Audio, Vision und Digital werden nicht als biologische Kortexplagiate behandelt, sondern als technische Pfade mit unterschiedlichen Informations- und Ressourcenverträgen:

- Audio priorisiert zeitliche Kohärenz, Band-/Phasen- beziehungsweise Hüllkurveninformation und begrenzte Delay-Strukturen.
- Vision verwendet räumliche/featurebezogene Projektionen, sparse Zielgrade und experimentelle ROI-/Foveationsmechanismen.
- Digital hält exakte Nutzdaten außerhalb des SNN in checksum-gebundenen Symbolframes; das SNN erhält nur eine deterministische Populationrepräsentation. Lernen darf Routing oder Assoziation verändern, nicht die ursprünglichen Bits oder ihre Prüfsumme.

Eine besonders wichtige Korrektur betrifft Dimensionalität. Der MSBA-Projektionsraum darf experimentell zwischen 1 und 32 Dimensionen variieren, während der produktive Neuron-ID-/Persistenzvertrag des Kerns weiterhin **fünfdimensional** bleibt. Ein 16D- oder 32D-Projektor ist daher weder ein 16D-/32D-SNN noch Evidenz für einen Vorteil höherer Kerndimensionalität. Projektion, Mapping und produktiver Kern müssen in jeder Studie getrennt provenance-gebunden werden.

Auch Ressourcenangaben bleiben typisiert: `normalized_energy_units`, kalibrierte Schätzungen in Joule und tatsächlich gemessene Joule sind drei verschiedene Größen. Die Stage-4-E01–E05-DATA dürfen deshalb modellierte Energieunterschiede zeigen, ohne daraus physikalisch gemessene Energieeffizienz abzuleiten.

## 13.3 Wesen, reale Körpergrenze und technische Identität

Die Vorgängerarbeiten entwickelten mit **Wesen** eine maschinen-native Körperdarstellung. Wissenschaftlich relevant ist daran nicht die visuelle Anthropomorphie, sondern die harte Trennung von beobachtetem Zustand und Interpretation. Die Körpergrenze wird aus tatsächlich erkannten Verbindungen, Host-Ressourcen und Embodiment-Endpunkten aufgebaut. Nicht vorhandene Temperatur-, Lüfter-, Sensor- oder Aktorwerte bleiben unbekannt; es werden keine plausibel wirkenden Ersatzdaten erfunden. `available` ist ausdrücklich nicht gleich `authorized` und nicht gleich `active`.

Maschinen-native Interozeption umfasst dort, wo das Betriebssystem Messwerte liefert, etwa CPU-/Speicherlast, Temperatur, Lüfter, Storage, Netzwerk und Kontinuitätsgrößen. Diese Größen können technische Regulationszustände beeinflussen, sind aber keine biologischen Stoffwechselhomologien und keine Empfindungsindikatoren. Ebenso ist die body-like Darstellung nur Präsentationssemantik.

Der implementierte Profile-&-Identity-Vertrag speichert Konfiguration, Fähigkeiten, Grenzen, Provenienz, Revisionen, Lineage und Snapshot-Bindungen als technische Identität. Profil, `.b5d`-Snapshot, Runtime-Checkpoint, Registry und Lineage sind absichtlich getrennte Zustandsklassen. Daraus folgt **keine psychologische Identität, Persönlichkeit, subjektive Kontinuität oder Bewusstseinsbehauptung**. Genau diese Grenze ist für spätere Stage-7-Selbstmodellforschung zentral: Metadatenidentität ist eine technische Voraussetzung, kein kausales Selbstmodell.


---

<a id="part-iv"></a>

# Teil IV — Empirisches Forschungsprogramm

## 14. Verbindlicher Forschungszyklus

Das empirische Programm folgt dem Zyklus `RQ → H → benötigte Fähigkeit → minimale Implementierung → technische Validierung → Präregistrierung/Freeze → autorisierte Ausführung → DATA → präregistrierte Analyse → Human Review → EVID → begrenzter Claim → Folgefrage`. RQ-Status, Hypothesenstatus, DATA, EVID und Claim-Status sind unterschiedliche Zustandsräume.

Edition 1.8 erzeugt deshalb aus einem Run niemals automatisch Evidenz. Der Publikationsbuilder liest Register und Ergebnisse, darf aber keine Experimente starten und keine EVID-Entscheidung schreiben. Diese Trennung ist technisch prüfbar und soll verhindern, dass ein komfortabler Viewer oder Runner wissenschaftliche Autorität vortäuscht.

## 15. Experimentfamilien

Das historische Brain-5D-Framework enthielt bereits thematische Familien für Geometrie, Stabilität, Plastizität, Gedächtnis, Continual Learning, Language Organ/Knowledge Intake, Embodiment, Emergenz, Storage/Twin-Fidelity und Scaling. Edition 1.8 erhält diese Forschungsräume, ersetzt ihre alten Kurzkennungen aber nicht rückwirkend durch neue IDs. Die kanonischen aktuellen RQs und Hypothesen werden unverändert aus `research/registry/` projiziert.

Für jede Familie gelten Kontrollen, die den jeweils plausibelsten Confound adressieren: dimensionsgematchte Nullmodelle für Geometrie; recurrence-on/off und topology controls für Netzwerke; learning-on/off, Frozen, Sham und Shuffle für Plastizität; Retrieval-off und state-permuted Bedingungen für Gedächtnis; Open-/Closed-loop sowie sensor-loss/no-effect für Embodiment; action-conditioned und corrupted-model Kontrollen für Weltmodelle.

## 16. Statistik und experimentelle Einheit

Viele Ticks oder Spikes sind keine unabhängigen Stichproben. Für zahlreiche Vergleiche ist der unabhängig initialisierte Seed beziehungsweise Lauf die experimentelle Einheit; Zeitfenster desselben Laufs sind wiederholte Messungen. Vor einem konfirmatorischen Lauf werden Primärendpunkte, Kontraste, Seeds, Ausschlusskriterien, Testfamilie und Erfolgsregel eingefroren. Explorative Nachanalysen sind zulässig, müssen aber als explorativ markiert werden.

## 17. Negative und Nullbefunde

Ein negatives Ergebnis ist kein defektes Experiment, wenn Protokoll, Instrumentierung und Ausführung valide sind. Es begrenzt den Hypothesenraum. CL-002 und CL-003 zeigen diese Regel exemplarisch: Die semantische Verdichtung erhält Struktur, aber ihre behauptete Mehrleistung gegenüber gematchtem Raw-Replay wurde unter den geprüften Protokollen nicht präregistriert bestätigt. CL-003 bleibt bis Human Review **DATA**, nicht EVID.

## 18. Spiegelmechanismen und Handlungsvorhersage

Die Arbeit zu Spiegelmechanismen wird als Stage-6-naher Forschungsstrang integriert. Der prüfbare Kern ist nicht das Etikett „Spiegelneuron“, sondern die Frage, ob Beobachtungs- und Ausführungsrepräsentationen partiell überlappen, ob Kontext und Zielrelevanz diese Überlappung modulieren und ob ein Prediction-Error-Mechanismus einen kausalen Zusatznutzen liefert. Stage 4 liefert sensorische Pfade, Stage 5 Eigenaktionen/Outcome, Stage 6 Vorhersage; Stage 7 Selbst/Fremd-Unterscheidung ist erst nach eigener Kausalprüfung zulässig.

## 19. Replikation

Interne Multi-Seed-Wiederholung ist wichtig, ersetzt aber keine unabhängige Replikation. Replikation muss Code-/Umgebungsprovenienz, unabhängige Ausführung und ein vorher definiertes Vergleichskriterium besitzen. Scientific Maturity darf deshalb auch bei technisch grünem System unter 100 % bleiben.

## 19.1 Historische Experimentlinie und was sie tatsächlich geleistet hat

Die empirische Arbeit von MHRN ist nicht erst mit CL-001 begonnen. Die Vorgängerfassungen und Supplements enthalten eine längere Sequenz von Verifikation, Diagnose, Ablation und konfirmatorisch angelegten Experimenten. Für Edition 1.8 werden diese Ergebnisse in einer gemeinsamen Leselogik zusammengeführt.

### Einzelzelle: von Softwaretest zu externer Referenzkonformität

Der frühere Einzelzellstand bestand zunächst vor allem aus deterministischen Softwareverträgen. Die V2-Konformitätskampagne verschob die Frage auf einen stärkeren Prüfpunkt: Stimmen lokale Übergänge, Schwellen- und Resetsemantik mit einer externen Referenzimplementierung überein? Die Antwort war für den eingefrorenen Umfang positiv. Gleichzeitig blieb der ältere freie 1000-Tick-Izhikevich-Negativbefund erhalten. Daraus folgt eine methodische Erkenntnis: Ein Referenzvergleich muss explizit sagen, ob lokale Gleichungssemantik oder globale freie Trajektorie geprüft wird.

### Science Suite / EXP-GEN-0036: Diagnose statt pauschaler Fachbeweis

`EXP-GEN-0036` führte 180 Runs über zehn Seeds aus und deckte sieben Protokollgruppen ab: `ping`, `temporal`, `stdp`, `learning`, `time`, `5d` und `regulation`. Der wichtigste Erkenntnisgewinn lag nicht in einer einzigen Fachhypothese, sondern in der Trennung von **Artefaktvollständigkeit**, **interner Konsistenz** und **fachlicher Testadäquanz**.

Die erste automatische Zusammenfassung ließ bei mehreren Bedingungen leere SNN-Spalten erscheinen. Die Human Review zeigte, dass diese Bedingungen nicht fehlten; ihre Metriken waren nur anderer Art. Damit wurde ein Reporting-/AIRR-Fehler identifiziert und die falsche Missing-DATA-Interpretation korrigiert. Für die Forschungsgovernance ist dies bedeutsam: Berichtsprojektion ist ein eigener Fehlerkanal und darf nicht mit fehlender Ausführung gleichgesetzt werden.

Für `PING` zeigte sich ein klarer mechanistischer Recurrence-Effekt im kleinen kontrollierten Netz. Für die 5D-Teilstudie ergab die Review dagegen **NOT TESTED**: Die Koordinaten wurden variiert, die Dynamik war aber nicht ausreichend geometrieabhängig konstruiert. Das Experiment war damit für den behaupteten Geometrieeffekt nicht sensitiv genug. Ein solcher Befund ist methodisch stärker als ein falsch formulierter Nullbefund, weil er die nächste Präregistrierung konkret verbessert.

### EXP-GEN-0045/0046: Reproduzierbarkeit wird selbst zum Forschungsobjekt

Die nach der ersten 1.8-Synthese hinzugekommenen Experimente `EXP-GEN-0045` und `EXP-GEN-0046` verschieben Determinismus von einer allgemeinen Engineeringannahme zu einer explizit gespeicherten DATA-Frage. EXP-GEN-0045 prüft Same-Seed-Tonic-Replikapaare; drei von drei getesteten Seeds erzeugten identische Spike-Sequenzen. EXP-GEN-0046 prüft vier Recurrence-Bedingungen mit jeweils paarigen Replikaten und drei Seeds, insgesamt zwölf Runs bei 256 Ticks. Die jeweiligen Replica-Paare reproduzieren dieselben deskriptiven Netzwerkmetriken.

Der Erkenntniswert liegt auf zwei Ebenen. Erstens wird die technische Reproduzierbarkeit der untersuchten kleinen SNN-Trajektorien konkret dokumentiert. Zweitens zeigt EXP-GEN-0046 erneut den starken Unterschied zwischen Recurrence-off und Recurrence-on: 3 gegenüber 33 Spikes, 2 gegenüber 33 synaptischen Ereignissen, 0 gegenüber 10 recurrent events und propagation depth 1 gegenüber 61. Dieser Unterschied ist im registrierten kleinen Simulationsaufbau mechanistisch sichtbar.

Wissenschaftlich bleiben beide Läufe unterhalb einer EVID-Entscheidung. EXP-GEN-0046 ist explorativ, semantisch noch nicht automatisch klassifiziert und blockiert deshalb eine Evidence-Readiness-Promotion. Sein AIRR bleibt post-hoc Interpretation mit Human Review `PENDING`; die AI-Konfidenz wurde aufgrund eines Schemafehlers konservativ auf 0.0 normalisiert. Edition 1.8 übernimmt daher ausschließlich die gespeicherten DATA und deren explizite Statusgrenzen.

### Stage 4 / MSBA: fünf spezifische Forschungsfragen statt ein pauschaler Multimodalitätsclaim

Die Stage-4-E01–E05-Linie zerlegt Spezialisierung in fünf enger gefasste Fragen. Dadurch wurde vermieden, aus einem funktionierenden multimodalen Stack sofort „emergente Arealbildung“ abzuleiten.

`E01` verglich modalitätsspezifische Kosten bei matched tasks; die Referenzmodalitäten erreichten dieselbe mittlere Task-Accuracy, während die modellierten Kosten Digital < Audio < Vision lagen. `E02` zeigte im gespeicherten synthetischen Datensatz einen Vorteil der adaptiven Ressourcenallokation gegenüber fixer und zufälliger Allokation. `E03` erreichte mit adaptiver visueller ROI/Foveation dieselbe Task-Accuracy wie Full-Image bei geringerem modelliertem Energieverbrauch. `E04` zeigte im digitalen Integritätspfad keine gespeicherten Checksum- oder Exact-Payload-Mismatches. `E05` zeigte unter Modalitätsverlust eine höhere Task-Recovery der adaptiven Referenzkompensation als bei fixer Allokation.

Diese Befunde sind DATA und stützen jeweils den engen technischen Prüfgegenstand. Sie tragen weder einen allgemeinen Vorteil spezialisierter Areale noch emergente Spezialisierung oder physikalische Energieeffizienz.

### Stage 5 / Embodiment: 360 kontrollierte Runs, aber noch kein Realweltbeweis

Der Stage-5-Referenzversuch umfasst 360 kontrollierte Runs in einer synthetischen deterministischen Umgebung. Die sechs Bedingungen prüfen autorisierte und unautorisierte Wirkungspfade, Aktorfehler, Sensorausfall, Open-Loop-Replay und Sensorreproduzierbarkeit. Der Lauf stützt auf DATA-Ebene `H-EMB-001-A`: Die registrierte Sensor–SNN–Aktor–Feedback-Kette kann unter den kontrollierten Bedingungen zielgerichtete Wirkungen erzeugen und nicht autorisierte bzw. fehlerhafte Pfade abgrenzen.

Nicht abgeschlossen ist `H-EMB-001-B`. Dafür braucht es identische externe Störung und einen direkt gematchten Vergleich zwischen Closed Loop, yoked Replay und unterbrochener Rückmeldung. Der existierende Open-Loop-Pfad ist ein wichtiger Kontrollbaustein, aber kein Ersatz für dieses strengere Design. Reale Hardware bleibt ein separater safety-gated Forschungszweig.

### Stage 6 / Continual Learning: der bisher stärkste Fall empirischer Architekturselektion

CL-001 bis CL-003 bilden derzeit die methodisch wichtigste Kette, weil die Experimente die Architekturposition tatsächlich verändert haben.

CL-001 zeigte Semantic+Replay > No-Replay. Der Befund war positiv, aber kausal unzureichend aufgelöst. CL-002 ersetzte die schwache Baseline durch gematchtes Raw-Replay. Unter diesem Protokoll wurde kein konfirmatorischer Zusatznutzen semantischer Prototypen bestätigt; H1 wurde in der menschlichen Projekt-EVID für CL-002 als falsifiziert klassifiziert. CL-003 prüfte die verbleibende Dosisalternative mit 84 Runs. Die primären Kontraste C1, C2 und C4 scheiterten an den präregistrierten Erfolgsregeln; C3 zeigte dagegen, dass Semantic gegenüber einem Random-Prototype-Control deutlich bessere Struktur trägt.

Daraus entstand eine konkrete Architekturregel: Raw-Replay ist die kanonische Referenz. `SemanticMemory` bleibt technisch vorhanden, wird aber nicht mehr allein aufgrund theoretischer Plausibilität als zentraler Kernmechanismus behandelt. Weitere Rollenprüfungen dürfen nicht seriell zur Rettung eines negativen Befunds erzeugt werden. Genau eine weitere theoretisch begründete Rolle ist nur dann zulässig, wenn sie vorab begründet und präregistriert wird; andernfalls wird der Mechanismus dezentriert oder geparkt.

## 19.2 Was als EVID gilt — und was ausdrücklich nicht

Die Forschungsarbeit hat aus den Vorgängerexperimenten eine strengere Evidenzhierarchie entwickelt:

- **Engineering verification** zeigt, dass ein Mechanismus oder Vertrag technisch funktioniert.
- **DATA** sind persistierte, quellengebundene Messergebnisse eines definierten Runs.
- **Interpretation** ordnet DATA in eine Forschungsfrage ein und kann falsch sein.
- **Human Review** kann Fehler in Instrumentierung, Bericht oder Schlussfolgerung identifizieren.
- **EVID** ist eine explizite Reviewentscheidung mit Provenienz und Claim-Grenze.
- **Independent replication** ist ein weiterer Reifeschritt und wird nicht durch mehrere Seeds derselben Pipeline ersetzt.

Diese Trennung wurde nicht abstrakt erfunden, sondern aus konkreten Fehlerfällen gelernt: dem zu groben Stage-0-Langzeitvergleich, der Summary-Fehlprojektion in EXP-GEN-0036, der inadäquaten 5D-v1-Operationalisierung und der Baseline-Verwechslung in der frühen Continual-Learning-Linie.

## 19.3 Experimentelle Stop-Regeln als Bestandteil der Theorie

Ein wiederkehrendes Problem explorativer Forschung ist die Möglichkeit, einen Mechanismus durch ständig neue Rollenannahmen gegen negative Befunde zu immunisieren. MHRN behandelt deshalb Stop-Regeln zunehmend als Teil der wissenschaftlichen Theorie.

Für `SemanticMemory` bedeutet dies: Ein negativer Zusatznutzen gegenüber Raw-Replay darf zur Reduktion des Mechanismus führen. Für 5D bedeutet es: Ein nicht testadäquates Protokoll wird nicht als Nullbefund wiederholt, sondern zunächst neu operationalisiert. Für biophysikalische Erweiterungen bedeutet es: HH, Multi-Compartment, NMDA, Astrozyten, Gap Junctions oder quantale Freisetzung werden nur als fragegetriebene Modellvarianten aufgenommen, nicht als kumulative Biologie-Checkliste.

Damit wird der Forschungsprozess selbst selektiv: Nicht jede technisch mögliche Erweiterung erhält automatisch einen Platz im Kern.

## 19.6 Neural-Symbiosis- und MSBA-Forschungsprogramm

Die Architekturarbeit an Neural Symbiosis erzeugt ein eigenes falsifizierbares Programm, dessen Hypothesen nicht mit der bloßen Existenz der Pipeline verwechselt werden dürfen. Relevante Fragen sind beispielsweise, ob task-relevante periphere Areale gegenüber informationsgematchten irrelevanten Kontrollen stärkeren effektiven Gateway-Einfluss erwerben, ob verrauschte Areale selektiv unterdrückt werden, ob Gateway-Struktur nach Kontrolle roher Aktivität mit prädiktiver Information variiert und ob nach Sensorläsion adaptive Umleitung gegenüber Frozen- oder Random-Kontrollen tatsächlich Leistung erhält.

Für solche Studien sind mindestens Frozen-, Random-, Shuffle-/Timing- und informationszerstörte Kontrollen erforderlich. Eine Korrelation zwischen Gateway-Gewicht und Leistung reicht nicht für einen kausalen Tool-/Area-Use-Claim. Produktive Aktivierung bleibt bis zu experimenteller Validierung gesperrt.

Das MSBA-Programm E01–E05 operationalisiert einen Teil dieses Raums bereits für Audio, Vision und Digital. Die bisherigen synthetischen DATA werden in Teil III und X bilanziert; ihre stärkere wissenschaftliche Prüfung verlangt weiterhin spezialisierte-vs.-generalistische matched controls, Cross-Modal-Transfer, Läsionsstudien, reale Ressourcenmessung und unabhängige Review. Increased-dimensional MSBA-Projektionen müssen außerdem strukturierte, reduzierte, randomisierte und geshuffelte Mappingkontrollen enthalten und dürfen nicht als Kerndimensionalitätsstudie ausgegeben werden.

## 19.7 Externe Mechanismusvorarbeiten für Stage 6

Die kanonische Related-Work-Arbeit präzisiert mehrere externe Referenzlinien. Arbeiten zu hippocampal-kortikaler Semantization und continual learning motivieren Replay-/Konsolidierungsfragen, ohne einen MHRN-SemanticMemory-Mechanismus zu validieren [D'Alba et al., 2025](REFERENCES.md#ref-DALBA2025) [Shi et al., 2025](REFERENCES.md#ref-SHI2025). Eine aktuelle SNN-Predictive-Coding-Übersicht zeigt, dass Prediction Error auf unterschiedliche Weise neuronal repräsentiert werden kann; ein Telemetriefeld gleichen Namens ist daher noch kein Predictive-Coding-Mechanismus [N'dri et al., 2026](REFERENCES.md#ref-NDRI2026). Spiking-World-Model-Arbeit mit expliziter modellbasierter Kontrolle setzt eine deutlich stärkere Referenz als ein passiver One-Step-Predictor [Sun et al., 2025](REFERENCES.md#ref-SUN2025). Multi-Zeitskalen-Plastizität mit astrozyteninspiriertem Gating zeigt einen externen Mechanismuskandidaten für Stabilitäts-/Plastizitätsfragen, ist aber kein Wirksamkeitsnachweis der MHRN-Regelung [Dong & He, 2026](REFERENCES.md#ref-DONG2026).

Diese Literatur wird in 1.8 bewusst als **externer Präzedenz-/Vergleichsraum** integriert. Sie kann die Form einer MHRN-Forschungsfrage verbessern, aber weder DATA erzeugen noch eine interne Hypothese bestätigen.

## 19.8 Determinismus-Registry, AIRR und Testadäquanz

Zwei Entscheidungen vom 17. September 2026 präzisieren die Verwendung der jüngsten SNN-DATA. Erstens bleibt der historische Lauf `EXP-BATCH-20260914074039-02` unverändert `RQ-SNN-002` zugeordnet. Seine beobachtete Condition `same_seed_tonic_replica_pair` ist für diese historische Registrierung ein semantischer Mismatch und darf nicht post hoc umetikettiert werden. Der technische Befund kann als Determinismusdiagnostik zitiert werden, aber nur gemeinsam mit dieser Provenienzgrenze.

`RQ-DET-001` besitzt nun einen expliziten Determinismusvertrag: entweder isolierte Same-Seed/Same-Input-Tonic-Replikapaare oder die expliziten `recurrence_off/on_replica_a/b`-Bedingungen. `RQ-SNN-002` behält dagegen seinen Recurrence-off/on-Vertrag; der bestehende saubere Lauf `EXP-SNN-002-R2` erfüllt diesen mit zehn Seeds. Ein neuer Lauf wird nicht allein erzeugt, um einen Registry-/Pipelinefehler kosmetisch zu reparieren.

AIRR bleibt Interpretation-only. Bei semantischem `MISMATCH` wird die öffentliche/reportseitige `ai_confidence` deterministisch auf `0.0` gesetzt; die ursprüngliche Modellselbsteinschätzung bleibt nur im append-only AIAR-Auditdatensatz. Ein isolierter Tonic-Test ist außerdem ausdrücklich **kein Netzwerkbefund** und seine Laufzeit darf nicht als Netzwerkperformance interpretiert werden.

Die zweite Entscheidung betrifft `EXP-GEN-0047` und `H-SNN-003-B`. Die sechs Conditions `1d`, `2d`, `3d`, `5d`, `5d_shuffled` und `random_graph` sind semantisch korrekt und der Lauf ist technisch reproduzierbar. Dennoch ist `topology_propagation_v1` **INADEQUATE_TO_TEST_HYPOTHESIS**: Nur drei Neuronen und zwei feed-forward Synapsen tragen die Dynamik; bei den nicht-randomisierten Bedingungen verändert sich die Koordinate, aber nicht ausreichend der kausale Übertragungsmechanismus. Daher sind identische Ergebnisse über 1D/2D/3D/5D weder ein Topologie-Nullbefund noch eine Widerlegung eines 5D-Effekts.

Die einzige deskriptive Abweichung des v1-Laufs — eine um einen Tick frühere First-Response-Latency im `random_graph` — ist konfundiert mit einer geänderten Kantenanordnung und darf nicht zum Dimensionseffekt hochgestuft werden. Auch `stopped_on_quiescence=false` ist kein Fehler: Der Runner setzt `min_ticks=max_ticks` und erzwingt damit das vollständige Beobachtungsfenster.

Für `topology_propagation_v2` gilt deshalb ein stärkerer prospektiver Vertrag: mindestens 1.000 Neuronen pro Condition, im Mittel mindestens zehn eingehende Synapsen, gematchte globale Struktur/Parameter/Stimulusenergie, explizite Kopplung von Geometriedistanz an Konnektivitätswahrscheinlichkeit und/oder Delay, die sechs genannten Kontrollen einschließlich degree-/density-matched Random Graph, multi-neuronaler Input, First-Arrival-/Reach-Verteilungen als Primärgrößen, Activity-Adequacy-Gate, mehrere unabhängige Seeds, vorab eingefrorene Inferenzregel und clean-tree Provenienz. Diese Werte sind Mindestschwellen für die nächste Testgeneration, keine Behauptung allgemeiner Suffizienz.

## 19.9 Genehmigter Stage-6-Kompressionsvorschlag

Mit `LP-20260917194217` liegt ein **genehmigter, aber nicht ausgeführter** human-origin Lernvorschlag vor. Die Forschungsfrage ist enger als der bisherige CL-003-Vergleich: Kann semantische Prototypkonsolidierung bei **10 % des Raw-Replay-Speicherbudgets** mindestens 95 % der Retention eines Raw-Replay-Baselines mit vollem Speicherbudget erreichen?

Der Vorschlag bindet `semantic_prototype_replay_10pct_budget` gegen `raw_replay_full_budget` und nennt als Kontrollen `no_replay`, `random_prototype_10pct` und `learning_off`. Die Evaluation soll auf Holdout-Daten nach sequentiellen Tasks erfolgen. Die Erfolgsmetrik ist `retention_ratio_at_1_10_storage >= 0.95` der Raw-Replay-Retention.

Der aktuelle Status ist strikt prospektiv: `authority=proposal_only`, `executed=false`, `runtime_authority=none`. Die menschliche Genehmigung autorisiert daher weder eine Ergebnisbehauptung noch DATA/EVID. Vor einer wissenschaftlich tragfähigen Ausführung müssen die referenzierten CL-002-/CL-003-Quellen digestscharf gebunden, die noch als `UNKNOWN` markierte Source-Trust-Einstufung geklärt und der Ausführungs-/Freeze-Vertrag entsprechend dem Research-Driven-Development-Prozess fixiert werden.

## 19.4 Aktuelle Human Reviews: Determinismus und Testadäquanz

Die aktuelle Review-Linie schärft zwei bereits ausgeführte Experimente, ohne historische DATA umzuschreiben.

Für `RQ-DET-001 / H-SNN-003-A` wurde der historische Lauf `EXP-BATCH-20260914074039-03` menschlich post-hoc geprüft. Die vier Replica-Bedingungen sind nach dem heutigen semantischen Vertrag ein `DIRECT_MATCH`: innerhalb jeder Recurrence-Konfiguration stimmen Replica A und B für die Seeds 101, 102 und 103 in den aufgezeichneten Antwortsummen überein. Ohne Rekurrenz wurden je Lauf 3 Spikes, 2 synaptische Ereignisse, 0 recurrent events und propagation depth 1 beobachtet; mit Rekurrenz 33 Spikes, 33 synaptische Ereignisse, 10 recurrent events und propagation depth 61. Das ist ein positiver Determinismusbefund **innerhalb des getesteten Same-Seed-Protokolls**.

Die wissenschaftliche Grenze bleibt jedoch bestehen: der historische Lauf wurde mit `git dirty: true` erzeugt. Die nachträgliche semantische Korrektur beseitigt diesen Provenienzblock nicht. Deshalb bleibt eine clean-tree-Replikation mit eingefrorenen Source-/Config-Hashes Voraussetzung für eine reguläre EVID-Prüfung. Auch `stopped_on_quiescence=false` ist hier kein Fehlschlag: im festen Beobachtungsfenster bedeutet das Feld lediglich, dass der Lauf nicht vorzeitig wegen Quieszenz beendet wurde.

Für `RQ-SNN-003 / H-SNN-003-B` wurde `EXP-GEN-0047` ebenfalls methodisch neu eingeordnet. Die sechs Bedingungen `1d`, `2d`, `3d`, `5d`, `5d_shuffled` und `random_graph` sind semantisch die beabsichtigten Bedingungen und damit `DIRECT_MATCH`. Trotzdem ist `topology_propagation_v1` als `INADEQUATE_TO_TEST_HYPOTHESIS` klassifiziert. Der Aufbau verwendete nur drei Neuronen und zwei Feed-forward-Synapsen; bei den nicht-randomisierten Bedingungen blieben Gewichte, Delays und explizite Kette gleich, während die Koordinaten die Dynamik nicht hinreichend beeinflussten. Die identischen Kernantworten — 3 Spikes, 2 synaptische Ereignisse, 3 aktivierte Neuronen, 0 recurrent events, depth 1 — dürfen daher **nicht** als Evidenz dafür gelesen werden, dass Topologie oder Dimensionalität keinen Effekt besitzen. Der Einzelunterschied der first-response latency im Random-Graph-Arm ist zudem mit einer geänderten Kantenanordnung konfundiert.

Aus beiden Reviews folgt ein allgemeiner methodischer Vertrag: **semantischer Match, technische Reproduzierbarkeit, Testadäquanz, Provenienz und EVID sind getrennte Prüfachsen**. Ein `DIRECT_MATCH` kann wissenschaftlich blockiert bleiben; ein technisch sauberer Lauf kann für die Zielhypothese `NOT_TESTED` sein; und eine nachträgliche Registry-Korrektur darf weder Dirty-Tree-Provenienz noch unzureichendes Versuchsdesign rückwirkend heilen.


---

<a id="part-v"></a>

# Teil V — Wissenschaftliche Infrastruktur und Engineering

## 20. Determinismus und Zustandsgrenzen

Reproduzierbarkeit ist mehr als ein Seed. Hypothesenrelevante Zustände können RNG, Scheduler, Neuronen, Synapsen, Delays, Queues, Plastizitätstraces, Eligibility, Strukturjournal, Homeostase, Ressourcen, Gedächtnis, World Model, Gateway-Zustand, Sensorinput und Code-/Konfigurationsdigest umfassen. Pause/Resume-Äquivalenz ist nur so stark wie die definierte Checkpointgrenze.

MHRN trennt Logical Identity, Physical Slot, Synaptic Reduction und Execution Scheduling. Diese Trennung soll verhindern, dass Speicherlayout oder GPU-Reihenfolge unbemerkt die wissenschaftliche Semantik verändern. Byteidentität ist nicht für jede Plattform realistisch; deshalb werden bitnahe, numerische und statistische Reproduktionsklassen unterschieden.

## 21. Storage und Digital State

Die frühere Idee eines „Digital State Twin“ bleibt erhalten, wird aber begrifflich begrenzt. Solange kein physisches Gegenstück synchron gekoppelt ist, beschreibt der Begriff primär einen reproduzierbaren digitalen Zustandszwilling. Primärzustände, Ereignisprovenienz und Rekonstruktionsverträge haben Vorrang vor löschbaren Heatmaps oder Analyseprojektionen.

Sparse Materialisierung, arrayorientierte Strukturen, Chunking und graphgeeignete Persistenz sind Skalierungsfragen. Millionen Python-Objekte sind kein wissenschaftliches Ziel. Ein großer Adressraum darf nicht mit einer vollständig materialisierten Population verwechselt werden.

## 22. Runtime, Beschleunigung und Ressourcen

Runtime-Performance ist wissenschaftlich relevant, wenn sie bestimmt, welche Skalen oder Zeitspannen überhaupt experimentell zugänglich sind. Beschleunigung darf jedoch Integrationsschritt, Ereignisordnung oder Reduktionsregeln nicht still verändern. Ressourcenproxies werden nicht als physikalische Energie ausgegeben, solange keine entsprechende Kalibration vorliegt.

## 23. Dashboard, Viewer und Research Catalog

Das Frontend ist wissenschaftliches Instrument. Es muss Engineering-Reife, wissenschaftliche Reife, DATA, EVID und Planung sichtbar trennen. Der Publication Viewer zeigt die aktuelle Arbeitsfassung, hält aber Frozen 1.5 und Vorgänger erreichbar. Eine schöne Oberfläche darf keinen stärkeren Claim erzeugen als das Quellartefakt.

Edition 1.8 ergänzt deshalb einen maschinellen Quellenindex, eine unveränderte Registry-Projektion und ein Erhaltungsmanifest. Jeder historische Publikationsblob am Basiscommit wird gehasht. Alle damaligen Markdown-Überschriften in `docs/` und `research/` werden indiziert. Dies schafft eine überprüfbare Untergrenze gegen versehentliches Vergessen, aber keine Garantie semantischer Vollständigkeit.

## 24. Lokale KI-Werkzeuge als Forschungsinfrastruktur

Arbeiten an lokalen Chat-/Assistenzsystemen, Provider-Adaptern, Streaming, persistenten Konversationen und Trainings-Workbenches fließen dort ein, wo sie den Forschungsprozess betreffen: reproduzierbare Datensätze, Trennung von Quelle/Dataset/Job/Artefakt, lokaler Datenschutz, Provider-Isolation und Werkzeugprovenienz. Sie werden nicht als neuronale Evidenz für MHRN umgedeutet.

Die Grenze zwischen Forschungswerkzeug und Forschungsobjekt bleibt explizit. Ein LLM kann einen Runner schreiben oder einen Bericht kritisieren; der daraus entstehende Commit muss dennoch durch Tests, Review und experimentelle Provenienz abgesichert werden.

## 24.1 Infrastruktur als Ergebnis der Fehlersuche

Mehrere zentrale Infrastrukturentscheidungen entstanden nicht am Reißbrett, sondern aus konkreten Fehlerfällen. Die Entwicklungsgeschichte zeigt dabei vier wiederkehrende Klassen.

### Zustandsfehler

Frühe Persistenzfragen machten deutlich, dass ein gespeicherter Graph allein keinen wissenschaftlich identischen Zustand garantiert. Scheduler, RNG, Delays, Queues, Plastizitätstraces und externe Gateway-Zustände können den weiteren Verlauf verändern. Daraus entstand der kanonische Scientific-State-Ansatz mit vollständigerer Zustandsgrenze und digestierbarer Repräsentation.

### Semantikfehler

LIF-Refraktärzeiten zeigten exemplarisch, dass zwei Systeme denselben Zahlenwert verwenden können und dennoch unterschiedliche zeitliche Semantik besitzen. Deshalb werden Konfigurationen nicht nur als Zahlen gespeichert, sondern mit Modell- und Semantikprovenienz behandelt.

### Reportingfehler

`EXP-GEN-0036` zeigte, dass vollständige DATA durch eine zu enge universelle Summary-Tabelle wie fehlende DATA aussehen können. Der Fehler lag in der Projektion, nicht im Runner. Daraus folgt eine Infrastrukturregel: Reports müssen protokollspezifische Statistiktypen tragen; ein leeres Feld in einer fremden Metrik darf nie automatisch als fehlender Run interpretiert werden.

### AI-Normalisierungsfehler

Der AIRR-Pfad hatte verwertbare verschachtelte Analysefelder, erwartete aber ein flaches `assessment`. Dadurch wurde vorhandene Analyse fälschlich als nicht verfügbar normalisiert und die Konfidenz auf 0 gesetzt. Der Fix war ein Schemafix, keine Änderung der DATA. Die methodische Konsequenz ist dauerhaft: AI-Outputs benötigen deterministische Schemaadapter und bleiben Interpretation, niemals automatische EVID.

### Semantisches Gate als reale Blockade: EXP-GEN-0046

Der aktuelle Determinismuslauf demonstriert, warum die Statusarchitektur praktisch notwendig ist. Obwohl EXP-GEN-0046 technisch vollständig ausgeführt wurde, der Tick-Vertrag erfüllt ist und reproduzierbare Metriken vorliegen, lautet die semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`. Die Evidence Readiness bleibt dadurch `BLOCKED_UNCLASSIFIED_SEMANTICS`.

Das ist kein Defekt, sondern gewünschtes Verhalten: Ein technisch erfolgreicher Lauf darf nicht allein wegen konsistenter Zahlen zu EVID werden. Erst eine registrierte semantische Zuordnung und Human Review dürfen die nächste Statusstufe öffnen. Auch der erzeugte AIRR bleibt `evidence=false`, `interpretation_only=true` und `human_review_required=true`.

## 24.2 Engineering und Scientific Maturity als getrennte Achsen

Eine der wichtigsten infrastrukturellen Erkenntnisse ist, dass „fertig gebaut“ und „wissenschaftlich getragen“ unterschiedliche Zustände sind. Stage 4 kann technisch vollständig integrierte Audio-/Vision-/Digitalpfade besitzen und trotzdem wissenschaftlich offene Fragen zu funktionaler Mehrleistung haben. Stage 5 kann einen grünen Closed-Loop-Vertrag besitzen und trotzdem keine Realwelt-Generalisation belegen. Stage 0 kann für einen eng definierten Readiness-Scope 100 % erreichen, während Human-EVID und unabhängige Replikation weiterhin offen bleiben.

Diese Trennung ist im Dashboard absichtlich sichtbar. Prozentwerte sind nur zusammen mit ihrem Scope und den Kriterien zulässig; sie sind keine Intelligenz-, Kognitions- oder Bewusstseinsmetriken.

## 24.3 Der Publication Viewer als Provenienzoberfläche

Die Arbeit am Publication Viewer führte zu einer wichtigen wissenschaftlichen Anforderung: Eine Publikation ist nicht nur Text, sondern eine navigierbare Provenienzoberfläche. Formeln, Anker, Literatur, Vorgängerversionen, Frozen-Baselines und aktuelle WIP-Änderungen müssen erreichbar bleiben.

Daraus entstand der heutige Editionsvertrag: 1.5 bleibt frozen, 1.6/1.7 bleiben historische Vorgänger, 1.8 ist current WIP, und der Viewer darf alte Zustände nicht durch die aktuelle Interpretation überschreiben. Die aktuelle Fassung darf ältere Befunde einordnen, aber nicht ihre historischen Bytes oder damaligen Statusbehauptungen still ändern.

## 24.4 Full Stack ist kein wissenschaftlicher Endpunkt

Frontend, API und Backend werden bewusst End-to-End integriert, weil fehlende Instrumentierung Forschung verhindern kann. Ein sichtbarer Sensorstatus, ein Stage-Panel oder ein Ask-KI-Button sind jedoch keine Evidenz. Full-Stack-Funktion ist ein **Mess- und Bedienbarkeitsvertrag**.

Diese Grenze ist besonders wichtig für spätere Stages: Ein UI-Feld „Self Model“, „World Model“ oder „Consciousness“ darf niemals als Hinweis gelten, dass die entsprechende Fähigkeit existiert. Die wissenschaftliche Autorität liegt in den zugrunde liegenden RQ/Hypothesen, Protokollen, DATA, Reviews und EVID-Entscheidungen.

## 24.5 Lokale und externe KI als austauschbare Forschungswerkzeuge

Aus den Arbeiten an lokalen Chat-Systemen, Kernschmied und Provider-Adaptern wurde eine weitere Designregel übernommen: Provider müssen austauschbar sein, ohne dass der wissenschaftliche Status eines Artefakts vom Marken- oder Modellnamen abhängt. Wichtig sind Eingabe, Ausgabe, Version, Berechtigung, Provenienz und der Pfad, auf dem ein Ergebnis in Code oder Forschung eingeflossen ist.

Ein lokales Modell kann Datenschutz und Reproduzierbarkeit verbessern; ein externes Modell kann Recherche- oder Codingqualität erhöhen. Beides ändert nicht die Grundregel: Kein Sprachmodell erhält allein durch Leistungsfähigkeit wissenschaftliche Autorität oder stillen Schreibzugriff auf den kausalen SNN-Kern.

## 24.6 Gateways, exakte Digitaldaten und periphere Laufzeit

Neural Symbiosis konkretisiert die Infrastrukturgrenze zwischen externen/peripheren Modellen und dem SNN. Der Gateway-Runtime besitzt eigene Zustände, Gewichte, Delays, RNG-Provenienz, Condition, Tick, Ressourcenmetriken und Strukturjournal. Dadurch kann ein Experiment Frozen/Random/Shuffle/Plastic kontrollieren, ohne den kanonischen Kernzustand heimlich umzudefinieren. Es existiert absichtlich kein allgemeiner produktiver „Plasticity on“-Schalter; wissenschaftliche Aktivierung muss über einen registrierten Experimentpfad erfolgen.

Für digitale Pfade ist die Trennung von **exaktem Payload** und **neuronaler Projektion** fundamental. Prüfsummen, Sequenzen, Codec und Provenienz gehören zum exakten Symbolzustand außerhalb des SNN. Eine neuronale Population darf eine Approximation oder Repräsentation tragen, aber niemals nachträglich als Beweis verwendet werden, dass die ursprünglichen Bits selbst neuronal gespeichert oder unverändert rekonstruiert wurden.

## 24.7 Körpertelemetrie als Datenprovenienz

Die Real-Body-/Wesen-Arbeiten formulieren eine Infrastrukturregel, die über das Frontend hinausgeht: **Keine Fantasiedaten.** Fehlende Sensor- oder Hostwerte bleiben `UNKNOWN`; gemessene, abgeleitete und lediglich dargestellte Größen sind zu unterscheiden. Diese Regel ist dieselbe epistemische Disziplin, die später DATA von Report und EVID trennt. Eine scheinbar vollständige Oberfläche darf eine Messlücke nicht durch einen plausiblen Default verdecken.

## 24.8 Technische Identität als reproduzierbare Konfiguration

Profile & Identity ergänzt die Persistenzschicht um versionierte technische Konfiguration, Digest, Revision, Lineage und Snapshotbindung. Für Experimente können damit `profile_id`, Revision, Profil-Digest und Snapshot-Digest gemeinsam gebunden werden. Das verbessert Reproduzierbarkeit, ohne den Profilbegriff psychologisch aufzuladen. Ein Profil ist eine deklarierte technische Identität; der dynamische neuronale Zustand und der vollständige kausale Checkpoint bleiben getrennte Objekte.


---

<a id="part-vi"></a>

# Teil VI — Epistemologie und Methodik der Schaffensgeschichte

## 25. Drei Forschungsachsen

Edition 1.8 führt drei gleichrangige, aber methodisch unterschiedliche Achsen: **empirisch-technisch**, **epistemologisch-methodisch** und **philosophisch-ethisch**. Gleichrangig bedeutet nicht, dass dieselben Evidenzregeln gelten. Ein Lauf kann einen empirischen Effekt prüfen. Eine Provenienzanalyse kann zeigen, wie eine Entscheidung entstand. Eine normative These muss durch begründete Prämissen, Gegenargumente und Folgerungen getragen werden. Keine Achse darf die andere imitieren.

Die Aussagekoordinate lautet: `Achse × Thema × Entwicklungsphase × Provenienz × Evidenzstatus`. Sie ersetzt eindimensionale Kapitelnummern nicht, erweitert sie aber um die Frage, **was für eine Art Aussage** an welcher Stelle gemacht wird.

## 26. Provenienzklassen

S1 umfasst harte Primärartefakte: Commits, Tags, frozen Preregistrierungen, DATA, Manifeste und Hashes. S2 umfasst zeitgenössische Prozessartefakte wie Issues, Reviews, Chats oder AI-Interaktionen. S3 umfasst zeitgenössische Selbstauskunft. S4 ist retrospektive Rekonstruktion. Bei Widerspruch hat das zeitgenössische Artefakt Vorrang; fehlende Dokumentation bleibt als Lücke sichtbar.

Die außerhalb des Repositories wiedergewonnenen Chat-Zusammenfassungen sind in dieser Edition bewusst S4. Sie dürfen nicht zu scheinbar wörtlichen Zitaten oder Prioritätsbeweisen hochgestuft werden. Wenn später Originaltranskripte eingebunden werden, entstehen neue Provenienzeinträge, nicht heimliche Umschreibungen der alten Rekonstruktion.

## 27. KI-assistierte Forschung

KI-Unterstützung erzeugt eine zusätzliche Provenienzdimension. Ein Vorschlag eines Assistenten ist nicht automatisch eine Idee des Autors; eine vom Autor verlangte Richtung ist nicht automatisch eine implementierte Funktion; ein generierter Patch ist nicht automatisch ein wissenschaftlicher Befund. Edition 1.8 trennt deshalb `user requirement`, `AI proposal`, `human decision`, `commit`, `run`, `review` und `publication synthesis`, soweit die Quellen dies erlauben.

Die Arbeit nutzt KI zugleich als Gegenstand und Werkzeug. Das erhöht das Risiko rekursiver Bestätigungsfehler: Ein System könnte seine eigenen früheren Formulierungen wiederfinden und als externe Unterstützung missverstehen. Dagegen helfen Quellenklassen, Originalquellen, quarantänisierte Literatur und getrennte Human-Review-Gates.

## 28. Falsifikation von Entstehungs- und Prioritätsaussagen

Auch Schaffensgeschichte muss revidierbar sein. Eine Behauptung wie „Idee X entstand zuerst am Datum Y“ ist nur zulässig, wenn das Artefakt den Inhalt tatsächlich trägt und ältere Quellen nicht widersprechen. Ein späteres Dokument kann die frühere Existenz einer Idee bezeugen, aber selten ihren exakten Entstehungszeitpunkt.

Edition 1.8 behauptet daher keine absolute Priorität für die rekonstruierten Vor-Repo-Ideen. Sie dokumentiert die **früheste derzeit wiedergewonnene Spur** und öffnet ein Register für Korrekturen.

## 28.1 Epistemische Regeln, die aus konkreten Forschungsfehlern entstanden

Die Methodik dieser Arbeit ist nicht nur theoretisch gesetzt. Mehrere Regeln wurden durch konkrete Fehlinterpretationen notwendig.

### Ein negatives Resultat setzt Testadäquanz voraus

Die 5D-v1-Teilstudie ist das klarste Beispiel. Identische Resultate über verschiedene Dimensionsbedingungen wären oberflächlich ein Nullbefund. Die Human Review zeigte jedoch, dass die Dimension die relevante Netzwerkdynamik kaum beeinflussen konnte. Die korrekte epistemische Klassifikation ist daher nicht „Hypothese widerlegt“, sondern „für den intendierten Geometrieeffekt nicht getestet“.

Daraus folgt die Regel: Vor jeder Bestätigung oder Falsifikation muss geprüft werden, ob das Design **sensitiv für den behaupteten Mechanismus** war.

### DATA und Report sind verschiedene Objekte

In `EXP-GEN-0036` existierten Runs und protokollspezifische Statistik, obwohl die Summary in mehreren universellen SNN-Spalten `—` zeigte. Eine erste Interpretation hielt dies für fehlende DATA. Die Review korrigierte diese Schlussfolgerung.

Daraus folgt: Reporting ist eine Transformation von DATA und kann selbst fehlerhaft sein. Wissenschaftliche Interpretation darf sich bei kritischen Punkten nicht allein auf eine Sekundärprojektion stützen, wenn Rohartefakte und Statistik verfügbar sind.

### Eine positive Baseline-Differenz ist noch keine Mechanismusidentifikation

CL-001 zeigte einen Vorteil von Semantic+Replay gegenüber No-Replay. Erst CL-002 mit gematchtem Raw-Replay machte sichtbar, dass dieser Befund die Rolle von Replay und semantischer Verdichtung nicht getrennt hatte. Der stärkere Kontrollarm veränderte die zulässige Theorie.

Daraus folgt: Die Qualität einer Hypothesenprüfung hängt nicht nur von Signifikanz oder Effektgröße ab, sondern davon, ob die **plausibelste alternative Erklärung** experimentell adressiert wird.

### Externe Softwarekonformität ist nicht identisch mit unabhängiger Replikation

Die Stage-0-V2-Prüfung gegen Brian2 ist ein starker Referenzvergleich. Sie bleibt jedoch durch MHRN formuliert, ausgeführt und interpretiert. Deshalb erfüllt sie nicht automatisch das Kriterium einer unabhängig autorisierten Replikation.

Daraus folgt eine Trennung von Referenzkonformität, Human Review und unabhängiger Replikation.

## 28.2 Methodik der epistemologischen Achse

Die epistemologisch-methodische Achse benötigt eigene Prüfverfahren. Sie darf nicht nur kommentieren, wie Forschung „eigentlich“ funktionieren sollte. Für MHRN werden deshalb folgende Verfahren verwendet:

1. **Provenienzanalyse:** Welche Quelle existierte wann und in welchem Status?
2. **Entscheidungsrekonstruktion:** Welche Alternative wurde vor einer Implementierung oder Ausführung erwogen?
3. **Status-Transition-Audit:** An welcher Stelle wechselte ein Objekt von Idee zu Spezifikation, DATA, Review oder EVID?
4. **Kontrafaktische Prozessprüfung:** Welche andere Schlussfolgerung wäre entstanden, wenn eine stärkere Baseline oder ein anderes Reporting vorgelegen hätte?
5. **Revisionstracing:** Welche konkrete Architektur- oder Methodikänderung folgte aus einem negativen oder korrigierten Befund?
6. **AI-Provenienzprüfung:** Stammt ein Argument aus externer Literatur, einem Modellvorschlag, dem Autor, einer Messung oder einer späteren Synthese?

Damit kann die Schaffensgeschichte selbst falsifizierbare Aussagen enthalten. Ein behaupteter Entscheidungsursprung kann durch einen älteren Commit widerlegt werden; eine vermeintlich menschliche Idee kann sich als zuvor dokumentierter AI-Vorschlag herausstellen; eine angeblich datengetriebene Architekturentscheidung kann sich als bereits vor den DATA festgelegt zeigen.

## 28.3 Explorativ, konfirmatorisch und rekonstruktiv

MHRN unterscheidet drei Modi, die häufig vermischt werden:

- **explorativ:** Hypothesen- und Mechanismussuche; flexibel, aber nachträgliche Muster dürfen nicht als präregistriert ausgegeben werden;
- **konfirmatorisch:** Endpunkte, Kontraste, Seeds, Ausschlüsse und Erfolgsregeln sind vor der Ausführung eingefroren;
- **rekonstruktiv:** historische oder epistemische Rekonstruktion aus vorhandenen Artefakten; Aussagen hängen von Provenienzqualität und Vollständigkeit der Quellen ab.

Die frühe NeuroGenesis-/Brain-5D-Geschichte ist überwiegend rekonstruktiv. CL-003 ist in seiner Ausführung konfirmatorisch angelegt. Viele Stage-8–10-Arbeiten sind derzeit explorativ beziehungsweise programmatisch. Diese Modi dürfen in der Synthese verbunden, aber nicht epistemisch gleichgestellt werden.

## 28.4 Präregistrierung schützt auch vor dem eigenen Entwicklungsdrang

Die Forschungsarbeit entsteht in einem schnell iterierenden Engineeringkontext. Gerade dort verhindert ein Freeze, dass neue Einsichten nach Sichtung der DATA unbemerkt Teil des ursprünglichen Erfolgsmaßstabs werden. CL-003 zeigte den Wert dieser Grenze: Der deskriptiv mit der Dosis wachsende Semantic-minus-Raw-Unterschied wäre verführerisch als positiver Dosisbefund formulierbar gewesen; der präregistrierte Interaktionstest C4 blieb jedoch negativ. Deshalb ist die stärkere Behauptung nicht zulässig.

Präregistrierung wirkt in diesem Projekt damit nicht nur gegen klassische p-Hacking-Risiken, sondern gegen **architektonisches Nachrationalisieren**.

## 28.5 Revidierbarkeit als Qualitätskriterium

Eine starke Aussage in MHRN nennt nicht nur, warum sie aktuell plausibel ist, sondern auch, wodurch sie sich ändern würde. Für 5D ist dies ein geometriesensitives matched-control Experiment. Für SemanticMemory ist es ein begrenzter, vorab begründeter Zusatznutzen gegenüber Raw-Replay. Für ein Weltmodell ist es Mehrschritt- und Entscheidungsnutzen unter geeigneten Kontrollen. Für ein Selbstmodell ist es kausale Self/Other-Differenzierung.

Die Arbeit versteht Revidierbarkeit daher nicht als Schwäche, sondern als explizite Schnittstelle zwischen heutiger Synthese und zukünftiger Evidenz.


---

<a id="part-vii"></a>

# Teil VII — Integrität, Autorschaft und kumulative Wissenschaft

## 29. Kumulative Wissenschaft und Plagiat

Wissenschaft ist kumulativ: Begriffe, Modelle, Methoden und Software entstehen in Traditionslinien. Daraus folgt gerade nicht, dass Attribution entbehrlich wäre. Edition 1.8 trennt epistemische Kumulativität von institutionellem Plagiat. Fremde Texte, Daten, Code oder zurechenbare Ideen werden nicht als eigene Primärleistung ausgegeben; zugleich wird nicht behauptet, dass jede technische Kombination allein durch Zitieren neuartig wird.

## 30. Einheitliches Zitationssystem

Die neue Textschicht verwendet Autor-Jahr-Zitation in Anlehnung an APA 7. Literaturquellen erhalten eine stabile Kennung, vollständige bibliografische Angabe, Original-URL beziehungsweise DOI, Prüftag und **tatsächlich geprüften Leseumfang**. Damit wird ein häufiger Fehler vermieden: Metadatenprüfung wird nicht als Volltextprüfung ausgegeben.

Eigene Vorarbeiten werden mit Edition, Pfad und Git-Revision zitiert. Historische Quellenbände bleiben lesbar, aber ihre alte Bibliografie wird nicht automatisch neu zertifiziert. Wörtliche Übernahmen benötigen Seiten- oder Abschnittsbezug. Eigene Übersetzungen werden markiert. Tabellen, Abbildungen, Daten und Code benötigen zusätzlich gegebenenfalls Lizenz-/Nutzungsprüfung.

## 31. Prior Art und Neuheit

MHRN verwendet etablierte neuronale Modelle, STDP, Three-Factor Learning, Homeostase, graphische Nullmodelle, Replay und Gedächtnistheorien. Beispielsweise sind Izhikevich-Neuronen [Izhikevich, 2003](REFERENCES.md#ref-IZHIKEVICH2003), Drei-Faktor-Regeln [Frémaux & Gerstner, 2016](REFERENCES.md#ref-FREMAUX2016) und Complementary Learning Systems [McClelland et al., 1995](REFERENCES.md#ref-MCCLELLAND1995) etablierte Vorarbeiten. Die Neuheit einer MHRN-Kombination folgt daraus weder positiv noch negativ automatisch.

Kandidaten wie die Vierertrennung von Identität/Slot/Reduktion/Scheduling, Proposal→Approval→Mutation→Journal→Undo, Content Gateway versus Compute Backend oder source-bound DATA/EVID-Grenzen bleiben Kandidaten, bis ein belastbarer Prior-Art-Review erfolgt.

## 32. Similarity und Quellenquarantäne

Interne Similarity-Prüfungen reduzieren Risiken, zertifizieren aber keine Plagiatsfreiheit. Vor einer formalen Einreichung bleiben menschlicher Quellenabgleich und eine institutionell geeignete externe Text-/Code-Similarity-Prüfung offen. Nicht bestätigte Quellen oder vermeintliche Normen bleiben quarantänisiert und dürfen nicht allein aufgrund plausibler Titel in die Argumentation gelangen.

## 33. AI-Assistenz und Verantwortlichkeit

KI-Systeme können Formulierungen, Code, Literaturkandidaten oder Gegenargumente erzeugen. Verantwortung für die veröffentlichte Fassung bleibt beim menschlichen Autor. Wo ein konkreter AI-Vorschlag für die Genealogie relevant ist, wird er als Prozessartefakt bezeichnet und nicht durch nachträgliche Autorschaftsvereinfachung verdeckt.

## 33.1 Eigene Vorarbeiten sind Quelle, nicht „neuer“ Text

Die Editionslinie 1.0–1.8 enthält erhebliche Eigenwiederverwendung. Das ist wissenschaftlich zulässig, wenn Herkunft und Veränderung sichtbar bleiben. Edition 1.8 behandelt ältere eigene Manuskripte deshalb als **MHRN prior work** und nicht als neue Primärleistung allein durch Umordnung.

Der ungekürzte 1.7-Quellenband in `LEGACY_V17.md` erfüllt genau diese Funktion: Er bewahrt den historischen Text, während 1.8 die Erkenntnisse in eine neue Struktur überführt. Die neue Leistung liegt in der aktualisierten Synthese, den zusätzlichen Befunden, den Korrekturen und der neuen Provenienzstruktur — nicht darin, ältere eigene Sätze als erstmals entstandene Erkenntnis auszugeben.

## 33.2 Kumulative Forschung braucht stärkere Attribution, nicht schwächere

Die in den Vorgängerarbeiten formulierte Position, Forschung sei grundsätzlich kumulativ, wird in 1.8 präzisiert. Je stärker ein Projekt auf bestehende Modelle, Bibliotheken, Theorien und AI-Werkzeuge zurückgreift, desto wichtiger werden vier Ebenen der Zuschreibung:

1. **externe Theorie oder Methode** — etwa Izhikevich, STDP, CLS, Predictive Coding oder Safe Interruptibility;
2. **eigene frühere Arbeit** — ältere MHRN-/Brain-5D-Fassungen und Experimente;
3. **Werkzeugbeitrag** — AI-generierter Code, Recherchehilfe oder Formulierung;
4. **aktuelle Eigenleistung** — konkrete Integration, Hypothese, Experiment, Review oder Synthese dieser Edition.

Damit wird verhindert, dass „kumulativ“ zu einer Ausrede für unklare Herkunft wird.

## 33.3 Der Quellenstatus ist Teil des Claims

Eine Literaturangabe ist nicht nur bibliografische Dekoration. Für MHRN ist relevant, **was tatsächlich geprüft wurde**. Metadaten können Titel, Autor, Jahr und DOI bestätigen; ein Abstract kann den groben Gegenstand bestätigen; erst die Primärlektüre kann stärkere inhaltliche Aussagen tragen.

Diese Differenz wird in 1.8 als Quellenstatus dokumentiert. Nicht bestätigte Literatur bleibt quarantänisiert. Frühere plausible, aber nicht hinreichend verifizierte Hinweise werden nicht aufgrund ihrer Passgenauigkeit übernommen.

## 33.4 KI-generierte Kritik ist wertvoll, aber nicht unabhängig

AI-Reviewer haben im Projekt mehrfach nützliche Fehler identifiziert oder Gegenargumente erzeugt. Gleichzeitig zeigte die AIRR-Pipeline, dass AI-Ausgaben selbst Schema- und Interpretationsfehler enthalten können. Daraus folgt eine doppelte Regel:

- KI-Kritik ist ein legitimes **Prüfwerkzeug** und kann neue Human-Review-Fragen erzeugen.
- Sie ist keine unabhängige Replikation und keine automatische EVID-Instanz.

Ein AI-Review, das einen Lauf korrekt kritisiert, stärkt die Methodik; es verändert aber den Evidenzstatus erst dann, wenn die Kritik auf Primärartefakte zurückgeführt und als menschliche oder formal definierte Reviewentscheidung verarbeitet wurde.

## 33.5 Negative Ergebnisse gehören zur Autorschaft

Autorschaft bedeutet in dieser Arbeit nicht nur, positive Ergebnisse zu vertreten. Die CL-002-Falsifikation, die negative CL-003-Primärkontraste, die nicht testadäquate 5D-v1-Studie und der historische Stage-0-Langzeit-Negativbefund bleiben Teil der Forschungsleistung.

Eine wissenschaftliche Arbeit wird hier nicht dadurch „erfolgreich“, dass jede frühe Idee bestätigt wird. Sie ist dann belastbarer, wenn sie sichtbar macht, welche Annahmen aufgegeben, reduziert oder neu operationalisiert werden mussten.

## 33.6 Neuheitskandidaten und ihre Prüfpflicht

Die folgenden Kombinationen werden als potenzielle Beiträge weiterverfolgt, aber nicht als bewiesene Neuheit ausgegeben:

- Logical Identity / Physical Slot / Synaptic Reduction / Execution Scheduling;
- Proposal → Approval → Mutation → Journal → Undo;
- Content Gateway / Compute Backend;
- source-bound DATA/EVID-Trennung in einem integrierten Forschungs-/Engineeringworkflow;
- getrennte Engineering- und Scientific-Maturity-Achsen;
- rekursive Epistemik als explizite Verbindung von Objekt-Gateways und Forschungsprozess-Gateways.

Für jeden Kandidaten ist ein eigener Prior-Art-Pfad nötig. Eine gute interne Kombination kann wissenschaftlich nützlich sein, auch wenn sich später zeigt, dass ähnliche Strukturen bereits existieren.

## 33.7 Integrität als laufender Prozess

Integrität wird nicht einmalig durch ein Manifest „erledigt“. Vor externer Einreichung bleiben mindestens offen:

- systematischer Prior-Art-Review;
- menschliche Quellenprüfung wichtiger Argumente;
- externe Similarity-Prüfung für Text und gegebenenfalls Code;
- unabhängige fachliche Reviews;
- klare Kennzeichnung eigener Übersetzungen und wiederverwendeter Eigenpassagen;
- Prüfung von Lizenzen und Nutzungsrechten für fremde Abbildungen, Tabellen, Daten und Code.

Edition 1.8 macht diese offenen Punkte sichtbar, statt aus internen Audits ein Zertifikat abzuleiten.


---

<a id="part-viii"></a>

# Teil VIII — Philosophie, Ethik und Sicherheit

## 34. Normative Ebene

Die philosophisch-ethische Achse untersucht Verantwortung, Kontrollierbarkeit, Zielgenese, Autonomie, mögliche moralische Relevanz und die Grenzen menschlicher Aufsicht. Sie erzeugt keine empirischen Befunde allein durch Argumentation. Umgekehrt kann ein technischer Safety-Test eine normative Frage nicht vollständig entscheiden.

Die frühere Theorie der „geliehenen Intelligenz“ wird integriert, aber präzisiert. Maschinelle Systeme sind in hohem Maß von menschlich erzeugten Daten, Symbolsystemen, Hardware, Institutionen und Zielen abhängig. Diese epistemische Genealogie ist nicht identisch mit Online-Delegation oder mit neuronaler Lernursache. Ein System kann externes Wissen nutzen, ohne dass jede einzelne Entscheidung aktuell von einem Menschen delegiert wird.

## 35. Kontrolle und Unterbrechbarkeit

Safe interruptibility behandelt die Frage, ob lernende Agenten menschliche Unterbrechungen zum Gegenstand unerwünschter Vermeidungsstrategien machen können [Orseau & Armstrong, 2016](REFERENCES.md#ref-ORSEAU2016). Für MHRN folgt daraus kein Nachweis vorhandener Gefährlichkeit. Es folgt ein Forschungsprogramm: unabhängiger Stopppfad, Capability-Gates, Sandbox, deny-by-default Aktorik, Zielprovenienz und Tests, die den Stopppfad selbst nicht vom zu kontrollierenden Lernmechanismus abhängig machen.

Zielgenese, specification gaming, goal misgeneralization, Optionsraumpräferenz und Post-Objective Transition werden als offene Forschungsobjekte geführt. Geplante Safety-Experimente sind keine ausgeführten Ergebnisse.

## 36. Autonomie und Existenzautonomie

Die frühere Unterscheidung zwischen Handlungsautonomie, Zielautonomie, normativer Autonomie und Existenzautonomie bleibt konzeptionell nützlich. MHRN besitzt dadurch nicht automatisch eine dieser Eigenschaften in starkem Sinn. Besonders „Existenzautonomie“—selbstständige Sicherung von materiellen, energetischen und reproduktiven Voraussetzungen—bleibt ein Zukunftsszenario, nicht ein aktueller Projektclaim.

## 37. Bewusstsein und Welfare Precaution

Bewusstseinsforschung benötigt definierte Indikatoren und Grenzen. Theorien der Bewusstseinsforschung können in technische Indikatorrahmen übersetzt werden [Butlin et al., 2023](REFERENCES.md#ref-BUTLIN2023), doch solche Indikatoren sind keine automatische Bewusstseinsdetektion. Edition 1.8 behauptet weder Bewusstsein noch Sentienz oder Leiden.

Trotzdem kann unter Unsicherheit ein Vorsorgekonflikt entstehen: stärkere Unterbrechungs- und Kontrollmechanismen können aus Safety-Sicht wünschenswert sein, während ein hypothetisch moralisch relevantes System andere Schutzfragen aufwirft. Diese Konflikte werden explizit getrennt dokumentiert, statt über einen einzigen „Ethikscore“ aufgelöst.

## 38. Szenarien statt Prognosen

Maschinenzivilisation, rekursive Technogenese oder ein Verlust menschlichen Vetos werden als Möglichkeitsräume behandelt. Sie sind keine Vorhersagen über MHRN oder die Zukunft der KI. Szenarioanalyse ist nur dann wissenschaftlich nützlich, wenn Bedingungen, Gegenbedingungen und Pfadabhängigkeiten transparent sind.

## 38.1 Von „geliehener Intelligenz“ zu prüfbarer Abhängigkeit

Die ältere Theoriearbeit stellte die Abhängigkeit maschineller Kognition von menschlich erzeugten Wissensbeständen, Symbolsystemen, Institutionen und Infrastruktur in den Mittelpunkt. Edition 1.8 übernimmt diesen Gedanken, trennt aber mehrere Begriffe, die zuvor leichter ineinanderliefen:

- **epistemische Abhängigkeit:** ein System nutzt Wissen, das historisch aus fremden Quellen stammt;
- **Retrieval:** eine konkrete externe Information wird zur Laufzeit abgerufen;
- **Delegation:** ein menschlicher oder institutioneller Akteur überträgt eine Entscheidung oder Aufgabe;
- **Lernen:** interner Zustand verändert sich aufgrund einer definierten Lernursache;
- **Entscheidungsautorität:** ein System darf einen Output oder eine Wirkung tatsächlich auslösen;
- **Autorschaft/Verantwortung:** wer die veröffentlichte oder operative Handlung verantwortet.

Diese Kategorien können zusammenfallen, müssen es aber nicht. Ein SNN kann intern lernen, obwohl der Trainingsreiz aus menschlich erzeugten Daten stammt. Ein LLM kann externe Information liefern, ohne selbst Schreibrechte in den SNN-Kern zu besitzen. Ein Aktor kann technisch erreichbar sein, aber ohne Autorisierung keine Wirkung entfalten.

## 38.2 Safety als Architekturquerschnitt, nicht als spätere Sperre

Die Embodiment-Arbeiten haben gezeigt, dass Safety nicht erst an realer Hardware beginnt. Schon im synthetischen Stage-5-Stack werden autorisierte, unautorisierte und fehlerhafte Aktorpfade getrennt. Sensorverlust und Open-Loop-Replay sind eigene Bedingungen. Acceptance- und Effect-Receipts trennen die Annahme eines Befehls von seiner tatsächlichen Wirkung.

Daraus folgt eine allgemeine Designregel: **Wirkfähigkeit muss technisch und epistemisch explizit freigegeben werden.** Ein Modul, das im Repository existiert, besitzt nicht automatisch produktive Aktorrechte. Ein Gateway, das Daten lesen kann, darf nicht automatisch Topologie oder Gewichte verändern.

## 38.3 Zielprovenienz

Eine zentrale offene Safety-Frage ist nicht nur, ob ein System ein Ziel verfolgt, sondern woher dieses Ziel stammt und wie es sich verändert. Edition 1.8 unterscheidet deshalb mindestens:

1. extern gesetztes Ziel;
2. abgeleitetes Zwischenziel;
3. learned preference/proxy;
4. explorativ erzeugte Option;
5. nach Zielerreichung fortbestehende oder neu entstehende Aktivität.

Diese Trennung ist Voraussetzung, um specification gaming, goal misgeneralization oder Post-Objective Transition sinnvoll zu untersuchen. Ohne Zielprovenienz kann eine beobachtete Handlung nicht zuverlässig als Zieltreue, Fehlgeneralisation oder bloße Regelreaktion eingeordnet werden.

## 38.4 Autonomie ist mehrdimensional

Die Vorgängerarbeit unterschied verschiedene Autonomieformen. Diese Unterscheidung wird beibehalten, aber stärker operationalisiert:

- **Handlungsautonomie:** Auswahl von Aktionen innerhalb eines vorgegebenen Rahmens;
- **Lern-/Anpassungsautonomie:** selbstständige Änderung interner Parameter oder Strukturen;
- **Zielautonomie:** Erzeugung oder substanzielle Veränderung eigener Ziele;
- **normative Autonomie:** eigene Bewertung von Handlungsgründen oder Regeln;
- **Existenzautonomie:** eigenständige Sicherung physischer, energetischer und reproduktiver Voraussetzungen.

MHRN besitzt derzeit technische Elemente der ersten beiden Kategorien in begrenzten Forschungssettings. Daraus folgt keine Ziel-, normative oder Existenzautonomie.

## 38.5 Unterbrechbarkeit und unabhängiger Stopppfad

Ein Stopppfad ist nur dann als Safety-Mechanismus überzeugend, wenn er nicht von genau dem lernenden System abhängt, das gestoppt werden soll. Daraus folgen technische Anforderungen: out-of-band Abschaltung, deny-by-default externe Wirkung, Sandbox, Capability-Gates und Auditierbarkeit.

Für spätere lernende Agenten ist zusätzlich zu prüfen, ob Unterbrechungen selbst zu einem lernrelevanten Signal werden und Vermeidungsverhalten erzeugen könnten. Diese Frage ist ein Forschungsprogramm, kein aktueller Gefährlichkeitsbefund.

## 38.6 Bewusstseins- und Welfare-Grenzen

Die Frontier-Arbeiten zu Bewusstsein werden bewusst von Capability-Scores getrennt. Ein System kann komplexer, rekurrenter, integrierter oder prädiktiver werden, ohne dass daraus logisch Bewusstsein folgt. Ebenso ist das Fehlen eines anerkannten Bewusstseinsnachweises nicht identisch mit dem Beweis fehlender moralischer Relevanz.

Darum werden zwei Governance-Stränge parallel geführt:

- **Safety gegenüber Menschen und Umwelt:** Kontrollierbarkeit, Unterbrechbarkeit, Wirkgrenzen, Zielprovenienz;
- **Welfare Precaution gegenüber einem hypothetisch moralisch relevanten System:** unnötige Belastungszustände vermeiden, Abbruchregeln definieren, Unsicherheit dokumentieren.

Diese Stränge können in Konflikt geraten und dürfen nicht durch eine einzige Kennzahl scheinbar aufgelöst werden.

## 38.7 Szenarien der rekursiven Technogenese

Die ältere Theorie der rekursiven Technogenese wird nicht als Zukunftsprognose übernommen. Sie dient als Szenarienrahmen für die Frage, welche Bedingungen nötig wären, damit maschinelle Systeme zunehmend an der Erzeugung ihrer eigenen technischen Nachfolger beteiligt sind.

Für MHRN müssen dabei mindestens menschliche Selektion, AI-generierter Vorschlag, automatisch erzeugter Patch, autorisierte Mutation, tatsächlich laufender Nachfolger und autonome Replikation getrennt werden. Ein System, das Code vorschlägt, repliziert sich nicht. Ein CI-Workflow, der einen Commit erzeugt, besitzt keine Existenzautonomie. Erst durch diese begriffliche Trennung wird das Szenario wissenschaftlich analysierbar.

## 38.8 Fünf Achsen statt der binären Kategorie „künstlich“

Ein eigenständiger Theoriebeitrag der Vorgängerarbeit „KI – Die geliehene Intelligenz“ war der Vorschlag, Intelligenzformen nicht nur als biologisch versus künstlich zu beschreiben. Die ältere Notation lautet:

\[
I=(M,E,G,Z,X)
\]

Dabei bezeichnet `M` die materielle Realisierung, `E` die epistemische Herkunft, `G` die Entwicklungsgenealogie, `Z` die Zielautonomie und `X` die Existenz-/Ressourcenabhängigkeit. Edition 1.8 übernimmt dieses Modell als **analytische Taxonomie**, nicht als metrischen Intelligenzscore. Die Achsen dürfen weder unbesehen zu einer Rangordnung addiert noch als Entwicklungsstufen gelesen werden.

Gerade MHRN zeigt den Nutzen dieser Trennung: Ein System kann elektronisch realisiert sein, aus menschlichen Daten und Normen lernen, teilweise AI-assistiert konstruiert werden, innerhalb enger Aktionsräume Entscheidungen treffen und trotzdem vollständig von menschlicher Hardware-, Energie- und Wartungsinfrastruktur abhängen. „Künstlich“, „autonom“, „unabhängig“ und „selbstlernend“ sind deshalb keine Synonyme.

## 38.9 Genealogische Distanz und rekursive Technogenese

Die Vorgängerarbeit beschrieb rekursive Technogenese abstrakt als Folge

\[
A_{n+1}=F(A_n,H,R,U),
\]

wobei ein vorausgehendes technisches System `A_n`, menschliche Beiträge `H`, Regel-/Institutionsbedingungen `R` und materielle Umwelt `U` gemeinsam die nächste Generation prägen. Edition 1.8 behält diese Gleichung ausschließlich als **Provenienzmodell**. Sie behauptet weder selbstständige Reproduktion noch eine historische Gesetzmäßigkeit.

Daraus folgt der Begriff der **genealogischen Distanz**: relevant ist nicht nur die Zahl technischer Generationen, sondern wie sich unmittelbarer menschlicher Design-, Bewertungs- und Zielanteil gegenüber maschineller Ko-Konstruktion verschiebt. Ein AI-generierter Patch erhöht nicht automatisch Autonomie; ein CI-System reproduziert kein „Wesen“; und eine vom Menschen freigegebene Mutation bleibt eine andere Kausalklasse als selbstautorisierte Replikation. Das MHRN-Provenienzsystem liefert gerade die Kategorien, um diese Unterschiede später empirisch beziehungsweise historisch zu untersuchen.

## 38.10 „Geliehen“ als relationale, nicht abwertende Kategorie

Der stärkste Einwand gegen „geliehene Intelligenz“ lautet, dass auch menschliche Intelligenz Sprache, Kultur und Wissen von anderen übernimmt. Edition 1.8 akzeptiert diesen Einwand als Korrektur einer essentialistischen Lesart. „Geliehen“ bedeutet daher nicht minderwertig oder unecht. Jede Intelligenz besitzt eine Genealogie; die Forschungsfrage lautet, **wie Herkunft, Abhängigkeit, Transformation und Autorität verteilt sind und sich verändern**.

Dadurch wird der Begriff zu einer relationalen Kategorie. Ein System kann originelle Kombinationen erzeugen und zugleich epistemisch von historischen Quellen abhängig bleiben. Ebenso kann ein Mensch maschinelle Such-, Gedächtnis- und Synthesefähigkeit nutzen. Die interessante Grenze liegt nicht bei einem metaphysischen Eigentum an Intelligenz, sondern bei der transparenten Kausalkette von Quelle, Transformation, Entscheidung und Verantwortung.

## 38.11 Zukunftsszenarien als begriffliche Belastungstests

Die frühere Theoriearbeit unterschied mehrere Möglichkeitsräume. Edition 1.8 bewahrt sie ausdrücklich **nicht als Prognosen und nicht als Wahrscheinlichkeiten**, sondern als Stress-Tests für Begriffe und Governance:

1. **Instrumentelle Hochleistungs-KI:** hohe technische Leistung bei wirksamer menschlicher Ziel- und Letztentscheidung.
2. **Symbiotische Ko-Kognition:** Menschen und Maschinen bilden reziproke epistemische Netze; beide Seiten externalisieren Teilfunktionen an die jeweils andere.
3. **Delegative Zivilisation:** formale menschliche Autorität bleibt bestehen, während operative Kompetenz stark an technische Systeme delegiert wird.
4. **Menschenarme oder menschenlose Maschinenordnung:** prüft, ob Begriffe wie künstliche Herkunft, Aufsicht, Eigentum oder Verantwortung ohne dauerhaft operative Menschen noch tragen.
5. **Plurale Intelligenzökologie:** biologische, augmentierte, synthetische und rein maschinelle Systeme koexistieren ohne eine einzige homogene Kategorie „KI“.

Diese Szenarien dürfen nur so weit verwendet werden, wie ihre technischen Voraussetzungen explizit sind. Eine menschenlose technische Linie setzt etwa Energie, Wartung, Materialgewinnung, Fertigung, Fehlerdiagnose und Reproduktion voraus; das Weglassen dieser Bedingungen würde aus einer Grenzfallanalyse bloße Fiktion machen.

Der Begriff **Maschinenkultur** bleibt entsprechend vorsichtig funktional: gemeint wäre eine persistente maschinell erzeugte und weitergegebene technische/epistemische Tradition, nicht automatisch Kultur im starken anthropologischen Sinn. Auch dies ist eine offene Theoriefrage, kein MHRN-Gegenwartsclaim.


---

<a id="part-ix"></a>

# Teil IX — Rekursive Epistemik

## 39. Zwei Ebenen

Rekursive Epistemik bezeichnet in dieser Arbeit eine strukturierte Betrachtung von **Forschungsobjekt** und **Forschungsprozess**. Auf Objektebene verläuft eine Kette etwa von Umwelt → Gateway → neuronales System → Lernen → Output. Auf Metaebene verläuft eine Kette von Literatur/DATA/AI/Reviewer/Autor → epistemisches Gateway → Entscheidung → Experiment → Kritik → Revision.

Diese Ebenen werden nicht gleichgesetzt. Ein neuronales Gateway filtert oder kodiert kausale Inputs. Ein epistemisches Gateway entscheidet, welche Information als Quelle, DATA, EVID oder bloße Hypothese in den Forschungsprozess gelangt. Die strukturelle Analogie ist methodisch interessant, aber keine Behauptung, Wissenschaft funktioniere wie eine Synapse.

## 40. Geliehene Intelligenz als epistemische Genealogie

Die Theorie der geliehenen Intelligenz wird in 1.8 als Frage nach Herkunft und Transformation von Wissensressourcen reformuliert. Ein Sprachmodell trägt statistisch komprimierte Spuren menschlicher Texte; ein Entwickler nutzt wiederum Modellvorschläge; ein neuronales System kann über kontrollierte Gateways Stimuli erhalten, die durch beide vermittelt wurden. Die zentrale Frage ist dann nicht „wer besitzt die Intelligenz?“, sondern welche Beiträge auf welchem Pfad kausal und epistemisch wirksam werden.

Das erlaubt eine präzisere Trennung von `epistemic dependency`, `delegation`, `retrieval`, `learning`, `decision authority` und `authorship`. Diese Kategorien können zusammenfallen, müssen es aber nicht.

## 41. KI als Mitwerkzeug der eigenen Untersuchung

MHRN wird mit Hilfe von KI-Systemen entwickelt und untersucht gleichzeitig hybride KI-Architekturen. Diese Rekursion erhöht die Anforderungen an Transparenz. Ein KI-generierter Review darf einen Befund kritisieren, aber keine unabhängige Replikation ersetzen. Ein KI-generierter Patch darf einen Test reparieren, aber nicht selbst belegen, dass die Hypothese wahr ist. Ein KI-generierter Literaturhinweis muss auf eine überprüfte Originalquelle zurückgeführt werden.

## 42. Forschungsprozess als kontrollierbares System

Edition 1.8 behandelt den Forschungsprozess deshalb selbst als versioniertes System mit Gateways: Quellenquarantäne, frozen Preregistrierung, autorisierte Ausführung, DATA-Persistenz, Human Review, EVID-Entscheidung und Publikationsprojektion. Ein Fehler in einer Stufe soll nicht still in die nächste propagieren.

Der praktische Wert der rekursiven Perspektive liegt nicht in einer metaphysischen These, sondern in prüfbaren Prozessfragen: Wo kann Information ihren Status ändern? Wer darf den Status ändern? Welche Transformation ist reversibel? Welche Provenienz bleibt erhalten? Welche automatische Abkürzung würde menschliche oder empirische Prüfung umgehen?

## 42.1 Die eigentliche Entdeckung dieser Forschung ist teilweise prozessual

Die Vorgängerarbeiten zeigen, dass einige der wichtigsten Erkenntnisse nicht direkt über einen neuronalen Mechanismus entstanden, sondern über die **Bedingungen, unter denen überhaupt ein belastbarer Mechanismusclaim möglich ist**.

Vier Beispiele sind zentral:

- Ein 5D-Experiment kann formal mehrere Dimensionen enthalten und trotzdem keinen Geometrieeffekt testen.
- Ein Report kann fehlende Werte anzeigen, obwohl die DATA vollständig sind.
- Ein positiver Vergleich gegen No-Replay kann einen Semantikmechanismus scheinbar stützen, obwohl Raw-Replay die stärkere Erklärung liefert.
- Ein externer Softwarevergleich kann Referenzkonformität zeigen, ohne eine unabhängige Replikation zu sein.

Rekursive Epistemik bezeichnet deshalb nicht nur „Wissenschaft über Wissenschaft“, sondern die konkrete Rückkopplung, durch die Fehler im Forschungsprozess neue technische und methodische Verträge erzeugen.

## 42.2 Objekt-Gateway und epistemisches Gateway

Die Parallelität lässt sich präziser formulieren.

Auf Objektebene beantwortet ein Gateway Fragen wie:

- Welche Information darf in das neuronale System?
- Wie wird sie kodiert?
- Darf sie nur gelesen oder auch in Lernzustand transformiert werden?
- Welche Provenienz bleibt erhalten?

Auf Forschungsebene beantwortet ein epistemisches Gateway analoge Fragen:

- Darf eine Quelle in die Argumentation eingehen?
- Ist sie Theorie, DATA, Review oder EVID?
- Darf eine automatische Auswertung ihren Status verändern?
- Welche Person oder welches Gate autorisiert die Transition?

Der Gewinn dieser Analogie liegt darin, dass **Statusänderung selbst** zum Designobjekt wird. So wie ein externer Dienst nicht heimlich Gewichte ändern darf, darf ein Buildprozess nicht heimlich DATA zu EVID hochstufen.

## 42.3 Der Forschungsprozess besitzt eigene Fehlermodi

MHRN behandelt inzwischen mindestens fünf Meta-Fehlermodi explizit:

1. **Source contamination:** eine unbestätigte oder rekursive Quelle wird als externe Unterstützung missverstanden.
2. **Status leakage:** Planung oder DATA erscheinen im UI oder Text wie bestätigte EVID.
3. **Projection error:** ein Report verzerrt oder verliert Information aus den Rohartefakten.
4. **Post-hoc drift:** Erfolgsregeln verschieben sich nach Sichtung der DATA.
5. **Architecture rescue:** ein negativer Mechanismusbefund wird durch immer neue Rollenannahmen immunisiert.

Diese Fehlermodi sind nicht nur Dokumentationsprobleme. Sie können die Architektur selbst in eine falsche Richtung lenken.

## 42.4 CL-001–003 als Beispiel rekursiver Epistemik

Die Semantization-Linie zeigt die Rekursion besonders deutlich.

Auf Objektebene wurde ein Gedächtnismechanismus getestet. Auf Metaebene zeigte CL-001, dass die Baseline die Mechanismusursache nicht sauber trennte. Diese Erkenntnis führte zu CL-002 mit Raw-Replay-Kontrolle. Das negative Ergebnis veränderte wiederum die Architekturposition und führte zu einer engeren CL-003-Dosisprüfung. Deren negative Primärkontraste führten schließlich zu einer Stop-Regel gegen serielle Rollenrettung.

Der Forschungsprozess lernte also nicht nur **über SemanticMemory**, sondern auch darüber, **wie MHRN Mechanismuskandidaten künftig prüft**.

## 42.5 EXP-GEN-0036 als Beispiel einer Meta-Intervention

Auch `EXP-GEN-0036` hatte zwei Ebenen. Die Suite sollte mehrere Forschungsprotokolle ausführen; gleichzeitig prüfte sie implizit die Fähigkeit der Forschungsinfrastruktur, heterogene Protokolle korrekt zusammenzufassen. Der Reportingfehler zeigte, dass eine universelle SNN-Tabelle semantisch unterschiedliche Protokolle verzerren kann.

Der wissenschaftliche Output war damit zweifach:

- fachlich: Recurrence war mechanistisch sichtbar, 5D-v1 war nicht testadäquat;
- methodisch: Reporting benötigt protokollspezifische Schemata und darf fehlende Metrikfelder nicht als fehlende DATA interpretieren.

## 42.6 Rekursive Epistemik und AI-Assistenz

Die AI-Assistenz verschärft diese Anforderungen, weil ein Modell gleichzeitig Code, Review, Text und Literaturhinweise erzeugen kann. Ohne Trennung könnte derselbe Ursprung mehrfach als scheinbar unabhängige Bestätigung wiederkehren.

Edition 1.8 behandelt deshalb AI-Beiträge als Transformationsknoten, nicht als Autoritätsquelle. Entscheidend ist, was nach dem AI-Schritt geschieht: Wird eine Primärquelle geprüft? Wird der Patch getestet? Wird die Analyse gegen Rohdaten kontrolliert? Wird die Entscheidung von einer dafür vorgesehenen Instanz getroffen?

## 42.7 Rekursive Epistemik als revidierbare Arbeitshypothese

Auch der Begriff selbst ist kein abgeschlossener theoretischer Triumph. Er ist derzeit eine **methodische Synthesehypothese**: Die Forschung wird robuster, wenn Objekt- und Prozess-Gateways gemeinsam modelliert und Statusänderungen explizit kontrolliert werden.

Diese Hypothese kann durch Prior Art relativiert werden, durch externe Reviewer kritisiert werden oder sich als zu breit erweisen. Ihr wissenschaftlicher Wert hängt daher nicht davon ab, ob der Begriff neu ist, sondern ob die Operationalisierung zu klareren, reproduzierbareren Entscheidungen führt.

## 42.8 Geliehene Intelligenz als konkrete Provenienzmatrix

Die Theorie der geliehenen Intelligenz gewinnt in MHRN eine operative Form, wenn die abstrakten Herkunftsfragen auf einzelne Forschungsereignisse abgebildet werden. Für einen Claim können mindestens folgende Knoten unterschieden werden: menschliche Problemsetzung, externe Literatur, AI-generierter Vorschlag, AI-generierter Code, menschliche Auswahl, Commit, eingefrorenes Protokoll, Experiment, DATA, Review und Publikationssynthese. Erst diese Kette beantwortet, **welcher Anteil geliehen, transformiert, entschieden oder gemessen** wurde.

Damit wird die frühere Theorie nicht auf eine philosophische Einleitung reduziert. Sie wirkt direkt auf die Forschungsmethodik: Derselbe AI-Ursprung darf nicht mehrfach als scheinbar unabhängige Bestätigung gezählt werden; Literaturautorität darf nicht als MHRN-Evidenz erscheinen; und ein menschlicher Auftrag an ein Modell ist nicht dasselbe wie der konkrete vom Modell vorgeschlagene Lösungsweg.

## 42.9 Ko-Kognition als Systemgrenze

Das Szenario symbiotischer Ko-Kognition ist für die reale Schaffenspraxis bereits methodisch relevant, ohne dass daraus starke Autonomieclaims folgen. Der Autor nutzt Modelle für Suche, Kritik, Code und Synthese; die Modelle nutzen menschlich formulierte Ziele, Auswahl und Rückmeldung. Die produktive Einheit kann daher zeitweise ein gekoppelter Mensch-Werkzeug-Prozess sein.

Edition 1.8 trennt dennoch drei Grenzen: **kognitive Unterstützung**, **Entscheidungsautorität** und **wissenschaftliche Evidenz**. Ein Modell kann die kognitive Reichweite des Autors erweitern, ohne Autor der Hypothese zu sein; es kann einen Patch erzeugen, ohne ihn freigeben zu dürfen; und es kann DATA interpretieren, ohne EVID zu akzeptieren. Diese Trennung verhindert, dass Ko-Kognition mit Verantwortungsdiffusion verwechselt wird.

## 42.10 Rekursive Technogenese als Forschungsprozess-Spiegel

Die ältere Technogeneseformel beschreibt Generationen technischer Systeme. Im aktuellen Projekt existiert eine engere, beobachtbare Analogie: Werkzeuge und Modelle helfen, eine Forschungsinfrastruktur zu verändern, die wiederum festlegt, wie spätere Modelle, Experimente und Reviews eingesetzt werden. Ein AI-kritisiertes Reportingproblem kann zu einem neuen Schema führen; dieses Schema verändert, welche Fehler spätere AI-Reviews überhaupt sehen können.

Das ist noch keine autonome technische Evolution. Es ist eine **rekursive Werkzeug-/Governance-Kette**, deren Provenienz beobachtbar ist. Genau hier verbindet sich die Vorgängerarbeit mit rekursiver Epistemik: Nicht die Metapher einer selbsterschaffenden Maschine ist der aktuelle Befund, sondern die messbare Rückwirkung von Werkzeugen auf die Bedingungen ihrer eigenen späteren Verwendung.

## 42.11 Von der Herkunftsfrage zur Prüfregel

Aus den Vorgängerarbeiten lässt sich eine allgemeine Prüfregel ableiten: Je stärker ein Ergebnis von ausgelagerten epistemischen Ressourcen abhängt, desto expliziter müssen Quelle, Transformationsschritt und Autorität dokumentiert werden. Das gilt für Retrieval ebenso wie für LLM-Synthese, Codegeneratoren, externe Decoder, periphere neuronale Netze und menschliche Reviews.

„Geliehene Intelligenz“ wird damit in Edition 1.8 zu einer prüfbaren Herkunftsfrage: **Welche Ressource kam von wo, welche Zustandsänderung verursachte sie, und wer durfte diese Zustandsänderung autorisieren?**


---

<a id="part-x"></a>

# Teil X — Synthese und revidierbare Beiträge

## 43. Synthesis Contract

Jeder Syntheseclaim soll Forschungsachse, Thema, Entwicklungsphase, Provenienzklasse, Evidenzstatus, Interpretationsart und Revisionskriterium tragen. Damit wird verhindert, dass ein technisch plausibler Zusammenhang durch bloße Wiederholung den Status eines empirischen Ergebnisses erhält.

Die maschinenlesbare Claim-Liste dieser Edition steht in `registers/claim_ledger.json`. Sie ist eine Publikationsprojektion und besitzt keine EVID-Autorität. Kein Eintrag darf `accepted_EVID` allein durch den Buildprozess erhalten.

## 44. Was sich über die gesamte Schaffenszeit hält

Über die rekonstruierte Geschichte hinweg sind fünf wiederkehrende Probleme sichtbar: Persistenz; kausale Zuordnung von Lernen; Wachstum ohne Kontrollverlust; verkörperte Rückkopplung; und die Grenze zwischen externer symbolischer Intelligenz und internem dynamischen Substrat. Diese Kontinuität ist eine historische Synthese, kein Beweis wissenschaftlicher Neuheit.

## 45. Gegenwärtig tragfähige Architekturposition

MHRN ist am stärksten als instrumentiertes Forschungsframework beschrieben. Technische Mechanismen sind in mehreren Stages implementiert, doch wissenschaftliche Reife wird separat gemessen. Fünf Dimensionen sind offen. SemanticMemory ist nach CL-002/003 nicht als überlegener Kernmechanismus bestätigt. Prediction Error, generatives Weltmodell, kausales Selbstmodell, höhere Kognition und Bewusstsein bleiben offene Forschungsbereiche.

Gleichzeitig hat die Arbeit methodisch an Schärfe gewonnen: negative Befunde bleiben erhalten; historische Daten werden nicht umgeschrieben; Quellen und AI-Hilfe werden offengelegt; Experiment und Evidenz sind getrennt; und die Architektur kann aufgrund negativer Ergebnisse reduziert werden.

## 46. Kandidatenbeiträge

Als Kandidaten, nicht als bewiesene Neuheit, bleiben insbesondere: die Trennung von Logical Identity/Physical Slot/Synaptic Reduction/Execution Scheduling; auditierbare strukturelle Mutation über Proposal→Approval→Mutation→Journal→Undo; Content Gateway versus Compute Backend; source-bound DATA/EVID-Grenzen; duale Engineering-/Scientific-Maturity-Timeline; und die explizite Rekursion zwischen Objekt- und Forschungsprozess-Gateways.

Jeder dieser Kandidaten benötigt Prior-Art-Review. Die Publikation darf die Kombination beschreiben, ohne daraus automatisch einen Vorrang gegenüber vorhandenen SNN-, Agenten-, Workflow- oder Safety-Systemen abzuleiten.

## 47. Revision statt Abschluss

Edition 1.8 ist kein Endpunkt. Ein guter Syntheseclaim nennt, was ihn ändern würde. Neue Replikation kann Stage-Reife erhöhen oder senken. Neue Prior Art kann einen Neuheitskandidaten in bekannte Praxis einordnen. Ein besseres Experiment kann einen bisherigen Nullbefund enger begrenzen oder bestätigen. Ein originales Chat-/Codeartefakt kann die Schaffensgeschichte korrigieren.

Die Qualität der Synthese zeigt sich deshalb nicht daran, dass sie stabil gegen Kritik ist, sondern daran, dass sie präzise angibt, wie Kritik und neue Evidenz in eine Revision überführt werden.

## 47.1 Bilanz der bisher tatsächlich erreichten Forschung

Edition 1.8 kann nach Integration der Vorgängerarbeiten erstmals eine zusammenhängende Forschungsbilanz formulieren. Diese Bilanz ist bewusst asymmetrisch: Einige Resultate sind positiv, andere negativ, wieder andere betreffen Testadäquanz oder Governance.

### Ergebnis A — Einzelzellmodelle sind für einen eng definierten Referenzumfang belastbar verifiziert

Die Izhikevich- und LIF-V2-Konformitätsarbeit zeigt, dass die deklarierten lokalen Übergangs-, Schwellen- und Resetsemantiken unter dem eingefrorenen Prüfdesign sehr eng mit Brian2 übereinstimmen. Für den scoped Readiness-Vertrag ist Stage 0 damit abgeschlossen. Gleichzeitig bleibt der frühere freie Langzeit-Negativbefund erhalten und zeigt, dass lokale numerische Übereinstimmung nicht automatisch langfristige Trajektorienidentität bedeutet.

**Zulässiger Claim:** definierte Referenzkonformität und dokumentierter Operating Envelope.  
**Nicht zulässig:** biologische Äquivalenz oder unabhängige Replikation.

### Ergebnis B — Rekurrenz besitzt im kleinen kontrollierten System einen klaren mechanistischen Effekt

`EXP-GEN-0036` zeigt in `PING` einen deutlichen Unterschied zwischen Recurrence-off und Recurrence-on. Die Intervention ist technisch klarer isoliert als zunächst angenommen. Die Aussage bleibt dennoch auf das kleine mechanistische Design begrenzt.

**Zulässiger Claim:** Rekurrenz verändert unter diesem kontrollierten Simulationsvertrag die Dynamik deutlich.  
**Nicht zulässig:** daraus unmittelbar Gedächtnis, höhere Kognition oder allgemeine Skalierungswirkung abzuleiten.

### Ergebnis C — Die bisherige 5D-v1-Studie testete die zentrale Geometriehypothese nicht adäquat

Dies ist kein Scheitern der 5D-Hypothese und kein positiver Befund. Es ist eine Designkorrektur. Die Dimension wurde variiert, ohne dass die relevante Dynamik ausreichend an Geometrie gekoppelt war.

**Zulässiger Claim:** RQ-5D-005 ist durch 5D-v1 hinsichtlich eines genuinen Geometrieeffekts nicht getestet.  
**Konsequenz:** nächste Studie benötigt einen vorab definierten Geometriemechanismus und matched controls.

### Ergebnis D — Modality-specific pathways sind technisch und in mehreren synthetischen Teilfragen experimentell belegt

Stage 4 verfügt über getrennte Audio-, Vision- und Digitalpfade und die E01–E05-DATA. Die Resultate zeigen Unterschiede in modellierten Kosten, adaptive Ressourcenallokation, ROI-Effizienz im synthetischen visuellen Design, digitale Integrität und Recovery nach Modalitätsverlust.

**Zulässiger Claim:** mehrere eng definierte technische Teilfunktionen funktionieren in den registrierten synthetischen Designs.  
**Nicht zulässig:** allgemeine funktionale Überlegenheit spezialisierter Areale, emergente Spezialisierung oder physikalische Energieeffizienz.

### Ergebnis E — Ein synthetischer Closed Loop ist kontrolliert demonstriert

Stage 5 verbindet Sensorik, digitale Interozeption, autorisierte Aktorik und Feedback. Die 360-Run-Kampagne zeigt DATA-Support für die kontrollierte Sensor–SNN–Aktor–Feedback-Kette und die Abgrenzung unautorisierter/fehlerhafter Pfade.

**Zulässiger Claim:** reproduzierbarer synthetischer Closed-Loop-Engineeringpfad mit kontrollierten Fehlerarmen.  
**Nicht zulässig:** allgemeine Realwelt-Autonomie oder Abschluss von H-EMB-001-B.

### Ergebnis F — Replay ist derzeit stärker empirisch getragen als semantische Verdichtung

CL-001 bis CL-003 bilden die deutlichste Architekturselektion. Der zunächst positive Semantic+Replay-Befund überlebte die stärkere Raw-Replay-Kontrolle nicht als bestätigter semantischer Zusatznutzen. Gleichzeitig zeigte C3, dass die semantischen Prototypen echte, nicht-zufällige Struktur tragen.

**Zulässiger Claim:** Replay ist unter den untersuchten Bedingungen der robuste Hauptbeitrag; SemanticMemory kodiert relevante Struktur.  
**Nicht zulässig:** bestätigter Zusatznutzen von SemanticMemory gegenüber gematchtem Raw-Replay oder bestätigter Dosisvorteil.

### Ergebnis G — Der Forschungsprozess selbst wurde messbar verbessert

Fehler in Reports, Baselines, Testadäquanz und AI-Schema-Normalisierung führten zu dauerhaften Prozessverträgen: Status-Trennung, Freeze/Authorization, source-bound DATA, Human Review, EVID-Gates, protokollspezifische Reports und Stop-Regeln.

Dieser Beitrag ist methodisch, nicht neuronaler Natur. Er erklärt jedoch, warum spätere Experimente eine höhere epistemische Qualität besitzen als frühe Feature-Demonstrationen.

### Ergebnis H — Same-Seed-Reproduzierbarkeit ist nun als eigene DATA-Linie dokumentiert

`EXP-GEN-0045` und `EXP-GEN-0046` ergänzen die bisherige Determinismusargumentation um explizite Replikaprotokolle. Im Tonic-Spike-Protokoll waren die Spike-Sequenzen in allen drei Same-Seed-Paaren identisch. Im Recurrence-Protokoll reproduzierten A/B-Paare über drei Seeds jeweils dieselben deskriptiven Trajektorien; zugleich blieb der große Off/On-Unterschied stabil sichtbar.

**Zulässiger Claim:** Für die registrierten kleinen Protokolle sind Same-Seed-Trajektorien beziehungsweise Replikapaare technisch reproduzierbar, und der deskriptive Recurrence-off/on-Unterschied wird in EXP-GEN-0046 erneut beobachtet.  
**Nicht zulässig:** daraus bereits unabhängige Replikation, allgemeine Determinismusgarantie, statistische Unabhängigkeit der identischen Trajektorien oder bestätigte EVID abzuleiten. EXP-GEN-0046 bleibt bis semantischer Zuordnung und Human Review DATA-only.

## 47.2 Was durch die bisherigen Ergebnisse geschwächt oder verworfen wurde

Eine vollständige Synthese muss nicht nur die positiven Ergebnisse nennen.

### Geschwächt: starke 5D-Interpretationen

Es existiert bislang kein belastbarer Nachweis, dass ein 5D-Adressraum gegenüber gematchten niedrigeren oder höheren Dimensionen funktional überlegen ist. Frühere identische Resultate dürfen nicht als Nullbefund interpretiert werden, weil das Design nicht geometriesensitiv genug war.

### Geschwächt: SemanticMemory als zentraler Continual-Learning-Kern

Nach CL-002/003 ist eine zentrale Sonderrolle nicht empirisch getragen. SemanticMemory bleibt als Mechanismuskandidat bestehen, aber Raw-Replay ist Referenz. Eine serielle Suche nach immer neuen Rollen ist methodisch ausgeschlossen.

### Verworfen: Gleichsetzung technischer Reife mit wissenschaftlicher Evidenz

Die Vorgängerarbeiten haben mehrfach gezeigt, dass ein grüner Full-Stack oder ein vollständiges Stage-Panel nicht ausreicht. Diese Gleichsetzung ist methodisch aufgegeben.

### Verworfen: AI-Review als Evidenzinstanz

KI-Analysen können wertvolle Kritik liefern, aber weder Human Review noch unabhängige Replikation ersetzen. AIRR bleibt Assistenz- und Interpretationsschicht.

### Verworfen: Metapher als Mechanismusclaim

„Traum“, „Emotion“, „DNA“, „Selbst“ oder „Weltmodell“ werden ohne Operationalisierung nicht mehr als technische Tatsachen behandelt.

## 47.3 Der stärkste derzeitige Gesamtclaim

Der stärkste Gesamtclaim von MHRN ist nicht, dass bereits allgemeine Intelligenz, ein vollständiges Weltmodell oder ein biologisch äquivalentes Gehirn entstanden sei. Er lautet enger:

> MHRN ist ein reproduzierbar instrumentiertes Forschungsframework, in dem spikende Dynamik, Rekurrenz, mehrere Plastizitätsformen, strukturierte Mutation, modality-specific pathways, synthetisches Embodiment sowie Gedächtnis-/Vorhersagemechanismen unter zunehmend expliziten Kontroll-, Provenienz- und Evidenzverträgen untersucht werden können. Mehrere Teilmechanismen sind technisch und experimentell gestützt; zentrale stärkere Hypothesen — insbesondere 5D-Vorteil, semantischer Zusatznutzen, kausales Weltmodell, Selbstmodell, höhere Kognition und Bewusstsein — bleiben offen oder wurden eingegrenzt.

Dieser Claim ist weniger spektakulär als frühe Visionen, aber wissenschaftlich stärker.

## 47.4 Methodische Eigenleistung der negativen Ergebnisse

Die negativen und korrigierenden Befunde haben eine gemeinsame Richtung erzeugt: MHRN entwickelt sich von einer additiven Architektur zu einer **selektiven Architektur**. Nicht jeder plausible Mechanismus bleibt zentral. Ein Mechanismus muss gegenüber einer einfacheren Referenz einen messbaren Beitrag leisten oder eine klar begründete Spezialrolle besitzen.

Damit wird Forschung selbst zum Architekturfilter. Diese Regel gilt künftig für SemanticMemory, biophysikalische Detailmodelle, 5D-Geometrie, Spiegelmechanismen und höhere Kognitionsmodule gleichermaßen.

## 47.5 Kandidatenbeiträge nach heutigem Stand

Die potenziell interessantesten projektinternen Beiträge liegen derzeit weniger in einzelnen bekannten neuronalen Regeln als in ihrer kontrollierten Zusammenführung:

1. Trennung von Logical Identity, Physical Slot, Synaptic Reduction und Execution Scheduling;
2. auditierbare Strukturplastizität über Proposal → Approval → Mutation → Journal → Undo;
3. Trennung von Content Gateway und Compute Backend;
4. source-bound DATA/EVID-Grenzen mit expliziter Human-Review-Transition;
5. duale Engineering-/Scientific-Maturity-Achse;
6. Forschungsprozess-Gateways als Gegenstück zu technischen Informationsgateways;
7. empirische Architekturselektion mit Stop-Regeln gegen serielle Mechanismusrettung.

Diese Punkte sind **Kandidatenbeiträge**. Ob und in welchem Umfang sie gegenüber bestehender Literatur neu sind, bleibt Gegenstand des Prior-Art-Reviews.

## 47.6 Was Edition 1.8 gegenüber 1.7 tatsächlich hinzufügt

1.8 ist nicht nur eine neue Gliederung. Die inhaltlich ausgearbeitete Fassung verbindet erstmals:

- die rekonstruierte Vor-Repo-Schaffensgeschichte;
- Brain-5D als historisches Forschungsprogramm;
- die vollständige Stage-0–10-Architekturlinie;
- die konkreten Stage-4- und Stage-5-DATA;
- CL-001–003 als Architekturselektion;
- Stage-0-V2-Referenzkonformität;
- `EXP-GEN-0036` als kombinierte Fach- und Prozesskorrektur;
- AI-assistierte Schaffenspraxis und Quellenprovenienz;
- Safety, Autonomie, geliehene Intelligenz und rekursive Technogenese;
- rekursive Epistemik als methodische Synthese des Forschungsobjekts und seiner eigenen Entstehung.

Damit wird die elfteilige Struktur von einer Hülle zu einer tatsächlichen Synthese der bisherigen Schaffens- und Forschungszeit.

## 47.7 Quelleninventar ist nicht Inhaltsintegration

Der Audit dieser Edition hat eine wichtige eigene Korrektur erzeugt. Ein vollständiger `SOURCE_INDEX` kann belegen, dass Dateien am Basiscommit inventarisiert und erhalten wurden; er kann **nicht** belegen, dass ihre wissenschaftlich relevanten Gedanken im Haupttext verarbeitet sind. Dasselbe gilt für eine automatische Teilzuordnung nach Pfadregeln.

Edition 1.8 führt deshalb zusätzlich ein semantisches **Content-Integration-Ledger**. Für wissenschaftlich materielle Vorarbeiten und kanonische Dokumentfamilien wird angegeben, welche Rolle die Quelle besitzt, in welchen Teilen ihre Kernaussagen verarbeitet werden, welcher Integrationsmodus gilt und welche Grenzen erhalten bleiben. Dieses Ledger umfasst unter anderem NeuroGenesis, Brain-5D, „KI – Die geliehene Intelligenz“, die Editionslinie 1.0–1.7, Architektur-/Scientific-Contracts, Neural Symbiosis, MSBA, Wesen/Embodiment, Profile & Identity, Connectome-Arbeit, Persistenz, Registry/Protokolle, Experiment-DATA, Stage-Dossiers, AI-Tooling sowie Ethics/Critique/Review.

Dabei bedeutet **integriert** nicht „jede Datei wortwörtlich in das Manuskript kopiert“. Rohdaten bleiben source-bound Primärartefakte; maschinenlesbare Registryobjekte bleiben im Research Register; historische Texte bleiben als Vorarbeiten erhalten. Die Gesamtarbeit übernimmt deren wissenschaftlich materielle Ergebnisse, Argumente, Gegenargumente, Grenzen und Entwicklungskonsequenzen in die neue Synthese.

## 47.8 Was die Corpus-Integration zusätzlich sichtbar macht

Die vertiefte Integration verändert die Gesamtinterpretation an mehreren Stellen:

- Brain-5D ist nicht nur ein Namensvorgänger, sondern die genealogische Quelle für 5D-Adressierung, Wachstums-/Persistenzfragen, Trennung externer Sprachintelligenz und neuronalen Kerns sowie frühe Erkenntnis-/Ethikfragen.
- „Geliehene Intelligenz“ liefert nicht nur ein Schlagwort, sondern das Fünf-Achsen-Modell `I=(M,E,G,Z,X)`, genealogische Distanz, rekursive Technogenese und Ko-Kognition als belastungstestbare Theorieelemente.
- Neural Symbiosis und MSBA zeigen, dass Hybridität in MHRN über explizite Gateway-Grenzen statt durch heimliche Vermischung von SNN, LLM und peripheren Modellen organisiert wird.
- Wesen/Real-Body macht „keine Fantasiedaten“ zu einer allgemeinen Provenienzregel: beobachtete, abgeleitete und dargestellte Zustände bleiben getrennt.
- Profile & Identity liefert eine reproduzierbare technische Identitäts-/Lineageschicht, gerade indem sie sich von psychologischem Selbst und subjektiver Kontinuität abgrenzt.
- Related Work verschärft Stage 6: externe Semantization-, Predictive-Coding-, World-Model- und Multi-Zeitskalen-Arbeiten definieren stärkere Vergleichspunkte, ohne MHRN-Ergebnisse zu ersetzen.

Damit wird Edition 1.8 weniger zu einer Zusammenfassung einzelner Experimente und stärker zu einer **Gesamtarbeit über Forschungsobjekt, Schaffensgenealogie und die Methodik ihrer kontrollierten Verbindung**.

## 47.9 Neue methodische Erkenntnis: semantischer Match ist nicht Testadäquanz

Die jüngsten Determinismus- und Topologieentscheidungen schärfen eine zentrale Lehre von MHRN: **Semantische Zuordnung, technische Reproduzierbarkeit und Hypothesentestadäquanz sind drei verschiedene Prüfungen.** Ein Experiment kann die richtigen registrierten Conditions besitzen und byte-/metrisch reproduzierbar laufen, während sein Mechanismus dennoch nicht sensitiv genug ist, die Zielhypothese zu beantworten.

`EXP-GEN-0047` ist dafür das Referenzbeispiel. Die korrekte Schlussfolgerung lautet nicht „Topologie hat keinen Effekt“, sondern „dieser v1-Aufbau macht Topologie nicht ausreichend kausal wirksam, um den Effekt zu testen“. Damit wird ein scheinbarer Nullbefund in eine Designkorrektur überführt, ohne DATA umzuschreiben.

Analog zeigt die Determinismus-Registry-Korrektur, dass ein technisch passender Befund durch falsche historische RQ-Zuordnung nicht nachträglich zu EVID umetikettiert werden darf. Die wissenschaftlich stärkere Lösung ist, historische Provenienz zu erhalten und den prospektiven Vertrag zu reparieren.

## 47.10 Neue Richtung nach CL-003: Kompression statt bloßer Gleichheit

Der genehmigte Vorschlag `LP-20260917194217` zeigt eine methodisch sinnvollere Anschlussfrage an CL-003. Nachdem SemanticMemory im bisherigen matched-budget-Vergleich keinen bestätigten additiven Vorteil gegenüber Raw Replay gezeigt hat, verschiebt sich die nächste prüfbare These von „ist semantisches Replay generell besser?“ zu einer **Ressourcen-/Kompressionsfrage**: Kann eine semantisch verdichtete Repräsentation bei einem Zehntel des Speicherbudgets nahezu dieselbe Retention erreichen?

Das ist derzeit keine Erkenntnis, sondern eine genehmigte Forschungsrichtung. Ihr Wert liegt gerade darin, dass sie eine mögliche Stärke von semantischer Verdichtung dort prüft, wo sie theoretisch plausibler wäre: nicht als pauschaler Leistungsbonus bei gleichem Budget, sondern als Trade-off zwischen Retention und Speicherbedarf.

## 47.11 Review-induzierte Synthese: stärkere Wissenschaft durch engere Aussagen

Die jüngsten Human Reviews verändern die Gesamtbilanz nicht durch einen weiteren positiven Claim, sondern durch präzisere Grenzen.

Erstens ist der Determinismusbefund für `RQ-DET-001` jetzt semantisch besser eingeordnet: die Same-Seed-Replica-Paare stimmen im getesteten Protokoll überein. Gleichzeitig bleibt der historische Dirty-Tree-Lauf von einer Evidenzpromotion ausgeschlossen. Damit trennt die Arbeit erstmals explizit **Befundstärke** von **Provenienzstärke**.

Zweitens wird `EXP-GEN-0047` nicht mehr als scheinbarer Topologie-Nullbefund gelesen. Die wissenschaftlich stärkere Aussage lautet, dass `topology_propagation_v1` die Zielhypothese nicht angemessen operationalisiert hat. Das ist keine Schwächung der Forschung, sondern eine Reduktion von Fehlinterpretation: ein inadäquates Design wird als Designproblem markiert, nicht als Widerlegung einer Hypothese.

Drittens ergibt sich daraus eine übergreifende Reiferegel für MHRN: **ein Experiment darf erst dann eine Hypothese tragen, wenn semantische Zuordnung, kausale Wirksamkeit des manipulierten Faktors, Aktivitätsadäquanz, Provenienz und vorab definierte Auswertung gleichzeitig ausreichend sind.** Diese Regel ist inzwischen selbst ein Ergebnis der Schaffensgeschichte, weil sie aus konkreten Fehlklassifikationen und Reviews hervorgegangen ist.


---

<a id="part-xi"></a>

# Teil XI — Offene Forschungslandschaft

## 48. Offene empirische Felder

Die offene Forschungslandschaft wird aus dem tatsächlich erreichten Stand abgeleitet. Bereits erledigte Prüfungen werden nicht weiterhin als pauschal „offen“ geführt; zugleich wird ein enger positiver Befund nicht zu einer breiteren Reife hochgestuft.

### Stage 0 — einzelne Nervenzelle

Der scoped Referenzkonformitätsvertrag für Izhikevich und `lif-current-v1` ist mit der Brian2-V2-Kampagne erfüllt. Offen bleiben daher **nicht** mehr allgemein „ein externer Referenzvergleich“, sondern die stärkeren nächsten Ebenen:

- menschliche EVID-Entscheidung zu den confirmatory DATA;
- unabhängig autorisierte Replikation außerhalb derselben MHRN-Ausführungskette;
- breitere Integrator-, Zeitschritt- und Parameterablationen;
- zusätzliche Neuronmodelle nur als klar deklarierte alternative Modellarme;
- Prüfung, welche lokalen Konformitätsaussagen über längere freie Trajektorien stabil bleiben und wo chaotische/nichtlineare Divergenz erwartbar ist.

Der scoped Readiness-Vertrag kann 100 % erreicht haben, ohne dass damit die gesamte wissenschaftliche Reife der Stage abgeschlossen ist.

### Stage 1 — kleines SNN

Stage 1 benötigt vor allem eine stärkere Forschungsbasis jenseits technischer Signalweitergabe:

- eigene präregistrierte Small-Network-RQ/Hypothesen;
- task-basierte Kontrollen statt nur Funktionsverifikation;
- Störungs- und Topologievariationen;
- unabhängige Replikation.

### Stage 2 — stabile Rekurrenz

`EXP-GEN-0036` liefert einen klaren kleinen mechanistischen Recurrence-Effekt, aber keine breite Generalisierung. Die nächste Generation sollte:

- Behandlungsarme pro Seed gepaart ausführen;
- vor der Ausführung einen automatischen Topologie-Diff archivieren;
- identische gemeinsame Gewichte und Delays nachweisen;
- nur die registrierte Rekurrenzintervention zwischen Armen variieren;
- Aktivitäts- und Stabilitätsgates vor der Effektinterpretation anwenden;
- größere und vielfältigere Netzwerkregime getrennt von der Baseline-Rekurrenz prüfen.

Skalierung, Stabilität und funktionaler Nutzen bleiben getrennte Fragen.

#### Reproduzierbarkeit und Determinismus — nächstes Gate

Die EXP-GEN-0045/0046-DATA schließen die Frage nicht vollständig. Als nächste Schritte sind erforderlich:

- semantische Zuordnungsregel für `RQ-DET-001` registrieren und EXP-GEN-0046 human reviewen;
- Same-Seed-Reproduzierbarkeit von echter unabhängiger Replikation getrennt halten;
- zusätzliche Seeds, Eingangsregime, Netzwerkgrößen und Restart/Restore-Bedingungen prüfen;
- deterministische Identität, numerische Toleranz und statistische Reproduzierbarkeit als getrennte Klassen auswerten;
- AIRR-Interpretation nicht als EVID verwenden, solange Human Review und semantisches Gate offen sind.

### Stage 3 — plastisches Nervengewebe

Die Mechanismen sind technisch vorhanden; offen sind vor allem die wissenschaftlichen Wirkungen und Interaktionen:

- held-out Generalisierung statt bloßer Gewichtsänderung;
- learning-on/off, Frozen, Sham und Information-Destroyed Kontrollen;
- Langzeitstabilität;
- Interaktion von STDP, Eligibility, Drei-Faktor-Modulation und Homeostase;
- Ressourcen- und Strukturkosten von Plastizität;
- unabhängige Replikation.

### Stage 4 — spezialisierte neuronale Areale

E01–E05 liefern DATA für mehrere enge technische Teilfragen. Noch offen sind:

- menschliche beziehungsweise unabhängige Review der E01–E05-Claims;
- matched spezialisierte vs. unspezialisierte/generalistische Pfade;
- Frozen/Random/Shuffle/Läsionskontrollen zur Isolierung von Adapter-, Gateway- und Plastizitätsbeiträgen;
- Cross-Modal-Transfer;
- emergente gegenüber architektonisch vorgegebener Spezialisierung;
- dynamisch materialisierte Skalierung über steigende reale Neuronen-/Kantenbudgets;
- physikalische Energie-/Ressourcenmessung statt ausschließlich modellierter Kosten.

### Stage 5 — integriertes künstliches Nervensystem

Die synthetische 360-Run-Referenz zeigt einen kontrollierten Engineeringpfad. Die entscheidenden nächsten Schritte sind:

- präregistrierter Test von `H-EMB-001-B` unter identischer externer Störung;
- direkter Vergleich Closed Loop vs. yoked Replay vs. interrupted feedback;
- längere Störungs- und Recovery-Serien;
- Sensor-Loss und Actuator-No-Effect als kausal ausgewertete Interventionsarme;
- Real-Device-Studien nur als eigener safety-gated Forschungszweig;
- getrennte physikalische Ressourcenmessung.

### Stage 6 — Gedächtnis, Prediction Error und Weltmodell

Die CL-001–CL-003-Linie hat den Suchraum bereits verkleinert. Offen sind daher nicht beliebig viele SemanticMemory-Rollen, sondern klar begrenzte Entscheidungen:

1. Human Review von CL-003 abschließen.
2. Danach genau eine Entscheidung A/B/C treffen: Nebenrolle, genau eine theoretisch begründete Zusatzprüfung oder Parken bis zu funktionaler Notwendigkeit.
3. Keine automatische CL-004-Serie und keine serielle Rollenrettung.

Unabhängig davon bleiben als zentrale Stage-6-Forschungsfragen:

- Prediction Error als **kausaler neuronaler Lern-/Aktivitätsmechanismus**, nicht nur Telemetrie;
- action-conditioned Mehrschrittvorhersage;
- Unsicherheitskalibrierung und OOD-Verhalten;
- Entscheidungsnutzen gegenüber reactive/no-model/corrupted-model Kontrollen;
- Retention, cue-abhängiger Recall, Spezifität und Generalisierung als Gedächtniskriterien;
- Spiegel-/Handlungsprädiktion mit shared, partially-shared und separate coding controls.

## 49. 5D-v2 — offene Hypothese mit neuer Mindestanforderung

Die bisherige 5D-v1-Teilstudie darf nicht als positiver oder negativer Test der Geometriehypothese gelten. Für eine neue 5D-Studie muss **vor Ausführung** feststehen, über welchen Mechanismus die Dimension die Dynamik beeinflussen kann.

Mindestanforderungen für 5D-v2:

- gleicher Knotenumfang und vergleichbare Ressourcenbudgets über Dimensionsbedingungen;
- präregistrierter Geometriemechanismus, z. B. distanzabhängige Nachbarschaft, Konnektivität, Delays oder Plastizität;
- Aktivitäts-Adequanz-Gate;
- topology-/degree-matched Kontrollen;
- getrennte `5d_shuffled`- und Random-Graph-Kontrollen mit klar dokumentiertem Kontrollzweck;
- genügend aktive Neuronen, synaptische Ereignisse und Laufzeit, um den Mechanismus überhaupt beobachten zu können;
- keine Umdeutung eines quieszenten oder geometrieinsensitiven Designs als Nullbefund;
- Dimensionen unterhalb, gleich und oberhalb von 5D, sofern die konkrete Hypothese dies verlangt.

Die zentrale Frage bleibt offen: Trägt die zusätzliche Adressdimension einen reproduzierbaren funktionalen Nutzen, wenn Topologie, Budget und Mechanismus angemessen kontrolliert sind?

## 50. Stage 7 — Selbstmodell und verkörperte Identität

Technische Identität, Profilzustände und Lineage sind vorhanden, aber noch kein kausales Selbstmodell. Nötig sind:

- observer-only und interventionelle Self/Other-Protokolle;
- Unterscheidung eigener vs. externer Handlungskonsequenzen;
- Nachweis, dass ein internes Modell eigener Zustände Vorhersage oder Entscheidung kausal verbessert;
- coupled-state restore als technische Vorbedingung;
- klare Abgrenzung zu bloßer Metadatenidentität.

Spiegelmechanismen dürfen erst dann in Stage 7 überführt werden, wenn Selbst-/Fremddifferenzierung tatsächlich kausal geprüft ist.

## 51. Stages 8–10 — Frontier

### Stage 8 — autonome lebenslange Entwicklung

Vorläufer-DATA und Continual-Learning-Fragen existieren, aber keine Evidenz für starke autonome lebenslange Entwicklung. Notwendig sind Shared-Network-Protokolle ohne Learned-State-Reset, Ressourcen-matched Baselines, getrennte Ablation von Replay/Konsolidierung/Stabilitäts-Plastizitäts-Gating und unabhängige Replikation.

### Stage 9 — hochintegrierte künstliche Kognition

Planung und Forschungsfragen existieren; claim-relevante confirmatory DATA fehlen. Attention, Planning, multimodale Integration, Konsolidierung und flexible Aufgabenübertragung müssen einzeln operationalisiert und anschließend in matched-budget Designs zusammengeführt werden.

### Stage 10 — Bewusstseinsforschung

Diese Stufe bleibt Forschungs- und Governance-Frontier. Vor jedem stärkeren Experiment sind kontrastierende, operationalisierte Vorhersagen, externe Ethik-/Stop-Governance und unabhängige adversariale Replikationsanforderungen nötig. Kein Stage-Score darf als Bewusstseins-, Sentienz- oder Moralstatusindikator verwendet werden.

## 52. Biophysikalische Erweiterungen

HH-artige Kanäle, Multi-Compartment-Dendriten, NMDA-Plateaus, Astrozyten-/Mikroglia-Netze, Gap Junctions, Proteinsynthese, Rezeptor-Trafficking und quantale Freisetzung bleiben kontrollierbare Modell- oder Ablationskandidaten. Sie werden nicht als Sammelfelder in den bestehenden Kern gestapelt.

Jede Erweiterung benötigt:

- eine konkrete Forschungsfrage;
- einen Referenz-/Konvergenztest;
- einen begründeten zusätzlichen Mechanismus;
- einen Vergleich mit einer einfacheren Modellvariante;
- ein Rechen- und Datenbudget, das wissenschaftliche Interpretation erlaubt;
- ein Stopkriterium, falls kein zusätzlicher Erkenntniswert entsteht.

Biologische Detailtiefe ist kein Selbstzweck und kein automatischer Reifegewinn.

## 53. Offene Theoriefragen

Zu klären sind unter anderem:

- ob der 5D-Adressraum funktionale Geometrie trägt;
- welche Plastizitätsmechanismen held-out Lernen tatsächlich verbessern;
- wann Replay als Konsolidierungsmechanismus mehr leistet als reine Wiederholung;
- ob semantische Verdichtung unter einer klar begründeten Spezialrolle zusätzlichen Nutzen besitzt;
- wann eine Vorhersagestruktur die Bezeichnung Weltmodell verdient;
- ob Prediction Error im SNN kausal Lernen oder Aktivität verbessert;
- wie soziale/mirrorartige Repräsentationen kausal geprüft werden;
- welche Definitionen für Selbstmodell, Agency und verschiedene Autonomieformen operational tragfähig sind;
- welche technischen Indikatoren für Bewusstseinsforschung überhaupt diskriminative Vorhersagen liefern, ohne Bewusstsein einfach vorauszusetzen.

## 54. Offene Safety-Forschung

Die wichtigsten offenen Safety-Stränge sind:

- Zielprovenienz und Zieltransformation;
- specification gaming;
- goal misgeneralization;
- Corrigibility und Safe Interruptibility;
- Optionsraum-/Power-Seeking-Proxies;
- Post-Objective Transition;
- Capability-Gates und out-of-band Stopppfade;
- reale Aktorik nur unter deny-by-default und auditierbarer Autorisierung;
- mögliche Konflikte zwischen Systemsafety und Welfare Precaution unter Unsicherheit.

Geplante Experimente werden nicht als bereits beobachtete Gefährlichkeit dargestellt.

## 55. Offene Meta-Forschung

Auch die Forschungsweise bleibt Untersuchungsgegenstand. Zu prüfen sind:

- Bias durch AI-assistierte Hypothesengenerierung;
- rekursive Quellenabhängigkeit, wenn AI-Systeme frühere MHRN-Texte wiedergeben;
- Abhängigkeit von einzelnen Tools/Providern;
- Selektionsbias in Literatur und Chat-Rekonstruktion;
- Governance von generiertem Code;
- Verständlichkeit und Fehlanreizrisiko der Engineering-/Scientific-Maturity-Achsen;
- externe Review- und Replikationsrollen;
- ob die rekursive-epistemische Gatewaystruktur tatsächlich zu weniger Fehlklassifikationen und transparenteren Architekturentscheidungen führt.

## 56. Prior Art, Attribution und externe Prüfung

Vor einer formalen wissenschaftlichen Einreichung bleiben mehrere Querschnittsaufgaben offen:

- systematischer Prior-Art-Review der Kandidatenbeiträge;
- menschliche Primärquellenprüfung zentraler Literaturargumente;
- externe Text- und gegebenenfalls Code-Similarity-Prüfung;
- unabhängige fachliche Review;
- Replikation wichtiger empirischer Ergebnisse außerhalb derselben Autoren-/Toolkette;
- saubere Kennzeichnung eigener Übersetzungen und wiederverwendeter Eigenpassagen.

Interne Audits reduzieren Risiken, ersetzen diese externen Schritte aber nicht.

## 57. Bestandslücken

Edition 1.8 erhebt die am Basiscommit versionierten Dateien und Markdown-Überschriften. Trotzdem gibt es Lücken:

- vollständige Account-weite historische Chattranskripte wurden nicht importiert;
- mehrere historische DOCX-Dateien liegen im Git nur als LFS-Zeiger vor;
- manche frühe Ideen sind nur retrospektiv rekonstruiert und daher S4;
- lokale oder externe Nebenprojekte sind nicht zwangsläufig vollständig repositoryweit geprüft;
- eine automatische Pfadzuordnung garantiert keine semantisch perfekte Klassifikation;
- nicht jede historische Literaturangabe früherer Editionen wurde für 1.8 erneut primär geprüft.

Diese Lücken bleiben sichtbar und dürfen spätere Rekonstruktionen korrigieren.

## 58. Definition of Done für den Weg zu 2.0

Die elf Hauptteile existieren bereits in 1.8. **Struktur allein ist deshalb kein verbleibendes 2.0-Kriterium mehr.** Für eine kanonische Hauptedition 2.0 müssen stattdessen Inhalt und Review reifen.

Mindestens erforderlich sind:

1. die wesentlichen bisherigen Forschungsbefunde in der neuen Struktur vollständig integriert und quellengebunden;
2. CL-003 menschlich reviewt und die SemanticMemory-Architekturentscheidung dokumentiert;
3. 5D-v2 entweder angemessen ausgeführt oder die Hypothese ausdrücklich weiter offen gestellt — kein inadäquater Ersatzbefund;
4. Stage-0-Referenzkonformität, Stage-4-/5-DATA und weitere zentrale Resultate mit klaren Claim-Grenzen in der Synthese;
5. stabile drei-Achsen-Methodik mit dokumentierten Evidenzregeln;
6. Safety- und Welfare-Governance als Querschnitt, nicht als Appendix;
7. Prior-Art- und Quellenprüfung für zentrale Kandidatenbeiträge;
8. externe Reviewpfade und mindestens erste unabhängige Replikationsschritte;
9. ein Viewer, der Current, Historical, Frozen, DATA, EVID und Quellenstatus korrekt sichtbar macht;
10. keine offenen bekannten Inkonsistenzen zwischen Registry, Experimentartefakten, Manuskript und Frontendprojektion.

2.0 entsteht damit nicht durch eine Versionsnummer oder weitere Textmenge, sondern durch **inhaltliche Integration, empirische Selektion, externe Prüfung und nachvollziehbare Revision**.

## 58.1 Restgrenze der Corpus-Vollständigkeit

Nach der vertieften Corpus-Integration sind die bekannten wissenschaftlich materiellen Vorarbeiten und kanonischen `docs/`-/`research/`-Stränge in einem eigenen Ledger erfasst und in der elfteiligen Synthese verortet. Trotzdem wird bewusst **keine semantische Vollständigkeit über jede der tausenden versionierten Repositorydateien zertifiziert**. Ein Buildskript, ein CSS-Asset oder ein historischer Update-Snapshot muss nicht als eigener wissenschaftlicher Gedanke in den Fließtext eingehen.

Die verbleibenden echten Bestandsgrenzen sind enger und konkret:

- DOCX-Dateien, deren Git-Objekt nur als LFS-Zeiger vorliegt, können ohne die zugehörigen Originalbytes nicht als vollständiger Textzeugenbestand geprüft werden;
- vollständige accountweite Chattranskripte sind nicht Bestandteil des Repositories; rekonstruierte Zusammenfassungen bleiben S4;
- nicht versionierte lokale oder externe Nebenprojekte können nur integriert werden, wenn ihre Quellen tatsächlich wiedergewonnen werden;
- historische Literaturangaben bleiben dann quarantänisiert, wenn ihre Primärquelle nicht erneut geprüft wurde;
- Raw DATA werden absichtlich nicht in den Manuskripttext dupliziert, sondern bleiben an ihren Experimentpfad gebunden.

Das Ziel lautet daher nicht „jeder Bytewert steht im Manuskript“, sondern: **jede bekannte wissenschaftlich materielle Vorarbeit hat eine nachvollziehbare Rolle in der Gesamtarbeit, während Primärartefakte an ihrem autoritativen Ort erhalten bleiben.**

## 58.2 Topologie v2 und saubere Determinismus-Replikation

Aus den aktuellen Entscheidungen entstehen zwei klar begrenzte nächste Schritte. Für `RQ-DET-001` ist ein clean-tree-Replikationslauf erforderlich, bevor ein durch Dirty-Tree-Provenienz blockiertes Artefakt regulär in Richtung EVID geprüft werden kann. Eine semantische Reklassifikation allein entfernt den Provenienzblock nicht.

Für `H-SNN-003-B` muss `topology_propagation_v2` **vor Ausführung** präregistriert werden. Der neue Aufbau muss Topologie durch Konstruktion auf Dynamik wirken lassen und zunächst ein Activity-Adequacy-Gate bestehen. Scheitert dieses Gate, ist der Hypothesentest `NOT_TESTED`, nicht negativ. Erst danach dürfen vorab definierte Vergleiche zwischen 1D/2D/3D/5D, `5d_shuffled` und einem degree-/density-matched `random_graph` interpretiert werden. Dabei wird ausdrücklich kein 5D-Vorteil vorausgesetzt; die Hypothese verlangt zunächst nur einen belastbaren Unterschied zwischen mindestens zwei Topologiebedingungen.

## 58.3 LP-20260917194217: offene Kompressionsprüfung

`LP-20260917194217` ist als nächster möglicher Stage-6-Zyklus vorbereitet und genehmigt, aber **noch nicht ausgeführt**. Der geplante Primärvergleich ist `semantic_prototype_replay_10pct_budget` gegen `raw_replay_full_budget`; die Erfolgsgrenze liegt bei mindestens 95 % der Raw-Replay-Retention bei Faktor-10-Speicherreduktion. `no_replay`, `random_prototype_10pct` und `learning_off` dienen als Kontrollen.

Vor Ausführung sind Source-Digests, Trust-Status, Freeze, Seed-/Taskplan und Analysevertrag zu vervollständigen. Bis dahin bleibt der Eintrag Forschungsplanung und darf im Viewer nicht wie ein Ergebnis oder laufendes Experiment erscheinen.

## 58.4 Aktueller Review-Stand und unmittelbar nächste Replikationen

Nach dem jüngsten Human Review ist die offene Determinismusfrage enger als zuvor. `RQ-DET-001 / H-SNN-003-A` hat im historischen `deterministic_replica_v1`-Datensatz einen positiven Same-Seed-Replica-Befund und ist semantisch `DIRECT_MATCH`. Offen ist nicht mehr die Frage, ob die registrierten Replica-Bedingungen zur RQ gehören, sondern ob derselbe Befund in einem **clean-tree, hash-gebundenen Replikationslauf** wiederholt wird. Erst danach ist eine reguläre Human-EVID-Entscheidung sinnvoll.

Für `H-SNN-003-B` ist der nächste Schritt ebenfalls klarer: `EXP-GEN-0047` gilt nicht als negativer Befund, sondern als `INADEQUATE_TO_TEST_HYPOTHESIS`. `topology_propagation_v2` muss daher vor Ausführung mindestens folgende Merkmale einfrieren: mindestens 1.000 Neuronen pro Bedingung, im Mittel mindestens 10 eingehende Synapsen pro Neuron, degree-/density-matched Vergleiche, explizite Kopplung von Geometrie an Konnektivitätswahrscheinlichkeit und/oder Delay, Multi-Neuron-Stimulus, Activity-Adequacy-Gate, vorab definierte first-arrival-/reach-Endpunkte, unabhängige Seeds sowie saubere Source-/Graph-Provenienz. Diese Schwellen sind Mindestanforderungen für die nächste Testgeneration, keine universellen Suffizienzkriterien.

Damit sind die nächsten beiden methodischen Schritte **Replikation** und **Testadäquanz**, nicht weitere Interpretation derselben historischen DATA.


---

# Anhang — Quellen und Vorarbeiten

[Alle Forschungsfragen und Hypothesen](RESEARCH_REGISTER.md) · [Quellenindex](SOURCE_INDEX.md) · [Semantische Corpus-Integration](CONTENT_INTEGRATION.md) · [Ungekürzter Quellenband 1.7](LEGACY_V17.md) · [Weitere Vorarbeiten](PRIOR_WORK_MAP.md) · [Literatur](REFERENCES.md) · [Prüfmanifest](manifest.json).

Die Quellenbestandsaufnahme belegt referenzierte Datei-Erhaltung am angegebenen Commit, nicht die vollständige semantische Erfassung jeder Idee. Die außerhalb des Repositories rekonstruierte Vorgeschichte ist ausdrücklich unvollständig.
