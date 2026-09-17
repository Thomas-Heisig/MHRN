# EXP-GEN-0045: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-SNN-002`
- Hypothese: `H-SNN-002-A`
- Protokoll: `tonic_spike_reproducibility_v1`
- Durchlaeufe: `3`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `256`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `nicht direkt messbar .. nicht direkt messbar` ausgeführte Ticks
- Tick-Vertrag: `NOT_APPLICABLE`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `MISMATCH`
- Evidence Readiness: `BLOCKED_SEMANTIC_MISMATCH`
- Begründung: RQ-SNN-002 erwartet einen kontrollierten Impulsantwort-Vergleich mit recurrence_off und recurrence_on.
- Beobachtete Conditions: `same_seed_tonic_replica_pair`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: tonic_spike_reproducibility_v1 — RQ-SNN-002
- Bedingungen: registered_protocol_conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `ad2c71424bea71dceb820c10c860b7cc9cb772c7`
- Git dirty: `False`
- Runtime: `0.0467132999910973` s

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
| same_seed_tonic_replica_pair | 3 | 101,102,103 | — | — | — | — | — | — |

**Wichtig:** `—` bedeutet in dieser Tabelle ausschließlich, dass die jeweilige SNN-Metrik für diese Bedingung nicht definiert oder nicht erhoben wird. Es bedeutet **nicht**, dass für die Bedingung keine DATA vorliegen. Protokollspezifische Messwerte werden direkt darunter ausgewiesen.

### 5.1 Protokollspezifische Metrikabdeckung

| Condition | zusätzliche numerische Mittelwerte |
| --- | --- |
| same_seed_tonic_replica_pair | `ticks_requested=256`; `tonic_current=10` |

#### Primäre und weitere boolesche Endpunkte

| Condition | Outcome | n | true | false | all_true |
| --- | --- | ---: | ---: | ---: | --- |
| same_seed_tonic_replica_pair | `automatic_evidence_promotion` | 3 | 0 | 3 | False |
| same_seed_tonic_replica_pair | `direct_test_of_hypothesis` | 3 | 3 | 0 | True |
| same_seed_tonic_replica_pair | `scientific_evidence` | 3 | 0 | 3 | False |
| same_seed_tonic_replica_pair | `spike_sequence_identical` | 3 | 3 | 0 | True |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | same_seed_tonic_replica_pair | — | — | — | — | — | — | — |
| 102 | same_seed_tonic_replica_pair | — | — | — | — | — | — | — |
| 103 | same_seed_tonic_replica_pair | — | — | — | — | — | — | — |

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

Das Izhikevich-Neuronenmodell erzeugt bei identischem Input reproduzierbare Spikefolgen, wie aus den identischen Spike-sequenzen in allen drei Experimenten hervorgeht.

KI-Konfidenz: `0.95` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- Die experimentellen Daten sind vollständig und konsistent, aber es fehlen statistische Tests zur Bestätigung der Reproduzierbarkeit.
- Die Verknüpfung der state_digests könnte eine zusätzliche Validierung der Determinismus-Eigenschaft erfordern.

### Alternative Erklaerungen

- Die Reproduzierbarkeit könnte auf die deterministische Natur der Izhikevich-Gleichungen zurückzuführen sein, nicht auf externe Faktoren.
- Die verwendete Software oder die Implement, 

### Fehlende Nachweise

- Eine detaillierte Analyse der Izhikevich-Gleichungen, um die deterministische Natur des Modells zu bestätigen.
- Ein Nachweis der Implementierungskonsistenz der Software, um externe Einflüsse auszuschließen.

### Empfohlene Folgeexperimente

- Ein Test mit variierenden Initialbedingungen, um die Robustheit der Reproduzierbarkeit zu überprüfen.
- Ein Vergleich mit anderen Neuronenmodellen, um die spezifische Determinismus-Eigenschaft des Izhikevich-Modells zu validieren.

## 9. Artefakte

- `analysis/ai_packet.json`
- `analysis/ai_packet_digest.json`
- `analysis/AIAR-critical_reviewer-20260917190034649986-d7ce9950.json`
- `analysis/AIAR-scientific_analyst-20260917185950670763-d7ce9950.json`
- `analysis/AIAR-scientific_writer-20260917190134048951-d7ce9950.json`
- `analysis/statistics.json`
- `DATA/current_run.json`
- `DATA/raw/run-0000-same_seed_tonic_replica_pair-seed-101.json.gz`
- `DATA/raw/run-0001-same_seed_tonic_replica_pair-seed-102.json.gz`
- `DATA/raw/run-0002-same_seed_tonic_replica_pair-seed-103.json.gz`
- `DATA/runs_compact.json`
- `DATA/runs_index.json`
- `manifest.json`
- `report.md`
- `reports/AIRR-2026-0001.json`
- `reports/AIRR-2026-0001.md`
- `workflow.json`

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `NOT_APPLICABLE`, semantische Zuordnung `MISMATCH`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
