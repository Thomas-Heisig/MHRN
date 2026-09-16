# EXP-GEN-0036: Wissenschaftliche Zusammenfassung

Diese Zusammenfassung wird deterministisch aus Manifest, Workflow, DATA und — sofern vorhanden — dem AIRR aufgebaut. Zahlen und Formeln stammen aus den gespeicherten Laufdaten beziehungsweise dem deterministischen Statistics Engine; KI-Text bleibt davon getrennt.

## 1. Identifikation und Status

- Experimentstatus: `completed`
- Forschungsfrage: `RQ-SUITE-001`
- Hypothese: `H-SUITE-001-A`
- Protokoll: `science_all_v1`
- Durchlaeufe: `180`
- Seeds: `[42, 43, 44, 45, 46, 47, 48, 49, 50, 51]`
- Angeforderte Ticks: `1000`
- Tickgebundene SNN-Läufe (PING/TEMP/5D): `1000 .. 1000` ausgeführte Ticks
- Tick-Vertrag: `SATISFIED`
- TIME-Ladder: Der angeforderte Endpunkt wird je Seed separat validiert; Zwischenstufen duerfen kleiner sein.
- Trial-/Regulationsprotokolle: Interne Versuchszyklen sind nicht mit `ticks_executed` gleichzusetzen und werden nicht in die SNN-Tickspanne eingerechnet.
- Laufmodus: `EXPLORATORY`
- Netzwerkmodus: `OFFLINE`

## 2. Semantische Konsistenz

- RQ/Condition-Pruefung: `DIRECT_MATCH`
- Evidence Readiness: `DIAGNOSTIC_ONLY`
- Begründung: SUITE erwartet science_all_v1 und PING, TEMP, STDP, Learning, TIME, 5D sowie Regulation unter gemeinsamer Provenienz.
- Beobachtete Conditions: `5d:1d, 5d:2d, 5d:3d, 5d:5d, 5d:5d_shuffled, 5d:random_graph, learning:learning_off, learning:learning_on, learning:sham_replay, ping:recurrence_off, ping:recurrence_on, regulation:chronic_pressure, regulation:nominal, regulation:telemetry_unknown, stdp:productive_reward_stdp, temporal:fast_medium_slow, time:100, time:1000`

`DIRECT_MATCH` bezeichnet einen gezielten RQ-spezifischen Lauf. `CONTAINS_MATCH` bedeutet, dass die passende Teilstudie innerhalb einer Gesamtsuite enthalten ist; nur diese Teilstudie ist primaer fuer die registrierte RQ auszuwerten. `MISMATCH` blockiert die Nutzung als Evidenz fuer die registrierte Forschungsfrage, auch wenn die technische Ausfuehrung fehlerfrei war.

## 3. Ausfuehrungsparameter

- Titel: Complete science suite diagnostic
- Bedingungen: Seeds 42,43,44,45,46,47,48,49,50,51; all registered science-suite runners; grouped conditions and common provenance.
- Notizen: Keine.
- Konfiguration: `F:\Brain-5D\configs\learning_experiment.yaml`
- Config SHA-256: `6f6cd457caf6216c286fee47ef03b529a0b496ed2dd53ee96b85d3b51e7b3a1c`
- Git Commit: `d745cc47c2c6289f0ae38b06def82c5dd5045b93`
- Git dirty: `False`
- Runtime: `4.840055500040762` s

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
| 5d:1d | 10 | 42,43,44,45,46,47,48,49,50,51 | 1000 | 3 | 2 | 3 | 0 | 1 |
| 5d:2d | 10 | 42,43,44,45,46,47,48,49,50,51 | 1000 | 3 | 2 | 3 | 0 | 1 |
| 5d:3d | 10 | 42,43,44,45,46,47,48,49,50,51 | 1000 | 3 | 2 | 3 | 0 | 1 |
| 5d:5d | 10 | 42,43,44,45,46,47,48,49,50,51 | 1000 | 3 | 2 | 3 | 0 | 1 |
| 5d:5d_shuffled | 10 | 42,43,44,45,46,47,48,49,50,51 | 1000 | 3 | 2 | 3 | 0 | 1 |
| 5d:random_graph | 10 | 42,43,44,45,46,47,48,49,50,51 | 1000 | 3 | 2 | 3 | 0 | 1 |
| learning:learning_off | 10 | 42,43,44,45,46,47,48,49,50,51 | — | — | — | — | — | — |
| learning:learning_on | 10 | 42,43,44,45,46,47,48,49,50,51 | — | — | — | — | — | — |
| learning:sham_replay | 10 | 42,43,44,45,46,47,48,49,50,51 | — | — | — | — | — | — |
| ping:recurrence_off | 10 | 42,43,44,45,46,47,48,49,50,51 | 1000 | 3 | 2 | 3 | 0 | 1 |
| ping:recurrence_on | 10 | 42,43,44,45,46,47,48,49,50,51 | 1000 | 33 | 33 | 3 | 10 | 61 |
| regulation:chronic_pressure | 10 | 42,43,44,45,46,47,48,49,50,51 | — | — | — | — | — | — |
| regulation:nominal | 10 | 42,43,44,45,46,47,48,49,50,51 | — | — | — | — | — | — |
| regulation:telemetry_unknown | 10 | 42,43,44,45,46,47,48,49,50,51 | — | — | — | — | — | — |
| stdp:productive_reward_stdp | 10 | 42,43,44,45,46,47,48,49,50,51 | — | — | — | — | — | — |
| temporal:fast_medium_slow | 10 | 42,43,44,45,46,47,48,49,50,51 | 1000 | 0 | — | — | — | — |
| time:100 | 10 | 42,43,44,45,46,47,48,49,50,51 | — | — | — | — | — | — |
| time:1000 | 10 | 42,43,44,45,46,47,48,49,50,51 | — | — | — | — | — | — |

### 5.2 Inter-Spike-Intervalle

- `5d:1d`: n=20, mean=1, median=1, min=1, max=1 Ticks.
- `5d:2d`: n=20, mean=1, median=1, min=1, max=1 Ticks.
- `5d:3d`: n=20, mean=1, median=1, min=1, max=1 Ticks.
- `5d:5d`: n=20, mean=1, median=1, min=1, max=1 Ticks.
- `5d:5d_shuffled`: n=20, mean=1, median=1, min=1, max=1 Ticks.
- `5d:random_graph`: n=20, mean=1, median=1, min=1, max=1 Ticks.
- `ping:recurrence_off`: n=20, mean=1, median=1, min=1, max=1 Ticks.
- `ping:recurrence_on`: n=320, mean=1.9375, median=2, min=1, max=4 Ticks.

### 5.3 Temporal-State-Horizonte

- `fast`: Referenzvergleiche=9980; discrepancy mean=0.00263097, max=0.952011; nonzero=9980 (1); mean(nonzero)=0.00263097.
- `medium`: Referenzvergleiche=9960; discrepancy mean=0.00379847, max=1.15894; nonzero=9960 (1); mean(nonzero)=0.00379847.
- `slow`: Referenzvergleiche=9940; discrepancy mean=0.00463849, max=1.17842; nonzero=9940 (1); mean(nonzero)=0.00463849.

## 6. Einzelne Läufe

| Seed | Condition | Ticks | Spikes | Syn. events | Aktivierte Neuronen | Recurrent events | Depth | Runtime error |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 42 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 42 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 43 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 43 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 44 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 44 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 45 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 45 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 46 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 46 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 47 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 47 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 48 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 48 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 49 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 49 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 50 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 50 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 51 | ping:recurrence_off | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 51 | ping:recurrence_on | 1000 | 33 | 33 | 3 | 10 | 61 | — |
| 42 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 43 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 44 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 45 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 46 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 47 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 48 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 49 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 50 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 51 | temporal:fast_medium_slow | 1000 | 0 | — | — | — | — | — |
| 42 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 43 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 44 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 45 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 46 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 47 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 48 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 49 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 50 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 51 | stdp:productive_reward_stdp | — | — | — | — | — | — | — |
| 42 | learning:learning_on | — | — | — | — | — | — | — |
| 42 | learning:learning_off | — | — | — | — | — | — | — |
| 42 | learning:sham_replay | — | — | — | — | — | — | — |
| 43 | learning:learning_on | — | — | — | — | — | — | — |
| 43 | learning:learning_off | — | — | — | — | — | — | — |
| 43 | learning:sham_replay | — | — | — | — | — | — | — |
| 44 | learning:learning_on | — | — | — | — | — | — | — |
| 44 | learning:learning_off | — | — | — | — | — | — | — |
| 44 | learning:sham_replay | — | — | — | — | — | — | — |
| 45 | learning:learning_on | — | — | — | — | — | — | — |
| 45 | learning:learning_off | — | — | — | — | — | — | — |
| 45 | learning:sham_replay | — | — | — | — | — | — | — |
| 46 | learning:learning_on | — | — | — | — | — | — | — |
| 46 | learning:learning_off | — | — | — | — | — | — | — |
| 46 | learning:sham_replay | — | — | — | — | — | — | — |
| 47 | learning:learning_on | — | — | — | — | — | — | — |
| 47 | learning:learning_off | — | — | — | — | — | — | — |
| 47 | learning:sham_replay | — | — | — | — | — | — | — |
| 48 | learning:learning_on | — | — | — | — | — | — | — |
| 48 | learning:learning_off | — | — | — | — | — | — | — |
| 48 | learning:sham_replay | — | — | — | — | — | — | — |
| 49 | learning:learning_on | — | — | — | — | — | — | — |
| 49 | learning:learning_off | — | — | — | — | — | — | — |
| 49 | learning:sham_replay | — | — | — | — | — | — | — |
| 50 | learning:learning_on | — | — | — | — | — | — | — |
| 50 | learning:learning_off | — | — | — | — | — | — | — |
| 50 | learning:sham_replay | — | — | — | — | — | — | — |
| 51 | learning:learning_on | — | — | — | — | — | — | — |
| 51 | learning:learning_off | — | — | — | — | — | — | — |
| 51 | learning:sham_replay | — | — | — | — | — | — | — |
| 42 | time:100 | 100 | — | — | — | — | — | — |
| 42 | time:1000 | 1000 | — | — | — | — | — | — |
| 43 | time:100 | 100 | — | — | — | — | — | — |
| 43 | time:1000 | 1000 | — | — | — | — | — | — |
| 44 | time:100 | 100 | — | — | — | — | — | — |
| 44 | time:1000 | 1000 | — | — | — | — | — | — |
| 45 | time:100 | 100 | — | — | — | — | — | — |
| 45 | time:1000 | 1000 | — | — | — | — | — | — |
| 46 | time:100 | 100 | — | — | — | — | — | — |
| 46 | time:1000 | 1000 | — | — | — | — | — | — |
| 47 | time:100 | 100 | — | — | — | — | — | — |
| 47 | time:1000 | 1000 | — | — | — | — | — | — |
| 48 | time:100 | 100 | — | — | — | — | — | — |
| 48 | time:1000 | 1000 | — | — | — | — | — | — |
| 49 | time:100 | 100 | — | — | — | — | — | — |
| 49 | time:1000 | 1000 | — | — | — | — | — | — |
| 50 | time:100 | 100 | — | — | — | — | — | — |
| 50 | time:1000 | 1000 | — | — | — | — | — | — |
| 51 | time:100 | 100 | — | — | — | — | — | — |
| 51 | time:1000 | 1000 | — | — | — | — | — | — |
| 42 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 42 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 42 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 42 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 42 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 42 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 43 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 43 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 43 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 43 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 43 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 43 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 44 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 44 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 44 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 44 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 44 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 44 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 45 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 45 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 45 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 45 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 45 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 45 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 46 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 46 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 46 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 46 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 46 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 46 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 47 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 47 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 47 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 47 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 47 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 47 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 48 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 48 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 48 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 48 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 48 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 48 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 49 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 49 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 49 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 49 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 49 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 49 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 50 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 50 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 50 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 50 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 50 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 50 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 51 | 5d:1d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 51 | 5d:2d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 51 | 5d:3d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 51 | 5d:5d | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 51 | 5d:5d_shuffled | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 51 | 5d:random_graph | 1000 | 3 | 2 | 3 | 0 | 1 | — |
| 42 | regulation:nominal | — | — | — | — | — | — | — |
| 42 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 42 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 43 | regulation:nominal | — | — | — | — | — | — | — |
| 43 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 43 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 44 | regulation:nominal | — | — | — | — | — | — | — |
| 44 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 44 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 45 | regulation:nominal | — | — | — | — | — | — | — |
| 45 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 45 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 46 | regulation:nominal | — | — | — | — | — | — | — |
| 46 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 46 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 47 | regulation:nominal | — | — | — | — | — | — | — |
| 47 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 47 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 48 | regulation:nominal | — | — | — | — | — | — | — |
| 48 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 48 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 49 | regulation:nominal | — | — | — | — | — | — | — |
| 49 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 49 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 50 | regulation:nominal | — | — | — | — | — | — | — |
| 50 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 50 | regulation:telemetry_unknown | — | — | — | — | — | — | — |
| 51 | regulation:nominal | — | — | — | — | — | — | — |
| 51 | regulation:chronic_pressure | — | — | — | — | — | — | — |
| 51 | regulation:telemetry_unknown | — | — | — | — | — | — | — |

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

Die Analyse konnte nicht vollstaendig schema-konform erzeugt werden. Das Modell hat das erforderliche assessment-Feld nicht geliefert.

KI-Konfidenz: `0.0` — dies ist keine statistische Konfidenz.

### Methodische Kritik

- Keine expliziten Angaben.

### Alternative Erklaerungen

- Keine expliziten Angaben.

### Fehlende Nachweise

- Keine expliziten zusätzlichen Nachweise im AIRR angegeben.

### Empfohlene Folgeexperimente

- Keine expliziten Folgeexperimente im AIRR angegeben.

## 9. Artefakte

- [analysis/ai_packet.json](analysis/ai_packet.json)
- [analysis/ai_packet_digest.json](analysis/ai_packet_digest.json)
- [analysis/AIAR-critical_reviewer-20260916175624306872-e85234d4.json](analysis/AIAR-critical_reviewer-20260916175624306872-e85234d4.json)
- [analysis/AIAR-scientific_analyst-20260916175603687958-e85234d4.json](analysis/AIAR-scientific_analyst-20260916175603687958-e85234d4.json)
- [analysis/AIAR-scientific_writer-20260916175643715702-e85234d4.json](analysis/AIAR-scientific_writer-20260916175643715702-e85234d4.json)
- [analysis/statistics.json](analysis/statistics.json)
- [DATA/current_run.json](DATA/current_run.json)
- [DATA/raw/run-0000-ping-recurrence_off-seed-42.json.gz](DATA/raw/run-0000-ping-recurrence_off-seed-42.json.gz)
- [DATA/raw/run-0001-ping-recurrence_on-seed-42.json.gz](DATA/raw/run-0001-ping-recurrence_on-seed-42.json.gz)
- [DATA/raw/run-0002-ping-recurrence_off-seed-43.json.gz](DATA/raw/run-0002-ping-recurrence_off-seed-43.json.gz)
- [DATA/raw/run-0003-ping-recurrence_on-seed-43.json.gz](DATA/raw/run-0003-ping-recurrence_on-seed-43.json.gz)
- [DATA/raw/run-0004-ping-recurrence_off-seed-44.json.gz](DATA/raw/run-0004-ping-recurrence_off-seed-44.json.gz)
- [DATA/raw/run-0005-ping-recurrence_on-seed-44.json.gz](DATA/raw/run-0005-ping-recurrence_on-seed-44.json.gz)
- [DATA/raw/run-0006-ping-recurrence_off-seed-45.json.gz](DATA/raw/run-0006-ping-recurrence_off-seed-45.json.gz)
- [DATA/raw/run-0007-ping-recurrence_on-seed-45.json.gz](DATA/raw/run-0007-ping-recurrence_on-seed-45.json.gz)
- [DATA/raw/run-0008-ping-recurrence_off-seed-46.json.gz](DATA/raw/run-0008-ping-recurrence_off-seed-46.json.gz)
- [DATA/raw/run-0009-ping-recurrence_on-seed-46.json.gz](DATA/raw/run-0009-ping-recurrence_on-seed-46.json.gz)
- [DATA/raw/run-0010-ping-recurrence_off-seed-47.json.gz](DATA/raw/run-0010-ping-recurrence_off-seed-47.json.gz)
- [DATA/raw/run-0011-ping-recurrence_on-seed-47.json.gz](DATA/raw/run-0011-ping-recurrence_on-seed-47.json.gz)
- [DATA/raw/run-0012-ping-recurrence_off-seed-48.json.gz](DATA/raw/run-0012-ping-recurrence_off-seed-48.json.gz)
- [DATA/raw/run-0013-ping-recurrence_on-seed-48.json.gz](DATA/raw/run-0013-ping-recurrence_on-seed-48.json.gz)
- [DATA/raw/run-0014-ping-recurrence_off-seed-49.json.gz](DATA/raw/run-0014-ping-recurrence_off-seed-49.json.gz)
- [DATA/raw/run-0015-ping-recurrence_on-seed-49.json.gz](DATA/raw/run-0015-ping-recurrence_on-seed-49.json.gz)
- [DATA/raw/run-0016-ping-recurrence_off-seed-50.json.gz](DATA/raw/run-0016-ping-recurrence_off-seed-50.json.gz)
- [DATA/raw/run-0017-ping-recurrence_on-seed-50.json.gz](DATA/raw/run-0017-ping-recurrence_on-seed-50.json.gz)
- [DATA/raw/run-0018-ping-recurrence_off-seed-51.json.gz](DATA/raw/run-0018-ping-recurrence_off-seed-51.json.gz)
- [DATA/raw/run-0019-ping-recurrence_on-seed-51.json.gz](DATA/raw/run-0019-ping-recurrence_on-seed-51.json.gz)
- [DATA/raw/run-0020-temporal-fast_medium_slow-seed-42.json.gz](DATA/raw/run-0020-temporal-fast_medium_slow-seed-42.json.gz)
- [DATA/raw/run-0021-temporal-fast_medium_slow-seed-43.json.gz](DATA/raw/run-0021-temporal-fast_medium_slow-seed-43.json.gz)
- [DATA/raw/run-0022-temporal-fast_medium_slow-seed-44.json.gz](DATA/raw/run-0022-temporal-fast_medium_slow-seed-44.json.gz)
- [DATA/raw/run-0023-temporal-fast_medium_slow-seed-45.json.gz](DATA/raw/run-0023-temporal-fast_medium_slow-seed-45.json.gz)
- [DATA/raw/run-0024-temporal-fast_medium_slow-seed-46.json.gz](DATA/raw/run-0024-temporal-fast_medium_slow-seed-46.json.gz)
- [DATA/raw/run-0025-temporal-fast_medium_slow-seed-47.json.gz](DATA/raw/run-0025-temporal-fast_medium_slow-seed-47.json.gz)
- [DATA/raw/run-0026-temporal-fast_medium_slow-seed-48.json.gz](DATA/raw/run-0026-temporal-fast_medium_slow-seed-48.json.gz)
- [DATA/raw/run-0027-temporal-fast_medium_slow-seed-49.json.gz](DATA/raw/run-0027-temporal-fast_medium_slow-seed-49.json.gz)
- [DATA/raw/run-0028-temporal-fast_medium_slow-seed-50.json.gz](DATA/raw/run-0028-temporal-fast_medium_slow-seed-50.json.gz)
- [DATA/raw/run-0029-temporal-fast_medium_slow-seed-51.json.gz](DATA/raw/run-0029-temporal-fast_medium_slow-seed-51.json.gz)
- [DATA/raw/run-0030-stdp-productive_reward_stdp-seed-42.json.gz](DATA/raw/run-0030-stdp-productive_reward_stdp-seed-42.json.gz)
- [DATA/raw/run-0031-stdp-productive_reward_stdp-seed-43.json.gz](DATA/raw/run-0031-stdp-productive_reward_stdp-seed-43.json.gz)
- [DATA/raw/run-0032-stdp-productive_reward_stdp-seed-44.json.gz](DATA/raw/run-0032-stdp-productive_reward_stdp-seed-44.json.gz)
- [DATA/raw/run-0033-stdp-productive_reward_stdp-seed-45.json.gz](DATA/raw/run-0033-stdp-productive_reward_stdp-seed-45.json.gz)
- [DATA/raw/run-0034-stdp-productive_reward_stdp-seed-46.json.gz](DATA/raw/run-0034-stdp-productive_reward_stdp-seed-46.json.gz)
- [DATA/raw/run-0035-stdp-productive_reward_stdp-seed-47.json.gz](DATA/raw/run-0035-stdp-productive_reward_stdp-seed-47.json.gz)
- [DATA/raw/run-0036-stdp-productive_reward_stdp-seed-48.json.gz](DATA/raw/run-0036-stdp-productive_reward_stdp-seed-48.json.gz)
- [DATA/raw/run-0037-stdp-productive_reward_stdp-seed-49.json.gz](DATA/raw/run-0037-stdp-productive_reward_stdp-seed-49.json.gz)
- [DATA/raw/run-0038-stdp-productive_reward_stdp-seed-50.json.gz](DATA/raw/run-0038-stdp-productive_reward_stdp-seed-50.json.gz)
- [DATA/raw/run-0039-stdp-productive_reward_stdp-seed-51.json.gz](DATA/raw/run-0039-stdp-productive_reward_stdp-seed-51.json.gz)
- [DATA/raw/run-0040-learning-learning_on-seed-42.json.gz](DATA/raw/run-0040-learning-learning_on-seed-42.json.gz)
- [DATA/raw/run-0041-learning-learning_off-seed-42.json.gz](DATA/raw/run-0041-learning-learning_off-seed-42.json.gz)
- [DATA/raw/run-0042-learning-sham_replay-seed-42.json.gz](DATA/raw/run-0042-learning-sham_replay-seed-42.json.gz)
- [DATA/raw/run-0043-learning-learning_on-seed-43.json.gz](DATA/raw/run-0043-learning-learning_on-seed-43.json.gz)
- [DATA/raw/run-0044-learning-learning_off-seed-43.json.gz](DATA/raw/run-0044-learning-learning_off-seed-43.json.gz)
- [DATA/raw/run-0045-learning-sham_replay-seed-43.json.gz](DATA/raw/run-0045-learning-sham_replay-seed-43.json.gz)
- [DATA/raw/run-0046-learning-learning_on-seed-44.json.gz](DATA/raw/run-0046-learning-learning_on-seed-44.json.gz)
- [DATA/raw/run-0047-learning-learning_off-seed-44.json.gz](DATA/raw/run-0047-learning-learning_off-seed-44.json.gz)
- [DATA/raw/run-0048-learning-sham_replay-seed-44.json.gz](DATA/raw/run-0048-learning-sham_replay-seed-44.json.gz)
- [DATA/raw/run-0049-learning-learning_on-seed-45.json.gz](DATA/raw/run-0049-learning-learning_on-seed-45.json.gz)
- [DATA/raw/run-0050-learning-learning_off-seed-45.json.gz](DATA/raw/run-0050-learning-learning_off-seed-45.json.gz)
- [DATA/raw/run-0051-learning-sham_replay-seed-45.json.gz](DATA/raw/run-0051-learning-sham_replay-seed-45.json.gz)
- [DATA/raw/run-0052-learning-learning_on-seed-46.json.gz](DATA/raw/run-0052-learning-learning_on-seed-46.json.gz)
- [DATA/raw/run-0053-learning-learning_off-seed-46.json.gz](DATA/raw/run-0053-learning-learning_off-seed-46.json.gz)
- [DATA/raw/run-0054-learning-sham_replay-seed-46.json.gz](DATA/raw/run-0054-learning-sham_replay-seed-46.json.gz)
- [DATA/raw/run-0055-learning-learning_on-seed-47.json.gz](DATA/raw/run-0055-learning-learning_on-seed-47.json.gz)
- [DATA/raw/run-0056-learning-learning_off-seed-47.json.gz](DATA/raw/run-0056-learning-learning_off-seed-47.json.gz)
- [DATA/raw/run-0057-learning-sham_replay-seed-47.json.gz](DATA/raw/run-0057-learning-sham_replay-seed-47.json.gz)
- [DATA/raw/run-0058-learning-learning_on-seed-48.json.gz](DATA/raw/run-0058-learning-learning_on-seed-48.json.gz)
- [DATA/raw/run-0059-learning-learning_off-seed-48.json.gz](DATA/raw/run-0059-learning-learning_off-seed-48.json.gz)
- [DATA/raw/run-0060-learning-sham_replay-seed-48.json.gz](DATA/raw/run-0060-learning-sham_replay-seed-48.json.gz)
- [DATA/raw/run-0061-learning-learning_on-seed-49.json.gz](DATA/raw/run-0061-learning-learning_on-seed-49.json.gz)
- [DATA/raw/run-0062-learning-learning_off-seed-49.json.gz](DATA/raw/run-0062-learning-learning_off-seed-49.json.gz)
- [DATA/raw/run-0063-learning-sham_replay-seed-49.json.gz](DATA/raw/run-0063-learning-sham_replay-seed-49.json.gz)
- [DATA/raw/run-0064-learning-learning_on-seed-50.json.gz](DATA/raw/run-0064-learning-learning_on-seed-50.json.gz)
- [DATA/raw/run-0065-learning-learning_off-seed-50.json.gz](DATA/raw/run-0065-learning-learning_off-seed-50.json.gz)
- [DATA/raw/run-0066-learning-sham_replay-seed-50.json.gz](DATA/raw/run-0066-learning-sham_replay-seed-50.json.gz)
- [DATA/raw/run-0067-learning-learning_on-seed-51.json.gz](DATA/raw/run-0067-learning-learning_on-seed-51.json.gz)
- [DATA/raw/run-0068-learning-learning_off-seed-51.json.gz](DATA/raw/run-0068-learning-learning_off-seed-51.json.gz)
- [DATA/raw/run-0069-learning-sham_replay-seed-51.json.gz](DATA/raw/run-0069-learning-sham_replay-seed-51.json.gz)
- [DATA/raw/run-0070-time-100-seed-42.json.gz](DATA/raw/run-0070-time-100-seed-42.json.gz)
- [DATA/raw/run-0071-time-1000-seed-42.json.gz](DATA/raw/run-0071-time-1000-seed-42.json.gz)
- [DATA/raw/run-0072-time-100-seed-43.json.gz](DATA/raw/run-0072-time-100-seed-43.json.gz)
- [DATA/raw/run-0073-time-1000-seed-43.json.gz](DATA/raw/run-0073-time-1000-seed-43.json.gz)
- [DATA/raw/run-0074-time-100-seed-44.json.gz](DATA/raw/run-0074-time-100-seed-44.json.gz)
- [DATA/raw/run-0075-time-1000-seed-44.json.gz](DATA/raw/run-0075-time-1000-seed-44.json.gz)
- [DATA/raw/run-0076-time-100-seed-45.json.gz](DATA/raw/run-0076-time-100-seed-45.json.gz)
- [DATA/raw/run-0077-time-1000-seed-45.json.gz](DATA/raw/run-0077-time-1000-seed-45.json.gz)
- [DATA/raw/run-0078-time-100-seed-46.json.gz](DATA/raw/run-0078-time-100-seed-46.json.gz)
- [DATA/raw/run-0079-time-1000-seed-46.json.gz](DATA/raw/run-0079-time-1000-seed-46.json.gz)
- [DATA/raw/run-0080-time-100-seed-47.json.gz](DATA/raw/run-0080-time-100-seed-47.json.gz)
- [DATA/raw/run-0081-time-1000-seed-47.json.gz](DATA/raw/run-0081-time-1000-seed-47.json.gz)
- [DATA/raw/run-0082-time-100-seed-48.json.gz](DATA/raw/run-0082-time-100-seed-48.json.gz)
- [DATA/raw/run-0083-time-1000-seed-48.json.gz](DATA/raw/run-0083-time-1000-seed-48.json.gz)
- [DATA/raw/run-0084-time-100-seed-49.json.gz](DATA/raw/run-0084-time-100-seed-49.json.gz)
- [DATA/raw/run-0085-time-1000-seed-49.json.gz](DATA/raw/run-0085-time-1000-seed-49.json.gz)
- [DATA/raw/run-0086-time-100-seed-50.json.gz](DATA/raw/run-0086-time-100-seed-50.json.gz)
- [DATA/raw/run-0087-time-1000-seed-50.json.gz](DATA/raw/run-0087-time-1000-seed-50.json.gz)
- [DATA/raw/run-0088-time-100-seed-51.json.gz](DATA/raw/run-0088-time-100-seed-51.json.gz)
- [DATA/raw/run-0089-time-1000-seed-51.json.gz](DATA/raw/run-0089-time-1000-seed-51.json.gz)
- [DATA/raw/run-0090-5d-1d-seed-42.json.gz](DATA/raw/run-0090-5d-1d-seed-42.json.gz)
- [DATA/raw/run-0091-5d-2d-seed-42.json.gz](DATA/raw/run-0091-5d-2d-seed-42.json.gz)
- [DATA/raw/run-0092-5d-3d-seed-42.json.gz](DATA/raw/run-0092-5d-3d-seed-42.json.gz)
- [DATA/raw/run-0093-5d-5d-seed-42.json.gz](DATA/raw/run-0093-5d-5d-seed-42.json.gz)
- [DATA/raw/run-0094-5d-5d_shuffled-seed-42.json.gz](DATA/raw/run-0094-5d-5d_shuffled-seed-42.json.gz)
- [DATA/raw/run-0095-5d-random_graph-seed-42.json.gz](DATA/raw/run-0095-5d-random_graph-seed-42.json.gz)
- [DATA/raw/run-0096-5d-1d-seed-43.json.gz](DATA/raw/run-0096-5d-1d-seed-43.json.gz)
- [DATA/raw/run-0097-5d-2d-seed-43.json.gz](DATA/raw/run-0097-5d-2d-seed-43.json.gz)
- [DATA/raw/run-0098-5d-3d-seed-43.json.gz](DATA/raw/run-0098-5d-3d-seed-43.json.gz)
- [DATA/raw/run-0099-5d-5d-seed-43.json.gz](DATA/raw/run-0099-5d-5d-seed-43.json.gz)
- [DATA/raw/run-0100-5d-5d_shuffled-seed-43.json.gz](DATA/raw/run-0100-5d-5d_shuffled-seed-43.json.gz)
- [DATA/raw/run-0101-5d-random_graph-seed-43.json.gz](DATA/raw/run-0101-5d-random_graph-seed-43.json.gz)
- [DATA/raw/run-0102-5d-1d-seed-44.json.gz](DATA/raw/run-0102-5d-1d-seed-44.json.gz)
- [DATA/raw/run-0103-5d-2d-seed-44.json.gz](DATA/raw/run-0103-5d-2d-seed-44.json.gz)
- [DATA/raw/run-0104-5d-3d-seed-44.json.gz](DATA/raw/run-0104-5d-3d-seed-44.json.gz)
- [DATA/raw/run-0105-5d-5d-seed-44.json.gz](DATA/raw/run-0105-5d-5d-seed-44.json.gz)
- [DATA/raw/run-0106-5d-5d_shuffled-seed-44.json.gz](DATA/raw/run-0106-5d-5d_shuffled-seed-44.json.gz)
- [DATA/raw/run-0107-5d-random_graph-seed-44.json.gz](DATA/raw/run-0107-5d-random_graph-seed-44.json.gz)
- [DATA/raw/run-0108-5d-1d-seed-45.json.gz](DATA/raw/run-0108-5d-1d-seed-45.json.gz)
- [DATA/raw/run-0109-5d-2d-seed-45.json.gz](DATA/raw/run-0109-5d-2d-seed-45.json.gz)
- [DATA/raw/run-0110-5d-3d-seed-45.json.gz](DATA/raw/run-0110-5d-3d-seed-45.json.gz)
- [DATA/raw/run-0111-5d-5d-seed-45.json.gz](DATA/raw/run-0111-5d-5d-seed-45.json.gz)
- [DATA/raw/run-0112-5d-5d_shuffled-seed-45.json.gz](DATA/raw/run-0112-5d-5d_shuffled-seed-45.json.gz)
- [DATA/raw/run-0113-5d-random_graph-seed-45.json.gz](DATA/raw/run-0113-5d-random_graph-seed-45.json.gz)
- [DATA/raw/run-0114-5d-1d-seed-46.json.gz](DATA/raw/run-0114-5d-1d-seed-46.json.gz)
- [DATA/raw/run-0115-5d-2d-seed-46.json.gz](DATA/raw/run-0115-5d-2d-seed-46.json.gz)
- [DATA/raw/run-0116-5d-3d-seed-46.json.gz](DATA/raw/run-0116-5d-3d-seed-46.json.gz)
- [DATA/raw/run-0117-5d-5d-seed-46.json.gz](DATA/raw/run-0117-5d-5d-seed-46.json.gz)
- [DATA/raw/run-0118-5d-5d_shuffled-seed-46.json.gz](DATA/raw/run-0118-5d-5d_shuffled-seed-46.json.gz)
- [DATA/raw/run-0119-5d-random_graph-seed-46.json.gz](DATA/raw/run-0119-5d-random_graph-seed-46.json.gz)
- [DATA/raw/run-0120-5d-1d-seed-47.json.gz](DATA/raw/run-0120-5d-1d-seed-47.json.gz)
- [DATA/raw/run-0121-5d-2d-seed-47.json.gz](DATA/raw/run-0121-5d-2d-seed-47.json.gz)
- [DATA/raw/run-0122-5d-3d-seed-47.json.gz](DATA/raw/run-0122-5d-3d-seed-47.json.gz)
- [DATA/raw/run-0123-5d-5d-seed-47.json.gz](DATA/raw/run-0123-5d-5d-seed-47.json.gz)
- [DATA/raw/run-0124-5d-5d_shuffled-seed-47.json.gz](DATA/raw/run-0124-5d-5d_shuffled-seed-47.json.gz)
- [DATA/raw/run-0125-5d-random_graph-seed-47.json.gz](DATA/raw/run-0125-5d-random_graph-seed-47.json.gz)
- [DATA/raw/run-0126-5d-1d-seed-48.json.gz](DATA/raw/run-0126-5d-1d-seed-48.json.gz)
- [DATA/raw/run-0127-5d-2d-seed-48.json.gz](DATA/raw/run-0127-5d-2d-seed-48.json.gz)
- [DATA/raw/run-0128-5d-3d-seed-48.json.gz](DATA/raw/run-0128-5d-3d-seed-48.json.gz)
- [DATA/raw/run-0129-5d-5d-seed-48.json.gz](DATA/raw/run-0129-5d-5d-seed-48.json.gz)
- [DATA/raw/run-0130-5d-5d_shuffled-seed-48.json.gz](DATA/raw/run-0130-5d-5d_shuffled-seed-48.json.gz)
- [DATA/raw/run-0131-5d-random_graph-seed-48.json.gz](DATA/raw/run-0131-5d-random_graph-seed-48.json.gz)
- [DATA/raw/run-0132-5d-1d-seed-49.json.gz](DATA/raw/run-0132-5d-1d-seed-49.json.gz)
- [DATA/raw/run-0133-5d-2d-seed-49.json.gz](DATA/raw/run-0133-5d-2d-seed-49.json.gz)
- [DATA/raw/run-0134-5d-3d-seed-49.json.gz](DATA/raw/run-0134-5d-3d-seed-49.json.gz)
- [DATA/raw/run-0135-5d-5d-seed-49.json.gz](DATA/raw/run-0135-5d-5d-seed-49.json.gz)
- [DATA/raw/run-0136-5d-5d_shuffled-seed-49.json.gz](DATA/raw/run-0136-5d-5d_shuffled-seed-49.json.gz)
- [DATA/raw/run-0137-5d-random_graph-seed-49.json.gz](DATA/raw/run-0137-5d-random_graph-seed-49.json.gz)
- [DATA/raw/run-0138-5d-1d-seed-50.json.gz](DATA/raw/run-0138-5d-1d-seed-50.json.gz)
- [DATA/raw/run-0139-5d-2d-seed-50.json.gz](DATA/raw/run-0139-5d-2d-seed-50.json.gz)
- [DATA/raw/run-0140-5d-3d-seed-50.json.gz](DATA/raw/run-0140-5d-3d-seed-50.json.gz)
- [DATA/raw/run-0141-5d-5d-seed-50.json.gz](DATA/raw/run-0141-5d-5d-seed-50.json.gz)
- [DATA/raw/run-0142-5d-5d_shuffled-seed-50.json.gz](DATA/raw/run-0142-5d-5d_shuffled-seed-50.json.gz)
- [DATA/raw/run-0143-5d-random_graph-seed-50.json.gz](DATA/raw/run-0143-5d-random_graph-seed-50.json.gz)
- [DATA/raw/run-0144-5d-1d-seed-51.json.gz](DATA/raw/run-0144-5d-1d-seed-51.json.gz)
- [DATA/raw/run-0145-5d-2d-seed-51.json.gz](DATA/raw/run-0145-5d-2d-seed-51.json.gz)
- [DATA/raw/run-0146-5d-3d-seed-51.json.gz](DATA/raw/run-0146-5d-3d-seed-51.json.gz)
- [DATA/raw/run-0147-5d-5d-seed-51.json.gz](DATA/raw/run-0147-5d-5d-seed-51.json.gz)
- [DATA/raw/run-0148-5d-5d_shuffled-seed-51.json.gz](DATA/raw/run-0148-5d-5d_shuffled-seed-51.json.gz)
- [DATA/raw/run-0149-5d-random_graph-seed-51.json.gz](DATA/raw/run-0149-5d-random_graph-seed-51.json.gz)
- [DATA/raw/run-0150-regulation-nominal-seed-42.json.gz](DATA/raw/run-0150-regulation-nominal-seed-42.json.gz)
- [DATA/raw/run-0151-regulation-chronic_pressure-seed-42.json.gz](DATA/raw/run-0151-regulation-chronic_pressure-seed-42.json.gz)
- [DATA/raw/run-0152-regulation-telemetry_unknown-seed-42.json.gz](DATA/raw/run-0152-regulation-telemetry_unknown-seed-42.json.gz)
- [DATA/raw/run-0153-regulation-nominal-seed-43.json.gz](DATA/raw/run-0153-regulation-nominal-seed-43.json.gz)
- [DATA/raw/run-0154-regulation-chronic_pressure-seed-43.json.gz](DATA/raw/run-0154-regulation-chronic_pressure-seed-43.json.gz)
- [DATA/raw/run-0155-regulation-telemetry_unknown-seed-43.json.gz](DATA/raw/run-0155-regulation-telemetry_unknown-seed-43.json.gz)
- [DATA/raw/run-0156-regulation-nominal-seed-44.json.gz](DATA/raw/run-0156-regulation-nominal-seed-44.json.gz)
- [DATA/raw/run-0157-regulation-chronic_pressure-seed-44.json.gz](DATA/raw/run-0157-regulation-chronic_pressure-seed-44.json.gz)
- [DATA/raw/run-0158-regulation-telemetry_unknown-seed-44.json.gz](DATA/raw/run-0158-regulation-telemetry_unknown-seed-44.json.gz)
- [DATA/raw/run-0159-regulation-nominal-seed-45.json.gz](DATA/raw/run-0159-regulation-nominal-seed-45.json.gz)
- [DATA/raw/run-0160-regulation-chronic_pressure-seed-45.json.gz](DATA/raw/run-0160-regulation-chronic_pressure-seed-45.json.gz)
- [DATA/raw/run-0161-regulation-telemetry_unknown-seed-45.json.gz](DATA/raw/run-0161-regulation-telemetry_unknown-seed-45.json.gz)
- [DATA/raw/run-0162-regulation-nominal-seed-46.json.gz](DATA/raw/run-0162-regulation-nominal-seed-46.json.gz)
- [DATA/raw/run-0163-regulation-chronic_pressure-seed-46.json.gz](DATA/raw/run-0163-regulation-chronic_pressure-seed-46.json.gz)
- [DATA/raw/run-0164-regulation-telemetry_unknown-seed-46.json.gz](DATA/raw/run-0164-regulation-telemetry_unknown-seed-46.json.gz)
- [DATA/raw/run-0165-regulation-nominal-seed-47.json.gz](DATA/raw/run-0165-regulation-nominal-seed-47.json.gz)
- [DATA/raw/run-0166-regulation-chronic_pressure-seed-47.json.gz](DATA/raw/run-0166-regulation-chronic_pressure-seed-47.json.gz)
- [DATA/raw/run-0167-regulation-telemetry_unknown-seed-47.json.gz](DATA/raw/run-0167-regulation-telemetry_unknown-seed-47.json.gz)
- [DATA/raw/run-0168-regulation-nominal-seed-48.json.gz](DATA/raw/run-0168-regulation-nominal-seed-48.json.gz)
- [DATA/raw/run-0169-regulation-chronic_pressure-seed-48.json.gz](DATA/raw/run-0169-regulation-chronic_pressure-seed-48.json.gz)
- [DATA/raw/run-0170-regulation-telemetry_unknown-seed-48.json.gz](DATA/raw/run-0170-regulation-telemetry_unknown-seed-48.json.gz)
- [DATA/raw/run-0171-regulation-nominal-seed-49.json.gz](DATA/raw/run-0171-regulation-nominal-seed-49.json.gz)
- [DATA/raw/run-0172-regulation-chronic_pressure-seed-49.json.gz](DATA/raw/run-0172-regulation-chronic_pressure-seed-49.json.gz)
- [DATA/raw/run-0173-regulation-telemetry_unknown-seed-49.json.gz](DATA/raw/run-0173-regulation-telemetry_unknown-seed-49.json.gz)
- [DATA/raw/run-0174-regulation-nominal-seed-50.json.gz](DATA/raw/run-0174-regulation-nominal-seed-50.json.gz)
- [DATA/raw/run-0175-regulation-chronic_pressure-seed-50.json.gz](DATA/raw/run-0175-regulation-chronic_pressure-seed-50.json.gz)
- [DATA/raw/run-0176-regulation-telemetry_unknown-seed-50.json.gz](DATA/raw/run-0176-regulation-telemetry_unknown-seed-50.json.gz)
- [DATA/raw/run-0177-regulation-nominal-seed-51.json.gz](DATA/raw/run-0177-regulation-nominal-seed-51.json.gz)
- [DATA/raw/run-0178-regulation-chronic_pressure-seed-51.json.gz](DATA/raw/run-0178-regulation-chronic_pressure-seed-51.json.gz)
- [DATA/raw/run-0179-regulation-telemetry_unknown-seed-51.json.gz](DATA/raw/run-0179-regulation-telemetry_unknown-seed-51.json.gz)
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
