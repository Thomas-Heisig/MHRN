# Präregistrierung: EXP-S6-SEM-CL-003

**Titel:** Replay-Dosis × Repräsentation bei konstantem Gesamt-Updatebudget auf Split-MNIST

**Status:** Präregistriert, nicht ausgeführt.

**Vorgänger:**

- `EXP-S6-SEM-CL-001`: positiver Mechanismusbefund gegenüber naiver No-Replay-Baseline;
- `EXP-S6-SEM-CL-002`: negativer Befund für einen semantischen Prototyp-Vorteil gegenüber gleich budgetiertem Raw-Replay bei 100 Replay-Updates pro Task-Wechsel.

## 1. Forschungsfrage

**RQ-S6-SEM-003:** Hängt ein möglicher Vorteil semantischer Prototypkonsolidierung gegenüber Raw-Experience-Replay von der Replay-Dosis ab, wenn das **Gesamt-Updatebudget über alle Bedingungen konstant** gehalten wird?

CL-003 testet damit die nach CL-002 offene mechanistische Alternative: Der negative CL-002-Befund könnte ein Regimeeffekt einer zu geringen Replay-Exposition sein. Diese Hypothese wird in einem neuen Experiment getestet; CL-002 wird nicht verändert oder erneut als konfirmatorischer Lauf ausgeführt.

## 2. Hypothesen

### H1 — semantischer Vorteil im CL-001-nahen 20%-Regime

Bei 20% Replay-Replacement erzielt Semantic-Prototype-Replay gegenüber Raw-Replay:

- mindestens +3 Prozentpunkte finale mittlere Accuracy und
- mindestens 5 Prozentpunkte weniger mittleres Forgetting.

Zusätzlich muss Semantic-Prototype-Replay bei 20% die größenangepasste Random-Prototype-Kontrolle um mindestens +3 Prozentpunkte finale Accuracy schlagen.

### H2 — Replay-Dosis-Interaktion

Der Accuracy-Vorteil `Semantic − Raw` ist bei 20% Replay-Replacement mindestens **+1,5 Prozentpunkte größer** als bei 5% Replay-Replacement.

H2 prüft, ob die Repräsentationsdifferenz mit Replay-Exposition sichtbar wird, statt nur einen allgemeinen Replay-Effekt abzubilden.

### H0

Kein praktisch relevanter semantischer Vorteil und keine praktisch relevante Dosis-Interaktion.

### H3 — explorative Gegenhypothese

Raw-Replay bleibt über alle Dosen gleichwertig oder besser. Eine hohe Replay-Dosis kann semantische Kompression sogar verschlechtern, wenn relevante Einzelfallinformation verloren geht.

## 3. Datensatz und gemeinsame Pipeline

- Datensatz: kanonisches MNIST, Split-MNIST mit fünf Tasks: `(0,1)`, `(2,3)`, `(4,5)`, `(6,7)`, `(8,9)`.
- Train: 1000 Beispiele je Klasse.
- Test: 200 Beispiele je Klasse.
- Spike-Encoding: identisch zu CL-001/CL-002: 4×4 Average Pooling auf 7×7, Schwellen `(0.2, 0.4, 0.6, 0.8)`, deterministische sparse Spike-IDs.
- Readout: identischer `OnlineSoftmaxReadout`, Learning Rate `0.025`.
- SemanticMemory: unverändert mit `min_episode_support=8`, `prototype_support=0.30`, `match_threshold=0.25`.
- Keine Testdaten für Training, Speicherwahl, Prototypbildung, Hyperparameterwahl oder Ausschlussentscheidung.

## 4. Seeds

Zwölf neue gepaarte Seeds, die weder in CL-001 noch CL-002 verwendet wurden:

`301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312`

Alle Bedingungen werden für jeden Seed mit identischen Train-/Test-Indizes ausgeführt.

## 5. Bedingungen

### Konfirmatorische Bedingungen

| ID | Repräsentation | Replay-Replacement | Replay-Slots je späterem Task | Gesamtupdates je Seed |
| --- | --- | ---: | ---: | ---: |
| R05 | Raw | 5% | 100 von 2000 | 10.000 |
| S05 | Semantic | 5% | 100 von 2000 | 10.000 |
| R20 | Raw | 20% | 400 von 2000 | 10.000 |
| S20 | Semantic | 20% | 400 von 2000 | 10.000 |
| X20 | Random matched | 20% | 400 von 2000 | 10.000 |

### Präregistrierte Dosis-Erweiterung

| ID | Repräsentation | Replay-Replacement | Replay-Slots je späterem Task | Gesamtupdates je Seed |
| --- | --- | ---: | ---: | ---: |
| R40 | Raw | 40% | 800 von 2000 | 10.000 |
| S40 | Semantic | 40% | 800 von 2000 | 10.000 |

Die 40%-Bedingungen werden vollständig persistiert und präregistriert analysiert, sind aber **nicht Teil der konjunktiven H1-Erfolgsregel**. Sie dienen der Prüfung von Sättigung bzw. möglicher Über-Replay-Verschlechterung.

## 6. Konstantes Updatebudget

Jeder Seed und jede Bedingung besitzt exakt **10.000 Readout-Updates**:

- Task 1: 2000 aktuelle Trainingsupdates, kein Replay;
- Tasks 2–5: jeweils exakt 2000 Update-Slots;
- Replay ersetzt aktuelle Task-Updates, es werden keine zusätzlichen Updates angehängt.

Damit unterscheiden sich Replay-Dosen **nicht** in der Gesamtzahl der Optimierungsschritte.

### Replay-Slot-Positionen

Für jeden `(seed, task_index, dose)` wird vor Bedingungsausführung eine deterministische Slot-Maske erzeugt. Die Replay-Slots werden über die 2000 Positionen möglichst gleichmäßig verteilt; Ties werden deterministisch über einen SHA-256-abgeleiteten Seed aufgelöst.

Für Raw und Semantic derselben Dosis sind die Replay-Slot-Positionen **identisch**. Damit werden innerhalb eines Dosisvergleichs exakt dieselben aktuellen Trainingspositionen ersetzt.

X20 verwendet dieselben Slot-Positionen wie R20/S20.

## 7. Speicherbudget

Die CL-002-A1-Regel bleibt erhalten.

Für Task `t`:

`R_t = min(50, number_of_mature_semantic_prototypes_for_task_t)`

Dann speichern:

- Semantic exakt `R_t` reife Prototypen;
- Raw exakt `R_t` rohe Trainingsrepräsentationen, deterministisch nach aufsteigendem originalen MNIST-Index;
- Random exakt `R_t` objektweise an Semantic gematchte Zufallsrepräsentationen.

Das realisierte Objektbudget ist damit innerhalb jedes Seeds und Tasks identisch.

### Random-Matching

X20 matched jedes semantische Objekt in:

- Task,
- Label,
- Feature-Dimension,
- Spike-Anzahl.

Spike-IDs werden ohne Zurücklegen gleichverteilt aus dem gültigen Feature-Raum gezogen. Random darf keine semantischen IDs, Rohmuster-IDs oder Testinformation verwenden.

## 8. Replay-Auswahl innerhalb der Slots

Zu jedem Zeitpunkt stehen nur Speicherobjekte aus **bereits abgeschlossenen Tasks** zur Verfügung.

Die aktuell verfügbaren Replay-Objekte werden in kanonischer Reihenfolge `(task_index, label, source_rank, spike_ids)` gehalten. Replay-Slots werden deterministisch zyklisch/balanciert über diesen Pool verteilt; die maximale Nutzungsdifferenz zwischen zwei verfügbaren Objekten darf pro Task höchstens 1 betragen.

Kein Sampling anhand aktueller Testleistung oder späterer Task-Ergebnisse.

## 9. Bedingungsreihenfolge und Isolation

Die sieben Bedingungen werden je Seed in einer deterministischen, ausschließlich seed-basierten Permutation ausgeführt.

Jede Bedingung startet mit:

- neu initialisiertem Readout,
- eigenem Memory-Zustand,
- identischen Datensatz-Indizes,
- identischem Encoder,
- gleicher Readout-Initialisierung für denselben Seed.

Es darf kein trainierbarer Zustand zwischen Bedingungen geteilt werden.

## 10. Primäre Endpunkte

Wie CL-001/CL-002:

1. **Final average accuracy** über alle fünf Tasks nach Task 5.
2. **Mean forgetting** für Tasks 1–4: beste historische Task-Accuracy minus finale Task-Accuracy.

## 11. Konfirmatorische Kontraste

### H1-Kontraste bei 20%

C1: `S20 − R20` final average accuracy.

C2: `R20 − S20` mean forgetting. Positive Werte bedeuten weniger Forgetting für Semantic.

C3: `S20 − X20` final average accuracy.

### H2-Dosisinteraktion

C4: `(S20 − R20) − (S05 − R05)` final average accuracy.

## 12. Präregistrierte Erfolgsregeln

### H1 bestätigt nur wenn alle Bedingungen erfüllt sind

- C1 Mittelwert ≥ `+0.03`;
- C2 Mittelwert ≥ `+0.05`;
- C3 Mittelwert ≥ `+0.03`;
- untere Grenze des gepaarten 95%-Bootstrap-KI > 0 für C1, C2 und C3;
- zweiseitiger gepaarter exakter Sign-Flip-Test p < 0.05 für C1, C2 und C3;
- alle 12 Seeds vollständig gepaart.

### H2 bestätigt nur wenn

- C4 Mittelwert ≥ `+0.015`;
- untere Grenze des 95%-Bootstrap-KI > 0;
- zweiseitiger gepaarter Sign-Flip-Test p < 0.05;
- alle 12 Seeds vollständig gepaart.

H1 und H2 werden separat entschieden. Ein positives H2 rettet kein negatives H1 und umgekehrt.

## 13. Präregistrierte 40%-Analyse

Für `S40 − R40` werden final average accuracy und mean forgetting mit demselben Bootstrap/Sign-Flip-Verfahren berichtet.

Die Analyse wird als **preregistered_secondary** markiert. Es gibt keine konfirmatorische Mindestwirkung und sie entscheidet H1/H2 nicht.

Zusätzlich werden die semantischen Raw-Differenzen bei 5%, 20% und 40% deskriptiv nebeneinander berichtet, um Nichtlinearität sichtbar zu machen. Es wird post hoc keine optimale Dosis als konfirmatorische Dosis ausgewählt.

## 14. Statistik

- gepaarter Bootstrap: 20.000 Resamples;
- 95%-KI über Seed-gepaarte Differenzen;
- exakter zweiseitiger Sign-Flip-Test;
- keine automatische Mehrfachtest-Korrektur über C1–C3, da H1 eine **konjunktive** Regel ist und alle drei passieren müssen;
- H2 ist eine separat benannte Hypothese;
- 40%-Analyse sekundär.

## 15. Abbruch- und Missing-Regel

Ein Seed gilt als unvollständig, sobald eine der sieben Bedingungen NaN/Inf erzeugt oder technisch nicht regelkonform beendet wird.

- Teil-DATA und Grund werden persistiert.
- kein automatischer Wiederholungslauf;
- kein Ersatzseed;
- H1/H2 können nur bei 12 vollständig gepaarten Seeds positiv werden;
- bei weniger als 12 vollständigen Seeds: `incomplete_preregistered_run`, deskriptive Analyse erlaubt, keine positive konfirmatorische Entscheidung.

## 16. Pre-execution Freeze

Vor dem ersten empirischen CL-003-Lauf müssen geschrieben, synthetisch getestet und SHA-256-gebunden sein:

- Datensatz-/Indexbildung;
- Spike-Encoding;
- deterministische Replay-Slot-Masken;
- Raw/Semantic/Random-Memory-Bildung;
- Budget-/Updatezähler;
- sieben Bedingungen;
- Endpunktberechnung;
- C1–C4-Berechnung;
- Bootstrap und Sign-Flip;
- H1/H2-Entscheidungslogik;
- 40%-Sekundäranalyse;
- Abort-/Missing-Logik.

Vor Freeze sind nur synthetische Testdaten zulässig, die nicht aus MNIST, CL-001, CL-002 oder künftigen CL-003-DATA abgeleitet sind.

## 17. Was CL-003 nicht testet

- keinen vollständigen rekurrenten MHRN-vs-Standard-SNN-Vergleich;
- keine biologische Validität;
- keine Generalisierung auf andere Datensätze;
- keine Optimierung der SemanticMemory-Schwellen;
- keine Auswahl einer „besten“ Replay-Dosis nach Ergebnis;
- keine nachträgliche Rehabilitierung von CL-002.

## 18. Ergebnisinterpretation

| H1 | H2 | Interpretation |
| --- | --- | --- |
| positiv | positiv | semantischer Vorteil im 20%-Regime plus Evidenz für Dosisabhängigkeit |
| positiv | negativ | semantischer Vorteil bei 20%, aber keine Evidenz, dass er gegenüber 5% dosisbedingt größer wird |
| negativ | positiv | Dosis verändert den relativen Effekt, aber 20% erreicht keinen praktisch ausreichenden semantischen Vorteil |
| negativ | negativ | keine konfirmatorische Unterstützung für semantischen Prototyp-Vorteil oder die vorgeschlagene Dosisalternative |

Jede Kombination wird veröffentlicht und bleibt wissenschaftlich verwertbar.

## 19. DATA/EVID/Veröffentlichung

- Roh- und Auswertungs-DATA vollständig persistieren.
- Machine Report bleibt DATA-only.
- Human EVID separat nach DATA-Merge.
- Keine automatische Evidenzpromotion.
- Negative und Nullbefunde werden veröffentlicht.
- Jede Änderung nach erstem empirischem Lauf erfordert eine neue Experiment-ID.

---

**Zusammenfassung:** CL-003 prüft, ob der in CL-002 nicht bestätigte semantische Vorteil bei einer CL-001-näheren Replay-Exposition sichtbar wird, ohne die Zahl der Readout-Updates zu erhöhen. Repräsentation und Replay-Dosis werden getrennt, bevor neue Daten gesehen werden.
