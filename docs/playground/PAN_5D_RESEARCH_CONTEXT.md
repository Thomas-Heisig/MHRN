# PAN-5D im MHRN Playground: Forschungsstand, Integration und Grenzen

**Status:** Playground-Dokumentation · explorativ · nicht kanonisch · keine EVID

Diese Seite beschreibt, wie der PAN-5D-Entwurf im MHRN Playground zu
bestehenden Forschungsrichtungen in Beziehung steht. Sie ist **keine
Neuheitsbescheinigung** und **keine wissenschaftliche Evidenz für PAN**.

Der aktuelle, methodisch zulässige Satz lautet:

> Eine gezielte Literaturprüfung identifiziert etablierte oder publizierte
> Vorarbeiten für viele einzelne Bausteine. In dieser Prüfung wurde keine
> einzelne Arbeit gefunden, die alle PAN-5D-Bausteine in genau der hier
> beschriebenen Kopplung zusammenführt. Das ist ein **Recherchebefund**, kein
> Beweis weltweiter Neuheit.

## 1. Was PAN-5D im Playground ist

PAN-5D ist eine optionale Explorationsschicht über dem bestehenden MHRN
Playground-Simulator. Sie kombiniert derzeit:

- spikende Neuronenmodelle, darunter ein exploratives `pan_adex_5d`,
- 5..32-dimensionale Hyperzustände,
- semantisch benannte Zustandsachsen,
- Health-, Energie- und Konsolidierungs-Proxys,
- variable Spike-Amplitude,
- optionales Hyperstate-Feedback,
- STP/STDP-nahe explorative Synapsendynamik,
- einen bounded Aging-/Apoptose-Zustand,
- explizite Forschungs-Kandidaten ohne Registry-Promotion.

Die Implementierung ist absichtlich modular. PAN kann mit und ohne Closed Loop,
mit verschiedenen Neuronenmodellen und mit unterschiedlichen Topologien
betrieben werden.

## 2. Was die Forschung bereits trägt

### 2.1 Hyperdimensionale Repräsentation und Spikes

Orchard, Furlong und Simone zeigen 2024 eine spikende Implementierung von
Fourier Holographic Reduced Representations (FHRR). Die Phase eines komplexen
Hypervektorelements wird als Spike-Zeit innerhalb eines Zyklus kodiert. Das
stützt die allgemeine Idee, HDC/VSA-Operationen in spikenden Systemen
darzustellen.

**Quelle:** Orchard et al., *Neural Computation* 36(9), 2024.  
DOI: `10.1162/neco_a_01693`

Olin-Ammentorp beschreibt 2026 Phase State Space Models mit
Resonate-and-Fire-Neuronen, rekurrentem Gedächtnis und explizitem Bezug zu
hyperdimensionalem Computing. Der aktuelle Playground behandelt diese Arbeit
als jüngere externe Referenz, nicht als Beleg für PAN.

**Quelle:** arXiv:`2608.07754`.

Ahmed, Samiei und Nozari verwenden 2026 räumliche und zeitliche Hypervektoren,
um neuronale Populationsaktivität in einen hochdimensionalen Raum abzubilden.

**Quelle:** *Frontiers in Computational Neuroscience* 20 (2026).  
DOI: `10.3389/fncom.2026.1885975`

**PAN-Lücke:** Diese Arbeiten etablieren nicht die spezifische semantische
PAN-Achsenbelegung mit Health, Energie, Plastizität und Informations-Proxy.

### 2.2 PID und infomorphe Lernregeln

Makkeh et al. publizieren 2025 ein Framework lokaler,
informationstheoretischer Zielfunktionen auf Basis partieller
Informationszerlegung.

**Quelle:** *PNAS* 122(10):e2408125122.  
DOI: `10.1073/pnas.2408125122`

Das ist eine wichtige Grundlage für spätere PAN-Fragen. Der aktuelle
Playground implementiert **keine PID**.

D4 heißt daher ausdrücklich:

```text
information_axis: local_surprise_proxy_not_PID
pid_status: NOT_IMPLEMENTED
```

Eine spätere PID-Linie benötigt vor einem Experiment:

1. definierte Quellenvariablen,
2. definierte Zielvariable,
3. Wahl des PID-Formalismus und Estimators,
4. Bias-/Sample-Size-Prüfung,
5. Preregistration,
6. neue kanonische DATA-Läufe.

### 2.3 Multi-Scale-Homeostase

Naudé et al. untersuchen 2013 homeostatische intrinsische Plastizität in
rekurrenten biologischen Netzwerkmodellen und deren dynamische Auswirkungen.

**Quelle:** *Journal of Neuroscience* 33(38), 15032-15043.  
DOI: `10.1523/JNEUROSCI.0870-13.2013`

Ein Review von 2025 ordnet neuronale Homeostase explizit über molekulare,
zelluläre und Netzwerk-Skalen ein.

**Quelle:** *Advanced Exercise and Health Science* 2(1), 2025.  
DOI: `10.1016/j.aehs.2025.02.002`

**PAN-Lücke:** Die Playground-Zeitskalen sind noch eine bounded technische
Approximation. Sie sind weder aus diesen Arbeiten abgeleitet noch biologisch
validiert.

### 2.4 Neurogenese und aktivitätsabhängige Apoptose

Chow, Wick und Riecke zeigen in einem Olfactory-Bulb-Modell, dass persistente
Neurogenese zusammen mit aktivitätsabhängigem Überleben bzw. Entfernen
inhibitorischer Interneurone die Netzstruktur adaptiv verändern und ähnliche
Stimulusrepräsentationen dekorrelieren kann.

**Quelle:** *PLoS Computational Biology* 8(3):e1002398, 2012.  
DOI: `10.1371/journal.pcbi.1002398`

**PAN-Lücke:** PAN verwendet aktuell einen kontinuierlichen Health-Zustand und
eine bounded Apoptose-Schwelle, aber noch keine echte Neurogenese-Lebenszyklus-
Replikation dieser Literatur.

### 2.5 Aging Transition

Cao et al. untersuchen 2026 explosive Aging Transitions in global gekoppelten
FitzHugh-Nagumo-Neuronen mit höherwertigen Interaktionen. Die Arbeit analysiert
unter anderem Hysterese, Mischzustände und Netzwerk-Resilienz.

**Quelle:** *Acta Physica Sinica* 75(12):120002, 2026.  
DOI: `10.7498/aps.75.20260125`

**PAN-Lücke:** Ein Netzwerk-Aging-Übergang ist nicht dasselbe wie der
individuelle PAN-Health-Wert eines Neurons. Die beiden Konzepte dürfen erst
nach einer formal definierten Abbildung miteinander verglichen werden.

### 2.6 Spike-Amplitude-Dependent Plasticity

Neuromorphe Memristor-Arbeiten zeigen, dass die Amplitude elektrischer Pulse
synaptische Zustandsänderungen modulieren kann. Beispielsweise demonstrieren
Mahata et al. Spike-Amplitude-Dependent Plasticity in einem
InGaZnO-basierten Memristor.

**Quelle:** *Journal of Chemical Physics* (2023).  
DOI: `10.1063/5.0179314`

Das stützt einen Hardware-/Device-Kontext für amplitudenabhängige
Plastizität. Es beweist **nicht**, dass die variable PAN-Spike-Amplitude eine
biologisch korrekte oder leistungssteigernde Netzwerkeigenschaft ist.

### 2.7 Achtung: zwei verschiedene SADP-Begriffe

In der Literatur existieren mindestens zwei unterschiedliche Verwendungen des
Kürzels **SADP**:

- **Spike-Amplitude-Dependent Plasticity**: Gewichtsänderung abhängig von
  Puls-/Spike-Amplitude, häufig in neuromorphen Bauelementen.
- **Spike Agreement Dependent Plasticity**: Lernregel auf Basis der
  Übereinstimmung von prä- und postsynaptischen Spike-Zügen.

Bej et al. beschreiben 2026 die zweite Bedeutung in *Neural Networks*.

DOI: `10.1016/j.neunet.2026.108809`

PAN-Dokumentation verwendet deshalb nach Möglichkeit die ausgeschriebenen
Bezeichnungen und nicht das mehrdeutige Kürzel allein.

## 3. Was derzeit nicht als etabliert gelten darf

Folgende Aussagen sind **noch keine wissenschaftlich bestätigten
PAN-Ergebnisse**:

- semantische PAN-Achsen seien einer generischen HDC-Repräsentation überlegen,
- Health (H_i) verbessere Robustheit oder Lernen,
- Apoptose im PAN-System verbessere Generalisierung,
- Hyperstate-Feedback (KX) verbessere Closed-Loop-Stabilität,
- variable Spike-Amplitude verbessere PAN-Lernen,
- D4 entspreche PID,
- PAN bilde ein validiertes Weltmodell,
- 5D sei gegenüber 2D/3D/N-D überlegen,
- die Gesamtintegration sei nach strengem Prior-Art-Standard nachgewiesen neu.

Diese Punkte sind Forschungsfragen.

## 4. Aktuelle Integrationsmatrix

| Baustein | Externe Vorarbeit | Playground-Status | Wissenschaftlicher Status |
|---|---|---|---|
| Spiking + HDC | Orchard et al. 2024 | Hyperstate 5..32D | explorativ |
| Phase/HDC-Rekurrenz | Olin-Ammentorp 2026 | Closed-Loop-Option | explorativ |
| Semantische Hyperachsen | keine direkte Entsprechung in geprüften Quellen | implementiert | Hypothese |
| PID-Lernen | Makkeh et al. 2025 | nicht implementiert | offen |
| Multi-Scale-Homeostase | Naudé 2013; Review 2025 | bounded Approximation | nicht validiert |
| Health (H_i) | indirekte Verwandtschaft | implementiert | Hypothese |
| Apoptose | Chow et al. 2012 | Schwellenmodell | explorativ |
| Neurogenese | Chow et al. 2012 | noch nicht implementiert | offen |
| Aging Transition | Cao et al. 2026 | Health/Aging-Proxys | keine Gleichsetzung |
| Spike-Amplitude | Memristor-Literatur | PAN-Amplitudenfaktor | explorativ |
| Spike Agreement Plasticity | Bej et al. 2026 | nicht gleich PAN-STP/STDP | externe Alternative |
| PAN-Gesamtintegration | keine Entsprechung in gezielter Suche identifiziert | Playground-Prototyp | Neuheit unbewiesen |

## 5. Neuheitsgrad: zulässige Formulierung

Nicht zulässig:

> PAN-5D ist bewiesenermaßen neu und wurde noch nie erforscht.

Zulässig:

> Die geprüfte Literatur enthält relevante Vorarbeiten für die einzelnen
> Komponenten. In der gezielten Suche wurde keine einzelne Publikation
> identifiziert, die semantische Hyperzustände, PID-orientierte lokale
> Informationsziele, kontinuierlichen Health-Zustand, Apoptose/Aging,
> variable Spike-Amplitude und hyperdimensionales Closed-Loop-Feedback in
> derselben Modellarchitektur kombiniert. Eine formale Prior-Art- oder
> systematische Review-Prüfung steht aus.

## 6. Erfolgsaussichten: keine Bewertung, sondern testbare Teilfragen

Statt einen Gesamterfolg vorwegzunehmen, wird PAN modular geprüft.

### Achse A — Hyperstate

Vergleich:

- gleiche Neuronen,
- gleiche Topologie,
- gleiche Seeds,
- Hyperstate-Feedback an/aus.

Messgrößen:

- Recovery nach Perturbation,
- Aktivitätsstabilität,
- Rate-/Synchronitätsdrift,
- Reproduzierbarkeit über Seeds.

### Achse B — Health und Apoptose

Vergleich:

- Health aktiv / konstant,
- Apoptose aktiv / aus,
- identische Belastung.

Messgrößen:

- aktive Neuronen,
- Netzwerkaktivität,
- Übergangszeit,
- Erholung,
- Hysterese.

### Achse C — Information

Zunächst:

- Surprise-/Entropy-Baseline.

Erst danach:

- sauber definierte PID,
- estimator-validierte PID,
- matched Vergleich gegen einfachere Informationsmaße.

### Achse D — Spike-Amplitude

Vergleich:

- konstante Amplitude,
- health-modulierte Amplitude,
- ggf. hardware-inspirierte Amplitudenregel.

Keine Variante wird vorab als besser klassifiziert.

## 7. Rechenaufwand und Skalierung

Hyperdimensionale Zustände erhöhen Speicher- und Rechenaufwand. Das ist ein
Engineering-Problem, aber noch kein Grund, frühzeitig neuromorphe Hardware zur
Voraussetzung zu machen.

Die sinnvolle Reihenfolge ist:

1. kleine deterministische CPU-Referenz,
2. Profiling und Komplexitätsmessung,
3. Vektorisierung/GPU nur bei Bedarf,
4. erst danach hardware-spezifische Portierung, falls die wissenschaftliche
   Frage dies rechtfertigt.

## 8. MHRN-Bezug

MHRN ist ein öffentliches experimentelles Forschungsprojekt mit expliziter
Trennung von Implementation, DATA, Human Review, EVID und Replikation.

In der hier durchgeführten gezielten Websuche wurde keine unabhängige
peer-reviewte Publikation gefunden, die MHRN selbst evaluiert oder zitiert.
Daraus folgt **nicht**, dass keine solche Quelle existiert; es beschreibt nur
den aktuellen Suchbefund.

PAN bleibt deshalb ein Playground-Modul und kein Beleg für MHRN.

## 9. Weg aus dem Playground in die Forschung

```text
Playground-Beobachtung
  ↓
Research Candidate
  ↓
neue Forschungsfrage
  ↓
Hypothese status: untested
  ↓
Preregistration DRAFT
  ↓
Freeze
  ↓
neuer kanonischer DATA-Lauf
  ↓
Human Review
  ↓
optional EVID
  ↓
unabhängige Replikation
```

Keine Playground-Session darf diesen Prozess abkürzen.

## 10. Primärquellen

- Orchard J, Furlong PM, Simone K. *Efficient Hyperdimensional Computing With
  Spiking Phasors*. Neural Computation, 2024. DOI: 10.1162/neco_a_01693.
- Makkeh A et al. *A general framework for interpretable neural learning based
  on local information-theoretic goal functions*. PNAS, 2025.
  DOI: 10.1073/pnas.2408125122.
- Naudé J et al. *Effects of cellular homeostatic intrinsic plasticity on
  dynamical and computational properties of biological recurrent neural
  networks*. J Neurosci, 2013. DOI: 10.1523/JNEUROSCI.0870-13.2013.
- Gao S et al. *Multi-scale neural homeostasis mechanisms*. 2025.
  DOI: 10.1016/j.aehs.2025.02.002.
- Chow S-F, Wick SD, Riecke H. *Neurogenesis Drives Stimulus Decorrelation in
  a Model of the Olfactory Bulb*. PLoS Comput Biol, 2012.
  DOI: 10.1371/journal.pcbi.1002398.
- Cao W et al. *Explosive aging transition in globally coupled FitzHugh-Nagumo
  neurons with higher-order interactions*. Acta Phys Sin, 2026.
  DOI: 10.7498/aps.75.20260125.
- Mahata C et al. *Uniform multilevel switching and synaptic properties in
  RF-sputtered InGaZnO-based memristor treated with oxygen plasma*. J Chem
  Phys, 2023. DOI: 10.1063/5.0179314.
- Bej S et al. *Fast agreement-driven device-calibrated local learning
  paradigms for spiking neural networks*. Neural Networks, 2026.
  DOI: 10.1016/j.neunet.2026.108809.
- Ahmed HF, Samiei T, Nozari E. *On the optimal temporal resolution for
  information representation in neural activity*. Front Comput Neurosci,
  2026. DOI: 10.3389/fncom.2026.1885975.


**Methodische Grenze:** kein Beweis weltweiter Neuheit.
