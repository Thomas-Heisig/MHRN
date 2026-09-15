# Präregistrierung: EXP-S6-SEM-CL-002

**Titel:** Semantische Prototypkonsolidierung vs. Raw-Experience-Replay bei identischem Speicher- und Updatebudget auf Split-MNIST

**Status:** Präregistriert, nicht ausgeführt.

**Vorgänger:** EXP-S6-SEM-CL-001 (positiver Mechanismus-Befund gegen naive Online-Baseline ohne Replay)

## 1. Forschungsfrage

**RQ-S6-SEM-002:** Liefert die semantische Prototypkonsolidierung von MHRN gegenüber gleich budgetiertem Raw-Experience-Replay einen messbaren Vorteil bei der Reduktion katastrophalen Vergessens?

Dieses Experiment trennt einen möglichen **Semantik-Effekt** von einem allgemeinen **Replay-Effekt**. Fällt B3 gegenüber B2 nicht überlegen aus, darf der positive Effekt aus EXP-S6-SEM-CL-001 nicht der semantischen Verdichtung zugeschrieben werden.

## 2. Hypothesen

**H1 (gerichtet):** Bei identischem Speicherbudget, identischem Updatebudget und identischem Readout reduziert die semantische Prototypkonsolidierung das mittlere Vergessen stärker als Raw-Experience-Replay und verbessert gleichzeitig die finale Accuracy.

**H0:** Kein Unterschied zwischen Semantic-Prototype und Raw-Experience-Replay.

**H2 (explorativ, gegenläufig):** Raw-Experience-Replay ist gleichwertig oder besser, weil reale Erfahrung mehr Information trägt als verdichtete Prototypen.

## 3. Bedingungen

Vier Bedingungen verwenden denselben Readout, dieselbe deterministische Spike-Repräsentation, dieselben Seeds und dieselbe Task-Reihenfolge.

| Bedingung | Speicher | Update-Regel | Budget |
| --- | --- | --- | --- |
| **B1 – Naive Online** | keiner | keine Replay-Updates | 0 Repräsentationen, 0 Replay-Schritte |
| **B2 – Raw-Replay** | N rohe Spike-Muster vergangener Tasks | Replay der Rohmuster | N Repräsentationen, K Replay-Schritte |
| **B3 – Semantic-Prototype** | N semantische Prototypen | Replay der Prototypen | N Repräsentationen, K Replay-Schritte |
| **B4 – Random-Prototype** | N zufällige, größenangepasste Spike-Muster | Replay der Zufallsmuster | N Repräsentationen, K Replay-Schritte |

B4 ist eine notwendige Negativkontrolle: Wenn B3 B4 nicht schlägt, kann der Effekt nicht überzeugend der semantischen Struktur der Prototypen zugeschrieben werden.

### Feste Budgets

- **N = 50 Repräsentationen pro Task** in B2, B3 und B4.
- **K = 100 Replay-Schritte pro Task-Wechsel** in B2, B3 und B4.
- **M = 5 Tasks**: (0,1), (2,3), (4,5), (6,7), (8,9).
- Keine Bedingung darf zusätzliche Readout-Updates, zusätzliche Trainingsbeispiele oder versteckte Speicherobjekte erhalten.

## 4. Präregistrierte Seeds

Die Seed-Liste ist vor Ausführung fixiert:

`201, 202, 203, 204, 205, 206, 207, 208, 209`

Damit gilt **n = 9 gepaarte Seeds** für alle vier Bedingungen.

Die Bedingungsreihenfolge wird pro Seed deterministisch aus dem jeweiligen Seed permutiert. Die Permutationsfunktion und alle abgeleiteten Zufallsquellen werden im Analysecode vor Ausführung fixiert.

## 5. Primäre Endpunkte

1. **Final average accuracy** nach Task 5 über alle fünf Tasks.
2. **Mean forgetting** über Tasks 1–4 nach Abschluss der Sequenz.

Berechnung, Spike-Encoding, Task-Splits und Readout entsprechen EXP-S6-SEM-CL-001, soweit diese Präregistrierung keine explizite Änderung festlegt.

## 6. Konfirmatorische Vergleiche

Die drei vorab festgelegten Primärdifferenzen sind:

1. `accuracy(B3) - accuracy(B2)`
2. `forgetting(B2) - forgetting(B3)` — positiv bedeutet weniger Vergessen durch B3.
3. `accuracy(B3) - accuracy(B4)`

Keine andere Differenz kann nachträglich als primärer Endpunkt deklariert werden.

## 7. Präregistrierte Erfolgsregel

EXP-S6-SEM-CL-002 zählt nur dann als **positiver Befund für einen Semantik-Effekt**, wenn **alle** folgenden Bedingungen erfüllt sind:

1. `accuracy(B3) - accuracy(B2) >= 0.03`
2. `forgetting(B2) - forgetting(B3) >= 0.05`
3. `accuracy(B3) - accuracy(B4) >= 0.03`
4. Untere Grenze des gepaarten 95-%-Bootstrap-Konfidenzintervalls ist für **jede** dieser drei Differenzen > 0.
5. Zweiseitiger gepaarter Sign-Flip-Test ergibt für **jede** der drei Differenzen `p < 0.05`.
6. Mindestens neun vollständig gepaarte Seeds liegen vor; keine selektive Seed-Auswahl ist zulässig.

### Ergebnisinterpretation

- Bedingungen 1–3 sowie Statistik erfüllt: **preregistered_positive_semantic_effect**.
- B3 ≈ B2, aber beide schlagen B4/B1: **replay_effect_without_semantic_advantage**.
- B3 ≈ B2 ≈ B4: **budget_or_generic_replay_effect**.
- B3 schlechter als B2: **negative_evidence_for_prototype_advantage**.
- Uneindeutige Statistik ohne klare Gegenrichtung: **null_or_inconclusive_result**.

## 8. Falsifikationskriterien

H1 gilt als falsifiziert, wenn mindestens eines gilt:

- B3 ist gegenüber B2 in der finalen Accuracy nicht signifikant positiv.
- B3 reduziert Forgetting gegenüber B2 nicht signifikant.
- B3 schlägt B4 in der finalen Accuracy nicht signifikant.
- B3 ist in finaler Accuracy oder Forgetting klar schlechter als B2.

Ein falsifizierendes Ergebnis wird persistiert, ausgewertet und publizierbar dokumentiert. Es wird nicht verworfen und nicht durch Wiederholung mit geänderten Parametern ersetzt.

## 9. Ausführungsprotokoll

- **Datensatz:** Split-MNIST, 5 Tasks, identisch zu EXP-S6-SEM-CL-001.
- **Spike-Repräsentation:** identische deterministische pooled rate coding-Repräsentation wie EXP-S6-SEM-CL-001.
- **Readout:** identischer Online-Softmax-Readout wie EXP-S6-SEM-CL-001.
- **Train/Test-Sampling:** identische Logik wie EXP-S6-SEM-CL-001; seedspezifisch deterministisch.
- **Seeds:** 201–209, identisch über alle Bedingungen.
- **Bedingungsreihenfolge:** seedspezifisch randomisiert, aber deterministisch reproduzierbar.
- **Speicherbudget:** exakt N = 50 Repräsentationen pro vergangenem Task in B2/B3/B4.
- **Replaybudget:** exakt K = 100 Replay-Updates pro Task-Wechsel in B2/B3/B4.
- **Abbruch:** NaN/Inf, ungültige Dimensionen, Budgetverletzung oder Datenintegritätsfehler führen zum dokumentierten Abbruch des betroffenen Seeds; keine stille Wiederholung.

## 10. Definition der Speicherbedingungen

### B2 – Raw-Replay

Aus den abgeschlossenen Tasks werden rohe, tatsächlich beobachtete Spike-Muster gespeichert. Die Auswahlregel wird vor Ausführung deterministisch fixiert. Pro Task dürfen maximal N = 50 gespeicherte Repräsentationen existieren. Replay zieht ausschließlich aus diesen gespeicherten Mustern.

### B3 – Semantic-Prototype

MHRN `SemanticMemory` konsolidiert unabhängige Episoden zu semantischen Prototypen. Für den Benchmark wird die Repräsentation auf maximal N = 50 Replay-Einheiten pro Task begrenzt. Falls mehr reife Konzepte existieren, wird die vorab fixierte deterministische Auswahlregel angewendet; falls weniger existieren, darf die Bedingung nicht mit zusätzlichen Rohmustern aufgefüllt werden.

### B4 – Random-Prototype

Für jedes semantische Replay-Objekt wird ein zufälliges Kontrollmuster erzeugt, dessen Spike-Anzahl an die Größenverteilung der B3-Prototypen angepasst wird. Die Zufallsquelle ist seedspezifisch und vor Ausführung festgelegt. Labels und Budgets entsprechen B3. B4 darf keine semantischen Ähnlichkeitsinformationen oder Rohbeispiele verwenden.

## 11. Statistik

Für jede primäre Differenz:

- gepaarte Differenz pro Seed,
- Mittelwert der Differenzen,
- 95-%-Bootstrap-KI über gepaarte Seeds,
- zweiseitiger gepaarter Sign-Flip-Test,
- vollständige seedweise Ergebnistabelle.

Bootstrap-Resamples: **20.000**.

Signifikanzniveau: **alpha = 0,05**.

Es gibt keine nachträgliche Korrektur der drei Primärtests durch Auswahl eines günstigeren Tests. Da die Erfolgsregel alle drei Tests gleichzeitig verlangt, fungiert die Konjunktion als strenge Entscheidungsschranke. Explorative weitere Vergleiche werden separat markiert.

## 12. Was dieses Experiment nicht testet

- keine biologische Validität der Semantisierung,
- keine Übertragbarkeit auf CIFAR, N-MNIST oder andere Datensätze,
- keine Überlegenheit des vollständigen rekurrenten MHRN-SNN gegenüber Standard-SNNs,
- kein Vergleich mit EWC, SI, GEM, LwF oder anderen etablierten Continual-Learning-Methoden,
- keine Aussage über Bewusstsein, Intelligenz oder biologische Gleichwertigkeit.

## 13. Daten- und Evidenzregeln

- **DATA:** Rohlogs, Seeds, Task-Matrizen, Budgets, gespeicherte Repräsentationsmetadaten, Zustands-/Quellhashes.
- **EVID:** separate menschlich geprüfte Interpretation.
- Analysecode wird vor dem ersten Datenlauf fixiert und über SHA-256 gebunden.
- Präregistrierung wird vor dem ersten Datenlauf nicht mehr inhaltlich geändert. Korrekturen danach benötigen ein Amendment mit Zeitstempel und Begründung.
- Keine Post-hoc-Änderung von Metriken, Ausschlussregeln, Seeds, N, K oder Erfolgsgrenzen.
- Post-hoc-Analysen sind zulässig, müssen aber explizit als **explorativ** markiert werden.
- Automatische DATA→EVID-Promotion bleibt deaktiviert.

## 14. Veröffentlichungsregel

Positiv:

`research/publications/2026-XX-XX_semantic-vs-raw-replay/`

Negativ/falsifiziert:

`research/publications/2026-XX-XX_semantic-vs-raw-replay-negative/`

Null/uneindeutig:

`research/publications/2026-XX-XX_semantic-vs-raw-replay-null/`

Jede Fassung enthält Präregistrierung, vollständige DATA, EVID, Protokollabweichungen, statistische Auswertung und Interpretation.

---

> Dieses Experiment entscheidet, ob der positive Befund aus EXP-S6-SEM-CL-001 ein MHRN-spezifischer Semantik-Beitrag ist oder im Wesentlichen ein Replay-/Budget-Effekt. Die Entscheidungskriterien sind vor der Ausführung festgelegt, nicht danach.
