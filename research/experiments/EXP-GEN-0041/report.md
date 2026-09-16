# EXP-GEN-0041: sustained_activity_stability_v2 — seed-bound robustness

## Forschungszuordnung
Forschungsfrage: `RQ-SNN-006`
Hypothese: `H-SNN-006-A`
Aufgeloester Runner: `run_sustained_stability_v2`

## Protokoll und Einstellungen
Protokoll: `sustained_activity_stability_v2`
Angeforderte Mindest-Ticks: `100000`
Seeds: `101, 102, 103, 104, 105, 106, 107, 108, 109, 110`
Tick-Vertrag: `{"mode": "minimum_per_run_with_control_and_treatment", "observed_max": 100000, "observed_min": 100000, "requested_ticks": 100000, "run_count": 20, "status": "SATISFIED"}`

## Bedingungen
paired no_input_control and tonic_drive across ten distinct seed-bound parameterizations
Runs: 20; Dauer: 36.012704 s

## Daten und Statistik
Versionierte kompakte Run-Projektion: `DATA/runs_compact.json`
Unveränderlicher Rohdatenindex: `DATA/runs_index.json`
KI-Eingabepaket: `analysis/ai_packet.json` (hart begrenzt)
Deterministische deskriptive Statistik: `analysis/statistics.json`
Die Summary verbindet Rohdaten, Formeln, Einzelruns, Bedingungen, Reproduzierbarkeit und AIRR ohne KI-generierte Statistik.

## Epistemische Ebenen
UI-Zustand: Dashboard-Steuerung und Fortschritt; kein wissenschaftliches Ergebnis.
DATA: Rohdaten, Run-Index und deterministische Statistik.
EVID: nicht erzeugt; Clean Freeze, semantische Zuordnung und Human Review erforderlich.
Interpretation: nachgelagerte KI-/Human-Interpretation; keine Ausfuehrungseingabe.

## Evidenzstatus
DATA, Manifest, Workflow und deterministische Statistik sind erzeugt. Wissenschaftliche EVID entsteht erst nach passender semantischer Zuordnung, Clean Freeze und Human Review.

## Hinweise
First execution after frozen PREREG-SNN-006; no post-hoc threshold or parameter changes.
