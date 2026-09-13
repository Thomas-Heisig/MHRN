"""Interpretation text for the source-bound Alpha.3 manuscript, not EVID."""

ARCHITECTURE = r"""# Architektur, Formalismus und wissenschaftliche Reichweite

## Gegenstand und Beitrag

MHRN ist ein experimentelles Framework f\u00fcr rekurrente spikende Netze mit kontrollierter Plastizit\u00e4t und expliziten Systemgrenzen. Die wissenschaftliche Leistung wird nicht durch die Anzahl der Module definiert, sondern durch pr\u00fcfbare Beziehungen zwischen Mechanismus, Intervention, Beobachtung und Schlussfolgerung. Diese Fassung verbindet die vollst\u00e4ndige theoretische Abhandlung mit einer quellengebundenen Neubewertung der ausgef\u00fchrten Protokolle.

Der Ausdruck Rekursive Epistemik bezeichnet hier eine Untersuchung der Herkunft, Verarbeitung und Kontrolle von Wissen in technisch geschlossenen und zugleich extern entworfenen Systemen. Er ist kein Messwert und keine Behauptung einer neuen physikalischen Dimension. MHRN trennt den prim\u00e4ren adaptiven SNN-Zustand von Sprachmodellen, externen Datenbest\u00e4nden und menschlichen Entscheidungen. Diese Trennung macht Zuschreibungen kontrollierbar; sie beweist nicht, dass jede beobachtete Leistung aus dem neuronalen Kern stammt.

## Punktneuronen und numerischer Vertrag

Das Izhikevich-Modell [1] beschreibt Membranvariable v und Recovery-Variable u durch

$$\dot v = 0.04v^2+5v+140-u+I,\qquad \dot u=a(bv-u).$$

Nach dem definierten Schwellenereignis erfolgt der Reset v auf c und die Erh\u00f6hung von u um d. Der verwendete diskrete Algorithmus ist von diesen kontinuierlichen Gleichungen zu unterscheiden: Integrationsschritt, Reihenfolge der v-/u-Aktualisierung, Spike-Erkennung, Refrakt\u00e4rbehandlung und Zustandserfassung geh\u00f6ren zum pr\u00fcfbaren Vertrag. In der isolierten Referenz d\u00fcrfen sekund\u00e4re Adaptationsmechanismen einen Modellvergleich nicht unbemerkt ver\u00e4ndern. Der alternative LIF-Pfad ersetzt den Membranintegrator; er ist nicht einfach ein zus\u00e4tzlicher Stromterm.

Die implementierten Varianten stehen in `src/core/neuron.py` und `src/core/neuron_models.py`. Der externe Einzelzellvergleich liegt in `src/research/empirical_evaluation.py`. Brian2 unterscheidet explizite Ausf\u00fchrungsphasen und die Phase eines Monitors [2,3]. Deshalb sind identische Modellgleichungen allein kein Nachweis identischer diskreter Spikefolgen. Ein nicht bestandenes Konformit\u00e4tskriterium bleibt ein negativer Befund; eine nachtr\u00e4gliche Toleranzlockerung w\u00e4re ein neues Protokoll und keine Korrektur der alten Daten.

## Rekurrenz, Identit\u00e4t und Raum

Der kanonische Kern benutzt kompatible f\u00fcnfdimensionale Koordinaten und verz\u00f6gerte Ereignisse. Eine Koordinate ist ein technischer Adress- und Topologieparameter, keine zus\u00e4tzliche Raumzeit. Entscheidend sind die tats\u00e4chlich erzeugten Kanten, Gewichte, Verz\u00f6gerungen und Eing\u00e4nge. Die Dimensionsstudien unterscheiden daher ver\u00e4nderte Graphgeometrie von einem blo\u00df ver\u00e4nderten Label auf identischem Graphen. Vergleichbare Knoten- und Kantenbudgets beseitigen nicht automatisch Unterschiede in Eingangsgrad, Motiven oder erreichbaren Pfaden.

Die Aussage, ein rekurrentes Netzwerk sei technisch vorhanden, l\u00e4sst sich an Laufzustand, Ereignis\u00fcbertragung, Wiederholung und Wiederherstellung pr\u00fcfen. Die weitergehende Behauptung eines n\u00fctzlichen, robusten rekurrenten Rechenmechanismus verlangt eine aufgabenbezogene Intervention, etwa Rekurrenz an/aus bei sonst gleichen Bedingungen. Blo\u00dfe Spikezahl, endliche Spannung oder ein sichtbarer Graph ersetzen diese Intervention nicht.

## Lernen und mehrere Zeitskalen

STDP koppelt Gewichts\u00e4nderung an die zeitliche Beziehung pr\u00e4- und postsynaptischer Ereignisse. Eine Drei-Faktor-Regel verbindet diese lokale Vorbedingung mit einem zus\u00e4tzlichen modulatorischen Signal. Als abstraktes Schema, nicht als vollst\u00e4ndige Spezifikation jeder implementierten Variante, gilt

$$\dot e_{ij}=-e_{ij}/\tau_e+F(s_i,s_j),\qquad \Delta w_{ij}=\eta\,r\,e_{ij}.$$

Die konkreten Vorzeichen, Schranken, Zeiteinheiten und Aktualisierungszeitpunkte sind dem eingefrorenen Code und der Konfiguration zu entnehmen. Der mechanistische Gedanke einer zeitlich \u00fcberdauernden Eligibility-Trace ist in der Literatur motiviert [4]. Der Literaturbezug ist jedoch kein Wirksamkeitsnachweis der MHRN-Implementierung.

Der Stage-3-Vertrag verbindet Tests von STDP, Reward/Eligibility, Hom\u00f6ostase, struktureller Plastizit\u00e4t und checkpointbarem Lernzustand mit deterministischen Learning-on/off/Sham-Kontrollen. Diese Batterie pr\u00fcft mehrere Komponenten und einen begrenzten Lernversuch. Sie ist nicht mit einem einzigen gleichzeitig vollplastischen Langzeitnetz aus 100.000 Neuronen gleichzusetzen. Insbesondere sind eine Gewichtszunahme, eine ge\u00e4nderte Probeantwort und eine Verbesserung auf wirklich neuen Testepisoden verschiedene Endpunkte.

## Hom\u00f6ostase und strukturelle Plastizit\u00e4t

Feuerraten-, Schwellen- und Energiekontrollen begrenzen ausgew\u00e4hlte Zustandsgr\u00f6\u00dfen. Eine lokale Schranke beweist weder globale asymptotische Stabilit\u00e4t noch die Stabilit\u00e4t unter allen Reglerkombinationen. Mehrere Regelkreise k\u00f6nnen gegeneinander arbeiten; identische Endzust\u00e4nde k\u00f6nnen durch verschiedene Beitr\u00e4ge entstehen. Deshalb sind mechanistische Ablationen, aufgezeichnete Reglerbeitr\u00e4ge, St\u00f6rungen und Erholungsma\u00dfe erforderlich.

Strukturelle Ver\u00e4nderungen besitzen einen Freigabe- und Persistenzpfad statt eines unsichtbaren direkten Eingriffs. Vorschlag, Entscheidung, begrenzte Mutation, Journal und Wiederherstellung sind Engineering-Vertr\u00e4ge. Ein nachweisbarer Mutationseintrag ist noch kein Beleg, dass die neue Topologie eine Aufgabe besser l\u00f6st. Diese Unterscheidung gilt auch f\u00fcr Heatmaps und historische Strukturansichten.

## Erweiterte biophysikalische Modelle

Der Quellstand enth\u00e4lt experimentelle Klassen und Vertr\u00e4ge f\u00fcr Hodgkin-Huxley-artige Kan\u00e4le, Kompartimente, NMDA-artige Nichtlinearit\u00e4t, Gap Junctions, Astrozyten-/Mikroglia-Modelle, langsame Konsolidierung, Rezeptor-Trafficking und stochastische synaptische Freisetzung. Deren konkrete Modelle sind in den entsprechenden `src/core`-Modulen und den Ablationstests offengelegt. Sie erweitern den Modellraum; sie sind kein Nachweis einer biologischen Vollsimulation.

Das Vorhandensein einer Klasse bedeutet nicht, dass diese Mechanik im produktiven Runtime-Pfad, in jedem Snapshot oder in allen Skalierungsversuchen aktiviert ist. Modellwahl, Integrator, Parameter und aktivierte Nebenmechanismen m\u00fcssen pro Versuch aufgezeichnet werden. Eine biologische Interpretation ben\u00f6tigt dar\u00fcber hinaus unabh\u00e4ngige Referenzdaten, Identifizierbarkeit und anwendungsbezogene Validierung.

## Speicher, Kognition und K\u00f6rpergrenze

Snapshots, Delta- und Strukturjournale dienen reproduzierbarer Fortsetzung. Die Aussage gilt jeweils f\u00fcr den vertraglich erfassten Zustand. Ein funktionierender Core-Checkpoint beweist nicht automatisch die deterministische Wiederherstellung eines gekoppelten Gesamtsystems aus Working Memory, episodischem Speicher, Weltmodell, Behavior Profile, Gateway und externen Diensten. Diese gekoppelte Grenze bleibt gesondert zu pr\u00fcfen.

Die vorhandenen Kognitionskomponenten sind begrenzte technische Funktionen: Speicherzugriff, Ein-Schritt-Vorhersage und Auswahl zwischen expliziten Aktionskandidaten. Die Studien pr\u00fcfen diese Komponenten und ihre Kontrollarme. Weder ein besserer Pr\u00e4diktionswert noch ein adaptierter Profilparameter allein rechtfertigt Begriffe wie subjektives Selbst, allgemeines Weltverst\u00e4ndnis oder autonome Zielbildung.

Sensoren und Aktoren sind explizit autorisierte Adapter. Ein fehlendes Ger\u00e4t wird nicht durch eine plausible Kamera- oder Audiodatenquelle ersetzt. Die K\u00f6rperansicht ist eine Projektion beobachteter technischer Verbindungen. Closed-loop-Leistung muss gegen Replay/Open-loop, wirkungslose Aktoren und Sensorst\u00f6rungen abgegrenzt werden. Dabei ist der Beitrag vorgeschalteter Regler und externer Modelle offenzulegen.

## Gateway, exakte Daten und CUDA

Das Gateway trennt exakte digitale Payloads von neuronalen Repr\u00e4sentationen sowie Codec, Projektion und Gateway-Lernen. Experimentelle Frozen-/Random-/Shuffle-Kontrollen erlauben begrenzte Funktionspr\u00fcfungen. Erreichbarkeit eines Endpunkts und korrekte Checksummen sind notwendige technische Eigenschaften, aber kein Beleg eines gelernten semantischen Verst\u00e4ndnisses.

Der neue Gateway-Neural-Interface-Vertrag v0.4 und der CUDA-Vertrag v0.3 sind Architekturarbeit. Der CUDA-Text erkl\u00e4rt selbst, dass noch keine CUDA-Implementierung vorliegt. CPU-Messungen, theoretische Speicherbudgets oder ein beschriebenes Kernel-Layout werden deshalb nicht als gemessene GPU-Beschleunigung ausgegeben. Externe Projektionsr\u00e4ume von 1 bis 32 Dimensionen sind vom weiterhin f\u00fcnfdimensionalen Persistenz-/ID-Vertrag zu unterscheiden.

## Beobachtbarkeit statt Darstellungswirkung

Dashboard, Chat und File Viewer sind Werkzeuge zur Inspektion. Die zentrale Ausgabe soll dieselben kanonischen Artefakte erschlie\u00dfen und unbekannte Werte als unbekannt anzeigen. Der Audit behebt deshalb rekursive Dokument-Cache-Aufrufe und bindet Frontend-Pr\u00fcfungen an tats\u00e4chlich geladene Stylesheets und den aktuellen Router. Solche Reparaturen verbessern Verf\u00fcgbarkeit und Pr\u00fcfbarkeit, erzeugen aber keine neue wissenschaftliche Evidenz.
"""

METHODS = r"""# Methodik, Ausf\u00fchrung und statistische Interpretation

## Quellenstand und Auswahl

Die Kampagne wird vor dem ersten Protokoll auf einen Git-Commit, einen Digest der relevanten Quellen, eine konkrete Konfiguration und eine vollst\u00e4ndige Auswahl gebunden. Code und wissenschaftlicher Plan m\u00fcssen sauber sein. Jeder Versuch startet in einem eigenen Prozess; die Prozesse werden seriell ausgef\u00fchrt. Ausgaben liegen w\u00e4hrend der Messung au\u00dferhalb des Quellbaums. Nach Ende wird die Quellenidentit\u00e4t erneut gepr\u00fcft.

Die Auswahl ist eine erneute explorative Ausf\u00fchrung registrierter Vertr\u00e4ge. Eine Registrierung im eigenen Repository wird nicht als unabh\u00e4ngige externe Pr\u00e4registrierung ausgegeben. Neue Analysen dieser Daten sind nachtr\u00e4gliche Interpretation, sofern kein vorher eingefrorener Auswertungsvertrag das konkrete Verfahren bereits nennt. Weitere wissenschaftliche Freigabe bleibt ein separater, menschlicher Schritt.

Die Ausf\u00fchrungskategorien werden nicht zusammengerechnet, als h\u00e4tten sie denselben Erkenntniswert. Ein direkt instrumentiertes Funktionsprotokoll, eine Grenzpr\u00fcfung, eine kombinierte Engineering-Suite und ein Fragebogen sind verschiedene Instrumente. Grenzpr\u00fcfungen dokumentieren beispielsweise eine fehlende Operationalisierung oder eine Schutzgrenze; sie beantworten nicht automatisch die zugeordnete inhaltliche Hypothese. Menschliche Vorlagen werden nicht mit automatisch ausgef\u00fcllten Antworten ersetzt.

## Beobachtungen, Provenienz und Ausf\u00e4lle

Pro Protokoll werden Auswahl, Manifest, komprimierte Rohdaten und ein Receipt mit SHA-256 der komprimierten und unkomprimierten Bytes gespeichert. Vor der Auswertung werden beide Digests sowie Identit\u00e4t, Status und Zahl der Datens\u00e4tze abgeglichen. Ein fehlender oder widerspr\u00fcchlicher Beleg macht den Auswertungszweig ung\u00fcltig. Nichtendliche numerische Werte und dokumentierte Runtime-Fehler werden nicht zu unauff\u00e4lligen Nullwerten gegl\u00e4ttet.

F\u00fcr jede beobachtete Bedingung wird gepr\u00fcft, ob alle deklarierten Seeds vorkommen. Diese Pr\u00fcfung allein beweist nicht, dass die Implementierung alle wissenschaftlich beabsichtigten Bedingungen erzeugt: Daf\u00fcr bleibt der Vergleich von Protokolltext, Runner und aufgezeichneten Bedingungsnamen notwendig. Ein Prozess-Timeout und ein negatives Hypothesenergebnis sind ebenfalls verschieden. Ein korrekt ausgef\u00fchrter Versuch darf das Erfolgskriterium verfehlen, ohne als Laufzeitfehler umgedeutet zu werden.

Einzelne Seeds, Bedingungen, Episoden und Ticks sind nicht austauschbare Stichprobeneinheiten. Die berichtete Anzahl gespeicherter Zeilen ist deshalb ein Rechenschaftsma\u00df, nicht automatisch eine inferentielle Stichprobengr\u00f6\u00dfe. Deterministisch identische Resultate unter verschiedenen Seed-Labels liefern keine unabh\u00e4ngigen stochastischen Wiederholungen. Bei gepaarten Armen ist der unabh\u00e4ngige Initialisierungs-/Umwelt-Seed die zentrale Analyseeinheit.

## Vorhandene Kontraste

Der Assoziationsversuch verwendet frische Testepisoden, eingefrorene Gewichte und Kontrollen mit deaktiviertem Lernen, Sham-Replay, zur\u00fcckgesetzten und permutierten Gewichten. Ein Trainingseffekt ist nur dann von blo\u00dfer Gewichts\u00e4nderung zu unterscheiden, wenn die gehaltene Testinformation nicht schon als Teacher-Signal oder Parameterwahl in das Ergebnis eingeht. Die konstruierten Eingabepopulationen und die externe Anleitung w\u00e4hrend der Akquisition sind Teil der Behandlung und werden nicht verborgen.

Die vorhandene Auswertung verwendet gepaarte Seed-Differenzen, Bootstrap-Perzentilintervalle und einen exakten zweiseitigen Vorzeichenwechseltest f\u00fcr die daf\u00fcr vorgesehenen Zehn-Seed-Vergleiche. Ein solcher Test setzt die f\u00fcr die Nullhypothese geeignete Austauschbarkeit beziehungsweise Symmetrie voraus; das Verfahren beweist seine Voraussetzungen nicht selbst [5]. Holm-Korrektur wird innerhalb der jeweils deklarierten Kontrastfamilie berichtet. Sie korrigiert nicht nachtr\u00e4glich die gesamte explorative Suche \u00fcber s\u00e4mtliche Protokolle.

Die Dimensionsauswertung vergleicht Aufgabenobservablen bei ge\u00e4nderter Graphgeometrie und kontrolliert separat die Wirkung blo\u00dfer Dimensionslabels. Ein Intervall, das null einschlie\u00dft, ist kein \u00c4quivalenzbeweis. Das Fehlen eines signifikanten 5D-Vorteils kann aus einem kleinen oder variablen Effekt, unzureichender Pr\u00e4zision oder mangelnder Aufgabensensitivit\u00e4t entstehen. Die zul\u00e4ssige Aussage bleibt daher auf die gemessene Aufgabe, Budgets und Kontraste begrenzt.

## Stabilit\u00e4t, Ressourcen und Skalierung

Lange stabile Referenzl\u00e4ufe pr\u00fcfen den gew\u00e4hlten Antrieb und die gew\u00e4hlte Topologie. Ein stilles Netz ist nicht automatisch ein n\u00fctzlich rechnendes Netz. Deshalb werden Nullinput, tonischer Antrieb, Spikes, synaptische Zustellung und Zustandsgrenzen getrennt betrachtet. Die maximale Zahl ausf\u00fchrbarer Ticks ist kein Ersatz f\u00fcr kontrollierte Langzeitlernstabilit\u00e4t.

Skalierungstabellen nennen nur die tats\u00e4chlich gespeicherten Gr\u00f6\u00dfen und Messfenster. Die gro\u00dfe Knotenzahl eines kurzen Sparse-Runs darf nicht mit einem langdauernden, vollplastischen, hochaktivierten biologischen Netz gleichgesetzt werden. RSS beinhaltet Interpreter und Bibliotheken und ist keine isolierte Spitzenallokation. CPU-Zeit, Simulationszeit und Wandzeit sind verschieden. Softwareinterne Energie- oder Ressourceneinheiten sind ohne physikalische Kalibrierung keine Joule.

Serielle Prozesse reduzieren direkte Konkurrenz innerhalb einer Kampagne, garantieren jedoch keinen exklusiven physikalischen Host. Die Umgebung wird deshalb mit Plattform, Python-/Paketversionen, CPU-Zahl und relevanten Thread-Variablen protokolliert. Leistungsaussagen gelten f\u00fcr diese Umgebung. Gleichzeitige lokale Diagnostik, Betriebssystemlast, Warm-up und Importkosten sind m\u00f6gliche St\u00f6rfaktoren; es wird kein fairer plattform\u00fcbergreifender Geschwindigkeitsrekord behauptet.

## Reproduzierbarkeit und Unabh\u00e4ngigkeit

Reproduktion bedeutet hier, die dokumentierte Software unter den deklarierten Bedingungen erneut auszuf\u00fchren. Eine unabh\u00e4ngige Replikation verlangt dar\u00fcber hinaus geeignete personelle beziehungsweise methodische Unabh\u00e4ngigkeit. Ein Runner mit dem Wort independent im Namen erf\u00fcllt diese Bedingung nicht durch seinen Namen. Das gilt ebenso f\u00fcr ein KI-generiertes Review: Es bleibt eine Interpretation mit offengelegter Assistenz, keine unabh\u00e4ngige Fachentscheidung.

Die bisherigen Ausgaben und Messdaten bleiben unver\u00e4ndert. Eine Quellen- oder Instrumentierungsreparatur erzeugt eine neue Version und neue Beobachtungen. Die alte Nullbeobachtung, ein fehlerhafter Skalierungsversuch oder ein nicht bestandener Frameworkvergleich wird nicht durch sp\u00e4tere Daten ersetzt. Softwareversion 0.6.0-alpha.3 und Publikationsfassung 1.5 bezeichnen unterschiedliche Artefakte.
"""

DISCUSSION = r"""# Diskussion, Fortschrittsbewertung und Grenzen

## Was als Fortschritt gilt

Der zentrale Fortschritt besteht in einer auswertbaren Verbindung von Code, Kontrollbedingungen, aufgezeichneten Daten und begrenzten Aussagen. Die Plattform enth\u00e4lt inzwischen mehr als Entw\u00fcrfe und Unit-Tests: Es gibt native Lern-, Rekurrenz-, Dimensions-, Speicher-, Verk\u00f6rperungs- und Skalierungsmessungen. Die genaue Ausf\u00fchrungsbilanz und die Prim\u00e4rma\u00dfe stehen im Ergebnisteil. Das allein macht jedoch keine der weitergehenden allgemeinen Hypothesen wahr.

Drei Ebenen bleiben getrennt. Erstens: Ein Mechanismus ist implementiert und erreichbar. Zweitens: Eine bestimmte kontrollierte Ausf\u00fchrung erzeugt eine reproduzierbare Beobachtung. Drittens: Fachlich begutachtete, hinreichend unabh\u00e4ngig best\u00e4tigte Befunde tragen eine bestimmte wissenschaftliche Behauptung. Ein gr\u00fcnes Engineering-Gate betrifft vor allem die erste und Teile der zweiten Ebene. Es darf die dritte nicht durch eine Farbe ersetzen.

## Lernbefunde und Zuordnung

Ein positiver nativer Assoziationskontrast ist relevant, weil eingefrorene Testgewichte und frische Episoden die Erkl\u00e4rung durch eine blo\u00dfe unmittelbare Teacher-Probe einschr\u00e4nken. Seine Reichweite bleibt eine konstruierte Aufgabe mit vorgegebenem Inputraum, Reward und Architektur. Er beweist weder selbst erzeugte Ziele noch allgemeine Sprache, neuronales autobiografisches Ged\u00e4chtnis oder menschliche Begriffsbildung. Kontrollen mit identischen Ergebnissen sind keine voneinander unabh\u00e4ngigen Best\u00e4tigungen.

In \u00e4lteren Lernprotokollen k\u00f6nnen deklarierte Holdout-Gr\u00f6\u00dfen und tats\u00e4chlich ausgef\u00fchrte Probeepisoden auseinanderfallen. Die neue Fassung bewertet deshalb die aufgezeichneten Interventionen, nicht allein die Feldnamen. Ein Interferenz-Screen mit getrennten Task-Netzen ist kein Nachweis gegen katastrophales Vergessen in einem gemeinsam weitertrainierten Netz. Ebenso darf ein nichtneuronaler Pr\u00e4diktor oder Ressourcenregler nicht ohne Ablation als Leistung des SNN bezeichnet werden.

## Negative Befunde als Erkenntnis

Die Dimensionsfrage ist eine Hypothese, keine Namensdefinition. Wenn die deklarierten Vergleiche keinen belastbaren Vorteil der 5D-Geometrie zeigen, wird genau dies berichtet. Daraus folgt weder die Unm\u00f6glichkeit eines Effekts auf anderen Aufgaben noch ein Nachweis der Gleichwertigkeit aller Dimensionen. Ein angemessener n\u00e4chster Versuch ben\u00f6tigt eine festgelegte Aufgabe, eine praktisch relevante Effektgrenze und ein ausreichend pr\u00e4zises Design statt weiterer attraktiver Visualisierungen.

Die externe Einzelzellkonformit\u00e4t pr\u00fcft einen besonders strengen diskreten Vertrag. Kleine Rechendifferenzen k\u00f6nnen in einem System mit Schwellen und Resets unterschiedliche Ereignisse erzeugen; ob dies den konkreten Befund vollst\u00e4ndig erkl\u00e4rt, muss durch isolierte Interventionen gezeigt werden. Deshalb bleiben Ein-Schritt-Vergleich, explizite Rechenausdr\u00fccke, Datentypen, Ereignisphasen und Spike-Matching-Toleranzen getrennte prospektive Pr\u00fcfungen. Die Toleranz wird nicht anhand eines gew\u00fcnschten Resultats nachjustiert.

## Was nicht geschlossen ist

Gro\u00dfe Zahl von Testf\u00e4llen, viele Protokollzeilen und lange L\u00e4ufe k\u00f6nnen dieselbe begrenzte Annahme wiederholt testen. Offene Punkte sind deshalb nicht nur fehlende Ausf\u00fchrungszeit. Es fehlen bei einem Teil des Registers unmittelbare Messkonstrukte, bei mehreren Integrationsfragen ein validierter gemeinsamer Zustand, bei weitreichenden Lernbehauptungen anspruchsvolle Generalisierungsaufgaben und bei wissenschaftlicher Freigabe unabh\u00e4ngige Menschen.

Insbesondere bleiben die volle gekoppelte Kognitions-Wiederherstellung, Generalisierung jenseits der konstruierten Assoziationsaufgabe, ein langzeitig vollplastisches Zielnetz unter deklariertem Ressourcenbudget, produktives Gateway-Lernen und ein gemessener CUDA-Backendvergleich eigene Abnahmekriterien. Mechanistische Tests f\u00fcr biophysikalische Erweiterungen ersetzen keine experimentelle neurobiologische Validierung. Diese L\u00fccken werden nicht durch allgemeine Begriffe wie Nervengewebe, Selbstmodell oder Bewusstsein geschlossen.

## Theorie und empirische Disziplin

Die theoretische Abhandlung untersucht delegierte Handlungsmacht, Wissensherkunft, rekursive technische Entwicklung und nichtorganisches Embodiment. Diese Begriffe k\u00f6nnen Beobachtungen ordnen und Versuche motivieren. Damit sie empirischen Gehalt gewinnen, m\u00fcssen unterschiedliche Deutungen unterschiedliche, messbare Vorhersagen unter geeigneten Interventionen liefern. Die Erkl\u00e4rung einer Funktionskette und die Zuschreibung eines Erlebens bleiben verschiedene Probleme.

Der methodische Vorsprung einer strikten Systemgrenze liegt darin, unerlaubte Schlussfolgerungen sichtbar zu machen. Ein externer Sprachgenerator kann eine beeindruckende Antwort liefern, ohne dass der SNN-Kern die entsprechende Information erworben hat. Eine Speicherkomponente kann einen Inhalt korrekt zur\u00fcckgeben, ohne dass dessen Entstehung durch neuronales Lernen erkl\u00e4rt ist. Eine Ethikrichtlinie kann vorsorglich sinnvoll sein, ohne das Vorliegen von Leidensf\u00e4higkeit festzustellen.

## Fazit

Die vorliegende Fassung dokumentiert eine reale technische und empirische Weiterentwicklung sowie reale Grenzen. Sie stellt den Stand weder als reine Ideenskizze noch als abgeschlossene allgemeine Intelligenz dar. Die verbleibende wissenschaftliche Aufgabe ist die gezielte Schlie\u00dfung klar definierter Evidenzl\u00fccken. Akzeptierte Evidenz entsteht aus einer nachvollziehbaren Pr\u00fcfung der Daten und ihrer Reichweite, nicht aus automatisch fortgeschriebenen Prozentanzeigen.
"""

REVIEW = r"""# Review, Verantwortung und Weiterf\u00fchrung

Das angek\u00fcndigte menschliche Review steht aus. Weder diese Ausgabe noch eine erfolgreiche CI-Ausf\u00fchrung liefert stellvertretend eine fachliche Annahmeentscheidung, ein institutionelles Mandat oder ein externes Ethikvotum. Die Bezeichnung Dissertationsmanuskript beschreibt eine Textgattung; sie behauptet keine Einreichung, Annahme oder Verleihung eines akademischen Grades.

Das Review sollte jede wesentliche Schlussfolgerung mit dem zugeh\u00f6rigen Versuch, dem prim\u00e4ren Endpunkt und den Grenzen verbinden. Erforderlich sind insbesondere die Pr\u00fcfung der Seed-/Bedingungsabdeckung, m\u00f6glicher Informationsleckage, der Rolle externer Regler, der statistischen Einheit und der Unabh\u00e4ngigkeit von Replikationen. Eine Zustimmung zur Interpretation ist nicht dasselbe wie die Freigabe eines EVID-Objekts.

Die offene Arbeitsliste unterscheidet ausf\u00fchrbare und ausgef\u00fchrte Protokolle, fehlende Instrumentierung, externe Voraussetzungen und menschliche Entscheidungen. Ein erneuter Lauf ohne ge\u00e4nderte methodische Frage schlie\u00dft keine fehlende Operationalisierung. F\u00fcr die n\u00e4chste konfirmatorische Stufe sind Hypothese, Population beziehungsweise Aufgabenverteilung, Kontrollarme, Stopping Rule, Ausschlussregeln, prim\u00e4res Ma\u00df und Auswertung vor der neuen Datenerzeugung festzulegen.

Vorsorgliche Ethik, Zugangsbeschr\u00e4nkungen und ein technisch unabh\u00e4ngiger Abbruchpfad bleiben unabh\u00e4ngig von metaphysischen Zuschreibungen sinnvoll. Die Plattform darf nicht allein \u00fcber ihre eigene Fortsetzung entscheiden. Werden menschliche Probanden, personenbezogene Daten oder reale Aktoren einbezogen, sind die konkreten organisatorischen und rechtlichen Voraussetzungen vor der betreffenden Studie zu kl\u00e4ren; eine Simulation oder ein Fragebogenentwurf ersetzt diese Pr\u00fcfung nicht.

KI-Unterst\u00fctzung wird f\u00fcr Quellpr\u00fcfung, Instrumentierung, Dokumentation und Interpretation offengelegt. Die Verantwortung f\u00fcr wissenschaftliche Behauptungen und Freigaben bleibt bei den benannten Menschen. Automatische Evidenz-Promotion ist in dieser Ausgabe ausdr\u00fccklich ausgeschlossen.
"""

REFERENCES = """# Methodische Quellen und Artefaktnachweise

[1] Izhikevich, E. M. (2003). Simple Model of Spiking Neurons. IEEE Transactions on Neural Networks, 14(6), 1569-1572. DOI: 10.1109/TNN.2003.820440. Autorenfassung und Referenzprogramm: https://izhikevich.org/publications/spikes.htm .

[2] Brian2-Autoren (Dokumentation 2.10.1). Example: Izhikevich_2003. https://brian2.readthedocs.io/en/2.10.1/examples/frompapers.Izhikevich_2003.html . Das dortige Standardbeispiel ist nicht identisch mit jedem MHRN-Vergleichspfad.

[3] Brian2-Autoren (Dokumentation 2.10.1). Running a simulation, insbesondere Scheduling und Store/restore. https://brian2.readthedocs.io/en/2.10.1/user/running.html .

[4] Izhikevich, E. M. (2007). Solving the Distal Reward Problem through Linkage of STDP and Dopamine Signaling. Cerebral Cortex, 17(10), 2443-2452. DOI: 10.1093/cercor/bhl152. Autorenfassung: https://www.izhikevich.org/publications/dastdp.htm . Mechanistisches Modell; keine MHRN-Validierung.

[5] SciPy-Entwickler. scipy.stats.permutation_test, offizielle API-Dokumentation. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html . Die verwendete eigene Vorzeichenwechselroutine und ihre konkreten Parameter stehen im eingefrorenen Kampagnenskript; die Referenz begr\u00fcndet keine ungepr\u00fcfte Austauschbarkeit der Daten.

Prim\u00e4re MHRN-Quellen sind der in der Kampagne genannte Git-Commit, plan.json, die einzelnen selection.json/manifest.json/receipt.json, die unver\u00e4nderten runs.json.gz und summary.json. Die bisherigen Literaturverzeichnisse und theoretischen Quellen sind im vollst\u00e4ndig erhaltenen Haupttext und in literatur_revision.bib enthalten. Externe Methodenquellen ersetzen nicht die experimentellen Artefakte.
"""


def decode_text(text: str) -> str:
    """Decode only deliberate Unicode escapes, preserving mathematical slashes."""
    import re

    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m[1], 16)), text)
