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
