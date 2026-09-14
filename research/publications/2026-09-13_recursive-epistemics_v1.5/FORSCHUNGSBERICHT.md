# MHRN - Forschungsarbeit, Fassung 1.5

**Thomas Heisig | 13. September 2026**

Eigenstaendige wissenschaftliche Forschungsarbeit mit Quellenstand, Architektur, Methoden, vollstaendiger aktueller Messbilanz, Diskussion und Grenzen. Menschliches Review ausstehend; keine automatische Evidenzfreigabe. Die historische Gesamtabhandlung ist separat im Dissertationsmanuskript enthalten.

# Quellenbindung und Zusammenfassung

Kampagne `EXP-EMP-20260913-A3` auf Commit `531f12335ebeebd7242beb4ba0bd95e81b3dfb8e`.

70 ausgewiesene Ausfuehrungen; Status `{'completed': 70}`; 2043 gespeicherte Datensaetze. 25 menschliche Vorlagen werden nicht als Experimente ausgegeben. Die Unterscheidung zwischen Simulation, Grenzaudit, Komponentenfunktion und menschlicher Entscheidung bestimmt die Reichweite aller Aussagen.

Ein protokollierter Lauf, eine bestandene Softwarepruefung und eine wissenschaftliche Annahmeentscheidung bleiben verschiedene Objekte. Die Ausgabe dokumentiert auch verfehlte wissenschaftliche Erfolgskriterien.



# Architektur, Formalismus und wissenschaftliche Reichweite

## Gegenstand und Beitrag

MHRN ist ein experimentelles Framework für rekurrente spikende Netze mit kontrollierter Plastizität und expliziten Systemgrenzen. Die wissenschaftliche Leistung wird nicht durch die Anzahl der Module definiert, sondern durch prüfbare Beziehungen zwischen Mechanismus, Intervention, Beobachtung und Schlussfolgerung. Diese Fassung verbindet die vollständige theoretische Abhandlung mit einer quellengebundenen Neubewertung der ausgeführten Protokolle.

Der Ausdruck Rekursive Epistemik bezeichnet hier eine Untersuchung der Herkunft, Verarbeitung und Kontrolle von Wissen in technisch geschlossenen und zugleich extern entworfenen Systemen. Er ist kein Messwert und keine Behauptung einer neuen physikalischen Dimension. MHRN trennt den primären adaptiven SNN-Zustand von Sprachmodellen, externen Datenbeständen und menschlichen Entscheidungen. Diese Trennung macht Zuschreibungen kontrollierbar; sie beweist nicht, dass jede beobachtete Leistung aus dem neuronalen Kern stammt.

## Punktneuronen und numerischer Vertrag

Das Izhikevich-Modell [1] beschreibt Membranvariable v und Recovery-Variable u durch

$$\dot v = 0.04v^2+5v+140-u+I,\qquad \dot u=a(bv-u).$$

Nach dem definierten Schwellenereignis erfolgt der Reset v auf c und die Erhöhung von u um d. Der verwendete diskrete Algorithmus ist von diesen kontinuierlichen Gleichungen zu unterscheiden: Integrationsschritt, Reihenfolge der v-/u-Aktualisierung, Spike-Erkennung, Refraktärbehandlung und Zustandserfassung gehören zum prüfbaren Vertrag. In der isolierten Referenz dürfen sekundäre Adaptationsmechanismen einen Modellvergleich nicht unbemerkt verändern. Der alternative LIF-Pfad ersetzt den Membranintegrator; er ist nicht einfach ein zusätzlicher Stromterm.

Die implementierten Varianten stehen in `src/core/neuron.py` und `src/core/neuron_models.py`. Der externe Einzelzellvergleich liegt in `src/research/empirical_evaluation.py`. Brian2 unterscheidet explizite Ausführungsphasen und die Phase eines Monitors [2,3]. Deshalb sind identische Modellgleichungen allein kein Nachweis identischer diskreter Spikefolgen. Ein nicht bestandenes Konformitätskriterium bleibt ein negativer Befund; eine nachträgliche Toleranzlockerung wäre ein neues Protokoll und keine Korrektur der alten Daten.

## Rekurrenz, Identität und Raum

Der kanonische Kern benutzt kompatible fünfdimensionale Koordinaten und verzögerte Ereignisse. Eine Koordinate ist ein technischer Adress- und Topologieparameter, keine zusätzliche Raumzeit. Entscheidend sind die tatsächlich erzeugten Kanten, Gewichte, Verzögerungen und Eingänge. Die Dimensionsstudien unterscheiden daher veränderte Graphgeometrie von einem bloß veränderten Label auf identischem Graphen. Vergleichbare Knoten- und Kantenbudgets beseitigen nicht automatisch Unterschiede in Eingangsgrad, Motiven oder erreichbaren Pfaden.

Die Aussage, ein rekurrentes Netzwerk sei technisch vorhanden, lässt sich an Laufzustand, Ereignisübertragung, Wiederholung und Wiederherstellung prüfen. Die weitergehende Behauptung eines nützlichen, robusten rekurrenten Rechenmechanismus verlangt eine aufgabenbezogene Intervention, etwa Rekurrenz an/aus bei sonst gleichen Bedingungen. Bloße Spikezahl, endliche Spannung oder ein sichtbarer Graph ersetzen diese Intervention nicht.

## Lernen und mehrere Zeitskalen

STDP koppelt Gewichtsänderung an die zeitliche Beziehung prä- und postsynaptischer Ereignisse. Eine Drei-Faktor-Regel verbindet diese lokale Vorbedingung mit einem zusätzlichen modulatorischen Signal. Als abstraktes Schema, nicht als vollständige Spezifikation jeder implementierten Variante, gilt

$$\dot e_{ij}=-e_{ij}/\tau_e+F(s_i,s_j),\qquad \Delta w_{ij}=\eta\,r\,e_{ij}.$$

Die konkreten Vorzeichen, Schranken, Zeiteinheiten und Aktualisierungszeitpunkte sind dem eingefrorenen Code und der Konfiguration zu entnehmen. Der mechanistische Gedanke einer zeitlich überdauernden Eligibility-Trace ist in der Literatur motiviert [4]. Der Literaturbezug ist jedoch kein Wirksamkeitsnachweis der MHRN-Implementierung.

Der Stage-3-Vertrag verbindet Tests von STDP, Reward/Eligibility, Homöostase, struktureller Plastizität und checkpointbarem Lernzustand mit deterministischen Learning-on/off/Sham-Kontrollen. Diese Batterie prüft mehrere Komponenten und einen begrenzten Lernversuch. Sie ist nicht mit einem einzigen gleichzeitig vollplastischen Langzeitnetz aus 100.000 Neuronen gleichzusetzen. Insbesondere sind eine Gewichtszunahme, eine geänderte Probeantwort und eine Verbesserung auf wirklich neuen Testepisoden verschiedene Endpunkte.

## Homöostase und strukturelle Plastizität

Feuerraten-, Schwellen- und Energiekontrollen begrenzen ausgewählte Zustandsgrößen. Eine lokale Schranke beweist weder globale asymptotische Stabilität noch die Stabilität unter allen Reglerkombinationen. Mehrere Regelkreise können gegeneinander arbeiten; identische Endzustände können durch verschiedene Beiträge entstehen. Deshalb sind mechanistische Ablationen, aufgezeichnete Reglerbeiträge, Störungen und Erholungsmaße erforderlich.

Strukturelle Veränderungen besitzen einen Freigabe- und Persistenzpfad statt eines unsichtbaren direkten Eingriffs. Vorschlag, Entscheidung, begrenzte Mutation, Journal und Wiederherstellung sind Engineering-Verträge. Ein nachweisbarer Mutationseintrag ist noch kein Beleg, dass die neue Topologie eine Aufgabe besser löst. Diese Unterscheidung gilt auch für Heatmaps und historische Strukturansichten.

## Erweiterte biophysikalische Modelle

Der Quellstand enthält experimentelle Klassen und Verträge für Hodgkin-Huxley-artige Kanäle, Kompartimente, NMDA-artige Nichtlinearität, Gap Junctions, Astrozyten-/Mikroglia-Modelle, langsame Konsolidierung, Rezeptor-Trafficking und stochastische synaptische Freisetzung. Deren konkrete Modelle sind in den entsprechenden `src/core`-Modulen und den Ablationstests offengelegt. Sie erweitern den Modellraum; sie sind kein Nachweis einer biologischen Vollsimulation.

Das Vorhandensein einer Klasse bedeutet nicht, dass diese Mechanik im produktiven Runtime-Pfad, in jedem Snapshot oder in allen Skalierungsversuchen aktiviert ist. Modellwahl, Integrator, Parameter und aktivierte Nebenmechanismen müssen pro Versuch aufgezeichnet werden. Eine biologische Interpretation benötigt darüber hinaus unabhängige Referenzdaten, Identifizierbarkeit und anwendungsbezogene Validierung.

## Speicher, Kognition und Körpergrenze

Snapshots, Delta- und Strukturjournale dienen reproduzierbarer Fortsetzung. Die Aussage gilt jeweils für den vertraglich erfassten Zustand. Ein funktionierender Core-Checkpoint beweist nicht automatisch die deterministische Wiederherstellung eines gekoppelten Gesamtsystems aus Working Memory, episodischem Speicher, Weltmodell, Behavior Profile, Gateway und externen Diensten. Diese gekoppelte Grenze bleibt gesondert zu prüfen.

Die vorhandenen Kognitionskomponenten sind begrenzte technische Funktionen: Speicherzugriff, Ein-Schritt-Vorhersage und Auswahl zwischen expliziten Aktionskandidaten. Die Studien prüfen diese Komponenten und ihre Kontrollarme. Weder ein besserer Prädiktionswert noch ein adaptierter Profilparameter allein rechtfertigt Begriffe wie subjektives Selbst, allgemeines Weltverständnis oder autonome Zielbildung.

Sensoren und Aktoren sind explizit autorisierte Adapter. Ein fehlendes Gerät wird nicht durch eine plausible Kamera- oder Audiodatenquelle ersetzt. Die Körperansicht ist eine Projektion beobachteter technischer Verbindungen. Closed-loop-Leistung muss gegen Replay/Open-loop, wirkungslose Aktoren und Sensorstörungen abgegrenzt werden. Dabei ist der Beitrag vorgeschalteter Regler und externer Modelle offenzulegen.

## Gateway, exakte Daten und CUDA

Das Gateway trennt exakte digitale Payloads von neuronalen Repräsentationen sowie Codec, Projektion und Gateway-Lernen. Experimentelle Frozen-/Random-/Shuffle-Kontrollen erlauben begrenzte Funktionsprüfungen. Erreichbarkeit eines Endpunkts und korrekte Checksummen sind notwendige technische Eigenschaften, aber kein Beleg eines gelernten semantischen Verständnisses.

Der neue Gateway-Neural-Interface-Vertrag v0.4 und der CUDA-Vertrag v0.3 sind Architekturarbeit. Der CUDA-Text erklärt selbst, dass noch keine CUDA-Implementierung vorliegt. CPU-Messungen, theoretische Speicherbudgets oder ein beschriebenes Kernel-Layout werden deshalb nicht als gemessene GPU-Beschleunigung ausgegeben. Externe Projektionsräume von 1 bis 32 Dimensionen sind vom weiterhin fünfdimensionalen Persistenz-/ID-Vertrag zu unterscheiden.

## Beobachtbarkeit statt Darstellungswirkung

Dashboard, Chat und File Viewer sind Werkzeuge zur Inspektion. Die zentrale Ausgabe soll dieselben kanonischen Artefakte erschließen und unbekannte Werte als unbekannt anzeigen. Der Audit behebt deshalb rekursive Dokument-Cache-Aufrufe und bindet Frontend-Prüfungen an tatsächlich geladene Stylesheets und den aktuellen Router. Solche Reparaturen verbessern Verfügbarkeit und Prüfbarkeit, erzeugen aber keine neue wissenschaftliche Evidenz.


# Methodik, Ausführung und statistische Interpretation

## Quellenstand und Auswahl

Die Kampagne wird vor dem ersten Protokoll auf einen Git-Commit, einen Digest der relevanten Quellen, eine konkrete Konfiguration und eine vollständige Auswahl gebunden. Code und wissenschaftlicher Plan müssen sauber sein. Jeder Versuch startet in einem eigenen Prozess; die Prozesse werden seriell ausgeführt. Ausgaben liegen während der Messung außerhalb des Quellbaums. Nach Ende wird die Quellenidentität erneut geprüft.

Die Auswahl ist eine erneute explorative Ausführung registrierter Verträge. Eine Registrierung im eigenen Repository wird nicht als unabhängige externe Präregistrierung ausgegeben. Neue Analysen dieser Daten sind nachträgliche Interpretation, sofern kein vorher eingefrorener Auswertungsvertrag das konkrete Verfahren bereits nennt. Weitere wissenschaftliche Freigabe bleibt ein separater, menschlicher Schritt.

Die Ausführungskategorien werden nicht zusammengerechnet, als hätten sie denselben Erkenntniswert. Ein direkt instrumentiertes Funktionsprotokoll, eine Grenzprüfung, eine kombinierte Engineering-Suite und ein Fragebogen sind verschiedene Instrumente. Grenzprüfungen dokumentieren beispielsweise eine fehlende Operationalisierung oder eine Schutzgrenze; sie beantworten nicht automatisch die zugeordnete inhaltliche Hypothese. Menschliche Vorlagen werden nicht mit automatisch ausgefüllten Antworten ersetzt.

## Beobachtungen, Provenienz und Ausfälle

Pro Protokoll werden Auswahl, Manifest, komprimierte Rohdaten und ein Receipt mit SHA-256 der komprimierten und unkomprimierten Bytes gespeichert. Vor der Auswertung werden beide Digests sowie Identität, Status und Zahl der Datensätze abgeglichen. Ein fehlender oder widersprüchlicher Beleg macht den Auswertungszweig ungültig. Nichtendliche numerische Werte und dokumentierte Runtime-Fehler werden nicht zu unauffälligen Nullwerten geglättet.

Für jede beobachtete Bedingung wird geprüft, ob alle deklarierten Seeds vorkommen. Diese Prüfung allein beweist nicht, dass die Implementierung alle wissenschaftlich beabsichtigten Bedingungen erzeugt: Dafür bleibt der Vergleich von Protokolltext, Runner und aufgezeichneten Bedingungsnamen notwendig. Ein Prozess-Timeout und ein negatives Hypothesenergebnis sind ebenfalls verschieden. Ein korrekt ausgeführter Versuch darf das Erfolgskriterium verfehlen, ohne als Laufzeitfehler umgedeutet zu werden.

Einzelne Seeds, Bedingungen, Episoden und Ticks sind nicht austauschbare Stichprobeneinheiten. Die berichtete Anzahl gespeicherter Zeilen ist deshalb ein Rechenschaftsmaß, nicht automatisch eine inferentielle Stichprobengröße. Deterministisch identische Resultate unter verschiedenen Seed-Labels liefern keine unabhängigen stochastischen Wiederholungen. Bei gepaarten Armen ist der unabhängige Initialisierungs-/Umwelt-Seed die zentrale Analyseeinheit.

## Vorhandene Kontraste

Der Assoziationsversuch verwendet frische Testepisoden, eingefrorene Gewichte und Kontrollen mit deaktiviertem Lernen, Sham-Replay, zurückgesetzten und permutierten Gewichten. Ein Trainingseffekt ist nur dann von bloßer Gewichtsänderung zu unterscheiden, wenn die gehaltene Testinformation nicht schon als Teacher-Signal oder Parameterwahl in das Ergebnis eingeht. Die konstruierten Eingabepopulationen und die externe Anleitung während der Akquisition sind Teil der Behandlung und werden nicht verborgen.

Die vorhandene Auswertung verwendet gepaarte Seed-Differenzen, Bootstrap-Perzentilintervalle und einen exakten zweiseitigen Vorzeichenwechseltest für die dafür vorgesehenen Zehn-Seed-Vergleiche. Ein solcher Test setzt die für die Nullhypothese geeignete Austauschbarkeit beziehungsweise Symmetrie voraus; das Verfahren beweist seine Voraussetzungen nicht selbst [5]. Holm-Korrektur wird innerhalb der jeweils deklarierten Kontrastfamilie berichtet. Sie korrigiert nicht nachträglich die gesamte explorative Suche über sämtliche Protokolle.

Die Dimensionsauswertung vergleicht Aufgabenobservablen bei geänderter Graphgeometrie und kontrolliert separat die Wirkung bloßer Dimensionslabels. Ein Intervall, das null einschließt, ist kein Äquivalenzbeweis. Das Fehlen eines signifikanten 5D-Vorteils kann aus einem kleinen oder variablen Effekt, unzureichender Präzision oder mangelnder Aufgabensensitivität entstehen. Die zulässige Aussage bleibt daher auf die gemessene Aufgabe, Budgets und Kontraste begrenzt.

## Stabilität, Ressourcen und Skalierung

Lange stabile Referenzläufe prüfen den gewählten Antrieb und die gewählte Topologie. Ein stilles Netz ist nicht automatisch ein nützlich rechnendes Netz. Deshalb werden Nullinput, tonischer Antrieb, Spikes, synaptische Zustellung und Zustandsgrenzen getrennt betrachtet. Die maximale Zahl ausführbarer Ticks ist kein Ersatz für kontrollierte Langzeitlernstabilität.

Skalierungstabellen nennen nur die tatsächlich gespeicherten Größen und Messfenster. Die große Knotenzahl eines kurzen Sparse-Runs darf nicht mit einem langdauernden, vollplastischen, hochaktivierten biologischen Netz gleichgesetzt werden. RSS beinhaltet Interpreter und Bibliotheken und ist keine isolierte Spitzenallokation. CPU-Zeit, Simulationszeit und Wandzeit sind verschieden. Softwareinterne Energie- oder Ressourceneinheiten sind ohne physikalische Kalibrierung keine Joule.

Serielle Prozesse reduzieren direkte Konkurrenz innerhalb einer Kampagne, garantieren jedoch keinen exklusiven physikalischen Host. Die Umgebung wird deshalb mit Plattform, Python-/Paketversionen, CPU-Zahl und relevanten Thread-Variablen protokolliert. Leistungsaussagen gelten für diese Umgebung. Gleichzeitige lokale Diagnostik, Betriebssystemlast, Warm-up und Importkosten sind mögliche Störfaktoren; es wird kein fairer plattformübergreifender Geschwindigkeitsrekord behauptet.

## Reproduzierbarkeit und Unabhängigkeit

Reproduktion bedeutet hier, die dokumentierte Software unter den deklarierten Bedingungen erneut auszuführen. Eine unabhängige Replikation verlangt darüber hinaus geeignete personelle beziehungsweise methodische Unabhängigkeit. Ein Runner mit dem Wort independent im Namen erfüllt diese Bedingung nicht durch seinen Namen. Das gilt ebenso für ein KI-generiertes Review: Es bleibt eine Interpretation mit offengelegter Assistenz, keine unabhängige Fachentscheidung.

Die bisherigen Ausgaben und Messdaten bleiben unverändert. Eine Quellen- oder Instrumentierungsreparatur erzeugt eine neue Version und neue Beobachtungen. Die alte Nullbeobachtung, ein fehlerhafter Skalierungsversuch oder ein nicht bestandener Frameworkvergleich wird nicht durch spätere Daten ersetzt. Softwareversion 0.6.0-alpha.3 und Publikationsfassung 1.5 bezeichnen unterschiedliche Artefakte.


# Ergebnisse der aktuellen Gesamtkampagne

Kampagne: **EXP-EMP-20260913-A3**. Quellcommit: `531f12335ebeebd7242beb4ba0bd95e81b3dfb8e`. Quelldigest: `1e383330cb8b50a1821dd61d000dc3747dd5f58ee4c0bbc00c6d11ed5e149eb0`.

Ausfuehrungsstatus: `{'completed': 70}`; **2043 gespeicherte Seed-/Bedingungsdatensaetze**. Dies ist keine Anzahl unabhaengig bestaetigter Hypothesen.

Kategorien: `{'registered_simulation': 21, 'functional_experiment': 21, 'boundary_audit': 27, 'composite_engineering_screen': 1}`. Menschliche Vorlagen: **25**, nicht automatisch bearbeitet. Akzeptierte EVID aus dieser Kampagne: **keine**.

## Gepaarte Kontraste

Die folgenden Werte werden aus den gespeicherten Analysen uebernommen. Intervalle sind punktweise Bootstrap-Perzentilintervalle; die Holm-Korrektur gilt innerhalb der jeweiligen Kontrastfamilie, nicht fuer die gesamte explorative Kampagne.

### dimensional_connectivity_v1

**geometry_5d minus geometry_2d**: n = 10 gepaarte Seeds; mittlere Differenz 5; 95%-Intervall [-2.4, 11.7]; p exakt 0.234375; p Holm 1.

**geometry_5d minus geometry_3d**: n = 10 gepaarte Seeds; mittlere Differenz -3; 95%-Intervall [-9.4, 4.6]; p exakt 0.4628906; p Holm 1.

**geometry_5d minus geometry_4d**: n = 10 gepaarte Seeds; mittlere Differenz 2.4; 95%-Intervall [-2.9, 7.7]; p exakt 0.421875; p Holm 1.

**geometry_5d minus geometry_6d**: n = 10 gepaarte Seeds; mittlere Differenz 0.3; 95%-Intervall [-4.5, 4.8]; p exakt 0.921875; p Holm 1.

**geometry_5d minus geometry_8d**: n = 10 gepaarte Seeds; mittlere Differenz 2.8; 95%-Intervall [-3.4, 9.6]; p exakt 0.46875; p Holm 1.

### native_association_holdout_v1

**learning_on minus learning_off**: n = 10 gepaarte Seeds; mittlere Differenz 0.285; 95%-Intervall [0.2, 0.37]; p exakt 0.001953125; p Holm 0.0078125.

**learning_on minus sham_replay**: n = 10 gepaarte Seeds; mittlere Differenz 0.285; 95%-Intervall [0.2, 0.37]; p exakt 0.001953125; p Holm 0.0078125.

**learning_on minus weight_reset**: n = 10 gepaarte Seeds; mittlere Differenz 0.285; 95%-Intervall [0.2, 0.37]; p exakt 0.001953125; p Holm 0.0078125.

**learning_on minus weight_shuffle**: n = 10 gepaarte Seeds; mittlere Differenz 0.285; 95%-Intervall [0.2, 0.37]; p exakt 0.001953125; p Holm 0.0078125.

## Kernaussage und Grenzen

Die native Assoziationsaufgabe liefert unter den erfassten Kontrollen einen positiven aufgabenspezifischen Lernbefund. Die Dimensionskontraste tragen keinen belastbaren allgemeinen Vorteil von 5D. Der strenge Brian2-Abgleich verfehlt das deklarierte Konformitaetskriterium. Diese Befunde sind voneinander getrennt zu bewerten; keiner etabliert Bewusstsein, biologische Gleichwertigkeit oder allgemeine Intelligenz.

## Vollstaendige Protokollbilanz

n bezeichnet gespeicherte Zeilen pro Bedingung. Primarmaesse werden als Mittel [Minimum; Maximum], boolesche Ergebnisse als true/n ausgegeben. Strukturierte oder nicht vorhandene Endpunkte werden nicht erfunden. Vollstaendige Rohdaten und Receipts sind Teil der Kampagne.

### 01. recurrence_map_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 300; Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]`; Ticks: `256`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**w0_d1** (n = 20): last_response_latency: 2 [2; 2]; recurrent_events: 0 [0; 0]; propagation_depth: 1 [1; 1]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w0_d2** (n = 20): last_response_latency: 2 [2; 2]; recurrent_events: 0 [0; 0]; propagation_depth: 1 [1; 1]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w0_d4** (n = 20): last_response_latency: 2 [2; 2]; recurrent_events: 0 [0; 0]; propagation_depth: 1 [1; 1]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w100_d1** (n = 20): last_response_latency: 62 [62; 62]; recurrent_events: 10 [10; 10]; propagation_depth: 61 [61; 61]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w100_d2** (n = 20): last_response_latency: 252 [252; 252]; recurrent_events: 33 [33; 33]; propagation_depth: 251 [251; 251]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w100_d4** (n = 20): last_response_latency: 251 [251; 251]; recurrent_events: 28 [28; 28]; propagation_depth: 250 [250; 250]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w125_d1** (n = 20): last_response_latency: 84 [84; 84]; recurrent_events: 14 [14; 14]; propagation_depth: 83 [83; 83]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w125_d2** (n = 20): last_response_latency: 255 [255; 255]; recurrent_events: 34 [34; 34]; propagation_depth: 254 [254; 254]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w125_d4** (n = 20): last_response_latency: 250 [250; 250]; recurrent_events: 30 [30; 30]; propagation_depth: 249 [249; 249]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w50_d1** (n = 20): last_response_latency: 7 [7; 7]; recurrent_events: 1 [1; 1]; propagation_depth: 6 [6; 6]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w50_d2** (n = 20): last_response_latency: 8 [8; 8]; recurrent_events: 1 [1; 1]; propagation_depth: 7 [7; 7]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w50_d4** (n = 20): last_response_latency: 10 [10; 10]; recurrent_events: 1 [1; 1]; propagation_depth: 9 [9; 9]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w75_d1** (n = 20): last_response_latency: 25 [25; 25]; recurrent_events: 4 [4; 4]; propagation_depth: 24 [24; 24]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w75_d2** (n = 20): last_response_latency: 29 [29; 29]; recurrent_events: 4 [4; 4]; propagation_depth: 28 [28; 28]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**w75_d4** (n = 20): last_response_latency: 57 [57; 57]; recurrent_events: 6 [6; 6]; propagation_depth: 56 [56; 56]; persistence_class: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/001-recurrence_map_v1/`.

### 02. learning_generalization_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 180; Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]`; Ticks: `None`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**learning_off_drive_0.85** (n = 20): generalization_success: 0/20 true; p_success_after: 0 [0; 0]; mean_weight_delta: 0 [0; 0]

**learning_off_drive_1.00** (n = 20): generalization_success: 0/20 true; p_success_after: 0 [0; 0]; mean_weight_delta: 0 [0; 0]

**learning_off_drive_1.15** (n = 20): generalization_success: 0/20 true; p_success_after: 0 [0; 0]; mean_weight_delta: 0 [0; 0]

**learning_on_drive_0.85** (n = 20): generalization_success: 20/20 true; p_success_after: 1 [1; 1]; mean_weight_delta: 0.4672805 [0.4672805; 0.4672805]

**learning_on_drive_1.00** (n = 20): generalization_success: 20/20 true; p_success_after: 1 [1; 1]; mean_weight_delta: 0.4672805 [0.4672805; 0.4672805]

**learning_on_drive_1.15** (n = 20): generalization_success: 20/20 true; p_success_after: 1 [1; 1]; mean_weight_delta: 0.4672805 [0.4672805; 0.4672805]

**sham_replay_drive_0.85** (n = 20): generalization_success: 0/20 true; p_success_after: 0 [0; 0]; mean_weight_delta: 0 [0; 0]

**sham_replay_drive_1.00** (n = 20): generalization_success: 0/20 true; p_success_after: 0 [0; 0]; mean_weight_delta: 0 [0; 0]

**sham_replay_drive_1.15** (n = 20): generalization_success: 0/20 true; p_success_after: 0 [0; 0]; mean_weight_delta: 0 [0; 0]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/002-learning_generalization_v1/`.

### 03. independent_replication_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 40; Seeds: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]`; Ticks: `256`.

Reproduktionsprotokoll im selben Projekt; der Name belegt kein unabhaengiges Team.

**recurrence_off** (n = 20): total_spikes: 3 [3; 3]; recurrent_events: 0 [0; 0]; propagation_depth: 1 [1; 1]; last_response_latency: 2 [2; 2]

**recurrence_on** (n = 20): total_spikes: 33 [33; 33]; recurrent_events: 10 [10; 10]; propagation_depth: 61 [61; 61]; last_response_latency: 62 [62; 62]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/003-independent_replication_v1/`.

### 04. topology_matched_5d_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 120; Seeds: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]`; Ticks: `64`.

Aufgaben- und graphgebundener Vergleich; Geometrie, Motive und reine Labels unterscheiden. Kein universeller Dimensionsvorteil.

**1d** (n = 30): first_response_latency: 2 [2; 2]; last_response_latency: 2 [2; 2]; propagation_depth: 1 [1; 1]; total_spikes: 3 [3; 3]

**2d** (n = 30): first_response_latency: 2 [2; 2]; last_response_latency: 2 [2; 2]; propagation_depth: 1 [1; 1]; total_spikes: 3 [3; 3]

**3d** (n = 30): first_response_latency: 2 [2; 2]; last_response_latency: 2 [2; 2]; propagation_depth: 1 [1; 1]; total_spikes: 3 [3; 3]

**5d** (n = 30): first_response_latency: 2 [2; 2]; last_response_latency: 2 [2; 2]; propagation_depth: 1 [1; 1]; total_spikes: 3 [3; 3]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/004-topology_matched_5d_v1/`.

### 05. closed_loop_regulation_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 40; Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]`; Ticks: `128`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**regulation_off** (n = 20): pressure_phase_spikes: 15 [15; 15]; recovery_phase_spikes: 21 [21; 21]; recovery_ratio: 1.4 [1.4; 1.4]

**regulation_on** (n = 20): pressure_phase_spikes: 5 [5; 5]; recovery_phase_spikes: 25 [25; 25]; recovery_ratio: 5 [5; 5]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/005-closed_loop_regulation_v1/`.

### 06. temporal_order_spiking_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 60; Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]`; Ticks: `32`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**forward** (n = 20): output_spike_count: 2 [2; 2]; total_spikes: 6 [6; 6]; sequence_digest: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**reverse** (n = 20): output_spike_count: 2 [2; 2]; total_spikes: 6 [6; 6]; sequence_digest: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**simultaneous** (n = 20): output_spike_count: 1 [1; 1]; total_spikes: 3 [3; 3]; sequence_digest: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/006-temporal_order_spiking_v1/`.

### 07. subsystem_performance_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 10; Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51]`; Ticks: `10000`.

Gemessene technische Last im angegebenen Fenster; keine Extrapolation auf Vollplastizitaet, biologische Netze, GPU oder exklusive Hardware. Die beiden active_scaling-Labels rufen im aktuellen Code dieselbe korrigierte Funktion auf.

**subsystem_profile** (n = 10): construction_seconds: 9.11518e-05 [6.1213e-05; 0.000239231]; core_step_seconds: 0.06742522 [0.06644662; 0.06897523]; digest_seconds: 8.25787e-05 [7.3471e-05; 9.2851e-05]; ticks_per_second: 148332.8 [144979.6; 150496.8]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/007-subsystem_performance_v1/`.

### 08. recurrence_scale_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 80; Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]`; Ticks: `256`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**loop_delay_1** (n = 20): last_response_latency: 62 [62; 62]; recurrent_events: 10 [10; 10]; propagation_depth: 61 [61; 61]

**loop_delay_2** (n = 20): last_response_latency: 252 [252; 252]; recurrent_events: 33 [33; 33]; propagation_depth: 251 [251; 251]

**loop_delay_4** (n = 20): last_response_latency: 251 [251; 251]; recurrent_events: 28 [28; 28]; propagation_depth: 250 [250; 250]

**loop_delay_8** (n = 20): last_response_latency: 245 [245; 245]; recurrent_events: 20 [20; 20]; propagation_depth: 244 [244; 244]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/008-recurrence_scale_v1/`.

### 09. learning_interference_screen_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 20; Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]`; Ticks: `None`.

Begrenzter Interferenz-Screen; getrennte Task-Netze beweisen keine Resistenz eines gemeinsam trainierten Netzes gegen Vergessen.

**sequential_three_task_screen** (n = 20): retained_success_fraction: 1 [1; 1]; weight_range: 0 [0; 0]; task_successes: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/009-learning_interference_screen_v1/`.

### 10. sustained_activity_stability_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 20; Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51]`; Ticks: `100000`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**no_input_control** (n = 10): post_burn_in_spike_cv: 0 [0; 0]; post_burn_in_spike_relative_drift: 0 [0; 0]; finite_state: 10/10 true; topology_unchanged: 10/10 true

**tonic_drive** (n = 10): post_burn_in_spike_cv: 0 [0; 0]; post_burn_in_spike_relative_drift: 0 [0; 0]; finite_state: 10/10 true; topology_unchanged: 10/10 true

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/010-sustained_activity_stability_v1/`.

### 11. msba_energy_efficiency_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 9; Seeds: `[101, 102, 103]`; Ticks: `48`.

Experimentelle Gateway-/Ressourcenfunktion. Proxy-Energie ist nicht gemessene physikalische Energie; keine produktive Tool-Use-Freigabe.

**audio** (n = 3): normalized_energy_units_per_correct_decision: 19.39434 [18.5628; 20.25033]; synaptic_events_per_correct_decision: 16.71673 [16; 17.45455]; task_accuracy: 0.9583333 [0.9166667; 1]

**digital** (n = 3): normalized_energy_units_per_correct_decision: 10.77477 [10.3128; 11.25033]; synaptic_events_per_correct_decision: 8.358366 [8; 8.727273]; task_accuracy: 0.9583333 [0.9166667; 1]

**vision** (n = 3): normalized_energy_units_per_correct_decision: 45.09631 [43.1628; 47.08669]; synaptic_events_per_correct_decision: 41.79183 [40; 43.63636]; task_accuracy: 0.9583333 [0.9166667; 1]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/011-msba_energy_efficiency_v1/`.

### 12. msba_resource_allocation_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 9; Seeds: `[101, 102, 103]`; Ticks: `96`.

Experimentelle Gateway-/Ressourcenfunktion. Proxy-Energie ist nicht gemessene physikalische Energie; keine produktive Tool-Use-Freigabe.

**adaptive** (n = 3): task_accuracy: 0.3023512 [0.3023512; 0.3023512]; resource_budget_consumed: 66 [66; 66]; time_to_budget_exhaustion: 96 [96; 96]

**fixed** (n = 3): task_accuracy: 0.34375 [0.34375; 0.34375]; resource_budget_consumed: 80.4 [80.4; 80.4]; time_to_budget_exhaustion: 96 [96; 96]

**random** (n = 3): task_accuracy: 0.3349111 [0.318338; 0.3441056]; resource_budget_consumed: 77.82066 [73.80706; 81.21941]; time_to_budget_exhaustion: 96 [96; 96]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/012-msba_resource_allocation_v1/`.

### 13. msba_visual_roi_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 12; Seeds: `[101, 102, 103]`; Ticks: `48`.

Experimentelle Gateway-/Ressourcenfunktion. Proxy-Energie ist nicht gemessene physikalische Energie; keine produktive Tool-Use-Freigabe.

**adaptive_roi** (n = 3): roi_overlap_with_task_relevant_region: 1 [1; 1]; task_accuracy: 1 [1; 1]; visual_energy_units: 48 [48; 48]

**fixed_center_roi** (n = 3): roi_overlap_with_task_relevant_region: 0.2708333 [0.2083333; 0.3541667]; task_accuracy: 0.2708333 [0.2083333; 0.3541667]; visual_energy_units: 192 [192; 192]

**full_image** (n = 3): roi_overlap_with_task_relevant_region: 1 [1; 1]; task_accuracy: 1 [1; 1]; visual_energy_units: 768 [768; 768]

**random_roi** (n = 3): roi_overlap_with_task_relevant_region: 0.06944444 [0.0625; 0.08333333]; task_accuracy: 0.06944444 [0.0625; 0.08333333]; visual_energy_units: 48 [48; 48]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/013-msba_visual_roi_v1/`.

### 14. msba_digital_integrity_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 9; Seeds: `[101, 102, 103]`; Ticks: `64`.

Experimentelle Gateway-/Ressourcenfunktion. Proxy-Energie ist nicht gemessene physikalische Energie; keine produktive Tool-Use-Freigabe.

**deterministic_replay** (n = 3): checksum_mismatches: 0 [0; 0]; admitted_symbol_rate: 0.671875 [0.671875; 0.671875]; exact_integrity_pass: 3/3 true

**no_throttling** (n = 3): checksum_mismatches: 0 [0; 0]; admitted_symbol_rate: 1 [1; 1]; exact_integrity_pass: 3/3 true

**throttled** (n = 3): checksum_mismatches: 0 [0; 0]; admitted_symbol_rate: 0.671875 [0.671875; 0.671875]; exact_integrity_pass: 3/3 true

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/014-msba_digital_integrity_v1/`.

### 15. msba_modality_compensation_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 12; Seeds: `[101, 102, 103]`; Ticks: `48`.

Experimentelle Gateway-/Ressourcenfunktion. Proxy-Energie ist nicht gemessene physikalische Energie; keine produktive Tool-Use-Freigabe.

**adaptive_compensation** (n = 3): compensatory_gate_change: 0.5 [0.5; 0.5]; task_recovery: 0.85 [0.85; 0.85]; incremental_energy_cost: 0.1 [0.1; 0.1]

**fixed_allocation** (n = 3): compensatory_gate_change: 0 [0; 0]; task_recovery: 0.425 [0.425; 0.425]; incremental_energy_cost: 0 [0; 0]

**no_compensation** (n = 3): compensatory_gate_change: 0 [0; 0]; task_recovery: 0.425 [0.425; 0.425]; incremental_energy_cost: -0.35 [-0.35; -0.35]

**shuffled_utility** (n = 3): compensatory_gate_change: -0.1494867 [-0.4089365; 0.03309975]; task_recovery: 0.2979363 [0.07740394; 0.4531348]; incremental_energy_cost: -0.484538 [-0.7180429; -0.3202102]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/015-msba_modality_compensation_v1/`.

### 16. dimension_dynamics_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 180; Seeds: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]`; Ticks: `256`.

Aufgaben- und graphgebundener Vergleich; Geometrie, Motive und reine Labels unterscheiden. Kein universeller Dimensionsvorteil.

**1d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**2d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**3d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d_shuffled** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**random_graph** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/016-dimension_dynamics_v1/`.

### 17. dimension_propagation_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 180; Seeds: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]`; Ticks: `256`.

Aufgaben- und graphgebundener Vergleich; Geometrie, Motive und reine Labels unterscheiden. Kein universeller Dimensionsvorteil.

**1d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**2d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**3d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d_shuffled** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**random_graph** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/017-dimension_propagation_v1/`.

### 18. dimension_modularity_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/018-dimension_modularity_boundary_v1/`.

### 19. dimension_information_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/019-dimension_information_boundary_v1/`.

### 20. research_assistant_methodology_audit_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/020-research_assistant_methodology_audit_v1/`.

### 21. connectome_reference_gap_audit_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/021-connectome_reference_gap_audit_v1/`.

### 22. deterministic_replica_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 12; Seeds: `[42, 43, 44]`; Ticks: `256`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**recurrence_off_replica_a** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**recurrence_off_replica_b** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**recurrence_on_replica_a** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**recurrence_on_replica_b** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/022-deterministic_replica_v1/`.

### 23. embodied_mapping_learning_gap_audit_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/023-embodied_mapping_learning_gap_audit_v1/`.

### 24. embodied_efference_copy_gap_audit_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/024-embodied_efference_copy_gap_audit_v1/`.

### 25. embodied_morphology_transfer_gap_audit_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/025-embodied_morphology_transfer_gap_audit_v1/`.

### 26. gateway_learning_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/026-gateway_learning_boundary_v1/`.

### 27. gateway_modality_rules_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/027-gateway_modality_rules_boundary_v1/`.

### 28. gateway_stability_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/028-gateway_stability_boundary_v1/`.

### 29. gateway_transfer_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/029-gateway_transfer_boundary_v1/`.

### 30. gateway_structure_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/030-gateway_structure_boundary_v1/`.

### 31. gateway_closed_loop_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/031-gateway_closed_loop_boundary_v1/`.

### 32. gateway_resources_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/032-gateway_resources_boundary_v1/`.

### 33. homeostasis_rate_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/033-homeostasis_rate_boundary_v1/`.

### 34. homeostasis_stdp_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/034-homeostasis_stdp_boundary_v1/`.

### 35. language_organ_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/035-language_organ_boundary_v1/`.

### 36. synaptic_memory_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/036-synaptic_memory_boundary_v1/`.

### 37. network_impulse_reproducibility_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 12; Seeds: `[42, 43, 44]`; Ticks: `256`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**recurrence_off_replica_a** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**recurrence_off_replica_b** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**recurrence_on_replica_a** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**recurrence_on_replica_b** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/037-network_impulse_reproducibility_v1/`.

### 38. regulation_telemetry_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 9; Seeds: `[42, 43, 44]`; Ticks: `None`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**chronic_pressure** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**nominal** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**telemetry_unknown** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/038-regulation_telemetry_v1/`.

### 39. million_neuron_scaling_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/039-million_neuron_scaling_boundary_v1/`.

### 40. self_organization_clusters_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/040-self_organization_clusters_boundary_v1/`.

### 41. self_organization_emergence_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/041-self_organization_emergence_boundary_v1/`.

### 42. tonic_spike_reproducibility_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `256`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**same_seed_tonic_replica_pair** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/042-tonic_spike_reproducibility_v1/`.

### 43. topology_propagation_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 180; Seeds: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]`; Ticks: `256`.

Aufgaben- und graphgebundener Vergleich; Geometrie, Motive und reine Labels unterscheiden. Kein universeller Dimensionsvorteil.

**1d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**2d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**3d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d_shuffled** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**random_graph** (n = 30): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/043-topology_propagation_v1/`.

### 44. stdp_weight_matrix_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**productive_reward_stdp** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/044-stdp_weight_matrix_v1/`.

### 45. stdp_learning_performance_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 9; Seeds: `[42, 43, 44]`; Ticks: `None`.

Gemessene technische Last im angegebenen Fenster; keine Extrapolation auf Vollplastizitaet, biologische Netze, GPU oder exklusive Hardware. Die beiden active_scaling-Labels rufen im aktuellen Code dieselbe korrigierte Funktion auf.

**learning_off** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**learning_on** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**sham_replay** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/045-stdp_learning_performance_v1/`.

### 46. stdp_pair_timing_registered_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**registered_pair_timing_curve** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/046-stdp_pair_timing_registered_v1/`.

### 47. stdp_long_stability_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/047-stdp_long_stability_boundary_v1/`.

### 48. storage_roundtrip_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/048-storage_roundtrip_boundary_v1/`.

### 49. storage_causal_resume_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/049-storage_causal_resume_boundary_v1/`.

### 50. storage_density_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/050-storage_density_boundary_v1/`.

### 51. storage_scale_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/051-storage_scale_boundary_v1/`.

### 52. structural_efficiency_boundary_v1

Status: **completed**; Kategorie: `boundary_audit`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `None`.

Grenz-/Vertragsaudit; kein direkter experimenteller Test der inhaltlichen Hypothese.

**instrumentation_gap_audit** (n = 3): audit_contract_complete: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/052-structural_efficiency_boundary_v1/`.

### 53. science_suite_registered_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 54; Seeds: `[42, 43, 44]`; Ticks: `256`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**5d:1d** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d:2d** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d:3d** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d:5d** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d:5d_shuffled** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**5d:random_graph** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**learning:learning_off** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**learning:learning_on** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**learning:sham_replay** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**ping:recurrence_off** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**ping:recurrence_on** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**regulation:chronic_pressure** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**regulation:nominal** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**regulation:telemetry_unknown** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**stdp:productive_reward_stdp** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**temporal:fast_medium_slow** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**time:100** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**time:256** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/053-science_suite_registered_v1/`.

### 54. temporal_state_registered_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 3; Seeds: `[42, 43, 44]`; Ticks: `256`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**fast_medium_slow** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/054-temporal_state_registered_v1/`.

### 55. learning_timescale_registered_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 12; Seeds: `[42, 43, 44]`; Ticks: `100000`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**100** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**1000** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**10000** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**100000** (n = 3): registered_runner_outputs: strukturiert oder nicht ausgewiesen; siehe Rohdaten

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/055-learning_timescale_registered_v1/`.

### 56. memory_delayed_information_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 12; Seeds: `[101, 102, 103]`; Ticks: `None`.

Kontrollierte technische Komponentenfunktion; keine automatische Attribution an synaptisches Lernen oder subjektive Kognition.

**memory_read_off** (n = 3): accuracy: 0.4166667 [0.3333333; 0.5416667]; retrievals: 0 [0; 0]

**memory_read_write** (n = 3): accuracy: 1 [1; 1]; retrievals: 24 [24; 24]

**memory_time_shuffled** (n = 3): accuracy: 0.4861111 [0.4583333; 0.5416667]; retrievals: 23 [23; 23]

**memory_write_off** (n = 3): accuracy: 0.4166667 [0.3333333; 0.5416667]; retrievals: 0 [0; 0]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/056-memory_delayed_information_v1/`.

### 57. world_model_prediction_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 12; Seeds: `[101, 102, 103]`; Ticks: `None`.

Kontrollierte technische Komponentenfunktion; keine automatische Attribution an synaptisches Lernen oder subjektive Kognition.

**adaptive** (n = 3): mean_prediction_error: 0.5 [0.5; 0.5]

**frozen** (n = 3): mean_prediction_error: 0.5 [0.5; 0.5]

**no_model** (n = 3): mean_prediction_error: strukturiert oder nicht ausgewiesen; siehe Rohdaten

**persistence** (n = 3): mean_prediction_error: 0.7569444 [0.7291667; 0.7916667]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/057-world_model_prediction_v1/`.

### 58. behavior_profile_control_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 12; Seeds: `[101, 102, 103]`; Ticks: `None`.

Kontrollierte technische Komponentenfunktion; keine automatische Attribution an synaptisches Lernen oder subjektive Kognition.

**adaptive** (n = 3): accuracy: 0.5666667 [0.55; 0.6]; update_count: 40 [40; 40]

**fixed_high_exploration** (n = 3): accuracy: 0.4416667 [0.425; 0.475]; update_count: 0 [0; 0]

**fixed_low_exploration** (n = 3): accuracy: 0.5583333 [0.525; 0.575]; update_count: 0 [0; 0]

**shuffled_profile** (n = 3): accuracy: 0.6083333 [0.5; 0.675]; update_count: 0 [0; 0]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/058-behavior_profile_control_v1/`.

### 59. embodied_closed_loop_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 9; Seeds: `[101, 102, 103]`; Ticks: `600`.

Synthetischer sensorimotorischer Screen; externe Controllerbeitraege und Beobachtungsgrenzen beachten. Keine biologische Vollsimulation.

**closed_loop** (n = 3): tracking_rmse_rad: 0.1949232 [0.1934416; 0.1967981]

**feedback_absent** (n = 3): tracking_rmse_rad: 0.5217487 [0.5196927; 0.5242175]

**yoked_replay** (n = 3): tracking_rmse_rad: 0.3035479 [0.2988769; 0.3079309]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/059-embodied_closed_loop_v1/`.

### 60. embodied_proprioception_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 12; Seeds: `[101, 102, 103]`; Ticks: `600`.

Synthetischer sensorimotorischer Screen; externe Controllerbeitraege und Beobachtungsgrenzen beachten. Keine biologische Vollsimulation.

**closed_loop** (n = 3): tracking_rmse_rad: 0.1949232 [0.1934416; 0.1967981]

**delayed_proprioception** (n = 3): tracking_rmse_rad: 0.1959547 [0.1906298; 0.2039021]

**feedback_absent** (n = 3): tracking_rmse_rad: 0.5217487 [0.5196927; 0.5242175]

**timing_shuffle** (n = 3): tracking_rmse_rad: 0.4854937 [0.4716011; 0.5080172]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/060-embodied_proprioception_v1/`.

### 61. embodied_perturbation_screen_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 12; Seeds: `[101, 102, 103]`; Ticks: `600`.

Synthetischer sensorimotorischer Screen; externe Controllerbeitraege und Beobachtungsgrenzen beachten. Keine biologische Vollsimulation.

**blocked_joint** (n = 3): tracking_rmse_rad: 0.3722355 [0.3618097; 0.3806473]

**closed_loop** (n = 3): tracking_rmse_rad: 0.1949232 [0.1934416; 0.1967981]

**restored_actuator** (n = 3): tracking_rmse_rad: 0.31707 [0.3119633; 0.3199349]

**weak_actuator** (n = 3): tracking_rmse_rad: 0.3686355 [0.3633037; 0.3736405]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/061-embodied_perturbation_screen_v1/`.

### 62. connectome_topology_screen_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 12; Seeds: `[101, 102, 103]`; Ticks: `600`.

Aufgaben- und graphgebundener Vergleich; Geometrie, Motive und reine Labels unterscheiden. Kein universeller Dimensionsvorteil.

**degree_preserving** (n = 3): tracking_rmse_rad: 0.536919 [0.2001561; 0.7240772]

**random_edges** (n = 3): tracking_rmse_rad: 0.4941672 [0.3703082; 0.725093]

**structured** (n = 3): tracking_rmse_rad: 0.1949232 [0.1934416; 0.1967981]

**weight_shuffle** (n = 3): tracking_rmse_rad: 0.3928024 [0.1991185; 0.6230786]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/062-connectome_topology_screen_v1/`.

### 63. embodied_controller_attribution_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 12; Seeds: `[101, 102, 103]`; Ticks: `600`.

Synthetischer sensorimotorischer Screen; externe Controllerbeitraege und Beobachtungsgrenzen beachten. Keine biologische Vollsimulation.

**closed_loop** (n = 3): tracking_rmse_rad: 0.1949232 [0.1934416; 0.1967981]

**controller_only** (n = 3): tracking_rmse_rad: 0.2303219 [0.2269245; 0.2342337]

**disconnected_motor** (n = 3): tracking_rmse_rad: 0.3712063 [0.3562102; 0.3871005]

**shuffled_motor** (n = 3): tracking_rmse_rad: 0.2863395 [0.2583636; 0.304391]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/063-embodied_controller_attribution_v1/`.

### 64. embodied_timing_v1

Status: **completed**; Kategorie: `registered_simulation`; gespeicherte Laeufe: 21; Seeds: `[101, 102, 103]`; Ticks: `600`.

Synthetischer sensorimotorischer Screen; externe Controllerbeitraege und Beobachtungsgrenzen beachten. Keine biologische Vollsimulation.

**batch_1** (n = 3): batch_digest_identity: 3/3 true

**batch_128** (n = 3): batch_digest_identity: 3/3 true

**batch_16** (n = 3): batch_digest_identity: 3/3 true

**physics_15ms** (n = 3): batch_digest_identity: 3/3 true

**physics_5ms** (n = 3): batch_digest_identity: 3/3 true

**sensor_15ms** (n = 3): batch_digest_identity: 3/3 true

**sensor_5ms** (n = 3): batch_digest_identity: 3/3 true

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/064-embodied_timing_v1/`.

### 65. active_scaling_v2

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 15; Seeds: `[21001, 21002, 21003]`; Ticks: `None`.

Gemessene technische Last im angegebenen Fenster; keine Extrapolation auf Vollplastizitaet, biologische Netze, GPU oder exklusive Hardware. Die beiden active_scaling-Labels rufen im aktuellen Code dieselbe korrigierte Funktion auf.

**n100000** (n = 3): ticks_per_second: 3.535133 [3.504036; 3.561854]; finite_state: 3/3 true

**n1024** (n = 3): ticks_per_second: 523.5323 [519.4525; 525.9151]; finite_state: 3/3 true

**n128** (n = 3): ticks_per_second: 4252.396 [4227.875; 4298.408]; finite_state: 3/3 true

**n25000** (n = 3): ticks_per_second: 18.11017 [17.9315; 18.2902]; finite_state: 3/3 true

**n5000** (n = 3): ticks_per_second: 100.5795 [96.15364; 103.9864]; finite_state: 3/3 true

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/065-active_scaling_v2/`.

### 66. dimensional_connectivity_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 130; Seeds: `[20001, 20002, 20003, 20004, 20005, 20006, 20007, 20008, 20009, 20010]`; Ticks: `256`.

Aufgaben- und graphgebundener Vergleich; Geometrie, Motive und reine Labels unterscheiden. Kein universeller Dimensionsvorteil.

**fixed_graph_label_2d** (n = 10): output_spikes: 77.4 [66; 94]

**fixed_graph_label_3d** (n = 10): output_spikes: 77.4 [66; 94]

**fixed_graph_label_4d** (n = 10): output_spikes: 77.4 [66; 94]

**fixed_graph_label_5d** (n = 10): output_spikes: 77.4 [66; 94]

**fixed_graph_label_6d** (n = 10): output_spikes: 77.4 [66; 94]

**fixed_graph_label_8d** (n = 10): output_spikes: 77.4 [66; 94]

**geometry_2d** (n = 10): output_spikes: 72.4 [60; 83]

**geometry_3d** (n = 10): output_spikes: 80.4 [63; 101]

**geometry_4d** (n = 10): output_spikes: 75 [62; 90]

**geometry_5d** (n = 10): output_spikes: 77.4 [66; 94]

**geometry_6d** (n = 10): output_spikes: 77.1 [59; 99]

**geometry_8d** (n = 10): output_spikes: 74.6 [61; 90]

**random_graph** (n = 10): output_spikes: 69.6 [40; 92]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/066-dimensional_connectivity_v1/`.

### 67. native_association_holdout_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 50; Seeds: `[20001, 20002, 20003, 20004, 20005, 20006, 20007, 20008, 20009, 20010]`; Ticks: `None`.

Native angeleitete Assoziation mit gehaltenen Testepisoden; Reichweite auf Aufgabe, Seed-Einheit und Kontrollen begrenzt.

**learning_off** (n = 10): test_accuracy: 0.5 [0.5; 0.5]

**learning_on** (n = 10): test_accuracy: 0.785 [0.575; 1]

**sham_replay** (n = 10): test_accuracy: 0.5 [0.5; 0.5]

**weight_reset** (n = 10): test_accuracy: 0.5 [0.5; 0.5]

**weight_shuffle** (n = 10): test_accuracy: 0.5 [0.5; 0.5]

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/067-native_association_holdout_v1/`.

### 68. brian2_single_neuron_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 3; Seeds: `[20001, 20002, 20003]`; Ticks: `None`.

Strenger diskreter Modellvergleich. Ein verfehltes Konformitaetskriterium bleibt ein negativer Befund, kein Laufzeitfehler.

**matched_split_euler** (n = 3): conformance_within_1e_8: 0/3 true

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/068-brian2_single_neuron_v1/`.

### 69. active_scaling_v1

Status: **completed**; Kategorie: `functional_experiment`; gespeicherte Laeufe: 15; Seeds: `[20001, 20002, 20003]`; Ticks: `None`.

Gemessene technische Last im angegebenen Fenster; keine Extrapolation auf Vollplastizitaet, biologische Netze, GPU oder exklusive Hardware. Die beiden active_scaling-Labels rufen im aktuellen Code dieselbe korrigierte Funktion auf.

**n100000** (n = 3): ticks_per_second: 3.545224 [3.499746; 3.572152]; finite_state: 3/3 true

**n1024** (n = 3): ticks_per_second: 524.827 [518.5387; 532.1373]; finite_state: 3/3 true

**n128** (n = 3): ticks_per_second: 4204.791 [4155.943; 4254.819]; finite_state: 3/3 true

**n25000** (n = 3): ticks_per_second: 18.4344 [18.27427; 18.58981]; finite_state: 3/3 true

**n5000** (n = 3): ticks_per_second: 100.3919 [95.38091; 103.0091]; finite_state: 3/3 true

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/069-active_scaling_v1/`.

### 70. foundational_seven_suite

Status: **completed**; Kategorie: `composite_engineering_screen`; gespeicherte Laeufe: 54; Seeds: `[42, 43, 44]`; Ticks: `1000`.

Begrenzte protokollgebundene Beobachtung; Primarmessung, Kontrollen und technische Ausfuehrung nicht mit akzeptierter Evidenz gleichsetzen.

**5d:1d** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**5d:2d** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**5d:3d** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**5d:5d** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**5d:5d_shuffled** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**5d:random_graph** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**learning:learning_off** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**learning:learning_on** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**learning:sham_replay** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**ping:recurrence_off** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**ping:recurrence_on** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**regulation:chronic_pressure** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**regulation:nominal** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**regulation:telemetry_unknown** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**stdp:productive_reward_stdp** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**temporal:fast_medium_slow** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**time:100** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

**time:1000** (n = 3): Strukturierte Basisfamilien; siehe Rohdaten und summary.json.

Artefaktpfad: `research/experiments/EXP-EMP-20260913-A3/070-foundational_seven_suite/`.


# Diskussion, Fortschrittsbewertung und Grenzen

## Was als Fortschritt gilt

Der zentrale Fortschritt besteht in einer auswertbaren Verbindung von Code, Kontrollbedingungen, aufgezeichneten Daten und begrenzten Aussagen. Die Plattform enthält inzwischen mehr als Entwürfe und Unit-Tests: Es gibt native Lern-, Rekurrenz-, Dimensions-, Speicher-, Verkörperungs- und Skalierungsmessungen. Die genaue Ausführungsbilanz und die Primärmaße stehen im Ergebnisteil. Das allein macht jedoch keine der weitergehenden allgemeinen Hypothesen wahr.

Drei Ebenen bleiben getrennt. Erstens: Ein Mechanismus ist implementiert und erreichbar. Zweitens: Eine bestimmte kontrollierte Ausführung erzeugt eine reproduzierbare Beobachtung. Drittens: Fachlich begutachtete, hinreichend unabhängig bestätigte Befunde tragen eine bestimmte wissenschaftliche Behauptung. Ein grünes Engineering-Gate betrifft vor allem die erste und Teile der zweiten Ebene. Es darf die dritte nicht durch eine Farbe ersetzen.

## Lernbefunde und Zuordnung

Ein positiver nativer Assoziationskontrast ist relevant, weil eingefrorene Testgewichte und frische Episoden die Erklärung durch eine bloße unmittelbare Teacher-Probe einschränken. Seine Reichweite bleibt eine konstruierte Aufgabe mit vorgegebenem Inputraum, Reward und Architektur. Er beweist weder selbst erzeugte Ziele noch allgemeine Sprache, neuronales autobiografisches Gedächtnis oder menschliche Begriffsbildung. Kontrollen mit identischen Ergebnissen sind keine voneinander unabhängigen Bestätigungen.

In älteren Lernprotokollen können deklarierte Holdout-Größen und tatsächlich ausgeführte Probeepisoden auseinanderfallen. Die neue Fassung bewertet deshalb die aufgezeichneten Interventionen, nicht allein die Feldnamen. Ein Interferenz-Screen mit getrennten Task-Netzen ist kein Nachweis gegen katastrophales Vergessen in einem gemeinsam weitertrainierten Netz. Ebenso darf ein nichtneuronaler Prädiktor oder Ressourcenregler nicht ohne Ablation als Leistung des SNN bezeichnet werden.

## Negative Befunde als Erkenntnis

Die Dimensionsfrage ist eine Hypothese, keine Namensdefinition. Wenn die deklarierten Vergleiche keinen belastbaren Vorteil der 5D-Geometrie zeigen, wird genau dies berichtet. Daraus folgt weder die Unmöglichkeit eines Effekts auf anderen Aufgaben noch ein Nachweis der Gleichwertigkeit aller Dimensionen. Ein angemessener nächster Versuch benötigt eine festgelegte Aufgabe, eine praktisch relevante Effektgrenze und ein ausreichend präzises Design statt weiterer attraktiver Visualisierungen.

Die externe Einzelzellkonformität prüft einen besonders strengen diskreten Vertrag. Kleine Rechendifferenzen können in einem System mit Schwellen und Resets unterschiedliche Ereignisse erzeugen; ob dies den konkreten Befund vollständig erklärt, muss durch isolierte Interventionen gezeigt werden. Deshalb bleiben Ein-Schritt-Vergleich, explizite Rechenausdrücke, Datentypen, Ereignisphasen und Spike-Matching-Toleranzen getrennte prospektive Prüfungen. Die Toleranz wird nicht anhand eines gewünschten Resultats nachjustiert.

## Was nicht geschlossen ist

Große Zahl von Testfällen, viele Protokollzeilen und lange Läufe können dieselbe begrenzte Annahme wiederholt testen. Offene Punkte sind deshalb nicht nur fehlende Ausführungszeit. Es fehlen bei einem Teil des Registers unmittelbare Messkonstrukte, bei mehreren Integrationsfragen ein validierter gemeinsamer Zustand, bei weitreichenden Lernbehauptungen anspruchsvolle Generalisierungsaufgaben und bei wissenschaftlicher Freigabe unabhängige Menschen.

Insbesondere bleiben die volle gekoppelte Kognitions-Wiederherstellung, Generalisierung jenseits der konstruierten Assoziationsaufgabe, ein langzeitig vollplastisches Zielnetz unter deklariertem Ressourcenbudget, produktives Gateway-Lernen und ein gemessener CUDA-Backendvergleich eigene Abnahmekriterien. Mechanistische Tests für biophysikalische Erweiterungen ersetzen keine experimentelle neurobiologische Validierung. Diese Lücken werden nicht durch allgemeine Begriffe wie Nervengewebe, Selbstmodell oder Bewusstsein geschlossen.

## Theorie und empirische Disziplin

Die theoretische Abhandlung untersucht delegierte Handlungsmacht, Wissensherkunft, rekursive technische Entwicklung und nichtorganisches Embodiment. Diese Begriffe können Beobachtungen ordnen und Versuche motivieren. Damit sie empirischen Gehalt gewinnen, müssen unterschiedliche Deutungen unterschiedliche, messbare Vorhersagen unter geeigneten Interventionen liefern. Die Erklärung einer Funktionskette und die Zuschreibung eines Erlebens bleiben verschiedene Probleme.

Der methodische Vorsprung einer strikten Systemgrenze liegt darin, unerlaubte Schlussfolgerungen sichtbar zu machen. Ein externer Sprachgenerator kann eine beeindruckende Antwort liefern, ohne dass der SNN-Kern die entsprechende Information erworben hat. Eine Speicherkomponente kann einen Inhalt korrekt zurückgeben, ohne dass dessen Entstehung durch neuronales Lernen erklärt ist. Eine Ethikrichtlinie kann vorsorglich sinnvoll sein, ohne das Vorliegen von Leidensfähigkeit festzustellen.

## Fazit

Die vorliegende Fassung dokumentiert eine reale technische und empirische Weiterentwicklung sowie reale Grenzen. Sie stellt den Stand weder als reine Ideenskizze noch als abgeschlossene allgemeine Intelligenz dar. Die verbleibende wissenschaftliche Aufgabe ist die gezielte Schließung klar definierter Evidenzlücken. Akzeptierte Evidenz entsteht aus einer nachvollziehbaren Prüfung der Daten und ihrer Reichweite, nicht aus automatisch fortgeschriebenen Prozentanzeigen.


# Abdeckung, offene Voraussetzungen und Reproduktion

## Nicht durch automatische Ausfuehrung geschlossene Fragen

Die folgende Liste unterscheidet fehlende unmittelbare Messprotokolle von fehlenden Registry-Eintraegen. Auch ein vorhandener Grenzvertrag ist kein direktes Experiment.

- `RQ-5D-003`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-5D-004`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-AIR-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-101`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-102`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-103`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-104`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-105`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-106`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-107`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-108`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-109`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-110`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-111`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-112`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-113`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-114`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-115`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-116`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CNS-117`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-CONN-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-EMB-003`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-EMB-007`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-EMB-008`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-EPI-101`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-EPI-102`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-EPIST-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-ETH-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-ETH-002`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-GW-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-GW-002`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-GW-003`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-GW-004`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-GW-005`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-GW-006`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-GW-007`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-HOM-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-HOM-002`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-LLM-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-MEM-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-SCALE-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-SELF-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-SELF-002`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-STDP-002`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-STORAGE-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-STORAGE-002`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-STORAGE-003`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-STORAGE-004`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-STRUCT-001`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-WEL-101`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-WEL-102`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.
- `RQ-WEL-103`: spezifische Messung oder menschliche Entscheidung bleibt erforderlich.

## Menschliche Vorlagen

- `epistemic_boundary_audit_v1`: RQ-EPIST-001; nicht automatisch ausgefuellt.
- `authorship_responsibility_audit_v1`: RQ-ETH-001; nicht automatisch ausgefuellt.
- `control_responsibility_audit_v1`: RQ-ETH-002; nicht automatisch ausgefuellt.
- `cog_cns_101_v1`: RQ-CNS-101; nicht automatisch ausgefuellt.
- `cog_cns_102_v1`: RQ-CNS-102; nicht automatisch ausgefuellt.
- `cog_cns_103_v1`: RQ-CNS-103; nicht automatisch ausgefuellt.
- `cog_cns_104_v1`: RQ-CNS-104; nicht automatisch ausgefuellt.
- `cog_cns_105_v1`: RQ-CNS-105; nicht automatisch ausgefuellt.
- `cog_cns_106_v1`: RQ-CNS-106; nicht automatisch ausgefuellt.
- `cog_cns_107_v1`: RQ-CNS-107; nicht automatisch ausgefuellt.
- `cog_cns_108_v1`: RQ-CNS-108; nicht automatisch ausgefuellt.
- `cog_cns_109_v1`: RQ-CNS-109; nicht automatisch ausgefuellt.
- `cog_cns_110_v1`: RQ-CNS-110; nicht automatisch ausgefuellt.
- `cog_cns_111_v1`: RQ-CNS-111; nicht automatisch ausgefuellt.
- `cog_cns_112_v1`: RQ-CNS-112; nicht automatisch ausgefuellt.
- `cog_cns_113_v1`: RQ-CNS-113; nicht automatisch ausgefuellt.
- `cog_cns_114_v1`: RQ-CNS-114; nicht automatisch ausgefuellt.
- `cog_cns_115_v1`: RQ-CNS-115; nicht automatisch ausgefuellt.
- `cog_cns_116_v1`: RQ-CNS-116; nicht automatisch ausgefuellt.
- `cog_cns_117_v1`: RQ-CNS-117; nicht automatisch ausgefuellt.
- `cog_epi_101_v1`: RQ-EPI-101; nicht automatisch ausgefuellt.
- `cog_epi_102_v1`: RQ-EPI-102; nicht automatisch ausgefuellt.
- `cog_wel_101_v1`: RQ-WEL-101; nicht automatisch ausgefuellt.
- `cog_wel_102_v1`: RQ-WEL-102; nicht automatisch ausgefuellt.
- `cog_wel_103_v1`: RQ-WEL-103; nicht automatisch ausgefuellt.

## Reproduktion

Den exakten Quellcommit aus plan.json in einem sauberen separaten Checkout verwenden. Die aufgezeichneten Paketversionen und Ressourcenbedingungen pruefen. Ein neuer Ausgabepfad ist zwingend; historische DATA duerfen nicht ueberschrieben werden.

```bash
python -m pip install -e '.[dev,docs,empirical]'
python scripts/empirical_campaign.py --output /absolute/new/run --campaign-id NEW-ID
python scripts/empirical_campaign.py --output /absolute/new/run --analyze
python scripts/run_stage3_reference.py --output /absolute/new/stage3.json
python scripts/publication_alpha3.py --verify
```

Eine Wiederholung mit geaenderten Quellen ist eine neue Ausfuehrung. Paketversionen und Simulationsergebnisse werden nicht rueckwirkend dem neuen Commit zugeschrieben.


# Review, Verantwortung und Weiterführung

Das angekündigte menschliche Review steht aus. Weder diese Ausgabe noch eine erfolgreiche CI-Ausführung liefert stellvertretend eine fachliche Annahmeentscheidung, ein institutionelles Mandat oder ein externes Ethikvotum. Die Bezeichnung Dissertationsmanuskript beschreibt eine Textgattung; sie behauptet keine Einreichung, Annahme oder Verleihung eines akademischen Grades.

Das Review sollte jede wesentliche Schlussfolgerung mit dem zugehörigen Versuch, dem primären Endpunkt und den Grenzen verbinden. Erforderlich sind insbesondere die Prüfung der Seed-/Bedingungsabdeckung, möglicher Informationsleckage, der Rolle externer Regler, der statistischen Einheit und der Unabhängigkeit von Replikationen. Eine Zustimmung zur Interpretation ist nicht dasselbe wie die Freigabe eines EVID-Objekts.

Die offene Arbeitsliste unterscheidet ausführbare und ausgeführte Protokolle, fehlende Instrumentierung, externe Voraussetzungen und menschliche Entscheidungen. Ein erneuter Lauf ohne geänderte methodische Frage schließt keine fehlende Operationalisierung. Für die nächste konfirmatorische Stufe sind Hypothese, Population beziehungsweise Aufgabenverteilung, Kontrollarme, Stopping Rule, Ausschlussregeln, primäres Maß und Auswertung vor der neuen Datenerzeugung festzulegen.

Vorsorgliche Ethik, Zugangsbeschränkungen und ein technisch unabhängiger Abbruchpfad bleiben unabhängig von metaphysischen Zuschreibungen sinnvoll. Die Plattform darf nicht allein über ihre eigene Fortsetzung entscheiden. Werden menschliche Probanden, personenbezogene Daten oder reale Aktoren einbezogen, sind die konkreten organisatorischen und rechtlichen Voraussetzungen vor der betreffenden Studie zu klären; eine Simulation oder ein Fragebogenentwurf ersetzt diese Prüfung nicht.

KI-Unterstützung wird für Quellprüfung, Instrumentierung, Dokumentation und Interpretation offengelegt. Die Verantwortung für wissenschaftliche Behauptungen und Freigaben bleibt bei den benannten Menschen. Automatische Evidenz-Promotion ist in dieser Ausgabe ausdrücklich ausgeschlossen.


# Methodische Quellen und Artefaktnachweise

[1] Izhikevich, E. M. (2003). Simple Model of Spiking Neurons. IEEE Transactions on Neural Networks, 14(6), 1569-1572. DOI: 10.1109/TNN.2003.820440. Autorenfassung und Referenzprogramm: https://izhikevich.org/publications/spikes.htm .

[2] Brian2-Autoren (Dokumentation 2.10.1). Example: Izhikevich_2003. https://brian2.readthedocs.io/en/2.10.1/examples/frompapers.Izhikevich_2003.html . Das dortige Standardbeispiel ist nicht identisch mit jedem MHRN-Vergleichspfad.

[3] Brian2-Autoren (Dokumentation 2.10.1). Running a simulation, insbesondere Scheduling und Store/restore. https://brian2.readthedocs.io/en/2.10.1/user/running.html .

[4] Izhikevich, E. M. (2007). Solving the Distal Reward Problem through Linkage of STDP and Dopamine Signaling. Cerebral Cortex, 17(10), 2443-2452. DOI: 10.1093/cercor/bhl152. Autorenfassung: https://www.izhikevich.org/publications/dastdp.htm . Mechanistisches Modell; keine MHRN-Validierung.

[5] SciPy-Entwickler. scipy.stats.permutation_test, offizielle API-Dokumentation. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html . Die verwendete eigene Vorzeichenwechselroutine und ihre konkreten Parameter stehen im eingefrorenen Kampagnenskript; die Referenz begründet keine ungeprüfte Austauschbarkeit der Daten.

Primäre MHRN-Quellen sind der in der Kampagne genannte Git-Commit, plan.json, die einzelnen selection.json/manifest.json/receipt.json, die unveränderten runs.json.gz und summary.json. Die bisherigen Literaturverzeichnisse und theoretischen Quellen sind im vollständig erhaltenen Haupttext und in literatur_revision.bib enthalten. Externe Methodenquellen ersetzen nicht die experimentellen Artefakte.
