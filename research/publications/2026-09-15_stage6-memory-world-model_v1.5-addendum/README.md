# Stage 6 — Gedächtnis und Weltmodell

**Nachtrag zur Dissertation und Forschungsarbeit 1.5 · 15. September 2026**

Dieser Nachtrag erweitert die Fassung 1.5 um den aktuellen Stage-6-Stand. Die historische Dissertation, ihre Kapiteldateien sowie vorhandene DOCX/PDF-Exporte werden nicht rückwirkend überschrieben. Der Nachtrag ist die zitierbare Fortschreibung für Gedächtnis, Semantisierung, Replay, Prediction Error und Weltmodellierung.

## Wissenschaftlicher Status

Stage 6 ist **technisch fortgeschritten, wissenschaftlich aber nicht abgeschlossen**. Implementierte Mechanismen und erfolgreiche Softwaretests sind zunächst Engineering-/DATA-Befunde. Sie werden nicht automatisch zu akzeptierter EVID.

Die übergeordneten Fragen `RQ-MEM-002` und `RQ-WM-001` bleiben offen. Insbesondere folgt aus vorhandener Persistenz, Musterwiedererkennung, Replayplanung oder Mehrschrittvorhersage weder ein Nachweis biologischer Gedächtnisäquivalenz noch ein Nachweis von Planung, Weltverständnis oder Bewusstsein.

## Implementierter Stand

1. **Temporale und episodische Repräsentation** — begrenzte episodische Speicher, reale SNN-Spikemuster als neuronale Episoden, partielle Cue-Suche, getrennte Lese-/Schreibkontrollen.
2. **Semantische Prototypen** — wiederkehrende sparse Aktivität kann nur über unabhängige Episoden Unterstützung akkumulieren; Wiederholungen innerhalb derselben Episode erhöhen den Support nicht.
3. **Replay-Vertrag** — `off`, `ordered` und `shuffled` sind getrennte, budgetierte Bedingungen. Replay ist derzeit Re-Selektion gespeicherter Episoden für einen Konsolidierungskonsumenten, nicht simuliertes Schlafen und keine Spike-Reinjektion.
4. **Prediction Error** — Umweltvorhersagefehler besitzt einen eigenen eligibility-basierten Plastizitätspfad und wird nicht über `LearningEngine.set_reward()` umgeleitet.
5. **Ein-Schritt-Referenzmodell** — typisierte, persistierbare, präquenzielle Übergangsstatistik bleibt als technische Baseline erhalten.
6. **Mehrschritt-Referenzmodell** — `state + action -> next_state`, begrenzte Rollouts, alternative Aktionen und deterministische Persistenz. Kennzeichnung: `statistical_multistep_reference_not_neural_evidence`.
7. **Offline-Entscheidungsnutzen** — ein separater Evaluator vergleicht gleich lange, eingefrorene Rollouts. Er ist keine Aktorik und keine Sicherheitsautorität; seine Empfehlung ist ausschließlich Forschungsoutput.

## Zentrale Trennungen

- episodisches Gedächtnis ≠ Replay
- Replay ≠ semantisches Gedächtnis
- semantisches Gedächtnis ≠ Weltmodell
- Vorhersagefehler ≠ Reward
- Ein-Schritt-Prädiktion ≠ Mehrschritt-Weltmodell
- Mehrschritt-Rollout ≠ bewiesene Planung
- alternative Modellrollouts ≠ kausale Counterfactual-Evidenz
- technischer Test ≠ wissenschaftliche Evidenz

## Neue Anhänge

- [Anhang A — Stage-6-Verträge und Implementierungsgrenzen](APPENDIX_A_STAGE6_CONTRACTS.md)
- [Anhang B — Experiment- und Ablationsmatrix](APPENDIX_B_STAGE6_EXPERIMENT_MATRIX.md)
- [Anhang C — Literatur und theoretische Einordnung](APPENDIX_C_STAGE6_LITERATURE_NOTES.md)
- [Anhang D — Reproduzierbarkeit und EVID-Promotion](APPENDIX_D_REPRODUCIBILITY.md)

Literaturdaten: [`research/literature/stage6_memory_world_model.bib`](../../../literature/stage6_memory_world_model.bib).

## Kernaussage für die Dissertation

Der aktuelle Stage-6-Stand rechtfertigt die Aussage, dass MHRN **getrennte, deterministisch testbare Engineering-Verträge für neuronale Episoden, semantische Prototypen, Replaybedingungen, unabhängigen Prediction Error und aktionskonditionierte Mehrschrittvorhersage** besitzt. Nicht gerechtfertigt sind derzeit Aussagen, wonach diese Mechanismen bereits funktional äquivalent zu hippocampo-kortikaler Konsolidierung seien oder auf unbekannten Aufgaben einen kausalen Entscheidungsnutzen eines neuronalen Weltmodells nachgewiesen hätten.

Die nächste wissenschaftliche Schwelle ist daher nicht zusätzliche Benennung, sondern kontrollierte Leistung: Delay+Distraktor-Recall aus realer SNN-Aktivität, held-out Semantisierung, Replay-Ablationen mit gleichem Budget, Prediction-Error-Ablationen unabhängig von Reward sowie eingefrorene Mehrschrittmodelle mit messbarem Entscheidungsnutzen auf zurückgehaltenen Episoden.
