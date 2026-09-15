# Präregistrierungs-Nachtrag A1: EXP-S6-SEM-CL-002

**Status:** Vor Ausführung ergänzt. Kein empirischer Lauf von EXP-S6-SEM-CL-002 hat vor diesem Nachtrag stattgefunden.

**Zweck:** Präzisierung der vier unterbestimmten Punkte der ursprünglichen Präregistrierung, ohne Hypothesen, Endpunkte, Seeds, Erfolgsgrenzen oder Datensatz nach Sichtung empirischer Resultate zu verändern.

## 1. Semantischer Prototyp (B3)

B3 verwendet exakt die bereits in `src/memory/semantic.py` implementierte `SemanticMemory`-Mechanik und die Parameter aus EXP-S6-SEM-CL-001:

- `semantic_min_episode_support = 8`
- `semantic_prototype_support = 0.30`
- `semantic_match_threshold = 0.25`
- semantische Gruppierung über `sensor_id = split-mnist-label-<label>` und `modality = pooled_rate_code`
- ein Spike-Kanal gehört zum Prototyp, wenn sein Episoden-Support geteilt durch die Zahl unabhängiger Episoden des Konzepts mindestens `0.30` beträgt
- ein Konzept ist nur replay-fähig, wenn es mindestens 8 unabhängige Episoden trägt und sein Prototyp nicht leer ist
- die vorhandene Dice-basierte Zuordnung und deterministische Tie-Break-Regel der Implementierung bleiben unverändert

Es wird für CL-002 kein neues Clustering-Verfahren, kein K-Means, kein Medoid und kein nachträgliches Prototyp-Tuning eingeführt.

## 2. Speicherbudget: harte Kapazität und realisierte Gleichheit

Die ursprüngliche Angabe `N = 50 Repräsentationen pro Task` wird präzisiert als **harte Kapazitätsobergrenze**, nicht als Pflicht zum künstlichen Auffüllen auf 50 Objekte.

Für jeden abgeschlossenen Task `t` wird nach B3-Konsolidierung die Zahl replay-fähiger semantischer Prototypen bestimmt:

`R_t = min(50, number_of_mature_B3_prototypes_for_task_t)`

Für denselben Seed und Task müssen danach gelten:

- B3 speichert exakt `R_t` semantische Prototypen,
- B2 speichert exakt `R_t` rohe beobachtete Spike-Muster,
- B4 speichert exakt `R_t` Random-Prototypen.

Damit ist die **realisierte Zahl gespeicherter Replay-Objekte** in B2, B3 und B4 identisch. Falls `R_t = 0`, erhalten B2, B3 und B4 für diesen Task ebenfalls 0 gespeicherte Replay-Objekte.

Die Auswahl bei mehr als 50 reifen B3-Prototypen erfolgt deterministisch in aufsteigender Reihenfolge `(label, concept_id)` und wird auf die ersten 50 begrenzt. B2 wird pro Task deterministisch aus den tatsächlich im Training beobachteten Mustern gewählt: nach aufsteigendem Original-MNIST-Index, begrenzt auf `R_t`. Es gibt kein Nachsampling und keine Ersetzung.

Die maximale Gesamtkapazität nach fünf Tasks beträgt damit 250 Objekte, die tatsächliche Gesamtkapazität ist `sum(R_t)` und in B2/B3/B4 identisch.

## 3. Random-Prototype-Kontrolle (B4)

B4 wird **objektweise an B3 gematcht**. Für jedes gespeicherte B3-Objekt wird genau ein B4-Objekt erzeugt mit:

- demselben Task,
- demselben Klassenlabel,
- exakt derselben Spike-Anzahl,
- derselben möglichen Feature-Dimension wie EXP-S6-SEM-CL-001.

Die Spike-IDs des B4-Objekts werden ohne Zurücklegen gleichverteilt aus allen gültigen Feature-IDs gezogen. Innerhalb eines Random-Prototyps sind daher keine doppelten Spike-IDs zulässig. Die Zufallsquelle ist ausschließlich aus `(seed, task_index, semantic_object_rank)` deterministisch abgeleitet.

B4 darf weder semantische Ähnlichkeit, B3-Spike-IDs, Rohbeispiel-Spike-IDs noch testseitige Informationen für die Auswahl der Spike-IDs verwenden. Gematcht werden nur Task, Label, Objektanzahl, Feature-Dimension und Spike-Anzahl.

## 4. Replay-Updatebudget

`K = 100` bedeutet exakt **100 Replay-Updates pro Task-Wechsel insgesamt** für B2, B3 und B4, sofern mindestens ein Replay-Objekt aus früheren Tasks vorhanden ist.

- Nach Task 1 gibt es vor Task 2 den ersten Replay-Block.
- Es gibt vier Task-Wechsel und damit maximal 400 Replay-Updates pro Seed und Replay-Bedingung.
- Die 100 Replay-Updates werden deterministisch gleichmäßig über alle aktuell gespeicherten Replay-Objekte verteilt: ganzzahliger Quotient plus die ersten Restplätze in kanonischer Objekt-Reihenfolge.
- Die Replay-Updates sind **zusätzliche, aber zwischen B2/B3/B4 exakt identische** Updates. B1 erhält keine Replay-Updates.
- Primärvergleiche B3–B2 und B3–B4 sind damit updatebudgetgleich. B1 bleibt bewusst die naive Referenz und ist nicht updatebudgetgleich mit Replay-Bedingungen.

Diese Präzisierung ersetzt keine Primärhypothese; sie verhindert lediglich verdeckte Unterschiede zwischen den drei Replay-Bedingungen.

## 5. Bedingungsreihenfolge

Die vier Bedingungen werden pro Seed in einer deterministischen Permutation ausgeführt, die ausschließlich aus dem Seed abgeleitet wird. Diese Reihenfolge darf keine Auswirkung auf gemeinsam genutzte Modellzustände haben: Jede Bedingung startet mit einem vollständig neu initialisierten Readout und eigenem Memory-Zustand. Datensatz-Splits und train/test Indizes sind für alle Bedingungen eines Seeds identisch.

## 6. Abgebrochene Seeds

Ein Seed gilt als **abgebrochen**, sobald in einer der vier Bedingungen ein präregistriertes Abbruchkriterium ausgelöst wird. Dann gilt:

1. Alle bis dahin erzeugten Daten und der konkrete Abbruchgrund werden persistiert.
2. Der Seed wird **nicht** automatisch erneut ausgeführt.
3. Der Seed wird nicht durch einen neuen Seed ersetzt.
4. Die konfirmatorische Erfolgsregel verlangt weiterhin mindestens 9 vollständig gepaarte Seeds. Da exakt 9 Seeds präregistriert sind, bedeutet jeder nicht aufgelöste Abbruch, dass das Experiment **keinen positiven konfirmatorischen Befund** liefern kann.
5. Deskriptive Auswertung der verbleibenden vollständigen Seeds ist zulässig, aber als `incomplete_preregistered_run` bzw. explorativ zu kennzeichnen.
6. Ein technischer Wiederholungslauf desselben Seeds ist nur nach dokumentierter Protokollabweichung zulässig und darf nicht stillschweigend in die konfirmatorische Analyse eingehen. Über seine Verwendbarkeit entscheidet die spätere menschliche EVID-Prüfung.

## 7. Analyse-Freeze vor Daten

Vor `execution_authorized=true` müssen vollständig implementiert und gehasht sein:

- Datenaufbereitung und Split-MNIST-Indexbildung,
- Spike-Encoding,
- B1/B2/B3/B4 Runner,
- Budgetabrechnung,
- Seed-/Bedingungs-Permutation,
- Berechnung von final average accuracy und mean forgetting,
- gepaarter Bootstrap mit 20.000 Resamples,
- zweiseitiger gepaarter Sign-Flip-Test,
- konjunktive Erfolgsregel,
- Abort-/Missing-Seed-Logik.

Die Statistik-Pipeline wird vor dem ersten empirischen Lauf nur mit synthetischen, nicht aus MNIST oder CL-001/CL-002 abgeleiteten Testdaten geprüft.

## 8. Unveränderte Punkte

Unverändert bleiben insbesondere:

- Forschungsfrage RQ-S6-SEM-002,
- Seeds 201–209,
- Split-MNIST mit fünf Tasks,
- primäre Endpunkte,
- drei Primärkontraste,
- Effektgrenzen +0.03 / +0.05 / +0.03,
- Bootstrap 20.000 / 95 %, untere Grenze > 0,
- gepaarter zweiseitiger Sign-Flip-Test p < 0.05,
- keine automatische DATA→EVID-Promotion,
- Veröffentlichung auch bei Null- oder Negativbefund.

Dieser Nachtrag wurde **vor Implementierung und Ausführung des CL-002-Runners** eingefroren.