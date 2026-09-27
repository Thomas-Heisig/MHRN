# PAN im MHRN Playground — Gesamtdokumentation

**Stand:** 27. September 2026  
**Klasse:** PLAYGROUND / PLAYGROUND_PAN / PLAYGROUND_GEOMETRY  
**Wissenschaftlicher Status:** explorativ · nicht kanonisch · keine DATA · keine EVID

Diese Dokumentation konsolidiert den aktuellen PAN-Stand im MHRN Playground:
Architektur, implementierte Mechanismen, geometrische Erweiterung, Diagnostik,
Literaturkontext, mathematische Korrekturen, offene Designfragen und alle
derzeit formulierten Research Candidates.

Sie ist ausdrücklich **kein wissenschaftlicher Ergebnisbericht im Sinne von
MHRN DATA oder EVID**.

---

## 1. Ergebnisstatus auf einen Blick

PAN liegt derzeit als funktionsfähige, isolierte Explorationsschicht im
Playground vor.

### Implementiert

- PAN-Hyperzustand mit 5..32 Zustandsdimensionen `Ds`
- semantische PAN-Achsen
- exploratives `pan_adex_5d`
- `pan_stp_stdp`
- Health, Energie, Aktivitätshistorie und Konsolidierungs-Proxy
- variable Spike-Amplitude
- bounded Aging-/Apoptose-Zustand
- optionaler Closed Loop über einen Populations-Hyperzustand
- Hypervektor-Binding und Bundling
- getrennte geometrische Dimensionen `Dg`
- `geometric_5d = (x,y,z,a,b)`
- additive und Shortcut-Geometriemodi
- xyz-basierte Leitungsverzögerung
- Geometrie- und Netzwerkdiagnostik
- PAN-Literaturkontext
- Geometrie-Literaturkontext
- acht nicht-präregistrierte Research Candidates

### Noch nicht implementiert

- echte Partial Information Decomposition (PID)
- PID-gesteuerte Lernregel im PAN-Neuron
- dynamische geometrische Positionierung
- PID-gesteuerte geometrische Kräfte
- Neurogenese mit Positionswahl
- adaptive Myelinisierung
- Klein-Flaschen-Identifikation
- wissenschaftlich validierte Bindung von Zustands- und Geometrierraum
- formale kanonische PAN-Preregistration
- kanonische PAN-DATA
- Human Review für PAN
- PAN-EVID

---

## 2. Governance-Grenze

Jeder Playground-Lauf bleibt zwingend:

```text
class: PLAYGROUND
scientific_evidence: false
data: false
evidence_eligible: false
registry_visible: false
maturity_contributing: false
promotion_path: none
note: Exploratory session. Not part of scientific evaluation.
```

PAN-Diagnostik verwendet zusätzlich:

```text
classification: PLAYGROUND_PAN
scientific_evidence: false
evidence_eligible: false
```

Geometriediagnostik verwendet:

```text
classification: PLAYGROUND_GEOMETRY
scientific_evidence: false
```

Kein Playground-Lauf darf direkt in die MHRN Research Registry, die Evidence
Matrix oder die Scientific Maturity eingehen.

Der einzige zulässige Übergang lautet:

```text
Playground observation
→ Research Candidate
→ neue Forschungsfrage
→ Hypothese status: untested
→ Preregistration DRAFT
→ Freeze
→ neuer kanonischer DATA-Lauf
→ Human Review
→ optional EVID
→ unabhängige Replikation
```

---

## 3. PAN-Systemarchitektur

PAN wird nicht als zweiter wissenschaftlicher Kernel neben MHRN geführt,
sondern als optionale Explorationsschicht über dem bestehenden Playground.

Vereinfachtes Schema:

```text
Neuron model
    │
    ├── membrane / adaptation dynamics
    │
    └── PAN state layer Ds
            │
            ├── Health
            ├── Energy
            ├── Information proxy
            ├── Consolidation
            └── Hyperstate
                    │
                    ▼
             population state
                    │
                    ▼
            optional feedback KX

Independent geometry Dg
    │
    ├── x,y,z
    ├── a,b
    ├── connection metric
    └── xyz-only delays
            │
            ▼
         synaptic graph
```

Zustand und Geometrie sind damit getrennte Verträge.

---

## 4. Zustandsraum Ds

### 4.1 Begriff

```text
x_i ∈ R^Ds
```

Der PAN-Zustandsraum beschreibt, **was ein Neuron im Modellzustand ist**.

`Ds` ist konfigurierbar zwischen 5 und 32.

### 4.2 Erste zehn semantische Achsen

| D | Name | Aktueller Status |
|---|---|---|
| D1 | intrinsische Simulationszeit | implementiert |
| D2 | Erregbarkeits-Proxy | implementiert |
| D3 | Plastizitätsaktivität | implementiert |
| D4 | lokaler Informations-/Surprise-Proxy | implementiert, **keine PID** |
| D5 | Health | implementiert |
| D6 | Neuromodulations-Proxy | implementiert |
| D7 | Energie | implementiert |
| D8 | Positionsprojektion | implementiert |
| D9 | Konsolidierungs-Proxy | implementiert |
| D10 | lokale Netzwerkkopplung | implementiert |

D11..D32 bleiben unzugewiesene latente Achsen.

### 4.3 Kritische Grenze bei D4

Der Playground meldet ausdrücklich:

```text
information_axis: local_surprise_proxy_not_PID
pid_status: NOT_IMPLEMENTED
```

D4 ist damit keine Partial Information Decomposition.

Für eine spätere PID-Forschungslinie müssen vor einem kanonischen Lauf
mindestens festgelegt werden:

1. Quellenvariablen,
2. Zielvariable,
3. PID-Formalismus,
4. Estimator,
5. Bias- und Sample-Size-Prüfung,
6. Vergleichsbaselines,
7. Preregistration.

---

## 5. Hypervektoroperationen

PAN stellt explorativ zwei Grundoperationen bereit.

### Binding

- Hadamard-Produkt
- zirkuläre Faltung

### Bundling

Komponentenweises Vorzeichen der Summe einer Population.

Diese Operationen sind technische PAN-Bausteine. Aus ihrer Implementierung
folgt keine wissenschaftliche Aussage über Repräsentationsqualität.

---

## 6. PAN-Neuronen- und Synapsenmechanismen

### 6.1 pan_adex_5d

Das explorative Modell verbindet AdEx-Membrandynamik mit dem PAN-State-Layer.

Es ist kein neues biologisch validiertes Neuronmodell, sondern ein
Playground-Prototyp.

### 6.2 Health

`H_i ∈ [0,1]` beschreibt einen technischen PAN-Lebenszustand.

Health wird unter anderem durch Aktivitätsstress und Energie beeinflusst.

Der Wert ist **kein biologischer Gesundheitsmarker**.

### 6.3 Energie

Ein bounded Energie-Proxy wird durch Aktivität belastet und in Richtung eines
Baseline-Niveaus zurückgeführt.

### 6.4 Spike-Amplitude

Die ausgehende synaptische Wirkung kann mit dem aktuellen Health-Zustand
moduliert werden.

Das ist nicht gleichbedeutend mit einer nachgewiesenen biologischen
Aktionspotential-Amplitudenregel.

### 6.5 Apoptose

Unterschreitet Health die konfigurierte Schwelle, wird das Modellneuron
deaktiviert.

Aktuelle Grenze:

- Apoptose ist implementiert.
- Neurogenese ist **nicht implementiert**.

### 6.6 pan_stp_stdp

Explorative Kombination aus Release-State-Depression/Recovery und
Pair-STDP-naher Gewichtsdynamik.

Sie ist kein kanonischer PAN- oder MHRN-Mechanismus.

---

## 7. Closed Loop

PAN kann den vorherigen Populations-Hyperzustand über eine deterministisch
initialisierte Feedback-Matrix auf zukünftige Neuronströme projizieren.

```text
I_feedback = gain · K · X
```

Der Playground misst unter anderem den mittleren absoluten Feedbackstrom.

Der Mechanismus ist ein experimenteller Closed Loop und **kein validiertes
Weltmodell**.

Aktueller Status:

```text
world_model_status:
exploratory_state_space_only_not_validated_world_model
```

---

## 8. Geometrischer Raum Dg

### 8.1 Trennung von Ds und Dg

```text
state space:      x_i ∈ R^Ds
geometric space:  g_i ∈ R^Dg
```

Ein Beispiel ist daher zulässig:

```text
Ds = 7
Dg = 5
```

ohne die beiden Räume gleichzusetzen.

### 8.2 geometric_5d

Die neue Geometrie lautet:

```text
g_i = (x, y, z, a, b)
```

- `x,y,z ∈ [0,1]`: kartesisch
- `a,b ∈ [0,2π)`: zyklisch

Die beiden zyklischen Koordinaten bilden in der aktuellen Implementierung:

```text
S¹ × S¹
```

also einen Torus.

Eine Klein-Flasche ist **nicht implementiert**.

---

## 9. Geometriemodus mixed_additive

Die additive Metrik ist:

```text
d_mix² = d_xyz²
       + λa (d_a/π)²
       + λb (d_b/π)²
```

Die mathematische Konsequenz ist:

```text
d_mix >= d_xyz
```

Die a/b-Komponenten können den Abstand daher nur vergrößern.

Dieser Modus testet kombinierte Nachbarschaft, aber keine echten
„räumlich weit, topologisch nah“-Shortcuts.

---

## 10. Geometriemodus shortcut_union

Für die Shortcut-Hypothese existiert separat:

```text
d_shortcut = min(d_xyz, d_ab)
```

Damit kann ein Paar verbunden werden, wenn es entweder in xyz oder im
zyklischen a/b-Raum nahe liegt.

Dieser Modus ist eine explizite Modellentscheidung und keine biologische
Tatsache.

---

## 11. Offene Normierungsfrage bei shortcut_union

Diese Frage bleibt **bewusst offen**.

Die aktuelle Implementierung normalisiert die einzelnen zyklischen Distanzen
durch π. Die xyz-Koordinaten liegen in einem Einheitswürfel. Trotzdem besitzen
die beiden zusammengesetzten Distanzräume nicht automatisch exakt dieselbe
Skala.

Dadurch kann eine der beiden Metriken die `min`-Operation systematisch
dominieren.

Zwei methodisch plausible Varianten sind für einen späteren, preregistrierten
Vergleich vorgesehen.

### Variante A — beide Räume auf [0,1] normieren

```text
d = min(
    d_xyz / d_xyz_max,
    d_ab  / d_ab_max
)
```

Für den aktuellen Einheitswürfel wäre beispielsweise:

```text
d_xyz_max = sqrt(3)
```

Die genaue Definition von `d_ab_max` muss zur Gewichtung `λa,λb` passen.

### Variante B — expliziter Gamma-Parameter

```text
d = min(d_xyz_normalized, γ · d_ab_normalized)
```

`γ` steuert dann die relative Bedeutung des topologischen Raums.

### Aktuelle Entscheidung

**Noch keine der beiden Varianten wird als wissenschaftlich bevorzugt.**

Vor einer kanonischen Untersuchung muss die Normierung in der Preregistration
fixiert werden. Eine nachträgliche Wahl anhand des Ergebnisses wäre methodisch
nicht zulässig.

---

## 12. Verbindungswahrscheinlichkeit

Für die geometrischen Modi gilt explorativ:

```text
P(i,j) = p0 exp(-d(i,j)² / (2σ²))    wenn d <= R
       = 0                            sonst
```

Parameter:

- Radius `R`
- Breite `σ`
- Basiswahrscheinlichkeit `p0`
- `λa`
- `λb`
- Geometriemodus

Die tatsächliche Kantenmenge wird zusätzlich durch das Playground-Edge-Budget
begrenzt.

Daher gilt ausdrücklich **nicht**:

> Höhere geometrische Dimension erzeugt automatisch mehr reale Synapsen.

---

## 13. Leitungsverzögerung

Bei `geometric_5d` wird die Leitungsverzögerung ausschließlich aus
`x,y,z` berechnet:

```text
delay_ticks = ceil(d_xyz / velocity_per_tick)
```

Die a/b-Achsen verkürzen keine physische Leitungslänge.

Aktivitätsabhängige Myelinisierung ist noch nicht implementiert:

```text
adm_status: NOT_IMPLEMENTED
```

---

## 14. Geometrische Diagnostik

`result["geometry"]` liefert derzeit:

- geometry dimensions,
- Achsentypen,
- mean out-degree,
- vollständige Out-Degree-Verteilung,
- Moran's I des Out-Degree im xyz-Raum,
- Moran's I der neuronalen Aktivität im xyz-Raum,
- mittlere xyz-Kantendistanz,
- mittlere topologische a/b-Distanz,
- mittlere additive Mischdistanz,
- xyz-basierte Delay-Statistik,
- Apoptosepositionen, wenn PAN aktiv ist.

Die Kanten werden zusätzlich klassifiziert als:

```text
spatial_only
topological_only
both
neither
```

und:

```text
topological_shortcut_fraction
```

wird deskriptiv ausgewiesen.

Diese Größe ist **ohne gematchte 3D-Baseline noch kein wissenschaftlicher
Effektnachweis**.

---

## 15. Erforderliche geometric_3d-Baseline

Für einen späteren Test von
`PAN-CANDIDATE-TOPOLOGICAL-SHORTCUTS` ist eine gematchte 3D-Kontrolle
erforderlich.

### Kontrollvertrag

Die spätere Baseline soll mindestens fixieren:

- gleiche Neuronenzahl,
- identische xyz-Koordinaten,
- gleiche Seeds,
- gleiche Stimuli,
- gleiche Neuronen- und Synapsenmodelle,
- gleicher Radius,
- gleiches σ,
- gleiches p0,
- gleiches Edge-Budget,
- gleiche Delay-Regel,
- keine a/b-Komponenten.

Wichtig ist außerdem eine **candidate-edge diagnostic vor dem Edge-Budget**.
Sonst kann ein fixes Budget zusätzliche mögliche Shortcuts verdecken.

### Primärer Strukturvergleich

Vorgesehen sind mindestens:

- zusätzliche Kandidatenkanten vor Budgetbegrenzung,
- topological-shortcut fraction,
- mean path length,
- clustering coefficient,
- connected components,
- degree distribution.

### Funktionale Messgrößen

Eine spätere Preregistration muss getrennt festlegen, ob zusätzlich
Netzwerkfunktion untersucht wird, beispielsweise:

- Recovery nach Perturbation,
- Rate-Stabilität,
- Synchronitätsdrift,
- Persistenz,
- reproduzierbare Seed-Effekte.

Damit bleibt die Strukturhypothese von einer möglichen Funktionshypothese
getrennt.

---

## 16. Nachbarschaftsskalierung

Für eine kontinuierliche euklidische d-Kugel wächst das Volumen bei festem d
proportional zu `r^d`.

Für ein diskretes Netzwerk folgt daraus jedoch **keine universelle Tabelle**
konkreter Nachbarzahlen.

Diese hängen unter anderem ab von:

- Gitter oder Punktprozess,
- Metrik,
- Radiusdefinition,
- Randbedingungen,
- Dichte,
- probabilistischer Verbindungsregel,
- Edge-Budget.

PAN misst diese Größen daher im Playground, statt feste Werte vorauszusetzen.

---

## 17. Aktuelle PAN-Diagnostik insgesamt

### Spike/Zeit

- ISI
- CV(ISI)
- Burst-Proxy
- First-Spike-Latency
- Persistence
- Propagation Proxy

### Populationsdynamik

- Synchrony Index
- Fano Factor
- Frequenzspektrum

### Netzwerk

- Degree Distribution
- Hubs
- Clustering
- Mean Path Length
- Components
- Reciprocal Edges
- Three-Cycle Proxy
- Edge-Distance Distribution

### Plastizität

- Weight Change
- Potentiation
- Depression
- Saturation
- Structural Additions/Removals

### Dimensionen

- PCA Explained Variance
- Effective Dimensionality
- Participation Ratio
- Dimension Variance
- N-D Occupancy ohne Qualitätswertung

### PAN

- Health
- Energy
- Alive/Apoptotic neurons
- Hyperstate population vector
- Population bundle
- Feedback magnitude

### Geometrie

- Out-Degree Spatial Autocorrelation
- Activity Spatial Autocorrelation
- Spatial/Topological Edge Classes
- Topological Shortcut Fraction
- xyz-only Delay Statistics
- Apoptosis Positions

---

## 18. Research Candidates 1–18

Alle Kandidaten tragen:

```text
status: DRAFT_IDEA_NOT_PREREGISTERED
```

### 1 — Homeostatic Survival

**Frage:** Ändert health-modulierte Homeostase die Recovery nach gematchten
Perturbationen?

### 2 — Hyperstate Feedback

**Frage:** Verändert Hyperstate-Feedback Stabilität oder Recovery gegenüber
einem gematchten Netzwerk ohne Feedback?

### 3 — Information Axis

**Frage:** Kann der aktuelle Surprise-Proxy später durch ein formal definiertes
Informationsmaß oder PID ersetzt werden?

### 4 — Aging

**Frage:** Erzeugen Health-, Energie- und Apoptose-Dynamiken reproduzierbare
Netzwerkübergänge unter gematchtem Stress?

### 5 — Geometric Scaling

**Frage:** Wie skaliert Kandidaten- und realisierter Out-Degree mit der
geometrischen Dimension unter explizit gematchten Randbedingungen?

### 6 — Topological Shortcuts

**Frage:** Erzeugen a/b-Achsen zusätzliche Shortcut-Kanten und verändern sie
Path Length oder Clustering relativ zu einem gematchten xyz-Kontrollgraphen?

### 7 — Activity-Dependent Positioning

**Frage:** Kann eine vorab definierte Aktivitäts- oder Informationsregel
stabile selbstorganisierte geometrische Cluster erzeugen?

Dieser Mechanismus ist noch nicht implementiert.

### 8 — Spatial Lifecycle

**Frage:** Kann eine später separat implementierte Neurogenese zusammen mit
Apoptose eine räumliche Dichte unter definierten Stress- und
Replacement-Regeln stabilisieren?

Neurogenese ist noch nicht implementiert.

### 9 — Gate Emergence

**Frage:** Bleiben aus Einstellungen abgeleitete Gatter-Schemata unter
gematchten Parameter-Sweeps und Seeds verhaltensstabil?

### 10 — Dual-Mode Consistency

**Frage:** Unter welchen begrenzten Bedingungen stimmen interleaved
Event/Continuous-Läufe mit Continuous-only-Referenzen innerhalb einer
vorab definierten Toleranz überein?

### 11 — Generative Growth

**Frage:** Erzeugt begrenztes ereignisgetriebenes Wachstum reproduzierbare
Topologieänderungen unter gematchten Aktivitätsverläufen?

### 12 — Memory Scaling

**Frage:** Wie skaliert gemessener Hot-State-Speicher mit Neuronen,
Kanten und PAN-Zustandsdimensionen?

### 13 — Hardware-Native Emergence

**Frage:** Ändert eine später gemessene register-native CUDA-Implementierung
Dynamik oder Ressourcenskalierung gegenüber dem Referenzbackend?

### 14 — Behavioral Emergence

**Frage:** Generalisiert reward-moduliertes Policy-Lernen auf neue Inputs,
ohne exakte externe Payloads als Fakten zu speichern?

### 15 — Hybrid Cognition

**Frage:** Liefert die Kopplung von PAN an die bestehenden
Gateway-/Neural-Symbiosis-Schnittstellen messbare Task-Effekte gegenüber
fixem Routing?

### 16 — Layer Emergence

**Frage:** Entwickeln plastische Layer-Gains oder Verbindungen reproduzierbare
funktionale Spezialisierung über die initiale Schichtzuordnung hinaus?

### 17 — Mode-Switch Consistency

**Frage:** Bewahrt der Wechsel zwischen sparse Event- und full Tick-Ausführung
die deklarierte Shared-State-Integrität und wie groß sind die
Trajektorienabweichungen?

### 18 — Hybrid Performance

**Frage:** Reduziert HYBRID_AUTO gemessene Laufzeit oder Energie gegenüber
beiden festen Modi unter gematchten Workloads?

Alle 18 bleiben `DRAFT_IDEA_NOT_PREREGISTERED`. Keine dieser Ideen wird
durch Playground-Ausführung automatisch zu DATA oder EVID.

---

## 19. Literaturbefund

### Hyperdimensionale / spikende Repräsentation

- Orchard, Furlong & Simone (2024): Spiking Phasors / FHRR.
  DOI: `10.1162/neco_a_01693`
- Ahmed, Samiei & Nozari (2026): räumliche und zeitliche Hypervektoren.
  DOI: `10.3389/fncom.2026.1885975`
- Olin-Ammentorp (2026): Phase State Space Models, arXiv:`2608.07754`.

### PID / infomorphe Netze

- Makkeh et al. (2025): lokale informationstheoretische Zielfunktionen.
  DOI: `10.1073/pnas.2408125122`

### Homeostase

- Naudé et al. (2013): Homeostatic Intrinsic Plasticity.
  DOI: `10.1523/JNEUROSCI.0870-13.2013`
- Gao et al. (2025): Multi-Scale Neural Homeostasis.
  DOI: `10.1016/j.aehs.2025.02.002`

### Neurogenese / Apoptose

- Chow, Wick & Riecke (2012): aktivitätsabhängiges Überleben / Neurogenese.
  DOI: `10.1371/journal.pcbi.1002398`

### Aging Transition

- Cao et al. (2026): explosive Aging Transitions in FHN-Netzwerken.
  DOI: `10.7498/aps.75.20260125`

### Spike-Amplitude / SADP

- Mahata et al. (2023): Spike-Amplitude-Dependent Plasticity.
  DOI: `10.1063/5.0179314`
- Bej et al. (2026): **anderes** SADP =
  Spike Agreement Dependent Plasticity.
  DOI: `10.1016/j.neunet.2026.108809`

### Geometrische Netzwerke

- Barthélemy (2011): Spatial Networks.
  DOI: `10.1016/j.physrep.2010.11.002`
- Krioukov et al. (2010): Hyperbolic Geometry of Complex Networks.
  DOI: `10.1103/PhysRevE.82.036106`
- Lin et al. (2024): Drosophila whole-brain connectome statistics.
  DOI: `10.1038/s41586-024-07968-y`
- Constantinescu et al. (2016): grid-like code in a 2D conceptual space.
  DOI: `10.1126/science.aaf0941`

---

## 20. Wissenschaftliche Korrekturen aus dem Reviewprozess

Folgende frühere Aussagen wurden ausdrücklich **nicht** übernommen oder
korrigiert.

### 20.1 Additive Metrik erzeugt keine Shortcuts

Korrigiert durch Trennung in:

- `mixed_additive`
- `shortcut_union`

### 20.2 a/b erzeugen Torus, nicht automatisch Klein-Flasche

Aktueller Status:

```text
topological_manifold: torus_S1_x_S1
klein_bottle_status: NOT_IMPLEMENTED
```

### 20.3 Keine universelle Nachbartabelle

Konkrete Nachbarzahlen werden gemessen und nicht aus einer universellen Tabelle
übernommen.

### 20.4 Keine universelle Small-World-Schwelle d >= 3

Eine solche allgemeine Schwelle ist im aktuellen PAN-Kontext nicht etabliert.

### 20.5 Keine belegte Drosophila-Dimension 4–6

Der Drosophila-Befund stützt räumliche Abhängigkeit von Konnektivität, nicht
die zuvor behauptete effektive Dimension 4–6.

### 20.6 Constantinescu ist kein Nachweis biologischer 5D-Grid-Cells

Die Arbeit untersucht einen grid-like Code in einem zweidimensionalen
konzeptuellen Raum.

### 20.7 D4 ist keine PID

Bis zu einer formal spezifizierten PID-Linie bleibt D4 ein Surprise-Proxy.

---

## 21. Was aktuell als Ergebnis bezeichnet werden darf

### Implementierungsergebnisse

Es ist zulässig zu sagen:

- PAN ist als isolierte Playground-Schicht implementiert.
- Ds und Dg sind technisch getrennt.
- 5..32D PAN-Hyperzustände können simuliert werden.
- geometric_5d ist implementiert.
- zwei Geometriemodi können explorativ verglichen werden.
- xyz-basierte Delays sind implementiert.
- PAN- und Geometriediagnostik werden ausgegeben.
- acht Research Candidates sind explizit formuliert.
- Research-/EVID-Grenzen werden technisch erzwungen.

### Noch keine wissenschaftlichen PAN-Ergebnisse

Nicht zulässig ist derzeit:

- PAN verbessere Lernen,
- PAN verbessere Robustheit,
- 5D sei besser als 3D,
- a/b-Shortcuts verbesserten Small-World-Eigenschaften,
- Health oder Apoptose seien funktional vorteilhaft,
- PID sei implementiert,
- PAN bilde ein validiertes Weltmodell,
- PAN sei formal nachgewiesen neu.

Diese Fragen benötigen neue kanonische Experimente.

---

## 22. Neuheitsstatus

Die zulässige Formulierung bleibt:

> Die geprüfte Literatur enthält relevante Vorarbeiten für die einzelnen
> Komponenten. In der gezielten Suche wurde keine einzelne Publikation
> identifiziert, die die aktuell skizzierte PAN-Kombination aus semantischem
> Hyperzustand, Health/Lifecycle, variablem Spike-Effekt,
> informationstheoretischer Zielperspektive, Closed Loop und unabhängiger
> xyz+toroidaler Geometrie in derselben Modellarchitektur realisiert. Das ist
> ein Recherchebefund und kein Beweis weltweiter Neuheit.

Ein formaler Prior-Art- oder systematischer Review steht aus.

---

## 23. Empfohlene Validierungsreihenfolge

1. statische `geometric_5d`-Geometrie technisch stabilisieren,
2. Normalisierung von `shortcut_union` vorab entscheiden,
3. gematchte `geometric_3d`-Kontrolle spezifizieren,
4. `TOPOLOGICAL-SHORTCUTS` als erste Geometrie-Preregistration formulieren,
5. Strukturhypothese vor Funktionshypothese testen,
6. erst danach Activity-Dependent Positioning untersuchen,
7. PID separat spezifizieren und validieren,
8. Neurogenese erst nach statischer Lifecycle-Baseline ergänzen.

Diese Reihenfolge verhindert, dass mehrere neue Mechanismen gleichzeitig
eingeführt werden und ihre Effekte nicht mehr trennbar sind.

---

## 24. Dokumentationskarte

Weitere Detailseiten:

- `docs/playground/pan.md` — PAN-Governance und Kernvertrag
- `docs/playground/PAN_5D_RESEARCH_CONTEXT.md` — externer Forschungsstand
- `docs/playground/geometry.md` — geometrischer Raum
- `docs/playground/GLOSSARY.md` — Glossar
- `src/playground/README.md` — Implementierungsübersicht

Diese Gesamtdokumentation ist die zentrale Einstiegsseite für PAN im
Playground.


---

## 25. Input, Output und neuronales I/O-Interface

PAN besitzt jetzt im Playground eine eigene Input-/Output-Grenze nach dem
bereits postulierten MHRN Gateway Neural Interface.

Die Trennung lautet:

```text
Payload != Neural Representation
```

und:

```text
Codec != GatewayTopology != GatewayLearning
```

### Input

Der exakte Payload bleibt in einem BoundaryFrame außerhalb des SNN.

Verfügbare Referenzcodecs:

- `population_latency_v1`
- `vector_population_v1`
- `sparse_symbol_v1`

Noch nicht produktiv:

- `bit_exact_v1`
- `hash_fingerprint_v0` als Negativkontrolle

Die neuronale Projektion erfolgt auf dedizierte Rollen:

- `AFFERENT`
- `GATEWAY_AFFERENT`

### Output

Output wird ausschließlich aus dedizierten:

- `EFFERENT`
- `GATEWAY_EFFERENT`

Populationen gelesen.

Aktuelle Decoder:

- `population_rate_v1`
- `sparse_symbol_v1`

Fehlende Aktivität erzeugt keinen erfundenen Inhalt, sondern
`INSUFFICIENT_ACTIVITY`.

### Query-/Response-Lifecycle

```text
QUERY -> WAIT -> RESPONSE
```

oder:

```text
QUERY -> WAIT -> TIMEOUT
```

Query und Response bleiben durch Richtung, Phase, `correlation_id` und
Provenienz unterscheidbar.

### Exakte Payload-Grenze

Der Rohpayload erscheint nicht in:

- `result["config"]`,
- `result["neural_io"]`,
- persistierten Playground-Sessions.

Persistiert bzw. ausgegeben werden nur:

- SHA-256,
- Payload-Größe,
- Content-Type,
- Provenienz,
- Codec-/Layout-Verträge,
- SpikeFrame-Metadaten.

### Verhältnis zu NetworkAreaAdapter

Ein `PlaygroundIOAreaAdapter` erfüllt den vorhandenen
`NetworkAreaAdapter`-Protocol. Er bleibt vom neuronalen Codec getrennt und hat
keinen direkten Zugriff auf den MHRN-Core.

### Kein Tool-/Actuator-Execution Path

Im Playground gilt:

```text
tool_plane_execution = false
actuator_execution   = false
```

Das Ergebnis endet bei `DecodeResult`.

### Shared 100 × 100 Layout

Der postulierte gemeinsame logische Query-/Response-Raum von 100 × 100 bzw.
10.000 Kanälen ist als Architekturmetadatum dokumentiert, aber wegen der
aktuellen Playground-Grenze von 1.024 Neuronen nicht physisch allokiert.

Status:

```text
EXPERIMENTAL_CONCEPT_NOT_ALLOCATED_IN_PLAYGROUND
```

Detaildokumentation:

- `docs/playground/neural_io.md`
- `docs/playground/neural_io_examples.md`
