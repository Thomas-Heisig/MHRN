# MHRN CUDA Architecture

## Stage CUDA-0 Final Contract Addendum v0.3

**Status:** Architekturentwurf vor Repo-Integration.
**Keine CUDA-Implementierung. Keine Änderung wissenschaftlicher DATA/EVID.**

Dieses Addendum schließt die verbliebenen State-, Determinismus- und Boundary-Verträge vor Beginn von Stage CUDA-1.

---

# 1. Neue Grundinvariante: fünf getrennte Ordnungen

Die bisherige Unterscheidung von vier Ordnungen wird um die Synapsenidentität ergänzt.

MHRN unterscheidet künftig konzeptionell:

```text
1. logical neuron identity
2. physical neuron placement
3. logical edge identity
4. numeric reduction order
5. execution scheduling order
```

Diese Ebenen dürfen sich nicht gegenseitig definieren.

Insbesondere gilt:

```text
logical_neuron_id != physical_slot

edge_id != CSR position

reduction order != scheduling order
```

Eine Speicherkompaktierung oder Änderung des CUDA-Schedules darf daher weder eine Neuron- noch eine Synapsenidentität verändern.

---

# 2. Connection Identity Contract

## 2.1 Problem

Eine Verbindung benötigt für CUDA eine Identität, die folgende Operationen überlebt:

```text
CSR rebuild
structural compaction
physical neuron relocation
checkpoint
snapshot reload
GPU repacking
```

`source_id + target_id` reicht hierfür nicht allgemein aus.

Insbesondere müssen mehrere Verbindungen zwischen denselben Neuronen eindeutig darstellbar bleiben.

---

# 3. Stabile `edge_id`

Jede kanonische Synapse erhält langfristig eine:

```text
edge_id: uint64
```

mit folgenden Invarianten:

```text
edge_id ist innerhalb einer Network-Lineage eindeutig

edge_id ändert sich bei CSR-Rebuild nicht

edge_id hängt nicht von CSR-Position ab

edge_id hängt nicht von physical_slot ab

gelöschte edge_id wird innerhalb derselben Lineage nicht wiederverwendet

eine neu erzeugte Verbindung erhält immer eine neue edge_id
```

Beispiel:

```text
A -> B   edge_id = 1042
A -> B   edge_id = 1179
```

sind zwei unterschiedliche Synapsen.

---

# 4. Edge-ID-Lifecycle

Die Runtime besitzt konzeptionell:

```text
next_edge_id
```

Neue Verbindung:

```text
edge_id = next_edge_id
next_edge_id += 1
```

Pruning:

```text
edge_id 1042
    ↓
tombstone / structural journal
```

Spätere Neuanlage derselben Verbindung:

```text
A -> B
edge_id = 1308
```

nicht erneut `1042`.

---

# 5. Migration bestehender Netze

Bestehende Snapshots besitzen noch keine `edge_id`.

Die erste Migration muss deshalb deterministisch und versioniert erfolgen.

Beispielsweise:

```text
edge_identity_migration = "edge-id-v1"
```

Die Zuweisung erfolgt einmal aus einer kanonisch definierten Reihenfolge des vorhandenen serialisierten Netzwerks.

Danach werden die IDs persistiert.

Wichtig:

> Nach erfolgter Migration darf `edge_id` niemals erneut aus der aktuellen Array- oder CSR-Position abgeleitet werden.

Die Migration selbst gehört in die Provenienz.

---

# 6. Canonical Incoming CSR

Innerhalb jedes Targets gilt ab CUDA-v1 exakt:

```text
incoming_edge_ids
```

sind in:

> **streng aufsteigender `edge_id`-Reihenfolge**

gespeichert.

Invariante:

```text
edge_id[i] < edge_id[i + 1]
```

innerhalb eines Targetbereichs.

Doppelte `edge_id` ist ein harter Topologiefehler.

Damit ist die Formulierung:

> „edge_id ascending oder äquivalente Reihenfolge“

ersetzt durch eine einzige normative Regel.

---

# 7. Reduction Contract v1

Bezeichnung:

```text
reduction_version =
"mhrn-deterministic-gather-v1"
```

Der Reduktionsbaum ist Bestandteil der Execution Provenance.

---

# 8. Small-Degree-Gather

Initiale CUDA-v1-Klasse:

```text
degree 0      empty
degree 1..8   SMALL
```

Ein Warp verarbeitet bis zu 32 Targets.

```text
lane 0  -> target 0
lane 1  -> target 1
...
lane 31 -> target 31
```

Jede Lane verarbeitet genau ein Target.

Innerhalb der Lane:

```text
sum = +0.0

for edge in target_edges_sorted_by_edge_id:
    sum = sum + contribution(edge)
```

Damit gilt:

* keine Cross-Lane-Reduktion;
* strikt steigende `edge_id`-Summationsreihenfolge;
* maximal acht lokale Edge-Schritte;
* begrenzte Warp-Divergenz.

Die Targets eines Buckets werden ihrerseits deterministisch in aufsteigender `physical_slot`-Reihenfolge im Schedule abgelegt.

---

# 9. Medium-Degree-Gather

Initial:

```text
degree 9..256
```

Ein vollständiger Warp bearbeitet genau ein Target.

Zuteilung:

```text
lane L:
    edge position L
    edge position L + 32
    edge position L + 64
    ...
```

Jede Lane akkumuliert ihre eigene Folge in steigender CSR-Position.

Nicht vorhandene Beiträge sind:

```text
+0.0
```

Danach erfolgt der normative Warp-Baum:

```text
offset 16
offset 8
offset 4
offset 2
offset 1
```

Lane 0 enthält anschließend das Ergebnis.

Konzeptionell:

```text
s[lane] += s[lane + 16]
s[lane] += s[lane + 8]
s[lane] += s[lane + 4]
s[lane] += s[lane + 2]
s[lane] += s[lane + 1]
```

mit jeweils gültiger aktiver Lane-Maske.

CUDA-Warp-Shuffle-Operationen unterstützen genau solche festen Lane-Austauschmuster; NVIDIA beschreibt insbesondere XOR-/Down-Shuffles als Grundlage für Baumreduktionen.

---

# 10. Large-Degree-Gather

Initial:

```text
degree > 256
```

CUDA-v1 verwendet normativ:

```text
blockDim = 256
```

Ein CTA bearbeitet ein Target.

Thread `T` akkumuliert:

```text
T
T + 256
T + 512
...
```

innerhalb des Target-CSR-Bereichs.

Danach:

```text
8 warps
   ↓
jeweils reduction 16,8,4,2,1
   ↓
lane 0 jedes warps
   ↓
shared_partial[warp_id]
```

Anschließend:

```text
__syncthreads()
```

Warp 0 lädt:

```text
lane 0..7  = shared_partial[0..7]
lane 8..31 = +0.0
```

und führt erneut aus:

```text
16
8
4
2
1
```

Lane 0 produziert den finalen Target-Strom.

---

# 11. Reduction-Invariante

Folgende Parameter sind eingefrorene Execution-Parameter:

```text
reduction_version
warp_width
small_degree_limit
medium_degree_limit
large_block_size
edge_order
lane_assignment_rule
warp_reduction_offsets
CTA_reduction_rule
accumulator_dtype
```

Sie werden nicht während eines wissenschaftlichen Runs automatisch optimiert.

---

# 12. Gather-Profile und Precision-Profile sind orthogonal

Diese beiden Achsen bleiben unabhängig.

## GatherProfile

```text
gather-reference
gather-degree-aware-v1
```

## PrecisionProfile

```text
reference64
deterministic32
future mixed profiles
```

Beispielsweise sind möglich:

```text
gather-reference + reference64

gather-reference + deterministic32

gather-degree-aware-v1 + deterministic32
```

Ein zukünftiges:

```text
gather-degree-aware-v1 + reference64
```

ist ebenfalls grundsätzlich zulässig.

Die Profile werden nicht implizit miteinander gekoppelt.

---

# 13. Bedeutung für D1 Replay

`D1 REPLAY` bedeutet nicht:

> Jeder denkbare Gather-Algorithmus erzeugt dieselben Floating-Point-Bits.

Sondern:

> Derselbe eingefrorene Execution Contract erzeugt unter demselben definierten Execution-Fingerprint denselben Zustand.

Zum Fingerprint gehören mindestens:

```text
backend version
kernel artifact hash
reduction_version
schedule_version
precision_profile
compiler configuration
CUDA runtime
CUDA driver
device architecture
topology_generation
```

Ein Wechsel des Reduktionsbaums erzeugt somit einen anderen Execution Contract.

---

# 14. Schedule Contract

Bezeichnung:

```text
schedule_version =
"degree-buckets-v1"
```

Der Schedule enthält:

```text
small_targets[]
medium_targets[]
large_targets[]
```

Innerhalb jedes Arrays:

```text
physical_slot ascending
```

Der Schedule wird deterministisch aus der aktuellen Topologie erzeugt.

---

# 15. Schedule gehört zum ExecutionSegment

Jedes `ExecutionSegment` enthält mindestens:

```text
schedule_version
schedule_hash
reduction_version
precision_profile
gather_profile
topology_generation
```

Eine Änderung von:

```text
small_degree_limit
medium_degree_limit
block size
bucket algorithm
reduction tree
```

erzeugt einen neuen Execution Contract.

---

# 16. Keine automatische Retuning-Mutation

Während eines wissenschaftlichen Runs ist:

```text
runtime_auto_tuning = false
```

verpflichtend.

Schwellwerte dürfen nicht aufgrund gemessener GPU-Auslastung plötzlich verändert werden.

Für technische Benchmarks darf Auto-Tuning später existieren, aber:

```text
schedule change
→ explicit segment boundary
→ provenance entry
```

Confirmatory Runs verbieten zunächst vollständig:

```text
schedule_transition_count > 0
```

---

# 17. Topologieänderung versus Schedule-Version

Ein CSR-Rebuild erzeugt nicht zwangsläufig eine neue `schedule_version`.

Beispiel:

```text
algorithm:
degree-buckets-v1
```

bleibt gleich.

Aber:

```text
topology_generation:
41 -> 42
```

und:

```text
schedule_hash
```

ändert sich.

Damit unterscheiden wir:

```text
Schedule algorithm version
```

von:

```text
Schedule instance
```

---

# 18. Packed Tissue State

Der Multi-Timescale-Tissue-State wird **nicht** in `PackedNeuronState` oder `PackedSynapseState` hineingemischt.

Stattdessen:

```text
PackedExecutionState
├── PackedNeuronState
├── PackedSynapseState
├── PackedTissueState
├── TopologyState
└── ExecutionMetadata
```

Der bestehende Tissue-Layer hält diese Zustände bereits bewusst als Sidecars außerhalb des kanonischen `NeuralNetwork`.

---

# 19. PackedTissueState

Struktur:

```text
PackedTissueState
├── schema_version
├── source_tissue_schema_version
├── neuron_sidecar
├── synapse_sidecar
├── timescale_config
└── tissue_config
```

Der aktuelle CPU-Sidecar verwendet bereits:

```text
schema_version = 1
```

und serialisiert Neuron- und Synapsen-Slow-State getrennt.

---

# 20. Neuron-Tissue-Layout

Neuronale Sidecar-Werte werden an `physical_slot` ausgerichtet.

Beispiel:

```text
calcium[N]
second_messenger[N]
neuromodulator_gain[N]
prediction[N]
prediction_error[N]
salience[N]
intrinsic_excitability[N]
metabolic_reserve[N]
glial_support[N]
activity_memory[N]
...
```

Die logische Zuordnung entsteht über dasselbe:

```text
physical_slot -> logical_neuron_id
```

Mapping wie beim Core.

---

# 21. Synapse-Tissue-Layout

Synapsen-Sidecars werden künftig nicht dauerhaft über:

```text
(pre_id, post_id)
```

adressiert, sondern über:

```text
edge_id
```

Der gepackte State kann physisch edge-slot-orientiert sein:

```text
edge_slot -> edge_id
```

Sidecar-Felder:

```text
depression_resource
facilitation
ready_vesicle_fraction
release_probability
presynaptic_calcium
ampa_gain
nmda_gain
gaba_a_gain
gaba_b_gain
retrograde_signal
bcm_threshold
synaptic_tag
consolidation
modulation_gain
confidence
dynamic_delay_offset
silent
frozen
cumulative_plasticity_cost
use_count
...
```

bleiben dadurch über CSR-Rebuilds korrekt gebunden.

---

# 22. Tissue Round-Trip

Stage CUDA-1 muss testen:

```text
Canonical Network
+
Canonical Tissue Sidecar
        │
        ▼
PackedExecutionState
        │
        ▼
Canonical Network
+
Canonical Tissue Sidecar
```

und danach:

```text
canonical_hash_before
==
canonical_hash_after
```

ohne Simulationsschritt.

Continuation-kritische Tissue-Felder dürfen nicht verloren gehen.

---

# 23. Aktuelle Konsequenz

Da der Tissue-Controller aktuell einen `to_dict()`-Pfad besitzt, aber der gegenwärtige Code keinen symmetrischen `from_dict()`-Contract zeigt, gehört ein vollständiger Restore-Vertrag **vor den eigentlichen GPU-Kernel**.

Dies ist keine CUDA-Sonderfunktion.

Es ist eine Voraussetzung dafür, dass der Sidecar überhaupt backend-neutral fortgesetzt werden kann.

---

# 24. BoundaryFrame ersetzt SymbolFrame nicht

Der bestehende `SymbolFrame` bleibt zuständig für:

```text
exact digital payload
codec name
sequence
provenance
SHA-256 payload checksum
```

und hält den exakten Payload bewusst außerhalb des SNN.

Der neue `BoundaryFrame` liegt **eine Stufe später**:

```text
SymbolFrame / sensor source
        │
        ▼
Codec
        │
        ▼
BoundaryFrame
        │
        ▼
Execution Backend
        │
        ▼
Afferent neural state
```

Damit gibt es keine doppelte Verantwortung.

---

# 25. BoundaryFrame Contract v1

```text
BoundaryFrame
├── schema_version
├── codec_id
├── codec_version
├── codec_artifact_hash
├── sequence_id
├── source_timestamp
├── target_tick
├── valid_until_tick
├── dtype
├── shape
├── layout
├── normalization_id
├── source_payload_sha256      optional
├── content_sha256
├── frame_sha256
└── values
```

---

# 26. Canonical Value Encoding

`encoded_frame_hash` darf nicht aus einer uneindeutigen JSON-Float-Darstellung entstehen.

Stattdessen bekommt jeder `dtype` eine kanonische Binärrepräsentation.

Beispielsweise:

```text
float32 -> IEEE-754 little-endian
float64 -> IEEE-754 little-endian
int32   -> signed little-endian
uint8   -> raw bytes
```

Arrays:

```text
C-contiguous canonical order
```

Der Codec-Contract definiert:

```text
dtype
shape
layout
endianness
```

explizit.

---

# 27. BoundaryFrame Hashes

## `content_sha256`

```text
SHA256(canonical encoded value bytes)
```

## `frame_sha256`

```text
SHA256(
    canonical_metadata_bytes
    +
    separator
    +
    canonical_value_bytes
)
```

Die Metadaten werden mit definierter kanonischer Serialisierung erzeugt:

```text
sorted keys
UTF-8
no insignificant whitespace
fixed schema
```

---

# 28. Source Payload Hash

Bei digitalen Daten:

```text
source_payload_sha256
```

kann direkt auf den bestehenden `SymbolFrame.checksum` verweisen.

Damit sind zwei unterschiedliche Aussagen prüfbar:

```text
source payload unchanged?
```

und:

```text
encoded neural boundary representation unchanged?
```

Diese Hashes dürfen nicht miteinander verwechselt werden.

---

# 29. Codec-Version-Änderung

Es besteht **keine Forderung**, dass:

```text
Codec v1
```

und:

```text
Codec v2
```

denselben `frame_sha256` erzeugen.

Im Gegenteil:

Eine semantische Codec-Änderung muss sichtbar sein durch:

```text
codec_version
codec_artifact_hash
frame_sha256
```

D1 fordert nur:

```text
same source
same codec artifact
same codec config
same execution contract

→ same BoundaryFrame
```

---

# 30. BoundaryFrame Contract Tests

Stage CUDA-1 bekommt CPU-only Tests für:

```text
same input -> same frame hash

single-bit payload mutation -> different source hash

single-value encoding mutation -> different content hash

metadata mutation -> different frame hash

shape mismatch -> reject

dtype mismatch -> reject

invalid tick interval -> reject

serialization round-trip -> identical frame hash

codec version change -> provenance visible
```

Damit kann der gesamte Boundary-Vertrag bereits auf CI-Systemen ohne GPU vollständig getestet werden.

---

# 31. BoundaryFrame Migration

Ein altes Frame wird nicht stillschweigend als neues Schema interpretiert.

Migration erzeugt:

```text
schema_version = new

migrated_from_schema = old

original_frame_sha256 = ...
```

und berechnet anschließend einen neuen:

```text
frame_sha256
```

Das Original bleibt auditierbar.

---

# 32. Physical Mapping Contract

Beide Richtungen existieren.

## Physical → Logical

Da `local_slot` dicht ist:

```text
physical_to_logical[local_slot]
```

als direktes Array.

Dies ist der schnelle Weg für:

* Outputs;
* Dumps;
* Probes;
* Snapshot-Kanonisierung.

## Logical → Physical

Da logische IDs nicht notwendigerweise dicht sind, wird die kanonische persistierbare Form als sortierte Zuordnung gespeichert:

```text
logical_ids[]
device_ids[]
local_slots[]
```

mit:

```text
logical_ids strictly ascending
```

Die Host-Runtime darf daraus zusätzlich eine Hash-Map aufbauen.

Diese Hash-Map ist aber:

```text
derived runtime cache
```

und kein persistierter kanonischer Zustand.

---

# 33. Mapping gehört nicht in den Hot Path

Normale Kernel arbeiten mit:

```text
local_slot
edge_slot
```

nicht permanent mit:

```text
logical_id lookup
```

Logische IDs werden an kontrollierten Grenzen benötigt:

```text
pack
unpack
checkpoint
probe registration
external mapping
structural barrier
```

Dadurch kostet die wissenschaftlich notwendige ID-Abstraktion nicht bei jeder Synapsenoperation einen Hash-Lookup.

---

# 34. Structural Barrier Contract

Eine strukturelle Mutation darf nie mitten im Tick committen.

Normative Grenze:

```text
Tick N
├── core phases
├── post-core plasticity phases
├── slow-clock phases
└── completed
        │
        ▼
optional structural barrier
        │
        ▼
Tick N+1
```

Der Barrier liegt somit:

> nach vollständigem Abschluss aller für Tick N vorgesehenen kausalen Phasen und vor `latch_external_input` von Tick N+1.

---

# 35. Structural Proposals und Commit sind getrennt

Ein Development-Step darf erzeugen:

```text
StructuralProposal
```

aber:

```text
proposal creation
!=
topology mutation
```

Mutation benötigt einen expliziten Barrier-Commit.

Dadurch kann eine Proposal-Liste niemals unabsichtlich mitten in einem Tick die Topologie verändern.

---

# 36. Wer löst einen Barrier aus?

Der Core löst nicht autonom aufgrund eines einzelnen Proposal-Events sofort einen Rebuild aus.

Der Barrier wird ausgelöst durch einen expliziten:

```text
StructuralBarrierPolicy
```

beispielsweise:

```text
manual
fixed_interval
experiment_defined
disabled
```

In wissenschaftlichen Runs ist diese Policy Bestandteil der eingefrorenen Konfiguration.

---

# 37. Gateway-Rollen

Folgende Rollen können bereits im Schema existieren:

```text
GATEWAY_AFFERENT
GATEWAY_EFFERENT
```

aber für:

```text
CUDA-1
CUDA-2
CUDA-3
```

gilt:

```text
gateway_runtime_activation = false
```

Die Rollen sind zunächst ausschließlich repräsentierbar.

Sie aktivieren weder MSBA noch Neural Symbiosis noch Gateway-Plastizität.

Produktive oder experimentelle Gateway-Ausführung folgt erst in der dafür vorgesehenen späteren CUDA-Stage.

---

# 38. Spike Compaction bleibt Pflicht in CUDA-3

Obwohl:

```text
spike_history
```

die kausale Wahrheit ist, bleibt:

```text
order-preserving spike_ids
```

Pflichtbestandteil von CUDA-3.

Nicht weil die rekurrente Delay-Semantik davon abhängt, sondern weil sie benötigt wird für:

```text
output extraction
debug/probes
telemetry
post-core sparse phases
future sparse propagation
performance measurement
```

Ihre Reihenfolge bleibt jedoch nicht kausal.

---

# 39. Numerical Fault Policy

Es werden zwei Fehlerklassen unterschieden.

## Core Numerical Fault

Beispiel:

```text
neuron v = NaN
synaptic weight = Inf
```

Dies setzt:

```text
run_health = NUMERICAL_FAULT
```

Für:

```text
Golden Tests
confirmatory experiments
deterministic validation
```

ist dies immer:

```text
FAIL + abort
```

---

# 40. Telemetry Numerical Fault

Wenn der Core-Zustand vollständig endlich ist, aber ausschließlich eine nichtkausale Telemetrieaggregation fehlschlägt:

```text
run_health = TELEMETRY_FAULT
```

Dann entscheidet der eingefrorene Experiment-/Runtime-Contract:

```text
abort
or
continue_with_flag
```

Der Fehler wird niemals stillschweigend als `0` oder fehlender Wert ausgegeben.

---

# 41. Schedule- und NaN-Policy im Experiment Contract

Damit gehören vor Run-Start mindestens folgende Felder in die technische Konfiguration:

```text
gather_profile
schedule_version
reduction_version
precision_profile
numerical_fault_policy
telemetry_fault_policy
structural_barrier_policy
```

Keines dieser Felder darf sich in einem confirmatory Run selbstständig ändern.

---

# 42. CUDA-Graph-Abgrenzung

Eine Änderung von:

```text
CSR contents
pointers
element counts
kernel parameters
```

erfordert nicht zwangsläufig eine neue CUDA-Graph-Topologie.

CUDA erlaubt bei gleichbleibender Graphstruktur die Aktualisierung bestimmter Kernelparameter und Speicheradressen; größere Änderungen an Topologie oder Node-Typen benötigen dagegen Re-Instanziierung.

Daher gilt:

```text
neural topology generation
!=
CUDA graph topology generation
```

Beide erhalten getrennte IDs.

---

# 43. Finaler Packed-State-Vertrag

Stage CUDA-1 arbeitet damit auf:

```text
PackedExecutionState
│
├── metadata
│   ├── packed_schema_version
│   ├── canonical_schema_version
│   ├── tissue_schema_version
│   ├── topology_generation
│   ├── execution_contract
│   └── mapping hashes
│
├── neurons
│   └── PackedNeuronState
│
├── synapses
│   └── PackedSynapseState
│
├── tissue
│   └── PackedTissueState
│
├── topology
│   ├── incoming CSR
│   ├── edge-slot mappings
│   └── gather schedule
│
├── temporal
│   └── SpikeHistoryRing
│
└── boundary
    └── BoundaryFrame buffers
```

---

# 44. Neue CUDA-1-Abnahmekriterien

Stage CUDA-1 ist erst abgeschlossen, wenn ohne GPU-Dynamik mindestens folgende Aussagen gelten:

### Neuron identity

```text
logical IDs survive pack/unpack exactly
```

### Edge identity

```text
edge IDs survive pack/unpack exactly
```

### Parallel-edge safety

```text
two edges with same source/target remain distinct
```

### Core state

```text
canonical core round-trip exact
```

### Tissue state

```text
canonical tissue round-trip exact
```

### Mapping

```text
logical <-> physical mapping is bijective
```

### CSR

```text
all incoming edge ranges are edge_id-sorted
```

### Schedule

```text
same topology + same schedule contract
→ same schedule hash
```

### Boundary

```text
same source + same codec
→ same BoundaryFrame hash
```

### GPU dependency

```text
none required for these contract tests
```

---

# 45. CUDA-0 Exit Gate

Stage CUDA-0 gilt erst dann als vollständig spezifiziert, wenn folgende Verträge schriftlich eingefroren sind:

```text
ExecutionBackend
PackedExecutionState
PackedNeuronState
PackedSynapseState
PackedTissueState
ConnectionIdentity
LogicalPhysicalMapping
IncomingCSR
GatherSchedule
ReductionContract
SpikeHistoryRing
BoundaryFrame
CodecContract
ExecutionSegment
StructuralBarrierPolicy
NumericalFaultPolicy
```

Erst danach beginnt CUDA-1.

---

# 46. Wichtigste neue Erkenntnis

Die CUDA-Vorbereitung hat damit einen zusätzlichen architektonischen Nutzen:

Sie zwingt MHRN dazu, drei bislang teilweise implizite Identitäten explizit zu machen:

```text
Neuron identity
Synapse identity
Execution identity
```

Das ist auch unabhängig von CUDA wertvoll.

Ein neuronales Forschungsmodell sollte unterscheiden können:

```text
Was ist das Objekt?

Wo liegt es gerade?

Wie wurde es gerade berechnet?
```

CUDA macht diese Trennung nur zwingend sichtbar.

---

# 47. Finaler Stage-CUDA-0-Stand

Damit gelten nun verbindlich:

```text
Neuron identity:
    stable logical_neuron_id

Neuron placement:
    device_id + local_slot

Synapse identity:
    stable edge_id

Synapse storage:
    edge_slot independent of edge_id

Incoming ordering:
    strict edge_id ascending

Small gather:
    one lane per target
    degree 1..8

Medium gather:
    one warp per target
    degree 9..256
    fixed 16-8-4-2-1 reduction

Large gather:
    one 256-thread CTA per target
    degree >256
    two-stage fixed reduction

Schedule:
    deterministic
    versioned
    hashed
    fixed during scientific run

Spike truth:
    spike_history

Spike frontier:
    order-preserving derived list

Tissue:
    separate PackedTissueState

Codec:
    CPU reference initially

Exact digital payload:
    remains in SymbolFrame/outside SNN

BoundaryFrame:
    canonical encoded backend input

Hashes:
    explicit canonical binary encoding

Mappings:
    bidirectional
    logical lookup outside hot path

Structural mutation:
    tick-boundary barrier only

NaN/Inf:
    never silently ignored

Gateway roles:
    representable but inactive through CUDA-3

Gather and precision:
    independent execution axes

CUDA Graph:
    execution topology distinct from neural topology

CUDA-1:
    packing and identity first
    GPU computation later
```

Damit ist Stage CUDA-0 nicht nur ein Performanceentwurf, sondern ein vollständiger **Identitäts-, State- und Execution-Contract für die spätere GPU-Beschleunigung**.
