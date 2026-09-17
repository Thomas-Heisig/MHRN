# EXP-GEN-0046: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-DET-001`
- Hypothese: `H-SNN-003-A`
- Protokoll: `deterministic_replica_v1`
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

- RQ/Condition-Pruefung: `NOT_AUTOMATICALLY_CLASSIFIED`
- Evidence Readiness: `BLOCKED_UNCLASSIFIED_SEMANTICS`
- Begründung: Keine automatische semantische Regel fuer diese RQ-Familie registriert.
- Beobachtete Conditions: `recurrence_off_replica_a, recurrence_off_replica_b, recurrence_on_replica_a, recurrence_on_replica_b`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: deterministic_replica_v1 — RQ-DET-001
- Bedingungen: registered_protocol_conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `ad2c71424bea71dceb820c10c860b7cc9cb772c7`
- Git dirty: `True`
- Runtime: `0.04422879999037832` s

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
| recurrence_off_replica_a | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| recurrence_off_replica_b | 3 | 101,102,103 | 256 | 3 | 2 | 3 | 0 | 1 |
| recurrence_on_replica_a | 3 | 101,102,103 | 256 | 33 | 33 | 3 | 10 | 61 |
| recurrence_on_replica_b | 3 | 101,102,103 | 256 | 33 | 33 | 3 | 10 | 61 |

**Wichtig:** `—` bedeutet in dieser Tabelle ausschließlich, dass die jeweilige SNN-Metrik für diese Bedingung nicht definiert oder nicht erhoben wird. Es bedeutet **nicht**, dass für die Bedingung keine DATA vorliegen. Protokollspezifische Messwerte werden direkt darunter ausgewiesen.

### 5.1 Protokollspezifische Metrikabdeckung

| Condition | zusätzliche numerische Mittelwerte |
| --- | --- |
| recurrence_off_replica_a | `first_response_latency=2`; `last_response_latency=2`; `max_synaptic_current_targets=1`; `peak_spike_rate=1`; `synaptic_activity_ticks=2`; `ticks_requested=256`; `total_synapses=2` |
| recurrence_off_replica_b | `first_response_latency=2`; `last_response_latency=2`; `max_synaptic_current_targets=1`; `peak_spike_rate=1`; `synaptic_activity_ticks=2`; `ticks_requested=256`; `total_synapses=2` |
| recurrence_on_replica_a | `first_response_latency=2`; `last_response_latency=62`; `max_synaptic_current_targets=1`; `peak_spike_rate=1`; `return_latency=3`; `synaptic_activity_ticks=33`; `ticks_requested=256`; `total_synapses=3` |
| recurrence_on_replica_b | `first_response_latency=2`; `last_response_latency=62`; `max_synaptic_current_targets=1`; `peak_spike_rate=1`; `return_latency=3`; `synaptic_activity_ticks=33`; `ticks_requested=256`; `total_synapses=3` |

#### Primäre und weitere boolesche Endpunkte

| Condition | Outcome | n | true | false | all_true |
| --- | --- | ---: | ---: | ---: | --- |
| recurrence_off_replica_a | `stopped_on_quiescence` | 3 | 0 | 3 | False |
| recurrence_off_replica_b | `stopped_on_quiescence` | 3 | 0 | 3 | False |
| recurrence_on_replica_a | `stopped_on_quiescence` | 3 | 0 | 3 | False |
| recurrence_on_replica_b | `stopped_on_quiescence` | 3 | 0 | 3 | False |

### 5.3 Inter-Spike-Intervalle

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

Deterministische Statistikdatei: `analysis/statistics.json`

## 8. AI Research Report

- AIRR Status: `generated`
- Wissenschaftliche Evidenz durch KI: `false`
- Human Review: `PENDING`
- AIRR Markdown: `reports/AIRR-2026-0001.md`
- AIRR JSON: `reports/AIRR-2026-0001.json`

### 8.1 KI-Einschaetzung

Die Spikefolge ist bei gleichem Seed, Input und Anfangszustand deterministisch identisch. Dies wird durch die konsistenten Metriken und die reproduzierbaren Ergebnisse unter den gleichen Bedingungen bestätigt.

KI-Konfidenz: `0.0` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- Die vom Modell ausgegebene confidence war schemawidrig, fehlte oder lag ausserhalb des Bereichs 0..1. Sie wurde fuer die AIRR-Provenienz konservativ auf 0.0 gesetzt; der Originalwert bleibt als confidence_original erhalten.

### Alternative Erklaerungen

- Keine expliziten Angaben.

### Fehlende Nachweise

- Keine expliziten Angaben.

### Empfohlene Folgeexperimente

- Keine expliziten Folgeexperimente im AIRR angegeben.

## 9. Artefakte

- `analysis/ai_packet.json`
- `analysis/ai_packet_digest.json`
- `analysis/AIAR-critical_reviewer-20260917190847781300-f8673f92.json`
- `analysis/AIAR-scientific_analyst-20260917190828109821-f8673f92.json`
- `analysis/AIAR-scientific_writer-20260917190907519701-f8673f92.json`
- `analysis/statistics.json`
- `DATA/current_run.json`
- `DATA/raw/run-0000-recurrence_off_replica_a-seed-101.json.gz`
- `DATA/raw/run-0001-recurrence_off_replica_b-seed-101.json.gz`
- `DATA/raw/run-0002-recurrence_on_replica_a-seed-101.json.gz`
- `DATA/raw/run-0003-recurrence_on_replica_b-seed-101.json.gz`
- `DATA/raw/run-0004-recurrence_off_replica_a-seed-102.json.gz`
- `DATA/raw/run-0005-recurrence_off_replica_b-seed-102.json.gz`
- `DATA/raw/run-0006-recurrence_on_replica_a-seed-102.json.gz`
- `DATA/raw/run-0007-recurrence_on_replica_b-seed-102.json.gz`
- `DATA/raw/run-0008-recurrence_off_replica_a-seed-103.json.gz`
- `DATA/raw/run-0009-recurrence_off_replica_b-seed-103.json.gz`
- `DATA/raw/run-0010-recurrence_on_replica_a-seed-103.json.gz`
- `DATA/raw/run-0011-recurrence_on_replica_b-seed-103.json.gz`
- `DATA/runs_compact.json`
- `DATA/runs_index.json`
- `manifest.json`
- `report.md`
- `reports/AIRR-2026-0001.json`
- `reports/AIRR-2026-0001.md`
- `workflow.json`

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `SATISFIED`, semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
