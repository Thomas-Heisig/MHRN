# EXP-BATCH-20260914074039-81: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-EVAL-004`
- Hypothese: `H-EVAL-004-A`
- Protokoll: `active_scaling_v1`
- Durchlaeufe: `15`
- Seeds: `[20001, 20002, 20003]`
- Angeforderte Ticks: `1000`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `32 .. 32` ausgeführte Ticks
- Tick-Vertrag: `VIOLATED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `NOT_AUTOMATICALLY_CLASSIFIED`
- Evidence Readiness: `BLOCKED_UNCLASSIFIED_SEMANTICS`
- Begründung: Keine automatische semantische Regel fuer diese RQ-Familie registriert.
- Beobachtete Conditions: `n100000, n1024, n128, n25000, n5000`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: active_scaling_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `57.51314120000461` s

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
| n100000 | 3 | 20001,20002,20003 | 32 | 1556.67 | — | — | — | — |
| n1024 | 3 | 20001,20002,20003 | 32 | 1035.33 | — | — | — | — |
| n128 | 3 | 20001,20002,20003 | 32 | 329.667 | — | — | — | — |
| n25000 | 3 | 20001,20002,20003 | 32 | 1504.67 | — | — | — | — |
| n5000 | 3 | 20001,20002,20003 | 32 | 1376 | — | — | — | — |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 20001 | n128 | 32 | 312 | — | — | — | — | — |
| 20001 | n1024 | 32 | 1065 | — | — | — | — | — |
| 20001 | n5000 | 32 | 1364 | — | — | — | — | — |
| 20001 | n25000 | 32 | 1475 | — | — | — | — | — |
| 20001 | n100000 | 32 | 1551 | — | — | — | — | — |
| 20002 | n128 | 32 | 334 | — | — | — | — | — |
| 20002 | n1024 | 32 | 1166 | — | — | — | — | — |
| 20002 | n5000 | 32 | 1505 | — | — | — | — | — |
| 20002 | n25000 | 32 | 1557 | — | — | — | — | — |
| 20002 | n100000 | 32 | 1560 | — | — | — | — | — |
| 20003 | n128 | 32 | 343 | — | — | — | — | — |
| 20003 | n1024 | 32 | 875 | — | — | — | — | — |
| 20003 | n5000 | 32 | 1259 | — | — | — | — | — |
| 20003 | n25000 | 32 | 1482 | — | — | — | — | — |
| 20003 | n100000 | 32 | 1559 | — | — | — | — | — |

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

Die Rolle scientific_writer konnte nicht ausgeführt werden. Es liegt keine schema-konforme Modellanalyse vor.

KI-Konfidenz: `0.0` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- AI analysis unavailable; deterministic experiment artifacts remain the authoritative data basis.
- Technical reason: ValueError: Invalid AI analysis output field: assessment

### Alternative Erklaerungen

- Keine expliziten Angaben.

### Fehlende Nachweise

- Run the role again with a schema-conforming backend response.
- Complete mandatory human review before interpreting this report.

### Empfohlene Folgeexperimente

- Keine expliziten Folgeexperimente im AIRR angegeben.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260914085721215296-f746f651.json](analysis/AIAR-critical_reviewer-20260914085721215296-f746f651.json)
- [analysis/AIAR-scientific_analyst-20260914085630190698-f746f651.json](analysis/AIAR-scientific_analyst-20260914085630190698-f746f651.json)
- [analysis/AIAR-scientific_writer-20260914085806360566-f746f651.json](analysis/AIAR-scientific_writer-20260914085806360566-f746f651.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-n128-seed-20001.json.gz](DATA/raw/run-0000-n128-seed-20001.json.gz)
- [DATA/raw/run-0001-n1024-seed-20001.json.gz](DATA/raw/run-0001-n1024-seed-20001.json.gz)
- [DATA/raw/run-0002-n5000-seed-20001.json.gz](DATA/raw/run-0002-n5000-seed-20001.json.gz)
- [DATA/raw/run-0003-n25000-seed-20001.json.gz](DATA/raw/run-0003-n25000-seed-20001.json.gz)
- [DATA/raw/run-0004-n100000-seed-20001.json.gz](DATA/raw/run-0004-n100000-seed-20001.json.gz)
- [DATA/raw/run-0005-n128-seed-20002.json.gz](DATA/raw/run-0005-n128-seed-20002.json.gz)
- [DATA/raw/run-0006-n1024-seed-20002.json.gz](DATA/raw/run-0006-n1024-seed-20002.json.gz)
- [DATA/raw/run-0007-n5000-seed-20002.json.gz](DATA/raw/run-0007-n5000-seed-20002.json.gz)
- [DATA/raw/run-0008-n25000-seed-20002.json.gz](DATA/raw/run-0008-n25000-seed-20002.json.gz)
- [DATA/raw/run-0009-n100000-seed-20002.json.gz](DATA/raw/run-0009-n100000-seed-20002.json.gz)
- [DATA/raw/run-0010-n128-seed-20003.json.gz](DATA/raw/run-0010-n128-seed-20003.json.gz)
- [DATA/raw/run-0011-n1024-seed-20003.json.gz](DATA/raw/run-0011-n1024-seed-20003.json.gz)
- [DATA/raw/run-0012-n5000-seed-20003.json.gz](DATA/raw/run-0012-n5000-seed-20003.json.gz)
- [DATA/raw/run-0013-n25000-seed-20003.json.gz](DATA/raw/run-0013-n25000-seed-20003.json.gz)
- [DATA/raw/run-0014-n100000-seed-20003.json.gz](DATA/raw/run-0014-n100000-seed-20003.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `VIOLATED`, semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
