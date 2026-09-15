# Stage 6 — Gedächtnis und Weltmodell

**Nachtrag zur Dissertation und Forschungsarbeit 1.5 · 15. September 2026**

Dieser Nachtrag erweitert die Fassung 1.5 um den aktuellen Stage-6-Stand. Die historische Dissertation, ihre Kapiteldateien sowie vorhandene DOCX/PDF-Exporte werden nicht rückwirkend überschrieben. Der Nachtrag ist die zitierbare Fortschreibung für Gedächtnis, Semantisierung, Replay, Prediction Error und Weltmodellierung.

## Wissenschaftlicher Status

Stage 6 ist **technisch fortgeschritten, wissenschaftlich aber nicht abgeschlossen**. Implementierte Mechanismen und erfolgreiche Softwaretests sind zunächst Engineering-/DATA-Befunde. Sie werden nicht automatisch zu akzeptierter EVID.

Die übergeordneten Fragen `RQ-MEM-002` und `RQ-WM-001` bleiben offen. Insbesondere folgt aus vorhandener Persistenz, Musterwiedererkennung, Replay, Mehrschrittvorhersage oder einem spikenden Übergangsassoziator weder ein Nachweis biologischer Gedächtnisäquivalenz noch ein Nachweis allgemeinen Weltverständnisses, Planung oder Bewusstsein.

## Implementierter Stand

1. **Temporale und episodische Repräsentation** — begrenzte episodische Speicher, reale SNN-Spikemuster als neuronale Episoden, partielle Cue-Suche, getrennte Lese-/Schreibkontrollen.
2. **Semantische Prototypen** — wiederkehrende sparse Aktivität kann über unabhängige Episoden Unterstützung akkumulieren; disjunkte Hold-out-Episoden werden in `S6-SEM-001` getrennt ausgewertet.
3. **Replay und Reaktivierung** — `S6-RPL-001` reinjiziert gespeicherte Spike-Muster in ein reales SNN und vergleicht geordnetes Replay mit No-Replay, Shuffle und zusätzlicher Wachaktivität unter gleichem SNN-Schrittbudget. Dies ist kein biologisches Schlafmodell.
4. **Prediction Error** — Umweltvorhersagefehler besitzt einen eigenen eligibility-basierten Plastizitätspfad und wird in `S6-PE-001` faktoriell gegen Reward on/off geprüft; er wird nicht über `LearningEngine.set_reward()` umgeleitet.
5. **Ein-Schritt-Referenzmodell** — typisierte, persistierbare, präquenzielle Übergangsstatistik bleibt als technische Baseline erhalten.
6. **Mehrschritt-Referenzmodell** — `state + action -> next_state`, begrenzte Rollouts, alternative Aktionen und deterministische Persistenz. Kennzeichnung: `statistical_multistep_reference_not_neural_evidence`.
7. **Offline-Entscheidungsnutzen** — ein separater Evaluator vergleicht gleich lange, eingefrorene Rollouts. Er ist keine Aktorik und keine Sicherheitsautorität; seine Empfehlung ist ausschließlich Forschungsoutput.
8. **Stage-6-Funktionsbundle** — sieben versionierte Protokolle besitzen eine eigene eingefrorene Preregistrierung, einen reproduzierbaren DATA-Runner und eine 1:n-Registry, weil mehrere orthogonale Protokolle dieselbe Forschungsfrage prüfen.
9. **Fortsetzungsintegrität** — ein additiver Stage-6-State-Bundle bindet neuronales Episodengedächtnis, semantisches Gedächtnis und Mehrschrittmodell per Hash an ein bestehendes Runtime-Bundle-Manifest, ohne historische Formate umzuschreiben.
10. **Experimenteller spikender Übergangsmodell-Kandidat** — `SpikingTransitionWorldModel` lernt diskrete Kontext→Folgezustand-Assoziationen über reale SNN-Synapsen und Pair-STDP. `S6-NWM-001` trennt trainiert, untrainiert, Ziel-Shuffle und statistische Referenz. Der Kandidat ist ausdrücklich exact-context und noch kein generalisierendes neuronales Weltmodell.

## Zentrale Trennungen

- episodisches Gedächtnis ≠ Replay
- Replay ≠ semantisches Gedächtnis
- semantisches Gedächtnis ≠ Weltmodell
- Vorhersagefehler ≠ Reward
- Ein-Schritt-Prädiktion ≠ Mehrschritt-Weltmodell
- statistisches Referenzmodell ≠ neuronales Weltmodell
- spikender exact-context Assoziator ≠ bewiesene Generalisation
- Mehrschritt-Rollout ≠ bewiesene Planung
- alternative Modellrollouts ≠ kausale Counterfactual-Evidenz
- Reaktivierung ≠ biologischer Schlaf
- technischer Test ≠ wissenschaftliche Evidenz

## Anhänge

- [Anhang A — Stage-6-Verträge und Implementierungsgrenzen](APPENDIX_A_STAGE6_CONTRACTS.md)
- [Anhang B — Experiment- und Ablationsmatrix](APPENDIX_B_STAGE6_EXPERIMENT_MATRIX.md)
- [Anhang C — Literatur und theoretische Einordnung](APPENDIX_C_STAGE6_LITERATURE_NOTES.md)
- [Anhang D — Reproduzierbarkeit und EVID-Promotion](APPENDIX_D_REPRODUCIBILITY.md)
- [Anhang E — Funktionale Stage-6-Protokolle und Fortsetzungsvertrag](APPENDIX_E_FUNCTIONAL_PROTOCOLS.md)
- [Anhang F — Experimenteller spikender Übergangsmodell-Kandidat](APPENDIX_F_SPIKING_WORLD_MODEL.md)

Literaturdaten: [`research/literature/stage6_memory_world_model.bib`](../../../literature/stage6_memory_world_model.bib).

## Kernaussage für die Dissertation

Der aktuelle Stage-6-Stand rechtfertigt die Aussage, dass MHRN **getrennte, deterministisch testbare Engineering-Verträge und ausführbare DATA-Protokolle für neuronale Episoden, semantische Prototypen, SNN-Reaktivierung, unabhängigen Prediction Error, aktionskonditionierte Mehrschrittvorhersage und einen ersten STDP-basierten spikenden Übergangsassoziator** besitzt.

Nicht gerechtfertigt sind derzeit Aussagen, wonach diese Mechanismen bereits funktional äquivalent zu hippocampo-kortikaler Konsolidierung seien oder ein generalisierendes neuronales Weltmodell mit Planung, Counterfactual Reasoning oder biologischem Weltverständnis nachgewiesen hätten.

Die nächste wissenschaftliche Schwelle ist kontrollierte Leistung über die aktuellen exact-context Aufgaben hinaus: längere Delay-/Interferenzreihen, robuste Semantisierung, Replay-Nutzen gegenüber gleich budgetierten Kontrollen, unabhängige Prediction-Error-Effekte, verteilte neuronale Zustandskodierung, Generalisation auf unbekannte Zustände und rekursive neuronale Mehrschrittvorhersage.
