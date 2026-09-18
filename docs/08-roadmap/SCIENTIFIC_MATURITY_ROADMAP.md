# MHRN Scientific Maturity Roadmap

**Stand:** 18. September 2026  
**Geltung:** Ergänzung zur technischen `ROADMAP.md`  
**Maschinenlesbarer Vertrag:** `src/dashboard/static/scientific-progress.json`

## Zweck

Die technische Roadmap beantwortet, welche Mechanismen und Systemverträge implementiert, integriert und verifiziert werden. Diese wissenschaftliche Roadmap beantwortet getrennt davon, welche Behauptungen durch Forschungsfragen, Protokolle, DATA, menschlich geprüfte EVID, unabhängige Replikation und Attribution getragen werden.

Eine Stufe kann technisch abgeschlossen sein und wissenschaftlich offen bleiben. Negativbefunde, engere Claim-Grenzen oder eine unabhängige Replikation können wissenschaftlichen Fortschritt erzeugen, ohne eine neue Produktfunktion hinzuzufügen.

## Akzeptanzmodell je Stufe

1. **RQ/Hypothese:** falsifizierbare, registrierte Aussage mit Alternativerklärung.
2. **Protokoll:** eingefrorene Intervention, Kontrollen, primärer Endpunkt, Seeds, Ausschluss-/Abbruchregeln.
3. **DATA:** quellengebundene Ausführung, Rohdaten, Receipts/Digests und vollständige Bedingungsabdeckung.
4. **EVID:** explizite menschliche Review-/Promotion-Entscheidung für einen konkreten Claim.
5. **Replikation:** hinreichend unabhängige Wiederholung der entscheidenden Aussage.
6. **Attribution:** nachvollziehbare Literatur-, Code-, Daten-, Abbildungs- und Eigenversionsprovenienz.

## Stage 0 – Einzelne Nervenzelle

**Ziel:** numerischen Modellvertrag gegen eine externe Referenzimplementierung und vorab definierte Ereignis-/Toleranzkriterien prüfen.

**Aktueller Gesamt-Scientific-Maturity-Score:** **82,5 %** nach dem kanonischen Gewichtungsvertrag in `scientific-progress.json`.

Erfüllt:
- `RQ-EVAL-006` und `H-EVAL-006-A/B/C` sind explizit registriert;
- `PREREG-EVAL-006-V2` wurde vor der konfirmatorischen Ausführung eingefroren;
- disjunkte Confirmatory-Seeds `21001–21003` wurden gegen Brian2 2.10.1 ausgeführt;
- alle eingefrorenen Primärendpunkte für Izhikevich-2003 und `lif-current-v1` bestanden innerhalb der deklarierten Toleranzen;
- der historische freie 1000-Tick-Izhikevich-Negativbefund bleibt unverändert erhalten;
- Modell-, Quellen- und Literaturattribution sind dokumentiert.

Separat gilt der **scoped Stage-0 research-readiness contract = 100 %**. Dieser engere Readiness-Wert bedeutet nur, dass die dort definierten technischen und methodischen Voraussetzungen erfüllt sind; er ist nicht identisch mit der Gesamt-Scientific-Maturity.

Offen:
- Human Review des eng definierten Konformitätsclaims ist am 18. September 2026 abgeschlossen und unterstützt den scoped Claim;
- die kanonische EVID-Promotion bleibt dennoch blockiert, weil der historische Lauf noch kein EvidenceEngine-kompatibles `manifest.json` mit `validity`, `git.dirty=false`, `provenance_digests` und `source_freeze_sha` besitzt; diese historischen Provenienzwerte werden nicht rückwirkend erfunden;
- deshalb ist vor EVID ein separat versionierter promotion-eligible Replikationslauf unter dem heutigen Provenienzvertrag erforderlich;
- unabhängig autorisierte Replikation außerhalb derselben Autoren-/Toolkette;
- keine biologische Gleichwertigkeit, universelle Langzeittrajektorienidentität oder Generalisierung auf ungeprüfte Modelle/Parameter aus dem Brian2-Vergleich ableiten.

## Stage 1 – Kleines SNN

**Ziel:** Netzwerkmechanismen über task-basierte Interventionen statt nur Konnektivitäts-/Propagationstests untersuchen.

Offen:
- task-basierte RQ,
- feed-forward/recurrent bzw. topology-destroyed Kontrollen,
- unabhängige Replikation.

## Stage 2 – Stabiles rekurrentes SNN

**Ziel:** funktionalen Beitrag von Rekurrenz von bloßer numerischer Stabilität trennen.

Offen:
- rekurrent vs. feed-forward/yoked/information-destroyed bei gleichem Budget,
- held-out zeitliche Aufgaben,
- unabhängige Replikation der relevanten Rekurrenz-Claims.

## Stage 3 – Plastisches Nervengewebe

**Ziel:** kausalen Lernbeitrag von STDP/Drei-Faktor-Lernen, Homöostase und Strukturplastizität belegen.

Offen:
- Learning-on/off, Sham und zerstörte Information präregistriert vergleichen,
- held-out Generalisierung und Retention statt nur Gewichtsänderung messen,
- Regler-/Mechanismusbeiträge separat abladieren,
- menschliche EVID-Promotion und unabhängige Replikation.

## Stage 4 – Spezialisierte neuronale Areale

**Ziel:** modality-spezifische Verarbeitung und Gateway-Lernen kausal von Codec/Adapter-/Budgeteffekten trennen.

Offen:
- E01–E05 unabhängig reviewen,
- Frozen/Random/Shuffle-Kontrollen vollständig auswerten,
- dynamisch materialisierte Skalierung als separaten Benchmark behandeln,
- keine aggregierte Topologiebudget-Zahl als ausgeführte Netzdynamik ausgeben.

## Stage 5 – Integriertes künstliches Nervensystem

**Ziel:** geschlossene sensorimotorische Rückkopplung gegen Replay/Open-loop und wirkungslose Aktorik abgrenzen.

Offen:
- matched disturbance,
- yoked replay,
- interrupted feedback,
- ineffective-actuator controls,
- reale Adapter ausschließlich in separaten safety-gated Studien.

## Stage 6 – Gedächtnis und Weltmodell

**Ziel:** Infrastruktur in explizite kognitive Mechanismen überführen.

### 6A Semantization

- episodische Akquisition,
- Replay/Konsolidierung,
- semantische Repräsentationsänderung,
- Replay-off, shuffled-replay und matched-compute Kontrollen,
- Retention und Generalisierung auf gehaltenen Episoden.

### 6B Predictive Coding

- neuronalen Träger für Vorhersage und Fehler definieren,
- bottom-up/top-down Beiträge kausal trennen,
- Pathway-/Delay-/Feedback-Ablationen,
- externe Prädiktoren und reine Telemetrie als Alternativerklärung ausschließen.

### 6C World Model

- mehrschrittige Vorhersage,
- aktionskonditionierte Dynamik,
- held-out Sequenzen,
- Unsicherheit/Kalibrierung,
- Verhaltens-/Planungsvorteil gegenüber reaktiven Baselines,
- World-model-off bzw. corrupted-model Kontrolle.

### 6D Persistenz

- gekoppelte Gedächtnis-/Predictor-/adaptive Zustände in den kanonischen Checkpoint-Vertrag aufnehmen,
- Pause/Resume/Restart-Identität prüfen.

## Stage 7 – Selbstmodell und verkörperte Identität

**Ziel:** kausale self/other Attribution statt Profil-/Identitätsetiketten.

Offen:
- eigene vs. externe/yoked Aktionsursachen,
- Vorhersage eigener Sensorfolgen,
- observer-only Auswertung,
- LLM-Selbstaussagen ausdrücklich nicht als SNN-Evidenz verwenden.

## Stage 8 – Autonome lebenslange Entwicklung

**Ziel:** Continual Learning in einem fortlaufend weitertrainierten gemeinsamen System.

Offen:
- kein Learned-State-Reset zwischen Aufgaben,
- Retention/Transfer/Interferenz,
- Replay-/Consolidation-Ablationen,
- resource-matched Baselines,
- Rollback-/Safety-Grenzen,
- unabhängige Replikation.

## Stage 9 – Hochintegrierte künstliche Kognition

**Ziel:** einzelne operationale Mechanismen erst isoliert, anschließend integriert testen.

Offen:
- Attention,
- Planning,
- Motivation/Drives,
- Langzeitgedächtnis,
- multimodale Integration,
- Konsolidierung,
- matched-budget Ablationen und externe Replikation.

## Stage 10 – Bewusstseinsforschung

**Ziel:** ausschließlich theorievergleichende, ethisch kontrollierte Forschung.

Mindestbedingungen vor stärkerer Interpretation:
- mehrere kontrastierende Theorien,
- vorab definierte diskriminierende Vorhersagen,
- kausale Interventionen,
- externe Ethik-/Stop-Governance,
- unabhängige adversariale Replikation.

Kein Stage-Score etabliert Bewusstsein, Sentienz, Leidensfähigkeit oder moralischen Status.

## Release-Regel

Jede Release-Beschreibung soll künftig mindestens enthalten:

- technische Änderung,
- wissenschaftliche Änderung,
- neue/geschlossene RQ oder Hypothese,
- neue DATA/EVID und deren Autorität,
- Negativbefunde,
- offene Mechanismus-/Replikationslücken,
- neue oder geänderte Related-Work-/Attributionsbezüge.
