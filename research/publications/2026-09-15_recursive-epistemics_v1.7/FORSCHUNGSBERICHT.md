# MHRN — Forschungsbericht 1.7

**Thomas Heisig · 15. September 2026 · fortgeschriebene Arbeitsfassung**

## 1. Forschungsgegenstand

MHRN untersucht, wie ein spikendes neuronales System schrittweise von deterministischen Einzelneuronen über rekurrente Dynamik, Plastizität, spezialisierte Modalitäten und geschlossene sensorimotorische Schleifen zu Gedächtnis-, Vorhersage- und späteren Kognitionsmechanismen erweitert werden kann, ohne technische Implementierung mit wissenschaftlicher Evidenz gleichzusetzen.

Der Forschungsbericht 1.7 ist die aktuelle methodisch-empirische Projektion. Die eingefrorene empirische Basis 1.5 bleibt separat unverändert. Fassung 1.6 ist die direkte integrative Vorgängerfassung.

## 2. Methodische Grundhierarchie

```text
RQ → Hypothese → eingefrorenes Protokoll → Ausführung → DATA
   → Analyse/Limitationen → Human/Independent Review → EVID → Claim
```

Ein Unit-Test oder Green CI ist Engineering-Verifikation. Ein Experimentlauf erzeugt DATA. Erst eine explizite Reviewentscheidung kann aus geeigneten DATA Evidenz für einen begrenzten Claim machen. Diese Ebenen werden in Registry, Dashboard und Publikation getrennt.

## 3. Aktueller Entwicklungs- und Forschungsstand

### Stage 0 — Einzelne Nervenzelle

Deterministische Membrandynamik, Spike-/Refraktärverhalten und alternative Modellpfade bilden die technische Grundlage. Offen bleiben systematische Integrator-/Parameterablationen und unabhängige Replikation. Biologische Inspiration wird nicht als Vollsimulation bezeichnet.

### Stage 1 — kleine Netzwerke

Signalweitergabe und lokale Netzwerkdynamik sind technisch verfügbar. Wissenschaftliche Reife bleibt geringer als die Engineeringreife, solange kontrollierte Multi-Seed-Studien und systematische Topologievergleiche fehlen.

### Stage 2 — stabiles rekurrentes SNN

Der scoped Engineeringvertrag wurde durch Langlauf-, Replay- und Restore-Prüfungen erreicht. Wissenschaftlich bleiben Zielskalierung, Dynamikregime, Störungsrobustheit und unabhängige Replikation eigenständige Aufgaben.

### Stage 3 — plastisches Nervengewebe

STDP, Eligibility, Drei-Faktor-Modulation, Homeostase, strukturelle Plastizität und Ressourcenregulation sind als Mechanismen integriert beziehungsweise referenzierbar. `Proposal → Approval → Mutation → Journal → Undo` macht strukturelle Änderung auditierbar. Der wissenschaftliche Nutzen dieser Mechanismen benötigt held-out Kontrollen und Multi-Seed-EVID.

### Stage 4 — spezialisierte neuronale Areale

Audio-, Vision- und Digitalpfade besitzen getrennte Adapter-/Kodierungs-/Plastizitätsverträge. E01–E05 liefern technische und DATA-Grundlagen. Die Hypothese eines funktionalen Vorteils spezialisierter Pfade bleibt durch matched/frozen/random/shuffle/lesion Controls zu prüfen.

### Stage 5 — integriertes künstliches Nervensystem

Sensorik, digitale Interozeption, autorisierte Aktorik, Feedback und Ressourcen sind Full-Stack integriert. Real-Device-, Sensor-Loss-, Actuator-No-Effect- und Open-/Closed-loop-EVID bleiben offen.

### Stage 6 — Gedächtnis und Weltmodell

Bounded Working-/Episodic-Memory, semantische Kandidaten, Replay-/Ablationsverträge, Prediction-/Prediction-Error-Infrastruktur und World-Model-Kandidaten bilden eine experimentierbare Grundlage. Daraus folgen ausdrücklich noch keine Claims vollständiger Semantization, hierarchischen Predictive Codings oder eines validierten generativen Weltmodells.

Drei confirmatory Linien sind prioritär:

1. Episoden → Replay/Konsolidierung → Generalisierung/Semantization gegen Replay-off und shuffled-replay.
2. Kausaler neuronaler Prediction Error gegen Residual-/Feedforward-Erklärungen.
3. Mehrschrittige action-conditioned Prediction mit uncertainty/OOD und decision-benefit gegen reactive/no-model/corrupted-model.

### Stage 7 — Identität/Selbstmodellgrundlagen

Versionierte technische Profile, Lineage und Behavior Profile sind technische Identitätsmechanismen. Sie sind kein psychologisches Selbst. Ein Selbstmodellclaim erfordert kausale self/other Repräsentation und messbaren funktionalen Nutzen.

### Stages 8–10 — Forschungsfrontier

Diese Bereiche werden als Forschungsprogramm und nicht als Ergebnis geführt. Für höhere Kognition, Metakognition/soziale Modelle und Bewusstseinsgrenzfragen fehlen hinreichende Operationalisierung, Implementierung und Evidenz. Insbesondere ist kein Stage-Score ein Bewusstseinsindikator.

## 4. Duale Reifebewertung

Engineering und Wissenschaft werden als getrennte Achsen geführt. Die wissenschaftliche Achse verwendet explizite Kriterien für Forschungsfrage, Protokoll, DATA, reviewte EVID, unabhängige Replikation und Attribution. Die Werte sind Governance-Signale und dürfen nicht als Intelligenzkennzahl interpretiert werden.

Der konservative Snapshot 1.7 liegt für Stage 0–10 bei 50, 30, 65, 55, 55, 55, 40, 28, 23, 15 und 13 Prozent wissenschaftlicher Reife. Die Einzelkriterien und Claim-Grenzen haben Vorrang vor dem aggregierten Wert.

## 5. Negative und unvollständige Befunde

Negative Ergebnisse und Instrumentierungsgrenzen bleiben erhalten. Frühere Läufe ohne hinreichend beobachtete Aktivität, boundary audits ohne direkten Hypothesentest und fehlgeschlagene Skalierungsversuche werden nicht rückwirkend positiv umgedeutet. Eine verbesserte Messmethode erzeugt einen neuen Run.

## 6. 5D-Adressraum

Der 5D-Adressraum bleibt eine technische Repräsentation und ungeprüfte funktionale Hypothese. Eine Überlegenheit kann nur über gematchte Dimensionsablationen gezeigt werden. 2D/3D/4D/5D/6D/8D-Vergleiche müssen Konnektivität, Ressourcen, Parameterzahl und Auswertungsbudget kontrollieren.

## 7. Reproduzierbarkeit

Je nach Experiment müssen neben Seeds alle claim-relevanten Zustände persistiert sein: neuronale/synaptische Zustände, Queues/Delays, Plastizitätstraces, strukturelle Journale, Ressourcen/Homeostase, Memory/World Model, Gateways, Profile und Inputs. Eine Pause/Resume-Äquivalenz ist nicht vollständig, solange gekoppelte Kognitionszustände außerhalb der Checkpointgrenze liegen.

## 8. Forschungsintegrität

Die Arbeit ist kumulativ und nutzt externe Theorien, Methoden und Softwareideen. Genau deshalb werden Übernahme, Transformation, Eigenentwicklung und ungeklärte Neuheit getrennt. Unverifizierte Quellen bleiben quarantined. Ein internes Similarity-Audit reduziert Risiken, ersetzt aber keine externe Plagiats-/Quellenprüfung.

## 9. Potenzielle Beiträge

Drei Kandidaten werden gezielt auf Prior Art geprüft:

- Trennung `Logical Identity / Physical Slot / Synaptic Reduction / Execution Scheduling`;
- `Proposal → Approval → Mutation → Journal → Undo` für strukturelle Plastizität;
- Trennung `Content Gateway / Compute Backend`.

Diese Punkte sind heute dokumentierbare MHRN-Mechanismen beziehungsweise Architekturentscheidungen. Ihre wissenschaftliche Neuheit wird nicht vorweggenommen.

## 10. Dokumentgovernance

Alle Dateien unter `docs/` und `research/` werden durch den Governance-Audit klassifiziert. Publikationen, Experimente, Registry, Schemas, generierte Projektionen und historische Dokumente erhalten unterschiedliche Status-/Autoritätsklassen. Damit soll verhindert werden, dass ein alter Report allein durch seine Auffindbarkeit als aktueller wissenschaftlicher Stand gelesen wird.

## 11. Publikationslinie

- 1.5: frozen empirical baseline;
- 1.6: historische integrative Vorgängerfassung;
- 1.7: aktuelles Work-in-Progress-Vollmanuskript im Publication Viewer.

Die aktuelle Fassung verweist sichtbar auf ihre Vorgänger. Historische Fassungen bleiben direkt erreichbar.

## 12. Priorisierte nächste Experimente

1. Stage-0 Modell-/Integratorablation.
2. Stage-2 unabhängige Replikation und Zielskalierung.
3. Stage-3 held-out Plasticity/Resource-Experimente.
4. Stage-4 modality-specific matched controls.
5. Stage-5 closed-loop Läsions-/No-Effect-Experimente.
6. Stage-6 Replay/Semantization, neural Prediction Error, action-conditioned World Model.
7. Stage-7 self/other Interventionen und vollständige Checkpointäquivalenz.
8. Dimensionsablation 2D–8D.
9. Prior-Art-Review der potenziellen Architekturbeiträge.
10. Externer Quellen-/Similarity-/Methodenaudit vor formaler Einreichung.

## 13. Schlussfolgerung

Der Fortschritt von MHRN liegt derzeit gleichermaßen in Mechanismen und in der wachsenden Fähigkeit, deren Aussagegrenzen sichtbar zu machen. Die belastbarste wissenschaftliche Position ist deshalb nicht „das System hat Kognition erreicht“, sondern: MHRN stellt zunehmend präzise, reproduzierbare Mechanismen und Experimentierräume bereit; stärkere kognitive Aussagen bleiben Hypothesen, bis kontrollierte DATA, Review und Replikation vorliegen.
