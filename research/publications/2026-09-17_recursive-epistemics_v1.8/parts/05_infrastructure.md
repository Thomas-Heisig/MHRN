# Teil V — Wissenschaftliche Infrastruktur und Engineering

## 20. Determinismus und Zustandsgrenzen

Reproduzierbarkeit ist mehr als ein Seed. Hypothesenrelevante Zustände können RNG, Scheduler, Neuronen, Synapsen, Delays, Queues, Plastizitätstraces, Eligibility, Strukturjournal, Homeostase, Ressourcen, Gedächtnis, World Model, Gateway-Zustand, Sensorinput und Code-/Konfigurationsdigest umfassen. Pause/Resume-Äquivalenz ist nur so stark wie die definierte Checkpointgrenze.

MHRN trennt Logical Identity, Physical Slot, Synaptic Reduction und Execution Scheduling. Diese Trennung soll verhindern, dass Speicherlayout oder GPU-Reihenfolge unbemerkt die wissenschaftliche Semantik verändern. Byteidentität ist nicht für jede Plattform realistisch; deshalb werden bitnahe, numerische und statistische Reproduktionsklassen unterschieden.

## 21. Storage und Digital State

Die frühere Idee eines „Digital State Twin“ bleibt erhalten, wird aber begrifflich begrenzt. Solange kein physisches Gegenstück synchron gekoppelt ist, beschreibt der Begriff primär einen reproduzierbaren digitalen Zustandszwilling. Primärzustände, Ereignisprovenienz und Rekonstruktionsverträge haben Vorrang vor löschbaren Heatmaps oder Analyseprojektionen.

Sparse Materialisierung, arrayorientierte Strukturen, Chunking und graphgeeignete Persistenz sind Skalierungsfragen. Millionen Python-Objekte sind kein wissenschaftliches Ziel. Ein großer Adressraum darf nicht mit einer vollständig materialisierten Population verwechselt werden.

## 22. Runtime, Beschleunigung und Ressourcen

Runtime-Performance ist wissenschaftlich relevant, wenn sie bestimmt, welche Skalen oder Zeitspannen überhaupt experimentell zugänglich sind. Beschleunigung darf jedoch Integrationsschritt, Ereignisordnung oder Reduktionsregeln nicht still verändern. Ressourcenproxies werden nicht als physikalische Energie ausgegeben, solange keine entsprechende Kalibration vorliegt.

## 23. Dashboard, Viewer und Research Catalog

Das Frontend ist wissenschaftliches Instrument. Es muss Engineering-Reife, wissenschaftliche Reife, DATA, EVID und Planung sichtbar trennen. Der Publication Viewer zeigt die aktuelle Arbeitsfassung, hält aber Frozen 1.5 und Vorgänger erreichbar. Eine schöne Oberfläche darf keinen stärkeren Claim erzeugen als das Quellartefakt.

Edition 1.8 ergänzt deshalb einen maschinellen Quellenindex, eine unveränderte Registry-Projektion und ein Erhaltungsmanifest. Jeder historische Publikationsblob am Basiscommit wird gehasht. Alle damaligen Markdown-Überschriften in `docs/` und `research/` werden indiziert. Dies schafft eine überprüfbare Untergrenze gegen versehentliches Vergessen, aber keine Garantie semantischer Vollständigkeit.

## 24. Lokale KI-Werkzeuge als Forschungsinfrastruktur

Arbeiten an lokalen Chat-/Assistenzsystemen, Provider-Adaptern, Streaming, persistenten Konversationen und Trainings-Workbenches fließen dort ein, wo sie den Forschungsprozess betreffen: reproduzierbare Datensätze, Trennung von Quelle/Dataset/Job/Artefakt, lokaler Datenschutz, Provider-Isolation und Werkzeugprovenienz. Sie werden nicht als neuronale Evidenz für MHRN umgedeutet.

Die Grenze zwischen Forschungswerkzeug und Forschungsobjekt bleibt explizit. Ein LLM kann einen Runner schreiben oder einen Bericht kritisieren; der daraus entstehende Commit muss dennoch durch Tests, Review und experimentelle Provenienz abgesichert werden.

## 24.1 Infrastruktur als Ergebnis der Fehlersuche

Mehrere zentrale Infrastrukturentscheidungen entstanden nicht am Reißbrett, sondern aus konkreten Fehlerfällen. Die Entwicklungsgeschichte zeigt dabei vier wiederkehrende Klassen.

### Zustandsfehler

Frühe Persistenzfragen machten deutlich, dass ein gespeicherter Graph allein keinen wissenschaftlich identischen Zustand garantiert. Scheduler, RNG, Delays, Queues, Plastizitätstraces und externe Gateway-Zustände können den weiteren Verlauf verändern. Daraus entstand der kanonische Scientific-State-Ansatz mit vollständigerer Zustandsgrenze und digestierbarer Repräsentation.

### Semantikfehler

LIF-Refraktärzeiten zeigten exemplarisch, dass zwei Systeme denselben Zahlenwert verwenden können und dennoch unterschiedliche zeitliche Semantik besitzen. Deshalb werden Konfigurationen nicht nur als Zahlen gespeichert, sondern mit Modell- und Semantikprovenienz behandelt.

### Reportingfehler

`EXP-GEN-0036` zeigte, dass vollständige DATA durch eine zu enge universelle Summary-Tabelle wie fehlende DATA aussehen können. Der Fehler lag in der Projektion, nicht im Runner. Daraus folgt eine Infrastrukturregel: Reports müssen protokollspezifische Statistiktypen tragen; ein leeres Feld in einer fremden Metrik darf nie automatisch als fehlender Run interpretiert werden.

### AI-Normalisierungsfehler

Der AIRR-Pfad hatte verwertbare verschachtelte Analysefelder, erwartete aber ein flaches `assessment`. Dadurch wurde vorhandene Analyse fälschlich als nicht verfügbar normalisiert und die Konfidenz auf 0 gesetzt. Der Fix war ein Schemafix, keine Änderung der DATA. Die methodische Konsequenz ist dauerhaft: AI-Outputs benötigen deterministische Schemaadapter und bleiben Interpretation, niemals automatische EVID.

### Semantisches Gate als reale Blockade: EXP-GEN-0046

Der aktuelle Determinismuslauf demonstriert, warum die Statusarchitektur praktisch notwendig ist. Obwohl EXP-GEN-0046 technisch vollständig ausgeführt wurde, der Tick-Vertrag erfüllt ist und reproduzierbare Metriken vorliegen, lautet die semantische Zuordnung `NOT_AUTOMATICALLY_CLASSIFIED`. Die Evidence Readiness bleibt dadurch `BLOCKED_UNCLASSIFIED_SEMANTICS`.

Das ist kein Defekt, sondern gewünschtes Verhalten: Ein technisch erfolgreicher Lauf darf nicht allein wegen konsistenter Zahlen zu EVID werden. Erst eine registrierte semantische Zuordnung und Human Review dürfen die nächste Statusstufe öffnen. Auch der erzeugte AIRR bleibt `evidence=false`, `interpretation_only=true` und `human_review_required=true`.

## 24.2 Engineering und Scientific Maturity als getrennte Achsen

Eine der wichtigsten infrastrukturellen Erkenntnisse ist, dass „fertig gebaut“ und „wissenschaftlich getragen“ unterschiedliche Zustände sind. Stage 4 kann technisch vollständig integrierte Audio-/Vision-/Digitalpfade besitzen und trotzdem wissenschaftlich offene Fragen zu funktionaler Mehrleistung haben. Stage 5 kann einen grünen Closed-Loop-Vertrag besitzen und trotzdem keine Realwelt-Generalisation belegen. Stage 0 kann für einen eng definierten Readiness-Scope 100 % erreichen, während Human-EVID und unabhängige Replikation weiterhin offen bleiben.

Diese Trennung ist im Dashboard absichtlich sichtbar. Prozentwerte sind nur zusammen mit ihrem Scope und den Kriterien zulässig; sie sind keine Intelligenz-, Kognitions- oder Bewusstseinsmetriken.

## 24.3 Der Publication Viewer als Provenienzoberfläche

Die Arbeit am Publication Viewer führte zu einer wichtigen wissenschaftlichen Anforderung: Eine Publikation ist nicht nur Text, sondern eine navigierbare Provenienzoberfläche. Formeln, Anker, Literatur, Vorgängerversionen, Frozen-Baselines und aktuelle WIP-Änderungen müssen erreichbar bleiben.

Daraus entstand der heutige Editionsvertrag: 1.5 bleibt frozen, 1.6/1.7 bleiben historische Vorgänger, 1.8 ist current WIP, und der Viewer darf alte Zustände nicht durch die aktuelle Interpretation überschreiben. Die aktuelle Fassung darf ältere Befunde einordnen, aber nicht ihre historischen Bytes oder damaligen Statusbehauptungen still ändern.

## 24.4 Full Stack ist kein wissenschaftlicher Endpunkt

Frontend, API und Backend werden bewusst End-to-End integriert, weil fehlende Instrumentierung Forschung verhindern kann. Ein sichtbarer Sensorstatus, ein Stage-Panel oder ein Ask-KI-Button sind jedoch keine Evidenz. Full-Stack-Funktion ist ein **Mess- und Bedienbarkeitsvertrag**.

Diese Grenze ist besonders wichtig für spätere Stages: Ein UI-Feld „Self Model“, „World Model“ oder „Consciousness“ darf niemals als Hinweis gelten, dass die entsprechende Fähigkeit existiert. Die wissenschaftliche Autorität liegt in den zugrunde liegenden RQ/Hypothesen, Protokollen, DATA, Reviews und EVID-Entscheidungen.

## 24.5 Lokale und externe KI als austauschbare Forschungswerkzeuge

Aus den Arbeiten an lokalen Chat-Systemen, Kernschmied und Provider-Adaptern wurde eine weitere Designregel übernommen: Provider müssen austauschbar sein, ohne dass der wissenschaftliche Status eines Artefakts vom Marken- oder Modellnamen abhängt. Wichtig sind Eingabe, Ausgabe, Version, Berechtigung, Provenienz und der Pfad, auf dem ein Ergebnis in Code oder Forschung eingeflossen ist.

Ein lokales Modell kann Datenschutz und Reproduzierbarkeit verbessern; ein externes Modell kann Recherche- oder Codingqualität erhöhen. Beides ändert nicht die Grundregel: Kein Sprachmodell erhält allein durch Leistungsfähigkeit wissenschaftliche Autorität oder stillen Schreibzugriff auf den kausalen SNN-Kern.
