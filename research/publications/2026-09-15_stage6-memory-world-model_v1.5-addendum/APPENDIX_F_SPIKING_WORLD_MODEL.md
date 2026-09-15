# Appendix F — Experimenteller spikender Übergangsmodell-Kandidat

Stand: 15. September 2026. Dieser Anhang dokumentiert `S6-NWM-001` und den zugehörigen Mechanismus `SpikingTransitionWorldModel`. Er beschreibt einen **experimentellen neuronalen Kandidaten**, nicht den Nachweis eines allgemeinen oder biologisch äquivalenten Weltmodells.

## 1. Motivation

Die bis einschließlich `S6-WM-002` verwendete Mehrschrittkomponente ist eine bewusst transparente statistische Referenz. Sie speichert beobachtete Übergänge als `state + action -> next_state` und kann daraus deterministische Rollouts erzeugen. Diese Referenz ist für kontrollierte Baselines nützlich, beantwortet jedoch nicht die stärkere Frage, ob der Übergang selbst durch eine spikende neuronale Dynamik gelernt und wieder ausgegeben werden kann.

`S6-NWM-001` führt deshalb einen getrennten Kandidaten ein. Die statistische Referenz bleibt unverändert erhalten und wird nicht rückwirkend als neuronales Modell umbenannt.

## 2. Architektur des Kandidaten

`SpikingTransitionWorldModel` verwendet den produktiven `NeuralNetwork`-Kern und den vorhandenen `LearningEngine`.

Für die experimentelle Referenz werden diskrete Zustands-/Aktionskontexte explizit kodiert:

- je `(state_key, action_key)` existiert ein Kontextneuron,
- je beobachtetem Folgezustand existiert ein Ausgangsneuron,
- Kontextneuronen sind mit allen bekannten Ausgangsneuronen verbunden,
- die Verbindungsgewichte beginnen bei null,
- Lernen erfolgt über den vorhandenen Pair-STDP-Pfad.

Der Encoder ist damit absichtlich **exact-context**. Eine Ähnlichkeitsmetrik zwischen unbekannten Zuständen oder eine kontinuierliche latente Zustandsrepräsentation wird nicht behauptet.

## 3. Lernen

Ein beobachteter Übergang wird teacher-forced präsentiert:

1. Kontextneuron für `state + action` wird stimuliert.
2. Der Netzwerk-Tick wird ausgeführt und an den `LearningEngine` übergeben.
3. Im Folgetick wird das Neuron des tatsächlich beobachteten nächsten Zustands stimuliert.
4. Der zweite Tick wird an den `LearningEngine` übergeben.
5. Pair-STDP verstärkt die zeitlich passende Kontext→Folgezustand-Synapse.
6. Definierte Cooldown-Ticks schließen die Trainingswiederholung ab.

Teacher forcing ist eine experimentelle Lernkonvention. Sie ist kein Beleg, dass biologische Systeme Zustandsübergänge auf dieselbe Weise trainieren.

## 4. Inferenz

Während `predict()` wird ausschließlich das bereits registrierte Kontextneuron stimuliert. Danach wird auf reale Ausgangsspikes des SNN gewartet. Die Vorhersage entsteht nur, wenn genau ein registriertes Ausgangsneuron feuert.

Für die Inferenz gelten zusätzlich:

- `LearningEngine.update()` wird während der gesamten Vorhersage einschließlich Cooldown nicht aufgerufen,
- die Kontext→Ausgangsgewichte werden vor und nach der Vorhersage verglichen,
- unbekannte Kontexte erzeugen `None` statt einer erfundenen Vorhersage,
- mehrere gleichzeitig feuende Ausgangszustände werden nicht willkürlich aufgelöst,
- die gemessene Latenz wird als Zahl von Inferenzschritten dokumentiert.

Damit sind Lern- und Inferenzphase technisch getrennt.

## 5. S6-NWM-001

Der Vergleich enthält vier Bedingungen:

| Bedingung | Bedeutung |
| --- | --- |
| `spiking_trained` | STDP-trainierter spikender Kandidat mit korrekten Folgezuständen |
| `spiking_untrained` | kein Training; unbekannte Kontexte dürfen nicht geraten werden |
| `spiking_target_shuffled` | gleicher Trainingspfad, aber systematisch falsche Zielzuordnung |
| `statistical_reference` | bestehendes nicht-neuronales `ActionConditionedWorldModel` |

Primäre Messgrößen sind:

- `exact_accuracy`,
- `prediction_coverage`,
- `mean_latency_steps`,
- `mean_correct_weight_margin`.

Die statistische Referenz dient der technischen Einordnung. Ein Gleichstand oder Vorteil des spikenden Kandidaten gegenüber dieser Referenz würde allein keine Überlegenheit eines neuronalen Weltmodells beweisen.

## 6. Evidenzgrenzen

Ein positiver `S6-NWM-001`-Befund darf höchstens die Aussage stützen, dass ein **diskreter exact-context Zustandsübergang durch reale SNN-Synapsen via STDP gelernt und anschließend als Ausgangsspike abgerufen werden kann**.

Nicht daraus ableitbar sind:

- Generalisation auf unbekannte Zustände,
- kontinuierliche latente Dynamik,
- Mehrschritt-Rollouts des spikenden Modells,
- kausale Counterfactual-Repräsentation,
- Planung,
- räumliches oder semantisches Weltverständnis,
- hippocampale oder kortikale biologische Äquivalenz,
- Bewusstsein.

## 7. Registry und Reproduzierbarkeit

Stage 6 besitzt mehrere orthogonale Protokolle für dieselben Forschungsfragen. Der historische globale Protokollkatalog verlangt dagegen höchstens ein Operational-Protokoll pro RQ. Um bestehende Kampagnen nicht rückwirkend zu brechen, führt `src/research/stage6_protocol_registry.py` einen separaten 1:n-Vertrag ein.

Für `RQ-MEM-002` sind drei Stage-6-Protokolle registriert; für `RQ-WM-001` vier. `validate_stage6_bundle()` prüft die Parität von Protokoll- und Preregistrierungsbundle sowie die Sperren gegen automatische Evidenzpromotion.

`scripts/run_stage6_operational.py` führt alle sieben Stage-6-Protokolle in einem gebundenen DATA-Lauf aus. `S6-NWM-001` wird dadurch unter derselben Seed-, Hash- und Human-Review-Governance wie die übrigen Stage-6-Versuche ausgeführt.

## 8. Nächste wissenschaftliche Schwelle

Nach `S6-NWM-001` bleibt für einen stärkeren neuronalen Weltmodell-Anspruch mindestens erforderlich:

1. verteilte Zustandskodierung statt eines Kontextneurons pro exaktem Zustand/Aktion-Paar,
2. Generalisation auf nicht trainierte, aber strukturell verwandte Zustände,
3. rekursive Mehrschrittvorhersage aus neuronalen Ausgangszuständen,
4. Unsicherheits- oder Konfidenzkalibrierung,
5. Entscheidungsvorteil des neuronalen Modells gegenüber statistischen und ablierten Kontrollen,
6. robuste Ergebnisse über unabhängige Seeds, Kapazitäten und Interferenzregime.

`S6-NWM-001` ist damit eine neue technische Schwelle, nicht das Ende der Weltmodellforschung.
