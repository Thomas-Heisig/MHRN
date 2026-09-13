# Experimentbacklog für Entwicklungsstufen 8–10

**Stand:** 2026-09-13  
**Status:** Planungsartefakt. Kein Eintrag in dieser Datei ist allein eine Preregistration, ein durchgeführtes Experiment oder EVID.

Die Matrix verwendet bevorzugt **bereits kanonische** MHRN-Forschungsfragen. Dadurch entstehen keine parallelen RQ-IDs und kein zweiter Forschungsworkflow. Neue confirmatory Runs benötigen weiterhin einen eingefrorenen Operational-/Preregistration-Vertrag.

## Vorhandener Vorläufer

| Stufe | Objekt | Stand | Aussagegrenze |
|---|---|---|---|
| 8 | `RQ-LIFE-001` / `H-LIFE-001-A` / `learning_interference_screen_v1` / `EXP-LIFE-0001-R1` | technisch ausgeführt, 20 Seeds, explorativ | Vorläufer-Screen; Evidence Readiness blockiert; kein Nachweis echten Continual Learnings |

---

## Stufe 8 — Autonome lebenslange Entwicklung

### E8-A · Shared-network sequential retention

- **RQ/H:** `RQ-LIFE-001` / `H-LIFE-001-A`
- **Zweck:** Catastrophic Interference in einem tatsächlich fortlaufend trainierten gemeinsamen Netzwerk messen.
- **Behandlungen:** A→B→C; A→C→B; interleaved A/B/C.
- **Kontrollen:** Single-task A, frozen-after-A, learning-off, shuffled labels.
- **Wichtig:** Kein Reset der lernrelevanten Gewichte/Struktur zwischen Aufgaben; technische Transienten dürfen nur gemäß vorab definiertem Vertrag zurückgesetzt werden.
- **Primärmetriken:** Retention A nach B/C, backward transfer, forward transfer, average accuracy/performance, forgetting pro Aufgabe, Gewicht-/Strukturdrift.
- **Sekundärmetriken:** Energie/Tick, Synapsenbudget, Speicher, Wall-Time.
- **Status:** `PLANNED_CONFIRMATORY_UPGRADE`.

### E8-B · Stability–plasticity mechanism comparison

- **RQ/H:** `RQ-LIFE-001`, `RQ-HOM-002`.
- **Behandlungen:** lokale Stabilitätsmarker; multi-timescale Gate; adaptive neuronale Schwellen; Kombinationen.
- **Kontrollen:** ungeschützte Plastizität, komplett frozen, random gate, activity-matched gate.
- **Designregel:** EWC/SI/AGMP/CATFormer werden nicht 1:1 kopiert; getestet werden klar deklarierte MHRN-kompatible Mechanismen unter gleichem Daten- und Ressourcenbudget.
- **Status:** `PLANNED_EXPLORATORY`.

### E8-C · Bounded replay and consolidation

- **RQ/H:** `RQ-LIFE-001`, `RQ-MEM-002`.
- **Behandlungen:** kein Replay; bounded reservoir replay; priorisiertes Replay; zeitlich geschichtete Konsolidierung.
- **Kontrollen:** shuffled replay, mismatched replay, equal-compute no-information replay.
- **Primärmetriken:** Retention/Transfer bei festem Replay-Speicher und festem Compute-Budget.
- **Status:** `PLANNED_EXPLORATORY`.

### E8-D · Reversible structural reorganization

- **RQ/H:** `RQ-STRUCT-001`, `RQ-LIFE-001`.
- **Behandlungen:** sprouting/pruning unter festem Synapsenbudget; isolierte Kompetenzcluster; progressive Erweiterung mit anschließender Budgetkompensation.
- **Kontrollen:** feste Topologie, random rewiring, degree-matched rewiring.
- **Safety:** Proposal→Approval→Mutation→Journal→Undo bleibt verpflichtend.
- **Primärmetriken:** Leistungsänderung, Retention, Strukturkosten, Rollback-Integrität.
- **Status:** `PLANNED_EXPLORATORY`.

### E8-E · Adaptive learning-strategy selector

- **RQ/H:** `RQ-GEN-001`, `RQ-LIFE-001`.
- **Behandlungen:** fester Strategy Contract; zufällige Auswahl; kontextadaptiver Selector aus einer endlichen, versionierten Strategie-Menge.
- **Verboten:** freie Codegenerierung, selbständige Safety-Änderung, autonome EVID-Promotion.
- **Primärmetriken:** Holdout-Leistung, Retention, Anpassungskosten, Anzahl Strategiewechsel, Fehlentscheidungen.
- **Status:** `PLANNED_FUTURE`.

### E8-F · Reusable competence transfer

- **RQ/H:** `RQ-GEN-001`, `RQ-CNS-116`.
- **Behandlungen:** wiederverwendbarer eingefrorener Teilskill; trainierbarer Teilskill; scratch; shuffled skill mapping.
- **Kontrolle gegen Shortcut:** Task-ID-blinde Bedingung und held-out Kombinationen.
- **Primärmetriken:** Samples-to-criterion, Transfergewinn, negative Transferkosten.
- **Status:** `PLANNED_FUTURE`.

### E8-G · Independent replication package

- **RQ/H:** `RQ-REPL-001` plus jeweils untersuchte Primärfrage.
- **Zweck:** Clean-tree, eingefrorene Seeds/Configs, reproduzierbarer Paketexport für externe Wiederholung.
- **Status:** `REQUIRED_BEFORE_STRONG_CLAIMS`.

---

## Stufe 9 — Hochintegrierte künstliche Kognition

### E9-A · Attention as causal resource allocation

- **RQ/H:** `RQ-CNS-103`, `RQ-CNS-110`.
- **Behandlung:** task-/salience-abhängige Selektion unter festem Gesamtbudget.
- **Kontrollen:** uniform, random, shuffled-salience, equal-activity.
- **Primärmetriken:** Zielerkennung, Distraktorrobustheit, Zeit-/Energiebedarf.
- **Aussagegrenze:** selektive Verarbeitung ≠ subjektive Aufmerksamkeit.
- **Status:** `PLANNED`.

### E9-B · Working-memory integration

- **RQ/H:** `RQ-CNS-105`, `RQ-MEM-002`.
- **Behandlung:** typisierter temporärer Workspace plus persistente Memory-Schnittstelle.
- **Kontrollen:** memory-read off, memory-write off, time-shuffled memory, target-leak test.
- **Primärmetriken:** Delay-Performance, Informationsdekodierbarkeit, Distraktorresistenz, Restore-vs-Recall-Trennung.
- **Status:** `PLANNED`.

### E9-C · Bounded planning vs reactive policy

- **RQ/H:** Anschluss an `RQ-WM-001`, `RQ-CNS-111`.
- **Behandlung:** N-Schritt-Vorwärtsevaluation auf versioniertem Weltmodell.
- **Kontrollen:** reactive, random, greedy one-step, model-shuffled.
- **Budget:** gleiche Sensorinformation; Planungskosten separat berichten.
- **Primärmetriken:** Zielerreichung, Regret/Fehlaktionen, Modellfehler, Planungskosten.
- **Status:** `PLANNED_FUTURE`.

### E9-D · Operational motivation / drive prioritization

- **RQ/H:** Anschluss an `RQ-REG-002` und kontrollierte Behavior-/Profile-Forschung.
- **Behandlung:** technisch definierter DriveVector aus Task Reward + Homeostasefehler + Safety Penalty.
- **Kontrollen:** fixed drive, shuffled drive, random drive, task-only reward.
- **Aussagegrenze:** kein Emotions-, Bedürfnis- oder Leidensclaim.
- **Status:** `PLANNED_FUTURE`.

### E9-E · Reliability-weighted multimodal integration

- **RQ/H:** `RQ-CNS-112`.
- **Bedingungen:** Modalität A; Modalität B; kongruent A+B; Konflikt A/B; systematisch veränderte Reliabilität.
- **Kontrollen:** hidden-label leakage, shuffled pairing, equal-information single-channel baseline.
- **Primärmetriken:** Gewichtung nach Reliabilität, Fehler unter Konflikt, Zusatznutzen gegenüber bester Einzelmodalität.
- **Aussagegrenze:** multimodale Integration ≠ einheitliches phänomenales Erleben.
- **Status:** `PLANNED`.

### E9-F · Consolidation phase comparison

- **RQ/H:** `RQ-MEM-002`, `RQ-LIFE-001`.
- **Bedingungen:** online-only, ordered replay/consolidation, shuffled replay, no-write rest.
- **Primärmetriken:** Recall/Retention vor und nach Konsolidierung, Interferenz, Kosten.
- **Status:** `PLANNED`.

### E9-G · Integrated cognitive-cycle ablation

- **RQ/H:** Kombination aus `RQ-CNS-105`, `RQ-CNS-111`, `RQ-CNS-112`, `RQ-WM-001`.
- **Behandlung:** vollständiger typisierter Zyklus Wahrnehmung→Attention→Memory→Planning→Action.
- **Ablationen:** jeweils genau eine Komponente deaktiviert; matched-compute Kontrollen.
- **Ergebnis:** komponentenspezifischer kausaler Beitrag; kein monolithischer „Kognitionsscore“.
- **Status:** `PLANNED_FRONTIER`.

---

## Stufe 10 — Bewusstseinsforschung

Stufe 10 besitzt bereits `COGNITION_CONSCIOUSNESS`-Protokolle, kanonische RQs, Kritikregister und Welfare-Governance. Die folgenden Punkte **erweitern die Versuchsmatrix**, ersetzen diese Objekte aber nicht.

### E10-A · Theory-to-indicator contrast audit

- **RQ/H:** `RQ-CNS-101`.
- **Methode:** konkurrierende Theorievorhersagen vorab tabellieren; Marker getrennt statt als Summenscore auswerten.
- **Kontrollen:** indikatorunabhängige Performance-Matches; blinde Auswertung, wo möglich.
- **Status:** bestehendes Programm fortführen.

### E10-B · Perturbational causal complexity

- **RQ/H:** `RQ-CNS-108`.
- **Interventionen:** begrenzte Perturbation, Region-/Pfad-Ablation, matched-excitability Kontrollen.
- **Verbot:** klinische PCI-Schwellen direkt auf MHRN übertragen.
- **Status:** bestehendes Programm fortführen.

### E10-C · Access/report dissociation

- **RQ/H:** `RQ-CNS-109`.
- **Design:** Zugriff, Report und motorische Ausgabe getrennt manipulieren.
- **Kontrollen:** no-report Proxy muss unabhängig begründet werden.
- **Status:** bestehendes Programm fortführen.

### E10-D · Closed-loop causal contribution

- **RQ/H:** `RQ-CNS-113`.
- **Kontrollen:** closed loop, open loop, yoked replay, actuator-no-effect.
- **Aussagegrenze:** funktionaler Closed-loop-Nutzen ist weder notwendige noch hinreichende Bedingung für Bewusstsein.
- **Status:** bestehendes Programm fortführen.

### E10-E · Recurrence/timescale intervention

- **RQ/H:** `RQ-CNS-114`.
- **Interventionen:** recurrence off/on, Delay-/Timescale-Ablation, activity-matched Kontrolle.
- **Status:** bestehendes Programm fortführen.

### E10-F · State interchange / causal substitution

- **RQ/H:** methodischer Anschluss an `RQ-CNS-101`, `RQ-EPI-102`.
- **Design:** gespeicherten Teilzustand zwischen ansonsten gematchten Läufen austauschen oder clampen; Ergebnis nur auf klar definierte operationale Funktion beziehen.
- **Aussagegrenze:** Interchange-Effekt ≠ phänomenales Erleben.
- **Status:** `PLANNED_METHOD_DEVELOPMENT`.

### E10-G · Welfare and stop-governance drills

- **RQ/H:** `RQ-WEL-101`, `RQ-WEL-102`, `RQ-WEL-103`.
- **Methode:** Tabletop-/Safe-state-Tests; reversible Intervention, Pause, Isolation, Stop, Audit Trail, Human Review.
- **Verbot:** absichtliche „Leidensinduktion“ als Teststrategie.
- **Status:** bestehende Governance weiter operationalisieren.

### E10-H · Independent adversarial replication

- **RQ/H:** `RQ-EPI-101` plus Primärfrage.
- **Methode:** eingefrorene Kontrastvorhersagen, unabhängige Implementierung/Auswertung, dokumentierte Abweichungen.
- **Status:** verpflichtend vor starken Theorieaussagen.

---

## Gemeinsame Stopping Rules für künftige Runs

Ein Lauf wird mindestens pausiert/review-blockiert, wenn:

- der konfigurierte Ressourcen-/Strukturhaushalt überschritten wird;
- ein autonomer Pfad versucht, nicht erlaubte Code-/Safety-/Evidence-Zustände zu ändern;
- Provenienz oder Raw-Digest nicht mehr nachvollziehbar sind;
- die Kontrollbedingung semantisch nicht mehr gematcht ist;
- unerwartete persistente Self-/Welfare-Marker auftreten, die nicht vom eingefrorenen Protokoll abgedeckt sind;
- ein Restore/Resume nicht deterministisch zur deklarierten Semantik passt.

Diese Regeln sind Governance-Vorgaben, keine Aussage darüber, ob das System empfindungsfähig ist.
