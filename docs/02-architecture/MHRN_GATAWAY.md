# MHRN Asynchronous LLM Gateway Contracts v0.2

## Ergänzung: Gateway Learning and Causal Credit Contract

### Status

Architektur- und Forschungsvertrag.

Keine automatische Evidenzpromotion.
Keine produktive Gateway-Plastizität.
Der Mechanismus muss zuerst technisch validiert und anschließend experimentell geprüft werden.

---

# 31. Warum die normale Eligibility nicht ausreicht

MHRN besitzt bereits synaptische Eligibility für normales Drei-Faktor-Lernen.

Diese beantwortet die Frage:

> Welche kürzlich aktive Synapse soll durch einen verzögerten Reward moduliert werden?

Ein LLM-Gateway erzeugt jedoch eine andere Kausalkette:

```text
synaptic activity
      ↓
REQUEST decision
      ↓
external latency
      ↓
RESPONSE
      ↓
response integration
      ↓
ACTION
      ↓
task outcome
```

Zwischen Request und Reward können:

```text
hundreds
bis
thousands of ticks
```

liegen.

Zusätzlich können mehrere Requests gleichzeitig offen sein.

Deshalb darf der Gateway-Reward nicht einfach in den bestehenden globalen Reward-Pfad eingespeist werden.

---

# 32. Gateway-Lernen ist ein eigener Sidecar

Es entsteht:

```text
GatewayLearningState
```

außerhalb des kanonischen Core.

Er verändert den Core nur über einen expliziten, experimentell aktivierten Commit-Pfad.

```text
Core activity
     │
     ▼
local eligibility
     │
     ▼
Gateway tag capture
     │
     ▼
request-specific credit state
     │
     ▼
delayed reward
     │
     ▼
bounded selected weight update
```

---

# 33. Gewähltes Modell für PoC: Tag-and-Capture

Für den ersten Gateway-Lernversuch wird **nicht** eine lang laufende Eligibility über sämtliche Synapsen eingeführt.

Stattdessen:

> Beim Auslösen eines Requests wird ein kleiner, expliziter Satz kausal beteiligter Synapsen eingefroren und mit diesem `request_id` verbunden.

Dies ist ein request-spezifisches Tag-and-Capture-Verfahren.

---

# 34. Warum Tag-and-Capture

Es löst vier Probleme gleichzeitig:

```text
lange LLM-Latenz
mehrere parallele Requests
falsche globale Synapsenmodulation
reproduzierbare Attribution
```

Insbesondere muss eine Synapse nicht über 2.000 Ticks eine globale Trace behalten.

Stattdessen wird ihre relevante Eligibility zum Zeitpunkt der Entscheidung eingefroren.

---

# 35. RequestEligibilityRecord

Bei jeder Gateway-Aktion entsteht:

```text
RequestEligibilityRecord
├── schema_version
├── eligibility_id
├── request_id
├── trial_id
├── gateway_id
├── operation
├── issued_tick
├── request_population_id
├── capture_window_ticks
├── gateway_tau_ticks
├── gateway_eligibility
├── tagged_edges[]
├── response_received_tick
├── response_consumed_tick
├── accumulated_credit
├── accumulated_cost
├── terminal_state
└── provenance
```

---

# 36. TaggedEdge

Jeder eingefrorene synaptische Beitrag wird explizit gespeichert:

```text
TaggedEdge
├── edge_id
├── local_eligibility_at_issue
├── tag_strength
├── pre_id
├── post_id
└── capture_tick
```

`edge_id` ist die stabile Connection Identity aus der MHRN-CUDA-/Core-Spezifikation.

CSR-Position oder Python-Objektadresse dürfen dafür nicht verwendet werden.

---

# 37. Welche Synapsen sind im PoC eligible?

Für PoC v1 gilt absichtlich eine enge Regel.

Eine Synapse ist request-eligible genau dann, wenn:

1. ihr Zielneuron zur ausgelösten `GATEWAY_EFFERENT`-Request-Population gehört;
2. sie innerhalb des festgelegten Entscheidungsfensters kausal aktiv war;
3. ihre bestehende lokale Eligibility zum `issued_tick` den Mindestbetrag überschreitet;
4. sie nicht frozen/disabled ist;
5. ihre `edge_id` eindeutig vorhanden ist.

Formal:

$$
T_r =
\left\{
e:
post(e)\in P_r
\land
|z_e(t_r)|\ge\epsilon_{tag}
\land
active_e(t_r-\Delta,t_r)
\right\}
$$

mit:

* \(P_r\): Request-Population;
* \(z_e\): normale lokale synaptische Eligibility;
* \(t_r\): Request-Tick;
* \(\Delta\): Capture Window;
* \(\epsilon_{tag}\): Mindesttrace.

---

# 38. Im ersten PoC nur ein Hop

Der erste Lernversuch verändert ausschließlich:

> eingehende Synapsen der Request-Entscheidungspopulation.

Nicht automatisch:

```text
gesamtes Assoziationsnetz
ContextProjector
Response-Population
Sensorpfade
Structural Plasticity
```

Damit lässt sich kausal prüfen, ob das SNN überhaupt die Auswahl eines Gateways lernen kann.

Spätere Experimente dürfen einen:

```text
credit_depth > 1
```

untersuchen.

Aber nicht PoC v1.

---

# 39. Tag-Erzeugung

Beim Request wird die normale synaptische Eligibility gelesen:

$$
z_e(t_r)
$$

und in einen eingefrorenen request-spezifischen Tag überführt:

$$
q_{r,e}
=
clip
\left(
\frac{z_e(t_r)}{z_{scale}},
-q_{max},
q_{max}
\right)
$$

Der Tag behält sein Vorzeichen.

Damit kann eine spätere Belohnung je nach lokalem Kausalzustand sowohl Potenzierung als auch Depression ermöglichen.

---

# 40. Wichtig: Die normale Eligibility wird nicht übernommen

Nach Capture entwickeln sich zwei Zustände unabhängig:

```text
normal synaptic eligibility
```

und:

```text
request tag q[r,e]
```

weiter.

Der Request-Tag ist ein Snapshot.

Spätere neuronale Aktivität verändert rückwirkend nicht, welche Synapsen Request `r` ausgelöst haben.

---

# 41. Gateway-Eligibility

Zusätzlich besitzt der Request selbst eine nichtnegative zeitliche Eligibility:

$$
g_r(t)
=
\exp
\left(
-\frac{t-t_r}{\tau_g}
\right)
$$

mit:

```text
0 <= g_r <= 1
```

und versioniertem:

```text
gateway_tau_ticks
```

---

# 42. `tau_g` ist keine biologische Behauptung

`tau_g` repräsentiert eine technische Credit-Zeitskala für externe Werkzeugnutzung.

Es wird nicht als biologische Zeitkonstante interpretiert.

Für Experimente muss der Wert preregistriert werden.

Beispielhafter Suchraum:

```text
250
500
1000
2000
5000 ticks
```

Nicht automatisch optimieren.

---

# 43. Gateway-Credit

Ein Request erhält Credit nur aus Ereignissen, die explizit zu ihm gehören.

Beispiele:

```text
response accepted
response consumed
task success
task failure
request cost
timeout
invalid response
stale response
```

Nicht erlaubt:

```text
ungebundener globaler Reward
    ↓
alle offenen Requests
```

---

# 44. RewardEvent benötigt Task-Identität

```text
GatewayRewardEvent
├── reward_id
├── trial_id
├── effective_tick
├── reward_type
├── value
├── source
├── causal_request_ids[]
└── provenance
```

Ein Reward ohne `trial_id` oder explizite Attribution darf im Gateway-Lernpfad keine Gewichtsänderung verursachen.

---

# 45. PoC-Attributionspolicy

Für PoC v1 gilt:

```text
task-bound-consumed-normalized-v1
```

Eligible sind nur Requests:

1. desselben `trial_id`;
2. deren Response tatsächlich vom SNN konsumiert wurde;
3. die noch nicht abgelaufen/cancelled waren;
4. deren Gateway-Eligibility oberhalb `epsilon_gateway` liegt.

---

# 46. Mehrere parallele Requests

Seien die eligible Requests:

$$
R = \{r_1,\ldots,r_n\}
$$

Dann erhält jeder Request den Attribution-Faktor:

$$
a_r
=
\frac{g_r(t)}
{\sum_{k\in R} g_k(t)}
$$

Damit gilt:

$$
\sum_r a_r = 1
$$

und ein Task-Reward wird nicht versehentlich vollständig auf jeden parallelen Request kopiert.

---

# 47. Kein Credit über Task-Grenzen

Request:

```text
trial_id = 17
```

kann niemals Reward erhalten von:

```text
trial_id = 18
```

selbst wenn beide zeitlich überlappen.

Das ist eine harte Invariante.

---

# 48. Gewichtsupdates

Für Request `r`, Edge `e` und Reward `R`:

$$
\Delta w_{r,e}
=
\eta_g
\cdot
R
\cdot
a_r
\cdot
g_r(t_R)
\cdot
q_{r,e}
$$

Danach wird die bereits bestehende Soft-Bound-Logik angewendet.

Konzeptionell:

```text
raw_delta
    ↓
directional soft bound
    ↓
configured weight limits
    ↓
weight update
```

---

# 49. Kosten werden als eigener negativer Credit behandelt

Gateway-Kosten werden nicht versteckt in den Task-Reward gemischt.

Ein Request kann beispielsweise erhalten:

$$
R_r =
R_{task}
-
\lambda_c C_r
-
\lambda_l L_r
$$

Aber die Einzelkomponenten bleiben gespeichert:

```text
task_credit
cost_penalty
latency_penalty
timeout_penalty
```

Damit kann später analysiert werden, warum ein Gateway weniger genutzt wurde.

---

# 50. PoC-Kostenmodell

Für den ersten PoC sollte das Kostenmodell absichtlich einfach sein:

```text
fixed_call_cost
+
normalized_latency_cost
```

Keine echten Euro-Providerkosten sind erforderlich.

Beispiel:

$$
C_r =
c_{call}
+
\lambda_{latency}
\cdot
clip
\left(
\frac{logical\_wait\_ticks}{L_{max}},
0,1
\right)
$$

Alle Koeffizienten werden preregistriert.

---

# 51. Drei-Faktor-Lernen vs. Gateway-Lernen

Normales Drei-Faktor-Lernen:

```text
recent synaptic activity
   ×
global/local reward
   ×
short eligibility
```

Gateway-Lernen:

```text
specific gateway action
   ×
frozen causal synaptic tags
   ×
request-specific delayed eligibility
   ×
task-bound attribution
   ×
gateway-specific delayed credit
```

Es handelt sich nicht um denselben Mechanismus.

Gateway-Lernen benutzt bestehende lokale Eligibility lediglich zur **Tag-Selektion**, nicht als lang laufenden globalen Gateway-Trace.

---

# 52. Keine doppelte Gewichtsmodulation

Ein Experiment muss explizit festlegen:

```text
gateway_learning_enabled
core_reward_learning_enabled
```

Für PoC v1:

```text
gateway_learning_enabled = true

core_reward_learning_enabled = false
```

für die Request-Auswahlsynapsen.

Damit wirkt derselbe Reward nicht gleichzeitig über zwei verschiedene Lernpfade auf dieselben Kanten.

---

# 53. Gateway Action Selection Contract

Eine Request-Population löst nicht bei jedem Spike eine Anfrage aus.

Für jede Gateway-Operation existiert ein Akkumulator:

$$
A_o(t)
=
\alpha A_o(t-1)
+
S_o(t)
$$

wobei:

* \(S_o(t)\): normalisierte Spikeaktivität der Request-Population;
* \(\alpha\): versionierter Decay.

---

# 54. Decision Windows

Gateway-Entscheidungen erfolgen nur an festen Grenzen:

```text
decision_interval_ticks
```

Beispiel:

```text
10 ticks
```

Nicht bei jedem einzelnen Tick.

---

# 55. Request-Auslösung

Eine Operation ist Kandidat, wenn:

$$
A_o \ge \theta_o
$$

Zusätzlich müssen gelten:

```text
cooldown expired
pending limit not exceeded
gateway available
resource policy permits request
```

---

# 56. Deterministische Auswahl

Wenn mehrere Operationen gleichzeitig kandidieren:

```text
highest accumulator wins
```

Bei exakt gleichem Wert:

```text
lowest stable operation_id wins
```

Damit ist die Entscheidung reproduzierbar.

---

# 57. NO_REQUEST ist eine echte Option

Das SNN muss lernen können:

> Kein externes Werkzeug ist nötig.

Deshalb besitzt der Entscheidungsraum implizit oder explizit:

```text
NO_REQUEST
```

Ein Gateway ist kein Pflichtpfad.

---

# 58. Cooldown

Nach Request-Auslösung:

```text
A_o = reset_value
```

und:

```text
cooldown_until_tick
```

wird gesetzt.

Während des Cooldowns kann dieselbe Operation keinen neuen Request erzeugen.

Damit verhindert MHRN:

```text
REQUEST
REQUEST
REQUEST
REQUEST
```

bei derselben persistenten Aktivität.

---

# 59. Concurrency Limit

Pro Gateway:

```text
max_pending_requests
```

und optional:

```text
max_pending_per_operation
```

Sind diese erreicht, erzeugt weitere Request-Aktivität keinen neuen externen Call.

Der blockierte Versuch darf als interozeptives Signal zurückgegeben werden.

---

# 60. Request Cancellation

Ein Pending Request kann einen zusätzlichen Zustand erhalten:

```text
CANCEL_REQUESTED
```

Transition:

```text
QUEUED/DISPATCHED
      ↓
CANCEL_REQUESTED
```

Wenn der externe Backend-Aufruf technisch abbrechbar ist:

```text
CANCEL_REQUESTED
      ↓
CANCELLED
```

Andernfalls läuft er extern weiter.

Eine später eintreffende Response wird dann:

```text
DISCARD
```

oder:

```text
MEMORY_ONLY
```

nach eingefrorener Policy behandelt.

Sie darf keine aktuelle Handlungsaktion auslösen.

---

# 61. Wer darf canceln?

Cancellation kann stammen aus:

```text
SNN cancellation population
context invalidation
trial termination
safety/runtime policy
```

Die Ursache wird gespeichert.

---

# 62. Response Population ist getrennt

Eine LLM-Antwort wird niemals in die Request-Population zurückgeschrieben.

Beispiel:

```text
REQUEST_LANGUAGE
    role = GATEWAY_EFFERENT
```

und:

```text
RESPONSE_LANGUAGE
    role = GATEWAY_AFFERENT
```

sind getrennte neuronale Populationen.

---

# 63. Context Binding

Eine Response besitzt:

```text
request_id
context_snapshot_id
```

Zusätzlich bekommt jeder aktive Pending Request einen begrenzten:

```text
context_slot
```

Beispiel:

```text
0..31
```

---

# 64. Response-Injection

Die Antwort wird als Kombination kodiert:

```text
Response content population
        +
Context-slot population
        +
Gateway identity population
        +
Trust/cost population
```

Also:

```text
CONTENT
   ×
CONTEXT
   ×
SOURCE
```

nicht nur als globaler `RESPONSE_LANGUAGE`-Impuls.

---

# 65. Context-Slot-Lifecycle

Ein `context_slot` wird beim Request reserviert.

Er darf erst wiederverwendet werden, wenn:

```text
request terminal
+
response processing completed
+
reuse guard expired
```

Dadurch kann eine verspätete Response nicht versehentlich einem neuen Request zugeordnet werden.

---

# 66. Response-Use-Credit

PoC v1 lernt zunächst nur:

```text
Soll ich das Gateway aufrufen?
```

Deshalb bleiben Response-Verarbeitungssynapsen zunächst frozen.

Eine spätere Stage darf zusätzlich erforschen:

```text
Wie soll ich eine konkrete Antwort nutzen?
```

Dafür wird ein zweites Tag-Set eingeführt:

```text
ResponseUseEligibility
```

Dieses wird bewusst **nicht** Bestandteil des ersten PoC.

---

# 67. Cost Timing

Gateway-Kosten entstehen zu unterschiedlichen Zeitpunkten.

Deshalb werden sie als Events behandelt.

### Issue-time

Bekannt:

```text
fixed_call_cost
estimated_budget
```

### Response-time

Bekannt:

```text
logical_wait_ticks
wall_latency_ms
response size
timeout
success
```

### Later reconciliation

Möglicherweise später bekannt:

```text
provider billing
measured energy
```

---

# 68. Keine rückwirkende stille Änderung

Ein später eintreffendes Billing-Signal darf nicht rückwirkend unbemerkt einen längst abgeschlossenen Lernschritt umschreiben.

Falls spätes Kosten-Credit Bestandteil eines Experiments sein soll, benötigt es einen expliziten:

```text
DelayedCostEvent
```

mit eigenem `effective_tick` und Attribution Contract.

PoC v1 benutzt ausschließlich Kosten, die spätestens beim Responseabschluss bekannt sind.

---

# 69. Response Schema Contract

Jede Response bindet:

```text
response_schema_id
response_schema_version
response_schema_hash
codec_version
```

Ein Schemawechsel innerhalb eines eingefrorenen Experiments ist nicht erlaubt.

Änderung von:

```text
schema v1 → schema v2
```

erzeugt einen neuen Experiment-/Execution-Contract.

---

# 70. CPU-Concurrency-Modell

Der Gateway-Service verwendet einen:

> **single-authoritative-writer state model**

Externe Worker dürfen keine `PendingRequest`- oder `GatewayMemory`-Objekte direkt mutieren.

Sie erzeugen nur immutable Events.

```text
external worker
      ↓
immutable GatewayEvent
      ↓
ordered ingress queue
      ↓
single gateway state owner
```

---

# 71. Deterministische Event-Anwendung

Im Replay-Modus werden Gateway-Events sortiert nach:

```text
delivery_tick
request_sequence
event_type_priority
```

Im Live-Modus wird die reale Arrival-Reihenfolge aufgezeichnet und auf eine definierte Tick-Grenze abgebildet.

Damit existiert nur eine Stelle, die Gateway-State verändert.

---

# 72. Golden Test GW-LEARN-001

Minimalnetz:

```text
Neuron A
   │ edge 101
   ▼
REQUEST neuron R

Neuron B
   │ edge 102
   ▼
REQUEST neuron R

Neuron X
   │ edge 999
   ▼
unrelated neuron Y
```

Initial:

```text
w101 = 0.50
w102 = 0.50
w999 = 0.50
```

Bei Tick 100:

```text
eligibility(edge101) = +0.8
eligibility(edge102) = -0.4
eligibility(edge999) = +1.0
```

Request wird durch Population R ausgelöst.

Capture:

```text
T_request = {
  101: +0.8,
  102: -0.4
}
```

Edge 999 wird **nicht** getaggt.

---

# 73. Golden Test Reward

Angenommen:

```text
tau_g = 1000 ticks
reward_tick = 600
task_reward = +1.0
eta_g = 0.01
one eligible request
```

Dann:

$$
g_r(600)
=
e^{-500/1000}
$$

und:

$$
\Delta w_{101}
=
0.01
\cdot 1
\cdot g_r
\cdot 0.8
$$

$$
\Delta w_{102}
=
0.01
\cdot 1
\cdot g_r
\cdot (-0.4)
$$

aber:

$$
\Delta w_{999}=0
$$

muss exakt gelten.

---

# 74. Golden-Test-Invarianten

Der Test muss zusätzlich zeigen:

```text
same seed/config
→ same tagged edge IDs

unrelated eligible synapse
→ no update

cancelled request
→ no positive task credit

expired request
→ no current-action credit

wrong trial reward
→ no update

duplicate reward_id
→ applied at most once

duplicate response
→ consumed at most once
```

---

# 75. Multi-Request Golden Test

Requests:

```text
R1 issued tick 100
R2 issued tick 300
```

Reward:

```text
tick 600
trial_id same
```

Dann werden:

$$
g_1(600)
$$

und:

$$
g_2(600)
$$

berechnet.

Attribution:

$$
a_1=
\frac{g_1}{g_1+g_2}
$$

$$
a_2=
\frac{g_2}{g_1+g_2}
$$

Der gesamte positive Task-Credit darf dadurch nicht verdoppelt werden.

---

# 76. Mechanismusvalidierung vor Verhaltenshypothese

Zwei Fragen werden strikt getrennt.

### Mechanismusfrage

> Implementiert MHRN den preregistrierten Gateway-Credit-Algorithmus korrekt?

Das prüfen:

```text
Golden Tests
deterministic replay
tag identity
reward attribution
bounded weight updates
```

### Forschungsfrage

> Führt dieser Mechanismus zu nützlicher selektiver Werkzeugnutzung?

Das prüfen die Gateway-Experimente.

---

# 77. Falsifikationslogik

Wenn der Mechanismus-Golden-Test fehlschlägt:

```text
experiment INVALID
```

nicht:

```text
hypothesis falsified
```

Denn die Intervention wurde technisch nicht korrekt umgesetzt.

---

# 78. Behavioral Falsification

Wenn hingegen:

1. alle Mechanismusvalidierungen bestanden sind;
2. alle Bedingungen korrekt ausgeführt wurden;
3. genügend preregistrierte unabhängige Seeds vorliegen;
4. der learned-gateway-Zustand keinen preregistrierten Vorteil zeigt;

dann ist die entsprechende Verhaltenshypothese:

```text
NOT SUPPORTED / FALSIFIED UNDER PROTOCOL
```

abhängig von der zuvor festgelegten statistischen Entscheidungsregel.

---

# 79. Konkret falsifizierbare Gateway-Hypothese

Beispielsweise:

> H-GW-LLM-01: Unter gleichem Ressourcenbudget erreicht die gelernte SNN-Gateway-Selektion eine höhere preregistrierte Utility als frozen, random und information-destroyed controls.

Utility wird **vorab** definiert.

Zum Beispiel:

$$
U =
TaskPerformance
-
\lambda_c GatewayCost
$$

Nicht nach Sichtung der Ergebnisse ändern.

---

# 80. Vergleich mit ALWAYS-LLM

`ALWAYS_LLM` besitzt eine besondere Rolle.

Wenn learned gateway:

```text
gleiche Leistung
+
weniger Calls
```

erreicht, kann das bereits ein Erfolg sein.

Es muss nicht zwingend höhere rohe Task Accuracy als ALWAYS erzielen.

Deshalb sollte ein primäres Ergebnis eher sein:

```text
utility under fixed budget
```

als:

```text
raw accuracy only
```

---

# 81. Condition F bleibt Pflicht

```text
ALWAYS_LLM_INFORMATION_DESTROYED
```

bleibt notwendig.

Zusätzlich sollte eine Timing-Kontrolle vorgesehen werden:

```text
CORRECT_INFORMATION_TIMING_SHUFFLED
```

um zu prüfen, ob die zeitlich korrekte Bindung zwischen Request und Response relevant ist.

---

# 82. Forschungsprogramm in Stufen

### GW-L0 — Mechanism Verification

Kein LLM erforderlich.

```text
synthetic responses
fixed rewards
golden tagged edges
```

### GW-L1 — Single Gateway Selection

Ein Gateway.

Eine Aufgabe.

Nur Request-Auswahlsynapsen lernen.

### GW-L2 — Delayed External Response

Echte variable Latenz.

Record/Replay.

### GW-L3 — Multiple Requests

Mehrere parallele Requests.

Explizite Attribution.

### GW-L4 — Cost-sensitive Selection

Gateway-Nutzung gegen Kosten optimieren.

### GW-L5 — Multiple Tools

Beispielsweise:

```text
LLM
Vision model
Memory
Logic service
```

### GW-L6 — Response-use Learning

Erst hier werden Synapsen der Response-Integration selbst plastisch.

---

# 83. Was PoC v1 ausdrücklich nicht tut

Nicht gleichzeitig lernen:

```text
gateway selection
response decoder
context projector
core global reward
structural plasticity
gateway topology
LLM prompt generation
```

PoC v1 lernt genau eine Sache:

> **Soll diese Gateway-Aktion unter diesem SNN-Zustand ausgelöst werden?**

---

# 84. Kernaussage des Lernvertrags

Der vollständige Pfad lautet jetzt:

```text
local synaptic causality
        ↓
request decision
        ↓
freeze sparse edge tags
        ↓
asynchronous external request
        ↓
request-specific gateway eligibility
        ↓
response consumption
        ↓
task-bound outcome
        ↓
normalized request attribution
        ↓
bounded updates only on tagged edges
```

Damit ist:

```text
accumulated_reward
```

kein unbestimmter Platzhalter mehr.

Es existiert ein expliziter, testbarer Pfad von einem konkreten Task-Ergebnis zurück zu genau den Synapsen, die die Gateway-Aktion mit ausgelöst haben.

---

# 85. Wissenschaftliche Grenze

Tag-and-Capture v1 ist **eine zu prüfende Lernhypothese**, keine behauptete biologische Wahrheit und kein bereits validierter optimaler Gateway-Lernalgorithmus.

Alternative Modelle wie:

```text
long eligibility trace
actor-critic
TD learning
policy gradient
hierarchical reinforcement learning
different tag propagation depths
```

dürfen später als kontrollierte Alternativen untersucht werden.

Sie dürfen nicht nachträglich stillschweigend unter derselben Modellversion ausgetauscht werden.


================================================================================
                   MHRN - SNN / GATEWAY / LLM ARCHITEKTUR
================================================================================


                         AUSSENWELT / SENSORIK / TASK
                         ============================

        Kamera        Audio        Digital        Task / Reward      Systemzustand
          |             |             |                |                  |
          v             v             v                v                  v
     +---------+   +---------+   +---------+      +---------+       +---------+
     | Encoder |   | Encoder |   | Codec   |      | Reward  |       | Intero- |
     | Vision  |   | Audio   |   | Digital |      | Source  |       | zeption |
     +----+----+   +----+----+   +----+----+      +----+----+       +----+----+
          |             |             |                |                  |
          +-------------+-------------+----------------+------------------+
                                        |
                                        v
                             +-----------------------+
                             |    Boundary Frames    |
                             |-----------------------|
                             | source_id             |
                             | sequence_id           |
                             | target_tick           |
                             | valid_until_tick      |
                             | codec_id              |
                             | payload / content hash|
                             +-----------+-----------+
                                         |
                                         v


================================================================================
                     GPU / SNN - SIMULATION TIME
================================================================================

                  Canonisches Spiking Neural Network
                  -------------------------------


       GATEWAY_AFFERENT / SENSORISCHE EINGANGSPOPULATIONEN
       ==================================================

         +-------------+   +-------------+   +-------------+
         | VISION_IN   |   | AUDIO_IN    |   | DIGITAL_IN  |
         | neurons     |   | neurons     |   | neurons     |
         +------+------+   +------+------+   +------+------+
                \                |                 /
                 \               |                /
                  \              |               /
                   v             v              v

                    +---------------------------+
                    | ASSOCIATIVE POPULATION    |
                    |---------------------------|
                    | Musterbildung             |
                    | Integration               |
                    | Rekurrenz                 |
                    | Prediction                |
                    | Salience                  |
                    +-------------+-------------+
                                  |
              +-------------------+-------------------+
              |                   |                   |
              v                   v                   v

      +---------------+   +---------------+   +---------------+
      | CONTEXT       |   | MEMORY        |   | VALUE / COST  |
      | population    |   | population    |   | population    |
      |---------------|   |---------------|   |---------------|
      | aktuelle Lage |   | Erfahrung     |   | Nutzen        |
      | task state    |   | Muster        |   | Kosten        |
      | relevance     |   | Assoziation   |   | Trust         |
      +-------+-------+   +-------+-------+   +-------+-------+
              \                   |                   /
               \                  |                  /
                +-----------------+-----------------+
                                  |
                                  v
                        +--------------------+
                        | ACTION SELECTION   |
                        |--------------------|
                        | NO_REQUEST         |
                        | REQUEST_LANGUAGE   |
                        | REQUEST_VISION     |
                        | REQUEST_MEMORY     |
                        | REQUEST_PLAN       |
                        | normal actions     |
                        +---------+----------+
                                  |
                                  |
                      decision interval / threshold
                                  |
                                  v

                 GATEWAY_EFFERENT REQUEST POPULATIONS
                 ====================================

             +----------------------+   +----------------------+
             | REQUEST_LANGUAGE     |   | REQUEST_MEMORY       |
             | population           |   | population           |
             +----------+-----------+   +----------+-----------+
                        |                          |
             +----------+-----------+   +----------+-----------+
             | REQUEST_VISION       |   | REQUEST_PLAN         |
             | population           |   | population           |
             +----------+-----------+   +----------+-----------+
                        \                          /
                         \                        /
                          +----------+-----------+
                                     |
                                     v
                           +---------------------+
                           | REQUEST DECODER     |
                           |---------------------|
                           | population activity |
                           | -> RequestFrame      |
                           +----------+----------+
                                      |
                                      |
                                      | asynchronous boundary
                                      |
                                      v


================================================================================
                         CPU - GATEWAY SERVICE
                         WALL-CLOCK TIME
================================================================================

                           +----------------------+
                           | Request Manager      |
                           |----------------------|
                           | request_id           |
                           | gateway_id           |
                           | operation            |
                           | issued_tick          |
                           | valid_until_tick     |
                           | context_snapshot_id  |
                           | trial_id             |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           | Pending Request      |
                           |----------------------|
                           | CREATED              |
                           | QUEUED               |
                           | DISPATCHED           |
                           | RESPONDED            |
                           | CONSUMED             |
                           | EXPIRED              |
                           | CANCELLED            |
                           +----------+-----------+
                                      |
                                      v
                    +--------------------------------------+
                    | NetworkAreaAdapter / Neural Symbiosis|
                    +------------------+-------------------+
                                       |
                     +-----------------+-----------------+
                     |                                   |
                     v                                   v
            +------------------+                +------------------+
            | LLM / Language   |                | Other Tool       |
            |------------------|                |------------------|
            | local model      |                | Vision model     |
            | CPU model        |                | Memory           |
            | remote service   |                | Logic            |
            | API              |                | Database         |
            +--------+---------+                +--------+---------+
                     |                                   |
                     +-----------------+-----------------+
                                       |
                                       v
                           +----------------------+
                           | Response Processor   |
                           |----------------------|
                           | schema validation    |
                           | confidence           |
                           | output normalization |
                           | response hash        |
                           +----------+-----------+
                                      |
                                      v
                           +----------------------+
                           | ResponseFrame        |
                           |----------------------|
                           | request_id           |
                           | context_snapshot_id  |
                           | structured payload   |
                           | provider confidence  |
                           | latency              |
                           | cost                 |
                           | backend provenance   |
                           +----------+-----------+
                                      |
                                      |
                                      | async return
                                      |
                                      v


================================================================================
                    GPU / SNN - RESPONSE-INJEKTION
================================================================================

                         +-----------------------+
                         | GatewayStateCodec     |
                         +-----------+-----------+
                                     |
            +------------------------+------------------------+
            |                        |                        |
            v                        v                        v

    +---------------+       +----------------+       +----------------+
    | RESPONSE      |       | CONTEXT SLOT   |       | GATEWAY STATE  |
    | population    |       | population     |       | population     |
    |---------------|       |----------------|       |----------------|
    | response info |       | request context|       | latency        |
    | concepts      |       | binding        |       | cost           |
    | attributes    |       |                |       | confidence     |
    +-------+-------+       +--------+-------+       | reliability    |
            \                        |               +--------+-------+
             \                       |                        /
              +----------------------+-----------------------+
                                     |
                                     v
                          +----------------------+
                          | ASSOCIATIVE NETWORK  |
                          +----------+-----------+
                                     |
                       +-------------+-------------+
                       |                           |
                       v                           v
              +----------------+          +----------------+
              | MEMORY UPDATE  |          | ACTION GATE    |
              | population     |          | population     |
              +-------+--------+          +-------+--------+
                      |                           |
                      |                           v
                      |                  +------------------+
                      |                  | EFFERENT OUTPUT  |
                      |                  |------------------|
                      |                  | motor            |
                      |                  | speech           |
                      |                  | digital action   |
                      |                  +--------+---------+
                      |                           |
                      +---------------------------+
                                                  |
                                                  v
                                             AUSSENWELT


================================================================================
                             SYNAPSENEBENE
================================================================================

 Normale Core-Synapse
 --------------------
   pre neuron
       |
       | weight
       | delay
       | STDP / eligibility
       v
   post neuron


 Beispiel:

   [ASSOCIATIVE neuron]
           |
           | edge_id = 1042
           | weight  = 0.63
           | delay   = 4 ticks
           v
   [REQUEST_LANGUAGE neuron]


 Wichtige Trennung:

   Synapse Identity:            edge_id
   Neuron Identity:             logical_neuron_id
   Speicherposition GPU:        physical_slot
   GPU-Synapsenposition:        edge_slot


================================================================================
                         GATEWAY-LEARNING-PFAD
================================================================================

          normale Aktivität vor Request
                     |
                     v
        +---------------------------+
        | normale Synaptic          |
        | Eligibility               |
        | kurze Zeitskala           |
        +-------------+-------------+
                      |
                      | Request ausgelöst
                      v
        +---------------------------+
        | TAG-AND-CAPTURE           |
        |---------------------------|
        | nur kausale edge_ids      |
        | werden eingefroren        |
        +-------------+-------------+
                      |
                      v
        RequestEligibilityRecord
        ------------------------
        request_id
        tagged_edges[]
        issued_tick
        tau_g
        trial_id
        context_id
                      |
                      |
            externe LLM-Wartezeit
                      |
                      v
                  Response
                      |
                      v
                  Aktion
                      |
                      v
                   Reward
                      |
                      v
          +-----------------------+
          | Gateway Attribution   |
          +-----------+-----------+
                      |
                      v

          Delta w(r,e) =
              eta_g
            * Reward
            * request_attribution
            * gateway_eligibility
            * captured_edge_tag

                      |
                      v
            NUR GETAGGTE SYNAPSEN
              werden verändert


 Nicht:

          Reward
            |
            v
     ALLE SYNAPSEN IM NETZ


================================================================================
                           AUSFÜHRUNGSORTE
================================================================================

 GPU / CUDA
 ----------
 - Neuronen
 - Synapsen
 - Membranmodelle
 - Spike propagation
 - Delay ring
 - STDP
 - lokale Eligibility
 - Tissue-State
 - Request-Populationen
 - Response-Populationen
 - Action Selection
 - neuronales Memory
 - Gateway-State-Repräsentation


 CPU / MHRN Runtime
 ------------------
 - Gateway Runtime
 - Request Manager
 - Pending Requests
 - Context Snapshot
 - BoundaryFrame / RequestFrame / ResponseFrame
 - Gateway Eligibility Records
 - Gateway Memory
 - Record / Replay
 - Provenienz
 - Checkpoints
 - Structural Barriers
 - Codec-Referenz


 EXTERN / OPTIONAL
 -----------------
 - LLM
 - Vision Transformer
 - Speech Model
 - Datenbank
 - Logic Engine
 - weitere neuronale Netze
 - Remote Services


 SSD
 ---
 - Snapshots
 - Checkpoints
 - Gateway Journal
 - Replay-Daten
 - Experiment DATA
 - EVID / Reports
 - große persistente Zustände


================================================================================
                           NEURON ROLE SCHEMA
================================================================================

                           Neuron
                              |
          +-------------------+-------------------+
          |                   |                   |
        MODEL               TYPE                ROLE
          |                   |                   |
    Izhikevich           sensory           ASSOCIATIVE
    LIF                  motor             AFFERENT
    HH future            RS                EFFERENT
    ...                  FS                GATEWAY_AFFERENT
                         ...               GATEWAY_EFFERENT


 Beispiel:

 logical_neuron_id = 4711

 Model:
     Izhikevich

 Type:
     sensory

 Role:
     GATEWAY_AFFERENT

 Population:
     RESPONSE_LANGUAGE

 physical_location:
     GPU 0 / slot 58213


================================================================================
                    GESAMTER GESCHLOSSENER KREIS
================================================================================

     Umwelt
       |
       v
   Sensoren
       |
       v
     SNN
       |
       | "Brauche ich externes Wissen?"
       |
       +---------------- NO ----------------+
       |                                    |
      YES                                   |
       |                                    |
       v                                    |
 Request Population                         |
       |                                    |
       v                                    |
 RequestFrame                               |
       |                                    |
       v                                    |
     LLM                                    |
       |                                    |
       v                                    |
 ResponseFrame                              |
       |                                    |
       v                                    |
 Response Neurons                           |
       |                                    |
       v                                    |
 Associatives SNN <-------------------------+
       |
       v
   Action Gate
       |
       v
     Aktion
       |
       v
    Ergebnis
       |
       v
 Reward / Cost / Trust
       |
       v
 Gateway Learning
       |
       v
 zukünftige Gateway-
 Entscheidungen ändern sich
