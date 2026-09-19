# Seed-Datenvertrag fuer reproduzierbare Experimente

**Status:** current scientific/method specification  
**Scope:** registrierte Experimente, Ausfuehrungs-DATA und Replikationsprovenienz  
**Grundregel:** Ein Seed ist ein deterministischer Eingabewert, nicht selbst ein wissenschaftliches Ergebnis.

## 1. Zweck und Datenmodell

Ein Seed initialisiert die fuer ein Protokoll freigegebenen deterministischen Zufallsstroeme. Je nach Experiment werden daraus unterschiedliche Seed-gebundene Daten erzeugt:

1. Netzwerk-, Parameter- oder Kontrollrealisierung;
2. Trainings-/Testindizes, Task-Reihenfolge oder Replay-Auswahl;
3. Stimulus-, Resampling- oder Perturbationsstrom;
4. deterministische Lauf- und Zustandsdaten;
5. Digest-/Provenienzwerte zur Integritaetspruefung.

Der Seed selbst enthaelt keine Identitaets-, Kontakt- oder personenbezogenen Daten. Er ist eine Ganzzahl oder ein vorab definierter Seed-Bereich. Die wissenschaftlich relevante Information entsteht aus der Kombination von Seed, eingefrorenem Protokoll, Code-/Config-Freeze, Bedingung und gespeicherten DATA-Artefakten.

## 2. Was pro Seed gespeichert wird

Ein ausgefuehrter Seed-Datensatz soll, soweit das Protokoll es definiert, mindestens folgende Beziehungen nachvollziehbar machen:

| Feldgruppe | Inhalt | Beispiel |
|---|---|---|
| Identitaet | `experiment_id`, `seed`, `condition`, ggf. `run_id` | `EXP-S6-SEM-CL-003`, `301`, `R05` |
| Protokollbindung | Preregistration, Protocol, Source-Freeze, Config-Digest | `PREREG-...`, `protocol`, `source_freeze_sha` |
| Seed-Realisierung | abgeleitete Parameter, Indizes, Stimulus-/Perturbationswerte | `weight_scale`, `drive_scale`, Replay-Auswahl |
| Laufvertrag | angeforderte/ausgefuehrte Ticks, Update-/Trialzahl, Fehlerstatus | `100000` Ticks, `10000` Updates |
| Messwerte | primaire und sekundare Endpunkte | Accuracy, Forgetting, Latenz, Spikes |
| Integritaet | Realisierungs-, Zustands- oder Rohdaten-Digest | SHA-256-Digest |
| Interpretation | Status und Grenzen der Seed-Realisierung | DATA-only, kein EVID-Anspruch |

Die konkrete Feldmenge darf pro Protokoll enger oder umfangreicher sein. Nicht vorhandene Felder duerfen nicht aus anderen Experimenten ergaenzt oder rueckwirkend erfunden werden.

## 3. Gepaarte Bedingungen

Bei kontrollierten Experimenten wird derselbe Seed ueber die verglichenen Bedingungen verwendet. Dadurch werden Seed-gebundene Unterschiede gepaart:

- CL-003 verwendet zum Beispiel Seed `301` fuer `R05`, `S05`, `R20`, `S20`, `X20`, `R40` und `S40.
- Topologie-Experimente verwenden dieselben Evaluation-Seeds ueber 1d, 2d, 3d, 5d, 5d_shuffled und random_graph.
- Eine Differenz ist immer als innerhalb desselben Seed-Paares zu lesen, nicht als Vergleich unverbundener Seed-Populationen.

Trials oder wiederholte Messungen innerhalb eines Seeds sind keine neuen unabhaengigen Seeds. Das gilt besonders fuer deterministische Komponentenexperimente.

## 4. Konkrete Seed-DATA-Beispiele

### 4.1 Seed-gebundene Parameterrealisierung: EXP-GEN-0041

Fuer Seed `101` werden unter anderem gespeichert:

- Bedingung `no_input_control`;
- `parameter_jitter_fraction = 0.05`;
- `drive_scale = 1.0329619144`;
- `weight_scale = 0.9885681737`;
- `weight_min = weight_max = 98.85681737`;
- `burn_in_ticks = 10000` und `ticks_executed = 100000`;
- `total_spikes = 0`, `activity_regime = quiescent`;
- `realization_digest` als SHA-256-Nachweis;
- `topology_unchanged = true` und `paired_realization = true`.

Die Control- und Treatment-Bedingung teilen die Seed-gebundene Realisierung. Die zehn Seed-Realisierungen sind unterschiedliche deterministische Parameterisierungen, keine unabhaengigen biologischen Stichproben.

Quelle: `research/experiments/EXP-GEN-0041/DATA/runs_compact.json` und `research/preregistrations/PREREG-SNN-006.json`.

### 4.2 Seed-gebundene Lern- und Datenpfade: EXP-S6-SEM-CL-003

Seed `301` wird fuer jede registrierte Replay-Bedingung verwendet. Pro Bedingung werden unter anderem gespeichert:

- `condition`, zum Beispiel `X20` oder `R05`;
- `task_accuracy_matrix` ueber die fuenf Split-MNIST-Tasks;
- `final_average_accuracy` und `mean_forgetting`;
- `current_task_updates`, `replay_updates` und `total_updates`;
- `stored_by_task` als realisiertes Speicherobjekt-Budget;
- `aborted` und `abort_reason`.

Das Dataset, die Trainings-/Testauswahl, Replay-Auswahl und Bedingungsisolation sind an die eingefrorene CL-003-Konfiguration gebunden. Die Resultate bleiben DATA; `H1_negative_H2_negative` ist eine preregistrierte Klassifikation, keine automatische EVID-Promotion.

Quelle: `research/experiments/EXP-S6-SEM-CL-003/results/results.json`, `runner-summary.json` und `research/preregistrations/operational/EXP-S6-SEM-CL-003.json`.

### 4.3 Seed-gebundene Replikationssignaturen: EXP-REC-002-CLEAN-R2

Die Seeds `7501-7520` werden ueber das vollstaendige Delay-Gitter `1, 2, 4, 8` eingesetzt. Fuer Seed `7501` werden pro Bedingung Signaturen aus den primaeren Metriken gespeichert:

- `loop_delay_1`: `[last_response_latency, recurrent_events, propagation_depth] = [62, 10, 61]`;
- `loop_delay_2`: `[252, 33, 251]`;
- `loop_delay_4`: `[251, 28, 250]`;
- `loop_delay_8`: `[245, 20, 244]`.

Das Protokoll erklaert ausdruecklich, dass diese Seeds deterministische Robustheitswiederholungen sind. Bei einer seed-insensitiven Drei-Neuronen-Konstruktion sind sie nicht als statistisch unabhaengige Stichproben zu interpretieren.

Quelle: `research/experiments/EXP-REC-002-CLEAN-R2-20260919/analysis/statistics.json` und `research/preregistrations/PREREG-REC-002-CLEAN-R2.json`.

### 4.4 Frische Topologie-Replikation: EXP-S1-TOPO-V3-R1

Die frischen Seeds `6201-6220` werden ueber sechs gematchte Topologien eingesetzt. Die DATA enthalten unter anderem:

- Bedingung und Topologiekoordinaten;
- `coordinate_digest`;
- `active_neurons`, `active_output_neurons`;
- zeitaufgeloeste Aktivierungsdaten und `activation_auc_0_32`;
- Latenz- und Output-Metriken;
- die Bindung an 64 Neuronen, 246 Kanten, Gewicht 55 und 128 Evaluations-Ticks.

Die frischen Seeds bilden eine interne Replikation innerhalb derselben Code-/Modellfamilie. Sie sind keine unabhaengige externe Replikation und belegen keine 5D-Ueberlegenheit.

Quelle: `research/experiments/EXP-S1-TOPO-V3-R1-20260918/data/evaluation.json` und `research/preregistrations/PREREG-S1-TOPO-V3-R1-TIME-RESOLVED.json`.

## 5. Seed-Familien im aktuellen Forschungsbestand

| Experiment | Seed-Familie | Seed-Einheit |
|---|---|---|
| Stage-0 Diagnose | `20001-20003` | diagnostische Modell-/Referenzlaeufe |
| Stage-0 Confirmatory V2 | `21001-21003` | gepaarte Konformitaetsbedingungen |
| Stage-0 Promotion-R1 | `22001-22003` | frische interne Promotion-Replikation |
| CL-001 | `101-110` | 10 gepaarte Lern-/Kontrollseeds |
| CL-002 | `201-209` | 9 gepaarte Seeds, keine Ersatzseeds |
| CL-003 | `301-312` | 12 Seeds x 7 Bedingungen = 84 Runs |
| Topologie V2 | `2101-2120` | 20 gepaarte Evaluation-Seeds |
| Topologie V3-R1 | `6201-6220` | 20 frische interne Replikations-Seeds |
| REC-002 Clean R2 | `7501-7520` | 20 Seeds x 4 Delay-Bedingungen = 80 Runs |
| SNN-004 STDP | kein unabhaengiger Seed-Faktor | 11 Timing-Bedingungen x 10 identische Wiederholungen |

Historische Batch-Workflows mit `42-44` bleiben technische/explorative Laufartefakte. Ihre Seed-Zahl darf nicht mit der Seed-Staerke eines konfirmatorischen Protokolls gleichgesetzt werden.

## 6. Reproduzierbarkeit und Grenzen

Ein Seed ermoeglicht die Wiederholung desselben deterministischen Pfades nur unter gleicher Preregistration, gleicher Code-/Config-Version, gleicher Datenquelle, gleicher Bedingung und gleichem Ausfuehrungsvertrag. Ein Seed ersetzt keine unabhaengige Autorenschaft, keine externe Replikation und keine menschliche Review.

Seed-DATA koennen technische Realisierungen und innerhalb-Protokoll-Unterschiede belegen. Sie belegen nicht automatisch biologische Stichproben, Bewusstsein, allgemeine Intelligenz, Generalisierung oder wissenschaftliche EVID.

## 7. Zitier- und Integritaetsregel

Bei wissenschaftlicher Nutzung sind immer Experiment-ID, Seed-Familie, Bedingung, Preregistration, DATA-Pfad und relevante Source-/Config-Digests gemeinsam zu nennen. Rohdaten und historische Artefakte bleiben unveraendert. Eine spaetere Analyse darf Seed-DATA neu auswerten, aber nicht Seed, Bedingung oder Ausfuehrungsprovenienz rueckwirkend umbenennen.
