# EXP-BATCH-20260914074039-75: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `failed`
- Forschungsfrage: `RQ-CONN-002`
- Hypothese: `H-CONN-002-A`
- Protokoll: `connectome_topology_screen_v1`
- Durchlaeufe: `12`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `1000`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `600 .. 600` ausgeführte Ticks
- Tick-Vertrag: `VIOLATED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `NOT_AUTOMATICALLY_CLASSIFIED`
- Evidence Readiness: `BLOCKED_UNCLASSIFIED_SEMANTICS`
- Begründung: Keine automatische semantische Regel fuer diese RQ-Familie registriert.
- Beobachtete Conditions: `degree_preserving, random_edges, structured, weight_shuffle`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: connectome_topology_screen_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.23628370004007593` s

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
| degree_preserving | 3 | 101,102,103 | 600 | 94 | — | — | — | — |
| random_edges | 3 | 101,102,103 | 600 | 102.333 | — | — | — | — |
| structured | 3 | 101,102,103 | 600 | 39 | — | — | — | — |
| weight_shuffle | 3 | 101,102,103 | 600 | 41.3333 | — | — | — | — |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | structured | 600 | 39 | — | — | — | — | — |
| 101 | degree_preserving | 600 | 109 | — | — | — | — | — |
| 101 | weight_shuffle | 600 | 63 | — | — | — | — | — |
| 101 | random_edges | 600 | 85 | — | — | — | — | — |
| 102 | structured | 600 | 39 | — | — | — | — | — |
| 102 | degree_preserving | 600 | 24 | — | — | — | — | — |
| 102 | weight_shuffle | 600 | 33 | — | — | — | — | — |
| 102 | random_edges | 600 | 183 | — | — | — | — | — |
| 103 | structured | 600 | 39 | — | — | — | — | — |
| 103 | degree_preserving | 600 | 149 | — | — | — | — | — |
| 103 | weight_shuffle | 600 | 28 | — | — | — | — | — |
| 103 | random_edges | 600 | 39 | — | — | — | — | — |

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
- [analysis/AIAR-critical_reviewer-20260914085105382628-38478c2a.json](analysis/AIAR-critical_reviewer-20260914085105382628-38478c2a.json)
- [analysis/AIAR-scientific_analyst-20260914085057091712-38478c2a.json](analysis/AIAR-scientific_analyst-20260914085057091712-38478c2a.json)
- [analysis/AIAR-scientific_writer-20260914085113541413-38478c2a.json](analysis/AIAR-scientific_writer-20260914085113541413-38478c2a.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/gateway_state.json](DATA/gateway_state.json)
- [DATA/raw/run-0000-structured-seed-101.json.gz](DATA/raw/run-0000-structured-seed-101.json.gz)
- [DATA/raw/run-0001-degree_preserving-seed-101.json.gz](DATA/raw/run-0001-degree_preserving-seed-101.json.gz)
- [DATA/raw/run-0002-weight_shuffle-seed-101.json.gz](DATA/raw/run-0002-weight_shuffle-seed-101.json.gz)
- [DATA/raw/run-0003-random_edges-seed-101.json.gz](DATA/raw/run-0003-random_edges-seed-101.json.gz)
- [DATA/raw/run-0004-structured-seed-102.json.gz](DATA/raw/run-0004-structured-seed-102.json.gz)
- [DATA/raw/run-0005-degree_preserving-seed-102.json.gz](DATA/raw/run-0005-degree_preserving-seed-102.json.gz)
- [DATA/raw/run-0006-weight_shuffle-seed-102.json.gz](DATA/raw/run-0006-weight_shuffle-seed-102.json.gz)
- [DATA/raw/run-0007-random_edges-seed-102.json.gz](DATA/raw/run-0007-random_edges-seed-102.json.gz)
- [DATA/raw/run-0008-structured-seed-103.json.gz](DATA/raw/run-0008-structured-seed-103.json.gz)
- [DATA/raw/run-0009-degree_preserving-seed-103.json.gz](DATA/raw/run-0009-degree_preserving-seed-103.json.gz)
- [DATA/raw/run-0010-weight_shuffle-seed-103.json.gz](DATA/raw/run-0010-weight_shuffle-seed-103.json.gz)
- [DATA/raw/run-0011-random_edges-seed-103.json.gz](DATA/raw/run-0011-random_edges-seed-103.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `failed`, Tick-Vertrag `VIOLATED`, semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
