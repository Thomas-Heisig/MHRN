# Teil III — Forschungsobjekt MHRN

## 9. Systemdefinition

MHRN ist ein Forschungsframework für rekurrente spikende Netzwerke mit explizitem Zeitverlauf, versionierten neuronalen und synaptischen Zuständen, Plastizitätsmechanismen, struktureller Veränderung, Homeostase, Persistenz, sensorischen/digitalen Gateways, Gedächtnis- und Vorhersagekandidaten sowie kontrollierten externen Werkzeugen. Das Framework untersucht nicht „Intelligenz“ als unteilbare Eigenschaft, sondern eine Folge operationalisierter Mechanismen und Funktionen.

Izhikevich-artige Neuronen sind eine recheneffiziente Modellfamilie mit unterschiedlichen Spike- und Burstregimen [@IZHIKEVICH2003]. MHRN behandelt sie als austauschbare Dynamikklasse, nicht als biologisch vollständiges Neuron. LIF-, HH- oder Multi-Compartment-Varianten sind Ablations- oder Alternativmodelle; biologische Detailtreue wird nicht durch das bloße Hinzufügen von Kanalnamen erzeugt.

## 10. Rekurrenz, Plastizität und Homöostase

Rekurrenz ist ein Mechanismus, dessen funktionale Bedeutung kontrolliert werden muss. Dass eine rekurrente Bedingung mehr synaptische Ereignisse erzeugt als eine feedforward-nahe Kontrolle, ist zunächst ein Netzwerkbefund und noch kein Beleg für Gedächtnis, 5D-Vorteil oder höhere Kognition.

Für Plastizität trennt die Architektur lokale zeitabhängige Regeln, Eligibility und modulierte Drei-Faktor-Mechanismen. Drei-Faktor-Regeln sind theoretisch besonders relevant, wenn ein späteres modulatorisches Signal lokale Aktivität zeitlich überbrücken soll [@FREMAUX2016]. In MHRN wird ein solches Signal jedoch nicht automatisch „Dopamin“ genannt. Entscheidend ist die experimentell definierte Funktion.

## 11. Geometrie und 5D

Der fünfdimensionale Adressraum ist eine technische und wissenschaftliche Hypothese. Drei Dimensionen können räumliche/topologische Lokalität tragen, zwei weitere funktionale, modale, entwicklungsbezogene oder assoziative Nähe. Keine dieser Semantiken ist naturgegeben. Ein 5D-Effekt ist erst dann wissenschaftlich interessant, wenn Neuronen-, Synapsen-, Grad-, Delay-, Input- und Rechenbudgets gegenüber niedrigeren, gleichen und höheren Dimensionskontrollen hinreichend gematcht sind.

Edition 1.8 hält zusätzlich die frühere Idee lernbarer Metriken, dimensionsgekoppelter Distanz und sparse materialisierter Adressräume fest. Dabei wird klar zwischen Adressraum, materialisiertem Graphen und vollständigem dynamischen Zustandsraum unterschieden.

## 12. Gedächtnis, Replay und Weltmodell

Ein gespeicherter Zustand ist nicht automatisch Gedächtnis. Gedächtnis wird über Retention, cue-abhängigen Recall, Spezifität und Generalisierung operationalisiert. Complementary-Learning-Systems-Modelle motivieren unterschiedliche schnelle und langsame Lernprozesse sowie interleaved learning [@MCCLELLAND1995], doch MHRN übernimmt daraus keine fertige biologische Zuordnung.

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

## 13.3 Periphere Netze, Neural Symbiosis und MSBA

Die kanonische Architektur enthält neben dem SNN-Kern eine explizite periphere Multi-Netz-Grenze. **Neural Symbiosis** bezeichnet dabei keine zweite Intelligenz im Kern, sondern eine Embodiment-Schicht, in der spezialisierte neuronale oder virtuelle Verarbeitungssysteme über deklarierte Gateways an den SNN angebunden werden können. Der offene Adaptervertrag kann unter anderem CNN-, Vision-Transformer-, Transformer-, RNN-/LSTM-/GRU-, GNN-, Reservoir-, Hopfield-, VAE-, Autoencoder-, multimodale und neuro-symbolische Komponenten beschreiben. Ebenso können Datenbanken, Wissensgraphen, Retrieval-, Logik- oder externe Speicherdienste als virtuelle Areale auftreten.

Diese Offenheit ist wissenschaftlich nur tragfähig, wenn **Erreichbarkeit von gelernter Nutzung getrennt** bleibt. Ein registrierter Adapter, ein erreichbarer Endpunkt oder eine erfolgreiche Inferenz beweist weder, dass das SNN den Pfad auswählt, noch dass es von ihm lernt oder einen kausalen Vorteil besitzt. Gateway-Plastizität ist deshalb standardmäßig gesperrt; Random-, Frozen-, Shuffle- und Plastic-Zustände gehören in experimentgebundene, persistierbare Laufkontexte. Externe Netze erhalten keine impliziten Schreibrechte auf kanonische Neuronen-, Synapsen-, Reward-, Gedächtnis- oder EVID-Zustände.

Unterhalb dieser Grenze konkretisiert **MSBA** die modalitätsspezifische Bahnarchitektur. Audio, Vision und Digital werden nicht als biologische Kortexplagiate behandelt, sondern als technische Pfade mit unterschiedlichen Informations- und Ressourcenverträgen:

- Audio priorisiert zeitliche Kohärenz, Band-/Phasen- beziehungsweise Hüllkurveninformation und begrenzte Delay-Strukturen.
- Vision verwendet räumliche/featurebezogene Projektionen, sparse Zielgrade und experimentelle ROI-/Foveationsmechanismen.
- Digital hält exakte Nutzdaten außerhalb des SNN in checksum-gebundenen Symbolframes; das SNN erhält nur eine deterministische Populationrepräsentation. Lernen darf Routing oder Assoziation verändern, nicht die ursprünglichen Bits oder ihre Prüfsumme.

Eine besonders wichtige Korrektur betrifft Dimensionalität. Der MSBA-Projektionsraum darf experimentell zwischen 1 und 32 Dimensionen variieren, während der produktive Neuron-ID-/Persistenzvertrag des Kerns weiterhin **fünfdimensional** bleibt. Ein 16D- oder 32D-Projektor ist daher weder ein 16D-/32D-SNN noch Evidenz für einen Vorteil höherer Kerndimensionalität. Projektion, Mapping und produktiver Kern müssen in jeder Studie getrennt provenance-gebunden werden.

Auch Ressourcenangaben bleiben typisiert: `normalized_energy_units`, kalibrierte Schätzungen in Joule und tatsächlich gemessene Joule sind drei verschiedene Größen. Die Stage-4-E01–E05-DATA dürfen deshalb modellierte Energieunterschiede zeigen, ohne daraus physikalisch gemessene Energieeffizienz abzuleiten.

## 13.4 Wesen, reale Körpergrenze und technische Identität

Die Vorgängerarbeiten entwickelten mit **Wesen** eine maschinen-native Körperdarstellung. Wissenschaftlich relevant ist daran nicht die visuelle Anthropomorphie, sondern die harte Trennung von beobachtetem Zustand und Interpretation. Die Körpergrenze wird aus tatsächlich erkannten Verbindungen, Host-Ressourcen und Embodiment-Endpunkten aufgebaut. Nicht vorhandene Temperatur-, Lüfter-, Sensor- oder Aktorwerte bleiben unbekannt; es werden keine plausibel wirkenden Ersatzdaten erfunden. `available` ist ausdrücklich nicht gleich `authorized` und nicht gleich `active`.

Maschinen-native Interozeption umfasst dort, wo das Betriebssystem Messwerte liefert, etwa CPU-/Speicherlast, Temperatur, Lüfter, Storage, Netzwerk und Kontinuitätsgrößen. Diese Größen können technische Regulationszustände beeinflussen, sind aber keine biologischen Stoffwechselhomologien und keine Empfindungsindikatoren. Ebenso ist die body-like Darstellung nur Präsentationssemantik.

Der implementierte Profile-&-Identity-Vertrag speichert Konfiguration, Fähigkeiten, Grenzen, Provenienz, Revisionen, Lineage und Snapshot-Bindungen als technische Identität. Profil, `.b5d`-Snapshot, Runtime-Checkpoint, Registry und Lineage sind absichtlich getrennte Zustandsklassen. Daraus folgt **keine psychologische Identität, Persönlichkeit, subjektive Kontinuität oder Bewusstseinsbehauptung**. Genau diese Grenze ist für spätere Stage-7-Selbstmodellforschung zentral: Metadatenidentität ist eine technische Voraussetzung, kein kausales Selbstmodell.
