# Wie die wissenschaftlichen Reifegrade zu lesen sind

Stand 2026-10-24. Die Prozentwerte sind ein **gewichteter Dokumentations- und
Bearbeitungsindex**, keine Wahrscheinlichkeit einer wahren Hypothese, keine
Konfidenz, kein Anteil vorhandener Intelligenz und keine biologische Reife.
Die Gewichte sind Projektentscheidungen, nicht empirisch kalibrierte Parameter.

## Kriterien und Berechnung

| Kriterium | Gewicht | Was bewertet wird |
| --- | ---: | --- |
| Forschungsfrage | 15 % | explizite, zugeordnete RQ/H |
| Protokoll | 20 % | vorab operationalisierter und eingefrorener Prüfplan |
| DATA | 20 % | passende, prüfbare Messdaten im ausgewiesenen Geltungsbereich |
| Reviewte Evidenz | 20 % | fachliche Human Review und kanonische EVID-Promotion |
| Unabhängige Replikation | 15 % | tatsächlich unabhängige Prüfung/Bestätigung |
| Attribution | 10 % | nachvollziehbare Quellen- und Beitragszuordnung |

Die bestehende Statusskala lautet `met=1`, `partial=0.5`, `open=0`.
Für jede Stufe gilt `score = Summe(Gewicht × Statuswert)`. Das angezeigte
Stage-Mittel ist der ungewichtete Mittelwert der elf Stufen 0–10. Es ist
keine Vollständigkeitsmetrik des Gesamtforschungsprogramms: die Auswahl und
Granularität der Stufen beeinflussen es. Rundung erfolgt erst zur Anzeige.
`not_applicable` darf nicht still als Erfolg zählen: im aktuellen Manifest
sind alle sechs Kriterien anwendbar; eine Änderung braucht einen neuen
Berechnungsvertrag einschließlich Nennerregel.

`partial` ist grob und verlangt eine dokumentierte Begründung. Beispielsweise
trennt Stufe 1 fachliche Human Review und kanonische Promotion als zwei
Teilvoraussetzungen. Bei Stufe 0 steht `partial` für einen externen
Softwarevergleich plus interne Wiederholung, ausdrücklich nicht für eine
bereits unabhängige Replikation. 0.5 bedeutet weder halbe Sicherheit noch
eine halbe erfolgreiche Studie. Status und Quellen bleiben fachlich zu prüfen.

## Pflichtprüfungen sind nicht verrechenbar

Ein hoher Summenwert darf fehlende Freigaben nicht ersetzen. Vor einem Claim
müssen RQ/H-Zuordnung, Testadäquanz und tatsächliche kausale Intervention,
vorab festgelegte Auswertung, gültige vollständige DATA, saubere
Quellprovenienz, fehlerfreie Ausführung und kanonische Human Review passen.
`EvidenceEngine.promote_validated_experiment` verlangt Source-Freeze und
Human Review; weitere Eignungsprüfungen erfordern inhaltliche Bewertung und
sind nicht allein durch diese Prozentrechnung automatisiert. Eine Aussage
über unabhängige Replikation benötigt einen unabhängigen Nachweis.

Diese Voraussetzungen werden **nicht als zusätzliche numerische Abschläge
oder geheime Caps** in den Index eingerechnet. Sie begrenzen separat, welche
Aussage zulässig ist. Ein Score von 92.5 % kann daher zusammen mit der Grenze
„keine unabhängige Replikation“ auftreten. Das ist keine 92.5-%-Bestätigung.

## Audit und Korrektur vom 2026-10-24

Im bisherigen Dashboardmanifest stimmten nur Stufen 0 und 1 mit der
angegebenen gewichteten Statussumme überein. Für die anderen neun waren keine
maschinell nachvollziehbaren Abschläge hinterlegt. Die alten Werte wurden in
`research/reviews/MANUSCRIPT_FOLLOWUP_20261024/maturity-score-audit.json`
aufbewahrt. Das aktuelle Dashboard zeigt jetzt die nachgerechnete Summe;
Kriterienstatus, Quellen, Human Reviews und EVID-Register wurden dabei nicht
hochgestuft. Die numerische Änderung ist eine Berechnungskorrektur und kein
neuer Forschungsfortschritt. Historische Publikationswerte bleiben datierte
Darstellungen und dürfen nicht rückwirkend als so berechnet ausgegeben werden.

Die Prüfung `scripts/check_scientific_maturity_integrity.py` kontrolliert nun
zusätzlich eindeutige vollständige Kriterien und Übereinstimmung von Score
und Gewichtung. Sie bestätigt interne Konsistenz, nicht wissenschaftliche
Gültigkeit. Andere technische Gate-/Engineering-Prozentwerte haben andere
Nenner und dürfen nicht mit diesem Index vermischt werden.
