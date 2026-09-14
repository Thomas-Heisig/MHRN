# EXP-BATCH-20260914074039-02: Wissenschaftliche Zusammenfassung

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

- Titel: Experiment workflow: tonic_spike_reproducibility_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.09472789999563247` s

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
| same_seed_tonic_replica_pair | 3 | 101,102,103 | — | — | — | — | — | — |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | same_seed_tonic_replica_pair | — | — | — | — | — | — | — |
| 102 | same_seed_tonic_replica_pair | — | — | — | — | — | — | — |
| 103 | same_seed_tonic_replica_pair | — | — | — | — | — | — | — |

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

Die Spikefolgen der Neuronenmodelle sind unter identischen Bedingungen reproduzierbar.

KI-Konfidenz: `1.0` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- Die Git-Provenance ist unvollständig oder nicht verfügbar.
- Es gibt keine verknüpften wissenschaftlichen Beweise für dieses Experiment.

### Alternative Erklaerungen

- Die verwendete Software oder Bibliothek könnte deterministische Ergebnisse liefern.
- Die verwendete Hardware oder Umgebung könnte deterministische Ergebnisse liefern.

### Fehlende Nachweise

- Verknüpfte wissenschaftliche Beweise für das Neuronenmodell.
- Dokumentation der verwendeten Software und Bibliotheken.
- Dokumentation der verwendeten Hardware und Umgebung.

### Empfohlene Folgeexperimente

- Ein Test mit unterschiedlichen Initialisierungsbedingungen.
- Ein Test mit variierenden Parametern des Neuronenmodells.
- Ein Test mit unterschiedlichen Seeds oder Zufallsgeneratoren.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260914074148666019-d7ee5e44.json](analysis/AIAR-critical_reviewer-20260914074148666019-d7ee5e44.json)
- [analysis/AIAR-scientific_analyst-20260914074132664842-d7ee5e44.json](analysis/AIAR-scientific_analyst-20260914074132664842-d7ee5e44.json)
- [analysis/AIAR-scientific_writer-20260914074244424413-d7ee5e44.json](analysis/AIAR-scientific_writer-20260914074244424413-d7ee5e44.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-same_seed_tonic_replica_pair-seed-101.json.gz](DATA/raw/run-0000-same_seed_tonic_replica_pair-seed-101.json.gz)
- [DATA/raw/run-0001-same_seed_tonic_replica_pair-seed-102.json.gz](DATA/raw/run-0001-same_seed_tonic_replica_pair-seed-102.json.gz)
- [DATA/raw/run-0002-same_seed_tonic_replica_pair-seed-103.json.gz](DATA/raw/run-0002-same_seed_tonic_replica_pair-seed-103.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `NOT_APPLICABLE`, semantische Zuordnung `MISMATCH`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
