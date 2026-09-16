# EXP-GEN-0040: sustained_activity_stability_v1 — RQ-SNN-001

## Forschungszuordnung
Forschungsfrage: `RQ-SNN-001`
Hypothese: `H-SNN-001-A`
Aufgeloester Runner: `run_sustained_stability`

## Protokoll und Einstellungen
Protokoll: `sustained_activity_stability_v1`
Angeforderte Mindest-Ticks: `100000`
Seeds: `42, 43, 44, 45, 46, 47, 48, 49, 50, 51`
Tick-Vertrag: `{"mode": "minimum_per_run_with_control_and_treatment", "observed_max": 100000, "observed_min": 100000, "requested_ticks": 100000, "run_count": 20, "status": "SATISFIED"}`

## Bedingungen
no_input_control (negative_control); tonic_drive (stability_treatment)
Runs: 20; Dauer: 13.904198 s

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
Keine.
