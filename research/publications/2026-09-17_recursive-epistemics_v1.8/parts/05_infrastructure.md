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

## 24.6 Gateways, exakte Digitaldaten und periphere Laufzeit

Neural Symbiosis konkretisiert die Infrastrukturgrenze zwischen externen/peripheren Modellen und dem SNN. Der Gateway-Runtime besitzt eigene Zustände, Gewichte, Delays, RNG-Provenienz, Condition, Tick, Ressourcenmetriken und Strukturjournal. Dadurch kann ein Experiment Frozen/Random/Shuffle/Plastic kontrollieren, ohne den kanonischen Kernzustand heimlich umzudefinieren. Es existiert absichtlich kein allgemeiner produktiver „Plasticity on“-Schalter; wissenschaftliche Aktivierung muss über einen registrierten Experimentpfad erfolgen.

Für digitale Pfade ist die Trennung von **exaktem Payload** und **neuronaler Projektion** fundamental. Prüfsummen, Sequenzen, Codec und Provenienz gehören zum exakten Symbolzustand außerhalb des SNN. Eine neuronale Population darf eine Approximation oder Repräsentation tragen, aber niemals nachträglich als Beweis verwendet werden, dass die ursprünglichen Bits selbst neuronal gespeichert oder unverändert rekonstruiert wurden.

## 24.7 Körpertelemetrie als Datenprovenienz

Die Real-Body-/Wesen-Arbeiten formulieren eine Infrastrukturregel, die über das Frontend hinausgeht: **Keine Fantasiedaten.** Fehlende Sensor- oder Hostwerte bleiben `UNKNOWN`; gemessene, abgeleitete und lediglich dargestellte Größen sind zu unterscheiden. Diese Regel ist dieselbe epistemische Disziplin, die später DATA von Report und EVID trennt. Eine scheinbar vollständige Oberfläche darf eine Messlücke nicht durch einen plausiblen Default verdecken.

## 24.8 Technische Identität als reproduzierbare Konfiguration

Profile & Identity ergänzt die Persistenzschicht um versionierte technische Konfiguration, Digest, Revision, Lineage und Snapshotbindung. Für Experimente können damit `profile_id`, Revision, Profil-Digest und Snapshot-Digest gemeinsam gebunden werden. Das verbessert Reproduzierbarkeit, ohne den Profilbegriff psychologisch aufzuladen. Ein Profil ist eine deklarierte technische Identität; der dynamische neuronale Zustand und der vollständige kausale Checkpoint bleiben getrennte Objekte.

## 24.9 Frozen-Environment FE-3 als backend-neutrale Ausführungsgrenze

Die Beschleunigungsintegration trennt inzwischen nicht nur neuronale Backend-Parität von wissenschaftlicher Evidenz, sondern auch zwei verschiedene Closed-Loop-Nachweise. Der ältere Builder-D3c-Pfad bleibt ein Playground-naher Engineering-Kontrollpfad. Zusätzlich existiert nun ein kanonischer FE-3-Adapter zwischen `FrozenWorldSession` und dem backend-neutralen `ExecutionBackend`.

Der Adapter erzeugt pro Tick aus dem aktuellen Weltzustand einen exakten `BoundaryFrame`, kodiert daraus einen deterministischen externen Stromvektor, führt genau den aktuellen Backend-Tick aus, dekodiert Spikes in einen `ActionCommand` und gibt diesen an die eingefrorene Welt zurück. Dadurch hängt der nächste Sensorzustand kausal von der Backend-Ausgabe ab. CPU-Referenz und CUDA verwenden dieselbe Schnittstelle; der CUDA-Kernel selbst wird für diese Kopplung nicht verändert.

Für die erste Hardware-Abnahme ist ein versioniertes Manifest `FE3_DETERMINISTIC_TARGET_V1.json` eingefroren. Entscheidend sind identischer Manifest-Hash, identischer Live-Input-Fingerprint und exakte D3c-Trajektorienparität. Die Execution Fingerprints von CPU und CUDA müssen dagegen absichtlich verschieden bleiben, weil Backend-Identität Teil der Provenienz ist.

Dieser Stand ist Engineering-Infrastruktur. Hosted CI kann Adapter, Manifest und CPU-Kontrollen prüfen; die physische CPU-vs-CUDA-FE-3-Abnahme auf der RTX-Referenzhardware bleibt ein eigener realer Nachweis. Weder Adapterimplementierung noch ein später grüner Hardware-Lauf erzeugen automatisch DATA, EVID, einen Speedup-Claim oder Aussagen über PAN-Hyperstate, Lernen oder Kognition.

## 24.10 Frontend-Projektion der Backend- und Evidenzgrenze

Der Dashboard-Stand bildet diese Grenze nun direkt aus kanonischen Quellen ab. Die Integrationsprojektion unterscheidet drei Zustände: **kanonisch integriert**, **softwareseitig verifiziert** und **physisch auf Referenzhardware akzeptiert**. Die ersten beiden Zustände können aus Quellstruktur, Backend-Capabilities und dem selbstverifizierenden FE-3-Manifest abgeleitet werden. Der dritte Zustand wird ausschließlich dann als erfüllt dargestellt, wenn ein geprüftes, datiertes `HARDWARE_ACCEPTANCE_<date>.json` im kanonischen Dokumentationspfad vorliegt.

Die gleiche Information erscheint kontextabhängig an mehreren Stellen: im Playground als Promotion-/Integrationspfad, im Release-Bereich als Engineering-Acceptance, im wissenschaftlichen Observatory als explizite Evidenzgrenze und unter `OLD` nur als Archiv-/Kompatibilitätshinweis. Damit wird Frontend-Vollständigkeit nicht mit wissenschaftlicher Reife verwechselt. Insbesondere bleibt ein grüner Hardware-Status **Engineering Verification**; DATA/EVID benötigen weiterhin den separaten preregistrierten Forschungs- und Reviewpfad.
