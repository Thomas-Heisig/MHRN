# Anhang C — Literatur und theoretische Einordnung

Die Stage-6-Architektur wird an mehrere Forschungsstränge angebunden, ohne technische Ähnlichkeit als biologische Gleichsetzung zu behandeln. Vollständige Literaturdaten stehen in `research/literature/stage6_memory_world_model.bib`.

## C.1 Complementary Learning Systems

McClelland, McNaughton und O'Reilly (1995) formulieren komplementäre Lernsysteme mit unterschiedlichen Lernzeitskalen als Lösung des Stabilitäts-/Plastizitätsproblems. Für MHRN begründet dies die Hypothese, schnelle episodische Bindung und langsamere strukturierende Konsolidierung getrennt zu behandeln. Die vorhandenen MHRN-Komponenten sind jedoch keine Implementierung der anatomischen Hippocampus-Neokortex-Aufteilung.

## C.2 Episodisch → semantisch

Chrysanthidis et al. (2022) zeigen in einem spikenden kortikalen Modell, dass Bayesian-Hebbian/BCPNN-Plastizität kontextübergreifende Semantisierung erzeugen kann. Der Befund ist besonders relevant, weil er zeigt, dass Semantisierung mehr ist als das Speichern einer Episode: wiederholte Exposition über Kontexte kann Item-Kontext-Kopplung verändern.

D'Alba et al. (2025) gehen weiter und modellieren hippocampo-kortikale Interaktion in einem plastischen SNN. Awake encoding und replay-basierte Konsolidierung werden dabei als getrennte Phasen behandelt. Für MHRN folgt daraus, dass Episodenspeicherung, Replay und semantische Abstraktion als eigene experimentelle Objekte geprüft werden müssen.

Chrysanthidis et al. (2025) zeigen zusätzlich, dass kurzfristige synaptische Dynamik und Recency episodischen Recall beeinflussen können. Deshalb darf ein erfolgreicher kurzer Delay-Test nicht vorschnell als Langzeitkonsolidierung interpretiert werden.

## C.3 Replay und Interferenz

Golden et al. (2022) demonstrieren in einem SNN, dass offline sleep-like reactivation katastrophales Vergessen reduzieren kann. Methodisch entscheidend ist für MHRN nicht die Bezeichnung „Schlaf“, sondern der kontrollierte Vergleich von Replay gegen no-replay und gegen alternative Lernbudgets. Der aktuelle MHRN-Replay-Scheduler ist nur die notwendige Experimentalstruktur; er simuliert noch keinen biologischen Schlafzustand.

## C.4 Predictive Coding und Prediction Error

Lee et al. (2024) implementieren predictive coding in einem SNN mit getrennten positiven und negativen Error-Neuronen. Dies belegt die Machbarkeit eines solchen Designs, aber nicht seine Exklusivität.

Mikulasch et al. (2023) diskutieren dendritische Fehlerberechnung als alternative physiologische Realisierung: Prediction Error kann lokal in Kompartimentdynamik liegen, statt zwingend in dedizierten Error Units. Für MHRN folgt daraus, dass `PredictionErrorPlasticity` zunächst ein funktionaler Lernfaktor ist. Die konkrete biologische Lokalisierung bleibt eine offene Modellhypothese.

Die Korrektur von Mikulasch et al. zu einer Gleichung in Box 2 wurde 2025 publiziert und ist in der Bibliographie vermerkt. Das ändert die übergeordnete Argumentation zur dendritischen Fehlerberechnung nicht, soll aber für formale Reproduktion nicht ignoriert werden.

## C.5 Weltmodelle und Handlungsnutzen

Hafner et al. (2025) zeigen mit DreamerV3 auf nicht-biologischer Basis, wie ein gelerntes Weltmodell zukünftige Outcomes möglicher Aktionen erzeugen und damit Verhalten verbessern kann. Für MHRN dient dies als Engineering-Kontrast: Ein Weltmodellanspruch wird stärker, wenn Vorhersage nicht nur numerisch besser ist, sondern nachweislich die Auswahl von Handlungsfolgen verbessert.

Sun et al. (2025) beschreiben ein spikendes Weltmodell mit Multicompartment-Neuronen, spiking state-space model, visueller Spike-Kodierung und modellbasiertem Reinforcement Learning. Diese Arbeit bildet einen deutlich stärkeren Vergleichspunkt für einen zukünftigen neuronalen MHRN-Weltmodellpfad als die aktuelle statistische Übergangsbaseline.

## C.6 Konsequenzen für MHRN

Aus der Literatur folgen fünf methodische Mindestanforderungen:

1. **Systeme trennen:** Episode, Konsolidierung, Semantik und Weltmodell dürfen nicht als Synonyme verwendet werden.
2. **Zeitskalen kontrollieren:** kurzfristige Recency/Traces müssen von langfristiger Retention getrennt werden.
3. **Replay fair vergleichen:** no-replay, shuffled replay und gleich budgetiertes alternatives Training sind nötig.
4. **Prediction Error lokalisierungsagnostisch testen:** funktionale Wirkung zuerst; biologische Zuordnung danach durch spezifischere Modelle/Ablationen.
5. **Weltmodell funktional prüfen:** held-out Mehrschrittvorhersage und Entscheidungsnutzen sind stärkere Kriterien als interne Persistenz allein.

Diese Einordnung unterstützt die Stage-6-Architektur, ersetzt aber keine MHRN-spezifische empirische Evidenz.
