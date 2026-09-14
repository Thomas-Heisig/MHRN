# EXP-BATCH-20260914074039-08: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-TEMP-001`
- Hypothese: `H-TEMP-001-A`
- Protokoll: `temporal_state_registered_v1`
- Durchlaeufe: `3`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `256`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `256 .. 256` ausgeführte Ticks
- Tick-Vertrag: `SATISFIED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `DIRECT_MATCH`
- Evidence Readiness: `BLOCKED_DIRTY_SOURCE_TREE`
- Begründung: TEMP erwartet fast_medium_slow mit FAST/MEDIUM/SLOW-Horizonten.
- Beobachtete Conditions: `fast_medium_slow`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: temporal_state_registered_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.23622159997466952` s

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
| fast_medium_slow | 3 | 101,102,103 | 256 | 0 | — | — | — | — |

### 5.3 Temporal-State-Horizonte

- `fast`: Referenzvergleiche=762; discrepancy mean=0.0103327, max=0.952011; nonzero=762 (1); mean(nonzero)=0.0103327.
- `medium`: Referenzvergleiche=756; discrepancy mean=0.0150033, max=1.15894; nonzero=756 (1); mean(nonzero)=0.0150033.
- `slow`: Referenzvergleiche=750; discrepancy mean=0.0184276, max=1.17842; nonzero=750 (1); mean(nonzero)=0.0184276.

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | fast_medium_slow | 256 | 0 | — | — | — | — | — |
| 102 | fast_medium_slow | 256 | 0 | — | — | — | — | — |
| 103 | fast_medium_slow | 256 | 0 | — | — | — | — | — |

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

Die Daten zeigen, dass die Temporal-State-Vergleiche unter den FAST-, MEDIUM- und SLOW-Horizonten unterschiedliche Discrepanzen aufweisen, was auf eine deterministische Unterscheidung hinweist. Es wurden jedoch keine inferenziellen Analysen durchgeführt, um statistische Signifikanz oder Kausalität zu bestätigen.

KI-Konfidenz: `0.75` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- AI analysis unavailable; deterministic experiment artifacts remain the authoritative data basis.
- Technical reason: ValueError: Invalid AI analysis output field: assessment

### Alternative Erklaerungen

- Keine expliziten Angaben.

### Fehlende Nachweise

- Eine inferenzielle Analyse der Discrepanzen in den FAST-, MEDIUM- und SLOW-Horizonten.
- Eine Validierung der beobachteten Discrepanzen durch eine Kontrollgruppe oder eine Reproduktion unter ähnlichen Bedingungen.
- Eine Analyse der möglichen systematischen Fehlerquellen oder unkontrollierten Variablen, die die Dispanzen beeinflussen könnten.

### Empfohlene Folgeexperimente

- Eine inferenzielle Analyse der Discrepanzen in den FAST-, MEDIUM- und SLOW-Horizonten, um statistische Signifikanz zu testen.
- Eine Validierung der beobachteten Discrepanzen durch eine Kontrollgruppe oder eine Reproduktion unter ähnlichen Bedingungen.
- Eine Analyse der möglichen systematischen Fehlerquellen oder unkontrollierten Variablen, die die Discrepanzen beeinflussen könnten.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260914075309212330-46405ab8.json](analysis/AIAR-critical_reviewer-20260914075309212330-46405ab8.json)
- [analysis/AIAR-scientific_analyst-20260914075209141766-46405ab8.json](analysis/AIAR-scientific_analyst-20260914075209141766-46405ab8.json)
- [analysis/AIAR-scientific_writer-20260914075334373869-46405ab8.json](analysis/AIAR-scientific_writer-20260914075334373869-46405ab8.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-fast_medium_slow-seed-101.json.gz](DATA/raw/run-0000-fast_medium_slow-seed-101.json.gz)
- [DATA/raw/run-0001-fast_medium_slow-seed-102.json.gz](DATA/raw/run-0001-fast_medium_slow-seed-102.json.gz)
- [DATA/raw/run-0002-fast_medium_slow-seed-103.json.gz](DATA/raw/run-0002-fast_medium_slow-seed-103.json.gz)
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
