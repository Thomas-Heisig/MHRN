# EXP-BATCH-20260914074039-04: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-SNN-003`
- Hypothese: `H-SNN-003-B`
- Protokoll: `topology_propagation_v1`
- Durchlaeufe: `18`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `256`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `256 .. 256` ausgeführte Ticks
- Tick-Vertrag: `SATISFIED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `NOT_AUTOMATICALLY_CLASSIFIED`
- Evidence Readiness: `BLOCKED_UNCLASSIFIED_SEMANTICS`
- Begründung: Keine automatische semantische Regel fuer diese RQ-Familie registriert.
- Beobachtete Conditions: `1d, 2d, 3d, 5d, 5d_shuffled, random_graph`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: topology_propagation_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.13028939999639988` s

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
| 1d | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| 2d | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| 3d | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| 5d | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| 5d_shuffled | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| random_graph | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |

### 5.2 Inter-Spike-Intervalle

- `1d`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `2d`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `3d`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `5d`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `5d_shuffled`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `random_graph`: n=6, mean=1, median=1, min=1, max=1 Ticks.

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | 1d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | 2d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | 3d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | 5d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | 5d_shuffled | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | random_graph | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 1d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 2d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 3d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 5d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 5d_shuffled | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | random_graph | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 1d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 2d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 3d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 5d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 5d_shuffled | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | random_graph | 256 | 3 | 2 | 3 | 0 | 1 | — |

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
- [analysis/AIAR-critical_reviewer-20260914074347553228-a6af81e4.json](analysis/AIAR-critical_reviewer-20260914074347553228-a6af81e4.json)
- [analysis/AIAR-scientific_analyst-20260914074341540840-a6af81e4.json](analysis/AIAR-scientific_analyst-20260914074341540840-a6af81e4.json)
- [analysis/AIAR-scientific_writer-20260914074353546221-a6af81e4.json](analysis/AIAR-scientific_writer-20260914074353546221-a6af81e4.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-1d-seed-101.json.gz](DATA/raw/run-0000-1d-seed-101.json.gz)
- [DATA/raw/run-0001-2d-seed-101.json.gz](DATA/raw/run-0001-2d-seed-101.json.gz)
- [DATA/raw/run-0002-3d-seed-101.json.gz](DATA/raw/run-0002-3d-seed-101.json.gz)
- [DATA/raw/run-0003-5d-seed-101.json.gz](DATA/raw/run-0003-5d-seed-101.json.gz)
- [DATA/raw/run-0004-5d_shuffled-seed-101.json.gz](DATA/raw/run-0004-5d_shuffled-seed-101.json.gz)
- [DATA/raw/run-0005-random_graph-seed-101.json.gz](DATA/raw/run-0005-random_graph-seed-101.json.gz)
- [DATA/raw/run-0006-1d-seed-102.json.gz](DATA/raw/run-0006-1d-seed-102.json.gz)
- [DATA/raw/run-0007-2d-seed-102.json.gz](DATA/raw/run-0007-2d-seed-102.json.gz)
- [DATA/raw/run-0008-3d-seed-102.json.gz](DATA/raw/run-0008-3d-seed-102.json.gz)
- [DATA/raw/run-0009-5d-seed-102.json.gz](DATA/raw/run-0009-5d-seed-102.json.gz)
- [DATA/raw/run-0010-5d_shuffled-seed-102.json.gz](DATA/raw/run-0010-5d_shuffled-seed-102.json.gz)
- [DATA/raw/run-0011-random_graph-seed-102.json.gz](DATA/raw/run-0011-random_graph-seed-102.json.gz)
- [DATA/raw/run-0012-1d-seed-103.json.gz](DATA/raw/run-0012-1d-seed-103.json.gz)
- [DATA/raw/run-0013-2d-seed-103.json.gz](DATA/raw/run-0013-2d-seed-103.json.gz)
- [DATA/raw/run-0014-3d-seed-103.json.gz](DATA/raw/run-0014-3d-seed-103.json.gz)
- [DATA/raw/run-0015-5d-seed-103.json.gz](DATA/raw/run-0015-5d-seed-103.json.gz)
- [DATA/raw/run-0016-5d_shuffled-seed-103.json.gz](DATA/raw/run-0016-5d_shuffled-seed-103.json.gz)
- [DATA/raw/run-0017-random_graph-seed-103.json.gz](DATA/raw/run-0017-random_graph-seed-103.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `SATISFIED`, semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
