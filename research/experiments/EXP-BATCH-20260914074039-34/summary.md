# EXP-BATCH-20260914074039-34: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-SUITE-001`
- Hypothese: `H-SUITE-001-A`
- Protokoll: `science_suite_registered_v1`
- Durchlaeufe: `54`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `256`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `256 .. 256` ausgeführte Ticks
- Tick-Vertrag: `SATISFIED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `MISMATCH`
- Evidence Readiness: `BLOCKED_SEMANTIC_MISMATCH`
- Begründung: SUITE erwartet science_all_v1 und PING, TEMP, STDP, Learning, TIME, 5D sowie Regulation unter gemeinsamer Provenienz.
- Beobachtete Conditions: `5d:1d, 5d:2d, 5d:3d, 5d:5d, 5d:5d_shuffled, 5d:random_graph, learning:learning_off, learning:learning_on, learning:sham_replay, ping:recurrence_off, ping:recurrence_on, regulation:chronic_pressure, regulation:nominal, regulation:telemetry_unknown, stdp:productive_reward_stdp, temporal:fast_medium_slow, time:100, time:256`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: science_suite_registered_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.5183241000049748` s

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
| 5d:1d | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| 5d:2d | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| 5d:3d | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| 5d:5d | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| 5d:5d_shuffled | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| 5d:random_graph | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| learning:learning_off | 3 | 101,102,103 | — | — | — | — | — | — |
| learning:learning_on | 3 | 101,102,103 | — | — | — | — | — | — |
| learning:sham_replay | 3 | 101,102,103 | — | — | — | — | — | — |
| ping:recurrence_off | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| ping:recurrence_on | 3 | 101,102,103 | 256 | 33 | 33 | 3 | 10 | 61 |
| regulation:chronic_pressure | 3 | 101,102,103 | — | — | — | — | — | — |
| regulation:nominal | 3 | 101,102,103 | — | — | — | — | — | — |
| regulation:telemetry_unknown | 3 | 101,102,103 | — | — | — | — | — | — |
| stdp:productive_reward_stdp | 3 | 101,102,103 | — | — | — | — | — | — |
| temporal:fast_medium_slow | 3 | 101,102,103 | 256 | 0 | — | — | — | — |
| time:100 | 3 | 101,102,103 | — | — | — | — | — | — |
| time:256 | 3 | 101,102,103 | — | — | — | — | — | — |

### 5.2 Inter-Spike-Intervalle

- `5d:1d`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `5d:2d`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `5d:3d`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `5d:5d`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `5d:5d_shuffled`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `5d:random_graph`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `ping:recurrence_off`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `ping:recurrence_on`: n=96, mean=1.9375, median=2, min=1, max=4 Ticks.

### 5.3 Temporal-State-Horizonte

- `fast`: Referenzvergleiche=762; discrepancy mean=0.0103327, max=0.952011; nonzero=762 (1); mean(nonzero)=0.0103327.
- `medium`: Referenzvergleiche=756; discrepancy mean=0.0150033, max=1.15894; nonzero=756 (1); mean(nonzero)=0.0150033.
- `slow`: Referenzvergleiche=750; discrepancy mean=0.0184276, max=1.17842; nonzero=750 (1); mean(nonzero)=0.0184276.

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | ping:recurrence_off | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | ping:recurrence_on | 256 | 33 | 33 | 3 | 10 | 61 | — |
| 102 | ping:recurrence_off | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | ping:recurrence_on | 256 | 33 | 33 | 3 | 10 | 61 | — |
| 103 | ping:recurrence_off | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | ping:recurrence_on | 256 | 33 | 33 | 3 | 10 | 61 | — |
| 101 | temporal:fast_medium_slow | 256 | 0 | — | — | — | — | — |
| 102 | temporal:fast_medium_slow | 256 | 0 | — | — | — | — | — |
| 103 | temporal:fast_medium_slow | 256 | 0 | — | — | — | — | — |
| 101 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 102 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 103 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 101 | learning:learning_on | — | — | — | — | — | — | — |
| 101 | learning:learning_off | — | — | — | — | — | — | — |
| 101 | learning:sham_replay | — | — | — | — | — | — | — |
| 102 | learning:learning_on | — | — | — | — | — | — | — |
| 102 | learning:learning_off | — | — | — | — | — | — | — |
| 102 | learning:sham_replay | — | — | — | — | — | — | — |
| 103 | learning:learning_on | — | — | — | — | — | — | — |
| 103 | learning:learning_off | — | — | — | — | — | — | — |
| 103 | learning:sham_replay | — | — | — | — | — | — | — |
| 101 | time:100 | 100 | — | — | — | — | — | — |
| 101 | time:256 | 256 | — | — | — | — | — | — |
| 102 | time:100 | 100 | — | — | — | — | — | — |
| 102 | time:256 | 256 | — | — | — | — | — | — |
| 103 | time:100 | 100 | — | — | — | — | — | — |
| 103 | time:256 | 256 | — | — | — | — | — | — |
| 101 | 5d:1d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | 5d:2d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | 5d:3d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | 5d:5d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | 5d:5d_shuffled | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | 5d:random_graph | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 5d:1d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 5d:2d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 5d:3d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 5d:5d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 5d:5d_shuffled | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | 5d:random_graph | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 5d:1d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 5d:2d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 5d:3d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 5d:5d | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 5d:5d_shuffled | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | 5d:random_graph | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | regulation:nominal | — | — | — | — | — | — | — |
| 101 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 101 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 102 | regulation:nominal | — | — | — | — | — | — | — |
| 102 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 102 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 103 | regulation:nominal | — | — | — | — | — | — | — |
| 103 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 103 | regulation:telemetry_unknown | — | — | — | — | — | — | — |

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
- [analysis/AIAR-critical_reviewer-20260914083321793643-dfb718e8.json](analysis/AIAR-critical_reviewer-20260914083321793643-dfb718e8.json)
- [analysis/AIAR-scientific_analyst-20260914083241822696-dfb718e8.json](analysis/AIAR-scientific_analyst-20260914083241822696-dfb718e8.json)
- [analysis/AIAR-scientific_writer-20260914083401721168-dfb718e8.json](analysis/AIAR-scientific_writer-20260914083401721168-dfb718e8.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-ping-recurrence_off-seed-101.json.gz](DATA/raw/run-0000-ping-recurrence_off-seed-101.json.gz)
- [DATA/raw/run-0001-ping-recurrence_on-seed-101.json.gz](DATA/raw/run-0001-ping-recurrence_on-seed-101.json.gz)
- [DATA/raw/run-0002-ping-recurrence_off-seed-102.json.gz](DATA/raw/run-0002-ping-recurrence_off-seed-102.json.gz)
- [DATA/raw/run-0003-ping-recurrence_on-seed-102.json.gz](DATA/raw/run-0003-ping-recurrence_on-seed-102.json.gz)
- [DATA/raw/run-0004-ping-recurrence_off-seed-103.json.gz](DATA/raw/run-0004-ping-recurrence_off-seed-103.json.gz)
- [DATA/raw/run-0005-ping-recurrence_on-seed-103.json.gz](DATA/raw/run-0005-ping-recurrence_on-seed-103.json.gz)
- [DATA/raw/run-0006-temporal-fast_medium_slow-seed-101.json.gz](DATA/raw/run-0006-temporal-fast_medium_slow-seed-101.json.gz)
- [DATA/raw/run-0007-temporal-fast_medium_slow-seed-102.json.gz](DATA/raw/run-0007-temporal-fast_medium_slow-seed-102.json.gz)
- [DATA/raw/run-0008-temporal-fast_medium_slow-seed-103.json.gz](DATA/raw/run-0008-temporal-fast_medium_slow-seed-103.json.gz)
- [DATA/raw/run-0009-stdp-productive_reward_stdp-seed-101.json.gz](DATA/raw/run-0009-stdp-productive_reward_stdp-seed-101.json.gz)
- [DATA/raw/run-0010-stdp-productive_reward_stdp-seed-102.json.gz](DATA/raw/run-0010-stdp-productive_reward_stdp-seed-102.json.gz)
- [DATA/raw/run-0011-stdp-productive_reward_stdp-seed-103.json.gz](DATA/raw/run-0011-stdp-productive_reward_stdp-seed-103.json.gz)
- [DATA/raw/run-0012-learning-learning_on-seed-101.json.gz](DATA/raw/run-0012-learning-learning_on-seed-101.json.gz)
- [DATA/raw/run-0013-learning-learning_off-seed-101.json.gz](DATA/raw/run-0013-learning-learning_off-seed-101.json.gz)
- [DATA/raw/run-0014-learning-sham_replay-seed-101.json.gz](DATA/raw/run-0014-learning-sham_replay-seed-101.json.gz)
- [DATA/raw/run-0015-learning-learning_on-seed-102.json.gz](DATA/raw/run-0015-learning-learning_on-seed-102.json.gz)
- [DATA/raw/run-0016-learning-learning_off-seed-102.json.gz](DATA/raw/run-0016-learning-learning_off-seed-102.json.gz)
- [DATA/raw/run-0017-learning-sham_replay-seed-102.json.gz](DATA/raw/run-0017-learning-sham_replay-seed-102.json.gz)
- [DATA/raw/run-0018-learning-learning_on-seed-103.json.gz](DATA/raw/run-0018-learning-learning_on-seed-103.json.gz)
- [DATA/raw/run-0019-learning-learning_off-seed-103.json.gz](DATA/raw/run-0019-learning-learning_off-seed-103.json.gz)
- [DATA/raw/run-0020-learning-sham_replay-seed-103.json.gz](DATA/raw/run-0020-learning-sham_replay-seed-103.json.gz)
- [DATA/raw/run-0021-time-100-seed-101.json.gz](DATA/raw/run-0021-time-100-seed-101.json.gz)
- [DATA/raw/run-0022-time-256-seed-101.json.gz](DATA/raw/run-0022-time-256-seed-101.json.gz)
- [DATA/raw/run-0023-time-100-seed-102.json.gz](DATA/raw/run-0023-time-100-seed-102.json.gz)
- [DATA/raw/run-0024-time-256-seed-102.json.gz](DATA/raw/run-0024-time-256-seed-102.json.gz)
- [DATA/raw/run-0025-time-100-seed-103.json.gz](DATA/raw/run-0025-time-100-seed-103.json.gz)
- [DATA/raw/run-0026-time-256-seed-103.json.gz](DATA/raw/run-0026-time-256-seed-103.json.gz)
- [DATA/raw/run-0027-5d-1d-seed-101.json.gz](DATA/raw/run-0027-5d-1d-seed-101.json.gz)
- [DATA/raw/run-0028-5d-2d-seed-101.json.gz](DATA/raw/run-0028-5d-2d-seed-101.json.gz)
- [DATA/raw/run-0029-5d-3d-seed-101.json.gz](DATA/raw/run-0029-5d-3d-seed-101.json.gz)
- [DATA/raw/run-0030-5d-5d-seed-101.json.gz](DATA/raw/run-0030-5d-5d-seed-101.json.gz)
- [DATA/raw/run-0031-5d-5d_shuffled-seed-101.json.gz](DATA/raw/run-0031-5d-5d_shuffled-seed-101.json.gz)
- [DATA/raw/run-0032-5d-random_graph-seed-101.json.gz](DATA/raw/run-0032-5d-random_graph-seed-101.json.gz)
- [DATA/raw/run-0033-5d-1d-seed-102.json.gz](DATA/raw/run-0033-5d-1d-seed-102.json.gz)
- [DATA/raw/run-0034-5d-2d-seed-102.json.gz](DATA/raw/run-0034-5d-2d-seed-102.json.gz)
- [DATA/raw/run-0035-5d-3d-seed-102.json.gz](DATA/raw/run-0035-5d-3d-seed-102.json.gz)
- [DATA/raw/run-0036-5d-5d-seed-102.json.gz](DATA/raw/run-0036-5d-5d-seed-102.json.gz)
- [DATA/raw/run-0037-5d-5d_shuffled-seed-102.json.gz](DATA/raw/run-0037-5d-5d_shuffled-seed-102.json.gz)
- [DATA/raw/run-0038-5d-random_graph-seed-102.json.gz](DATA/raw/run-0038-5d-random_graph-seed-102.json.gz)
- [DATA/raw/run-0039-5d-1d-seed-103.json.gz](DATA/raw/run-0039-5d-1d-seed-103.json.gz)
- [DATA/raw/run-0040-5d-2d-seed-103.json.gz](DATA/raw/run-0040-5d-2d-seed-103.json.gz)
- [DATA/raw/run-0041-5d-3d-seed-103.json.gz](DATA/raw/run-0041-5d-3d-seed-103.json.gz)
- [DATA/raw/run-0042-5d-5d-seed-103.json.gz](DATA/raw/run-0042-5d-5d-seed-103.json.gz)
- [DATA/raw/run-0043-5d-5d_shuffled-seed-103.json.gz](DATA/raw/run-0043-5d-5d_shuffled-seed-103.json.gz)
- [DATA/raw/run-0044-5d-random_graph-seed-103.json.gz](DATA/raw/run-0044-5d-random_graph-seed-103.json.gz)
- [DATA/raw/run-0045-regulation-nominal-seed-101.json.gz](DATA/raw/run-0045-regulation-nominal-seed-101.json.gz)
- [DATA/raw/run-0046-regulation-chronic_pressure-seed-101.json.gz](DATA/raw/run-0046-regulation-chronic_pressure-seed-101.json.gz)
- [DATA/raw/run-0047-regulation-telemetry_unknown-seed-101.json.gz](DATA/raw/run-0047-regulation-telemetry_unknown-seed-101.json.gz)
- [DATA/raw/run-0048-regulation-nominal-seed-102.json.gz](DATA/raw/run-0048-regulation-nominal-seed-102.json.gz)
- [DATA/raw/run-0049-regulation-chronic_pressure-seed-102.json.gz](DATA/raw/run-0049-regulation-chronic_pressure-seed-102.json.gz)
- [DATA/raw/run-0050-regulation-telemetry_unknown-seed-102.json.gz](DATA/raw/run-0050-regulation-telemetry_unknown-seed-102.json.gz)
- [DATA/raw/run-0051-regulation-nominal-seed-103.json.gz](DATA/raw/run-0051-regulation-nominal-seed-103.json.gz)
- [DATA/raw/run-0052-regulation-chronic_pressure-seed-103.json.gz](DATA/raw/run-0052-regulation-chronic_pressure-seed-103.json.gz)
- [DATA/raw/run-0053-regulation-telemetry_unknown-seed-103.json.gz](DATA/raw/run-0053-regulation-telemetry_unknown-seed-103.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `SATISFIED`, semantische Zuordnung `MISMATCH`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
