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
