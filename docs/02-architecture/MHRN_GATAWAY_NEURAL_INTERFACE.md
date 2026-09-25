# MHRN Gateway Neural Interface – konsolidierter Architekturvertrag v0.4

## 1. Ziel und Grundprinzip

Das MHRN Gateway Neural Interface ist keine bloße Datenkonvertierung und kein biologischer Ersatz für einen Computerbus.

Es ist eine:

> **explizite, versionierte und experimentell überprüfbare Transduktionsschicht zwischen exakten digitalen Daten und einer spatio-temporalen neuronalen Repräsentation.**

Die zentrale Trennung lautet:

```text
Payload != Neural Representation
```

und:

```text
Codec != GatewayTopology != GatewayLearning
```

Diese drei Ebenen dürfen weder im Code noch in wissenschaftlichen Experimenten implizit miteinander verschmelzen.

Die exakten digitalen Daten bleiben außerhalb des kanonischen SNN. Das SNN erhält ausschließlich eine explizit deklarierte neuronale Repräsentation.

---

# 2. Fünf Ebenen des Interfaces

```text
DIGITAL WORLD
     │
     ▼
1. Exact Boundary Plane
     │
     ▼
2. Codec Plane
     │
     ▼
3. Neural Projection Plane
     │
     ▼
4. Neural Readout / Decoder Plane
     │
     ▼
5. Exact Output / Tool Plane
```

Im Detail:

```text
BoundaryFrame
     │
     ▼
CodecContract
     │
     ▼
SpikeFrame / SpikeFrameSet
     │
     ▼
GatewayTopology
     │
     ▼
MHRN SNN
     │
     ▼
ReadoutWindow
     │
     ▼
DecodeResult
     │
     ▼
GatewayResponseFrame / Tool / LLM / API / Actuator
```

---

# 3. Exact Boundary Plane

Der bestehende `SymbolFrame` bleibt konzeptionell korrekt:

* exakter Payload;
* Sequenz;
* Provenienz;
* SHA-256;
* Payload außerhalb des SNN.

Er sollte jedoch in einen allgemeineren Boundary-Vertrag eingebettet werden.

## BoundaryFrame

```python
@dataclass(frozen=True, slots=True)
class BoundaryFrame:
    schema_version: int

    frame_id: str
    stream_id: str
    sequence: int

    direction: str
    kind: str

    content_type: str
    schema_id: str | None

    payload: bytes | None
    payload_ref: str | None

    payload_size_bytes: int
    payload_sha256: str

    correlation_id: str | None
    priority: int

    source_id: str
    provenance: str

    arrival_time_ns: int | None
    admitted_tick: int | None
```

## Wichtige Zeittrennung

```text
arrival_time_ns
```

ist externe reale Zeit.

```text
admitted_tick
```

ist kausale MHRN-Zeit.

Beide dürfen nicht gleichgesetzt werden.

Für Replay ist ausschließlich die dokumentierte Tick-Zuweisung kausal relevant.

Große Payloads können content-addressed ausgelagert werden:

```text
payload_ref = sha256:<digest>
```

---

# 4. CodecContract

Der Codec ist ein eigener versionierter Vertrag.

```python
@dataclass(frozen=True, slots=True)
class CodecContract:
    schema_version: int

    codec_id: str
    codec_version: str

    input_kind: str
    output_kind: str
    coding_scheme: str

    population_size: int
    population_layout_ref: str

    window_ticks: int
    refractory_ticks: int

    input_domain: dict
    normalization: dict
    quantization: dict

    encoding_parameters: dict
    decoding_parameters: dict

    determinism_class: str

    rng_algorithm: str | None
    seed_policy: str | None

    vocabulary_ref: str | None

    reconstruction_class: str
    error_metric: str | None
    error_bound: float | None

    max_spikes_per_frame: int
    max_events_per_tick: int

    encoder_id: str
    decoder_id: str

    contract_sha256: str
```

## Reconstruction Classes

Mindestens:

```text
EXACT
BOUNDED_LOSS
APPROXIMATE
IDENTITY_ONLY
NON_INVERTIBLE
```

Ein Codec darf niemals Fähigkeiten behaupten, die seine mathematische Struktur nicht besitzt.

Beispiel:

```text
HashFingerprintCodec
```

muss mindestens sein:

```text
IDENTITY_ONLY
```

oder:

```text
NON_INVERTIBLE
```

und niemals `EXACT`.

---

# 5. Population Layout Contract

`population_layout` darf kein freier String bleiben.

Die Geometrie der Population ist Bestandteil der neuronalen Bedeutung.

## PopulationLayout

```python
@dataclass(frozen=True, slots=True)
class PopulationLayout:
    schema_version: int

    layout_id: str
    layout_version: str

    layout_kind: str

    population_size: int

    logical_neuron_ids: tuple[int, ...]
    neuron_order: tuple[int, ...]

    preferred_values: tuple[float, ...] | None

    coordinates: tuple[tuple[float, ...], ...] | None

    layout_sha256: str
```

Mögliche Layout-Arten:

```text
LINEAR_1D
GRID_2D
GRID_ND
SPARSE
TOPOLOGICAL
DETERMINISTIC_RANDOM
SYMBOLIC
```

Für einen `PopulationLatencyCodec` gehören die bevorzugten Werte:

```text
μ0 ... μN-1
```

explizit zum Layout.

Damit ist eindeutig definiert:

```text
logical neuron
        ↕
layout position
        ↕
preferred value
```

---

# 6. Symbol-Vokabular

`SparseSymbolCodec` und `VSACodec` benötigen ein reproduzierbares Vokabular.

Dieses darf nicht implizit aus einem Python-Dictionary oder einer aktuellen Datei entstehen.

## Vocabulary Contract

```text
vocabulary_ref = sha256:<digest>
```

Das Vokabular wird separat content-addressed gespeichert.

Beispielsweise:

```json
{
  "schema_version": 1,
  "vocabulary_id": "gateway-response-symbols",
  "version": "1.0",
  "symbols": [
    "SUCCESS",
    "FAILURE",
    "CONTINUE",
    "STOP",
    "UNKNOWN"
  ]
}
```

Ändert sich ein Symbol, seine ID oder seine Zuordnung, entsteht:

```text
neuer vocabulary hash
```

und damit:

```text
neuer CodecContract hash
```

Eine stillschweigende Vokabularänderung ist verboten.

---

# 7. Atomarer SpikeFrame

Ein atomarer `SpikeFrame` verwendet:

* genau einen Codec;
* genau eine Source-Population;
* genau ein Population Layout.

```python
@dataclass(frozen=True, slots=True)
class SpikeEvent:
    source_channel: int
    tick_offset: int


@dataclass(frozen=True, slots=True)
class SpikeFrame:
    schema_version: int

    spike_frame_id: str

    source_frame_id: str
    source_frame_sha256: str

    correlation_id: str | None

    codec_id: str
    codec_version: str
    codec_contract_sha256: str

    source_population_id: str
    population_layout_sha256: str

    start_tick: int
    end_tick: int

    events: tuple[SpikeEvent, ...]

    event_count: int
    event_sha256: str

    empty_reason: str | None
```

Normative Event-Reihenfolge:

```text
tick_offset ascending
source_channel ascending
```

---

# 8. Composite Responses: SpikeFrameSet

Ein LLM- oder Tool-Response kann mehrere semantisch unterschiedliche Felder enthalten.

Beispiel:

```text
status
decision
provider_reported_score
category
value
```

Diese dürfen nicht künstlich in einen einzigen Codec gepresst werden.

Deshalb bleibt `SpikeFrame` atomar und es entsteht:

```python
@dataclass(frozen=True, slots=True)
class SpikeFrameSet:
    schema_version: int

    frame_set_id: str

    parent_boundary_frame_id: str
    parent_boundary_sha256: str

    correlation_id: str

    member_frames: tuple[SpikeFrame, ...]

    member_codec_ids: tuple[str, ...]
    member_population_ids: tuple[str, ...]

    composite_event_sha256: str
```

Beispiel:

```text
GatewayResponseFrame
       │
       ├── status
       │     ↓
       │   SparseSymbolCodec
       │     ↓
       │   SpikeFrame A
       │
       ├── decision
       │     ↓
       │   SparseSymbolCodec
       │     ↓
       │   SpikeFrame B
       │
       ├── provider_reported_score
       │     ↓
       │   PopulationLatencyCodec
       │     ↓
       │   SpikeFrame C
       │
       └── value
             ↓
           PopulationLatencyCodec
             ↓
           SpikeFrame D

                ↓
           SpikeFrameSet
```

Damit ist die Verarbeitung zusammengesetzter Daten eindeutig spezifiziert.

---

# 9. Provider Confidence

Ein extern gemeldeter numerischer Wert darf nicht automatisch als statistisch kalibrierte Confidence interpretiert werden.

Deshalb sollte:

```text
provider_confidence
```

durch:

```text
provider_reported_score
```

oder:

```text
provider_self_assessment
```

ersetzt werden.

Nur kalibrierte Werte dürfen explizit als `confidence` bezeichnet werden.

---

# 10. Leere SpikeFrames

Ein SpikeFrame mit:

```text
event_count = 0
```

ist zulässig.

Er darf aber nicht semantisch mehrdeutig sein.

Deshalb:

```text
empty_reason
```

mit beispielsweise:

```text
NO_CHANGE
BELOW_THRESHOLD
SUPPRESSED
NO_SYMBOL
RESOURCE_THROTTLED
```

Ein ungültiger Eingang sollte dagegen grundsätzlich:

```text
kein gültiger SpikeFrame
```

sein.

`INVALID_INPUT` sollte daher vorzugsweise einen Fehlerzustand erzeugen und nicht als normale leere neuronale Nachricht behandelt werden.

---

# 11. Refractory Contract

Der Codec muss das deklarierte Refraktärverhalten einhalten.

Neue Invariante:

```text
I16

No spike event may target the same source_channel
within refractory_ticks of a previous spike event
inside the same causal spike stream.
```

Wichtig ist die Korrektur gegenüber einer reinen Frame-Regel:

Die Refraktärzeit endet nicht notwendigerweise an einer Frame-Grenze.

Daher muss sie gelten über:

```text
konsekutive SpikeFrames derselben Population
```

und nicht nur innerhalb eines einzelnen Frames.

Der Scheduler bzw. Encoder benötigt dafür gegebenenfalls einen reproduzierbaren:

```text
CodecStreamState
```

---

# 12. CodecStreamState

Stateful Codecs wie Delta-Encoding benötigen Zustand zwischen Frames.

Dieser Zustand darf nicht versteckt bleiben.

```python
@dataclass(frozen=True, slots=True)
class CodecStreamState:
    schema_version: int

    stream_id: str
    codec_contract_sha256: str

    last_sequence: int
    last_tick: int

    state_payload: dict

    state_sha256: str
```

Beispiele für State:

```text
DeltaEventCodec:
    previous_reference

Refractory handling:
    last_spike_tick[channel]

Windowed rate decoder:
    previous window state
```

Dieser Zustand muss bei Checkpoint und Replay persistierbar sein.

---

# 13. Frame-Überlappung und Kanalisierung

Mehrere Frames können zeitlich überlappen.

Das muss explizit erlaubt oder verhindert werden.

Für Gateway Interface v1 gilt:

> Eine Population darf gleichzeitig nur einen aktiven Frame derselben logischen Codec-Lane besitzen, sofern der verwendete Codec nicht explizit als multiplexfähig deklariert wurde.

Dafür sollte der Vertrag enthalten:

```text
channel_policy
```

mit beispielsweise:

```text
SERIAL
MULTIPLEXED
DEDICATED_POPULATION
```

Für den ersten PoC:

```text
DEDICATED_POPULATION
```

oder:

```text
SERIAL
```

Dadurch wird verhindert, dass zwei `PopulationLatencyCodec`-Frames dieselben Spikezeiten ununterscheidbar vermischen.

---

# 14. Decoder Contract

```python
@dataclass(frozen=True, slots=True)
class DecodeResult:
    schema_version: int

    decoder_id: str
    decoder_version: str

    source_population_id: str

    source_spike_frame_ids: tuple[str, ...]

    start_tick: int
    end_tick: int

    status: str

    decoded_value: object | None

    reconstruction_class: str
    reconstruction_error: float | None

    ambiguity_score: float | None

    determinism_class: str

    codec_contract_sha256: str
    readout_sha256: str
```

Mögliche Statuswerte:

```text
EXACT
VALID
AMBIGUOUS
INSUFFICIENT_ACTIVITY
OUT_OF_RANGE
INVALID
TIMEOUT
```

Ein Decoder darf bei unzureichenden Daten niemals erfundene Inhalte erzeugen.

---

# 15. Pipeline Determinism

Nicht nur der Encoder, sondern auch Decoder und Scheduling benötigen eine deterministische Klassifikation.

Die Determinismusklasse der vollständigen kausalen Pipeline entspricht der schwächsten Klasse eines kausal beteiligten Bestandteils.

Konzeptionell:

```text
D_pipeline =
    min(
        D_boundary,
        D_scheduler,
        D_encoder,
        D_projection,
        D_snn,
        D_readout,
        D_decoder
    )
```

Die genaue Ordnung richtet sich nach den für MHRN bereits definierten D-Klassen.

Ein Experiment darf niemals eine stärkere Replay-Garantie behaupten als der schwächste beteiligte Abschnitt.

---

# 16. Primärer Codec-Stack

Es gibt keinen universell besten neuronalen Code.

Die Codec-Wahl hängt ab von:

* Signaltyp;
* Aufgabe;
* zeitlicher Struktur;
* Rauschen;
* Latenz;
* Energie;
* Hardware;
* gewünschter Rekonstruktionsgenauigkeit.

Deshalb:

| Datentyp                         | Codec                       |
| -------------------------------- | --------------------------- |
| Skalar                           | `PopulationLatencyCodec-v1` |
| numerischer Vektor               | `VectorPopulationCodec-v1`  |
| kontinuierliches Änderungssignal | `DeltaEventCodec-v1`        |
| Kategorie/Symbol                 | `SparseSymbolCodec-v1`      |
| strukturierte Symbolik           | später `VSACodec-v1`        |
| exakte Bitreferenz               | `BitExactCodec-v1`          |
| Negativkontrolle                 | `HashFingerprintCodec-v0`   |
| klassische Baseline              | `PopulationRateCodec-v1`    |

---

# 17. PopulationLatencyCodec

Für:

```text
x ∈ [xmin, xmax]
```

erhalten Population-Neuronen bevorzugte Werte:

```text
μ0 ... μN-1
```

Aktivierung:

$$
a_i =
\exp
\left(
-\frac{(x-\mu_i)^2}
{2\sigma^2}
\right)
$$

Spike-Latenz:

$$
t_i =
t_0 +
round((1-a_i)(W-1))
$$

Ein Spike entsteht, wenn:

$$
a_i \ge \theta
$$

Dadurch gilt:

```text
ähnlicher Eingang
→ ähnliche aktive Population
→ ähnliche Spikezeiten
```

und nicht:

```text
ähnlicher Eingang
→ völlig unabhängiger Hashcode
```

---

# 18. Numerische Randwerte

Für:

```text
x = xmin
```

oder:

```text
x = xmax
```

muss das Verhalten deterministisch sein.

Der Codec erhält deshalb:

```text
out_of_range_policy
```

mit beispielsweise:

```text
REJECT
CLAMP_EXPLICIT
```

Standard für wissenschaftliche Runs:

```text
REJECT
```

Kein stilles Clipping.

Zusätzlich:

```text
minimum_activity_policy
```

beispielsweise:

```text
NONE
GUARANTEE_ONE_SPIKE
```

Bei:

```text
GUARANTEE_ONE_SPIKE
```

wird deterministisch der maximal aktivierte Rezeptor ausgewählt.

Eine künstliche Veränderung von `a_i` auf `θ + ε` ist nicht nötig; besser ist eine explizite Encoder-Regel:

```text
if no activation passes threshold:
    select argmax(a_i)
```

mit definiertem Tie-Break:

```text
lowest logical neuron id
```

---

# 19. DeltaEventCodec

Für zeitlich kontinuierliche Signale:

```text
if x - reference >= δ:
    emit ON event
    reference += δ

if reference - x >= δ:
    emit OFF event
    reference -= δ
```

Große Signaländerungen können mehrere Events erzeugen.

Beispiel:

```text
reference = 20
input = 24
δ = 1
```

ergibt vier positive Delta-Ereignisse.

Der Codec ist stateful.

Sein Zustand muss deshalb im `CodecStreamState` persistiert werden.

Vorteil:

```text
keine Veränderung
→ keine Ereignisse
```

anstatt künstlich bei jedem Samplingzeitpunkt neuronale Aktivität zu erzeugen.

---

# 20. SparseSymbolCodec

Symbole werden über ein versioniertes, content-addressed Vokabular auf eine stabile sparse Population abgebildet.

Die Zuordnung darf weder von:

```text
Python hash()
```

noch von:

```text
Dictionary iteration order
```

abhängen.

Die Zuordnung muss aus:

```text
vocabulary hash
+
codec version
+
explizitem mapping
```

reproduzierbar sein.

---

# 21. VSA

Vector-Symbolic Architectures werden nicht Teil des Pflichtpfades von Gateway-v1.

Sie werden als eigener experimenteller Codec behandelt:

```text
VSACodec-v1
```

Mögliche spätere Nutzung:

```text
OBJECT ⊗ CAR
+
COLOR ⊗ RED
+
POSITION ⊗ LEFT
```

VSA ist damit eine Option für strukturierte, relationale Symbolik, aber kein Ersatz für numerische oder sensorische Codecs.

---

# 22. HashFingerprintCodec-v0

Die bisherige:

```python
SHA256(payload)
→ digest[index] % 2
```

Abbildung wird nicht als produktiver neuronaler Codec verwendet.

Sie wird bewusst zur Negativkontrolle:

```text
HashFingerprintCodec-v0
```

Eigenschaften:

```text
deterministic = true
invertible = false
semantic_locality = false
numeric_locality = false
similarity_preserving = false
reconstruction_class = IDENTITY_ONLY
```

## Korrektur des >32-Byte-Problems

Die bisherige Implementierung darf nicht über das SHA-256-Digest hinaus indizieren.

Für v0 wird die Definition eingefroren:

```text
digest = SHA256(payload)
```

Die 256 Digest-Bits werden zyklisch **nicht** wiederverwendet.

Daher gilt:

```text
maximum population_size = 256
```

wenn wirklich einzelne Digest-Bits verwendet werden.

Der bisherige Ansatz:

```text
digest[index] % 2
```

nutzt dagegen lediglich ein Paritätsbit pro Digest-Byte und bietet nur 32 Werte.

Dieser historische Modus sollte als:

```text
HashFingerprintLegacyByteParity-v0
```

erhalten werden, falls bestehende Experimente ihn benötigen.

Der neue Negativ-Control sollte stattdessen echte Digest-Bits verwenden:

```text
256 SHA-256 bits
→ max 256 channels
```

Für größere Populationen wird der Codec nicht erweitert, sondern:

```text
fail closed
```

Damit bleibt seine Semantik klar und es entsteht kein versteckter PRNG.

---

# 23. BitExactCodec-v1

Der `BitExactCodec` ist keine effiziente Produktivlösung.

Er ist die obere Referenz für Übertragungsintegrität.

Grundbedingung:

```text
payload
→ encode
→ spikes
→ decode
→ payload'
```

mit:

```text
payload' == payload
```

bitgenau.

Beispielsweise:

```text
0 → ZERO_i population
1 → ONE_i population
```

Die genaue Kodierung muss versioniert werden.

Er dient insbesondere als Referenz für:

```text
RQ-MSBA-E04
```

und für Decoder-/Pipeline-Integritätstests.

---

# 24. LLM- und Tool-Responses

Unstrukturierter Freitext sollte in Gateway-v1 nicht direkt über einen Hash in wenige Neuronen projiziert werden.

Bevorzugt wird eine strukturierte Antwort:

```json
{
  "status": "success",
  "decision": "continue",
  "provider_reported_score": 0.78,
  "category": "object_detected",
  "value": 0.42
}
```

Dann:

```text
status
→ SparseSymbolCodec

decision
→ SparseSymbolCodec

provider_reported_score
→ PopulationLatencyCodec

category
→ SparseSymbolCodec

value
→ PopulationLatencyCodec
```

Freier Text bleibt als exakter Boundary-Payload erhalten.

Eine spätere Language-Interface-Schicht kann gesondert untersucht werden.

---

# 25. Gateway Request ist kein Daten-Codec

Populationen wie:

```text
REQUEST_LLM
REQUEST_MEMORY
REQUEST_VISION
REQUEST_TOOL
```

gehören zur:

```text
Gateway Action Selection
```

und nicht zur Payload-Kodierung.

Der Ablauf bleibt:

```text
SNN
↓
REQUEST population
↓
Gateway Action Selector
↓
BoundaryFrame
↓
external service
↓
GatewayResponseFrame
↓
Codec stack
↓
SpikeFrameSet
↓
response populations
↓
SNN
```

Dadurch bleibt auch das bereits definierte request-spezifische Delayed-Credit-Modell sauber getrennt:

```text
neural activity
↓
request
↓
external latency
↓
response
↓
response consumption
↓
task outcome
↓
request-specific credit
```

---

# 26. Gateway Learning bleibt separate Sidecar-Logik

Gateway Learning und Codec Learning sind zwei verschiedene Forschungsfragen.

Gateway-v1:

```text
encoder learning = OFF
decoder learning = OFF
vocabulary mutation = OFF
layout mutation = OFF
normalization learning = OFF
```

Nur in gesondert preregistrierten Experimenten dürfen aktiviert werden:

```text
GatewayTopology plasticity
Gateway routing adaptation
admission adaptation
request selection learning
```

Auch diese dürfen nicht automatisch den Codec verändern.

---

# 27. Runtime-Abhängigkeiten

`gateway_runtime.py` darf nicht sämtliche Codec-Implementierungen kennen.

Abhängigkeitsrichtung:

```text
gateway_runtime
    ↓
contracts only
```

nicht:

```text
gateway_runtime
    ↓
PopulationLatencyCodec
DeltaCodec
VSACodec
etc.
```

Ein Resolver übernimmt:

```python
codec = codec_resolver.resolve(contract)

spike_frame = codec.encode(
    boundary_frame,
    contract,
    stream_state
)
```

Der Runtime werden anschließend nur die standardisierten Ergebnisse übergeben.

Damit bleibt sie vergleichbar mit einer Backend-Abstraktion:

```text
contract
→ implementation
→ canonical result
```

---

# 28. Empfohlene Modulstruktur

```text
src/embodiment/
│
├── gateway_runtime.py
│
├── gateway_frames.py
│
├── gateway_scheduler.py
│
├── gateway_codec_contracts.py
│
├── gateway_codec_registry.py
│
├── gateway_stream_state.py
│
├── gateway_readout.py
│
├── gateway_codecs/
│   ├── base.py
│   ├── population_latency.py
│   ├── population_rate.py
│   ├── vector_population.py
│   ├── delta_event.py
│   ├── sparse_symbol.py
│   ├── bit_exact.py
│   ├── hash_fingerprint.py
│   └── vsa.py
│
└── msba.py
```

`msba.py` bleibt für:

```text
Modality policy
Projection
Energy/resource accounting
MSBA experiments
```

zuständig.

---

# 29. Interface-weite Versionierung

Einzelne `schema_version`-Felder reichen nicht.

Es wird eine Top-Level-Version eingeführt:

```python
MHRN_GATEWAY_INTERFACE_VERSION = "1.0"
```

Zusätzlich behält jede Struktur ihre eigene Schema-Version.

Beispiel:

```text
Gateway Interface 1.0

BoundaryFrame schema 1
CodecContract schema 1
PopulationLayout schema 1
SpikeFrame schema 1
SpikeFrameSet schema 1
CodecStreamState schema 1
DecodeResult schema 1
```

Breaking Changes an der Gesamtsemantik erhöhen:

```text
MHRN_GATEWAY_INTERFACE_VERSION
```

Ein Reader darf inkompatible Versionen nicht still interpretieren.

---

# 30. RNG Contract

RNG-basierte Codecs stellen ein besonderes Reproduzierbarkeitsproblem dar.

CPU- und CUDA-RNGs liefern nicht automatisch identische Sequenzen.

Für Gateway Interface v1 gilt deshalb:

> Produktive Referenz-Codecs sollen nach Möglichkeit deterministisch ohne RNG arbeiten.

Falls RNG notwendig ist:

```text
rng_algorithm
rng_version
seed
counter/index semantics
```

müssen exakt spezifiziert sein.

Ein einfaches:

```text
seed = 42
```

reicht nicht.

Bis ein plattformübergreifender RNG-Vertrag existiert, dürfen RNG-basierte Codecs entweder:

```text
CPU_REFERENCE_ONLY
```

sein oder nur eine schwächere Determinismusklasse beanspruchen.

---

# 31. CUDA-Grenze

Die Codec-Schicht soll CUDA nicht mit JSON, UTF-8, HTTP oder LLM-Semantik belasten.

CUDA erhält:

```text
source_channel[]
event_tick[]
frame_offset[]
```

bzw. einen kanonisch sortierten Eventbuffer.

Beispiel:

```text
BoundaryFrame
     ↓
CPU / codec boundary
     ↓
SpikeFrame
     ↓
canonical packed event buffer
     ↓
CUDA SNN
```

CUDA muss nichts wissen über:

```text
HTTP
JSON
LLM
CBOR
UTF-8
SymbolFrame
vocabulary files
```

Dies ist die richtige Grenze für Stage CUDA-1.

---

# 32. Invarianten I1–I16+

## I1

Exact payload never enters canonical SNN state.

## I2

SNN activity can never mutate BoundaryFrame payload bytes.

## I3

Every neural representation references its source-frame checksum.

## I4

Every atomic neural representation references exactly one CodecContract.

## I5

Unknown codec or codec version fails closed.

## I6

No silent codec fallback.

## I7

No silent numerical clipping.

## I8

Codec state is independent from GatewayTopology state.

## I9

GatewayTopology state is independent from canonical SNN synapse state.

## I10

Encoder and decoder learning are disabled in Gateway Interface v1.

## I11

Gateway plasticity cannot mutate CodecContract parameters.

## I12

Decoder failure returns UNKNOWN, INVALID or AMBIGUOUS and never fabricated content.

## I13

Same:

```text
BoundaryFrame
+
CodecContract
+
PopulationLayout
+
CodecStreamState
+
seed where applicable
+
tick schedule
```

must reproduce the same `SpikeFrame` within the claimed determinism class.

## I14

Throttling may delay or reject a frame but may never mutate its exact payload.

## I15

Scientific experiments persist:

```text
codec
codec hash
layout
layout hash
vocabulary hash
mapping
seed
BoundaryFrame digest
SpikeFrame digest
decoder digest
```

## I16

No source channel may violate the declared refractory interval across the same causal codec stream.

## I17

Composite information must be represented through explicit `SpikeFrameSet` membership rather than hidden multi-codec semantics in a single SpikeFrame.

## I18

A vocabulary change produces a new content hash and invalidates the old CodecContract identity.

## I19

A PopulationLayout change produces a new layout hash and therefore a new effective neural representation contract.

## I20

A stateful codec must expose and persist all state needed for deterministic continuation.

## I21

An empty SpikeFrame must contain an explicit semantic `empty_reason`.

## I22

Frame multiplexing requires an explicitly declared multiplex-capable contract.

## I23

A pipeline may not claim a stronger determinism class than its weakest causal component.

## I24

Codec-generated neural events may affect the SNN only through declared afferent populations and GatewayTopology mappings.

## I25

Exact digital integrity is evaluated on the BoundaryFrame plane, not inferred from neural similarity.

---

# 33. Forschungsfrage für die Codecs

Nicht:

> Population Coding ist besser.

Sondern:

```text
RQ-GW-CODEC-001
```

> Welches explizit deklarierte neuronale Kodierungsverfahren liefert für eine definierte digitale Aufgabe unter identischem Ressourcenbudget die beste Kombination aus Rekonstruktions- bzw. Task-Leistung, Latenz, Spikezahl, synaptischen Operationen, Energiebedarf, Robustheit und Replay-Stabilität?

Verglichen werden mindestens:

```text
PopulationLatencyCodec
PopulationRateCodec
BitExactCodec
HashFingerprintCodec
```

und für geeignete zeitliche Aufgaben:

```text
DeltaEventCodec
```

sowie später gegebenenfalls:

```text
VSACodec
```

---

# 34. Experimentelle Kontrollen

Mindestens:

```text
structured representation
random mapping
shuffled mapping
hash fingerprint
bit-exact reference
```

Optional:

```text
spike jitter
spike drop
spike duplication
timing shift
population lesion
added background noise
```

Metriken:

```text
task accuracy
reconstruction error
latency
spikes/frame
synaptic events
estimated energy
measured energy where available
noise robustness
replay consistency
decoder ambiguity
```

---

# 35. Gateway-v1 Mindestumfang

Für den ersten implementierbaren PoC:

```text
BoundaryFrame-v1
PopulationLayout-v1
CodecContract-v1
CodecStreamState-v1
SpikeFrame-v1
SpikeFrameSet-v1
DecodeResult-v1
```

Codecs:

```text
PopulationLatencyCodec-v1
PopulationRateCodec-v1
DeltaEventCodec-v1
SparseSymbolCodec-v1
BitExactCodec-v1
HashFingerprintCodec-v0
```

Noch nicht zwingend für PoC:

```text
VectorPopulationCodec
VSACodec
learned encoder
learned decoder
learned vocabulary
adaptive population geometry
```

---

# 36. Drei unmittelbar blockierende Punkte

Vor dem ersten ernsthaften PoC müssen zwingend definiert bzw. implementiert sein:

### 1. Composite Frames

Gelöst durch:

```text
SpikeFrameSet
```

### 2. Population Layout

Gelöst durch:

```text
PopulationLayout
+
layout_sha256
```

### 3. Symbol-Vokabular

Gelöst durch:

```text
content-addressed Vocabulary
+
vocabulary_ref
```

Ohne diese drei Verträge wäre insbesondere eine strukturierte LLM-/Tool-Antwort nicht reproduzierbar spezifiziert.

---

# 37. Weitere Korrekturen vor Stage CUDA-1

Ebenfalls vor einer endgültigen CUDA-Integration festzulegen:

```text
decoder determinism
codec stream state
refractory semantics
frame overlap policy
channel policy
RNG contract
exact hash-control semantics
interface-wide versioning
numeric boundary policy
```

Sie sind teilweise weniger sichtbar als Composite/Layout/Vocabulary, beeinflussen aber direkt Replay und Backend-Parität.

---

# 38. Dokumentationsstruktur

Die bestehende Datei:

```text
MHRN_GATAWAY.md
```

soll in:

```text
MHRN_GATEWAY.md
```

umbenannt werden.

Die Dokumentation sollte anschließend getrennt werden.

## `MHRN_GATEWAY.md`

Enthält:

```text
Gateway Lifecycle
Gateway Action Selection
Request/Response lifecycle
Concurrency
Cancellation
GatewayTopology
Gateway Learning
Tag-and-Capture
Delayed causal credit
RequestEligibilityRecord
GatewayRewardEvent
Plasticity
Safety
```

## `MHRN_GATEWAY_NEURAL_INTERFACE.md`

Enthält:

```text
BoundaryFrame
CodecContract
PopulationLayout
Vocabulary
CodecStreamState
SpikeFrame
SpikeFrameSet
Readout
DecodeResult
Codec stack
Determinism
CUDA boundary
Interface invariants
Codec experiments
```

Damit wird auch dokumentarisch sichtbar:

```text
Tool use / Gateway behaviour
```

ist nicht dasselbe wie:

```text
digital-to-neural representation
```

---

# 39. Verhältnis zu Gateway Learning

Die bereits definierte Gateway-Lernarchitektur bleibt erhalten.

Insbesondere:

```text
RequestEligibilityRecord
TaggedEdge
request-specific eligibility
delayed credit
task-bound attribution
NO_REQUEST
cooldown
pending limits
```

werden nicht durch das Neural Interface ersetzt.

Das neue Interface ergänzt lediglich:

```text
Wie werden exakte digitale Daten
in neuronale Ereignisse übersetzt
und wieder daraus gelesen?
```

Gateway Learning beantwortet dagegen:

```text
Warum wurde ein Gateway gewählt,
und welche beteiligten Synapsen
erhalten später Credit?
```

Diese Forschungsfragen müssen getrennt bleiben.

---

# 40. Verhältnis zu MSBA

MSBA bleibt die modalitätsspezifische Projektions- und Ressourcenebene.

Beispielsweise:

```text
Audio
Vision
Digital
```

können unterschiedliche Feature-Geometrien und Throttle-Strategien besitzen.

Das Neural Interface definiert dagegen die allgemeine formale Grenze:

```text
external exact representation
↔
neural event representation
```

Somit:

```text
Codec
↓
SpikeFrame
↓
MSBA projection
↓
GatewayTopology
↓
SNN
```

und nicht:

```text
Codec == MSBA
```

---

# 41. Gesamtarchitektur

Das vollständige Zielbild lautet:

```text
EXTERNAL SYSTEM
      │
      ▼
BoundaryFrame
exact / immutable
      │
      ▼
Schema validation
      │
      ▼
CodecContract
      │
      ├── PopulationLatency
      ├── PopulationRate
      ├── DeltaEvent
      ├── SparseSymbol
      ├── BitExact
      ├── HashFingerprint
      └── future VSA
      │
      ▼
PopulationLayout
      │
      ▼
CodecStreamState
      │
      ▼
SpikeFrame
      │
      ├─────────────┐
      │             │
      │       additional fields
      │             │
      ▼             ▼
   SpikeFrame   SpikeFrame
      │             │
      └──────┬──────┘
             ▼
        SpikeFrameSet
             │
             ▼
        MSBA projection
             │
             ▼
        GatewayTopology
             │
             ▼
          MHRN SNN
             │
             ▼
        ReadoutWindow
             │
             ▼
          Decoder
             │
             ▼
        DecodeResult
             │
             ▼
      exact gateway logic
             │
             ▼
       TOOL / LLM / API
```

---

# 42. Zentrale wissenschaftliche Aussage

Die Architektur behauptet ausdrücklich **nicht**, einen biologisch korrekten universellen neuronalen Code gefunden zu haben.

Stattdessen behandelt sie neuronale Kodierung als:

> **explizite, versionierte und falsifizierbare Modellentscheidung.**

Population Coding, Temporal Coding, Rate Coding, Delta Encoding, Sparse Symbol Codes und spätere VSA-Verfahren sind experimentelle Alternativen.

Ihre Eignung muss durch kontrollierte Versuche bestimmt werden.

---

# 43. Ergebnis

Mit diesen Ergänzungen ist das Gateway Neural Interface konzeptionell deutlich vollständiger.

Die entscheidenden Korrekturen sind:

```text
kein universell „bester“ Codec

Hash-Fingerprint = Negativkontrolle

BitExact = Integritätsreferenz

Composite Responses = SpikeFrameSet

Population geometry = versionierter PopulationLayout

Symbol semantics = content-addressed Vocabulary

stateful codecs = expliziter CodecStreamState

decoder = eigene Determinismusklassifikation

refractory state = frameübergreifend

keine stille Frame-Überlagerung

kein stilles Clipping

kein stilles Codec-Fallback

provider score != calibrated confidence

Codec implementation != GatewayRuntime

interface-wide versioning

CPU/GPU RNG parity nicht voraussetzen
```

Damit entsteht keine bloße Codec-Bibliothek, sondern eine vollständig auditierbare Kausalkette:

```text
Was kam digital hinein?
↓
Welcher exakte Payload war es?
↓
Welches Schema galt?
↓
Welcher Codec galt?
↓
Welches Vokabular galt?
↓
Welches PopulationLayout galt?
↓
Welcher Codec-Zustand galt?
↓
Welche Spike-Ereignisse entstanden?
↓
Welche Population erhielt sie?
↓
Welche GatewayTopology war aktiv?
↓
Wie reagierte das SNN?
↓
Welche Readout-Aktivität entstand?
↓
Welcher Decoder wurde verwendet?
↓
Was wurde daraus rekonstruiert?
↓
Welche Unsicherheit oder Mehrdeutigkeit bestand?
↓
Welche Determinismusklasse gilt?
↓
Welche Komponente durfte überhaupt lernen?
```

Genau diese Nachvollziehbarkeit sollte der normative Kern des **MHRN Gateway Neural Interface** sein.


# 38. Digitaler Sinn und gemeinsamer neuronaler Query/Response-Raum

## 38.1 Architekturposition

Der digitale Gateway wird nicht als externer Gedächtniskern interpretiert, sondern als zusätzliche sensorische Umweltmodalität. Das bestehende MHRN-SNN bleibt der lernende neuronale Kern.

```text
SNN -> Gateway Action -> exact digital process -> response -> Codec -> SNN
```

Der exakte digitale Inhalt bleibt im Exact Boundary Plane. Nur die deklarierte neuronale Repräsentation tritt in den SNN-Kausalraum ein.

## 38.2 100 x 100 PopulationLayout-Kandidat

Für Experimente darf ein gemeinsames `GRID_2D` mit `100 x 100 = 10_000` logischen Kanälen verwendet werden. Es dient als gemeinsamer Projektions-/Readout-Raum für Query- und Response-Muster.

Normative Grenzen:

- keine Behauptung, dass 10.000 Kanäle 10.000 semantische Dimensionen darstellen;
- keine automatische VSA-/HDC-Eigenschaft;
- keine Faktenspeicherung als Zieldefinition;
- Query und Response müssen trotz gemeinsamem Layout durch `direction`, `correlation_id`, Phase und Provenienz getrennt bleiben;
- semantische bzw. relationale Bindung benötigt einen eigenen Codec- und Testvertrag.

## 38.3 Query als Gateway-Aktion

Das SNN muss keine SQL-, HTTP- oder Prompt-Syntax direkt erzeugen. Die neuronale Ebene wählt eine deklarierte Gateway-Aktion und gegebenenfalls neuronale Argumentpopulationen. Die exakte syntaktische Serialisierung gehört zum Tool-/Boundary-Plane.

Damit bleibt die Forschungsfrage präzise: **lernt das SNN die Auswahl und Nutzung eines Informationskanals?** Nicht: kann es ohne Transduktionsschicht ein externes Protokoll byteweise sprechen?

## 38.4 Query-Kontext / funktionale Efferenzkopie

Das ausgehende Query-Muster darf in einem getrennten internen Zustand bis zur Response erhalten werden. Dadurch können erwartete und tatsächliche Rückmeldung verglichen sowie Prediction Error und delayed credit assignment untersucht werden.

Die Bezeichnung `efference-copy-artig` beschreibt ausschließlich die funktionale Schleifenstruktur und keine biologische Homologie.

## 38.5 Lifecycle-Gating

Mindestens folgende Phasen sind für den experimentellen Vertrag zulässig:

```text
IDLE
QUERY
WAIT
RESPONSE
TIMEOUT
```

Das Phase-Gate verhindert, dass ein Netz sein eigenes Query-Muster im gemeinsamen Layout als externe Antwort klassifiziert. Ob die Übergänge fest, teilweise gelernt oder vollständig gelernt werden, ist eine unabhängige Variable.

## 38.6 Forschungsabbildung

- Quellentransfer -> `RQ-GW-004`;
- Modalitätsrouting -> `RQ-GW-002`;
- gelernter bidirektionaler Query/Response-Kreis -> `RQ-GW-006`;
- Codec/Binding -> `RQ-GW-CODEC-001 / H-GW-CODEC-001-A` (kanonisch registriert; noch kein eingefrorenes Protokoll, keine DATA/EVID).

Details und Claim-Grenzen:
`research/decisions/2026-09-25_digital-sense-neural-interface.md`.
