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
