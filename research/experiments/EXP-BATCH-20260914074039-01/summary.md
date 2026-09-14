# EXP-BATCH-20260914074039-01: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-SNN-001`
- Hypothese: `H-SNN-001-A`
- Protokoll: `sustained_activity_stability_v1`
- Durchlaeufe: `20`
- Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51]`
- Angeforderte Ticks: `100000`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `100000 .. 100000` ausgeführte Ticks
- Tick-Vertrag: `SATISFIED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `CONFIRMATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `DIRECT_MATCH`
- Evidence Readiness: `BLOCKED_DIRTY_SOURCE_TREE`
- Begründung: RQ-SNN-001 verwendet das dedizierte Sustained-Activity-Protokoll mit Kontroll- und Tonic-Drive-Bedingung.
- Beobachtete Conditions: `no_input_control, tonic_drive`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: sustained_activity_stability_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `15.515038900019135` s

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
| no_input_control | 10 | 42,43,44,45,46,47,48,49,50,51 | 100000 | — | — | — | — | — |
| tonic_drive | 10 | 42,43,44,45,46,47,48,49,50,51 | 100000 | — | — | — | — | — |

### 5.1 Deskriptive Zwei-Bedingungs-Effekte

- `burn_in_ticks`: $\Delta=0$; $R=1$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `drive_current`: $\Delta=50$; $R=—$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `neuron_v_max`: $\Delta=5$; $R=0.928571$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `neuron_v_min`: $\Delta=-25.5949$; $R=1.36564$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_mean_spikes`: $\Delta=300$; $R=—$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_spike_cv`: $\Delta=0$; $R=—$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_spike_relative_drift`: $\Delta=0$; $R=—$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_window_count`: $\Delta=0$; $R=1$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `ticks_executed`: $\Delta=0$; $R=1$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `ticks_requested`: $\Delta=0$; $R=1$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `weight_max`: $\Delta=0$; $R=1$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `weight_min`: $\Delta=0$; $R=1$; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `window_ticks`: $\Delta=0$; $R=1$; Referenz `no_input_control`, Vergleich `tonic_drive`.

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 42 | no_input_control | 100000 | — | — | — | — | — | — |
| 42 | tonic_drive | 100000 | — | — | — | — | — | — |
| 43 | no_input_control | 100000 | — | — | — | — | — | — |
| 43 | tonic_drive | 100000 | — | — | — | — | — | — |
| 44 | no_input_control | 100000 | — | — | — | — | — | — |
| 44 | tonic_drive | 100000 | — | — | — | — | — | — |
| 45 | no_input_control | 100000 | — | — | — | — | — | — |
| 45 | tonic_drive | 100000 | — | — | — | — | — | — |
| 46 | no_input_control | 100000 | — | — | — | — | — | — |
| 46 | tonic_drive | 100000 | — | — | — | — | — | — |
| 47 | no_input_control | 100000 | — | — | — | — | — | — |
| 47 | tonic_drive | 100000 | — | — | — | — | — | — |
| 48 | no_input_control | 100000 | — | — | — | — | — | — |
| 48 | tonic_drive | 100000 | — | — | — | — | — | — |
| 49 | no_input_control | 100000 | — | — | — | — | — | — |
| 49 | tonic_drive | 100000 | — | — | — | — | — | — |
| 50 | no_input_control | 100000 | — | — | — | — | — | — |
| 50 | tonic_drive | 100000 | — | — | — | — | — | — |
| 51 | no_input_control | 100000 | — | — | — | — | — | — |
| 51 | tonic_drive | 100000 | — | — | — | — | — | — |

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
- [analysis/AIAR-critical_reviewer-20260914074121754022-bec796f8.json](analysis/AIAR-critical_reviewer-20260914074121754022-bec796f8.json)
- [analysis/AIAR-scientific_analyst-20260914074121070255-bec796f8.json](analysis/AIAR-scientific_analyst-20260914074121070255-bec796f8.json)
- [analysis/AIAR-scientific_writer-20260914074122470759-bec796f8.json](analysis/AIAR-scientific_writer-20260914074122470759-bec796f8.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-no_input_control-seed-42.json.gz](DATA/raw/run-0000-no_input_control-seed-42.json.gz)
- [DATA/raw/run-0001-tonic_drive-seed-42.json.gz](DATA/raw/run-0001-tonic_drive-seed-42.json.gz)
- [DATA/raw/run-0002-no_input_control-seed-43.json.gz](DATA/raw/run-0002-no_input_control-seed-43.json.gz)
- [DATA/raw/run-0003-tonic_drive-seed-43.json.gz](DATA/raw/run-0003-tonic_drive-seed-43.json.gz)
- [DATA/raw/run-0004-no_input_control-seed-44.json.gz](DATA/raw/run-0004-no_input_control-seed-44.json.gz)
- [DATA/raw/run-0005-tonic_drive-seed-44.json.gz](DATA/raw/run-0005-tonic_drive-seed-44.json.gz)
- [DATA/raw/run-0006-no_input_control-seed-45.json.gz](DATA/raw/run-0006-no_input_control-seed-45.json.gz)
- [DATA/raw/run-0007-tonic_drive-seed-45.json.gz](DATA/raw/run-0007-tonic_drive-seed-45.json.gz)
- [DATA/raw/run-0008-no_input_control-seed-46.json.gz](DATA/raw/run-0008-no_input_control-seed-46.json.gz)
- [DATA/raw/run-0009-tonic_drive-seed-46.json.gz](DATA/raw/run-0009-tonic_drive-seed-46.json.gz)
- [DATA/raw/run-0010-no_input_control-seed-47.json.gz](DATA/raw/run-0010-no_input_control-seed-47.json.gz)
- [DATA/raw/run-0011-tonic_drive-seed-47.json.gz](DATA/raw/run-0011-tonic_drive-seed-47.json.gz)
- [DATA/raw/run-0012-no_input_control-seed-48.json.gz](DATA/raw/run-0012-no_input_control-seed-48.json.gz)
- [DATA/raw/run-0013-tonic_drive-seed-48.json.gz](DATA/raw/run-0013-tonic_drive-seed-48.json.gz)
- [DATA/raw/run-0014-no_input_control-seed-49.json.gz](DATA/raw/run-0014-no_input_control-seed-49.json.gz)
- [DATA/raw/run-0015-tonic_drive-seed-49.json.gz](DATA/raw/run-0015-tonic_drive-seed-49.json.gz)
- [DATA/raw/run-0016-no_input_control-seed-50.json.gz](DATA/raw/run-0016-no_input_control-seed-50.json.gz)
- [DATA/raw/run-0017-tonic_drive-seed-50.json.gz](DATA/raw/run-0017-tonic_drive-seed-50.json.gz)
- [DATA/raw/run-0018-no_input_control-seed-51.json.gz](DATA/raw/run-0018-no_input_control-seed-51.json.gz)
- [DATA/raw/run-0019-tonic_drive-seed-51.json.gz](DATA/raw/run-0019-tonic_drive-seed-51.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `SATISFIED`, semantische Zuordnung `DIRECT_MATCH`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
