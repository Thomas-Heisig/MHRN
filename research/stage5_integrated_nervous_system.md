# Stage 5 — Integriertes künstliches Nervensystem

Stand: 14. September 2026

## Ziel und Umfang

Stage 5 verbindet die bereits vorhandenen technischen Teilsysteme zu einem überprüfbaren künstlichen Nervensystem-Vertrag: **Sensorik → Kodierung/SNN → Dekodierung → autorisierte Aktorik → Umweltbeobachtung/Feedback**, ergänzt um **digitale Interozeption** und einen begrenzten **Ressourcenhaushalt**.

Die Stufe ist eine Engineering-Integration. Sie ist weder ein Nachweis biologischer Gleichwertigkeit noch ein Nachweis bewusster Erfahrung oder autonomer Realwelt-Handlungsfähigkeit.

## Full-Stack-Zuordnung

| Bereich | Implementierung | Laufzeit-/Frontend-Projektion |
| --- | --- | --- |
| Sensorik | `src/embodiment/sensor.py`, `system_sensor.py`, `sensor_activation.py` | `/api/embodiment/state`, `/api/embodiment/sensors`, `/api/embodiment/connections` |
| Interozeption | `src/embodiment/interoception.py` | abgeleitete Ressourcen-/Unsicherheitszustände; keine erfundenen Messwerte |
| Aktorik | `controlled.py`, `actuator_hub.py`, `audit.py` | autorisierte Kommandos sowie Acceptance-/Effect-Receipts |
| Feedback | `src/experience/engine.py`, `deterministic.py` | `/api/embodiment/pipeline`, `last_observation_state` |
| Ressourcenhaushalt | `interoception.py`, `msba.py` | begrenzter Resource Pressure / Energy Accounting; kein biologischer Metabolismus |
| Frontend | `frontend/modules/integrated-nervous-system.js` | Stage-5-Karte in Runtime/Wesen aus bestehenden Live-APIs |

Der read-only Integrationsvertrag liegt in `src/embodiment/integrated_nervous_system.py`. Er aktiviert keine externe Aktorik und verändert den kanonischen SNN-Zustand nicht.

## End-to-End-Referenzversuch

Die aktuelle Referenz wird als neuer, datierter Lauf unter
`research/experiments/EXP-STAGE5-20260914-INTEGRATED-NERVOUS-SYSTEM` erzeugt. Grundlage ist der registrierte `EXP-EMB-0001`-Protokollrunner mit sechs Kontrollbedingungen:

1. `authorized`
2. `unauthorized`
3. `actuator_failure`
4. `sensor_loss`
5. `open_loop_replay`
6. `sensor_reproducibility`

Die Stage-5-Referenz führt 20 unabhängige Seeds × 3 Wiederholungen × 6 Bedingungen = **360 kontrollierte Läufe** aus. Sie prüft unter anderem reproduzierbare Sensorframes, autorisierte Wirkpfade, Blockade nicht autorisierter Aktorik, fehlende Effekte bei Aktorfehlern, Erkennung von Sensorausfall sowie die explizite Trennung eines präregistrierten Open-Loop-Replays vom Network-Output.

Alle Resultate bleiben **DATA**. `evidence_eligible=false` und es gibt keine automatische EVID-Promotion.

## Forschungsfrage und Hypothesen

### RQ-EMB-001

**Frage:** Kann MHRN in einer Sensor-Aktor-Schleife sinnvoll bzw. zielgerichtet agieren?

### H-EMB-001-A

Der deterministische Referenzversuch adressiert `H-EMB-001-A` direkt: ein kontrollierter geschlossener Sensor-Aktor-Kreis kann in der synthetischen Zielumgebung zielgerichtete Wirkungen erzeugen. Das ist ein technischer DATA-Befund, noch keine akzeptierte wissenschaftliche EVID.

### H-EMB-001-B

`H-EMB-001-B` fordert einen Vergleich unter identischer externer Störung zwischen geschlossenem Kreis, yoked Replay und unterbrochener Rückmeldung anhand von `tracking_rmse_rad` und Sensorkonsequenzen. **Diese Hypothese wird durch den Stage-5-Referenzversuch nicht getestet.** Der vorhandene `open_loop_replay`-Kontrollpfad ist methodisch nützlich, ersetzt aber keinen matched-disturbance/yoked-Replay-Versuch.

Damit wird Stage 5 technisch vervollständigt, ohne die wissenschaftliche Evidenzlücke künstlich zu schließen.

## Verhältnis zu den Roadmap-Fragen

Stage 5 trägt zu den breiteren Embodiment-/Gateway-Fragen `RQ6`, `RQ7`, `RQ8` und `RQ9` bei. Die technische Integration schließt diese Fragen nicht automatisch. Insbesondere produktive reale Geräte, langfristige Stabilität, externe Störungen und Modalitätsintegration unter realen Bedingungen benötigen eigene kontrollierte Versuche.

## Wissenschaftliche Grenzen

- Der E2E-Versuch nutzt eine **synthetische deterministische Zielumgebung**.
- Reale Kamera-, Mikrofon-, Motor- oder Robotikgeräte werden dadurch nicht validiert.
- Host-Telemetrie ist **digitale Interozeption**, keine biologische Interozeption.
- `energy_reserve`, Resource Pressure und MSBA-Energiegrößen sind technische Regel-/Kostenvariablen, kein biologischer Stoffwechsel.
- Langzeitbetrieb und autonome Realwelt-Interaktion sind nicht nachgewiesen.
- H-EMB-001-B bleibt offen.
- Es gibt keine Aussage über Bewusstsein, Empfindung oder subjektives Erleben.
- DATA wird nicht automatisch zu EVID.

## Abschlusskriterium Stage 5

Stage 5 kann als **Engineering-Stufe vollständig integriert** gelten, wenn der Stage-5-Workflow den Integrationsvertrag, die 360 kontrollierten Referenzläufe, die Frontend-Verträge und die Publikationsgrenzen reproduzierbar verifiziert. Die wissenschaftliche Evidenzpromotion und unabhängige Replikation bleiben davon getrennte offene Aufgaben.


## Digital query as sensorimotor action

The digital interface is integrated into Stage 5 using the same causal principle as other sensor–actor loops:

```text
neural state -> query action -> external system -> returned information -> sensory encoding -> neural state
```

A database, API, algorithm or LLM is therefore treated as part of the **external environment**, not as a hidden MHRN cognitive module. Exact query syntax is produced at the declared decoder/boundary; the returned result re-enters through the declared encoder.

The action copy may be retained as an efference-copy signal, but it is not identical to an expected response. Response prediction requires a separate registered predictor and can later be tested against no-copy, shuffled-copy and delayed-copy controls.

The first direct learning question is `RQ-GW-009 / H-GW-009-A`: whether MHRN learns when to request information under matched query/resource budgets rather than relying on a fixed request schedule. This is not yet an executed Stage-5 finding.
