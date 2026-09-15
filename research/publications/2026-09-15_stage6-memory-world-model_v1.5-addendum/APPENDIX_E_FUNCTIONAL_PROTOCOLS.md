# Appendix E — Funktionale Stage-6-Protokolle und Fortsetzungsvertrag

Stand: 15. September 2026. Dieser Anhang ergänzt Fassung 1.5 und den Stage-6-Nachtrag. Er dokumentiert **implementierte Forschungsinstrumente**, nicht akzeptierte wissenschaftliche Evidenz.

## 1. Anlass

Die ersten Stage-6-Komponenten belegten vor allem technische Verträge: ein begrenzter episodischer Speicher, semantische Prototypen, Replay-Selektion, ein unabhängiger Prediction-Error-Pfad und ein statistisches, aktionskonditioniertes Mehrschrittmodell. Das ältere Experiment `memory_delayed_information_v1` war für eine starke Gedächtnisbehauptung ungeeignet, weil `snn_involved=false` galt und die Zielinformation aus gespeicherten Datensätzen gelesen werden konnte.

Die neue Protokollgruppe beseitigt diese methodische Vermischung. Sie trennt sechs Fragen:

1. Kann eine durch reale SNN-Aktivität kodierte Episode nach Distraktoraktivität über einen partiellen neuronalen Schlüssel wiedergefunden werden?
2. Entstehen über mehrere neuronale Episoden abstrahierte Prototypen, die auf disjunkten Hold-out-Episoden nutzbar sind?
3. Lässt sich Replay als kontrollierte Reaktivierung gegenüber No-Replay, Shuffle und zusätzlicher Wachaktivität mit gleichem Budget testen?
4. Ist der Umwelt-Prediction-Error-Pfad experimentell vom externen Reward-Pfad getrennt?
5. Liefert ein eingefrorenes aktionskonditioniertes Referenzmodell Mehrschrittvorhersagen jenseits von Persistence und Shuffle?
6. Verbessert dieses eingefrorene Referenzmodell offline eine Entscheidungsauswertung, ohne daraus Aktor-Autorität abzuleiten?

## 2. Implementierte Protokolle

| Protokoll | Kernbehandlung | Kontrollen | SNN im Messpfad | Claim-Grenze |
| --- | --- | --- | --- | --- |
| `S6-EPI-001` | neuronaler Key/Value-Recall nach Delay | read-off, write-off, episode-shuffle | ja | funktionales episodisches DATA, keine hippocampale Äquivalenz |
| `S6-SEM-001` | Cross-Episode-Prototypen | label-shuffle, no-semantic | ja | Hold-out-Generalisation, kein Nachweis menschlicher Semantik |
| `S6-RPL-001` | geordnete Reaktivierung | no-replay, shuffled, equal-budget-awake | ja | kontrollierte Reaktivierung, kein Schlafmodell |
| `S6-PE-001` | Prediction Error × Reward | PE disabled/shuffled × reward off/on | ja | Pfadtrennung/Plastizität, PE bleibt nicht Reward |
| `S6-WM-001` | eingefrorene Mehrschrittvorhersage | shuffled, persistence, no-model | nein, statistische Referenz | Referenzdynamik, kein neuronales Weltmodell |
| `S6-WM-002` | offline decision benefit | disabled, shuffled, persistence | nein, statistische Referenz | Entscheidungsevaluator, keine Aktor-Autorität |

Die Implementierung liegt in `src/research/stage6_experiments.py`. Die maschinenlesbare Deklaration liegt in `research/protocols/STAGE6_OPERATIONAL_PROTOCOLS.json`; die eingefrorenen Bedingungen und Auswertungsregeln liegen in `research/preregistrations/operational/stage6_bundle_v1.json`.

## 3. Schutz gegen Ziel-Leakage in S6-EPI-001

`S6-EPI-001` kodiert einen Schlüssel und eine binäre Zielklasse als reale Spike-Aktivität. Zwischen Kodierung und Abruf feuern unabhängige Distraktor-Neuronen. Beim Abruf wird nur der Schlüssel erneut stimuliert. Die Klassenausgabe wird aus den Spike-IDs der abgerufenen Episode relativ zu den zuvor festgelegten Klassen-Neuronengruppen bestimmt.

Für den Entscheidungsweg gelten explizit:

- kein Lesen des Zielwerts aus `frame_payload`,
- kein Lesen eines Zielwerts aus `actual_state`,
- `frame_payload` enthält nur Phasen-/Versuchsmetadaten,
- read-off und write-off sind echte Lesionsbedingungen,
- der Shuffle-Arm verwendet eine andere gespeicherte Episode,
- Distraktoraktivität wird als reale Netzwerkaktivität gemessen.

Damit ist die frühere Schwäche der direkten Record-Abfrage technisch beseitigt. Ob daraus robuste Gedächtnisleistung entsteht, ist eine **empirische** Frage des ausgeführten Datensatzes und nicht durch den Code allein beantwortet.

## 4. Semantik und Replay

`S6-SEM-001` trennt Trainings- und Auswertungsepisoden vollständig. Die Klassenzuordnung liegt nicht in den Episoden-Payloads. Prototypen werden aus wiederkehrenden Spike-Mengen gebildet und anschließend auf neue Episoden mit neuer Störkomponente angewendet. Der Shuffle-Arm zerstört die Zuordnung zwischen Trainingsziel und neuronaler Kernstruktur.

`S6-RPL-001` unterscheidet Replay von bloßer zusätzlicher Verarbeitung. Geordnete und zeitlich gemischte Episoden werden als Spike-Muster erneut in ein SNN injiziert. No-Replay erhält ein entsprechendes Leerlaufbudget; `equal_budget_awake` erhält die gleiche Zahl von Reaktivierungs-/Verarbeitungsschritten, jedoch als zusätzliche Wachkontrolle. Eine mögliche Differenz darf daher nicht allein mit unterschiedlicher Anzahl von Simulationsschritten erklärt werden.

Trotzdem gilt: Diese Reaktivierung ist **kein biologisches Schlafmodell**. Ein positiver Befund wäre zunächst ein funktionaler Replay-/Konsolidierungsbefund im MHRN-Kontext.

## 5. Prediction Error und Reward

`S6-PE-001` kreuzt drei Prediction-Error-Bedingungen (`correct`, `disabled`, `shuffled`) mit Reward `on/off`. `PredictionErrorPlasticity` verwendet vorhandene Eligibility-Traces, besitzt jedoch eine eigene Konfiguration, eigene Statistik und ruft `LearningEngine.set_reward()` nicht auf.

Die faktoriellen Bedingungen erlauben erstmals, folgende Aussagen getrennt zu prüfen:

- ein Effekt des Prediction Errors bei ausgeschaltetem Reward,
- ein Reward-Effekt bei ausgeschaltetem Prediction Error,
- mögliche Interaktion beider Faktoren,
- Verlust oder Richtungsänderung bei gemischtem Prediction Error.

Ein Prediction Error wird dadurch nicht zu einem biologischen Belohnungssignal erklärt.

## 6. Mehrschritt-Weltmodell und Entscheidungsnutzen

`S6-WM-001` verwendet ein eingefrorenes, diskretes Referenzmodell `state + action -> next_state`. Die Auswertung erfolgt über Aktionssequenzen von mehreren Schritten und vergleicht gegen ein absichtlich verfälschtes Modell, Persistence und No-Model. Während der Hold-out-Auswertung findet kein Update statt.

`S6-WM-002` führt Kandidatenaktionen ausschließlich durch Modell-Rollouts. Das Ergebnis ist eine `DecisionRecommendation`, niemals ein `ActionCommand`. Der Evaluator besitzt keine Autorisierung für externe oder simulierte Aktoren. Gemessen wird lediglich, ob das korrekte eingefrorene Modell bei bekannten Übergängen einen höheren offline Utility-Wert ermöglicht als die Kontrollen.

Damit kann Entscheidungsnutzen der **statistischen Referenz** getestet werden. Der Befund wäre ausdrücklich noch kein Nachweis eines neuronalen oder generalisierenden Weltmodells.

## 7. Fortsetzungs- und Persistenzvertrag

Der bisherige `RuntimeBundle` bindet den Runtime-Checkpoint an den älteren `MemoryWorldModel`-Zustand. Der additive `Stage6StateBundle` erweitert dies, ohne historische Formate umzuschreiben. Er bindet:

- das exakte Runtime-Bundle-Manifest per SHA-256,
- `NeuralEpisodicMemory`,
- `SemanticMemory`,
- `ActionConditionedWorldModel`,
- die `run_id` der neuronalen Episode,
- Hashes aller gespeicherten Zustandsdateien,
- einen Integritätsdigest des Zusatzmanifests.

Das ist ein **Continuation-Integrity-Vertrag**. Er zeigt nicht automatisch, dass nach Restore eine komplette gekoppelte Simulation bitidentisch weiterläuft. Ein solcher Pause/Resume-Nachweis bleibt ein eigener experimenteller Test.

## 8. Reproduzierbare Ausführung

`scripts/run_stage6_operational.py` liest ausschließlich die eingefrorene Stage-6-Protokolldatei und das zugehörige Preregistrierungsbundle. Es erzwingt mindestens drei eindeutige Seeds, vergleicht deklarierte mit tatsächlich erzeugten Bedingungen und verweigert Resultate, die sich selbst als `scientific_evidence=true` markieren.

Jede Ausgabe enthält mindestens:

- Commit-SHA,
- SHA-256 der Protokolldatei,
- SHA-256 der Preregistrierung,
- verwendete Seeds,
- alle Bedingungen und Einzelresultate,
- `scientific_evidence=false`,
- `automatic_evidence_promotion=false`.

## 9. Was weiterhin fehlt

Die neue Infrastruktur reduziert mehrere technische Lücken, schließt Stage 6 wissenschaftlich aber nicht ab. Weiter offen sind insbesondere:

1. Ausführung der eingefrorenen Protokolle mit ausreichender unabhängiger Seedzahl und statistischer Auswertung;
2. Robustheit über mehrere Delay-Längen, Distraktorstärken, Kapazitäten und Interferenzregime;
3. ein **tatsächlich spikendes bzw. neuronales Zustandsdynamikmodell** (`S6-NWM-001`) gegen die statistische Referenz;
4. Generalisation des Weltmodells auf nicht identische Zustände/Kontexte statt Exact-Context-Lookup;
5. vollständige Pause/Resume-Äquivalenz der gekoppelten Runtime inklusive aller Stage-6-Komponenten;
6. externe/humane wissenschaftliche Begutachtung vor jeder EVID-Promotion.

`RQ-MEM-002` und `RQ-WM-001` bleiben daher offen. Dieser Anhang erhöht die technische Prüfbarkeit, nicht automatisch den Evidenzstatus.
