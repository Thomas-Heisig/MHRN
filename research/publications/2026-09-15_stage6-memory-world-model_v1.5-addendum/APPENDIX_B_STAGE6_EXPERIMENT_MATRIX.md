# Anhang B — Stage-6-Experiment- und Ablationsmatrix

## B.1 Leitprinzip

Jeder Versuch muss den behaupteten Mechanismus isolieren. Gleiche Seeds, gleiche Trainings-/Interaktionsbudgets und identische Auswertungsfenster sind Pflicht, soweit die jeweilige Behandlung dies zulässt. Ein erfolgreicher Lauf erzeugt DATA. EVID entsteht erst nach den registrierten Promotionskriterien.

## B.2 Experimentmatrix

| ID | Ziel | Hauptbedingungen | Primäre Messgrößen | EVID-relevanter Befund |
|---|---|---|---|---|
| `S6-EPI-001` | neuronaler episodischer Recall nach Delay | memory-on; read-off; shuffled-cue | Recall-Genauigkeit, Cue-Abdeckung, Aufgabenleistung über Delay | Vorteil nach Distraktoren, der bei speicherspezifischer Läsion verschwindet |
| `S6-SEM-001` | Cross-Episode-Semantisierung | semantic-on; episode-only; shuffled episode labels | held-out Klassifikation/Ähnlichkeit, Prototype-Support | Generalisierung auf nicht zur Prototypbildung verwendete Episoden |
| `S6-RPL-001` | Replay/Konsolidierung | off; ordered; shuffled; extra-awake mit gleichem Budget | Retention, Interferenz, held-out Generalisierung | Replay-spezifischer Vorteil gegenüber no-replay und equal-budget awake |
| `S6-PE-001` | Prediction Error als eigener Lernfaktor | PE correct/disabled/shuffled × reward on/off | Aufgabenleistung, Gewichtsdifferenz, Lernkurve | PE-Effekt unabhängig vom Reward-Pfad; Shuffle zerstört gerichteten Vorteil |
| `S6-WM-001` | Mehrschritt-Vorhersage | frozen adaptive; persistence; disabled; shuffled transitions | N-step error, coverage, unknown rate | geringerer held-out Mehrschrittfehler ohne Lernen im Testfenster |
| `S6-WM-002` | Entscheidungsnutzen | correct frozen model; disabled; shuffled model; persistence | Auswahlgenauigkeit, Regret, Erfolgsrate, Coverage | bessere Entscheidung auf zurückgehaltenen Episoden bei gleichem Kandidatenbudget |
| `S6-NWM-001` | neuronales Weltmodell | künftiges spiking state-space model vs statistische Baseline | N-step error, task utility, Spike-/State-Diagnostik | neuronaler Zustand trägt prädiktive Information und funktionalen Nutzen |

## B.3 `S6-EPI-001` — Delay + Distraktor

**Frage:** Bleibt aufgabenrelevante Information in einer neuronalen Episode über Distraktoren nutzbar?

**Design:** Ein Cue wird durch das reale SNN kodiert. Danach folgen vorab registrierte Distraktorintervalle. Der Probe-Cue enthält nur einen Teil des ursprünglichen sparse Musters. Die Zielvariable darf nicht aus `EpisodeRecord.frame_payload` direkt als Antwort gelesen werden.

**Kontrollen:**
- vollständiger Memory-Pfad,
- Read-Läsion bei unverändertem Write-Pfad,
- Cue-Shuffle innerhalb desselben Seeds,
- optional Write-Läsion als separate Mechanismuskontrolle.

## B.4 `S6-SEM-001` — Held-out Semantik

Trainingsepisoden und Testepisoden müssen disjunkt sein. Die zentrale Frage lautet nicht, ob ein gespeicherter Trainingsvektor wiedergefunden wird, sondern ob ein über mehrere Episoden gebildeter Prototyp neue Exemplare derselben Struktur besser erfasst als Kontrollen.

## B.5 `S6-RPL-001` — Konsolidierung

Replay muss gegen **gleich budgetiertes zusätzliches Wachtraining** verglichen werden. Andernfalls wäre ein beobachteter Vorteil lediglich durch zusätzliche Updates erklärbar. `shuffled` kontrolliert die Informationsstruktur, `off` das Fehlen von Replay.

## B.6 `S6-PE-001` — Prediction Error unabhängig von Reward

Prediction Error und Reward werden faktoriell getrennt. Für jede PE-Bedingung wird derselbe Reward-Zustand verwendet. Ein PE-Effekt gilt nur als mechanistisch interpretierbar, wenn Reward-Zähler und Reward-Signal nicht verdeckt verändert werden.

## B.7 `S6-WM-001/002` — Frozen Evaluation

Training und Evaluation sind strikt getrennt. Im Evaluationsfenster ist `learning_enabled=false`; das Modell wird eingefroren. Jede Behandlung erhält dieselben Initialzustände, Kandidatenfolgen, Horizonte und Auswertungsbudgets.

Der neue `OfflineDecisionEvaluator` darf lediglich Modellrollouts bewerten. Seine Empfehlung darf in dieser Experimentstufe keine reale Aktorik auslösen. Zunächst wird offline gegen die bekannten späteren Outcomes verglichen.

## B.8 Statistik und Replikation

Für confirmatorische Promotion wird eine vorab registrierte Seedzahl benötigt; als Standardziel gelten mindestens 20 unabhängige Initialisierungsseeds, sofern eine Poweranalyse keine andere Zahl begründet. Berichtet werden mindestens Effektgröße, Konfidenzintervall, Einzel-Seed-Verteilung und negative/null Befunde. Mehrere Messgrößen werden vorab als primär oder sekundär markiert.

## B.9 Abbruch- und Negativkriterien

Ein Versuch wird nicht als positiver Nachweis gewertet, wenn:

- Train/Test-Leakage vorliegt,
- eine Kontrolle weniger Compute-/Update-Budget erhält,
- während frozen evaluation weiter gelernt wird,
- ein unbekannter Modellzustand stillschweigend als korrekte Vorhersage zählt,
- Reward und Prediction Error nicht getrennt protokolliert sind,
- ausschließlich technische Unit-Tests anstelle eines aufgabenbezogenen Outcomes vorliegen.
