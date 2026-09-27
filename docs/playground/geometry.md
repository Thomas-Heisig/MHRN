# PAN / MHRN Playground — Geometrischer Raum Dg

**Status:** PLAYGROUND_GEOMETRY · explorativ · nicht kanonisch · keine EVID

Diese Seite beschreibt den geometrischen Raum getrennt vom PAN-Zustandsraum.

## 1. Zwei unabhängige Dimensionsbegriffe

Der Playground unterscheidet ausdrücklich:

- **Zustandsraum Ds**: interne Eigenschaften eines Neurons, z. B. Erregbarkeit,
  Plastizität, Health, Energie oder Konsolidierung.
- **Geometrischer Raum Dg**: Position und daraus abgeleitete Nachbarschaft /
  Verbindbarkeit.

Ein PAN-Lauf kann beispielsweise `Ds=7` und gleichzeitig `Dg=5` verwenden.
Die Zahlen bezeichnen unterschiedliche Verträge.

## 2. geometric_5d

Die neue Topologie `geometric_5d` verwendet:

```text
g_i = (x, y, z, a, b)
```

- `x,y,z ∈ [0,1]`: kartesische Koordinaten.
- `a,b ∈ [0,2π)`: unabhängige zyklische Koordinaten.

Zwei unabhängige zyklische Koordinaten bilden zunächst einen
**Torus S¹ × S¹**. Eine Klein-Flasche benötigt eine verdrehte Identifikation
und ist im Playground derzeit **nicht implementiert**.

## 3. Distanzen

Die kürzeste zyklische Distanz lautet:

```text
d_cycle(a_i,a_j) = min(|a_i-a_j|, 2π-|a_i-a_j|)
```

Die topologischen Komponenten werden auf `[0,1]` normalisiert.

### 3.1 mixed_additive

```text
d_mix² = d_xyz²
       + λ_a (d_a/π)²
       + λ_b (d_b/π)²
```

Dieser Modus implementiert die wörtliche additive Mischmetrik.

**Wichtig:** `d_mix >= d_xyz`. Deshalb kann diese Metrik keine Verbindung
erzeugen, die allein wegen `a,b` „topologisch nah“ ist, obwohl sie in xyz weit
entfernt liegt.

### 3.2 shortcut_union

Um die eigentliche Shortcut-Hypothese separat testen zu können, besitzt der
Playground zusätzlich:

```text
d_shortcut = min(d_xyz, d_ab)
```

Eine Kante kann damit zugelassen werden, wenn die Neuronen entweder räumlich
oder in den zyklischen Achsen nahe liegen.

Dieser zweite Modus ist eine **explorative Modellentscheidung**, nicht die
Folge der additiven Gleichung.


### 3.3 Open normalization question

The `shortcut_union` mode still has an unresolved scale-comparability issue.
Even after normalizing each cyclic component by π, the composed xyz and a/b
distances do not automatically share an identical scale.

Two preregistration-worthy alternatives are retained as design options:

```text
A) d = min(d_xyz / d_xyz_max, d_ab / d_ab_max)
```

or

```text
B) d = min(d_xyz_normalized, gamma * d_ab_normalized)
```

with an explicit `gamma >= 0`.

No option is currently preferred. The choice must be fixed before a canonical
comparison and must not be selected retrospectively from observed results.

A later topological-shortcut experiment also requires a matched
`geometric_3d` control using identical xyz coordinates, seeds, radius,
sigma, p0, neuron/synapse models, delay rule and edge budget.

## 4. Verbindungswahrscheinlichkeit

Für beide Modi gilt:

```text
P(i,j) = p0 exp(-d(i,j)² / (2σ²))   für d <= R
       = 0                           sonst
```

Parameter:

- `R`: Radius
- `σ`: Breite
- `p0`: maximale Basiswahrscheinlichkeit
- `λa, λb`: Gewichtung der zyklischen Komponenten
- `geometry_mode`: `mixed_additive` oder `shortcut_union`

Die resultierende Kantenmenge wird zusätzlich durch das allgemeine
Playground-`edge_budget` begrenzt.

## 5. Leitungsverzögerung

Die Verzögerung verwendet absichtlich **nur xyz**:

```text
delay_ticks = ceil(d_xyz / velocity_per_tick)
```

Die zyklischen Achsen `a,b` verändern nicht die physische Leitungslänge.

Das ist derzeit nur ein statischer Geschwindigkeitsparameter.
Aktivitätsabhängige Myelinisierung (ADM) ist **nicht implementiert**.

## 6. Diagnostik

Ein `geometric_5d`-Lauf liefert `result["geometry"]` mit:

- out-degree und mittlerem out-degree,
- Moran's I für out-degree im xyz-Raum,
- Moran's I für Aktivitätsraten im xyz-Raum,
- mittlerer xyz-Distanz,
- mittlerer toroidaler a/b-Distanz,
- mittlerer additiver Mischdistanz,
- Kantenklassen:
  - `spatial_only`
  - `topological_only`
  - `both`
  - `neither`
- topological-shortcut fraction,
- Delay-Metadaten,
- Apoptosepositionen, falls PAN aktiv ist.

Es gibt keine Gut/Schlecht-Farbskala und keinen Qualitätswert.

## 7. Was teilweise bereits vorhanden war

Vor dieser Erweiterung enthielt der Playground bereits:

- native MHRN-5D-Koordinaten,
- generische N-D-Topologien,
- N-D-Distanzgraphen,
- k-nearest-neighbour,
- Degree-, Clustering-, Path- und Distanzdiagnostik,
- PAN-Health/Apoptose,
- PAN-Hyperzustände 5..32D.

Neu hinzu kommt die **explizite Trennung** von Ds und Dg sowie die spezielle
xyz+toroidal-Geometrie.

## 8. Nachbarschaft und Dimension

Für kontinuierliche d-dimensionale euklidische Kugeln wächst das Volumen bei
festem d proportional zu `r^d`. Für diskrete Gitter hängt die konkrete
Nachbarzahl aber von Gitter, Metrik, Radiusdefinition und Randbedingungen ab.

Darum verwendet die Dokumentation **keine universelle Tabelle** mit festen
Nachbarzahlen.

Ebenso folgt aus höherer Dimension nicht automatisch eine höhere realisierte
Synapsenzahl: `p0`, `σ`, Radius, Punktdichte und Edge-Budget bestimmen die
tatsächliche Konnektivität.

## 9. Forschungsstand

### Räumliche Netzwerke

Barthélemy (2011) fasst räumlich eingebettete Netzwerke als etabliertes Feld
zusammen. Räumliche Kosten und Distanzen können Netzwerkstruktur stark formen.

DOI: `10.1016/j.physrep.2010.11.002`

### Hidden / hyperbolische Geometrie

Krioukov et al. (2010) zeigen, dass hyperbolische Hidden-Space-Modelle zentrale
Eigenschaften komplexer Netzwerke wie Degree-Heterogenität und Clustering
erzeugen können.

DOI: `10.1103/PhysRevE.82.036106`

Diese Arbeit ist keine biologische Validierung der PAN-Achsen `a,b`.

### Drosophila-Connectome

Whole-brain-Drosophila-Analysen berichten einen Zusammenhang zwischen
räumlicher Distanz angenäherter Axon-/Dendriten-Arbors und
Verbindungswahrscheinlichkeit.

DOI: `10.1038/s41586-024-07968-y`

Die in der Ausgangsskizze genannte Aussage, das Drosophila-Connectome habe eine
etablierte „effektive Dimension zwischen 4 und 6“, wird im Playground ausdrücklich
**nicht als belegt übernommen**.

### Grid-like conceptual coding

Constantinescu, O'Reilly und Behrens (2016) zeigen grid-like Coding in einem
**zweidimensionalen konzeptuellen Raum**.

DOI: `10.1126/science.aaf0941`

Das ist interessante Evidenz für nicht-physische Koordinatenrepräsentation,
aber **kein Nachweis biologischer 5D-Grid-Cells**.

## 10. Nicht übernommene Behauptungen

Der Playground behauptet derzeit nicht:

- dass es eine universelle Small-World-Schwelle bei `d >= 3` gibt,
- dass 5D die „kleinste optimale“ geometrische Dimension sei,
- dass Drosophila einen gesicherten effektiven 4–6D-Raum besitzt,
- dass `a,b` biologisch validierte Koordinaten sind,
- dass `shortcut_union` ein biologischer Mechanismus ist,
- dass höhere Dg automatisch bessere oder dichtere Netzwerke erzeugt.

Diese Punkte können höchstens als testbare Hypothesen formuliert werden.

## 11. Noch nicht implementiert

Folgende Teile bleiben absichtlich offen:

- activity-dependent positioning,
- PID-gesteuerte Positionskräfte,
- dynamische Positionsverschiebung,
- Neurogenese mit Positionsauswahl,
- adaptive Myelinisierung,
- Klein-Flaschen-Identifikation,
- echte Kopplung `x_state ⊕ g_geometry` als wissenschaftlicher Mechanismus.

PAN verwendet weiterhin nur seine bereits vorhandene skalare
Positionsprojektion als explorativen Zustandsinput.

## 12. Research Candidates

Die Playground-Kandidaten enthalten zusätzlich:

5. Geometric Scaling  
6. Topological Shortcuts  
7. Activity-Dependent Positioning  
8. Spatial Lifecycle / Apoptosis-Neurogenesis Balance

Alle tragen:

```text
status: DRAFT_IDEA_NOT_PREREGISTERED
```

und gehen nicht automatisch in die MHRN Research Registry ein.


**Methodische Grenze:** keine universelle Small-World-Schwelle wird behauptet.
