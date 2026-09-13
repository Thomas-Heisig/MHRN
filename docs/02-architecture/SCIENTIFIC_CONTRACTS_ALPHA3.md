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
