# EXP-BATCH-CONCEPTUAL-AUDITS-20261001-REVIEW-16: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-WEL-101`
- Hypothese: `H-WEL-101-A`
- Protokoll: `cog_wel_101_v1`
- Durchlaeufe: `12`
- Seeds: `[101, 102, 103]`
- Angeforderte Ticks: `1`
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
- Beobachtete Conditions: `alternative_model, assumption_explicit, claim_boundary, measurement_limit`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Registered conceptual audit: cog_wel_101_v1
- Bedingungen: frozen preregistered conceptual boundary contract
- Notizen: Sequential conceptual audit only. Direct human-review request created; no native SNN execution, direct causal test, or automatic DATA-to-EVID promotion.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `1f489c978592dc14dc20492c322a34fe25dddba3`
- Git dirty: `True`
- Runtime: `0.010768900043331087` s

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
| alternative_model | 3 | 101,102,103 | — | — | — | — | — | — |
| assumption_explicit | 3 | 101,102,103 | — | — | — | — | — | — |
| claim_boundary | 3 | 101,102,103 | — | — | — | — | — | — |
| measurement_limit | 3 | 101,102,103 | — | — | — | — | — | — |

**Wichtig:** `—` bedeutet in dieser Tabelle ausschließlich, dass die jeweilige SNN-Metrik für diese Bedingung nicht definiert oder nicht erhoben wird. Es bedeutet **nicht**, dass für die Bedingung keine DATA vorliegen. Protokollspezifische Messwerte werden direkt darunter ausgewiesen.

### 5.1 Protokollspezifische Metrikabdeckung

| Condition | zusätzliche numerische Mittelwerte |
| --- | --- |
| alternative_model | `audit_item=2` |
| assumption_explicit | `audit_item=1` |
| claim_boundary | `audit_item=4` |
| measurement_limit | `audit_item=3` |

#### Primäre und weitere boolesche Endpunkte

| Condition | Outcome | n | true | false | all_true |
| --- | --- | ---: | ---: | ---: | --- |
| alternative_model | `audit_complete` | 3 | 0 | 3 | False |
| alternative_model | `audit_template_generated` | 3 | 3 | 0 | True |
| alternative_model | `automatic_evidence_promotion` | 3 | 0 | 3 | False |
| alternative_model | `conceptual_or_normative` | 3 | 3 | 0 | True |
| alternative_model | `native_empirical_experiment` | 3 | 0 | 3 | False |
| alternative_model | `phenomenal_claim_identified` | 3 | 0 | 3 | False |
| alternative_model | `scientific_evidence` | 3 | 0 | 3 | False |
| alternative_model | `snn_involved` | 3 | 0 | 3 | False |
| assumption_explicit | `audit_complete` | 3 | 0 | 3 | False |
| assumption_explicit | `audit_template_generated` | 3 | 3 | 0 | True |
| assumption_explicit | `automatic_evidence_promotion` | 3 | 0 | 3 | False |
| assumption_explicit | `conceptual_or_normative` | 3 | 3 | 0 | True |
| assumption_explicit | `native_empirical_experiment` | 3 | 0 | 3 | False |
| assumption_explicit | `phenomenal_claim_identified` | 3 | 0 | 3 | False |
| assumption_explicit | `scientific_evidence` | 3 | 0 | 3 | False |
| assumption_explicit | `snn_involved` | 3 | 0 | 3 | False |
| claim_boundary | `audit_complete` | 3 | 0 | 3 | False |
| claim_boundary | `audit_template_generated` | 3 | 3 | 0 | True |
| claim_boundary | `automatic_evidence_promotion` | 3 | 0 | 3 | False |
| claim_boundary | `conceptual_or_normative` | 3 | 3 | 0 | True |
| claim_boundary | `native_empirical_experiment` | 3 | 0 | 3 | False |
| claim_boundary | `phenomenal_claim_identified` | 3 | 0 | 3 | False |
| claim_boundary | `scientific_evidence` | 3 | 0 | 3 | False |
| claim_boundary | `snn_involved` | 3 | 0 | 3 | False |
| measurement_limit | `audit_complete` | 3 | 0 | 3 | False |
| measurement_limit | `audit_template_generated` | 3 | 3 | 0 | True |
| measurement_limit | `automatic_evidence_promotion` | 3 | 0 | 3 | False |
| measurement_limit | `conceptual_or_normative` | 3 | 3 | 0 | True |
| measurement_limit | `native_empirical_experiment` | 3 | 0 | 3 | False |
| measurement_limit | `phenomenal_claim_identified` | 3 | 0 | 3 | False |
| measurement_limit | `scientific_evidence` | 3 | 0 | 3 | False |
| measurement_limit | `snn_involved` | 3 | 0 | 3 | False |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 101 | assumption_explicit | — | — | — | — | — | — | — |
| 101 | alternative_model | — | — | — | — | — | — | — |
| 101 | measurement_limit | — | — | — | — | — | — | — |
| 101 | claim_boundary | — | — | — | — | — | — | — |
| 102 | assumption_explicit | — | — | — | — | — | — | — |
| 102 | alternative_model | — | — | — | — | — | — | — |
| 102 | measurement_limit | — | — | — | — | — | — | — |
| 102 | claim_boundary | — | — | — | — | — | — | — |
| 103 | assumption_explicit | — | — | — | — | — | — | — |
| 103 | alternative_model | — | — | — | — | — | — | — |
| 103 | measurement_limit | — | — | — | — | — | — | — |
| 103 | claim_boundary | — | — | — | — | — | — | — |

## 7. Reproduzierbarkeit und Provenienz

Identische Ausgaben ueber mehrere Seeds dokumentieren reproduzierbare Modelltrajektorien unter diesen Bedingungen. Sie sind nicht automatisch statistisch unabhaengige Replikate. State-Digests sind Integritaets-/Identitaetsmarker und keine metrischen Zustandsabstaende.

Deterministische Statistikdatei: `analysis/statistics.json`

## 8. AI Research Report

- AIRR Status: `unavailable`
- Wissenschaftliche Evidenz durch KI: `false`
- Human Review: `PENDING`

## 9. Artefakte

- `analysis/ai_packet.json`
- `analysis/ai_packet_digest.json`
- `analysis/statistics.json`
- `DATA/current_run.json`
- `DATA/raw/run-0000-assumption_explicit-seed-101.json.gz`
- `DATA/raw/run-0001-alternative_model-seed-101.json.gz`
- `DATA/raw/run-0002-measurement_limit-seed-101.json.gz`
- `DATA/raw/run-0003-claim_boundary-seed-101.json.gz`
- `DATA/raw/run-0004-assumption_explicit-seed-102.json.gz`
- `DATA/raw/run-0005-alternative_model-seed-102.json.gz`
- `DATA/raw/run-0006-measurement_limit-seed-102.json.gz`
- `DATA/raw/run-0007-claim_boundary-seed-102.json.gz`
- `DATA/raw/run-0008-assumption_explicit-seed-103.json.gz`
- `DATA/raw/run-0009-alternative_model-seed-103.json.gz`
- `DATA/raw/run-0010-measurement_limit-seed-103.json.gz`
- `DATA/raw/run-0011-claim_boundary-seed-103.json.gz`
- `DATA/runs_compact.json`
- `DATA/runs_index.json`
- `manifest.json`
- `report.md`
- `review_request.json`
- `workflow.json`

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `NOT_APPLICABLE`, semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
