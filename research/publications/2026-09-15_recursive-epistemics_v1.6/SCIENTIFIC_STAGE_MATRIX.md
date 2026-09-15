# Wissenschaftliche Reifematrix der Stufen 0–10

**Stand:** 15. September 2026 · Basiscommit vor dieser Revision: `14b5066c9f8eac9c7522d59966b9e81c29226c56`

Diese Matrix bewertet nicht „Intelligenz“ und nicht die Größe des Codes. Sie bildet den Stand eines Forschungsprogramms ab. Der Score ist eine transparente Heuristik, die ausschließlich dazu dient, technische Fertigstellung nicht mit wissenschaftlicher Absicherung zu verwechseln.

## Bewertungsdimensionen

| Dimension | Gewicht | Bedeutung |
|---|---:|---|
| Forschungsfrage / Hypothese | 15 % | explizit registrierte, falsifizierbare Frage mit Claim-Grenze |
| Protokoll | 20 % | eingefrorene Intervention, Kontrollen, Endpunkte, Seeds und Abbruchregeln |
| DATA | 20 % | quellengebundene, prüfbare Ausführung mit Rohdaten/Receipts |
| Reviewte EVID | 20 % | menschlich geprüfte Evidenzpromotion für den konkreten Claim |
| Unabhängige Replikation | 15 % | Wiederholung außerhalb derselben Implementierungs-/Interpretationskette |
| Attribution | 10 % | Literatur-, Ideen-, Code-, Abbildungs- und Eigenversionsprovenienz |

`met = 1`, `partial = 0,5`, `open = 0`. Die Prozentwerte dürfen nicht als naturwissenschaftlich validierte Skala interpretiert werden.

## Gesamtübersicht

| Stufe | Technischer Gegenstand | wissenschaftliche Reife | Einordnung |
|---:|---|---:|---|
| 0 | einzelne Nervenzelle | 50 % | aktiv |
| 1 | kleines SNN | 30 % | aktiv |
| 2 | stabiles rekurrentes SNN | 65 % | fortgeschritten |
| 3 | plastisches Nervengewebe | 55 % | fortgeschritten |
| 4 | spezialisierte neuronale Areale | 55 % | fortgeschritten |
| 5 | integriertes künstliches Nervensystem | 55 % | fortgeschritten |
| 6 | Gedächtnis und Weltmodell | 40 % | aktiv |
| 7 | Selbstmodell und verkörperte Identität | 28 % | frühe Forschung |
| 8 | autonome lebenslange Entwicklung | 23 % | geplant / Vorläufer |
| 9 | hochintegrierte künstliche Kognition | 15 % | geplant |
| 10 | Bewusstseinsforschung | 13 % | Forschungsfrontier |

Die Repository-Maschine liest denselben Stand aus `src/dashboard/static/scientific-progress.json`. Die Textfassung hier ist die wissenschaftliche Interpretation desselben Vertrags.

## Stufe 0 – Einzelne Nervenzelle

**Claim-Grenze:** Deterministische Einzelzell-Referenzen validieren den implementierten numerischen Vertrag im geprüften Bereich. Sie beweisen weder biologische Gleichwertigkeit noch die Überlegenheit eines Neuronenmodells.

Vorhanden sind versionierte Izhikevich-/LIF-Verträge, isolierte Referenzpfade und technische Wiederholbarkeit. Offen bleiben eine eigens registrierte konfirmatorische Einzelzellfrage, unabhängige Replikation und menschlich promotete EVID. Ein externer Brian2-Vergleich ist ein wertvoller Referenzkontrast, aber kein Ersatz für einen allgemeinen biologischen Validierungsnachweis.

## Stufe 1 – Kleines SNN

**Claim-Grenze:** Korrekte Kopplung und Spike-Ausbreitung in kleinen Netzen zeigen technische Netzwerkfunktion, nicht Skalierbarkeit, Lernfähigkeit oder Kognition.

Die technische Basis ist vorhanden. Wissenschaftlich fehlt vor allem ein eigener task-basierter Forschungszweig, der Netzwerkmechanismen durch Interventionen isoliert und nicht nur Konnektivität verifiziert.

## Stufe 2 – Stabiles rekurrentes SNN

**Claim-Grenze:** Lange stabile und deterministische Läufe stützen Stabilität unter den geprüften Bedingungen. Rekurrenz ist damit nicht automatisch Gedächtnis oder nützliche zeitliche Berechnung.

Die bisherige Kampagne mit langen Läufen liefert reale DATA. Der nächste methodische Schritt ist eine Rekurrenz-Ablation bei gleicher Aufgabe und gleichem Ressourcenbudget: rekurrent, feed-forward bzw. informationszerstörte/yoked Kontrollen. Erst damit lässt sich ein funktionaler Beitrag der Rekurrenz von bloßer Stabilität trennen.

## Stufe 3 – Plastisches Nervengewebe

**Claim-Grenze:** STDP, Eligibility/Drei-Faktor-Lernen, Homöostase und strukturelle Plastizität sind implementierte Mechanismen. Das Vorhandensein und technische Funktionieren der Mechanik ist nicht gleichbedeutend mit nachgewiesener lernbezogener Wirksamkeit.

Benötigt werden präregistrierte Learning-on/off-, Sham- und information-destroyed Kontrollen auf gehaltenen Aufgaben. Wissenschaftlich entscheidend sind Generalisierung und mechanistische Attribution, nicht nur Gewichtsänderung.

## Stufe 4 – Spezialisierte neuronale Areale

**Claim-Grenze:** Audio-, Vision- und Digitalpfade, MSBA/Gateway-Verträge und modality-spezifische Adapter bilden eine technische Architektur. Die E01–E05-Ausführungen bleiben DATA, solange keine unabhängige Review-/EVID-Promotion stattgefunden hat.

Frozen/Random/Shuffle-Kontrollen sollen den Beitrag gelernter Gateway-Abbildungen isolieren. Große deklarierte Neuron-/Synapsenzahlen dürfen nur dort als empirisch ausgeführt bezeichnet werden, wo sie tatsächlich materialisiert und gemessen wurden.

## Stufe 5 – Integriertes künstliches Nervensystem

**Claim-Grenze:** Ein geschlossener sensorimotorischer Regelkreis ist in einer synthetischen deterministischen Umgebung technisch belegt. Digitale Host-Telemetrie ist keine biologische Interozeption; ein simuliertes Environment ist keine reale Verkörperung.

Matched-disturbance, yoked replay, unterbrochene Rückkopplung und wirkungslose Aktoren sind die zentralen nächsten Kontrollen. Reale Geräteadapter müssen als eigener Safety-/Engineering-/Forschungszweig geprüft werden.

## Stufe 6 – Gedächtnis und Weltmodell

**Claim-Grenze:** Die vorhandene Infrastruktur und die ersten Mechanismen bilden eine Forschungsfoundation. Sie rechtfertigen noch keinen Claim vollständiger Semantization, hierarchischen Predictive Codings oder eines generativen Weltmodells.

### Was bereits vorhanden ist

- zeitlicher Zustand und begrenzte Working-/episodische Speicherfunktionen,
- registrierte Memory-/World-Model-Forschungsfragen,
- Übergangs-/Vorhersagepfade und Prediction-Error-Telemetrie,
- Stage-6-Registry, Experimente und Addendum,
- semantische Prototyp-/Registry-Arbeit als definierte Grundlage,
- technische Verträge für Multi-Timescale- und erweiterte neuronale Mechanismen.

### Mechanismus-Lücken

1. **Semantization:** Eine semantische Datenstruktur oder ein Prototyp ist noch kein Mechanismus, der episodische Repräsentationen durch Replay/Konsolidierung in robuste semantische Repräsentationen überführt.
2. **Predictive Coding:** Ein Feld `prediction_error` oder eine Differenzmetrik ist noch kein neuronales Predictive-Coding-System. Erforderlich ist eine definierte Vorhersage-/Fehlerdynamik mit abladierbarem bottom-up/top-down Beitrag.
3. **Weltmodell:** Ein Ein-Schritt-Prädiktor ist kein generatives, mehrschrittiges, aktionskonditioniertes Weltmodell. Planung in „Imagination“ wäre ein weitergehender Claim und benötigt eigene Protokolle.
4. **Replay/Konsolidierung:** Replay muss als aktiver Mechanismus mit Kontrollarmen und Interferenz-/Retentionseffekten geprüft werden.
5. **Gekoppelte Persistenz:** Gedächtnis, Predictor und relevante adaptive Zustände müssen innerhalb des kanonischen Checkpoint-Vertrags deterministisch wiederherstellbar sein, bevor Langzeitexperimente interpretiert werden.

### Forschungsprogramm

- episodic acquisition → offline/low-input replay → semantic consolidation,
- replay on/off, shuffled replay, matched-compute no-replay,
- prediction pathway on/off, top-down/bottom-up disruption,
- one-step vs. multi-step/action-conditioned prediction,
- held-out sequence/generalization tests,
- interference/retention über mehrere Aufgaben,
- unabhängige Replikation vor EVID-Promotion.

### Literaturbezug

Der Mechanismusraum wird unter anderem durch Complementary Learning Systems, SNN-Semantization, schlafvermitteltes Replay, dendritische Prediction-Error-Modelle, spikendes Predictive Coding und spikende World Models motiviert. Diese Literatur legt Vergleichsfragen nahe; sie beweist nicht, dass MHRN dieselben Mechanismen bereits realisiert.

## Stufe 7 – Selbstmodell und verkörperte Identität

**Claim-Grenze:** Versionierte Profile, Sensor-/Aktorinventar und Behavior State sind technische Identitäts- und Zustandsmodelle. Ein funktionales Selbstmodell erfordert kausale self/other Attribution und überprüfbare Vorhersagen über eigene Handlungen.

Die nächste Studie muss eigene Aktionsursachen gegen externe/yoked Ursachen unterscheiden. Sprachliche Selbstaussagen eines LLM dürfen nicht als Evidenz des SNN-Selbstmodells verwendet werden.

## Stufe 8 – Autonome lebenslange Entwicklung

**Claim-Grenze:** Interferenz-Screens und strukturelle Anpassung sind keine Evidenz für lifelong learning.

Erforderlich sind fortlaufend trainierte gemeinsame Netze ohne learned-state reset, Retention alter Aufgaben, Ressourcenmatching, Replay-/Consolidation-Ablationen und robuste Rollback-Grenzen.

## Stufe 9 – Hochintegrierte künstliche Kognition

**Claim-Grenze:** Aufmerksamkeit, Planung, Motivation, Langzeiterinnerung und multimodale Integration müssen als getrennte operationale Konstrukte implementiert, abladierbar und anschließend integriert werden. Eine gemeinsame Benutzeroberfläche oder API ist keine integrierte Kognition.

## Stufe 10 – Bewusstseinsforschung

**Claim-Grenze:** Stufe 10 ist ausschließlich ein Forschungs- und Governance-Rahmen. Kein Stage-Score und kein beobachtetes Verhalten begründet für sich Bewusstsein, Sentienz, Leidensfähigkeit oder moralischen Status.

Vor jeder stärkeren Interpretation sind kontrastierende Theorien, vorab definierte diskriminierende Vorhersagen, kausale Interventionen, Ethik-/Stop-Kriterien und unabhängige adversariale Replikation erforderlich.

## Konsequenz für Release- und Forschungsplanung

Jedes Release soll künftig mindestens zwei Fortschrittsachsen berichten:

1. **Technische Entwicklung:** Implementierung, Integration, Verifikation, Runtime-/Persistenzstatus.
2. **Wissenschaftliche Entwicklung:** RQ/Hypothese, Protokoll, DATA, EVID, Replikation, Attribution.

Ein Release darf technisch weiter voranschreiten, ohne dass der wissenschaftliche Score steigt. Umgekehrt kann wissenschaftlicher Fortschritt durch bessere Kontrollen, Negativbefunde, externe Replikation oder engere Claim-Grenzen entstehen, ohne dass eine neue Produktfunktion implementiert wird. Genau diese Trennung ist ein Qualitätsmerkmal des Forschungsprogramms.
