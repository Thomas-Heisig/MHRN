# EXP-GEN-0036 — Human Review und Design-Audit

**Datum:** 2026-09-16  
**Status:** post-hoc Human Review; keine Änderung der archivierten DATA  
**Experiment:** `EXP-GEN-0036`  
**Primäre RQ:** `RQ-SUITE-001`  
**Evidenzrolle:** Diagnose-/Infrastrukturprüfung; keine automatische Fach-Evidenzfreigabe

## 1. Zweck dieser Review

Diese Review korrigiert eine zunächst naheliegende, aber nach Prüfung der Rohartefakte falsche Interpretation der generierten `summary.md`: Die dort bei mehreren Bedingungen angezeigten Gedankenstriche (`—`) bedeuten **nicht**, dass die entsprechenden Teilprotokolle nicht ausgeführt wurden oder keine DATA erzeugt haben.

Die archivierten Rohdaten und die deterministische Statistik zeigen, dass die Science Suite alle registrierten Protokollgruppen ausgeführt hat. Der Fehler lag in der **Berichtsprojektion**: Die Haupttabelle der Zusammenfassung war auf SNN-Metriken wie Spike-Zahl, synaptische Events und Propagation Depth festgelegt. Trial-, Lern-, STDP-, TIME- und Regulationsprotokolle besitzen andere Metriken und erschienen deshalb in diesen Spalten als `—`.

Die historischen DATA bleiben unverändert.

## 2. Korrigierte Suite-Bilanz

### 2.1 Ausführung

`EXP-GEN-0036` enthält 180 Runs über zehn Seeds. In den archivierten Runs sind die registrierten Gruppen vorhanden:

- `ping:*`
- `temporal:*`
- `stdp:*`
- `learning:*`
- `time:*`
- `5d:*`
- `regulation:*`

Auch die deterministische `analysis/statistics.json` enthält Statistikblöcke für die nicht-SNN-förmigen Protokolle, darunter Lerngewichte, Trial-Zahlen, STDP-bezogene Größen, Laufzeitmetriken und Regulationszustände.

### 2.2 Konsequenz für H-SUITE-001-A

Die Behauptung, H-SUITE-001-A sei allein deshalb widerlegt, weil neun Bedingungen keine DATA erzeugt hätten, ist **nicht haltbar**. Die zugrunde gelegte Prämisse — fehlende Runs/fehlende Statistik — trifft nach Prüfung der archivierten Artefakte nicht zu.

Damit ist jedoch noch nicht automatisch gezeigt, dass die Suite wissenschaftlich vollständig oder für jede enthaltene Fach-RQ aussagekräftig ist. Zu unterscheiden sind:

1. **Artefaktvollständigkeit:** Runs und protokollspezifische Messwerte sind vorhanden.
2. **Interne Konsistenz:** DATA, Statistik, Provenienz und Report müssen widerspruchsfrei zusammenpassen.
3. **Fachliche Testadäquanz:** Ein ausgeführtes Teilprotokoll muss die jeweilige Forschungsfrage tatsächlich operationalisieren.

`RQ-SUITE-001` bleibt daher als **diagnostische Human-Review-Frage** zu behandeln. Der konkrete Fehler dieses Laufs liegt primär in der Reporting-/AIRR-Schicht, nicht in einem Ausfall der registrierten Runner.

## 3. 5D-Teilstudie: stärkeres Designproblem als Unterpowerung

Der zunächst formulierte Befund „zu kleines beziehungsweise zu inaktives Netzwerk“ ist richtig, aber unvollständig.

`run_5d()` erzeugt in der gegenwärtigen v1-Implementierung für jede Dimensionsbedingung eine kontrollierte Kette mit nur drei Neuronen. Die Dimensionskoordinaten werden verändert, die eigentliche Dynamik dieser Kette wird dadurch aber nicht dimensionsabhängig parametrisiert: Die wesentlichen Verbindungen, Gewichte und Delays werden explizit gesetzt.

Damit ist das aktuelle Protokoll **konstruktiv kaum sensitiv für einen geometrischen Dimensionalitätseffekt**. Identische Spike-Zahlen zwischen 1D, 2D, 3D und 5D sind deshalb nicht als Nullbefund für eine 5D-Hypothese zu lesen.

### Review-Status für 5D

**RQ-5D-005: NOT TESTED durch dieses Teilprotokoll für einen genuinen Geometrieeffekt.**

Begründung:

- nur drei aktive Knoten,
- sehr geringe Aktivität,
- feste Kettenkonnektivität,
- keine hinreichende Kopplung zwischen räumlicher Einbettung und der zu messenden Dynamik.

Eine Nachfolgeversion muss vor Ausführung explizit festlegen, **über welchen Mechanismus** 5D-Geometrie einen Unterschied erzeugen darf, beispielsweise Nachbarschaftsbildung, distanzabhängige Delays, distanzabhängige Konnektivität oder eine registrierte Plastizitätsregel. Ohne eine solche Kopplung ist „Dimension“ lediglich Metadaten-/Koordinatenvariation.

## 4. Recurrence-Befund

Die PING-Bedingungen zeigen einen starken deskriptiven Unterschied zwischen `recurrence_off` und `recurrence_on`.

Die Implementierung ist kontrollierter, als eine reine Betrachtung der Reportwerte vermuten lässt: Beide Bedingungen werden mit derselben `_network()`-Konstruktion erzeugt; die Recurrence-Bedingung ergänzt gezielt die Rückkante vom Output zum Input. Dennoch bleibt der aktuelle Lauf ein sehr kleines mechanistisches Netzwerk und die über Seeds identischen Trajektorien sind keine zehn statistisch unabhängigen Replikate.

### Review-Status für PING

**Mechanistische Demonstration innerhalb des simulierten Systems; deskriptiv klar, aber keine breite Generalisierung.**

Für eine stärkere kausale Prüfung sollte die Nachfolgeversion zusätzlich automatisch nachweisen und archivieren:

- identische Basistopologie vor Intervention,
- identische Gewichte/Delays aller gemeinsamen Kanten,
- genau definierte Interventionsdifferenz,
- gepaarte Auswertung pro Seed,
- Aktivitäts- und Stabilitätskriterien vor der Effektinterpretation.

## 5. Temporal: 0 Spikes und trotzdem Diskrepanzwerte

Hier liegt kein notwendiger Datenwiderspruch vor.

Das Temporal-Protokoll berechnet pro Tick Zustandsframes mit unter anderem Membranpotential, Spike-Zahl und Synapsenzahl und vergleicht diese mit gespeicherten Referenzzuständen verschiedener Horizonte. Die daraus resultierende `discrepancy` ist eine **Zustandsvergleichsmetrik**, keine Spike-Metrik.

Deshalb können bei `total_spikes = 0` weiterhin definierte Diskrepanzwerte entstehen, wenn sich andere Bestandteile des Zustandsvektors verändern.

Die korrekte Interpretation lautet:

- für spikebasierte Aussagen ist die Bedingung quieszent,
- der registrierte Zustandsvergleich kann trotzdem ausgeführt worden sein,
- daraus folgt noch keine Aussage über lernende Vorhersage oder Prediction Error; diese sind im aktuellen Protokoll nicht verfügbar.

## 6. AIRR-Fehler

Der archivierte Scientific-Analyst-Output enthält verwertbaren Inhalt, aber in einer verschachtelten Struktur (`analysis`, `recommendations`, `limitations`). Die bisherige Normalisierung erwartete unter anderem ein flaches Top-Level-Feld `assessment`.

Dadurch wurde eine vorhandene Analyse fälschlich durch den Fallback „Analyse nicht verfügbar“ ersetzt und die Konfidenz konservativ auf `0.0` gesetzt.

Dies ist ein **technischer Schema-/Normalisierungsfehler der AIRR-Pipeline**, kein wissenschaftlicher Fehler der DATA. Der Fix adaptiert bekannte verschachtelte Strukturen deterministisch auf das kanonische AIRR-Schema. Der epistemische Status bleibt unverändert: KI-Auswertung ist Interpretation und **keine wissenschaftliche Evidenz**.

## 7. Konsequenzen für die nächste Experimentgeneration

### 7.1 Suite-Preflight und Vollständigkeits-Gate

Vor einer wissenschaftlichen Interpretation muss die Suite maschinell prüfen:

- erwartete Protokollgruppen vorhanden,
- erwartete Conditions vorhanden,
- DATA-Runzahl stimmt mit Statistik-Runzahl überein,
- jede Condition besitzt mindestens einen protokollspezifischen Statistikblock,
- Runtime-Fehler sind explizit gezählt,
- `—` in einer universellen Tabelle wird niemals als fehlende DATA interpretiert.

### 7.2 5D-v2

Vor einer neuen 5D-Ausführung ist eine neue Präregistrierung erforderlich. Mindestanforderungen:

- gleicher Knotenumfang über alle Dimensionsbedingungen,
- vorab definierter geometrischer Mechanismus,
- Aktivitäts-Adequanz-Gate vor der Hypothesenprüfung,
- topology-matched und/oder degree-matched Kontrollen entsprechend der konkreten Hypothese,
- `5d_shuffled` und Random-Graph-Kontrolle klar nach Kontrollzweck getrennt,
- ausreichend lange Dynamik und genügend aktivierte Neuronen/synaptische Ereignisse,
- keine Umdeutung eines fehlenden Aktivitätsregimes als Nullbefund.

### 7.3 Recurrence-v2/v3

- gepaarte Behandlung pro Seed,
- automatische Topologie-Diff-Prüfung,
- nur die registrierte Rekurrenzintervention darf zwischen Armen differieren,
- Effektgrößen auf gepaarten Runs,
- unabhängige Replikation erst dann als solche bezeichnen, wenn tatsächlich unabhängige Variation vorliegt.

## 8. Revidierte Gesamtbewertung

`EXP-GEN-0036` ist ein technisch valider Diagnose-Lauf, der einen **echten Reporting-/AIRR-Fehler** aufgedeckt hat. Die Science Suite hat die registrierten Protokollgruppen nicht einfach ausgelassen; die generierte Zusammenfassung hat verschiedene Protokolltypen in eine zu enge SNN-Metriktabelle projiziert.

Der wissenschaftlich wichtigste Negativbefund liegt stattdessen in der Testadäquanz einzelner Teilprotokolle: Insbesondere die 5D-v1-Studie operationalisiert einen geometrischen Dimensionseffekt nicht ausreichend und darf dafür nicht als bestätigende, widerlegende oder auch nur hinreichend sensitive Prüfung verwendet werden.

**Review-Fazit:**

- Suite-Runs/Statistik: **vorhanden; ursprüngliche Missing-DATA-Interpretation korrigiert**.
- H-SUITE-001-A: **nicht aufgrund fehlender neun Bedingungen widerlegt; Human Review der vollständigen Vertragskriterien erforderlich**.
- RQ-5D-005: **NOT TESTED durch 5D-v1 für einen geometrischen Effekt**.
- PING/Recurrence: **klarer mechanistischer deskriptiver Effekt; Nachfolgeprüfung mit explizitem Interventionsaudit empfohlen**.
- Temporal: **0 Spikes widersprechen Zustandsdiskrepanzmetriken nicht**.
- AIRR: **Schemaadaptionsfehler identifiziert und in der Pipeline korrigiert; weiterhin keine KI-Evidenz**.
