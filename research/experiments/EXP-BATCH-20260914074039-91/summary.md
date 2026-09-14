# EXP-BATCH-20260914074039-91: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-MSBA-E02`
- Hypothese: `H-MSBA-E02-A`
- Protokoll: `msba_resource_allocation_v1`
- Durchlaeufe: `9`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `96`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `nicht direkt messbar .. nicht direkt messbar` ausgeführte Ticks
- Tick-Vertrag: `NOT_APPLICABLE`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `CONFIRMATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `NOT_AUTOMATICALLY_CLASSIFIED`
- Evidence Readiness: `BLOCKED_UNCLASSIFIED_SEMANTICS`
- Begründung: Keine automatische semantische Regel fuer diese RQ-Familie registriert.
- Beobachtete Conditions: `adaptive, fixed, random`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: msba_resource_allocation_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.02601839997805655` s

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
| adaptive | 3 | 101,102,103 | — | — | — | — | — | — |
| fixed | 3 | 101,102,103 | — | — | — | — | — | — |
| random | 3 | 101,102,103 | — | — | — | — | — | — |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | adaptive | — | — | — | — | — | — | — |
| 101 | fixed | — | — | — | — | — | — | — |
| 101 | random | — | — | — | — | — | — | — |
| 102 | adaptive | — | — | — | — | — | — | — |
| 102 | fixed | — | — | — | — | — | — | — |
| 102 | random | — | — | — | — | — | — | — |
| 103 | adaptive | — | — | — | — | — | — | — |
| 103 | fixed | — | — | — | — | — | — | — |
| 103 | random | — | — | — | — | — | — | — |

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

Die Daten zeigen keine signifikanten Unterschiede in der Aufgabenleistung zwischen den Bedingungen. Die adaptive Allokation erzielte eine leicht geringere Aufgabenleistung als die fixe Allokation, aber die Unterschiede sind nicht statistisch signifikant. Die zufaellige Allokation zeigte eine Aufgabenleistung, die sich in einem engen Bereich um die fixe Allokation bewegte. Die Ergebnisse sind in der Regel konsistent, aber es fehlen statistische Tests zur Bestimmung der Signifikanz.

KI-Konfidenz: `0.65` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- Die Daten enthalten keine statistischen Tests zur Bestimmung der Signifikanz der beobachteten Unterschiede.
- Die Ergebnisse sind ausgewertet, ohne die Varianz der Messwerte zu beruecksichtigen.
- Die Interpretation der Ergebnisse basiert ausschliesslich auf deskriptiven Statistiken, ohne inferentielle Analysen.
- Die Daten sind ausgewertet, ohne die potenziellen Auswirkungen von Stichprobenfehlern zu beruecksichtigen.

### Alternative Erklaerungen

- Die geringere Aufgabenleistung der adaptive Allokation kann auf andere Faktoren zurueckzufuehren sein, wie z.B. die Allokationsstrategie oder die Ressourcenverteilung.
- Die zufaellige Allokation kann eine geringere Aufgabenleistung aufweisen, da sie nicht optimiert ist, aber dies ist nicht statistisch signifikant.
- Die Unterschiede in der Aufgabenleistung koennen auf Zufaelligkeit oder andere nicht gemessene Faktoren zurueckzufuehren sein.
- Die geringere Aufgabenleistung der adaptive Allokation kann auf die Allokationsstrategie zurueckzufuehren sein, die nicht optimal ist.
- Die zufaellige Allokation kann eine geringere Aufgabenleistung aufweisen, da sie nicht optimiert ist, aber dies ist nicht statistisch signifikant.

### Fehlende Nachweise

- Statistische Tests zur Bestimmung der Signifikanz der beobachteten Unterschiede.
- Daten zur Varianz der Messwerte.
- Inferentielle Analysen zur Untersuchung der Beziehungen zwischen den Bedingungen und der Aufgabenleistung.
- Daten zur Auswirkung von Stichprobenfehlern auf die Ergebnisse.
- Daten zu den Allokationsstrategien und deren Auswirkungen auf die Aufgabenleistung.

### Empfohlene Folgeexperimente

- Fuehren Sie statistische Tests durch, um die Signifikanz der beobachteten Unterschiede zu bestimmen.
- Erweitern Sie die Stichprobe, um die Varianz der Messwerte zu beruecksichtigen.
- Fuehren Sie inferentielle Analysen durch, um die Beziehungen zwischen den Bedingungen und der Aufgabenleistung zu untersuchen.
- Testen Sie die Auswirkungen von Stichprobenfehlern auf die Ergebnisse.
- Fuehren Sie Experimente mit unterschiedlichen Allokationsstrategien durch, um die Effekte der verschiedenen Bedingungen zu vergleichen.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260914091126235001-5c701d85.json](analysis/AIAR-critical_reviewer-20260914091126235001-5c701d85.json)
- [analysis/AIAR-scientific_analyst-20260914091039535351-5c701d85.json](analysis/AIAR-scientific_analyst-20260914091039535351-5c701d85.json)
- [analysis/AIAR-scientific_writer-20260914091244617564-5c701d85.json](analysis/AIAR-scientific_writer-20260914091244617564-5c701d85.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/gateway_state.json](DATA/gateway_state.json)
- [DATA/raw/run-0000-adaptive-seed-101.json.gz](DATA/raw/run-0000-adaptive-seed-101.json.gz)
- [DATA/raw/run-0001-fixed-seed-101.json.gz](DATA/raw/run-0001-fixed-seed-101.json.gz)
- [DATA/raw/run-0002-random-seed-101.json.gz](DATA/raw/run-0002-random-seed-101.json.gz)
- [DATA/raw/run-0003-adaptive-seed-102.json.gz](DATA/raw/run-0003-adaptive-seed-102.json.gz)
- [DATA/raw/run-0004-fixed-seed-102.json.gz](DATA/raw/run-0004-fixed-seed-102.json.gz)
- [DATA/raw/run-0005-random-seed-102.json.gz](DATA/raw/run-0005-random-seed-102.json.gz)
- [DATA/raw/run-0006-adaptive-seed-103.json.gz](DATA/raw/run-0006-adaptive-seed-103.json.gz)
- [DATA/raw/run-0007-fixed-seed-103.json.gz](DATA/raw/run-0007-fixed-seed-103.json.gz)
- [DATA/raw/run-0008-random-seed-103.json.gz](DATA/raw/run-0008-random-seed-103.json.gz)
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
