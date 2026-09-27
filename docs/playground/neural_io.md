# MHRN Playground — Input, Output und Neural I/O Interface

**Status:** PLAYGROUND_NEURAL_IO · explorativ · nicht kanonisch · keine DATA · keine EVID

Diese Seite dokumentiert die Playground-Referenzimplementierung des bereits
postulierten **MHRN Gateway Neural Interface**. Sie erfindet keinen zweiten
I/O-Vertrag, sondern bildet die vorhandene Architektur in einer isolierten,
begrenzten Playground-Form ab.

## 1. Grundprinzip

Die zentrale Grenze lautet:

```text
Payload != Neural Representation
```

und zusätzlich:

```text
Codec != GatewayTopology != GatewayLearning
```

Exakte Nutzdaten bleiben außerhalb des SNN. Das SNN erhält nur eine explizit
kodierte neuronale Repräsentation.

## 2. Datenfluss

```text
EXACT INPUT / DIGITAL OR SENSOR WORLD
        │
        ▼
BoundaryFrame
        │
        ▼
CodecContract
        │
        ▼
SpikeFrame
        │
        ▼
AFFERENT / GATEWAY_AFFERENT population
        │
        ▼
Playground SNN
        │
        ▼
EFFERENT / GATEWAY_EFFERENT population
        │
        ▼
Readout / DecodeResult
        │
        ▼
PLAYGROUND OUTPUT
```

Die produktive Tool-/Actuator-Ebene ist im Playground absichtlich deaktiviert.

```text
tool_plane_execution = false
actuator_execution   = false
```

## 3. Verhältnis zu bestehenden MHRN-Verträgen

### SymbolFrame

Der bestehende `src.embodiment.msba.SymbolFrame` hält den exakten digitalen
Payload und seinen SHA-256-Hash außerhalb des SNN.

Die Playground-`BoundaryFrame` kapselt diesen Vertrag und ergänzt:

- Frame-ID
- Stream-ID
- Sequenz
- Richtung
- Kind / Modalität
- Content-Type
- `correlation_id`
- Provenienz
- `admitted_tick`

Der Rohpayload wird **nicht** in das Session-Ergebnis oder die persistierte
Playground-Session geschrieben.

### SensorFrame

`SensorFrame` bleibt der allgemeine Embodiment-Sensorvertrag. Ein späterer
Sensorpfad kann einen SensorFrame in einen BoundaryFrame überführen. Der
Playground-Builder verwendet zunächst einen direkten Boundary-Input, damit der
Codec separat getestet werden kann.

### ActionCommand

`ActionCommand` bleibt der autorisierte Embodiment-Ausgangsvertrag.
Der Playground erzeugt **keinen** ActionCommand und führt keine Aktion aus.
Er endet bei `DecodeResult`.

### NetworkAreaAdapter

Der Playground enthält `PlaygroundIOAreaAdapter`, der den vorhandenen
`NetworkAreaAdapter`-Protocol erfüllt. Dieser Adapter darf Payloads
vorverarbeiten, hat aber keinen direkten Zugriff auf den MHRN-Core.

Die neuronale Kodierung bleibt davon getrennt.

## 4. Neuronale Rollen

Das Interface verwendet die bereits postulierten orthogonalen Rollen:

```text
ASSOCIATIVE
AFFERENT
EFFERENT
GATEWAY_AFFERENT
GATEWAY_EFFERENT
```

Im Playground werden dedizierte Populationen reserviert:

- die ersten N Kanäle: Input/Afferent
- die letzten M Kanäle: Output/Efferent
- der mittlere Bereich: Associative/Core

Input und Output dürfen sich nicht überlappen.

## 5. Input Plane

Aktuell verfügbare Referenzcodecs:

### population_latency_v1

Für einen normierten Skalar `x ∈ [0,1]`.

Jeder Kanal hat einen bevorzugten Wert. Aktivierung wird in Spike-Latenz
übersetzt.

Reconstruction Class:

```text
BOUNDED_LOSS
```

### vector_population_v1

Ein normierter numerischer JSON-Vektor wird kanalweise als Latenzereignis
kodiert.

Reconstruction Class:

```text
BOUNDED_LOSS
```

### sparse_symbol_v1

Ein Symbol aus einem festen Playground-Vokabular wird deterministisch auf einen
dedizierten Kanal projiziert.

Das Vokabular enthält zunächst unter anderem:

- QUERY
- RESPONSE
- SUCCESS
- FAILURE
- CONTINUE
- STOP
- UNKNOWN
- REQUEST_TOOL
- REQUEST_MEMORY
- REQUEST_VISION
- REQUEST_LLM

Reconstruction Class:

```text
IDENTITY_ONLY
```

### Noch nicht produktiv implementiert

`BitExactCodec-v1` bleibt als obere Integritätsreferenz geplant.

`HashFingerprintCodec-v0` bleibt eine Negativkontrolle und wird nicht als
produktiver neuronaler Codec angeboten.

## 6. SpikeFrame

Ein SpikeFrame besitzt genau:

- einen Codec,
- eine Source-Population,
- ein PopulationLayout,
- einen kausalen Tick-Bereich.

Events werden normativ sortiert:

```text
tick_offset ascending
source_channel ascending
```

Ein leerer Frame ist zulässig, trägt aber einen expliziten `empty_reason`.

## 7. Output Plane

Der Output liest ausschließlich die dedizierte EFFERENT- oder
GATEWAY_EFFERENT-Population.

Aktuell verfügbare Decoder:

### population_rate_v1

Erzeugt einen Ratenvektor aus den Output-Spikecounts.

Bei fehlender Aktivität:

```text
status = INSUFFICIENT_ACTIVITY
decoded_value = null
```

Es wird kein Inhalt erfunden.

### sparse_symbol_v1

Wählt genau dann ein Symbol, wenn ein eindeutiger Gewinnerkanal vorhanden ist.

Mögliche Status:

```text
VALID
AMBIGUOUS
INSUFFICIENT_ACTIVITY
```

## 8. Query/Response Lifecycle

Der postulierte Lifecycle ist explizit implementiert:

```text
QUERY
  ↓
WAIT
  ↓
RESPONSE
```

oder:

```text
QUERY
  ↓
WAIT
  ↓
TIMEOUT
```

Query und Response werden über folgende Felder auseinandergehalten:

- Richtung
- Phase
- `correlation_id`
- Provenienz

Damit kann derselbe logische Layout-Raum verwendet werden, ohne Query und
Response semantisch zu vermischen.


### 8.1 Implementierungsgrenze des Lifecycles

Der Playground implementiert derzeit nur die **Referenz-State-Machine**.

```text
lifecycle_status = REFERENCE_STATE_MACHINE_ONLY
gateway_action_selection_status = NOT_IMPLEMENTED
external_round_trip_status = NOT_IMPLEMENTED
```

Ein `RESPONSE`-Übergang im aktuellen Playground bedeutet nur, dass nach der
Wait-Grenze Aktivität in der dedizierten Egress-Population beobachtet wurde.
Er ist **kein** Beleg für eine tatsächlich ausgeführte externe Query und
**kein** empfangener `GatewayResponseFrame`.

Der produktive Vertrag bleibt separat:

```text
SNN request population
-> Gateway Action Selector
-> external BoundaryFrame
-> external service
-> GatewayResponseFrame
-> codec
-> afferent response population
```

Dieser externe Roundtrip wird im Playground absichtlich nicht ausgeführt.

## 9. correlation_id

Jeder I/O-Zyklus besitzt eine `correlation_id`.

Wenn keine ID vorgegeben wird, erzeugt der Playground deterministisch eine ID
aus:

- Seed
- Payload-Hash
- Interface-Kontext

Der exakte Payload selbst wird hierfür nicht veröffentlicht.

## 10. 100 × 100 Shared Layout

Die postulierte gemeinsame logische Query-/Response-Fläche:

```text
100 × 100
= 10.000 logische Kanäle
```

ist im Interface-Metadatenvertrag dokumentiert, aber im aktuellen Playground
**nicht physisch allokiert**.

Grund:

Der Playground ist derzeit auf 1.024 Neuronen begrenzt.

Status:

```text
EXPERIMENTAL_CONCEPT_NOT_ALLOCATED_IN_PLAYGROUND
```

Das verhindert, dass eine Architekturidee fälschlich als bereits skalierte
Implementierung ausgegeben wird.

## 11. Learning Boundary

Gateway-v1 im Playground hält standardmäßig aus:

```text
encoder_learning       = false
decoder_learning       = false
vocabulary_mutation    = false
layout_mutation        = false
gateway_learning       = false
```

Codec-Learning, Routing-Learning und Gateway-Plastizität bleiben getrennte
Forschungsfragen.

## 12. Dashboard

Der Playground besitzt einen eigenen Bereich:

```text
07 · Neural I/O Interface
```

Dort können gewählt werden:

- Input Codec
- Input Payload
- Input-Kanäle
- AFFERENT/GATEWAY_AFFERENT
- Output Decoder
- Output-Kanäle
- EFFERENT/GATEWAY_EFFERENT
- Codec-Fenster
- Input-Strom
- Lifecycle-Phase
- Modalität
- Source ID

Das Ergebnis erscheint separat unter:

```text
result["neural_io"]
```

## 13. Ergebnisstruktur

```text
result["neural_io"]
├── classification
├── exact_boundary
│   ├── payload_sha256
│   ├── payload_size_bytes
│   └── raw_payload_persisted = false
├── input
│   ├── role
│   ├── layout
│   ├── codec_contract
│   └── spike_frame
├── output
│   ├── role
│   ├── layout
│   ├── spike_counts
│   └── decode_result
├── roles
├── lifecycle
├── learning
└── promotion_path
```

## 14. Wissenschaftliche Grenze

Diese Implementierung zeigt:

- dass der postulierte I/O-Vertrag im Playground ausführbar abgebildet werden
  kann,
- dass exakte Payloads von neuronalen Repräsentationen getrennt werden können,
- dass Afferent/Efferent-Rollen explizit reserviert werden können,
- dass Query/Response-Lifecycle und Provenienz sichtbar bleiben.

Sie zeigt **nicht**:

- dass ein bestimmter Codec optimal ist,
- dass das SNN externe Semantik versteht,
- dass Query-Selektion gelernt wurde,
- dass Gateway-Lernen funktioniert,
- dass ein 100×100-Layout skaliert,
- dass dekodierte Ausgaben korrekt oder nützlich sind.

Solche Aussagen benötigen eigene kanonische Experimente.

## 15. Verhältnis zu PAN

PAN-State `Ds`, Geometrie `Dg` und Neural I/O sind drei getrennte Ebenen:

```text
Exact / Sensor Input
       │
       ▼
Neural I/O Gateway
       │
       ▼
SNN + optional PAN state Ds
       │
       ├── optional geometry Dg
       │
       ▼
Neural I/O Readout
       │
       ▼
Decoded Playground Output
```

Keine der Ebenen darf implizit als Beweis für eine andere Ebene verwendet
werden.

## 16. Übergang in Forschung

Wie für PAN insgesamt gilt:

```text
Playground observation
→ Research Candidate
→ neue Hypothese
→ Preregistration
→ Freeze
→ neuer canonical DATA run
→ Human Review
→ optional EVID
```
