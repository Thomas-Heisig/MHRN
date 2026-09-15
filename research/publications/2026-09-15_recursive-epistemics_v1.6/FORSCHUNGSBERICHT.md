# MHRN – Forschungsarbeit, Fassung 1.6

**Thomas Heisig | 15. September 2026**

Diese Fassung führt den empirischen Stand der Fassung 1.5 mit dem aktuellen Entwicklungsstand des Repositories zusammen, ohne historische Daten rückwirkend umzudeuten. Die vollständige Messkampagne der Fassung 1.5 bleibt die eingefrorene empirische Basis. Neue technische Implementierungen, Stage-4/5/6-Erweiterungen, Forschungspläne und wissenschaftliche Reifebewertungen werden als nachfolgende Entwicklung ausgewiesen.

## 1. Forschungsgegenstand und neue Trennung der Fortschrittsbegriffe

MHRN ist ein experimentelles Framework für rekurrente spikende neuronale Netze mit kontrollierter Plastizität, expliziten Systemgrenzen und quellengebundener Forschungsinfrastruktur. Eine zentrale methodische Korrektur dieser Fassung ist die formale Trennung von **Engineering-Reife** und **wissenschaftlicher Reife**.

Engineering-Reife fragt, ob ein Mechanismus implementiert, integriert, persistiert und technisch verifiziert ist. Wissenschaftliche Reife fragt, ob eine konkrete Behauptung durch eine falsifizierbare Forschungsfrage, ein vorab definiertes Protokoll, geeignete Kontrollarme, quellengebundene DATA, menschlich geprüfte EVID, unabhängige Replikation und vollständige Attribution getragen wird. Eine grüne CI, ein bestandener Unit-Test oder ein vorhandenes Datenfeld sind daher keine wissenschaftliche Bestätigung.

Diese Trennung wird systemweit über die Stufen 0–10 geführt. Die vollständige Matrix steht in `SCIENTIFIC_STAGE_MATRIX.md`; das Release-Frontend liest denselben Vertrag aus `src/dashboard/static/scientific-progress.json`.

## 2. Methodischer Grundsatz: Der Mechanismus ist die prüfbare Wissenschaft

Eine Datenstruktur kann einen Zustand speichern, aber sie erklärt nicht den Mechanismus, durch den dieser Zustand entsteht. Deshalb gilt in dieser Fassung eine verbindliche Unterscheidung:

- ein `episodic_memory`-Objekt ist nicht automatisch episodisches Gedächtnis im kognitionswissenschaftlichen Sinn;
- ein `semantic_memory`-Index ist nicht automatisch Semantization;
- ein `prediction_error`-Wert ist nicht automatisch Predictive Coding;
- ein `/api/cognition/world-model`-Endpunkt ist nicht automatisch ein Weltmodell;
- ein Behavior Profile ist nicht automatisch ein Selbstmodell;
- eine technische Identität ist kein Bewusstseinsnachweis.

Für jeden stärkeren Begriff muss der zugrunde liegende Mechanismus operationalisiert, intervenierbar und gegen Alternativerklärungen geprüft werden.

## 3. Stand der Stufen 0–5

### Stufe 0 – Einzelne Nervenzelle

Die implementierten Izhikevich-/LIF-Pfade, Referenzverträge und deterministischen Wiederholungen bilden eine belastbare Softwarebasis. Externe Vergleiche bleiben modell- und diskretisierungsabhängig. Biologische Gleichwertigkeit wird nicht behauptet.

### Stufe 1 – Kleines SNN

Kopplung, sparse Topologie und Spike-Ausbreitung sind technisch vorhanden. Der wissenschaftliche Wert bleibt begrenzt, solange keine task-basierte Intervention zeigt, welche konkrete Rechenfunktion aus der kleinen Netzwerkstruktur entsteht.

### Stufe 2 – Rekurrentes SNN

Lange deterministische Runs und Restore-Verträge stützen Stabilität unter den geprüften Bedingungen. Für die Behauptung funktional nützlicher Rekurrenz ist eine Rekurrenz-Ablation gegen feed-forward bzw. yoked/informationszerstörte Kontrollen erforderlich.

### Stufe 3 – Plastisches Nervengewebe

STDP, Eligibility/Drei-Faktor-Lernen, Homöostase und strukturelle Plastizität sind als Mechanismen implementiert. Die wissenschaftliche Lücke liegt in der kausalen Wirksamkeitsprüfung: Lerngewinn auf gehaltenen Aufgaben, Generalisierung, Interferenz und Mechanismusablation müssen stärker gewichtet werden als bloße Gewichtsänderung.

### Stufe 4 – Spezialisierte neuronale Areale

Modality-specific pathways, MSBA, Gateway-Verträge und experimentelle Frozen/Random/Shuffle-Kontrollen schaffen eine geeignete Architektur für multimodale Forschung. Die aufgezeichneten E01–E05-Läufe bleiben DATA, solange keine unabhängige Review-/EVID-Promotion erfolgt ist.

### Stufe 5 – Integriertes künstliches Nervensystem

Der synthetische geschlossene Regelkreis, autorisierte Aktorpfade, digitale Interozeption und Ressourcenbilanz bilden eine technische Embodiment-Basis. Die entscheidenden nächsten Kontrollen sind matched disturbance, yoked replay, interrupted feedback und wirkungslose Aktoren. Digitale Host-Telemetrie wird nicht als biologische Interozeption ausgegeben.

## 4. Stufe 6 – Gedächtnis und Weltmodell

Stage 6 ist der derzeit wichtigste Übergang von Forschungsinfrastruktur zu kognitiven Mechanismen. Das Repository enthält inzwischen zeitliche Zustände, begrenzte Working-/episodische Speicherpfade, semantische Prototyp-/Registry-Arbeit, Vorhersage-/Prediction-Error-Telemetrie, World-Model-Kandidaten und Stage-6-Protokolle. Diese Bausteine rechtfertigen jedoch noch keine Gleichsetzung mit den Mechanismen der aktuellen Gedächtnis- und Predictive-Coding-Forschung.

### 4.1 Episodisch und semantisch

Die Complementary-Learning-Systems-Tradition trennt schnelle episodische Speicherung von langsamer strukturierter Konsolidierung. Neuere SNN-Arbeiten zu Semantization und Replay zeigen, dass der Übergang nicht durch bloße statistische Aggregation definiert ist, sondern durch aktive Reaktivierung, Konsolidierung und veränderte Repräsentation. Für MHRN folgt daraus ein klarer Prüfvertrag: episodische Akquisition → Offline-/Low-input-Replay → semantische Konsolidierung, jeweils mit Replay-off, shuffled-replay und matched-compute Kontrollen.

### 4.2 Predictive Coding

Eine Vorhersage und eine Fehlerzahl reichen für Predictive Coding nicht aus. Ein entsprechender MHRN-Mechanismus muss top-down Vorhersage und bottom-up Fehlerbeitrag als kausal unterscheidbare Pfade definieren. Multi-Compartment- oder explizite Fehlerpopulationen sind mögliche Kandidaten, aber keine Vorgabe. Entscheidend ist die experimentelle Trennbarkeit: Pathway-on/off, Störung der Rückprojektion, zeitliche Delays und held-out Sequenzen.

### 4.3 Weltmodell

Der vorhandene Ein-Schritt-Vorhersagepfad ist eine Foundation. Ein stärkerer Weltmodell-Claim erfordert mindestens mehrschrittige und aktionskonditionierte Dynamik, Unsicherheitsbehandlung und einen Vorteil für Verhalten oder Planung gegenüber reiner Reaktivität. „Learning in imagination“ wäre ein zusätzlicher, eigenständig zu testender Claim.

### 4.4 Replay und Continual Learning

Replay ist zugleich Stage-6- und Stage-8-relevant. Ein Replay-Mechanismus muss nicht biologisch als „Schlaf“ bezeichnet werden. Wissenschaftlich prüfbar sind Retention, Transfer, Interferenz, Ressourcenverbrauch und der Unterschied zwischen strukturiertem Replay und bloß zusätzlicher Trainingszeit.

## 5. Stufen 7–10 und Claim-Disziplin

Stufe 7 verlangt kausale self/other Attribution; persistente Profile allein reichen nicht. Stufe 8 verlangt kontinuierliches Lernen in einem gemeinsam weitertrainierten System ohne Learned-State-Reset. Stufe 9 verlangt getrennte und anschließend integrierte Operationalisierung von Aufmerksamkeit, Planung, Motivation, Langzeiterinnerung und multimodaler Verarbeitung. Stufe 10 bleibt ausschließlich eine Forschungs- und Governance-Frontier; kein Score oder Verhalten etabliert Bewusstsein oder Sentienz.

## 6. Forschungsintegrität, Plagiatsrisiko und Eigenwiederverwendung

Die wissenschaftliche Integrität wird als Prozess behandelt. Externe Ideen, Algorithmen, Code, Abbildungen und Datensätze werden quellengebunden dokumentiert. Eigene Vorfassungen werden ebenfalls zitiert bzw. als geerbte Edition gekennzeichnet. Dadurch wird Text-Recycling nicht unsichtbar als neue Originalleistung ausgegeben.

Automatische oder KI-gestützte Literaturhinweise werden erst nach Prüfung bibliographischer Identität, DOI/Publisher und inhaltlicher Passung als Quelle verwendet. Unbestätigte Arbeiten bleiben in Quarantäne. Eine Repository-Prüfung kann keine Plagiatsfreiheit garantieren; vor formaler Einreichung bleiben menschliche Quellenkontrolle und gegebenenfalls externe Similarity-Prüfung erforderlich.

## 7. Related Work und wissenschaftliche Positionierung

MHRN wird nicht als „führend“ bezeichnet, nur weil eine ähnliche Architekturkomponente vorhanden ist. Der Vergleich mit Related Work erfolgt entlang konkreter Mechanismen und Messverträge. Für Stage 6 sind insbesondere CLS, SNN-Semantization, replay-vermitteltes Continual Learning, dendritische Prediction-Error-Modelle, spikendes Predictive Coding und Spiking World Models relevant. Die Literatur motiviert Hypothesen und Baselines; sie ist kein Ersatz für MHRN-Evidenz.

## 8. Reproduzierbarkeit

Reproduzierbarkeit umfasst mehr als Seed-Wiederholung. Notwendig sind Source-Commit, Konfiguration, Datensatz-/Stimulusversion, Softwareumgebung, numerischer Vertrag, Ausführungsart, Kontrollarme, Rohdaten, Digests und Auswertungsvertrag. Bit-exakte Plattformgleichheit wird nur dort behauptet, wo sie tatsächlich spezifiziert und getestet ist. Nicht verifizierte externe Spezifikationen werden nicht als Standard übernommen.

## 9. Release- und Publikationsmodell

Jeder Release soll künftig technische und wissenschaftliche Fortschritte getrennt berichten. Wissenschaftlicher Fortschritt kann auch in engeren Claims, besseren Kontrollen, einem Negativbefund oder einer unabhängigen Replikation bestehen. Umgekehrt darf eine neue technische Funktion den wissenschaftlichen Reifegrad unverändert lassen.

Fassung 1.6 ist daher selbst ein Beispiel dieser Trennung: Sie dokumentiert erhebliche methodische und wissenschaftliche Fortschritte, ohne neue historische DATA zu erfinden oder die Fassung 1.5 rückwirkend als konfirmatorischer erscheinen zu lassen.

## 10. Schlussfolgerung

MHRN besitzt eine ungewöhnlich umfangreiche Forschungsinfrastruktur und zunehmend reale neuronale Mechanismen. Die wesentliche nächste Aufgabe ist nicht weitere Benennung, sondern die Schließung der Mechanismus- und Evidenzlücken. Für Stage 6 bedeutet dies insbesondere Semantization durch Replay/Konsolidierung, kausal definierte Prediction-Error-Dynamik und ein mehrschrittiges aktionskonditioniertes Weltmodell. Für alle Stufen gilt: technische Funktion, technische Verifikation, wissenschaftliche DATA und akzeptierte EVID bleiben verschiedene Objekte.
