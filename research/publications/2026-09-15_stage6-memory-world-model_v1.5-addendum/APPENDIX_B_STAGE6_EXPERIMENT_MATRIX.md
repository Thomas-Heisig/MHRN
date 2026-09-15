# Anhang B — Stage-6-Experiment- und Ablationsmatrix

## B.1 Leitprinzip

Jeder Versuch muss den behaupteten Mechanismus isolieren. Gleiche Seeds, kontrollierte Trainings-/Interaktionsbudgets und identische Auswertungsfenster sind Pflicht, soweit die Behandlung dies zulässt. Ein erfolgreicher Lauf erzeugt DATA. EVID entsteht erst nach registrierten Promotionskriterien und menschlicher wissenschaftlicher Prüfung.

## B.2 Implementierte Experimentmatrix

| ID | Ziel | Hauptbedingungen | Primäre Messgrößen | Status / EVID-relevanter Befund |
|---|---|---|---|---|
| `S6-EPI-001` | neuronaler episodischer Recall nach Delay | intact; read-off; write-off; episode-shuffle | Accuracy, Retrievals, Distraktor-Spikes | **implementiert**; Vorteil nach Distraktoren muss gegenüber Lesion/Shuffle bestehen |
| `S6-SEM-001` | Cross-Episode-Semantisierung | intact; label-shuffle; no-semantic | held-out Accuracy, Matches, mature concepts | **implementiert**; Generalisierung auf disjunkte Episoden erforderlich |
| `S6-RPL-001` | Replay/Reaktivierung | no-replay; ordered; shuffled; equal-budget-awake | Reaktivierungsfidelity, mature concepts, Budgetgleichheit | **implementiert**; Replay-spezifischer späterer Retentions-/Generalisierungsvorteil bleibt stärkere Schwelle |
| `S6-PE-001` | Prediction Error als eigener Lernfaktor | PE correct/disabled/shuffled × reward on/off | Gewichtsdifferenz, PE-Updates, Reward Calls | **implementiert**; PE-Effekt muss vom Reward-Pfad getrennt bleiben |
| `S6-WM-001` | Mehrschritt-Vorhersage der statistischen Referenz | frozen-correct; frozen-shuffled; persistence; no-model | exact final-state rate, mean absolute final-state error, coverage | **implementiert**; frozen Referenz, nicht neuronale Evidenz |
| `S6-WM-002` | offline Entscheidungsnutzen der statistischen Referenz | correct; disabled; shuffled; persistence | Utility Ratio, Utility, Recommendations | **implementiert**; keine Aktor-Autorität |
| `S6-NWM-001` | erster spikender Übergangsmodell-Kandidat | spiking-trained; spiking-untrained; target-shuffled; statistical-reference | exact accuracy, coverage, latency, weight margin | **implementiert**; exact-context STDP-Assoziator, keine unbekannte Zustands-Generalisation |

## B.3 `S6-EPI-001` — Delay + Distraktor

Ein Schlüssel und die Zielklasse werden als reale SNN-Spikes kodiert. Danach folgen reale Distraktor-Spikes. Beim Abruf wird nur der Schlüssel erneut stimuliert. Die Antwort wird aus den Spike-IDs der abgerufenen neuronalen Episode dekodiert.

**Verbotene Leakage-Pfade:**
- Zielwert aus `frame_payload`,
- Zielwert aus `actual_state`,
- direkte Datenbankabfrage nach der korrekten Trial-ID als Antwortmechanismus.

**Kontrollen:** intact, read-off, write-off und episode-shuffle.

## B.4 `S6-SEM-001` — Held-out Semantik

Trainingsepisoden und Testepisoden sind disjunkt. Ein semantischer Prototyp muss neue neuronale Exemplare besser klassifizieren als label-shuffle und no-semantic. Ein positiver Engineering-Lauf ist noch kein Nachweis menschlicher oder biologischer Semantik.

## B.5 `S6-RPL-001` — Replay und Reaktivierung

Gespeicherte Episodenmuster werden tatsächlich erneut in ein SNN injiziert. Geordnetes Replay wird gegen No-Replay, zeitlich gemischtes Replay und `equal_budget_awake` verglichen. Das SNN-Schrittbudget wird explizit protokolliert.

Die aktuelle Reaktivierung ist **kein Schlafmodell**. Für einen stärkeren Konsolidierungsbefund muss Replay zusätzlich eine spätere Retention oder Generalisierung gegenüber der gleich budgetierten Wachkontrolle verbessern.

## B.6 `S6-PE-001` — Prediction Error unabhängig von Reward

Prediction Error und Reward sind faktoriell getrennt. Der Prediction-Error-Pfad verwendet Eligibility-Traces, ruft jedoch nicht `LearningEngine.set_reward()` auf. Reward Calls werden als eigene Messgröße protokolliert.

Ein gerichteter PE-Befund ist nur interpretierbar, wenn die deaktivierte und gemischte PE-Kontrolle sowie Reward on/off denselben übrigen Versuchsvertrag behalten.

## B.7 `S6-WM-001/002` — eingefrorene statistische Referenz

`S6-WM-001` prüft mehrere Übergangsschritte unter eingefrorener Evaluation. `S6-WM-002` bewertet alternative Modellrollouts ausschließlich offline. Die Ausgabe des Evaluators ist eine Forschungs-Empfehlung, kein `ActionCommand`.

Diese beiden Protokolle messen die Leistungsfähigkeit einer transparenten statistischen Referenz und dürfen nicht als neuronales Weltmodell bezeichnet werden.

## B.8 `S6-NWM-001` — spikender Übergangsassoziator

Der neue Kandidat besitzt ein Kontextneuron je diskretem Zustand/Aktion-Paar und Ausgangsneuronen für Folgezustände. Kontext→Ausgangsgewichte werden über den vorhandenen Pair-STDP-Pfad trainiert. Bei der Inferenz wird ausschließlich das Kontextneuron stimuliert; die Vorhersage wird nur aus realen Ausgangsspikes dekodiert. Lernen ist während Inferenz und Inferenz-Cooldown deaktiviert.

Kontrollen:
- trainierter spikender Kandidat,
- untrainierter spikender Kandidat,
- spikender Kandidat mit falscher Zielzuordnung,
- statistische Referenz.

Der Versuch prüft **exact-context neuronale Übergangsassoziation**. Er prüft noch keine Generalisation auf unbekannte Zustände, keine verteilte Zustandsrepräsentation und keine rekursive neuronale Mehrschrittvorhersage.

## B.9 Preregistrierung, Statistik und Replikation

Alle sieben Protokolle liegen im dedizierten 1:n-Stage-6-Registry-Vertrag und im eingefrorenen Bundle `stage6_bundle_v1.json`. Der Engineering-Snapshot verwendet drei eindeutige Seeds. Für eine confirmatorische Promotion gilt als Standardziel mindestens 20 unabhängige Initialisierungsseeds, sofern eine Poweranalyse keine andere Zahl begründet.

Berichtet werden mindestens Einzel-Seed-Verteilungen, Effektgrößen beziehungsweise relevante Kontraste, Unsicherheitsintervalle und negative/null Befunde. Die drei Seeds des Engineering-Snapshots dienen der Reproduzierbarkeits- und Pipelineprüfung und schließen keine Forschungsfrage.

## B.10 Abbruch- und Negativkriterien

Ein Versuch wird nicht als positiver wissenschaftlicher Nachweis gewertet, wenn:

- Train/Test- oder Ziel-Leakage vorliegt,
- eine Kontrollbedingung ein systematisch anderes Budget erhält, ohne dass dies Teil der Manipulation ist,
- während einer als frozen deklarierten Evaluation weiter gelernt wird,
- ein unbekannter Zustand stillschweigend als korrekte Vorhersage zählt,
- Reward und Prediction Error nicht getrennt protokolliert sind,
- der spikende Weltmodell-Kandidat nur bekannte IDs nachschlägt, ohne dass die Vorhersage als Netzwerkspike entsteht,
- ausschließlich technische Unit-Tests statt aufgabenbezogener Outcomes vorliegen,
- oder DATA ohne registrierte menschliche Prüfung zu EVID hochgestuft werden.
