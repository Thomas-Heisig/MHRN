# MHRN Playground / PAN-5D Glossar

**Geltungsbereich:** nicht-kanonische Playground-Dokumentation.

## AdEx
Adaptive Exponential Integrate-and-Fire. Punktneuronenmodell mit exponentiellem
Spike-Anstieg und Adaptationsvariable.

## Aging Transition
Übergang eines gekoppelten dynamischen Systems von makroskopischer
Oszillation/Aktivität zu einem weitgehend inaktiven Zustand, häufig untersucht
durch steigenden Anteil inaktiver Einheiten. Nicht identisch mit dem
PAN-Health-Wert eines einzelnen Neurons.

## Apoptose
Programmierter Zelltod. Im PAN Playground lediglich als bounded technische
Deaktivierung eines Modellneurons nach Unterschreiten einer Health-Schwelle
repräsentiert.

## Binding
Operation zur Verknüpfung zweier Hypervektoren. Im Playground stehen
Hadamard-Produkt und zirkuläre Faltung als explorative Operationen zur
Verfügung.

## Bundling
Zusammenfassung mehrerer Hypervektoren zu einer Populationsrepräsentation. Der
Playground verwendet dafür eine komponentenweise Vorzeichen-Bündelung.

## Closed Loop
Rückkopplung eines abgeleiteten Netzwerkzustands auf zukünftige Eingaben oder
Neuronströme. PAN kann den vorherigen Populations-Hyperzustand über eine
deterministische Matrix zurückprojizieren.

## DATA
Kanonische Forschungsdaten eines nach dem MHRN-Protokoll ausgeführten Laufs.
Playground-Ausgaben sind **keine DATA**.

## D1–D10
Bezeichnungen der ersten PAN-Hyperzustandsachsen:

- D1 intrinsische Simulationszeit
- D2 Erregbarkeits-Proxy
- D3 Plastizitätsaktivität
- D4 Informations-/Surprise-Proxy
- D5 Health
- D6 Neuromodulations-Proxy
- D7 Energie
- D8 Positionsprojektion
- D9 Konsolidierungs-Proxy
- D10 Netzwerkkopplungs-Proxy

Die Benennung ist eine PAN-Modellentscheidung, keine etablierte Standardachse
des Hyperdimensional Computing.

## EVID
Von MHRN akzeptierter Evidenzstatus nach dem jeweils geltenden Governance- und
Human-Review-Prozess. Ein Playground-Lauf kann nicht direkt EVID werden.

## FHRR
Fourier Holographic Reduced Representation. Vektor-symbolische Repräsentation
mit komplexwertigen Komponenten; in Spiking-Phasor-Arbeiten wird deren Phase
durch Spike-Zeit kodiert.

## Health / H_i
Normierter explorativer PAN-Zustand eines Neurons. Der Wert ist kein
biologischer Gesundheitsmarker.

## HDC
Hyperdimensional Computing. Rechnen mit hochdimensionalen verteilten
Vektorrepräsentationen.

## Higher-Order Interaction
Interaktion, die nicht nur paarweise Einheiten koppelt, sondern drei oder mehr
Einheiten gemeinsam einbezieht. Nicht automatisch Bestandteil des aktuellen
PAN-Simulators.

## Homeostase
Regulation eines Systems in Richtung eines funktionalen Arbeitsbereichs.
PAN nutzt derzeit technische bounded Approximationen; diese sind nicht als
biologische MHRN-Homeostase validiert.

## Hyperstate / Hyperzustand
PAN-interner D-dimensionaler Zustandsvektor eines Modellneurons.

## Hypervektor
Hochdimensionaler Vektor, der Zustände, Symbole oder Merkmale verteilt
repräsentiert. Ein PAN-Hyperzustand ist eine spezielle, semantisch benannte
Verwendung und nicht synonym mit jeder HDC-Repräsentation.

## Infomorphic / infomorphes Neuron
Neuronales Lernkonzept, bei dem lokale informationstheoretische Zielfunktionen,
unter anderem auf Basis von PID-Terms, die Gewichtsanpassung bestimmen.

## Intrinsic Time
Im PAN-Modell die Simulationszeit eines Zustandsverlaufs. Nicht Wanduhrzeit und
keine zusätzliche physikalische Raumzeitdimension.

## K-Matrix
Explorative Rückkopplungsmatrix, die einen PAN-Populationszustand auf
Neuronströme projiziert. Kein validiertes Weltmodell.

## MHRN
Multi-Scale Homeostatic Recurrence Network. Das Projekt trennt Software,
kanonische DATA, Human Review, EVID und Replikation. PAN ist aktuell nur ein
Playground-Modul.

## Neurogenese
Entstehung neuer Neuronen. Im aktuellen PAN Playground noch nicht als
vollständiger Lebenszyklus implementiert.

## Neuromodulation
Modulation neuronaler Dynamik oder Plastizität durch zusätzliche Signale. Die
PAN-D6-Achse ist derzeit nur ein technischer Proxy.

## N-D
N-dimensional. Der Playground unterstützt generische N-D-Geometrien und
PAN-Hyperzustände bis zu den konfigurierten Sicherheitsgrenzen.

## PAN
Bezeichnung der explorativen Modellfamilie in diesem Playground. PAN besitzt
keinen wissenschaftlichen Evidenzstatus allein durch Implementierung.

## PAN-5D
PAN-Konfiguration mit mindestens fünf semantisch benannten Hyperzustandsachsen.
5D ist kein behauptetes Optimum.

## Partial Information Decomposition / PID
Informations-theoretische Zerlegung gemeinsamer, redundanter, einzigartiger und
synergetischer Informationsbeiträge mehrerer Quellen über ein Ziel. Der PAN
Playground implementiert derzeit **keine PID**.

## PLAYGROUND
Governance-Klasse für nicht-kanonische Exploration. Kein DATA, kein EVID, kein
Maturity-Beitrag.

## PLAYGROUND_PAN
Zusätzliche Klassifikation für PAN-bezogene Playground-Diagnostik. Sie ändert
die allgemeine PLAYGROUND-Grenze nicht.

## Preregistration
Vorab fixiertes Forschungsprotokoll mit Hypothesen, Messgrößen, Kontrollen und
Auswertung. Voraussetzung für einen späteren kanonischen PAN-bezogenen
Forschungsstrang.

## Research Candidate
Nicht-präregistrierte Idee, die aus Exploration entstehen darf. Sie ist noch
keine registrierte Hypothese.

## SADP — Spike-Amplitude-Dependent Plasticity
Plastizitätsbegriff, bei dem die Stärke eines Pulses/Spikes die
Gewichtsänderung beeinflusst, häufig in neuromorphen Bauelementen.

## SADP — Spike Agreement Dependent Plasticity
Anderer Plastizitätsbegriff: Lernregel auf Basis der Übereinstimmung von
Spike-Zügen. Trotz gleichem Kürzel nicht mit Spike-Amplitude-Dependent
Plasticity verwechseln.

## Spike-Amplitude
Im PAN Playground ein modulierender Faktor für die Stärke eines ausgehenden
synaptischen Ereignisses. Kein Beleg für biologische Aktionspotential-Amplitude
oder Leistungsgewinn.

## Spiking Phasor
Spikende Repräsentation einer Phasenkomponente eines Hypervektors, bei der die
Phase über Spike-Zeit innerhalb eines Zyklus kodiert wird.

## STDP
Spike-Timing-Dependent Plasticity. Gewichtsänderung abhängig von relativer
Spike-Zeit von Prä- und Postsynapse.

## STP
Short-Term Plasticity. Kurzfristige Veränderung synaptischer Wirksamkeit.

## Surprise Proxy
Aktueller PAN-D4-Ersatzwert aus lokaler Aktivitätswahrscheinlichkeit. Er ist
keine PID und keine allgemeine Informationstheorie-Messung.

## VSA
Vector Symbolic Architecture. Familie kompositioneller
Vektorrepräsentationssysteme; HDC und FHRR werden häufig in diesem Kontext
diskutiert.

## Weltmodell
Interne Repräsentation, die für Vorhersage, Zustandsabschätzung oder Planung
genutzt werden kann. Der PAN-Hyperraum ist derzeit nur ein explorativer
Zustandsraum und **kein validiertes Weltmodell**.
