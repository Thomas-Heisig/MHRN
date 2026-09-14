# EXP-BATCH-20260914074039-89: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-GW-007`
- Hypothese: `H-GW-007-A`
- Protokoll: `gateway_resources_boundary_v1`
- Durchlaeufe: `3`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `1000`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `nicht direkt messbar .. nicht direkt messbar` ausgeführte Ticks
- Tick-Vertrag: `NOT_APPLICABLE`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `NOT_AUTOMATICALLY_CLASSIFIED`
- Evidence Readiness: `BLOCKED_UNCLASSIFIED_SEMANTICS`
- Begründung: Keine automatische semantische Regel fuer diese RQ-Familie registriert.
- Beobachtete Conditions: `instrumentation_gap_audit`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: gateway_resources_boundary_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.01754949998576194` s

## 4. Deterministische Formeln

Die im Bericht verwendeten deskriptiven Groessen sind:

- Mittelwert: $\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i$
- Populationsstandardabweichung: $\sigma=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i-\bar{x})^2}$
- Absolute Differenz: $\Delta_x=\bar{x}_B-\bar{x}_A$
- Verhältnis: $R_x=\bar{x}_B/\bar{x}_A$ fuer $\bar{x}_A\neq0$
- Inter-Spike-Intervall: $ISI_i=t_{i+1}-t_i$

Diese Formeln sind deskriptiv. Ohne registrierten Inferenztest, unabhaengige Stichprobenannahme und passende Versuchsplanung werden daraus keine Signifikanz- oder Kausalbehauptungen abgeleitet.

## 5. Ergebnisse nach Bedingung

| Condition | n | Seeds | Ticks mean | Spikes mean | Syn. events mean | Aktivierte Neuronen mean | Recurrent events mean | Propagation depth mean |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| instrumentation_gap_audit | 3 | 101,102,103 | — | — | — | — | — | — |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | instrumentation_gap_audit | — | — | — | — | — | — | — |
| 102 | instrumentation_gap_audit | — | — | — | — | — | — | — |
| 103 | instrumentation_gap_audit | — | — | — | — | — | — | — |

## 7. Reproduzierbarkeit und Provenienz

Identische Ausgaben ueber mehrere Seeds dokumentieren reproduzierbare Modelltrajektorien unter diesen Bedingungen. Sie sind nicht automatisch statistisch unabhaengige Replikate. State-Digests sind Integritaets-/Identitaetsmarker und keine metrischen Zustandsabstaende.

Deterministische Statistikdatei: [`analysis/statistics.json`](analysis/statistics.json)

## 8. AI Research Report

- AIRR Status: `generated`
- Wissenschaftliche Evidenz durch KI: `false`
- Human Review: `PENDING`
- AIRR Markdown: [`reports/AIRR-2026-0001.md`](reports/AIRR-2026-0001.md)
- AIRR JSON: [`reports/AIRR-2026-0001.json`](reports/AIRR-2026-0001.json)

### 8.1 KI-Einschaetzung

Die Daten sind beschreibend, keine inferenzielle Analyse vorhanden.

KI-Konfidenz: `0.0` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- Keine wissenschaftliche Evidenz ist mit diesem Experiment verknuepft.
- Die Git-Provenance ist unvollstaendig oder nicht verfuegbar.
- Die Experimente sind rein deskriptiv und enthalten keine inferenziellen Analysen.

### Alternative Erklaerungen

- Die fehlende wissenschaftliche Evidenz kann auf eine unzureichende Experimentaldesign oder -durchfuehrung zurueckzufuehren sein.
- Die Ergebnisse sind nicht ausreichend, um Schlussfolgerungen zu ziehen.
- Die verwendeten Formeln sind theoretisch, aber keine numerischen Daten wurden berechnet oder gemessen.

### Fehlende Nachweise

- Messbare numerische Ergebnisse oder Berechnungen der definierten Formeln.
- Empirische Daten zur skalierenden Beziehung zwischen Gateway-Latenz, Traffic, synaptischen Operationen und Energie.
- Ein direkter Test der Hypothese mit inferenziellen Analysen oder wissenschaftlicher Evidenz.
- Eine vollständige Git-Provenance mit sauberen Commits und verfügbaren Artefakten.

### Empfohlene Folgeexperimente

- Ein Experiment, das direkt die Hypothese 'Gateway-Traffic, Latenz und Energie skalieren innerhalb definierter Limits nachvollziehbar mit der aggregierten Topologie' testet.
- Ein Experiment, das wissenschaftliche Evidenz durch empirische Messungen oder inferenzielle Analysen erzeugt.
- Ein Experiment, das die Ressourcen- und Latenzmessungen unter wachsender Topologie systematisch erfasst und analysiert.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260914090724259778-473a6c1c.json](analysis/AIAR-critical_reviewer-20260914090724259778-473a6c1c.json)
- [analysis/AIAR-scientific_analyst-20260914090701629803-473a6c1c.json](analysis/AIAR-scientific_analyst-20260914090701629803-473a6c1c.json)
- [analysis/AIAR-scientific_writer-20260914090818847676-473a6c1c.json](analysis/AIAR-scientific_writer-20260914090818847676-473a6c1c.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-instrumentation_gap_audit-seed-101.json.gz](DATA/raw/run-0000-instrumentation_gap_audit-seed-101.json.gz)
- [DATA/raw/run-0001-instrumentation_gap_audit-seed-102.json.gz](DATA/raw/run-0001-instrumentation_gap_audit-seed-102.json.gz)
- [DATA/raw/run-0002-instrumentation_gap_audit-seed-103.json.gz](DATA/raw/run-0002-instrumentation_gap_audit-seed-103.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `NOT_APPLICABLE`, semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
