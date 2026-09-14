# EXP-BATCH-20260914074039-21: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-STORAGE-003`
- Hypothese: `H-STOR-003-A`
- Protokoll: `storage_density_boundary_v1`
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

- Titel: Experiment workflow: storage_density_boundary_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.012370599957648665` s

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

Die vorliegenden Daten zeigen keine direkten kausalen Messungen oder statistischen Tests zur Bestätigung der Hypothese. Die Experimente sind auf die Überprüfung der Vertragsbedingungen für die Speicherdichte beschränkt, ohne eine klare kausale Beziehung oder signifikante Ergebnisse zu ermitteln.

KI-Konfidenz: `0.0` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- Fehlende direkte kausale Messung
- Keine statistische Signifikanz getestet
- Keine wissenschaftliche Evidenz verknüpft

### Alternative Erklaerungen

- Die Speicherdichte könnte auf andere Weise beeinflusst werden, die nicht in den Experimenten berücksichtigt wurden.
- Die Vertragsbedingungen könnten die Ergebnisse beeinflussen, ohne die tatsächliche Speicherdichte zu messen.

### Fehlende Nachweise

- Messungen der Speicherdichte unter kontrollierten Bedingungen.
- Statistische Analysen der Skal, der Speicherdichte.
- Verknüpfung der Experimente mit wissenschaftlichen Evidenzen oder Literaturquellen.

### Empfohlene Folgeexperimente

- Ein Experiment zur direkten Messung der Speicherdichte unter verschiedenen Neuronenzahlen.
- Ein statistischer Test zur Bestimmung der Skalierung der Speicherdichte.
- Ein Vergleich der Speicherdichte mit anderen Speicherformaten unter gleichen Bedingungen.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260914081541011408-1ee18713.json](analysis/AIAR-critical_reviewer-20260914081541011408-1ee18713.json)
- [analysis/AIAR-scientific_analyst-20260914081503460233-1ee18713.json](analysis/AIAR-scientific_analyst-20260914081503460233-1ee18713.json)
- [analysis/AIAR-scientific_writer-20260914081555379031-1ee18713.json](analysis/AIAR-scientific_writer-20260914081555379031-1ee18713.json)
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
