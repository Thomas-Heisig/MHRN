# MHRN — Forschungsgetriebener Entwicklungsmodus

**Status:** canonical working rule  
**Gültig ab:** Edition 1.7 / 2026-09-16  
**Geltungsbereich:** neue wissenschaftlich relevante Mechanismen, Experimente und Stage-Entscheidungen

## 1. Kanonischer Grundsatz

> **MHRN wird als wissenschaftsgetriebenes System entwickelt. Neue Mechanismen, Module und Fähigkeiten werden grundsätzlich aus expliziten Forschungsfragen, experimentellen Befunden, methodischen Erfordernissen oder nachgewiesenen technischen Grenzen abgeleitet. Die Softwarearchitektur wächst damit aus dem Forschungsprozess; sie ist nicht dessen nachträgliche Rechtfertigung.**

> **Ein negatives Experiment gilt nicht als Entwicklungsfehler. Es begrenzt den Hypothesenraum und kann unmittelbar die nächste Architekturentscheidung bestimmen.**

Die bevorzugte Entwicklungsrichtung lautet damit:

`Forschungsfrage → Hypothesen → Experimentbedarf → minimale Implementierung → technische Validierung → Freeze → DATA → Analyse → Human Review → EVID → Antwort → Folgefrage`

Nicht kanonisch ist dagegen:

`Feature → Feature → Feature → nachträgliche wissenschaftliche Begründung`.

## 2. Forschungsobjekte und Statusgrenzen

Jedes Forschungsobjekt besitzt seinen **eigenen** Status. Insbesondere dürfen folgende Ebenen nicht gleichgesetzt werden:

- Forschungsfrage (RQ),
- Hypothese (H),
- Experiment (EXP),
- Roh- und Auswertungsdaten (DATA),
- Human Review,
- akzeptierte Evidenz (EVID),
- Claim,
- technische Implementierung,
- Publikationsstand.

Ein abgeschlossenes Experiment ist DATA, aber nicht automatisch EVID. Ein Claim-Status ist kein RQ-Status. Eine implementierte Fähigkeit beantwortet keine Forschungsfrage ohne die hierfür definierte Evidenzkette.

Das minimale gemeinsame Mapping-Schema liegt unter:

`research/schemas/research_object_mapping.schema.json`

Es enthält nur:

- `id`
- `axis`
- `stage`
- `object_type`
- `evidence_mode`
- `parent_ids`
- `publication_refs`
- `status`

Dieses Schema ist absichtlich klein. Eine vollständige manuelle Master-Matrix über sämtliche historischen Objekte ist **nicht** Voraussetzung des aktuellen Arbeitszyklus und soll nicht als einmalige Großmigration den eigentlichen Forschungsprozess blockieren.

## 3. Phase 0 vor dem ersten neuen Zyklus

Vor der nächsten empirischen Ausführung müssen einmalig folgende Voraussetzungen erfüllt sein:

1. `EVIDENCE_MATRIX` trennt RQ- und Claim-Status.
2. Die generierte Summary besitzt einen Regressionstest für diese Trennung.
3. Das minimale Mapping-Schema ist festgeschrieben.
4. Der aktuelle Experiment-Freeze ist gegen den tatsächlich auszuführenden Quellstand geprüft.
5. Tests, Runner, Analysecode, DATA-Schema und Hashbindung sind vor produktiven Daten validiert.
6. Die Ausführung wird erst **danach** separat autorisiert.

## 4. Ein Experiment = ein vollständiger Forschungszyklus

### 4.1 Forschungsfrage auswählen

Ausgangspunkt ist immer eine offene Forschungsfrage, nicht ein gewünschtes Feature.

Mindestens zu erfassen:

`RQ-ID → Achse → Stage → übergeordnete Forschungsfrage → bisheriger Wissensstand`

### 4.2 Hypothesen vor Daten kontrollieren

Vor neuen produktiven Daten müssen dokumentiert sein:

- H1,
- H0,
- Gegenhypothese(n),
- erwartbare Alternativerklärungen,
- Falsifikationskriterien,
- primäre Endpunkte,
- Kontrollen,
- Seeds,
- Statistik,
- Ausschluss-, Missing- und Abort-Regeln.

Fehlende Punkte werden **vor** der Ausführung ergänzt.

### 4.3 Experimentelle Fähigkeit bestimmen

Erst jetzt wird gefragt:

> Welche Fähigkeiten benötigt dieses Experiment, die MHRN heute noch nicht besitzt?

Die Antwort wird getrennt in:

- **für das Experiment notwendig** → darf implementiert werden;
- **interessant, aber nicht erforderlich** → Backlog.

### 4.4 Nur erforderlichen Code implementieren

Jede neue wissenschaftlich relevante Funktion soll eine nachvollziehbare Herkunft besitzen:

`RQ → benötigte Fähigkeit → fehlende Komponente → Implementierung → Tests`

Damit bleibt später rekonstruierbar, warum ein Mechanismus in MHRN eingeführt wurde.

### 4.5 Technisch validieren

Vor produktiven Daten:

- Unit Tests,
- Integration Tests,
- deterministische Tests,
- synthetische Daten,
- Kontrollbedingungen,
- Seed-Reproduzierbarkeit,
- Budgetkontrollen,
- DATA-Schema,
- Analysecode.

Synthetische Validierung darf nicht als empirischer Befund ausgegeben werden.

### 4.6 Präregistrierung einfrieren

Die Kette

`RQ → H → Operationalisierung → Experiment → Runner → Analyse → Freeze`

wird SHA-256-gebunden.

Nach dem Freeze gilt:

> **Keine wissenschaftlich relevante Änderung am eingefrorenen Experiment.**

Eine notwendige wissenschaftliche Änderung erzeugt eine neue Experiment-ID oder eine explizit versionierte neue Präregistrierung; historische DATA werden nicht rückwirkend umdefiniert.

### 4.7 Experiment ausführen

Erst nach erfolgreichem Freeze und separater Authorization entstehen produktive DATA.

Dabei gilt:

- alle präregistrierten Seeds ausführen,
- alle präregistrierten Kontrollen ausführen,
- keine Ergebnis-Selektion,
- Abbrüche protokollieren,
- negative und Nullbefunde behalten,
- Rohdaten unverändert persistieren.

### 4.8 Präregistrierte Analyse durchführen

Die präregistrierte Hauptanalyse entscheidet die konfirmatorischen Hypothesen.

Zusätzliche Beobachtungen müssen als `exploratory` markiert werden.

- konfirmatorischer Befund → beantwortet eine bestehende Frage;
- exploratorischer Befund → kann eine neue Forschungsfrage erzeugen.

### 4.9 Forschungsfrage tatsächlich beantworten

Ein Experiment ist nicht allein durch `completed` abgeschlossen. Die zugehörige RQ erhält eine explizite Antwort oder den Status, dass sie weiterhin unbeantwortet ist.

Mindestens zu dokumentieren:

- Ergebnis,
- Status jeder konfirmatorischen Hypothese (`supported`, `refuted`, `inconclusive` oder projektweit definierte Entsprechung),
- Evidenzgrenzen,
- Alternativerklärungen,
- ausdrücklich **nicht** gezeigte Aussagen,
- Konfidenz,
- Folgefrage.

### 4.10 DATA → Human Review → EVID

Die verbindliche Kette lautet:

`Experiment → DATA → Machine Report → Human Review → EVID → Hypothesenstatus → Claim`

Kein Runner und kein Machine Report darf seine eigenen Ergebnisse automatisch zu akzeptierter Evidenz erklären.

### 4.11 Wissenschaftliche Arbeit sofort fortschreiben

Nach jedem abgeschlossenen Forschungszyklus werden, soweit betroffen, unmittelbar aktualisiert:

- Forschungsfrage,
- Methodik,
- Ergebnisse,
- Tabellen und Grafiken,
- Diskussion,
- Limitationen,
- Claims,
- offene Fragen,
- Evidenzmatrix,
- aktuelle Dissertation/Edition,
- Publication Viewer.

Die aktuelle Publikation soll den aktuellen Forschungsstand abbilden; frozen Editionen bleiben unverändert reproduzierbar.

### 4.12 Erst aus dem Befund die nächste Fähigkeit ableiten

Nach der Interpretation lautet die nächste Architekturfrage:

> Was hat das Experiment über MHRN gezeigt, und welche nächste technische Fähigkeit ergibt sich daraus wissenschaftlich?

Ein Mechanismus wird daher nicht implementiert, weil er allgemein plausibel oder interessant ist, sondern weil eine explizite RQ, ein empirischer Befund, eine methodische Notwendigkeit oder eine nachgewiesene technische Grenze ihn verlangt.

## 5. Stage-Governance

Stages bleiben Orientierungsrahmen, aber Prozentwerte oder vorhandene Features allein schließen eine Stage nicht wissenschaftlich ab.

Für jede Stage sollen schrittweise definiert werden:

- Exit-RQs,
- erforderliche Hypothesenentscheidungen,
- minimale Evidenzarten,
- Replikations- oder Robustheitsanforderungen,
- bekannte offene Grenzen.

Die maßgebliche Frage lautet:

> **Welche Forschungsfragen müssen beantwortet und welche Evidenzanforderungen erfüllt sein, damit diese Stage wissenschaftlich als erreicht gelten kann?**

Ein Stage-Score darf deshalb nicht automatisch aus Feature-Vollständigkeit abgeleitet werden.

## 6. Aktueller erster Zyklus: CL-003

Der erste Zyklus unter diesem Modus ist:

1. Evidence-Matrix-Fix,
2. Minimal-Mapping-Schema,
3. CL-003 Freeze/Hashes/Tests/Runner prüfen,
4. CL-003 separat autorisieren,
5. CL-003 ausführen,
6. C1–C4 präregistriert auswerten,
7. H1/H2 entscheiden,
8. `RQ-S6-SEM-003` beantworten,
9. Human Review und EVID durchführen,
10. Edition 1.7 und Publication Viewer fortschreiben,
11. aus dem Befund die nächste Forschungsfrage bestimmen,
12. nur den hierfür erforderlichen MHRN-Code ergänzen,
13. nächstes Experiment präregistrieren.

CL-003 darf erst zu Schritt 4 wechseln, wenn sein Freeze den **aktuellen** gebundenen Quellstand reproduzierbar beschreibt.

## 7. Konsequenz für die wissenschaftliche Arbeit

Die wissenschaftliche Arbeit ist nicht die nachträgliche Dokumentation eines bereits gebauten Systems. Sie ist Teil des Steuerungsmechanismus, aus dem das System schrittweise entsteht.

Daraus folgt für MHRN:

- positive Ergebnisse können Architekturentscheidungen stützen;
- negative Ergebnisse können Architekturentscheidungen verhindern oder umlenken;
- inkonklusive Ergebnisse rechtfertigen keine stärkeren Claims;
- exploratorische Beobachtungen erzeugen Fragen, nicht rückwirkende Bestätigungen;
- technische Reife und wissenschaftliche Evidenz bleiben getrennt.
