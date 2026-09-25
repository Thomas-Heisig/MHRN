# Digitaler Sinn als neuronales Interface — Integrationsentscheidung 2026-09-25

**Status:** architecture/research integration decision  
**Evidenzrolle:** keine DATA, keine EVID  
**Geltung:** Gesamtarbeit / Stage 4–6 / Gateway / Neural Symbiosis

## Entscheidung

Das bestehende MHRN-Kernmodell wird durch den digitalen Informationszugriff **nicht** durch ein zweites kognitives System ersetzt. Digitale Daten- und Informationsquellen werden als zusätzliche Umwelt-/Sinnesmodalität behandelt.

Der kanonische Pfad lautet:

```text
MHRN activity
  -> learned/selected gateway action
  -> exact boundary/tool plane
  -> external digital process
  -> exact response boundary
  -> declared codec
  -> spike representation
  -> MHRN activity
```

Die exakte Payload bleibt außerhalb des kanonischen SNN. Die neuronale Repräsentation ist der wahrnehmbare Zustand; der externe Inhalt ist nicht automatisch neuronales Gedächtnis.

## Keine Stage-Verschiebung

Die 11 Stages bleiben unverändert.

- **Stage 4:** Digital ist neben Audio und Vision eine sensorische Modalität mit eigenem Codec-/Routingvertrag.
- **Stage 5:** Abfrage und Antwort werden als geschlossener Wahrnehmungs-Handlungs-Kreis behandelt.
- **Stage 6:** internes Working/Episodic Memory, Prediction Error und World-Model-Mechanismen bleiben eigenständige Forschungsobjekte. Externe Inhaltsquellen ersetzen diese Mechanismen nicht, müssen aber auch nicht als dauerhafter Faktenspeicher in Synapsen repliziert werden.

Damit wird Stage 6 nicht in eine Datenbank-Schicht umdefiniert.

## Gemeinsamer neuronaler Interface-Raum

Ein `100 x 100`-Array wird als **experimenteller PopulationLayout-Kandidat** mit 10.000 logischen Kanälen aufgenommen, nicht als universeller Codec und nicht als bewiesene semantische Repräsentation.

Zulässige Interpretation:

```text
100 x 100 GRID_2D
= gemeinsamer neuronaler Projektions-/Readout-Raum
= experimentelles Interface-Substrat
!= 10.000 gespeicherte Fakten
!= bewiesenes VSA
!= bewiesene symbolische Semantik
```

Abfrage- und Antwortmuster dürfen denselben Layout-Raum verwenden, müssen aber durch Richtung, correlation_id, Phase und Provenienz unterscheidbar bleiben.

## Query als Handlung

Eine digitale Abfrage ist semantisch eine **Aktion** des Systems, nicht bloß ein passiver Datenimport.

Die Query-Selektion gehört zur bestehenden Gateway Action Selection; Syntax, Tool/API-Aufruf und exakte Payload-Ausführung bleiben im Boundary/Tool Plane. Das SNN muss daher nicht SQL, HTTP oder LLM-Promptsyntax bitweise erzeugen. Wissenschaftlich relevant ist, ob es den passenden Aktions-/Argumentraum lernbar auswählt.

## Efference-copy-artiger Kontext

Für kontrollierte Experimente darf das ausgehende Query-Muster als intern verfügbarer kausaler Kontext erhalten bleiben, damit erwartete und tatsächliche Rückmeldung getrennt analysiert werden können.

Dies ist eine **funktionale Analogie**, keine Behauptung biologischer Gleichwertigkeit mit Corollary Discharge oder motorischer Efferenzkopie.

## Lifecycle / Phase Gating

Ein experimenteller Lifecycle-Mechanismus darf Query-, Wait-, Response- und Timeout-Phasen explizit trennen. Seine Aufgaben sind:

- Selbst-/Antwort-Verwechslung im gemeinsamen Repräsentationsraum verhindern;
- Antwortlatenz und Timeout kausal binden;
- verspätete oder fehlende Antworten kennzeichnen;
- delayed credit assignment für Eligibility-/Reward-Experimente messbar machen.

Ob dieses Gating fest verdrahtet oder erlernt werden muss, ist selbst eine Versuchsvariable und darf nicht vorab als emergente Fähigkeit behauptet werden.

## Offene Kernprobleme

1. **Codec/Binding:** Strukturierte Relationen dürfen nicht stillschweigend vom klassischen Encoder gelöst werden.
2. **Decoder-Grenze:** Exakte Tool-/API-Syntax bleibt konventionelle Boundary-Funktion; gelernt werden Auswahl, Routing, Parameterpopulation und Nutzung, sofern ein Experiment dies zeigt.
3. **Delayed Credit Assignment:** externe Antwortlatenz muss mit Eligibility-/Reward-Mechanismen kontrolliert geprüft werden.
4. **Autoassoziative Verwechslung:** Query und Response im gleichen PopulationLayout benötigen explizite Richtung/Phase/correlation_id.
5. **Nutzenfrage:** neuronale Ausführung ist nur gerechtfertigt, wenn sie gegen einfachere nicht-neuronale oder fest geroutete Baselines einen messbaren Nutzen zeigt.

## Kanonische Falsifikationstests

### A — Quellentransfer

**Mapping:** `RQ-GW-004`

Entwicklung mit Quelle A; Test mit Quelle B bei gleichem Interface-Schema und neuen Inhalten.

Der Test trägt nur dann eine Transferaussage, wenn Leistung auf B gegenüber geeigneten Baselines erhalten bleibt und die Testinhalte nicht Teil des Lernkorpus waren.

### B — Abfrage als gelernte Handlung

**Mapping:** `RQ-GW-006`

Das Netz erhält Situationen, in denen zusätzliche digitale Information unterschiedlich nützlich ist. Query-Zeitpunkt und/oder Query-Kanal dürfen nicht vollständig fest vorgegeben sein.

Der Test scheitert hinsichtlich gelerntem Werkzeuggebrauch, wenn der relevante Query-Pfad nur durch harte Ablaufsteuerung ausgelöst wird.

### C — Modalitätsrouting

**Mapping:** `RQ-GW-002`

Audio, Vision und Digital liefern unterschiedlich informative Signale. Gematchte Frozen-, Random-/Shuffle- und lernbare Routingbedingungen prüfen, ob das Netz den für die Aufgabe nützlichen Sinn bevorzugt.

Fest verdrahtetes Routing zählt nicht als Selbstorganisation.

### D — Binding/Codec

**Mapping:** `RQ-GW-CODEC-001 / H-GW-CODEC-001-A` (kanonisch registriert, `open` / `untested`)

Strukturierte Werte/Relationen müssen unter definiertem Codec decodierbar bleiben. Ein möglicher 100x100-/VSA-Pfad ist experimentell und darf erst nach eigener Präregistrierung als funktionale Bindungsrepräsentation gelten.

## Claim-Grenze

Die Integration erlaubt derzeit die Aussage:

> MHRN besitzt einen expliziten Architekturpfad, digitale Informationsquellen als zusätzliche sensorische Umweltmodalität in einen geschlossenen neuronalen Wahrnehmungs-/Handlungskreis einzubinden.

Nicht zulässig sind derzeit:

- "MHRN hat gelernt, das Internet/eine Datenbank/ein LLM autonom zu benutzen";
- "das 100x100-Array versteht Formeln oder Code";
- "digitale Query/Response ist biologisch identisch zu motorischer Efferenzkopie";
- "externes Wissen macht internes Gedächtnis vollständig überflüssig";
- "der digitale Sinn ist RAG überlegen";
- "die Interface-Architektur beweist allgemeine Intelligenz".

Diese stärkeren Aussagen benötigen die oben definierten kontrollierten Experimente.


## Publikationssynchronisation

Die Edition-1.8-Projektion wurde nach dieser Integrationsentscheidung deterministisch neu erzeugt. `MANUSCRIPT.md`, Publikationsregister und Manifest sind damit aus denselben kanonischen Parts abgeleitet. Diese Synchronisation erzeugt keine neue DATA oder EVID.
