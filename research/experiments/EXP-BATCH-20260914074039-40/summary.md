# EXP-BATCH-20260914074039-40: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-TEMP-002`
- Hypothese: `H-TEMP-002-A`
- Protokoll: `temporal_order_spiking_v1`
- Durchlaeufe: `60`
- Seeds: `[101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]`
- Angeforderte Ticks: `32`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `32 .. 32` ausgeführte Ticks
- Tick-Vertrag: `SATISFIED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `CONFIRMATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `DIRECT_MATCH`
- Evidence Readiness: `BLOCKED_DIRTY_SOURCE_TREE`
- Begründung: TEMP-002 erwartet Forward-, Reverse- und Simultankontrolle.
- Beobachtete Conditions: `forward, reverse, simultaneous`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: temporal_order_spiking_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `0.06530049996217713` s

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
| forward | 20 | 101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120 | 32 | 6 | — | — | — | — |
| reverse | 20 | 101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120 | 32 | 6 | — | — | — | — |
| simultaneous | 20 | 101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120 | 32 | 3 | — | — | — | — |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | forward | 32 | 6 | — | — | — | — | — |
| 101 | reverse | 32 | 6 | — | — | — | — | — |
| 101 | simultaneous | 32 | 3 | — | — | — | — | — |
| 102 | forward | 32 | 6 | — | — | — | — | — |
| 102 | reverse | 32 | 6 | — | — | — | — | — |
| 102 | simultaneous | 32 | 3 | — | — | — | — | — |
| 103 | forward | 32 | 6 | — | — | — | — | — |
| 103 | reverse | 32 | 6 | — | — | — | — | — |
| 103 | simultaneous | 32 | 3 | — | — | — | — | — |
| 104 | forward | 32 | 6 | — | — | — | — | — |
| 104 | reverse | 32 | 6 | — | — | — | — | — |
| 104 | simultaneous | 32 | 3 | — | — | — | — | — |
| 105 | forward | 32 | 6 | — | — | — | — | — |
| 105 | reverse | 32 | 6 | — | — | — | — | — |
| 105 | simultaneous | 32 | 3 | — | — | — | — | — |
| 106 | forward | 32 | 6 | — | — | — | — | — |
| 106 | reverse | 32 | 6 | — | — | — | — | — |
| 106 | simultaneous | 32 | 3 | — | — | — | — | — |
| 107 | forward | 32 | 6 | — | — | — | — | — |
| 107 | reverse | 32 | 6 | — | — | — | — | — |
| 107 | simultaneous | 32 | 3 | — | — | — | — | — |
| 108 | forward | 32 | 6 | — | — | — | — | — |
| 108 | reverse | 32 | 6 | — | — | — | — | — |
| 108 | simultaneous | 32 | 3 | — | — | — | — | — |
| 109 | forward | 32 | 6 | — | — | — | — | — |
| 109 | reverse | 32 | 6 | — | — | — | — | — |
| 109 | simultaneous | 32 | 3 | — | — | — | — | — |
| 110 | forward | 32 | 6 | — | — | — | — | — |
| 110 | reverse | 32 | 6 | — | — | — | — | — |
| 110 | simultaneous | 32 | 3 | — | — | — | — | — |
| 111 | forward | 32 | 6 | — | — | — | — | — |
| 111 | reverse | 32 | 6 | — | — | — | — | — |
| 111 | simultaneous | 32 | 3 | — | — | — | — | — |
| 112 | forward | 32 | 6 | — | — | — | — | — |
| 112 | reverse | 32 | 6 | — | — | — | — | — |
| 112 | simultaneous | 32 | 3 | — | — | — | — | — |
| 113 | forward | 32 | 6 | — | — | — | — | — |
| 113 | reverse | 32 | 6 | — | — | — | — | — |
| 113 | simultaneous | 32 | 3 | — | — | — | — | — |
| 114 | forward | 32 | 6 | — | — | — | — | — |
| 114 | reverse | 32 | 6 | — | — | — | — | — |
| 114 | simultaneous | 32 | 3 | — | — | — | — | — |
| 115 | forward | 32 | 6 | — | — | — | — | — |
| 115 | reverse | 32 | 6 | — | — | — | — | — |
| 115 | simultaneous | 32 | 3 | — | — | — | — | — |
| 116 | forward | 32 | 6 | — | — | — | — | — |
| 116 | reverse | 32 | 6 | — | — | — | — | — |
| 116 | simultaneous | 32 | 3 | — | — | — | — | — |
| 117 | forward | 32 | 6 | — | — | — | — | — |
| 117 | reverse | 32 | 6 | — | — | — | — | — |
| 117 | simultaneous | 32 | 3 | — | — | — | — | — |
| 118 | forward | 32 | 6 | — | — | — | — | — |
| 118 | reverse | 32 | 6 | — | — | — | — | — |
| 118 | simultaneous | 32 | 3 | — | — | — | — | — |
| 119 | forward | 32 | 6 | — | — | — | — | — |
| 119 | reverse | 32 | 6 | — | — | — | — | — |
| 119 | simultaneous | 32 | 3 | — | — | — | — | — |
| 120 | forward | 32 | 6 | — | — | — | — | — |
| 120 | reverse | 32 | 6 | — | — | — | — | — |
| 120 | simultaneous | 32 | 3 | — | — | — | — | — |

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

Die Daten zeigen, dass bei gleicher Ereignisanzahl unterschiedliche Reihenfolgen unterschiedliche spike-basierte Antwortsignaturen erzeugen. Die Ergebnisse sind konsistent und reproduzierbar, da alle Metriken in allen Bedingungen identisch sind. Es gibt jedoch keine statistische Signifikanz, da keine inferenzstatistischen Analysen durchgeführt wurden.

KI-Konfidenz: `0.95` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- Die Daten sind rein deskriptiv und keine inferenzstatistischen Analysen wurden durchgeführt.
- Es gibt keine Kontrollgruppe oder Vergleichsbedingung, die die Ergebnisse isolieren könnte.
- Die Reihenfolge der Ereignisse könnte eine andere Variable beeinflussen, die nicht gemessen wurde.

### Alternative Erklaerungen

- Die unterschiedlichen Antwortsignaturen könnten aufgrund der unterschiedlichen Scheduling-Strategien entstehen, die die Spike-Aktivität beeinflussen.
- Die unterschiedlichen Antwortsignaturen könnten aufgrund der unterschiedlichen state_digests entstehen, die die Spike-Aktivität beeinflussen.
- Die unterschiedlichen Antwortsignaturen könnten aufgrund der unterschiedlichen seeds entstehen, die die Spike-Aktivität beeinflussen.

### Fehlende Nachweise

- Eine inferenzstatistische Analyse der Daten, um die Signifikanz der Ergebnisse zu testen.
- Ein Experiment mit einer Kontrollgruppe, um die Ergebnisse zu isolieren.
- Ein Experiment mit einer anderen Scheduling-Strategie, um die Auswirkungen auf die Spike-Aktivität zu testen.

### Empfohlene Folgeexperimente

- Eine inferenzstatistische Analyse der Daten, um die Signifikanz der Ergebnisse zu testen.
- Ein Experiment mit einer Kontrollgruppe, um die Ergebnisse zu isolieren.
- Ein Experiment mit einer anderen Scheduling-Strategie, um die Auswirkungen auf die Spike-Aktivität zu testen.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260914084243379954-a6475baf.json](analysis/AIAR-critical_reviewer-20260914084243379954-a6475baf.json)
- [analysis/AIAR-scientific_analyst-20260914084133906848-a6475baf.json](analysis/AIAR-scientific_analyst-20260914084133906848-a6475baf.json)
- [analysis/AIAR-scientific_writer-20260914084305127027-a6475baf.json](analysis/AIAR-scientific_writer-20260914084305127027-a6475baf.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-forward-seed-101.json.gz](DATA/raw/run-0000-forward-seed-101.json.gz)
- [DATA/raw/run-0001-reverse-seed-101.json.gz](DATA/raw/run-0001-reverse-seed-101.json.gz)
- [DATA/raw/run-0002-simultaneous-seed-101.json.gz](DATA/raw/run-0002-simultaneous-seed-101.json.gz)
- [DATA/raw/run-0003-forward-seed-102.json.gz](DATA/raw/run-0003-forward-seed-102.json.gz)
- [DATA/raw/run-0004-reverse-seed-102.json.gz](DATA/raw/run-0004-reverse-seed-102.json.gz)
- [DATA/raw/run-0005-simultaneous-seed-102.json.gz](DATA/raw/run-0005-simultaneous-seed-102.json.gz)
- [DATA/raw/run-0006-forward-seed-103.json.gz](DATA/raw/run-0006-forward-seed-103.json.gz)
- [DATA/raw/run-0007-reverse-seed-103.json.gz](DATA/raw/run-0007-reverse-seed-103.json.gz)
- [DATA/raw/run-0008-simultaneous-seed-103.json.gz](DATA/raw/run-0008-simultaneous-seed-103.json.gz)
- [DATA/raw/run-0009-forward-seed-104.json.gz](DATA/raw/run-0009-forward-seed-104.json.gz)
- [DATA/raw/run-0010-reverse-seed-104.json.gz](DATA/raw/run-0010-reverse-seed-104.json.gz)
- [DATA/raw/run-0011-simultaneous-seed-104.json.gz](DATA/raw/run-0011-simultaneous-seed-104.json.gz)
- [DATA/raw/run-0012-forward-seed-105.json.gz](DATA/raw/run-0012-forward-seed-105.json.gz)
- [DATA/raw/run-0013-reverse-seed-105.json.gz](DATA/raw/run-0013-reverse-seed-105.json.gz)
- [DATA/raw/run-0014-simultaneous-seed-105.json.gz](DATA/raw/run-0014-simultaneous-seed-105.json.gz)
- [DATA/raw/run-0015-forward-seed-106.json.gz](DATA/raw/run-0015-forward-seed-106.json.gz)
- [DATA/raw/run-0016-reverse-seed-106.json.gz](DATA/raw/run-0016-reverse-seed-106.json.gz)
- [DATA/raw/run-0017-simultaneous-seed-106.json.gz](DATA/raw/run-0017-simultaneous-seed-106.json.gz)
- [DATA/raw/run-0018-forward-seed-107.json.gz](DATA/raw/run-0018-forward-seed-107.json.gz)
- [DATA/raw/run-0019-reverse-seed-107.json.gz](DATA/raw/run-0019-reverse-seed-107.json.gz)
- [DATA/raw/run-0020-simultaneous-seed-107.json.gz](DATA/raw/run-0020-simultaneous-seed-107.json.gz)
- [DATA/raw/run-0021-forward-seed-108.json.gz](DATA/raw/run-0021-forward-seed-108.json.gz)
- [DATA/raw/run-0022-reverse-seed-108.json.gz](DATA/raw/run-0022-reverse-seed-108.json.gz)
- [DATA/raw/run-0023-simultaneous-seed-108.json.gz](DATA/raw/run-0023-simultaneous-seed-108.json.gz)
- [DATA/raw/run-0024-forward-seed-109.json.gz](DATA/raw/run-0024-forward-seed-109.json.gz)
- [DATA/raw/run-0025-reverse-seed-109.json.gz](DATA/raw/run-0025-reverse-seed-109.json.gz)
- [DATA/raw/run-0026-simultaneous-seed-109.json.gz](DATA/raw/run-0026-simultaneous-seed-109.json.gz)
- [DATA/raw/run-0027-forward-seed-110.json.gz](DATA/raw/run-0027-forward-seed-110.json.gz)
- [DATA/raw/run-0028-reverse-seed-110.json.gz](DATA/raw/run-0028-reverse-seed-110.json.gz)
- [DATA/raw/run-0029-simultaneous-seed-110.json.gz](DATA/raw/run-0029-simultaneous-seed-110.json.gz)
- [DATA/raw/run-0030-forward-seed-111.json.gz](DATA/raw/run-0030-forward-seed-111.json.gz)
- [DATA/raw/run-0031-reverse-seed-111.json.gz](DATA/raw/run-0031-reverse-seed-111.json.gz)
- [DATA/raw/run-0032-simultaneous-seed-111.json.gz](DATA/raw/run-0032-simultaneous-seed-111.json.gz)
- [DATA/raw/run-0033-forward-seed-112.json.gz](DATA/raw/run-0033-forward-seed-112.json.gz)
- [DATA/raw/run-0034-reverse-seed-112.json.gz](DATA/raw/run-0034-reverse-seed-112.json.gz)
- [DATA/raw/run-0035-simultaneous-seed-112.json.gz](DATA/raw/run-0035-simultaneous-seed-112.json.gz)
- [DATA/raw/run-0036-forward-seed-113.json.gz](DATA/raw/run-0036-forward-seed-113.json.gz)
- [DATA/raw/run-0037-reverse-seed-113.json.gz](DATA/raw/run-0037-reverse-seed-113.json.gz)
- [DATA/raw/run-0038-simultaneous-seed-113.json.gz](DATA/raw/run-0038-simultaneous-seed-113.json.gz)
- [DATA/raw/run-0039-forward-seed-114.json.gz](DATA/raw/run-0039-forward-seed-114.json.gz)
- [DATA/raw/run-0040-reverse-seed-114.json.gz](DATA/raw/run-0040-reverse-seed-114.json.gz)
- [DATA/raw/run-0041-simultaneous-seed-114.json.gz](DATA/raw/run-0041-simultaneous-seed-114.json.gz)
- [DATA/raw/run-0042-forward-seed-115.json.gz](DATA/raw/run-0042-forward-seed-115.json.gz)
- [DATA/raw/run-0043-reverse-seed-115.json.gz](DATA/raw/run-0043-reverse-seed-115.json.gz)
- [DATA/raw/run-0044-simultaneous-seed-115.json.gz](DATA/raw/run-0044-simultaneous-seed-115.json.gz)
- [DATA/raw/run-0045-forward-seed-116.json.gz](DATA/raw/run-0045-forward-seed-116.json.gz)
- [DATA/raw/run-0046-reverse-seed-116.json.gz](DATA/raw/run-0046-reverse-seed-116.json.gz)
- [DATA/raw/run-0047-simultaneous-seed-116.json.gz](DATA/raw/run-0047-simultaneous-seed-116.json.gz)
- [DATA/raw/run-0048-forward-seed-117.json.gz](DATA/raw/run-0048-forward-seed-117.json.gz)
- [DATA/raw/run-0049-reverse-seed-117.json.gz](DATA/raw/run-0049-reverse-seed-117.json.gz)
- [DATA/raw/run-0050-simultaneous-seed-117.json.gz](DATA/raw/run-0050-simultaneous-seed-117.json.gz)
- [DATA/raw/run-0051-forward-seed-118.json.gz](DATA/raw/run-0051-forward-seed-118.json.gz)
- [DATA/raw/run-0052-reverse-seed-118.json.gz](DATA/raw/run-0052-reverse-seed-118.json.gz)
- [DATA/raw/run-0053-simultaneous-seed-118.json.gz](DATA/raw/run-0053-simultaneous-seed-118.json.gz)
- [DATA/raw/run-0054-forward-seed-119.json.gz](DATA/raw/run-0054-forward-seed-119.json.gz)
- [DATA/raw/run-0055-reverse-seed-119.json.gz](DATA/raw/run-0055-reverse-seed-119.json.gz)
- [DATA/raw/run-0056-simultaneous-seed-119.json.gz](DATA/raw/run-0056-simultaneous-seed-119.json.gz)
- [DATA/raw/run-0057-forward-seed-120.json.gz](DATA/raw/run-0057-forward-seed-120.json.gz)
- [DATA/raw/run-0058-reverse-seed-120.json.gz](DATA/raw/run-0058-reverse-seed-120.json.gz)
- [DATA/raw/run-0059-simultaneous-seed-120.json.gz](DATA/raw/run-0059-simultaneous-seed-120.json.gz)
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
