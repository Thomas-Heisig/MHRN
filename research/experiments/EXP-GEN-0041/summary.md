# EXP-GEN-0041: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-SNN-006`
- Hypothese: `H-SNN-006-A`
- Protokoll: `sustained_activity_stability_v2`
- Durchlaeufe: `20`
- Seeds: `[101, 102, 103, 104, 105, 106, 107, 108, 109, 110]`
- Angeforderte Ticks: `100000`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `100000 .. 100000` ausgeführte Ticks
- Tick-Vertrag: `SATISFIED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `CONFIRMATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `NOT_AUTOMATICALLY_CLASSIFIED`
- Evidence Readiness: `BLOCKED_UNCLASSIFIED_SEMANTICS`
- Begründung: Keine automatische semantische Regel fuer diese RQ-Familie registriert.
- Beobachtete Conditions: `no_input_control, tonic_drive`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: sustained_activity_stability_v2 — seed-bound robustness
- Bedingungen: paired no_input_control and tonic_drive across ten distinct seed-bound parameterizations
- Notizen: First execution after frozen PREREG-SNN-006; no post-hoc threshold or parameter changes.
- Konfiguration: `/home/runner/work/MHRN/MHRN/configs/learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `593234e9a4daaf38619adc10c7b56f97da17104f`
- Git dirty: `False`
- Runtime: `36.01270391599999` s

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
| no_input_control | 10 | 101,102,103,104,105,106,107,108,109,110 | 100000 | 0 | — | — | — | — |
| tonic_drive | 10 | 101,102,103,104,105,106,107,108,109,110 | 100000 | 27015.3 | — | — | — | — |

**Wichtig:** `—` bedeutet in dieser Tabelle ausschließlich, dass die jeweilige SNN-Metrik für diese Bedingung nicht definiert oder nicht erhoben wird. Es bedeutet **nicht**, dass für die Bedingung keine DATA vorliegen. Protokollspezifische Messwerte werden direkt darunter ausgewiesen.

### 5.1 Protokollspezifische Metrikabdeckung

| Condition | zusätzliche numerische Mittelwerte |
| --- | --- |
| no_input_control | `active_window_fraction=0`; `burn_in_ticks=10000`; `drive_current=0`; `drive_scale=1.01696`; `effective_drive_current=0`; `neuron_v_max=-70`; `neuron_v_min=-70`; `parameter_jitter_fraction=0.05`; `post_burn_in_mean_spikes=0`; `post_burn_in_spike_cv=0`; `post_burn_in_spike_relative_drift=0`; `post_burn_in_voltage_relative_drift=0`; `post_burn_in_window_count=90`; `realization_drive_scale=1.01696`; `realization_weight_scale=0.994217`; `silent_window_fraction=1`; `ticks_requested=100000`; `weight_max=99.4217`; `weight_min=99.4217`; `weight_scale=0.994217`; `window_ticks=1000` |
| tonic_drive | `active_window_fraction=1`; `burn_in_ticks=10000`; `drive_current=50`; `drive_scale=1.01696`; `effective_drive_current=50.8478`; `first_active_tick=2`; `last_active_tick=99997`; `neuron_v_max=-47.9576`; `neuron_v_min=-94.5585`; `parameter_jitter_fraction=0.05`; `post_burn_in_mean_spikes=269.983`; `post_burn_in_spike_cv=0.0147467`; `post_burn_in_spike_relative_drift=0.0139679`; `post_burn_in_voltage_relative_drift=0.000546182`; `post_burn_in_window_count=90`; `realization_drive_scale=1.01696`; `realization_weight_scale=0.994217`; `silent_window_fraction=0`; `ticks_requested=100000`; `weight_max=99.4217`; `weight_min=99.4217`; `weight_scale=0.994217`; `window_ticks=1000` |

#### Primäre und weitere boolesche Endpunkte

| Condition | Outcome | n | true | false | all_true |
| --- | --- | ---: | ---: | ---: | --- |
| no_input_control | `active_dynamics_pass` | 10 | 0 | 10 | False |
| no_input_control | `finite_state` | 10 | 10 | 0 | True |
| no_input_control | `numerical_stability_pass` | 10 | 10 | 0 | True |
| no_input_control | `paired_realization` | 10 | 10 | 0 | True |
| no_input_control | `realization_unique_across_registered_seeds` | 10 | 10 | 0 | True |
| no_input_control | `robustness_stability_pass` | 10 | 10 | 0 | True |
| no_input_control | `seed_effect_expected` | 10 | 10 | 0 | True |
| no_input_control | `topology_unchanged` | 10 | 10 | 0 | True |
| tonic_drive | `active_dynamics_pass` | 10 | 10 | 0 | True |
| tonic_drive | `finite_state` | 10 | 10 | 0 | True |
| tonic_drive | `numerical_stability_pass` | 10 | 10 | 0 | True |
| tonic_drive | `paired_realization` | 10 | 10 | 0 | True |
| tonic_drive | `realization_unique_across_registered_seeds` | 10 | 10 | 0 | True |
| tonic_drive | `robustness_stability_pass` | 10 | 10 | 0 | True |
| tonic_drive | `seed_effect_expected` | 10 | 10 | 0 | True |
| tonic_drive | `topology_unchanged` | 10 | 10 | 0 | True |

### 5.2 Deskriptive Zwei-Bedingungs-Effekte

- `active_window_fraction`: `absolute_difference=1`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `burn_in_ticks`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `drive_current`: `absolute_difference=50`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `drive_scale`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `effective_drive_current`: `absolute_difference=50.8478`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `neuron_v_max`: `absolute_difference=22.0424`; `ratio=0.685108`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `neuron_v_min`: `absolute_difference=-24.5585`; `ratio=1.35084`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `parameter_jitter_fraction`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_mean_spikes`: `absolute_difference=269.983`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_spike_cv`: `absolute_difference=0.0147467`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_spike_relative_drift`: `absolute_difference=0.0139679`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_voltage_relative_drift`: `absolute_difference=0.000546182`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `post_burn_in_window_count`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `realization_drive_scale`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `realization_weight_scale`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `silent_window_fraction`: `absolute_difference=-1`; `ratio=0`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `ticks_executed`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `ticks_requested`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `total_spikes`: `absolute_difference=27015.3`; `ratio=—`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `weight_max`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `weight_min`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `weight_scale`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.
- `window_ticks`: `absolute_difference=0`; `ratio=1`; Referenz `no_input_control`, Vergleich `tonic_drive`.

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 101 | tonic_drive | 100000 | 26967 | — | — | — | — | — |
| 102 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 102 | tonic_drive | 100000 | 26240 | — | — | — | — | — |
| 103 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 103 | tonic_drive | 100000 | 26545 | — | — | — | — | — |
| 104 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 104 | tonic_drive | 100000 | 30004 | — | — | — | — | — |
| 105 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 105 | tonic_drive | 100000 | 26469 | — | — | — | — | — |
| 106 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 106 | tonic_drive | 100000 | 23430 | — | — | — | — | — |
| 107 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 107 | tonic_drive | 100000 | 30010 | — | — | — | — | — |
| 108 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 108 | tonic_drive | 100000 | 26556 | — | — | — | — | — |
| 109 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 109 | tonic_drive | 100000 | 26980 | — | — | — | — | — |
| 110 | no_input_control | 100000 | 0 | — | — | — | — | — |
| 110 | tonic_drive | 100000 | 26952 | — | — | — | — | — |

## 7. Reproduzierbarkeit und Provenienz

Identische Ausgaben ueber mehrere Seeds dokumentieren reproduzierbare Modelltrajektorien unter diesen Bedingungen. Sie sind nicht automatisch statistisch unabhaengige Replikate. State-Digests sind Integritaets-/Identitaetsmarker und keine metrischen Zustandsabstaende.

Deterministische Statistikdatei: `analysis/statistics.json`

## 8. AI Research Report

- AIRR Status: `unavailable`
- Wissenschaftliche Evidenz durch KI: `false`
- Human Review: `PENDING`

## 9. Artefakte

- `DATA/current_run.json`
- `DATA/raw/run-0000-no_input_control-seed-101.json.gz`
- `DATA/raw/run-0001-tonic_drive-seed-101.json.gz`
- `DATA/raw/run-0002-no_input_control-seed-102.json.gz`
- `DATA/raw/run-0003-tonic_drive-seed-102.json.gz`
- `DATA/raw/run-0004-no_input_control-seed-103.json.gz`
- `DATA/raw/run-0005-tonic_drive-seed-103.json.gz`
- `DATA/raw/run-0006-no_input_control-seed-104.json.gz`
- `DATA/raw/run-0007-tonic_drive-seed-104.json.gz`
- `DATA/raw/run-0008-no_input_control-seed-105.json.gz`
- `DATA/raw/run-0009-tonic_drive-seed-105.json.gz`
- `DATA/raw/run-0010-no_input_control-seed-106.json.gz`
- `DATA/raw/run-0011-tonic_drive-seed-106.json.gz`
- `DATA/raw/run-0012-no_input_control-seed-107.json.gz`
- `DATA/raw/run-0013-tonic_drive-seed-107.json.gz`
- `DATA/raw/run-0014-no_input_control-seed-108.json.gz`
- `DATA/raw/run-0015-tonic_drive-seed-108.json.gz`
- `DATA/raw/run-0016-no_input_control-seed-109.json.gz`
- `DATA/raw/run-0017-tonic_drive-seed-109.json.gz`
- `DATA/raw/run-0018-no_input_control-seed-110.json.gz`
- `DATA/raw/run-0019-tonic_drive-seed-110.json.gz`
- `DATA/runs_compact.json`
- `DATA/runs_index.json`
- `analysis/ai_packet.json`
- `analysis/ai_packet_digest.json`
- `analysis/statistics.json`
- `manifest.json`
- `report.md`
- `workflow.json`

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `SATISFIED`, semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
