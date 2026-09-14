# EXP-BATCH-20260914074039-05: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-SNN-004`
- Hypothese: `H-SNN-004-A`
- Protokoll: `stdp_weight_matrix_v1`
- Durchlaeufe: `3`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `1000`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `nicht direkt messbar .. nicht direkt messbar` ausgeführte Ticks
- Tick-Vertrag: `NOT_APPLICABLE`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `NOT_AUTOMATICALLY_CLASSIFIED`
- Evidence Readiness: `BLOCKED_UNCLASSIFIED_SEMANTICS`
- Begründung: Keine automatische semantische Regel fuer diese RQ-Familie registriert.
- Beobachtete Conditions: `productive_reward_stdp`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: stdp_weight_matrix_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.10662139998748899` s

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
| productive_reward_stdp | 3 | 101,102,103 | — | — | — | — | — | — |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | productive_reward_stdp | — | — | — | — | — | — | — |
| 102 | productive_reward_stdp | — | — | — | — | — | — | — |
| 103 | productive_reward_stdp | — | — | — | — | — | — | — |

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

Provider output could not be validated as structured analysis; no scientific interpretation is inferred.

KI-Konfidenz: `0.0` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- Die Experimente wurden ohne Kontrollgruppe durchgeführt, was eine Verzerrung der Ergebnisse ermöglichen könnte.
- Die gleichen Ergebnisse in allen drei Experimenten deuten auf eine mögliche Übergeneralisierung oder eine fehlende Varianz hin.
- Die Verwendung von deterministischen Modellen könnte die Ergebnisse beeinflussen, da zufällige Faktoren nicht berücksichtigt werden.
- Die fehlende statistische Signifikanzanalyse macht es schwierig, die Ergebnisse zu validieren.
- Die fehlende Validierung der Zeitabstände und der Gewichtsanpassung könnte zu einer Verzerrung der Ergebnisse führen.

### Alternative Erklaerungen

- Die asymmetrische Gewichtsanpassung könnte auf andere Faktoren wie externe Reize oder neuronale Aktivitätsmuster zurückzuführen sein.
- Die gleichen Ergebnisse in allen Experimenten könnten auf eine fehlende Varianz oder eine zu kleine Stichprobe zurückzuführen sein.
- Die deterministischen Modelle könnten die Ergebnisse beeinflussen, da zufällige Faktoren nicht berücksichtigt werden.
- Die fehlende Validierung der Zeitabstände und der Gewichtsanpassung könnte zu einer Verzerrung der Ergebnisse führen.

### Fehlende Nachweise

- Repeat provider analysis from the same immutable research packet.

### Empfohlene Folgeexperimente

- Keine expliziten Folgeexperimente im AIRR angegeben.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260914074543745478-0c121f24.json](analysis/AIAR-critical_reviewer-20260914074543745478-0c121f24.json)
- [analysis/AIAR-scientific_analyst-20260914074522660162-0c121f24.json](analysis/AIAR-scientific_analyst-20260914074522660162-0c121f24.json)
- [analysis/AIAR-scientific_writer-20260914074717923194-0c121f24.json](analysis/AIAR-scientific_writer-20260914074717923194-0c121f24.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-productive_reward_stdp-seed-101.json.gz](DATA/raw/run-0000-productive_reward_stdp-seed-101.json.gz)
- [DATA/raw/run-0001-productive_reward_stdp-seed-102.json.gz](DATA/raw/run-0001-productive_reward_stdp-seed-102.json.gz)
- [DATA/raw/run-0002-productive_reward_stdp-seed-103.json.gz](DATA/raw/run-0002-productive_reward_stdp-seed-103.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `NOT_APPLICABLE`, semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
