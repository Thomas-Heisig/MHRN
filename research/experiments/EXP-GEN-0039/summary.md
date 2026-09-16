# EXP-GEN-0039: Wissenschaftliche Zusammenfassung

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

- Titel: sustained_activity_stability_v1 — RQ-SNN-001 technical replication
- Bedingungen: no_input_control (negative_control); tonic_drive (stability_treatment)
- Notizen: Second clean execution to verify deterministic reproducibility; not counted as statistically independent evidence.
- Konfiguration: `/home/runner/work/MHRN/MHRN/configs/learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `fa689378651d83c0d4a6e81a17751e3037db469a`
- Git dirty: `False`
- Runtime: `34.5996038830001` s

## 4. Deterministische Formeln

Die im Bericht verwendeten deskriptiven Groessen sind:

- Mittelwert: `mean(x) = (1/n) * sum_i x_i`
- Populationsstandardabweichung: `sigma = sqrt((1/n) * sum_i (x_i - mean(x))^2)`
- Absolute Differenz: `Delta_x = mean(x_B) - mean(x_A)`
- Verhältnis: `R_x = mean(x_B) / mean(x_A)` fuer `mean(x_A) != 0`
- Inter-Spike-Intervall: `ISI_i = t_(i+1) - t_i`

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

#### Primäre und weitere boolesche Endpunkte

| Condition | Outcome | n | true | false | all_true |
| --- | --- | ---: | ---: | ---: | --- |
| no_input_control | `finite_state` | 10 | 10 | 0 | True |
| no_input_control | `stability_pass` | 10 | 10 | 0 | True |
| no_input_control | `topology_unchanged` | 10 | 10 | 0 | True |
| tonic_drive | `finite_state` | 10 | 10 | 0 | True |
| tonic_drive | `stability_pass` | 10 | 10 | 0 | True |
| tonic_drive | `topology_unchanged` | 10 | 10 | 0 | True |

### 5.2 Deskriptive Zwei-Bedingungs-Effekte

- `burn_in_ticks`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `drive_current`: `absolute_difference=50`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `neuron_v_max`: `absolute_difference=5`; `ratio=0.928571`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `neuron_v_min`: `absolute_difference=-25.5949`; `ratio=1.36564`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_mean_spikes`: `absolute_difference=300`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_spike_cv`: `absolute_difference=0`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_spike_relative_drift`: `absolute_difference=0`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_window_count`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `ticks_executed`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `ticks_requested`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `weight_max`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `weight_min`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `window_ticks`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.

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

Deterministische Statistikdatei: `analysis/statistics.json`

## 8. AI Research Report

- AIRR Status: `unavailable`
- Wissenschaftliche Evidenz durch KI: `false`
- Human Review: `PENDING`

## 9. Artefakte

- `DATA/current_run.json`
- `DATA/raw/run-0000-no_input_control-seed-42.json.gz`
- `DATA/raw/run-0001-tonic_drive-seed-42.json.gz`
- `DATA/raw/run-0002-no_input_control-seed-43.json.gz`
- `DATA/raw/run-0003-tonic_drive-seed-43.json.gz`
- `DATA/raw/run-0004-no_input_control-seed-44.json.gz`
- `DATA/raw/run-0005-tonic_drive-seed-44.json.gz`
- `DATA/raw/run-0006-no_input_control-seed-45.json.gz`
- `DATA/raw/run-0007-tonic_drive-seed-45.json.gz`
- `DATA/raw/run-0008-no_input_control-seed-46.json.gz`
- `DATA/raw/run-0009-tonic_drive-seed-46.json.gz`
- `DATA/raw/run-0010-no_input_control-seed-47.json.gz`
- `DATA/raw/run-0011-tonic_drive-seed-47.json.gz`
- `DATA/raw/run-0012-no_input_control-seed-48.json.gz`
- `DATA/raw/run-0013-tonic_drive-seed-48.json.gz`
- `DATA/raw/run-0014-no_input_control-seed-49.json.gz`
- `DATA/raw/run-0015-tonic_drive-seed-49.json.gz`
- `DATA/raw/run-0016-no_input_control-seed-50.json.gz`
- `DATA/raw/run-0017-tonic_drive-seed-50.json.gz`
- `DATA/raw/run-0018-no_input_control-seed-51.json.gz`
- `DATA/raw/run-0019-tonic_drive-seed-51.json.gz`
- `DATA/runs_compact.json`
- `DATA/runs_index.json`
- `analysis/REPLICATION-COMPARISON.json`
- `analysis/ai_packet.json`
- `analysis/ai_packet_digest.json`
- `analysis/statistics.json`
- `manifest.json`
- `report.md`
- `workflow.json`

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `SATISFIED`, semantische Zuordnung `DIRECT_MATCH`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
