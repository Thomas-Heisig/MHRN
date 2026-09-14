# EXP-BATCH-20260914074039-07: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-PING-001`
- Hypothese: `H-PING-001-A`
- Protokoll: `network_impulse_reproducibility_v1`
- Durchlaeufe: `12`
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
- Begründung: PING erwartet recurrence_off und recurrence_on.
- Beobachtete Conditions: `recurrence_off_replica_a, recurrence_off_replica_b, recurrence_on_replica_a, recurrence_on_replica_b`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: network_impulse_reproducibility_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.10253620002185926` s

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
| recurrence_off_replica_a | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| recurrence_off_replica_b | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| recurrence_on_replica_a | 3 | 101,102,103 | 256 | 33 | 33 | 3 | 10 | 61 |
| recurrence_on_replica_b | 3 | 101,102,103 | 256 | 33 | 33 | 3 | 10 | 61 |

### 5.2 Inter-Spike-Intervalle

- `recurrence_off_replica_a`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `recurrence_off_replica_b`: n=6, mean=1, median=1, min=1, max=1 Ticks.
- `recurrence_on_replica_a`: n=96, mean=1.9375, median=2, min=1, max=4 Ticks.
- `recurrence_on_replica_b`: n=96, mean=1.9375, median=2, min=1, max=4 Ticks.

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | recurrence_off_replica_a | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | recurrence_off_replica_b | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 101 | recurrence_on_replica_a | 256 | 33 | 33 | 3 | 10 | 61 | — |
| 101 | recurrence_on_replica_b | 256 | 33 | 33 | 3 | 10 | 61 | — |
| 102 | recurrence_off_replica_a | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | recurrence_off_replica_b | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 102 | recurrence_on_replica_a | 256 | 33 | 33 | 3 | 10 | 61 | — |
| 102 | recurrence_on_replica_b | 256 | 33 | 33 | 3 | 10 | 61 | — |
| 103 | recurrence_off_replica_a | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | recurrence_off_replica_b | 256 | 3 | 2 | 3 | 0 | 1 | — |
| 103 | recurrence_on_replica_a | 256 | 33 | 33 | 3 | 10 | 61 | — |
| 103 | recurrence_on_replica_b | 256 | 33 | 33 | 3 | 10 | 61 | — |

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
- [analysis/AIAR-critical_reviewer-20260914075128768152-f87eb7b4.json](analysis/AIAR-critical_reviewer-20260914075128768152-f87eb7b4.json)
- [analysis/AIAR-scientific_analyst-20260914075118966005-f87eb7b4.json](analysis/AIAR-scientific_analyst-20260914075118966005-f87eb7b4.json)
- [analysis/AIAR-scientific_writer-20260914075146515421-f87eb7b4.json](analysis/AIAR-scientific_writer-20260914075146515421-f87eb7b4.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-recurrence_off_replica_a-seed-101.json.gz](DATA/raw/run-0000-recurrence_off_replica_a-seed-101.json.gz)
- [DATA/raw/run-0001-recurrence_off_replica_b-seed-101.json.gz](DATA/raw/run-0001-recurrence_off_replica_b-seed-101.json.gz)
- [DATA/raw/run-0002-recurrence_on_replica_a-seed-101.json.gz](DATA/raw/run-0002-recurrence_on_replica_a-seed-101.json.gz)
- [DATA/raw/run-0003-recurrence_on_replica_b-seed-101.json.gz](DATA/raw/run-0003-recurrence_on_replica_b-seed-101.json.gz)
- [DATA/raw/run-0004-recurrence_off_replica_a-seed-102.json.gz](DATA/raw/run-0004-recurrence_off_replica_a-seed-102.json.gz)
- [DATA/raw/run-0005-recurrence_off_replica_b-seed-102.json.gz](DATA/raw/run-0005-recurrence_off_replica_b-seed-102.json.gz)
- [DATA/raw/run-0006-recurrence_on_replica_a-seed-102.json.gz](DATA/raw/run-0006-recurrence_on_replica_a-seed-102.json.gz)
- [DATA/raw/run-0007-recurrence_on_replica_b-seed-102.json.gz](DATA/raw/run-0007-recurrence_on_replica_b-seed-102.json.gz)
- [DATA/raw/run-0008-recurrence_off_replica_a-seed-103.json.gz](DATA/raw/run-0008-recurrence_off_replica_a-seed-103.json.gz)
- [DATA/raw/run-0009-recurrence_off_replica_b-seed-103.json.gz](DATA/raw/run-0009-recurrence_off_replica_b-seed-103.json.gz)
- [DATA/raw/run-0010-recurrence_on_replica_a-seed-103.json.gz](DATA/raw/run-0010-recurrence_on_replica_a-seed-103.json.gz)
- [DATA/raw/run-0011-recurrence_on_replica_b-seed-103.json.gz](DATA/raw/run-0011-recurrence_on_replica_b-seed-103.json.gz)
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
