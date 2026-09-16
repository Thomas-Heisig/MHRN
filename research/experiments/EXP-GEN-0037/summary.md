# EXP-GEN-0037: Wissenschaftliche Zusammenfassung

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
- Evidence Readiness: `HUMAN_REVIEW_REQUIRED`
- Begründung: RQ-SNN-001 verwendet das dedizierte Sustained-Activity-Protokoll mit Kontroll- und Tonic-Drive-Bedingung.
- Beobachtete Conditions: `no_input_control, tonic_drive`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: sustained_activity_stability_v1 — RQ-SNN-001
- Bedingungen: no_input_control (negative_control); tonic_drive (stability_treatment)
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `43b35ca28910dc2d62a72f5539050f3833794183`
- Git dirty: `False`
- Runtime: `14.465531099999907` s

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

**Wichtig:** `—` bedeutet in dieser Tabelle ausschließlich, dass die jeweilige SNN-Metrik für diese Bedingung nicht definiert oder nicht erhoben wird. Es bedeutet **nicht**, dass für die Bedingung keine DATA vorliegen. Protokollspezifische Messwerte werden direkt darunter ausgewiesen.

### 5.1 Protokollspezifische Metrikabdeckung

| Condition | zusätzliche numerische Mittelwerte |
| --- | --- |
| no_input_control | `burn_in_ticks=10000`; `drive_current=0`; `neuron_v_max=-70`; `neuron_v_min=-70`; `post_burn_in_mean_spikes=0`; `post_burn_in_spike_cv=0`; `post_burn_in_spike_relative_drift=0`; `post_burn_in_window_count=90`; `ticks_requested=100000`; `weight_max=100`; `weight_min=100`; `window_ticks=1000` |
| tonic_drive | `burn_in_ticks=10000`; `drive_current=50`; `neuron_v_max=-65`; `neuron_v_min=-95.5949`; `post_burn_in_mean_spikes=300`; `post_burn_in_spike_cv=0`; `post_burn_in_spike_relative_drift=0`; `post_burn_in_window_count=90`; `ticks_requested=100000`; `weight_max=100`; `weight_min=100`; `window_ticks=1000` |

### 5.2 Deskriptive Zwei-Bedingungs-Effekte

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

The experiment confirms that Brain-5D can produce stable spike dynamics over extended simulation periods. The results support the hypothesis that the system can maintain consistent neural activity without numerical drift, which is essential for further learning and self-organization experiments.

KI-Konfidenz: `0.0` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- No registered scientific evidence is linked to this experiment.
- The results are based on deterministic simulations and may not reflect real-world biological systems.
- Die vom Modell ausgegebene confidence war schemawidrig, fehlte oder lag ausserhalb des Bereichs 0..1. Sie wurde fuer die AIRR-Provenienz konservativ auf 0.0 gesetzt; der Originalwert bleibt als confidence_original erhalten.

### Alternative Erklaerungen

- Keine expliziten Angaben.

### Fehlende Nachweise

- Keine expliziten Angaben.

### Empfohlene Folgeexperimente

- Keine expliziten Angaben.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260916183955739240-d3066655.json](analysis/AIAR-critical_reviewer-20260916183955739240-d3066655.json)
- [analysis/AIAR-scientific_analyst-20260916183939789628-d3066655.json](analysis/AIAR-scientific_analyst-20260916183939789628-d3066655.json)
- [analysis/AIAR-scientific_writer-20260916184011727120-d3066655.json](analysis/AIAR-scientific_writer-20260916184011727120-d3066655.json)
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
