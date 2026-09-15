# Forschungsaddendum: Wissenschaftliche Reife, Kritikpunkte und Forschungsintegrität

**Datum:** 15. September 2026  
**Bezugsstand:** `14b5066c9f8eac9c7522d59966b9e81c29226c56`  
**Status:** Entwicklungsaddendum; keine automatische EVID-Promotion

## 1. Anlass

Die bisherige Release-Entwicklung zeigte technische Implementierung, Verifikation und einen zusammengefassten wissenschaftlichen Marker. Diese Darstellung konnte den falschen Eindruck erzeugen, dass eine weit entwickelte Infrastruktur automatisch eine ebenso weit entwickelte wissenschaftliche Evidenzlage bedeutet.

Dieses Addendum führt deshalb eine zweite, eigenständige wissenschaftliche Reifeachse für die Stufen 0–10 ein. Die Achse bewertet nicht Modulzahl oder UI-Fertigstellung, sondern die wissenschaftliche Kette aus Forschungsfrage, Protokoll, DATA, menschlich geprüfter EVID, unabhängiger Replikation und Attribution.

## 2. Korrektur der Fortschrittsinterpretation

Ein technischer Fortschrittswert beantwortet: **Ist der Mechanismus implementiert, integriert und technisch verifiziert?**

Ein wissenschaftlicher Fortschrittswert beantwortet dagegen: **Ist für die konkrete Behauptung eine nachvollziehbare, kontrollierte, quellengebundene und hinreichend unabhängige Evidenzkette vorhanden?**

Beide Größen dürfen auseinanderlaufen. Insbesondere kann eine Stage technisch weit fortgeschritten und wissenschaftlich noch offen sein.

## 3. Stage 6 als aktuelles Beispiel

Für Gedächtnis und Weltmodell liegen inzwischen mehr Grundlagen vor als im früheren Alpha.3-Befund: bounded working/episodic memory, zeitliche Zustände, ein Beobachtungsprädiktor, registrierte Kandidaten/Protokolle und Stage-6-DATA-Strukturen. Der aktuelle Hauptstand enthält zudem den Stage-6-Neural-World-Model-Registry-/DATA-Merge.

Trotzdem bleiben die zentralen wissenschaftlichen Grenzen bestehen:

- episodischer Speicher ist kein semantisches Gedächtnis;
- statistische Aggregation ist keine nachgewiesene Semantization;
- ein Ein-Schritt-Beobachtungsprädiktor ist kein generatives oder planungsfähiges Weltmodell;
- ein `prediction_error`-Messwert ist kein neuronaler Predictive-Coding-Mechanismus;
- Telemetrie und APIs sind Beobachtbarkeit, nicht Kognition;
- die aktuelle wissenschaftliche Reife darf deshalb nicht aus dem technischen Stage-6-Fortschrittswert abgeleitet werden.

Der wissenschaftliche Stage-6-Wert im neuen Manifest ist bewusst konservativ (`0.40`) und an konkrete fehlende Evidenzschritte gebunden.

## 4. Mechanismus-Lücken als Forschungsprogramm

### 4.1 Semantization und Replay

Aktuelle externe Arbeiten zeigen explizite Konsolidierungs-/Replay-Mechanismen als prüfbare Dynamik. Für MHRN folgt daraus kein Kopierauftrag, sondern ein experimentelles Programm:

1. episodische Akquisition definieren;
2. Offline-/Replay-Phase als explizite Intervention implementieren;
3. semantische Generalisierung operationalisieren;
4. Replay-on/off, shuffled replay und resource-matched controls vergleichen;
5. Retention, Generalisierung und Interferenz auf held-out Daten auswerten;
6. erst nach menschlichem Review EVID promoten.

### 4.2 Predictive Coding

Die Literatur kennt mehrere neuronale Repräsentationen von Prediction Error. MHRN muss vor Implementierung entscheiden, welche Klasse getestet wird. Die Forschungsfrage lautet nicht „gibt es ein Feld prediction_error?“, sondern beispielsweise: Verbessert eine explizite neuronale Fehlerrepräsentation unter identischem Ressourcenbudget Sequenzvorhersage oder Credit Assignment gegenüber geeigneten Kontrollen?

### 4.3 Weltmodell

Ein wissenschaftlich belastbares MHRN-Weltmodell benötigt mindestens einen internen, held-out validierten Übergangsmechanismus. Für stärkere Claims sind Mehrschritt-Prädiktion, Aktionskonditionierung, Gegenfaktuale oder planungsrelevante Interventionen notwendig. Reine Zustandsprotokollierung bleibt Telemetrie.

### 4.4 Multi-Timescale und Stabilitäts-Plastizitäts-Dilemma

MHRN besitzt mehrere technische Zeitskalen. Offen ist die kausale Frage, ob langsame Modulation/Konsolidierung tatsächlich Retention verbessert, ohne Adaptation unangemessen zu blockieren. Kandidaten wie astrozyteninspiriertes Gating gehören deshalb in eine kontrollierte Ablation, nicht als ungeprüfte biologische Wahrheit in den Produktivkern.

## 5. Kritikmanagement

„Kritikfrei“ ist kein wissenschaftlich sinnvolles Qualitätsziel. Eine robuste Arbeit soll stattdessen:

- bekannte Gegenargumente selbst benennen;
- Null- und Negativergebnisse erhalten;
- technische und wissenschaftliche Reife trennen;
- Alternativerklärungen testen;
- Mechanismusbeiträge durch Ablationen isolieren;
- Skalierungsclaims getrennt von Funktionsclaims behandeln;
- Unsicherheit und fehlende Replikation sichtbar halten.

Die neue Timeline macht diese offenen Punkte als Teil des Fortschritts sichtbar, statt sie durch einen einzigen Prozentwert zu verdecken.

## 6. Forschungsintegrität und Plagiatsrisiko

Plagiatsfreiheit kann nicht durch ein Repository-Gate garantiert werden. Das Projekt führt deshalb einen präventiven Integritätsprozess ein:

- Quellen- und Ideenprovenienz;
- Code-/Lizenzattribution;
- Offenlegung wiederverwendeter eigener Texte und Resultate;
- Quarantäne nicht verifizierter KI-generierter Literaturhinweise;
- manuelle Claim-zu-Quelle-Prüfung;
- externe Textähnlichkeitsprüfung vor Einreichung;
- getrennte Behandlung von Ähnlichkeit, korrekter Zitation und tatsächlichem Plagiat.

Verbindliche Regeln stehen in `research/INTEGRITY_AND_ATTRIBUTION.md`; verifizierte und quarantänisierte Literaturhinweise in `research/RELATED_WORK.md`.

## 7. Neue Release-Darstellung

Der Release-Bereich erhält zwei getrennte Darstellungen:

1. **Engineering Maturity** — bestehende repository-basierte technische Stage-Timeline.
2. **Scientific Maturity** — neue Stage-0–10-Timeline aus `src/dashboard/static/scientific-progress.json`.

Die wissenschaftliche Timeline verwendet folgende Gewichte:

| Dimension | Gewicht |
|---|---:|
| Forschungsfrage/Hypothese | 15 % |
| Protokoll | 20 % |
| DATA | 20 % |
| menschlich geprüfte EVID | 20 % |
| unabhängige Replikation | 15 % |
| Attribution / Related Work | 10 % |

Der resultierende Prozentwert ist eine Projekt-Reifeheuristik, **keine Kognitions-, Wahrheits- oder Qualitätsmetrik**. Die Einzelkriterien und Claim-Grenzen bleiben primär.

## 8. Literaturstand dieses Addendums

Verifizierte Referenzen und ihre begrenzte Verwendung sind in `research/RELATED_WORK.md` festgehalten. Dazu gehören Arbeiten zu hippocampal-kortikaler Semantization, corticohippocampal continual learning, predictive coding in SNNs, spiking world models und astrozyteninspiriertem Multi-Timescale-Lernen.

Nicht ausreichend verifizierte Namen/Claims aus früheren KI-gestützten Notizen werden nicht stillschweigend übernommen, sondern explizit quarantänisiert. Das betrifft insbesondere den behaupteten `ArithSpec`-Standard und mehrere noch nicht auf Primärquellen geprüfte 2026er Modellnamen.

## 9. Schlussfolgerung

Der wissenschaftliche Fortschritt des Projekts ist real, aber anders zu messen als der technische Fortschritt. MHRN hat in mehreren frühen und mittleren Stufen belastbare Forschungsinfrastruktur, registrierte Fragen, Protokolle und DATA aufgebaut. Menschlich freigegebene EVID und unabhängige Replikation bleiben jedoch deutlich seltener und müssen im Release-Status entsprechend sichtbar sein.

Der nächste qualitative Sprung liegt nicht in weiteren Datenfeldern oder APIs, sondern in **expliziten, abladierbaren kognitiven Mechanismen und deren unabhängiger Validierung**.
