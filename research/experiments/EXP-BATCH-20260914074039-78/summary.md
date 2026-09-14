# EXP-BATCH-20260914074039-78: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-EVAL-001`
- Hypothese: `H-EVAL-001-A`
- Protokoll: `dimensional_connectivity_v1`
- Durchlaeufe: `130`
- Seeds: `[20001, 20002, 20003, 20004, 20005, 20006, 20007, 20008, 20009, 20010]`
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
- Beobachtete Conditions: `fixed_graph_label_2d, fixed_graph_label_3d, fixed_graph_label_4d, fixed_graph_label_5d, fixed_graph_label_6d, fixed_graph_label_8d, geometry_2d, geometry_3d, geometry_4d, geometry_5d, geometry_6d, geometry_8d, random_graph`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Experiment workflow: dimensional_connectivity_v1
- Bedingungen: Registered protocol conditions
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `8e096931a779b2d2eb4d010eb20154150b07bbf2`
- Git dirty: `True`
- Runtime: `11.050001099996734` s

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
| fixed_graph_label_2d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1160.1 | — | — | — | — |
| fixed_graph_label_3d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1160.1 | — | — | — | — |
| fixed_graph_label_4d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1160.1 | — | — | — | — |
| fixed_graph_label_5d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1160.1 | — | — | — | — |
| fixed_graph_label_6d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1160.1 | — | — | — | — |
| fixed_graph_label_8d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1160.1 | — | — | — | — |
| geometry_2d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1245.6 | — | — | — | — |
| geometry_3d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1229.6 | — | — | — | — |
| geometry_4d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1163.8 | — | — | — | — |
| geometry_5d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1160.1 | — | — | — | — |
| geometry_6d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1160.9 | — | — | — | — |
| geometry_8d | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1101.7 | — | — | — | — |
| random_graph | 10 | 20001,20002,20003,20004,20005,20006,20007,20008,20009,20010 | 256 | 1150.2 | — | — | — | — |

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 20001 | geometry_2d | 256 | 1220 | — | — | — | — | — |
| 20001 | geometry_3d | 256 | 1269 | — | — | — | — | — |
| 20001 | geometry_4d | 256 | 1143 | — | — | — | — | — |
| 20001 | geometry_5d | 256 | 1153 | — | — | — | — | — |
| 20001 | geometry_6d | 256 | 1238 | — | — | — | — | — |
| 20001 | geometry_8d | 256 | 1124 | — | — | — | — | — |
| 20001 | fixed_graph_label_2d | 256 | 1153 | — | — | — | — | — |
| 20001 | fixed_graph_label_3d | 256 | 1153 | — | — | — | — | — |
| 20001 | fixed_graph_label_4d | 256 | 1153 | — | — | — | — | — |
| 20001 | fixed_graph_label_5d | 256 | 1153 | — | — | — | — | — |
| 20001 | fixed_graph_label_6d | 256 | 1153 | — | — | — | — | — |
| 20001 | fixed_graph_label_8d | 256 | 1153 | — | — | — | — | — |
| 20001 | random_graph | 256 | 1307 | — | — | — | — | — |
| 20002 | geometry_2d | 256 | 1263 | — | — | — | — | — |
| 20002 | geometry_3d | 256 | 1250 | — | — | — | — | — |
| 20002 | geometry_4d | 256 | 1130 | — | — | — | — | — |
| 20002 | geometry_5d | 256 | 1185 | — | — | — | — | — |
| 20002 | geometry_6d | 256 | 1214 | — | — | — | — | — |
| 20002 | geometry_8d | 256 | 1123 | — | — | — | — | — |
| 20002 | fixed_graph_label_2d | 256 | 1185 | — | — | — | — | — |
| 20002 | fixed_graph_label_3d | 256 | 1185 | — | — | — | — | — |
| 20002 | fixed_graph_label_4d | 256 | 1185 | — | — | — | — | — |
| 20002 | fixed_graph_label_5d | 256 | 1185 | — | — | — | — | — |
| 20002 | fixed_graph_label_6d | 256 | 1185 | — | — | — | — | — |
| 20002 | fixed_graph_label_8d | 256 | 1185 | — | — | — | — | — |
| 20002 | random_graph | 256 | 784 | — | — | — | — | — |
| 20003 | geometry_2d | 256 | 1304 | — | — | — | — | — |
| 20003 | geometry_3d | 256 | 1260 | — | — | — | — | — |
| 20003 | geometry_4d | 256 | 1172 | — | — | — | — | — |
| 20003 | geometry_5d | 256 | 1144 | — | — | — | — | — |
| 20003 | geometry_6d | 256 | 1169 | — | — | — | — | — |
| 20003 | geometry_8d | 256 | 1127 | — | — | — | — | — |
| 20003 | fixed_graph_label_2d | 256 | 1144 | — | — | — | — | — |
| 20003 | fixed_graph_label_3d | 256 | 1144 | — | — | — | — | — |
| 20003 | fixed_graph_label_4d | 256 | 1144 | — | — | — | — | — |
| 20003 | fixed_graph_label_5d | 256 | 1144 | — | — | — | — | — |
| 20003 | fixed_graph_label_6d | 256 | 1144 | — | — | — | — | — |
| 20003 | fixed_graph_label_8d | 256 | 1144 | — | — | — | — | — |
| 20003 | random_graph | 256 | 753 | — | — | — | — | — |
| 20004 | geometry_2d | 256 | 1301 | — | — | — | — | — |
| 20004 | geometry_3d | 256 | 1253 | — | — | — | — | — |
| 20004 | geometry_4d | 256 | 1111 | — | — | — | — | — |
| 20004 | geometry_5d | 256 | 1165 | — | — | — | — | — |
| 20004 | geometry_6d | 256 | 1157 | — | — | — | — | — |
| 20004 | geometry_8d | 256 | 1072 | — | — | — | — | — |
| 20004 | fixed_graph_label_2d | 256 | 1165 | — | — | — | — | — |
| 20004 | fixed_graph_label_3d | 256 | 1165 | — | — | — | — | — |
| 20004 | fixed_graph_label_4d | 256 | 1165 | — | — | — | — | — |
| 20004 | fixed_graph_label_5d | 256 | 1165 | — | — | — | — | — |
| 20004 | fixed_graph_label_6d | 256 | 1165 | — | — | — | — | — |
| 20004 | fixed_graph_label_8d | 256 | 1165 | — | — | — | — | — |
| 20004 | random_graph | 256 | 787 | — | — | — | — | — |
| 20005 | geometry_2d | 256 | 1267 | — | — | — | — | — |
| 20005 | geometry_3d | 256 | 1190 | — | — | — | — | — |
| 20005 | geometry_4d | 256 | 1199 | — | — | — | — | — |
| 20005 | geometry_5d | 256 | 1151 | — | — | — | — | — |
| 20005 | geometry_6d | 256 | 1137 | — | — | — | — | — |
| 20005 | geometry_8d | 256 | 1100 | — | — | — | — | — |
| 20005 | fixed_graph_label_2d | 256 | 1151 | — | — | — | — | — |
| 20005 | fixed_graph_label_3d | 256 | 1151 | — | — | — | — | — |
| 20005 | fixed_graph_label_4d | 256 | 1151 | — | — | — | — | — |
| 20005 | fixed_graph_label_5d | 256 | 1151 | — | — | — | — | — |
| 20005 | fixed_graph_label_6d | 256 | 1151 | — | — | — | — | — |
| 20005 | fixed_graph_label_8d | 256 | 1151 | — | — | — | — | — |
| 20005 | random_graph | 256 | 1310 | — | — | — | — | — |
| 20006 | geometry_2d | 256 | 1211 | — | — | — | — | — |
| 20006 | geometry_3d | 256 | 1271 | — | — | — | — | — |
| 20006 | geometry_4d | 256 | 1169 | — | — | — | — | — |
| 20006 | geometry_5d | 256 | 1143 | — | — | — | — | — |
| 20006 | geometry_6d | 256 | 1215 | — | — | — | — | — |
| 20006 | geometry_8d | 256 | 1061 | — | — | — | — | — |
| 20006 | fixed_graph_label_2d | 256 | 1143 | — | — | — | — | — |
| 20006 | fixed_graph_label_3d | 256 | 1143 | — | — | — | — | — |
| 20006 | fixed_graph_label_4d | 256 | 1143 | — | — | — | — | — |
| 20006 | fixed_graph_label_5d | 256 | 1143 | — | — | — | — | — |
| 20006 | fixed_graph_label_6d | 256 | 1143 | — | — | — | — | — |
| 20006 | fixed_graph_label_8d | 256 | 1143 | — | — | — | — | — |
| 20006 | random_graph | 256 | 1301 | — | — | — | — | — |
| 20007 | geometry_2d | 256 | 1343 | — | — | — | — | — |
| 20007 | geometry_3d | 256 | 1190 | — | — | — | — | — |
| 20007 | geometry_4d | 256 | 1171 | — | — | — | — | — |
| 20007 | geometry_5d | 256 | 1127 | — | — | — | — | — |
| 20007 | geometry_6d | 256 | 1056 | — | — | — | — | — |
| 20007 | geometry_8d | 256 | 1149 | — | — | — | — | — |
| 20007 | fixed_graph_label_2d | 256 | 1127 | — | — | — | — | — |
| 20007 | fixed_graph_label_3d | 256 | 1127 | — | — | — | — | — |
| 20007 | fixed_graph_label_4d | 256 | 1127 | — | — | — | — | — |
| 20007 | fixed_graph_label_5d | 256 | 1127 | — | — | — | — | — |
| 20007 | fixed_graph_label_6d | 256 | 1127 | — | — | — | — | — |
| 20007 | fixed_graph_label_8d | 256 | 1127 | — | — | — | — | — |
| 20007 | random_graph | 256 | 1309 | — | — | — | — | — |
| 20008 | geometry_2d | 256 | 1209 | — | — | — | — | — |
| 20008 | geometry_3d | 256 | 1185 | — | — | — | — | — |
| 20008 | geometry_4d | 256 | 1156 | — | — | — | — | — |
| 20008 | geometry_5d | 256 | 1096 | — | — | — | — | — |
| 20008 | geometry_6d | 256 | 1107 | — | — | — | — | — |
| 20008 | geometry_8d | 256 | 994 | — | — | — | — | — |
| 20008 | fixed_graph_label_2d | 256 | 1096 | — | — | — | — | — |
| 20008 | fixed_graph_label_3d | 256 | 1096 | — | — | — | — | — |
| 20008 | fixed_graph_label_4d | 256 | 1096 | — | — | — | — | — |
| 20008 | fixed_graph_label_5d | 256 | 1096 | — | — | — | — | — |
| 20008 | fixed_graph_label_6d | 256 | 1096 | — | — | — | — | — |
| 20008 | fixed_graph_label_8d | 256 | 1096 | — | — | — | — | — |
| 20008 | random_graph | 256 | 1337 | — | — | — | — | — |
| 20009 | geometry_2d | 256 | 1296 | — | — | — | — | — |
| 20009 | geometry_3d | 256 | 1210 | — | — | — | — | — |
| 20009 | geometry_4d | 256 | 1191 | — | — | — | — | — |
| 20009 | geometry_5d | 256 | 1222 | — | — | — | — | — |
| 20009 | geometry_6d | 256 | 1238 | — | — | — | — | — |
| 20009 | geometry_8d | 256 | 1219 | — | — | — | — | — |
| 20009 | fixed_graph_label_2d | 256 | 1222 | — | — | — | — | — |
| 20009 | fixed_graph_label_3d | 256 | 1222 | — | — | — | — | — |
| 20009 | fixed_graph_label_4d | 256 | 1222 | — | — | — | — | — |
| 20009 | fixed_graph_label_5d | 256 | 1222 | — | — | — | — | — |
| 20009 | fixed_graph_label_6d | 256 | 1222 | — | — | — | — | — |
| 20009 | fixed_graph_label_8d | 256 | 1222 | — | — | — | — | — |
| 20009 | random_graph | 256 | 1336 | — | — | — | — | — |
| 20010 | geometry_2d | 256 | 1042 | — | — | — | — | — |
| 20010 | geometry_3d | 256 | 1218 | — | — | — | — | — |
| 20010 | geometry_4d | 256 | 1196 | — | — | — | — | — |
| 20010 | geometry_5d | 256 | 1215 | — | — | — | — | — |
| 20010 | geometry_6d | 256 | 1078 | — | — | — | — | — |
| 20010 | geometry_8d | 256 | 1048 | — | — | — | — | — |
| 20010 | fixed_graph_label_2d | 256 | 1215 | — | — | — | — | — |
| 20010 | fixed_graph_label_3d | 256 | 1215 | — | — | — | — | — |
| 20010 | fixed_graph_label_4d | 256 | 1215 | — | — | — | — | — |
| 20010 | fixed_graph_label_5d | 256 | 1215 | — | — | — | — | — |
| 20010 | fixed_graph_label_6d | 256 | 1215 | — | — | — | — | — |
| 20010 | fixed_graph_label_8d | 256 | 1215 | — | — | — | — | — |
| 20010 | random_graph | 256 | 1278 | — | — | — | — | — |

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

Die Rolle scientific_writer konnte nicht ausgeführt werden. Es liegt keine schema-konforme Modellanalyse vor.

KI-Konfidenz: `0.0` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- AI analysis unavailable; deterministic experiment artifacts remain the authoritative data basis.
- Technical reason: ValueError: Invalid AI analysis output field: assessment

### Alternative Erklaerungen

- Keine expliziten Angaben.

### Fehlende Nachweise

- Run the role again with a schema-conforming backend response.
- Complete mandatory human review before interpreting this report.

### Empfohlene Folgeexperimente

- Keine expliziten Folgeexperimente im AIRR angegeben.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260914085415712755-a9e30786.json](analysis/AIAR-critical_reviewer-20260914085415712755-a9e30786.json)
- [analysis/AIAR-scientific_analyst-20260914085342834259-a9e30786.json](analysis/AIAR-scientific_analyst-20260914085342834259-a9e30786.json)
- [analysis/AIAR-scientific_writer-20260914085448668555-a9e30786.json](analysis/AIAR-scientific_writer-20260914085448668555-a9e30786.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-geometry_2d-seed-20001.json.gz](DATA/raw/run-0000-geometry_2d-seed-20001.json.gz)
- [DATA/raw/run-0001-geometry_3d-seed-20001.json.gz](DATA/raw/run-0001-geometry_3d-seed-20001.json.gz)
- [DATA/raw/run-0002-geometry_4d-seed-20001.json.gz](DATA/raw/run-0002-geometry_4d-seed-20001.json.gz)
- [DATA/raw/run-0003-geometry_5d-seed-20001.json.gz](DATA/raw/run-0003-geometry_5d-seed-20001.json.gz)
- [DATA/raw/run-0004-geometry_6d-seed-20001.json.gz](DATA/raw/run-0004-geometry_6d-seed-20001.json.gz)
- [DATA/raw/run-0005-geometry_8d-seed-20001.json.gz](DATA/raw/run-0005-geometry_8d-seed-20001.json.gz)
- [DATA/raw/run-0006-fixed_graph_label_2d-seed-20001.json.gz](DATA/raw/run-0006-fixed_graph_label_2d-seed-20001.json.gz)
- [DATA/raw/run-0007-fixed_graph_label_3d-seed-20001.json.gz](DATA/raw/run-0007-fixed_graph_label_3d-seed-20001.json.gz)
- [DATA/raw/run-0008-fixed_graph_label_4d-seed-20001.json.gz](DATA/raw/run-0008-fixed_graph_label_4d-seed-20001.json.gz)
- [DATA/raw/run-0009-fixed_graph_label_5d-seed-20001.json.gz](DATA/raw/run-0009-fixed_graph_label_5d-seed-20001.json.gz)
- [DATA/raw/run-0010-fixed_graph_label_6d-seed-20001.json.gz](DATA/raw/run-0010-fixed_graph_label_6d-seed-20001.json.gz)
- [DATA/raw/run-0011-fixed_graph_label_8d-seed-20001.json.gz](DATA/raw/run-0011-fixed_graph_label_8d-seed-20001.json.gz)
- [DATA/raw/run-0012-random_graph-seed-20001.json.gz](DATA/raw/run-0012-random_graph-seed-20001.json.gz)
- [DATA/raw/run-0013-geometry_2d-seed-20002.json.gz](DATA/raw/run-0013-geometry_2d-seed-20002.json.gz)
- [DATA/raw/run-0014-geometry_3d-seed-20002.json.gz](DATA/raw/run-0014-geometry_3d-seed-20002.json.gz)
- [DATA/raw/run-0015-geometry_4d-seed-20002.json.gz](DATA/raw/run-0015-geometry_4d-seed-20002.json.gz)
- [DATA/raw/run-0016-geometry_5d-seed-20002.json.gz](DATA/raw/run-0016-geometry_5d-seed-20002.json.gz)
- [DATA/raw/run-0017-geometry_6d-seed-20002.json.gz](DATA/raw/run-0017-geometry_6d-seed-20002.json.gz)
- [DATA/raw/run-0018-geometry_8d-seed-20002.json.gz](DATA/raw/run-0018-geometry_8d-seed-20002.json.gz)
- [DATA/raw/run-0019-fixed_graph_label_2d-seed-20002.json.gz](DATA/raw/run-0019-fixed_graph_label_2d-seed-20002.json.gz)
- [DATA/raw/run-0020-fixed_graph_label_3d-seed-20002.json.gz](DATA/raw/run-0020-fixed_graph_label_3d-seed-20002.json.gz)
- [DATA/raw/run-0021-fixed_graph_label_4d-seed-20002.json.gz](DATA/raw/run-0021-fixed_graph_label_4d-seed-20002.json.gz)
- [DATA/raw/run-0022-fixed_graph_label_5d-seed-20002.json.gz](DATA/raw/run-0022-fixed_graph_label_5d-seed-20002.json.gz)
- [DATA/raw/run-0023-fixed_graph_label_6d-seed-20002.json.gz](DATA/raw/run-0023-fixed_graph_label_6d-seed-20002.json.gz)
- [DATA/raw/run-0024-fixed_graph_label_8d-seed-20002.json.gz](DATA/raw/run-0024-fixed_graph_label_8d-seed-20002.json.gz)
- [DATA/raw/run-0025-random_graph-seed-20002.json.gz](DATA/raw/run-0025-random_graph-seed-20002.json.gz)
- [DATA/raw/run-0026-geometry_2d-seed-20003.json.gz](DATA/raw/run-0026-geometry_2d-seed-20003.json.gz)
- [DATA/raw/run-0027-geometry_3d-seed-20003.json.gz](DATA/raw/run-0027-geometry_3d-seed-20003.json.gz)
- [DATA/raw/run-0028-geometry_4d-seed-20003.json.gz](DATA/raw/run-0028-geometry_4d-seed-20003.json.gz)
- [DATA/raw/run-0029-geometry_5d-seed-20003.json.gz](DATA/raw/run-0029-geometry_5d-seed-20003.json.gz)
- [DATA/raw/run-0030-geometry_6d-seed-20003.json.gz](DATA/raw/run-0030-geometry_6d-seed-20003.json.gz)
- [DATA/raw/run-0031-geometry_8d-seed-20003.json.gz](DATA/raw/run-0031-geometry_8d-seed-20003.json.gz)
- [DATA/raw/run-0032-fixed_graph_label_2d-seed-20003.json.gz](DATA/raw/run-0032-fixed_graph_label_2d-seed-20003.json.gz)
- [DATA/raw/run-0033-fixed_graph_label_3d-seed-20003.json.gz](DATA/raw/run-0033-fixed_graph_label_3d-seed-20003.json.gz)
- [DATA/raw/run-0034-fixed_graph_label_4d-seed-20003.json.gz](DATA/raw/run-0034-fixed_graph_label_4d-seed-20003.json.gz)
- [DATA/raw/run-0035-fixed_graph_label_5d-seed-20003.json.gz](DATA/raw/run-0035-fixed_graph_label_5d-seed-20003.json.gz)
- [DATA/raw/run-0036-fixed_graph_label_6d-seed-20003.json.gz](DATA/raw/run-0036-fixed_graph_label_6d-seed-20003.json.gz)
- [DATA/raw/run-0037-fixed_graph_label_8d-seed-20003.json.gz](DATA/raw/run-0037-fixed_graph_label_8d-seed-20003.json.gz)
- [DATA/raw/run-0038-random_graph-seed-20003.json.gz](DATA/raw/run-0038-random_graph-seed-20003.json.gz)
- [DATA/raw/run-0039-geometry_2d-seed-20004.json.gz](DATA/raw/run-0039-geometry_2d-seed-20004.json.gz)
- [DATA/raw/run-0040-geometry_3d-seed-20004.json.gz](DATA/raw/run-0040-geometry_3d-seed-20004.json.gz)
- [DATA/raw/run-0041-geometry_4d-seed-20004.json.gz](DATA/raw/run-0041-geometry_4d-seed-20004.json.gz)
- [DATA/raw/run-0042-geometry_5d-seed-20004.json.gz](DATA/raw/run-0042-geometry_5d-seed-20004.json.gz)
- [DATA/raw/run-0043-geometry_6d-seed-20004.json.gz](DATA/raw/run-0043-geometry_6d-seed-20004.json.gz)
- [DATA/raw/run-0044-geometry_8d-seed-20004.json.gz](DATA/raw/run-0044-geometry_8d-seed-20004.json.gz)
- [DATA/raw/run-0045-fixed_graph_label_2d-seed-20004.json.gz](DATA/raw/run-0045-fixed_graph_label_2d-seed-20004.json.gz)
- [DATA/raw/run-0046-fixed_graph_label_3d-seed-20004.json.gz](DATA/raw/run-0046-fixed_graph_label_3d-seed-20004.json.gz)
- [DATA/raw/run-0047-fixed_graph_label_4d-seed-20004.json.gz](DATA/raw/run-0047-fixed_graph_label_4d-seed-20004.json.gz)
- [DATA/raw/run-0048-fixed_graph_label_5d-seed-20004.json.gz](DATA/raw/run-0048-fixed_graph_label_5d-seed-20004.json.gz)
- [DATA/raw/run-0049-fixed_graph_label_6d-seed-20004.json.gz](DATA/raw/run-0049-fixed_graph_label_6d-seed-20004.json.gz)
- [DATA/raw/run-0050-fixed_graph_label_8d-seed-20004.json.gz](DATA/raw/run-0050-fixed_graph_label_8d-seed-20004.json.gz)
- [DATA/raw/run-0051-random_graph-seed-20004.json.gz](DATA/raw/run-0051-random_graph-seed-20004.json.gz)
- [DATA/raw/run-0052-geometry_2d-seed-20005.json.gz](DATA/raw/run-0052-geometry_2d-seed-20005.json.gz)
- [DATA/raw/run-0053-geometry_3d-seed-20005.json.gz](DATA/raw/run-0053-geometry_3d-seed-20005.json.gz)
- [DATA/raw/run-0054-geometry_4d-seed-20005.json.gz](DATA/raw/run-0054-geometry_4d-seed-20005.json.gz)
- [DATA/raw/run-0055-geometry_5d-seed-20005.json.gz](DATA/raw/run-0055-geometry_5d-seed-20005.json.gz)
- [DATA/raw/run-0056-geometry_6d-seed-20005.json.gz](DATA/raw/run-0056-geometry_6d-seed-20005.json.gz)
- [DATA/raw/run-0057-geometry_8d-seed-20005.json.gz](DATA/raw/run-0057-geometry_8d-seed-20005.json.gz)
- [DATA/raw/run-0058-fixed_graph_label_2d-seed-20005.json.gz](DATA/raw/run-0058-fixed_graph_label_2d-seed-20005.json.gz)
- [DATA/raw/run-0059-fixed_graph_label_3d-seed-20005.json.gz](DATA/raw/run-0059-fixed_graph_label_3d-seed-20005.json.gz)
- [DATA/raw/run-0060-fixed_graph_label_4d-seed-20005.json.gz](DATA/raw/run-0060-fixed_graph_label_4d-seed-20005.json.gz)
- [DATA/raw/run-0061-fixed_graph_label_5d-seed-20005.json.gz](DATA/raw/run-0061-fixed_graph_label_5d-seed-20005.json.gz)
- [DATA/raw/run-0062-fixed_graph_label_6d-seed-20005.json.gz](DATA/raw/run-0062-fixed_graph_label_6d-seed-20005.json.gz)
- [DATA/raw/run-0063-fixed_graph_label_8d-seed-20005.json.gz](DATA/raw/run-0063-fixed_graph_label_8d-seed-20005.json.gz)
- [DATA/raw/run-0064-random_graph-seed-20005.json.gz](DATA/raw/run-0064-random_graph-seed-20005.json.gz)
- [DATA/raw/run-0065-geometry_2d-seed-20006.json.gz](DATA/raw/run-0065-geometry_2d-seed-20006.json.gz)
- [DATA/raw/run-0066-geometry_3d-seed-20006.json.gz](DATA/raw/run-0066-geometry_3d-seed-20006.json.gz)
- [DATA/raw/run-0067-geometry_4d-seed-20006.json.gz](DATA/raw/run-0067-geometry_4d-seed-20006.json.gz)
- [DATA/raw/run-0068-geometry_5d-seed-20006.json.gz](DATA/raw/run-0068-geometry_5d-seed-20006.json.gz)
- [DATA/raw/run-0069-geometry_6d-seed-20006.json.gz](DATA/raw/run-0069-geometry_6d-seed-20006.json.gz)
- [DATA/raw/run-0070-geometry_8d-seed-20006.json.gz](DATA/raw/run-0070-geometry_8d-seed-20006.json.gz)
- [DATA/raw/run-0071-fixed_graph_label_2d-seed-20006.json.gz](DATA/raw/run-0071-fixed_graph_label_2d-seed-20006.json.gz)
- [DATA/raw/run-0072-fixed_graph_label_3d-seed-20006.json.gz](DATA/raw/run-0072-fixed_graph_label_3d-seed-20006.json.gz)
- [DATA/raw/run-0073-fixed_graph_label_4d-seed-20006.json.gz](DATA/raw/run-0073-fixed_graph_label_4d-seed-20006.json.gz)
- [DATA/raw/run-0074-fixed_graph_label_5d-seed-20006.json.gz](DATA/raw/run-0074-fixed_graph_label_5d-seed-20006.json.gz)
- [DATA/raw/run-0075-fixed_graph_label_6d-seed-20006.json.gz](DATA/raw/run-0075-fixed_graph_label_6d-seed-20006.json.gz)
- [DATA/raw/run-0076-fixed_graph_label_8d-seed-20006.json.gz](DATA/raw/run-0076-fixed_graph_label_8d-seed-20006.json.gz)
- [DATA/raw/run-0077-random_graph-seed-20006.json.gz](DATA/raw/run-0077-random_graph-seed-20006.json.gz)
- [DATA/raw/run-0078-geometry_2d-seed-20007.json.gz](DATA/raw/run-0078-geometry_2d-seed-20007.json.gz)
- [DATA/raw/run-0079-geometry_3d-seed-20007.json.gz](DATA/raw/run-0079-geometry_3d-seed-20007.json.gz)
- [DATA/raw/run-0080-geometry_4d-seed-20007.json.gz](DATA/raw/run-0080-geometry_4d-seed-20007.json.gz)
- [DATA/raw/run-0081-geometry_5d-seed-20007.json.gz](DATA/raw/run-0081-geometry_5d-seed-20007.json.gz)
- [DATA/raw/run-0082-geometry_6d-seed-20007.json.gz](DATA/raw/run-0082-geometry_6d-seed-20007.json.gz)
- [DATA/raw/run-0083-geometry_8d-seed-20007.json.gz](DATA/raw/run-0083-geometry_8d-seed-20007.json.gz)
- [DATA/raw/run-0084-fixed_graph_label_2d-seed-20007.json.gz](DATA/raw/run-0084-fixed_graph_label_2d-seed-20007.json.gz)
- [DATA/raw/run-0085-fixed_graph_label_3d-seed-20007.json.gz](DATA/raw/run-0085-fixed_graph_label_3d-seed-20007.json.gz)
- [DATA/raw/run-0086-fixed_graph_label_4d-seed-20007.json.gz](DATA/raw/run-0086-fixed_graph_label_4d-seed-20007.json.gz)
- [DATA/raw/run-0087-fixed_graph_label_5d-seed-20007.json.gz](DATA/raw/run-0087-fixed_graph_label_5d-seed-20007.json.gz)
- [DATA/raw/run-0088-fixed_graph_label_6d-seed-20007.json.gz](DATA/raw/run-0088-fixed_graph_label_6d-seed-20007.json.gz)
- [DATA/raw/run-0089-fixed_graph_label_8d-seed-20007.json.gz](DATA/raw/run-0089-fixed_graph_label_8d-seed-20007.json.gz)
- [DATA/raw/run-0090-random_graph-seed-20007.json.gz](DATA/raw/run-0090-random_graph-seed-20007.json.gz)
- [DATA/raw/run-0091-geometry_2d-seed-20008.json.gz](DATA/raw/run-0091-geometry_2d-seed-20008.json.gz)
- [DATA/raw/run-0092-geometry_3d-seed-20008.json.gz](DATA/raw/run-0092-geometry_3d-seed-20008.json.gz)
- [DATA/raw/run-0093-geometry_4d-seed-20008.json.gz](DATA/raw/run-0093-geometry_4d-seed-20008.json.gz)
- [DATA/raw/run-0094-geometry_5d-seed-20008.json.gz](DATA/raw/run-0094-geometry_5d-seed-20008.json.gz)
- [DATA/raw/run-0095-geometry_6d-seed-20008.json.gz](DATA/raw/run-0095-geometry_6d-seed-20008.json.gz)
- [DATA/raw/run-0096-geometry_8d-seed-20008.json.gz](DATA/raw/run-0096-geometry_8d-seed-20008.json.gz)
- [DATA/raw/run-0097-fixed_graph_label_2d-seed-20008.json.gz](DATA/raw/run-0097-fixed_graph_label_2d-seed-20008.json.gz)
- [DATA/raw/run-0098-fixed_graph_label_3d-seed-20008.json.gz](DATA/raw/run-0098-fixed_graph_label_3d-seed-20008.json.gz)
- [DATA/raw/run-0099-fixed_graph_label_4d-seed-20008.json.gz](DATA/raw/run-0099-fixed_graph_label_4d-seed-20008.json.gz)
- [DATA/raw/run-0100-fixed_graph_label_5d-seed-20008.json.gz](DATA/raw/run-0100-fixed_graph_label_5d-seed-20008.json.gz)
- [DATA/raw/run-0101-fixed_graph_label_6d-seed-20008.json.gz](DATA/raw/run-0101-fixed_graph_label_6d-seed-20008.json.gz)
- [DATA/raw/run-0102-fixed_graph_label_8d-seed-20008.json.gz](DATA/raw/run-0102-fixed_graph_label_8d-seed-20008.json.gz)
- [DATA/raw/run-0103-random_graph-seed-20008.json.gz](DATA/raw/run-0103-random_graph-seed-20008.json.gz)
- [DATA/raw/run-0104-geometry_2d-seed-20009.json.gz](DATA/raw/run-0104-geometry_2d-seed-20009.json.gz)
- [DATA/raw/run-0105-geometry_3d-seed-20009.json.gz](DATA/raw/run-0105-geometry_3d-seed-20009.json.gz)
- [DATA/raw/run-0106-geometry_4d-seed-20009.json.gz](DATA/raw/run-0106-geometry_4d-seed-20009.json.gz)
- [DATA/raw/run-0107-geometry_5d-seed-20009.json.gz](DATA/raw/run-0107-geometry_5d-seed-20009.json.gz)
- [DATA/raw/run-0108-geometry_6d-seed-20009.json.gz](DATA/raw/run-0108-geometry_6d-seed-20009.json.gz)
- [DATA/raw/run-0109-geometry_8d-seed-20009.json.gz](DATA/raw/run-0109-geometry_8d-seed-20009.json.gz)
- [DATA/raw/run-0110-fixed_graph_label_2d-seed-20009.json.gz](DATA/raw/run-0110-fixed_graph_label_2d-seed-20009.json.gz)
- [DATA/raw/run-0111-fixed_graph_label_3d-seed-20009.json.gz](DATA/raw/run-0111-fixed_graph_label_3d-seed-20009.json.gz)
- [DATA/raw/run-0112-fixed_graph_label_4d-seed-20009.json.gz](DATA/raw/run-0112-fixed_graph_label_4d-seed-20009.json.gz)
- [DATA/raw/run-0113-fixed_graph_label_5d-seed-20009.json.gz](DATA/raw/run-0113-fixed_graph_label_5d-seed-20009.json.gz)
- [DATA/raw/run-0114-fixed_graph_label_6d-seed-20009.json.gz](DATA/raw/run-0114-fixed_graph_label_6d-seed-20009.json.gz)
- [DATA/raw/run-0115-fixed_graph_label_8d-seed-20009.json.gz](DATA/raw/run-0115-fixed_graph_label_8d-seed-20009.json.gz)
- [DATA/raw/run-0116-random_graph-seed-20009.json.gz](DATA/raw/run-0116-random_graph-seed-20009.json.gz)
- [DATA/raw/run-0117-geometry_2d-seed-20010.json.gz](DATA/raw/run-0117-geometry_2d-seed-20010.json.gz)
- [DATA/raw/run-0118-geometry_3d-seed-20010.json.gz](DATA/raw/run-0118-geometry_3d-seed-20010.json.gz)
- [DATA/raw/run-0119-geometry_4d-seed-20010.json.gz](DATA/raw/run-0119-geometry_4d-seed-20010.json.gz)
- [DATA/raw/run-0120-geometry_5d-seed-20010.json.gz](DATA/raw/run-0120-geometry_5d-seed-20010.json.gz)
- [DATA/raw/run-0121-geometry_6d-seed-20010.json.gz](DATA/raw/run-0121-geometry_6d-seed-20010.json.gz)
- [DATA/raw/run-0122-geometry_8d-seed-20010.json.gz](DATA/raw/run-0122-geometry_8d-seed-20010.json.gz)
- [DATA/raw/run-0123-fixed_graph_label_2d-seed-20010.json.gz](DATA/raw/run-0123-fixed_graph_label_2d-seed-20010.json.gz)
- [DATA/raw/run-0124-fixed_graph_label_3d-seed-20010.json.gz](DATA/raw/run-0124-fixed_graph_label_3d-seed-20010.json.gz)
- [DATA/raw/run-0125-fixed_graph_label_4d-seed-20010.json.gz](DATA/raw/run-0125-fixed_graph_label_4d-seed-20010.json.gz)
- [DATA/raw/run-0126-fixed_graph_label_5d-seed-20010.json.gz](DATA/raw/run-0126-fixed_graph_label_5d-seed-20010.json.gz)
- [DATA/raw/run-0127-fixed_graph_label_6d-seed-20010.json.gz](DATA/raw/run-0127-fixed_graph_label_6d-seed-20010.json.gz)
- [DATA/raw/run-0128-fixed_graph_label_8d-seed-20010.json.gz](DATA/raw/run-0128-fixed_graph_label_8d-seed-20010.json.gz)
- [DATA/raw/run-0129-random_graph-seed-20010.json.gz](DATA/raw/run-0129-random_graph-seed-20010.json.gz)
- [DATA/runs.json](DATA/runs.json)
- [DATA/runs_index.json](DATA/runs_index.json)
- [manifest.json](manifest.json)
- [report.md](report.md)
- [reports/AIRR-2026-0001.json](reports/AIRR-2026-0001.json)
- [reports/AIRR-2026-0001.md](reports/AIRR-2026-0001.md)
- [workflow.json](workflow.json)

## 10. Wissenschaftliche Grenze und Schlussfolgerung

Die technischen Laufdaten duerfen deskriptiv ausgewertet werden. Eine Hypothese gilt dadurch nicht automatisch als bestaetigt oder widerlegt. Kausale Aussagen sind nur fuer explizit kontrollierte Interventionen und nur innerhalb des simulierten Systems zulaessig; biologische Generalisierung erfordert zusaetzliche Evidenz. Die KI-Auswertung ist post-hoc und besitzt keine Evidenzfreigabe.

**Gesamtstatus:** technische Ausfuehrung `completed`, Tick-Vertrag `SATISFIED`, semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`, wissenschaftliche Evidenz `false` bis zur menschlichen Review/Freigabe.
