# EXP-BATCH-20260914074039-77: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `failed`
- Forschungsfrage: `RQ-TIME-002`
- Hypothese: `H-TIME-002-A`
- Protokoll: `embodied_timing_v1`
- Durchlaeufe: `21`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `1000`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `600 .. 600` ausgeführte Ticks
- Tick-Vertrag: `VIOLATED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `MISMATCH`
- Evidence Readiness: `BLOCKED_SEMANTIC_MISMATCH`
- Begründung: TIME erwartet numerische Tick-Leiter-Bedingungen.
- Beobachtete Conditions: `batch_1, batch_128, batch_16, physics_15ms, physics_5ms, sensor_15ms, sensor_5ms`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: embodied_timing_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.306832599977497` s

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
| batch_1 | 3 | 101,102,103 | 600 | 39 | — | — | — | — |
| batch_128 | 3 | 101,102,103 | 600 | 39 | — | — | — | — |
| batch_16 | 3 | 101,102,103 | 600 | 39 | — | — | — | — |
| physics_15ms | 3 | 101,102,103 | 600 | 38 | — | — | — | — |
| physics_5ms | 3 | 101,102,103 | 600 | 38 | — | — | — | — |
| sensor_15ms | 3 | 101,102,103 | 600 | 40 | — | — | — | — |
| sensor_5ms | 3 | 101,102,103 | 600 | 38 | — | — | — | — |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | batch_1 | 600 | 39 | — | — | — | — | — |
| 101 | batch_16 | 600 | 39 | — | — | — | — | — |
| 101 | batch_128 | 600 | 39 | — | — | — | — | — |
| 101 | physics_5ms | 600 | 36 | — | — | — | — | — |
| 101 | physics_15ms | 600 | 36 | — | — | — | — | — |
| 101 | sensor_5ms | 600 | 39 | — | — | — | — | — |
| 101 | sensor_15ms | 600 | 39 | — | — | — | — | — |
| 102 | batch_1 | 600 | 39 | — | — | — | — | — |
| 102 | batch_16 | 600 | 39 | — | — | — | — | — |
| 102 | batch_128 | 600 | 39 | — | — | — | — | — |
| 102 | physics_5ms | 600 | 39 | — | — | — | — | — |
| 102 | physics_15ms | 600 | 39 | — | — | — | — | — |
| 102 | sensor_5ms | 600 | 36 | — | — | — | — | — |
| 102 | sensor_15ms | 600 | 42 | — | — | — | — | — |
| 103 | batch_1 | 600 | 39 | — | — | — | — | — |
| 103 | batch_16 | 600 | 39 | — | — | — | — | — |
| 103 | batch_128 | 600 | 39 | — | — | — | — | — |
| 103 | physics_5ms | 600 | 39 | — | — | — | — | — |
| 103 | physics_15ms | 600 | 39 | — | — | — | — | — |
| 103 | sensor_5ms | 600 | 39 | — | — | — | — | — |
| 103 | sensor_15ms | 600 | 39 | — | — | — | — | — |

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
- [analysis/AIAR-critical_reviewer-20260914085240220864-912aeaca.json](analysis/AIAR-critical_reviewer-20260914085240220864-912aeaca.json)
- [analysis/AIAR-scientific_analyst-20260914085232800218-912aeaca.json](analysis/AIAR-scientific_analyst-20260914085232800218-912aeaca.json)
- [analysis/AIAR-scientific_writer-20260914085247618173-912aeaca.json](analysis/AIAR-scientific_writer-20260914085247618173-912aeaca.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/gateway_state.json](DATA/gateway_state.json)
- [DATA/raw/run-0000-batch_1-seed-101.json.gz](DATA/raw/run-0000-batch_1-seed-101.json.gz)
- [DATA/raw/run-0001-batch_16-seed-101.json.gz](DATA/raw/run-0001-batch_16-seed-101.json.gz)
- [DATA/raw/run-0002-batch_128-seed-101.json.gz](DATA/raw/run-0002-batch_128-seed-101.json.gz)
- [DATA/raw/run-0003-physics_5ms-seed-101.json.gz](DATA/raw/run-0003-physics_5ms-seed-101.json.gz)
- [DATA/raw/run-0004-physics_15ms-seed-101.json.gz](DATA/raw/run-0004-physics_15ms-seed-101.json.gz)
- [DATA/raw/run-0005-sensor_5ms-seed-101.json.gz](DATA/raw/run-0005-sensor_5ms-seed-101.json.gz)
- [DATA/raw/run-0006-sensor_15ms-seed-101.json.gz](DATA/raw/run-0006-sensor_15ms-seed-101.json.gz)
- [DATA/raw/run-0007-batch_1-seed-102.json.gz](DATA/raw/run-0007-batch_1-seed-102.json.gz)
- [DATA/raw/run-0008-batch_16-seed-102.json.gz](DATA/raw/run-0008-batch_16-seed-102.json.gz)
- [DATA/raw/run-0009-batch_128-seed-102.json.gz](DATA/raw/run-0009-batch_128-seed-102.json.gz)
- [DATA/raw/run-0010-physics_5ms-seed-102.json.gz](DATA/raw/run-0010-physics_5ms-seed-102.json.gz)
- [DATA/raw/run-0011-physics_15ms-seed-102.json.gz](DATA/raw/run-0011-physics_15ms-seed-102.json.gz)
- [DATA/raw/run-0012-sensor_5ms-seed-102.json.gz](DATA/raw/run-0012-sensor_5ms-seed-102.json.gz)
- [DATA/raw/run-0013-sensor_15ms-seed-102.json.gz](DATA/raw/run-0013-sensor_15ms-seed-102.json.gz)
- [DATA/raw/run-0014-batch_1-seed-103.json.gz](DATA/raw/run-0014-batch_1-seed-103.json.gz)
- [DATA/raw/run-0015-batch_16-seed-103.json.gz](DATA/raw/run-0015-batch_16-seed-103.json.gz)
- [DATA/raw/run-0016-batch_128-seed-103.json.gz](DATA/raw/run-0016-batch_128-seed-103.json.gz)
- [DATA/raw/run-0017-physics_5ms-seed-103.json.gz](DATA/raw/run-0017-physics_5ms-seed-103.json.gz)
- [DATA/raw/run-0018-physics_15ms-seed-103.json.gz](DATA/raw/run-0018-physics_15ms-seed-103.json.gz)
- [DATA/raw/run-0019-sensor_5ms-seed-103.json.gz](DATA/raw/run-0019-sensor_5ms-seed-103.json.gz)
- [DATA/raw/run-0020-sensor_15ms-seed-103.json.gz](DATA/raw/run-0020-sensor_15ms-seed-103.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `failed`, Tick-Vertrag `VIOLATED`, semantische Zuordnung `MISMATCH`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
