# Anhang A — Stage-6-Verträge und Implementierungsgrenzen

## A.1 Gegenstände

Stage 6 wird nicht als ein einzelnes Modul behandelt, sondern als sechs unterscheidbare Forschungsobjekte:

| Objekt | Technischer Vertrag | Aktueller Status | Nicht daraus ableitbar |
|---|---|---|---|
| Temporale Spuren | begrenzte Zustands-/Plastizitätsspuren über Ticks | implementiert | Langzeitgedächtnis |
| Episodische Repräsentation | reale sparse SNN-Spikemuster, Episode/Modus/Sensor gebunden | implementiert | hippocampale Äquivalenz |
| Semantische Repräsentation | Prototypen aus Unterstützung über unabhängige Episoden | implementiert | neokortikale Semantik |
| Replay/Konsolidierung | budgetierte `off`/`ordered`/`shuffled`-Selektion | implementiert | biologischer Schlaf oder Reaktivierung im laufenden SNN |
| Prediction Error | eigener eligibility-basierter Lernfaktor | implementiert | Reward oder universeller kortikaler Fehlercode |
| Weltmodell | Ein-Schritt-Baseline plus aktionskonditionierter Mehrschritt-Referenzvertrag | implementiert | neuronales Weltmodell, Planung oder kausales Weltverständnis |

## A.2 Episodisches Gedächtnis

`NeuralEpisodicMemory` speichert Aktivitätsmuster, die aus tatsächlichen Netzwerkresultaten stammen. Eine partielle Cue-Suche arbeitet über Überlappung der sparse Spikemengen. Read und Write sind unabhängig schaltbar; Kapazität und Persistenz sind begrenzt.

Der entscheidende offene Punkt ist die **kausale Nutzbarkeit**: Eine gespeicherte Episode darf nicht allein deshalb als funktionales Gedächtnis gelten, weil sie später technisch wieder auffindbar ist. Für `RQ-MEM-002` muss ein Delay+Distraktor-Protokoll zeigen, dass eine aus SNN-Aktivität rekonstruierte Information eine definierte Aufgabe verbessert und dass eine speicherspezifische Läsion diesen Vorteil entfernt.

## A.3 Semantische Prototypen

`SemanticMemory` zählt Unterstützung je unabhängiger Episode. Mehrfache Traces derselben Episode können den Support nicht aufblasen. Damit ist eine notwendige technische Bedingung für Cross-Episode-Abstraktion implementiert.

Der offene Nachweis ist held-out Generalisierung: Prototypbildung und Testdaten müssen getrennt sein. Eine Wiedererkennung von Trainingsmustern wäre keine hinreichende Semantik-Evidenz.

## A.4 Replay

Der `EpisodicReplayScheduler` trennt die Bedingungen `off`, `ordered` und `shuffled` und begrenzt die Anzahl wiederverwendeter Episoden. Das erlaubt kontrollierte Konsolidierungsexperimente.

Der aktuelle Replay-Vertrag injiziert jedoch keine Spike-Sequenzen in das laufende Netzwerk. Er ist daher eine **Konsolidierungsbaseline**, kein Modell biologischen Schlafs. Ein stärkerer Anspruch benötigt einen eigenen Mechanismus und Vergleich gegen gleich budgetiertes zusätzliches Wachtraining.

## A.5 Prediction Error

`PredictionErrorPlasticity` nutzt vorhandene Eligibility-Traces, besitzt aber eigene Konfiguration und Statistik. Umwelt-Prediction-Error wird nicht auf `set_reward()` abgebildet. Damit können Reward und Prediction Error faktoriell getrennt werden.

Für wissenschaftliche Aussagen sind mindestens `correct`, `disabled` und `shuffled` als Prediction-Error-Bedingungen nötig. Zusätzlich muss Reward unabhängig geschaltet werden, damit eine Wirkung nicht durch Belohnungslernen erklärt wird.

## A.6 Mehrschritt-Weltmodell

`ActionConditionedWorldModel` lernt diskrete Übergangsstatistiken `state + action -> next_state`, kann über explizite Aktionsfolgen rollen und beendet unbekannte Pfade früh. Alternative Aktionen können nebeneinander verglichen werden. Seine Kennzeichnung ist absichtlich:

`statistical_multistep_reference_not_neural_evidence`

Es handelt sich damit um eine Referenz für spätere neuronale Modelle. Das Modell liefert keine Evidenz dafür, dass MHRN intern eine neuronale Zustandsraumdarstellung gelernt hat.

## A.7 Offline-Entscheidungsevaluation

`OfflineDecisionEvaluator` bewertet nur gleich lange Aktionssequenzen und mutiert das Weltmodell nicht. Unvollständige Rollouts werden nicht ausgewählt. Gleichstände werden deterministisch behandelt. Der Output ist `DecisionRecommendation`, kein `ActionCommand`.

Damit wird die für `RQ-WM-001` und nachfolgende Weltmodellfragen notwendige Brücke geschaffen: Vorhersagen können auf ihren **funktionalen Entscheidungswert** geprüft werden, ohne den Evaluator direkt in die Aktorik zu koppeln.

## A.8 Sicherheits- und Erkenntnisgrenze

Keiner der Stage-6-Bausteine darf selbst:

1. externe Aktoren autorisieren,
2. Safety-Stopps aufheben,
3. EVID freigeben,
4. Bewusstseins- oder Wohlfahrtsstatus festlegen,
5. ein externes LLM als kanonischen Speicher oder Weltmodell einsetzen.

Diese Grenzen sind Teil des Forschungsdesigns, nicht nur Implementierungsdetails.
