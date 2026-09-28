"use strict";

import { apiGet, apiPost, byId } from "../core/api.js";
import { initGuidedWorkspace } from "./playground-workspace.js";
import { getLanguage } from "../core/i18n.js?v=i18n-fix-20260920b";

let lastResult = null;
let catalogState = null;
let liveSessionId = null;
let liveLoopTimer = null;
let nightPollTimer = null;
let catalogInfoItems = new Map();
let activeCatalogInfo = null;
const PLAYGROUND_PRESETS_STORAGE = "mhrn.playground.presets.v1";
const DEFAULT_PLAYGROUND_PRESET = "full_embodiment";
const BUILTIN_PLAYGROUND_PRESETS = {
  izhikevich_reference: {
    label: "Izhikevich · Referenz",
    description: "Klarer deterministischer Ausgangspunkt für das Izhikevich-RS-Modell.",
    settings: { neuron_model: "izhikevich_rs", synapse_model: "static", plasticity_rule: "none", topology: "mhrn_5d", n_neurons: 128, edge_budget: 1024, k_neighbors: 16, modules: 2, weight: 4, stimulus_current: 8, geometry_mode: "mixed_additive", pan_enabled: false, behavior_learning_enabled: false },
  },
  pan_exploration: {
    label: "PAN · Explorationsprofil",
    description: "PAN mit geschlossenem Input-Aktion-Reward-Loop; explorativ und nicht kanonisch.",
    settings: { neuron_model: "pan_adex_5d", pan_enabled: true, pan_closed_loop: true, pan_feedback_gain: 1.5, pan_feedback_nonlinearity: "tanh", pan_feedback_saturation: 20, input_topology: "channel_partitioned", input_channels: 8, target_encoding: "one_hot", target_cue_channel: 0, target_cue_current: 30, target_persistence: 16, action_loop_enabled: true, action_space_size: 4, action_coupling_strength: 2, reward_signal_enabled: true, reward_magnitude: 5, reward_channel: 1, inhibitory_fraction: 0.2, gaba_strength: 4, neuron_threshold_variance: 0.15, neuron_tau_m_variance: 0.1, geometry_mode: "mixed_additive", weight: 4, behavior_learning_enabled: true, behavior_learning_rate: 0.2, behavior_epsilon: 0.2 },
  },
};
const PLAYGROUND_REPO_ELEMENTS = [
  ["NetworkAreaAdapter", "Repo · Embodiment", "Gemeinsamer Adaptervertrag für autorisierte neuronale Netzwerkbereiche und externe Modalitäten.", "src/embodiment/neural_symbiosis.py"],
  ["NeuralIOInterface", "Playground · Neural I/O", "Referenzschnittstelle für Codec, Decoder, Rollen, Phasen und Provenienz; Payloads bleiben außerhalb des SNN.", "src/playground/neural_io/interface.py"],
  ["PANRuntime", "Playground · PAN", "Bündelt Hyperzustand, Health, Energie, Aktivität, Feedback und Apoptose als explorative Runtime-Schicht.", "src/playground/pan/runtime.py"],
  ["BehavioralLearningEngine", "Playground · Lernen", "Begrenzte Policy-Referenz mit Aktivitätstraces, Reward und Exploration; kein biologischer Lernnachweis.", "src/playground/pan/behavioral_learning.py"],
  ["StickFigureSandbox", "Playground · Embodiment", "Deterministische Punktmassen-/Feder-Sandbox mit Sensorik, Aktoren, Posture-Reward und Episodenreset.", "src/playground/pan/sandbox.py"],
  ["ResearchRegistry", "Repo · Wissenschaft", "Kanonischer Registry-Bereich für Forschungsfragen, Hypothesen, Claims und EVID; Playground-Ergebnisse werden nicht automatisch eingetragen.", "src/research/registry.py"],
  ["EvidenceEngine", "Repo · Wissenschaft", "Verarbeitet Quellen- und Reviewverträge zu EVID; nicht Teil einer explorativen Playground-Ausführung.", "src/research/evidence_engine.py"],
  ["pack_coords", "Repo · Core", "Kanonischer Koordinaten-Packvertrag für native MHRN-5D-IDs.", "src/core/spatial_index.py"],
  ["NightRunManager", "Playground · Meta", "Begrenzter, resumierbarer Meta-Lauf für Strategie-/Routing-Experimente außerhalb des SNN.", "src/playground/night_run.py"],
];

function playgroundEscape(value){return String(value??"").replace(/[&<>"']/g,character=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[character]));}

const CATALOG_CATEGORY_COPY = {
  en: { models: "Neuron models", topologies: "Topologies", stimuli: "Stimuli", synapses: "Synapses", plasticity: "Plasticity", readouts: "Readouts", panCandidates: "PAN research candidates", panLiterature: "PAN literature context", geometryLiterature: "Geometry literature context", neuralIO: "Neural I/O codecs", analyses: "Analyses", robustness: "Robustness controls", cudaCompiler: "CUDA gate compiler", cudaParity: "CUDA parity", repo: "Repo & Playground components" },
  de: { models: "Neuronmodelle", topologies: "Topologien", stimuli: "Stimuli", synapses: "Synapsen", plasticity: "Plastizität", readouts: "Readouts", panCandidates: "PAN Research Candidates", panLiterature: "PAN Literaturkontext", geometryLiterature: "Geometrie-Literaturkontext", neuralIO: "Neural-I/O-Codecs", analyses: "Analysen", robustness: "Robustheitskontrollen", cudaCompiler: "CUDA Gate Compiler", cudaParity: "CUDA Parität", repo: "Repo- und Playground-Komponenten" },
};

const CATALOG_DESCRIPTION_COPY = {
  izhikevich_rs: { en: "A regular-spiking point-neuron model with a compact two-variable membrane state. It is useful as a deterministic reference because its parameters make tonic firing and spike timing easy to inspect; it does not represent a complete biological neuron.", de: "Ein Point-Neuron-Modell für reguläres Spiking mit einem kompakten Membranzustand aus zwei Variablen. Es eignet sich als deterministische Referenz, weil tonisches Feuern und Spike-Zeitpunkte gut untersuchbar sind; ein vollständiges biologisches Neuron wird damit nicht dargestellt." },
  izhikevich_fs: { en: "A fast-spiking Izhikevich variant with parameters chosen for brief, frequent action potentials. Compare it with the regular-spiking variant under matched input, topology, seed, and tick budget rather than treating the label as a biological classification.", de: "Eine schnell feuernde Izhikevich-Variante mit Parametern für kurze, häufige Aktionspotenziale. Sie sollte unter identischem Input, identischer Topologie, identischem Seed und Tick-Budget mit der Regular-Spiking-Variante verglichen werden; das Label ist keine biologische Klassifikation." },
  lif: { en: "The leaky integrate-and-fire baseline accumulates current, relaxes toward a resting potential, emits a threshold event, and resets. It is intentionally simple and makes a useful control for separating network effects from nonlinear intrinsic dynamics.", de: "Die Leaky-Integrate-and-Fire-Basis akkumuliert Strom, kehrt zum Ruhepotenzial zurück, erzeugt bei einer Schwelle ein Ereignis und wird zurückgesetzt. Sie ist bewusst einfach und dient als Kontrolle, um Netzwerkeffekte von nichtlinearen intrinsischen Dynamiken zu trennen." },
  adex: { en: "Adaptive exponential integrate-and-fire adds an adaptation variable and an exponential spike onset to the membrane equation. In the Playground it is an executable reference model, not a claim that the chosen parameters reproduce a particular cell type.", de: "Adaptive Exponential Integrate-and-Fire ergänzt die Membrangleichung um eine Adaptationsvariable und einen exponentiellen Spikebeginn. Im Playground ist es ein ausführbares Referenzmodell und keine Behauptung, dass die Parameter einen bestimmten Zelltyp reproduzieren." },
  pan_adex_5d: { en: "An AdEx membrane model combined with the exploratory PAN health, energy, feedback, and hyperstate layer. The additional state is a software experiment surface; it is explicitly outside canonical MHRN evidence and requires matched controls for interpretation.", de: "Ein AdEx-Membranmodell mit der explorativen PAN-Schicht für Health, Energie, Feedback und Hyperzustand. Der zusätzliche Zustand ist eine Software-Experimentierfläche, liegt ausdrücklich außerhalb kanonischer MHRN-Evidenz und benötigt gematchte Kontrollen für jede Interpretation." },
  static: { en: "A fixed weighted connection whose weight is applied without synaptic learning. Use it as the cleanest control when the question concerns neuron, topology, stimulus, or geometry effects rather than adaptation.", de: "Eine feste gewichtete Verbindung, deren Gewicht ohne synaptisches Lernen angewendet wird. Sie ist die sauberste Kontrolle, wenn es um Neuron, Topologie, Stimulus oder Geometrie und nicht um Anpassung geht." },
  stdp: { en: "Pair-based spike-timing-dependent plasticity updates a connection from the relative timing of pre- and postsynaptic spikes. The Playground implementation is bounded and exploratory; learning-rate, trace, seed, and weight-clamp settings must be reported with every comparison.", de: "Paarbasierte Spike-Timing-Dependent Plasticity aktualisiert eine Verbindung anhand des relativen Zeitpunkts prä- und postsynaptischer Spikes. Die Playground-Implementierung ist begrenzt und explorativ; Lernrate, Traces, Seed und Gewichtsklammer müssen bei jedem Vergleich dokumentiert werden." },
  triplet_stdp: { en: "A trace-based triplet approximation extends pair timing with additional pre/post activity history. It can expose sensitivity to burst structure, but it is not a validated implementation of a universal triplet rule.", de: "Eine Trace-basierte Triplet-Näherung ergänzt Paar-Timing um zusätzliche Prä-/Post-Aktivitätshistorie. Sie kann Empfindlichkeit für Burst-Strukturen zeigen, ist aber keine validierte Implementierung einer universellen Triplet-Regel." },
  eligibility_trace: { en: "Stores a temporary eligibility signal so that a later modulator can influence a connection. This separates local spike timing from delayed credit assignment, while remaining a bounded Playground mechanism.", de: "Speichert ein temporäres Eligibility-Signal, damit ein späterer Modulator eine Verbindung beeinflussen kann. Dadurch werden lokales Spike-Timing und verzögerte Credit-Zuweisung getrennt; es bleibt jedoch ein begrenzter Playground-Mechanismus." },
  three_factor: { en: "Combines local eligibility with a third modulatory factor such as reward or oscillatory state. The entry is useful for controlled software comparisons, not evidence for a biological three-factor learning mechanism.", de: "Verbindet lokale Eligibility mit einem dritten modulierenden Faktor wie Reward oder Oszillationszustand. Der Eintrag dient kontrollierten Softwarevergleichen und ist keine Evidenz für einen biologischen Drei-Faktoren-Lernmechanismus." },
  none: { en: "Disables the corresponding adaptive mechanism. This is the reference condition for asking whether an observed change actually depends on learning, plasticity, or reward routing.", de: "Deaktiviert den jeweiligen adaptiven Mechanismus. Dies ist die Referenzbedingung für die Frage, ob eine beobachtete Änderung tatsächlich von Lernen, Plastizität oder Reward-Routing abhängt." },
  linear: { en: "Returns the mean activity across the selected population. It preserves a continuous signal and is suitable when downstream analysis should reflect magnitude rather than a binary decision.", de: "Gibt die mittlere Aktivität der ausgewählten Population zurück. Das Signal bleibt kontinuierlich und eignet sich, wenn nachgelagerte Analysen die Stärke statt einer binären Entscheidung abbilden sollen." },
  threshold: { en: "Converts mean population activity into a binary decision using the configured threshold. This is easy to inspect, but it discards amplitude information and should be paired with continuous metrics.", de: "Wandelt die mittlere Populationsaktivität anhand der konfigurierten Schwelle in eine binäre Entscheidung um. Das ist leicht zu inspizieren, verwirft aber Amplitudeninformation und sollte mit kontinuierlichen Metriken ergänzt werden." },
  population_vector: { en: "Normalizes non-negative population rates into a vector whose entries sum to one. It describes relative participation, not absolute activity or a decoded semantic payload.", de: "Normiert nichtnegative Populationsraten zu einem Vektor, dessen Einträge sich zu eins summieren. Er beschreibt relative Beteiligung, nicht absolute Aktivität und keinen dekodierten semantischen Payload." },
  "stimuli:none": { en: "Provides zero external current to every neuron. It is useful for measuring spontaneous or internally generated activity and for detecting whether a configuration has hidden drive.", de: "Gibt jedem Neuron keinen externen Strom. Damit lassen sich spontane oder intern erzeugte Aktivität messen und versteckte Antriebe in einer Konfiguration erkennen." },
  none_stimulus: { en: "Provides zero external current to every neuron. It is useful for measuring spontaneous or internally generated activity and for detecting whether a configuration has hidden drive.", de: "Gibt jedem Neuron keinen externen Strom. Damit lassen sich spontane oder intern erzeugte Aktivität messen und versteckte Antriebe in einer Konfiguration erkennen." },
  deterministic: { en: "Applies a repeatable block stimulus to a small leading subset of neurons. Fixed timing makes it useful for replay and debugging, but it can introduce a strong input-position bias.", de: "Legt einen wiederholbaren Block-Stimulus auf eine kleine führende Neuronengruppe. Die feste zeitliche Struktur eignet sich für Replay und Debugging, kann aber einen starken Inputpositions-Bias erzeugen." },
  poisson: { en: "Samples independent pulse events with a bounded Poisson-like probability derived from rate and timestep. The seed is part of the experiment contract because each run receives a different event sequence otherwise.", de: "Erzeugt unabhängige Pulsereignisse mit einer aus Rate und Zeitschritt abgeleiteten, begrenzten Poisson-ähnlichen Wahrscheinlichkeit. Der Seed ist Teil des Versuchsvertrags, da sonst jede Ausführung eine andere Ereignisfolge erhält." },
  ramp: { en: "Increases the applied current over a bounded cycle from zero to the configured maximum. It probes activation thresholds and adaptation, but the repeating cycle must be considered during interpretation.", de: "Steigert den angelegten Strom in einem begrenzten Zyklus von null bis zum konfigurierten Maximum. Damit lassen sich Aktivierungsschwellen und Adaptation untersuchen; der wiederholte Zyklus muss bei der Interpretation berücksichtigt werden." },
  oscillatory: { en: "Drives the population with a sinusoidal current at the configured frequency. It is a synthetic forcing function for phase, synchrony, and frequency-response diagnostics, not a model of a specific biological oscillator.", de: "Treibt die Population mit einem sinusförmigen Strom der konfigurierten Frequenz. Das ist eine synthetische Anregung für Phase-, Synchronie- und Frequenzantwortdiagnostik, kein Modell eines bestimmten biologischen Oszillators." },
  channel_ab: { en: "Alternates stimulation between two spatially separated neuron groups. The pattern makes routing and population selectivity visible while keeping timing deterministic and easy to replay.", de: "Wechselt die Stimulation zwischen zwei räumlich getrennten Neuronengruppen. Das Muster macht Routing und Populationsselektivität sichtbar und bleibt zeitlich deterministisch sowie leicht reproduzierbar." },
  NetworkAreaAdapter: { en: "The adapter boundary connects authorized neural network areas and external modalities without silently merging their ownership or evidence status. It is an integration contract for routing and inspection, not a claim that the connected areas form one validated biological system.", de: "Die Adaptergrenze verbindet autorisierte neuronale Netzwerkbereiche und externe Modalitäten, ohne Besitz- oder Evidenzstatus stillschweigend zu vermischen. Sie ist ein Integrationsvertrag für Routing und Inspektion, keine Behauptung eines validierten biologischen Gesamtsystems." },
  NeuralIOInterface: { en: "This interface separates external payload handling, codec selection, gateway roles, lifecycle phases, and provenance from the internal neural state. It makes the boundary auditable and prevents a transport payload from being mistaken for a neural representation.", de: "Diese Schnittstelle trennt externen Payload, Codec-Auswahl, Gateway-Rollen, Lebenszyklusphasen und Provenienz vom internen neuronalen Zustand. Dadurch bleibt die Grenze prüfbar und ein Transport-Payload wird nicht mit einer neuronalen Repräsentation verwechselt." },
  PANRuntime: { en: "The PAN runtime groups health, energy, activity, feedback, hyperstate, and apoptosis bookkeeping around an exploratory network run. It provides bounded software state and telemetry; it is not a validated physiological model or a scientific evidence layer.", de: "Die PAN-Runtime bündelt Health, Energie, Aktivität, Feedback, Hyperzustand und Apoptose-Buchhaltung um einen explorativen Netzwerklauf. Sie liefert begrenzten Softwarezustand und Telemetrie, ist aber kein validiertes physiologisches Modell und keine wissenschaftliche Evidenzschicht." },
  BehavioralLearningEngine: { en: "A bounded activity-gated policy reference that maps observations to actions and updates parameters from reward. It is intended for reproducible Playground comparisons, with explicit episode, exploration, and reward settings rather than an implicit claim of animal-like learning.", de: "Eine begrenzte, aktivitätsbewachte Policy-Referenz, die Beobachtungen auf Aktionen abbildet und Parameter über Reward aktualisiert. Sie dient reproduzierbaren Playground-Vergleichen mit expliziten Episoden-, Explorations- und Reward-Einstellungen und behauptet kein tierähnliches Lernen." },
  StickFigureSandbox: { en: "A deterministic point-mass and spring sandbox with sensors, actuators, posture analysis, reward channels, friction, boundaries, and episode reset. It tests closed-loop plumbing and reward timing; it is not a biomechanical body simulation.", de: "Eine deterministische Punktmassen- und Feder-Sandbox mit Sensoren, Aktoren, Posture-Analyse, Reward-Kanälen, Reibung, Grenzen und Episodenreset. Sie testet Closed-Loop-Verkabelung und Reward-Timing, ist aber keine biomechanische Körpersimulation." },
  ResearchRegistry: { en: "The registry is the canonical place for research questions, hypotheses, claims, identifiers, and evidence status. Playground output stays outside it unless a separate human-controlled workflow creates and reviews a scientific record.", de: "Die Registry ist der kanonische Ort für Forschungsfragen, Hypothesen, Claims, Kennungen und Evidenzstatus. Playground-Ausgaben bleiben außerhalb, sofern kein separater, menschlich kontrollierter Workflow einen wissenschaftlichen Datensatz anlegt und prüft." },
  EvidenceEngine: { en: "This area turns source and review contracts into EVID artifacts under explicit provenance rules. It is intentionally separated from exploratory execution so that a descriptive Playground result cannot promote itself into evidence.", de: "Dieser Bereich verarbeitet Quellen- und Reviewverträge unter expliziten Provenienzregeln zu EVID-Artefakten. Er bleibt bewusst von der explorativen Ausführung getrennt, damit ein beschreibendes Playground-Ergebnis sich nicht selbst zu Evidenz hochstufen kann." },
  pack_coords: { en: "The coordinate packing contract converts canonical x, y, z, d4, and d5 coordinates into stable native identifiers. It protects identity and lookup semantics at the MHRN boundary; it does not choose a topology or prove a geometric hypothesis.", de: "Der Koordinaten-Packvertrag wandelt kanonische x-, y-, z-, d4- und d5-Koordinaten in stabile native Kennungen um. Er schützt Identitäts- und Lookup-Semantik an der MHRN-Grenze, wählt aber keine Topologie und beweist keine geometrische Hypothese." },
  NightRunManager: { en: "A bounded, resumable manager for long-running strategy, routing, or meta-learning experiments. Checkpoints preserve exploratory state and policy parameters; they do not turn an overnight run into a preregistered scientific result.", de: "Ein begrenzter, fortsetzbarer Manager für länger laufende Strategie-, Routing- oder Meta-Learning-Experimente. Checkpoints erhalten explorativen Zustand und Policy-Parameter; ein Nachtlauf wird dadurch nicht zu einem preregistrierten wissenschaftlichen Ergebnis." },
};

function catalogLanguage(){return getLanguage()==="de"?"de":"en";}

function catalogCategoryTitle(category, language=catalogLanguage()){
  return CATALOG_CATEGORY_COPY[language]?.[category]||category;
}

function describeCatalogItem(item, category, language=catalogLanguage()){
  const key=String(item?.name||"");
  const categoryId=String(item?.categoryKey||category||"");
  const exact=CATALOG_DESCRIPTION_COPY[`${categoryId}:${key}`]?.[language]||CATALOG_DESCRIPTION_COPY[key]?.[language];
  if(exact)return exact;
  const source=String(item?.note||item?.description||"").trim();
  const name=String(item?.label||item?.name||"Baustein");
  if(categoryId==="panCandidates")return language==="de"?`Eine explorative PAN-Forschungsidee: ${source||name}. Der Eintrag ist weder registrierte Hypothese noch Evidenz. Für eine wissenschaftliche Prüfung wären Vorabdefinition, gematchte Kontrollen, Seeds und ein eingefrorenes Protokoll erforderlich.`:`An exploratory PAN research idea: ${source||name}. This entry is neither a registered hypothesis nor evidence. Scientific examination would require a preregistered definition, matched controls, fixed seeds, and a frozen protocol.`;
  if(categoryId==="panLiterature"||categoryId==="geometryLiterature")return language==="de"?`Kontextquelle für die Einordnung von ${name}. Sie liefert Orientierung und Begriffe für den explorativen Playground, ersetzt aber weder eine systematische Review noch einen Nachweis für eine Playground-Ausführung.`:`Context source for interpreting ${name}. It provides orientation and terminology for the exploratory Playground, but it is neither a systematic review nor evidence for a Playground execution.`;
  if(categoryId==="analyses")return language==="de"?`Diagnostik ${name}: Diese Auswertung verdichtet einen beobachtbaren Laufzustand zu einer beschreibenden Kennzahl oder Strukturansicht. Sie erklärt keine Ursache und wird erst durch Seeds, Kontrollen, Rohdaten und Protokoll interpretierbar.`:`Diagnostic ${name}: this analysis condenses an observable run state into a descriptive metric or structural view. It does not establish causality and becomes interpretable only with seeds, controls, raw data, and a recorded protocol.`;
  if(categoryId==="robustness")return language==="de"?`Robustheitskontrolle ${name}: Diese Variation prüft, ob ein beobachtetes Muster gegenüber einer gezielten Störung oder alternativen Konfiguration bestehen bleibt. Sie ist ein Kontrollwerkzeug, kein automatischer Robustheitsnachweis.`:`Robustness control ${name}: this variation checks whether an observed pattern survives a targeted perturbation or alternative configuration. It is a control tool, not an automatic proof of robustness.`;
  if(categoryId==="topologies")return language==="de"?`Netzwerk-Baustein ${name}: Er definiert, wie Neuronen im explorativen Graphen räumlich oder logisch verbunden werden. Kantenbudget, Dimensionen, Seed und Geometrie bestimmen das tatsächlich erzeugte Netzwerk; der Name ist keine Qualitätswertung.`:`Network building block ${name}: it defines how neurons are connected in the exploratory graph, spatially or logically. Edge budget, dimensions, seed, and geometry determine the realized network; the name is not a quality ranking.`;
  if(categoryId==="stimuli")return language==="de"?`Input-Baustein ${name}: Er erzeugt den externen Stromverlauf für den Lauf. Rate, Amplitude, Seed und zeitliche Struktur beeinflussen die Ausführung und müssen bei Vergleichen zusammen mit dem Neuronen- und Netzwerkzustand angegeben werden.`:`Input building block ${name}: it generates the external current sequence for a run. Rate, amplitude, seed, and timing affect the execution and must be reported together with neuron and network state for comparisons.`;
  if(categoryId==="neuralIO")return language==="de"?`Schnittstellen-Baustein ${name}: Er beschreibt die kontrollierte Grenze zwischen externem Payload, Codec und neuronaler Repräsentation. Der Eintrag macht keine Aussage darüber, dass ein Payload im SNN selbst semantisch gespeichert ist.`:`Interface building block ${name}: it describes the controlled boundary between external payload, codec, and neural representation. It does not claim that a payload is semantically stored inside the SNN.`;
  return language==="de"?`Explorativer Playground-Baustein ${name}. ${source||"Der Eintrag steuert einen klar abgegrenzten Teil der Konfiguration oder Auswertung."} Er ist ausführbar oder auswertbar innerhalb des Playground-Vertrags, erzeugt aber keine DATA- oder EVID-Einstufung.`:`Exploratory Playground building block ${name}. ${source||"The entry controls a bounded part of the configuration or analysis."} It is executable or inspectable within the Playground contract, but it does not create a DATA or EVID classification.`;
}

const PLAYGROUND_DEFAULT_HINTS = {
  "pg-weight": "4", "pg-weight-decay": "0", "pg-weight-max-clamp": "100", "pg-dimensions": "5", "pg-neurons": "128", "pg-edges": "1024",
  "pg-radius": "0.35", "pg-k": "16", "pg-rewire": "0.15", "pg-modules": "2", "pg-delay": "1",
  "pg-ticks": "256", "pg-current": "8", "pg-rate": "20", "pg-seed": "12345", "pg-ensemble": "1",
  "pg-pan-dimensions": "5", "pg-pan-feedback-gain": "0.05", "pg-pan-health-decay": "0.001", "pg-pan-apoptosis": "0.1", "pg-pan-bias-current": "10",
  "pg-geometry-lambda-a": "0.5", "pg-geometry-lambda-b": "0.5", "pg-geometry-sigma": "0.1", "pg-geometry-p0": "0.3", "pg-geometry-delay-velocity": "0.25",
  "pg-clock-base-hz": "100", "pg-clock-event-batch": "10", "pg-execution-high": "0.30", "pg-execution-low": "0.05", "pg-execution-hysteresis": "0.02", "pg-execution-dwell": "100", "pg-execution-window": "100",
  "pg-growth-activity": "0.25", "pg-growth-coactivation": "2", "pg-growth-info": "0.25", "pg-growth-prune": "0.05", "pg-growth-max-synapses": "128", "pg-growth-max-new": "8", "pg-cuda-budget": "2048", "pg-offload-snapshot": "1000",
  "pg-thalamic-threshold": "0", "pg-thalamic-attention": "1.15", "pg-thalamic-inhibition": "0.35", "pg-cortical-layers": "6", "pg-cortical-lr": "0.01", "pg-behavior-actions": "4", "pg-behavior-target": "0", "pg-behavior-min-activity": "0.01", "pg-behavior-lr": "0.2", "pg-behavior-epsilon": "0.2", "pg-behavior-episode": "16", "pg-behavior-bias": "3",
  "pg-neural-io-input-channels": "16", "pg-neural-io-output-channels": "16", "pg-neural-io-window": "16", "pg-neural-io-current": "25",
};

function updateDefaultHints() {
  Object.entries(PLAYGROUND_DEFAULT_HINTS).forEach(([id, defaultValue]) => {
    const field = byId(id);
    if (!field) return;
    const currentValue = String(field.value);
    const changed = currentValue !== defaultValue;
    const message = changed
      ? `Abweichend vom Standard: ${currentValue}. Standardwert: ${defaultValue}.`
      : `Standardwert: ${defaultValue}.`;
    field.title = message;
    field.closest("label")?.classList.toggle("pg-non-default", changed);
  });
}

function injectStyles() {
  if (byId("mhrn-playground-styles")) return;
  const style = document.createElement("style");
  style.id = "mhrn-playground-styles";
  style.textContent = `
    #tab-playground .workspace-header{margin-bottom:0;padding-bottom:12px;border-bottom:1px solid var(--rule)}#tab-playground .workspace-header p{max-width:72rem;color:var(--ink-3)}
    .pg-permanent-boundary{position:relative;display:flex;gap:.8rem;align-items:flex-start;margin:.7rem 0 1rem;padding:.8rem 1rem;border:1px solid color-mix(in srgb,var(--amber) 48%,var(--rule));border-left:3px solid var(--amber);border-radius:var(--r-sm);background:var(--amber-wash);box-shadow:none}.pg-permanent-boundary>span{font-size:1rem;line-height:1.2}.pg-permanent-boundary strong{display:block;color:var(--ink)}.pg-permanent-boundary p{margin:.2rem 0 0;opacity:.78;font-size:.7rem;line-height:1.45}
    .playground-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;align-items:start}.playground-grid>.playground-card:nth-child(-n+4){border-top:3px solid var(--accent)}.playground-grid>.playground-card:nth-child(n+5):nth-child(-n+6){border-top:3px solid var(--indigo)}.playground-grid>.playground-card:nth-child(n+7):nth-child(-n+9){border-top:3px solid var(--moss)}.playground-grid>.playground-card:nth-child(n+10):nth-child(-n+16){border-top:3px solid var(--amber)}.playground-grid>.playground-card:nth-child(n+17){border-top:3px solid var(--rule-3)}
    .playground-preset-deck{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:10px;margin:0 0 12px;padding:12px;border:1px solid var(--rule-2);border-top:3px solid var(--accent);border-radius:var(--r-md);background:var(--paper-2)}.playground-preset-deck h3{margin:0 0 4px;font-size:.95rem}.playground-preset-deck p{margin:0;color:var(--ink-3);font-size:.68rem;line-height:1.45}.playground-preset-copy{display:flex;gap:8px;align-items:flex-start}.playground-preset-copy::before{content:"01";color:var(--accent);font:700 .56rem/1 var(--font-mono);letter-spacing:.08em}.playground-preset-controls{display:grid;grid-template-columns:1fr 1fr;gap:7px;align-items:end}.playground-preset-controls label{display:grid;gap:4px;color:var(--ink-3);font-size:.64rem}.playground-preset-controls label:first-child{grid-column:1/-1}.playground-preset-controls input,.playground-preset-controls select{width:100%;min-height:30px;padding:5px 7px;border:1px solid var(--rule-2);border-radius:var(--r-xs);background:var(--paper);color:var(--ink);font-size:.68rem}.playground-preset-controls button{min-height:30px;padding:0 8px;border:1px solid var(--rule-2);border-radius:var(--r-xs);background:var(--paper);color:var(--ink-2);font-size:.62rem}.playground-preset-controls button:hover{border-color:var(--accent);background:var(--accent-wash)}.playground-preset-description{grid-column:1/-1;margin:0!important;padding:6px 8px;border-left:2px solid var(--rule-3);background:var(--paper-3);font:500 .6rem/1.4 var(--font-mono);white-space:pre-wrap}
    .playground-card,.playground-viz,.playground-analysis-card{border:1px solid var(--rule);border-radius:var(--r-md);padding:12px;background:var(--paper-2);box-shadow:0 1px 0 color-mix(in srgb,var(--ink) 4%,transparent)}
    .playground-card{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:10px;align-content:start}.playground-card h3,.playground-card small{grid-column:1/-1}.playground-card h3,.playground-viz h3,.playground-analysis-card h3{margin:0 0 9px;padding-bottom:7px;border-bottom:1px solid var(--rule);font-size:.82rem;letter-spacing:.01em}.playground-card h3::first-letter{color:var(--accent)}.playground-live-launcher{border-top:3px solid var(--indigo)}.playground-live-launcher p,.playground-live-launcher pre{grid-column:1/-1}.playground-live-launcher p{margin:0 0 5px;color:var(--ink-3);font-size:.68rem;line-height:1.45}
    .playground-card label{display:grid;gap:4px;margin:0 0 8px;color:var(--ink-3);font-size:.65rem;line-height:1.2}.playground-card small{display:block;margin-top:2px;color:var(--ink-4);line-height:1.45}.playground-card label.pg-non-default{outline:1px dotted color-mix(in srgb,var(--accent) 55%,transparent);outline-offset:4px;border-radius:2px}
    .playground-card input,.playground-card select,.playground-card textarea{width:100%;min-height:30px;padding:5px 7px;border:1px solid var(--rule-2);border-radius:var(--r-xs);background:var(--paper);color:var(--ink);font-size:.7rem}.playground-card input:focus,.playground-card select:focus,.playground-card textarea:focus{border-color:var(--accent);background:var(--paper-2);box-shadow:0 0 0 2px var(--accent-wash)}.playground-card textarea{min-height:72px;resize:vertical;font-family:var(--font-mono);font-size:.64rem}
    .playground-actions{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}.playground-actions button{min-height:30px;padding:0 10px;border-radius:var(--r-xs);border:1px solid var(--rule-2);background:var(--paper-2);color:var(--ink-2);font-size:.65rem}.playground-actions button:hover{background:var(--paper-3);border-color:var(--accent)}.playground-actions .primary{font-weight:700;border-color:var(--accent);background:var(--accent);color:var(--paper-2)}
    .playground-status{padding:9px 11px;border:1px solid var(--rule);border-left:3px solid var(--rule-3);border-radius:var(--r-xs);background:var(--paper-2);color:var(--ink-2);font-size:.68rem;white-space:pre-wrap;overflow:auto}.playground-status[data-state="error"]{border-left-color:var(--crimson);color:var(--crimson)}.playground-status[data-state="ok"]{border-left-color:var(--moss);color:var(--moss)}
    .pg-live-monitor{width:min(94vw,1000px);max-height:84vh;padding:0;border:1px solid var(--rule-3);border-radius:var(--r-md);background:var(--paper);color:var(--ink);box-shadow:var(--shadow-float)}.pg-live-monitor::backdrop{background:rgba(20,16,12,.55);backdrop-filter:blur(4px)}.pg-live-monitor>header{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;padding:9px 12px;border-bottom:1px solid var(--rule);background:var(--paper-2)}.pg-live-monitor>header h2{margin:0;font-size:.95rem}.pg-live-monitor>header p{margin:2px 0 0;color:var(--ink-3);font-size:.61rem}.pg-live-monitor-close{min-width:28px;padding:0}.pg-live-monitor-body{padding:9px;overflow:hidden}.pg-live-monitor-metrics{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:5px;margin-bottom:7px}.pg-live-monitor-metric{padding:6px;border:1px solid var(--rule);border-radius:var(--r-xs);background:var(--paper-2)}.pg-live-monitor-metric span{display:block;color:var(--ink-4);font:700 .46rem/1.1 var(--font-mono);text-transform:uppercase}.pg-live-monitor-metric strong{display:block;margin-top:3px;font:600 .7rem/1 var(--font-mono)}.pg-live-monitor-grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(220px,1fr);gap:7px}.pg-live-monitor-panel{min-width:0;padding:7px;border:1px solid var(--rule);border-radius:var(--r-xs);background:var(--paper-2)}.pg-live-monitor-panel h3{margin:0 0 5px;padding-bottom:4px;border-bottom:1px solid var(--rule);font-size:.68rem}.pg-live-monitor-panel canvas{display:block;width:100%;height:130px;background:var(--paper);border:1px solid var(--rule)}.pg-live-monitor-params{margin:0;max-height:118px;overflow:hidden;font:500 .55rem/1.25 var(--font-mono);white-space:pre-wrap}.pg-live-monitor-actions{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px}.pg-live-monitor-actions button{min-height:27px;padding:0 8px;font-size:.6rem}.pg-live-monitor-actions .pg-monitor-primary{border-color:var(--accent);background:var(--accent);color:var(--paper-2)}
    .playground-metrics{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:5px;margin:10px 0}.playground-metric{padding:8px 9px;border:1px solid var(--rule);border-radius:var(--r-xs);background:var(--paper-2)}.playground-metric span{display:block;color:var(--ink-4);font:700 .5rem/1.2 var(--font-mono);letter-spacing:.07em;text-transform:uppercase}.playground-metric strong{display:block;margin-top:4px;color:var(--ink);font:600 .82rem/1.1 var(--font-mono)}
    .pg-live-monitor-visuals{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:5px;margin-top:7px}.pg-live-monitor-tile{display:block;width:100%;padding:5px;border:1px solid var(--rule);border-radius:var(--r-xs);background:var(--paper-2);color:var(--ink);text-align:left;cursor:pointer}.pg-live-monitor-tile:hover,.pg-live-monitor-tile:focus-visible{border-color:var(--accent);background:var(--accent-wash)}.pg-live-monitor-tile span{display:block;margin-bottom:3px;color:var(--ink-3);font:700 .47rem/1.1 var(--font-mono);text-transform:uppercase}.pg-live-monitor-tile canvas{display:block;width:100%;height:65px;background:var(--paper);border:1px solid var(--rule);image-rendering:auto}.pg-live-zoom{width:min(96vw,1400px);max-height:92vh;padding:0;border:1px solid var(--rule-3);border-radius:var(--r-md);background:var(--paper);box-shadow:var(--shadow-float)}.pg-live-zoom::backdrop{background:rgba(20,16,12,.66);backdrop-filter:blur(5px)}.pg-live-zoom header{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;padding:10px 13px;border-bottom:1px solid var(--rule);background:var(--paper-2)}.pg-live-zoom header strong{display:block;font-size:.96rem}.pg-live-zoom header p{margin:3px 0 0;color:var(--ink-3);font-size:.62rem}.pg-live-zoom-toolbar{display:flex;flex-wrap:wrap;gap:6px;padding:8px 13px;border-bottom:1px solid var(--rule);background:var(--paper-3)}.pg-live-zoom-toolbar button{min-height:30px;padding:0 9px;border:1px solid var(--rule-2);border-radius:var(--r-xs);background:var(--paper);color:var(--ink-2);font-size:.64rem}.pg-live-zoom-toolbar button:hover,.pg-live-zoom-toolbar button:focus-visible{border-color:var(--accent);background:var(--accent-wash)}.pg-live-zoom-stage{min-height:360px;padding:12px;overflow:auto;background:var(--paper)}.pg-live-zoom canvas{display:block;width:100%;height:min(72vh,760px);min-height:360px;background:var(--paper-2);border:1px solid var(--rule);image-rendering:auto}
    .playground-viz-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.playground-viz{min-height:260px}.playground-viz canvas{width:100%;height:210px;display:block}
    .playground-analysis-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:10px}.playground-analysis-card pre{font-size:.62rem;max-height:260px;overflow:auto;white-space:pre-wrap}
    .playground-session-list{display:grid;gap:6px}.playground-session{display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:9px 10px;border:1px solid var(--rule);border-radius:var(--r-xs);background:var(--paper-2)}.playground-session small{display:block;color:var(--ink-4)}
    .playground-catalog{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.playground-catalog article{padding:10px;border:1px solid var(--rule);border-radius:var(--r-xs);background:var(--paper-2)}.playground-chip{display:inline-flex;margin:2px;padding:3px 5px;border-radius:var(--r-xs);border:1px solid var(--rule);background:var(--paper-3);color:var(--ink-3);font:500 .58rem/1.2 var(--font-mono);cursor:pointer}.playground-chip:hover,.playground-chip:focus-visible{border-color:var(--accent);background:var(--accent-wash);color:var(--accent-2)}.playground-catalog-dialog{width:min(92vw,620px);padding:0;border:1px solid var(--rule-3);border-radius:var(--r-md);background:var(--paper);color:var(--ink);box-shadow:var(--shadow-float)}.playground-catalog-dialog::backdrop{background:rgba(20,16,12,.52);backdrop-filter:blur(4px)}.playground-catalog-dialog header{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;padding:12px 14px;border-bottom:1px solid var(--rule);background:var(--paper-2)}.playground-catalog-dialog header h2{margin:0;font-size:1rem}.playground-catalog-dialog header p{margin:3px 0 0;color:var(--accent);font:700 .55rem/1.2 var(--font-mono);text-transform:uppercase}.playground-catalog-dialog-body{padding:14px}.playground-catalog-dialog-body p{font-size:.76rem;line-height:1.5}.playground-catalog-dialog-body code{font-size:.65rem}
    .pg-neutral-note{padding:9px 11px;margin:9px 0;border-left:3px solid var(--indigo);background:var(--indigo-wash);color:var(--ink-2);font-size:.68rem;line-height:1.45}.pg-neutral-note strong{color:var(--ink)}
    @media(max-width:1150px){.playground-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.playground-metrics{grid-template-columns:repeat(4,1fr)}.playground-preset-deck{grid-template-columns:1fr 1.4fr}.pg-live-monitor-visuals{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:760px){.playground-grid,.playground-viz-grid,.playground-analysis-grid,.playground-catalog{grid-template-columns:1fr}.playground-card{grid-template-columns:1fr}.playground-card h3,.playground-card small{grid-column:auto}.playground-metrics{grid-template-columns:repeat(2,1fr)}.playground-preset-deck{grid-template-columns:1fr}.playground-preset-controls{grid-template-columns:1fr}.pg-live-monitor-metrics,.pg-live-monitor-grid,.pg-live-monitor-visuals{grid-template-columns:1fr}}
  `;
  document.head.append(style);
}

function optionMarkup(items, labelKey = "label") {
  return (items || []).filter((item) => item.available !== false).map((item) => {
    const label = item[labelKey] || item.name;
    return `<option value="${item.name}" title="${item.note || ""}">${label}</option>`;
  }).join("");
}

function ensurePermanentBoundary(root) {
  if (byId("pg-permanent-boundary")) return;
  const boundary = document.createElement("div");
  boundary.id = "pg-permanent-boundary";
  boundary.className = "pg-permanent-boundary";
  boundary.dataset.mhrnPersistent = "";
  boundary.innerHTML = `<span>🧪</span><div><strong>PLAYGROUND · explorativ, nicht-wissenschaftlich, keine EVID-Bindung</strong><p>Bausteine dürfen frei kombiniert werden. Ergebnisse sind weder DATA noch EVID und verändern Registry, Dissertation Map oder Scientific Maturity nicht.</p></div>`;
  const header = root.querySelector(":scope > .workspace-header, :scope > header");
  header?.insertAdjacentElement("afterend", boundary) || root.prepend(boundary);
}

function buildPanels(root) {
  if (byId("playground-builder")) return;
  root.insertAdjacentHTML("beforeend", `
    <section data-generated-panel="builder" id="playground-builder">
      <div class="pg-neutral-note"><strong>Neutraler Baukasten:</strong> Keine Modell- oder Topologieauswahl ist eine Empfehlung. <code>MHRN 5D</code> ist der Architektur-Default, weil er den nativen MHRN-Vertrag <code>(x,y,z,d4,d5)</code> verwendet — nicht weil 5D als überlegen gilt.</div>
      <section class="playground-preset-deck" aria-labelledby="pg-preset-deck-title">
        <div class="playground-preset-copy"><div><h3 id="pg-preset-deck-title">Preset Lab</h3><p>Empfohlene Startpunkte für Izhikevich und PAN. Presets verändern nur den Playground. Eigene Profile liegen im Browser; der Katalog kommt vom Server.</p></div></div>
        <div class="playground-preset-controls"><label>Profil<select id="pg-user-preset-select"></select></label><label>Eigenes Preset speichern<input id="pg-user-preset-name" type="text" placeholder="z. B. PAN · Seed 2"></label><button type="button" id="pg-user-preset-apply">Anwenden</button><button type="button" id="pg-user-preset-save">Speichern</button><button type="button" id="pg-user-preset-delete">Eigenes löschen</button><p id="pg-user-preset-description" class="playground-preset-description">Preset auswählen oder eigene Einstellungen speichern.</p></div>
      </section>
      <div class="playground-grid">
        <article class="playground-card"><h3>01 · Neuronen & Synapsen</h3>
          <label>Neuronmodell<select id="pg-neuron-model"></select></label>
          <label>Synapsenmodell<select id="pg-synapse-model"></select></label>
          <label>Startgewicht<input id="pg-weight" type="number" min="0" max="100" step="0.1" value="4"></label>
          <label>Gewichtszerfall<input id="pg-weight-decay" type="number" min="0" max="1" step="0.001" value="0"></label>
          <label>Gewichtsmaximum<input id="pg-weight-max-clamp" type="number" min="0.1" max="100" step="0.1" value="100"></label>
          <label>Plastizität<select id="pg-plasticity"></select></label>
          <label>Readout<select id="pg-readout"></select></label>
          <small>Enthält Izhikevich RS/FS/IB/CH/LTS/Resonator/Sensory/Motor, LIF, AdEx, HH Na/K/Ca und Multi-Compartment.</small>
        </article>
        <article class="playground-card"><h3>02 · Geometrie & Netzwerk</h3>
          <label>Topologie<select id="pg-topology"></select></label>
          <label>Dimensionen (Generic N-D)<input id="pg-dimensions" type="number" min="1" max="32" value="5"></label>
          <label>Neuronen<input id="pg-neurons" type="number" min="2" max="1024" value="128"></label>
          <label>Kanten<input id="pg-edges" type="number" min="2" max="20000" value="1024"></label>
          <small>MHRN 5D verwendet explizit x/y/z/d4/d5 und den kanonischen <code>pack_coords</code>-Vertrag. Generic N-D reicht bis 32D.</small>
        </article>
        <article class="playground-card"><h3>03 · Konnektivität</h3>
          <label>Radius<input id="pg-radius" type="number" min="0.001" max="2" step="0.01" value="0.35"></label>
          <label>k Nachbarn<input id="pg-k" type="number" min="1" max="64" value="16"></label>
          <label>Rewiring-Wahrscheinlichkeit<input id="pg-rewire" type="number" min="0" max="1" step="0.01" value="0.15"></label>
          <label>Module<input id="pg-modules" type="number" min="1" max="32" value="2"></label>
          <label>Delay (Ticks)<input id="pg-delay" type="number" min="1" max="64" value="1"></label>
        </article>
        <article class="playground-card"><h3>04 · Stimulus & Lauf</h3>
          <label>Stimulus<select id="pg-stimulus"></select></label>
          <label>Ticks<input id="pg-ticks" type="number" min="1" max="2048" value="256"></label>
          <label>Strom<input id="pg-current" type="number" min="0" max="500" step="0.5" value="8"></label>
          <label>Rate Hz<input id="pg-rate" type="number" min="0" max="1000" value="20"></label>
          <label>Seed<input id="pg-seed" type="number" min="0" value="12345"></label>
          <label>Seed-Ensemble<input id="pg-ensemble" type="number" min="1" max="8" value="1"></label>
          <label><span><input id="pg-persist" type="checkbox"> Session lokal speichern</span></label>
        </article>
        <article class="playground-card"><h3>05 · PAN-Hyperstate</h3>
          <label><span><input id="pg-pan-enabled" type="checkbox"> PAN explorativ aktivieren</span></label>
          <label>PAN-Dimensionen<input id="pg-pan-dimensions" type="number" min="5" max="32" value="5"></label>
          <label><span><input id="pg-pan-closed-loop" type="checkbox" checked> Closed Loop</span></label>
          <label>Feedback-Gain<input id="pg-pan-feedback-gain" type="number" min="0" max="5" step="0.01" value="0.05"></label>
          <label>Feedback Delay<input id="pg-pan-feedback-delay" type="number" min="0" max="64" value="0"></label>
          <label>Feedback Quelle<select id="pg-pan-feedback-source"><option value="population">population</option><option value="layer">layer</option><option value="subset">subset</option><option value="hypervector">hypervector</option></select></label>
          <label>Feedback Ziel<select id="pg-pan-feedback-target"><option value="all">all</option><option value="layer">layer</option><option value="random_subset">random_subset</option></select></label>
          <label>Nichtlinearität<select id="pg-pan-feedback-nonlinearity"><option value="linear">linear</option><option value="tanh">tanh</option><option value="sign">sign</option><option value="clip">clip</option></select></label>
          <label>Feedback θ<input id="pg-pan-feedback-threshold" type="number" min="0" max="1" step="0.01" value="0"></label>
          <label>Feedback Sättigung<input id="pg-pan-feedback-saturation" type="number" min="0" max="100" step="0.5" value="100"></label>
          <label>Health-Decay<input id="pg-pan-health-decay" type="number" min="0" max="1" step="0.001" value="0.001"></label>
          <label>Apoptose-Schwelle<input id="pg-pan-apoptosis" type="number" min="0" max="1" step="0.01" value="0.1"></label>
          <label>PAN Bias-Strom<input id="pg-pan-bias-current" type="number" min="0" max="500" step="0.5" value="10"></label>
          <small>PAN ist eine nicht-kanonische Explorationsschicht. D4 nutzt aktuell einen Surprise-Proxy, keine validierte PID.</small>
        </article>
        <article class="playground-card"><h3>06 · Geometrischer Raum Dg</h3>
          <label>Geometrie-Modus<select id="pg-geometry-mode"><option value="mixed_additive" selected>Mixed Additive</option><option value="shortcut_union">Shortcut Union</option></select></label>
          <label>λa<input id="pg-geometry-lambda-a" type="number" min="0" max="10" step="0.05" value="0.5"></label>
          <label>λb<input id="pg-geometry-lambda-b" type="number" min="0" max="10" step="0.05" value="0.5"></label>
          <label>σ<input id="pg-geometry-sigma" type="number" min="0.001" max="2" step="0.01" value="0.1"></label>
          <label>p0<input id="pg-geometry-p0" type="number" min="0" max="1" step="0.05" value="0.3"></label>
          <label>xyz-Geschwindigkeit / Tick<input id="pg-geometry-delay-velocity" type="number" min="0.001" max="10" step="0.01" value="0.25"></label>
          <small><code>x,y,z</code> sind kartesisch; <code>a,b</code> sind zyklische Torus-Koordinaten. Zustandsraum Ds und Geometrierraum Dg bleiben unabhängig. Klein-Flasche, dynamische Positionierung, PID-Kraft und Neurogenese sind nicht implementiert.</small>
        </article>
        <article class="playground-card"><h3>07 · Generative PAN Runtime</h3>
          <label>Clock<select id="pg-clock-mode"><option value="continuous">Continuous</option><option value="dual">Dual · Event + Continuous</option></select></label>
          <label>Base Hz<input id="pg-clock-base-hz" type="number" min="1" max="10000" value="100"></label>
          <label>Event Batch ms<input id="pg-clock-event-batch" type="number" min="0.05" max="1000" step="0.05" value="10"></label>
          <label>Execution<select id="pg-execution-mode"><option value="HYBRID_AUTO">HYBRID_AUTO</option><option value="EVENT_ONLY">EVENT_ONLY</option><option value="TICK_ONLY">TICK_ONLY</option></select></label>
          <label>Initial Engine<select id="pg-execution-initial"><option value="EVENT_ONLY">EVENT_ONLY</option><option value="TICK_ONLY">TICK_ONLY</option></select></label>
          <label>θ high<input id="pg-execution-high" type="number" min="0" max="1" step="0.01" value="0.30"></label>
          <label>θ low<input id="pg-execution-low" type="number" min="0" max="1" step="0.01" value="0.05"></label>
          <label>Hysterese<input id="pg-execution-hysteresis" type="number" min="0" max="0.5" step="0.01" value="0.02"></label>
          <label>Min. Dwell (Ticks)<input id="pg-execution-dwell" type="number" min="0" max="2048" value="100"></label>
          <label>Aktivitätsfenster<input id="pg-execution-window" type="number" min="1" max="2048" value="100"></label>
          <label>Transition<select id="pg-execution-transition"><option value="clean">clean</option><option value="debug">debug</option><option value="fast">fast</option></select></label>
          <label><span><input id="pg-execution-sync" type="checkbox" checked> Sync on switch</span></label>
          <label><span><input id="pg-execution-log" type="checkbox" checked> Transitionen loggen</span></label>
          <label><span><input id="pg-growth-enabled" type="checkbox"> generatives Wachstum</span></label>
          <label>Aktivität θ<input id="pg-growth-activity" type="number" min="0" max="1" step="0.01" value="0.25"></label>
          <label>Co-Aktivierung θ<input id="pg-growth-coactivation" type="number" min="1" max="1000" value="2"></label>
          <label>Info θ<input id="pg-growth-info" type="number" min="0" max="1" step="0.01" value="0.25"></label>
          <label>Prune θ<input id="pg-growth-prune" type="number" min="0" max="100" step="0.01" value="0.05"></label>
          <label>max. Synapsen/Neuron<input id="pg-growth-max-synapses" type="number" min="1" max="512" value="128"></label>
          <label>max. neue Synapsen/Barriere<input id="pg-growth-max-new" type="number" min="1" max="256" value="8"></label>
          <label>Hardware-Profil<select id="pg-hardware-profile"><option value="reference_cpu">Python Reference</option><option value="cuda_8gb_balanced_plan">CUDA 8GB Balanced · Plan</option></select></label>
          <label>CUDA-Budget MiB<input id="pg-cuda-budget" type="number" min="128" max="16384" value="2048"></label>
          <label><span><input id="pg-offload-enabled" type="checkbox"> SSD-Offload</span></label>
          <label>Snapshot-Intervall<input id="pg-offload-snapshot" type="number" min="1" max="1000000" value="1000"></label>
          <small>Referenzpfad: deterministisch interleaved. CUDA wird hier nur budgetiert; persistente Kernel, Dynamic Parallelism, Hardware-/Thermal-Kopplung sind ausdrücklich nicht implementiert.</small>
        </article>
        <article class="playground-card"><h3>08 · Lernen & kognitive Organisation</h3>
          <label><span><input id="pg-thalamic-enabled" type="checkbox"> Thalamic Gating</span></label>
          <label>Relay θ<input id="pg-thalamic-threshold" type="number" min="0" max="1" step="0.01" value="0"></label>
          <label>Attention Gain<input id="pg-thalamic-attention" type="number" min="0" max="4" step="0.05" value="1.15"></label>
          <label>Inhibition Gain<input id="pg-thalamic-inhibition" type="number" min="0" max="1" step="0.05" value="0.35"></label>
          <label><span><input id="pg-cortical-enabled" type="checkbox"> kortikale Organisation</span></label>
          <label>Schichten<input id="pg-cortical-layers" type="number" min="2" max="12" value="6"></label>
          <label><span><input id="pg-cortical-plasticity" type="checkbox" checked> Layer-Gain plastisch</span></label>
          <label>Layer Lernrate<input id="pg-cortical-lr" type="number" min="0" max="1" step="0.005" value="0.01"></label>
          <label><span><input id="pg-behavior-enabled" type="checkbox"> Verhalten lernen</span></label>
          <label>Aktionen<input id="pg-behavior-actions" type="number" min="1" max="16" value="4"></label>
          <label>Zielaktion<input id="pg-behavior-target" type="number" min="0" max="15" value="0"></label>
          <label>Zielmodus<select id="pg-behavior-target-mode"><option value="cycle">cycle</option><option value="fixed">fixed</option></select></label>
          <label>Min. Aktivität<input id="pg-behavior-min-activity" type="number" min="0" max="1" step="0.01" value="0.01"></label>
          <label>Policy Lernrate<input id="pg-behavior-lr" type="number" min="0.001" max="1" step="0.01" value="0.2"></label>
          <label>Exploration ε<input id="pg-behavior-epsilon" type="number" min="0" max="1" step="0.01" value="0.2"></label>
          <label>Episode (Ticks)<input id="pg-behavior-episode" type="number" min="1" max="2048" value="16"></label>
          <label>Policy Bias-Strom<input id="pg-behavior-bias" type="number" min="0" max="100" step="0.5" value="3"></label>
          <small>Lernpfad speichert Policy-Parameter, Aktivitätstraces und Reward-Historie, keine exakten externen Payloads. Thalamus/Kortex sind funktionale Playground-Abstraktionen, keine biologische Gleichsetzung.</small>
        </article>
        <article class="playground-card"><h3>09 · Neural I/O Interface</h3>
          <label><span><input id="pg-neural-io-enabled" type="checkbox"> neuronales I/O aktivieren</span></label>
          <label>Input Codec<select id="pg-neural-io-codec"></select></label>
          <label>Input Payload<textarea id="pg-neural-io-payload">0.5</textarea></label>
          <label>Input-Kanäle<input id="pg-neural-io-input-channels" type="number" min="1" max="256" value="16"></label>
          <label>Input-Rolle<select id="pg-neural-io-input-role"><option>GATEWAY_AFFERENT</option><option>AFFERENT</option></select></label>
          <label>Output Decoder<select id="pg-neural-io-decoder"></select></label>
          <label>Output-Kanäle<input id="pg-neural-io-output-channels" type="number" min="1" max="256" value="16"></label>
          <label>Output-Rolle<select id="pg-neural-io-output-role"><option>GATEWAY_EFFERENT</option><option>EFFERENT</option></select></label>
          <label>Codec-Fenster (Ticks)<input id="pg-neural-io-window" type="number" min="1" max="2048" value="16"></label>
          <label>Input-Strom<input id="pg-neural-io-current" type="number" min="0" max="500" step="0.5" value="25"></label>
          <label>Phase<select id="pg-neural-io-phase"><option>QUERY</option><option>IDLE</option><option>WAIT</option><option>RESPONSE</option><option>TIMEOUT</option></select></label>
          <label>Modality<input id="pg-neural-io-modality" value="digital"></label>
          <label>Source ID<input id="pg-neural-io-source" value="playground.input"></label>
          <small><strong>Payload ≠ Neural Representation.</strong> Exakte Nutzdaten bleiben außerhalb des SNN. Query/Response werden durch Richtung, Phase, <code>correlation_id</code> und Provenienz getrennt. Tools/Aktoren werden im Playground nie ausgeführt.</small>
        </article>
        <article class="playground-card"><h3>10 · Input-Kanäle</h3>
          <label>Input-Topologie<select id="pg-input-topology"><option value="uniform">uniform</option><option value="channel_partitioned">channel_partitioned</option><option value="spatial_gradient">spatial_gradient</option><option value="random_per_neuron">random_per_neuron</option></select></label>
          <label>Kanäle<input id="pg-input-channels" type="number" min="1" max="64" value="16"></label>
          <label>Kanal → Neuronen (JSON)<textarea id="pg-input-channel-map">[]</textarea></label>
          <label>Amplituden (JSON)<textarea id="pg-input-amplitudes">[]</textarea></label>
          <label>Frequenzen Hz (JSON)<textarea id="pg-input-frequencies">[]</textarea></label>
          <label>Phasen rad (JSON)<textarea id="pg-input-phases">[]</textarea></label>
          <label>Noise σ<input id="pg-input-noise" type="number" min="0" max="1" step="0.01" value="0"></label>
          <label>Ziel-Cue Kanal<input id="pg-target-cue-channel" type="number" min="0" max="63" value="0"></label>
          <label>Reward-Cue Kanal<input id="pg-reward-cue-channel" type="number" min="0" max="63" value="0"></label>
          <label>Action-Feedback Kanal<input id="pg-action-feedback-channel" type="number" min="0" max="63" value="0"></label>
        </article>
        <article class="playground-card"><h3>11 · Aktions-Loop</h3>
          <label><span><input id="pg-action-loop-enabled" type="checkbox"> Aktions-Loop aktiv</span></label>
          <label>Loop Delay<input id="pg-action-loop-delay" type="number" min="1" max="64" value="1"></label>
          <label>Persistenz<input id="pg-action-persistence" type="number" min="1" max="128" value="1"></label>
          <label>Aktionsraum<input id="pg-action-space-size" type="number" min="2" max="32" value="4"></label>
          <label>Action → Input Map<input id="pg-action-to-input-map" value="auto"></label>
          <label>Kopplungsstärke<input id="pg-action-coupling" type="number" min="0" max="10" step="0.1" value="0"></label>
          <label>Aktionsrauschen<input id="pg-action-noise" type="number" min="0" max="1" step="0.01" value="0"></label>
          <label><span><input id="pg-geometry-input-coupling" type="checkbox"> Geometrie-Input-Kopplung</span></label>
          <label>Geometrie σ<input id="pg-geometry-input-sigma" type="number" min="0.001" max="2" step="0.01" value="0.2"></label>
          <label><span><input id="pg-sandbox-enabled" type="checkbox"> Stick-Figure Sandbox koppeln</span></label>
          <label>Sandbox Sensor Noise<input id="pg-sandbox-sensor-noise" type="number" min="0" max="1" step="0.01" value="0.05"></label>
        </article>
        <article class="playground-card"><h3>12 · Ziel-Kodierung</h3>
          <label>Kodierung<select id="pg-target-encoding"><option value="none">none</option><option value="one_hot">one_hot</option><option value="rate">rate</option><option value="population_latency">population_latency</option></select></label>
          <label>Ziel sichtbar (Ticks)<input id="pg-target-persistence" type="number" min="1" max="256" value="1"></label>
          <label>Ziel-Cue Strom<input id="pg-target-cue-current" type="number" min="0" max="500" step="0.5" value="0"></label>
          <label><span><input id="pg-target-shuffle" type="checkbox"> Ziel-Zuordnung shuffeln</span></label>
          <label>Sequenz<select id="pg-target-predictability"><option value="deterministic">deterministic</option><option value="stochastic">stochastic</option><option value="adversarial">adversarial</option></select></label>
        </article>
        <article class="playground-card"><h3>13 · Belohnung</h3>
          <label><span><input id="pg-reward-enabled" type="checkbox"> Reward-Signal aktiv</span></label>
          <label>Magnitude<input id="pg-reward-magnitude" type="number" min="0" max="10" step="0.1" value="1"></label>
          <label>Reward Delay<input id="pg-reward-delay" type="number" min="0" max="64" value="0"></label>
          <label>Shaping<select id="pg-reward-shaping"><option value="sparse">sparse</option><option value="dense">dense</option><option value="potential_based">potential_based</option></select></label>
          <label>Baseline<input id="pg-reward-baseline" type="number" min="-1" max="1" step="0.05" value="0"></label>
          <label>Decay<input id="pg-reward-decay" type="number" min="0" max="1" step="0.01" value="0"></label>
          <label>Reward Kanal<input id="pg-reward-channel" type="number" min="0" max="63" value="0"></label>
        </article>
        <article class="playground-card"><h3>14 · Kredit-Zuweisung</h3>
          <label>Modus<select id="pg-credit-assignment"><option value="none">none</option><option value="trace">trace</option><option value="reward_modulated_stdp">reward_modulated_stdp</option></select></label>
          <label>Credit Window<input id="pg-credit-window" type="number" min="1" max="512" value="64"></label>
          <label>Eligibility τ ms<input id="pg-eligibility-tau" type="number" min="1" max="1000" step="1" value="200"></label>
          <label>TD-λ<input id="pg-td-lambda" type="number" min="0" max="1" step="0.01" value="0.9"></label>
          <label>γ Discount<input id="pg-gamma-discount" type="number" min="0" max="1" step="0.01" value="0.95"></label>
        </article>
        <article class="playground-card"><h3>15 · Netzwerk-Heterogenität & Zeit</h3>
          <label>Threshold Varianz<input id="pg-threshold-variance" type="number" min="0" max="1" step="0.01" value="0"></label>
          <label>τm Varianz<input id="pg-tau-m-variance" type="number" min="0" max="1" step="0.01" value="0"></label>
          <label>Inhibitorischer Anteil<input id="pg-inhibitory-fraction" type="number" min="0" max="1" step="0.01" value="0"></label>
          <label>GABA Stärke<input id="pg-gaba-strength" type="number" min="0" max="10" step="0.1" value="1"></label>
          <label>E/I Ratio<input id="pg-e-i-ratio" type="number" min="0" max="10" step="0.1" value="1"></label>
          <label>Delay-Verteilung<select id="pg-delay-distribution"><option value="fixed">fixed</option><option value="uniform">uniform</option><option value="lognormal">lognormal</option><option value="gamma">gamma</option></select></label>
          <label>Delay Mean<input id="pg-delay-mean" type="number" min="1" max="32" step="0.1" value="1"></label>
          <label>Refraktär Varianz<input id="pg-refractory-variance" type="number" min="0" max="1" step="0.01" value="0"></label>
          <label>Adaptation Stärke<input id="pg-adaptation-strength" type="number" min="0" max="10" step="0.1" value="0"></label>
          <label>Adaptation τ ms<input id="pg-adaptation-tau" type="number" min="10" max="1000" value="200"></label>
          <label><span><input id="pg-oscillation-enabled" type="checkbox"> interne Oszillation</span></label>
          <label>Oszillation Hz<input id="pg-oscillation-frequency" type="number" min="0.5" max="100" step="0.5" value="8"></label>
        </article>
      </div>
      <div class="playground-actions"><button type="button" class="primary" id="pg-run">▶ Playground starten</button><button type="button" id="pg-robustness">Robustheitskontrollen</button><button type="button" id="pg-reset">Standardwerte</button></div>
      <article class="playground-card playground-live-launcher"><h3>17 · PAN Live Monitor</h3><p>Die laufende PAN-Session mit Start/Pause, Input, Sandbox-Männchen und allen Live-Grafiken im Monitor-Popup.</p><div class="playground-actions"><button type="button" class="primary" id="pg-live-open">Live Monitor öffnen</button><button type="button" id="pg-live-clear">Temporäre Sessions löschen</button></div><pre id="pg-live-state">Keine Live-Session geöffnet.</pre></article>
      <article class="playground-card"><h3>18 · CUDA & Parität</h3>
        <div class="playground-grid">
          <label>Target SM<input id="pg-cuda-target-sm" value="sm_86"></label>
          <label>PTX Version<input id="pg-cuda-ptx-version" value="7.1"></label>
          <label>GPU Neuronen<input id="pg-cuda-neurons" type="number" min="1" max="12288" value="256"></label>
          <label>Blockgröße<select id="pg-cuda-block-size"><option>32</option><option selected>64</option><option>128</option><option>256</option><option>512</option></select></label>
          <label>Device<input id="pg-cuda-device" type="number" min="0" value="0"></label>
          <label>RNG Samples<input id="pg-cuda-rng-samples" type="number" min="1" max="4096" value="1000"></label>
          <label><span><input id="pg-freeze-actions" type="checkbox"> Actions einfrieren</span></label>
          <label><span><input id="pg-freeze-rewards" type="checkbox"> Rewards einfrieren</span></label>
          <label>Referenz-Commit<input id="pg-parity-reference-commit" placeholder="Git SHA"></label>
        </div>
        <div class="playground-actions">
          <button type="button" id="pg-cuda-status">CUDA-Status</button>
          <button type="button" id="pg-cpu-determinism">CPU-Determinismus</button>
          <button type="button" id="pg-cuda-compile">Gate IR / PTX</button>
          <button type="button" id="pg-cuda-preflight">ptxas + Occupancy</button>
          <button type="button" class="primary" id="pg-cuda-smoke">RTX Hardware-Smoke</button>
          <button type="button" id="pg-cuda-rng">RNG-Parität</button>
        </div>
        <small>D1 = exakte Spike-Ereignisse · D2 = numerische Zustandsparität · D3 = Verhaltens-/Metrikparität. CUDA-1.3 prüft den 17-Parameter-Gate-ABI gegen dieselbe CPU-Gate-Referenz. GPU-Portierung von Membran-/Adaptations-/Refractory-State, Synapsen, Delays, Plastizität und Sandbox folgt in CUDA-1.4 bis 1.6.</small>
        <div class="playground-analysis-grid">
          <article class="playground-analysis-card"><h3>CUDA Reifegrad</h3><pre id="pg-cuda-stage-state">Status noch nicht geladen.</pre></article>
          <article class="playground-analysis-card"><h3>ptxas & Occupancy</h3><pre id="pg-cuda-resource-state">Noch kein Preflight.</pre></article>
          <article class="playground-analysis-card"><h3>D2 Hardware-Parität</h3><pre id="pg-cuda-parity-state">Noch kein Hardware-Smoke.</pre></article>
          <article class="playground-analysis-card"><h3>RNG ε-greedy</h3><pre id="pg-cuda-rng-state">Noch kein RNG-Paritätstest.</pre></article>
        </div>
        <pre id="pg-cuda-compiler-state">Noch kein CUDA-/Parity-Lauf.</pre>
      </article>
      <article class="playground-card"><h3>19 · Meta-Nachtlauf</h3>
        <div class="playground-grid">
          <label>Stunden<input id="pg-night-hours" type="number" min="0.01" max="24" step="0.25" value="8"></label>
          <label>Max. Episoden<input id="pg-night-episodes" type="number" min="1" max="1000000" value="10000"></label>
          <label>Checkpoint Sekunden<input id="pg-night-checkpoint" type="number" min="10" max="3600" value="600"></label>
          <label>Seed<input id="pg-night-seed" type="number" min="0" value="12345"></label>
        </div>
        <div class="playground-actions"><button type="button" class="primary" id="pg-night-start">Nachtlauf starten</button><button type="button" id="pg-night-stop">Stop</button><button type="button" id="pg-night-refresh">Status</button></div>
        <small>Meta-Tasks: finden · ablegen · verknüpfen. KnowledgeBase bleibt außerhalb des SNN; PAN lernt Strategie-/Routing-Policies. Checkpoint standardmäßig alle 10 Minuten.</small>
        <pre id="pg-night-state">Kein Nachtlauf aktiv.</pre>
      </article>
      <article class="playground-card"><h3>20 · Posture Reward</h3>
        <label><span><input id="pg-posture-reward-enabled" type="checkbox"> Posture Reward aktiv</span></label>
        <label>Upright-Gewicht<input id="pg-posture-weight-upright" type="number" min="0" max="1" step="0.05" value="0.4"></label>
        <label>Height-Gewicht<input id="pg-posture-weight-height" type="number" min="0" max="1" step="0.05" value="0.3"></label>
        <label>Stability-Gewicht<input id="pg-posture-weight-stability" type="number" min="0" max="1" step="0.05" value="0.2"></label>
        <label>Symmetry-Gewicht<input id="pg-posture-weight-symmetry" type="number" min="0" max="1" step="0.05" value="0.1"></label>
        <label>Zielhöhe<input id="pg-posture-target-height" type="number" min="0" max="2" step="0.1" value="1"></label>
        <label>Max. Tilt<input id="pg-posture-tilt-max" type="number" min="0.1" max="3.14" step="0.1" value="1"></label>
        <label>Max. Velocity<input id="pg-posture-velocity-max" type="number" min="0.1" max="10" step="0.1" value="5"></label>
      </article>
      <article class="playground-card"><h3>21 · Reward Triggers</h3>
        <label>Good Score<input id="pg-trigger-good-score" type="number" min="0.5" max="1" step="0.01" value="0.85"></label>
        <label>Good Dauer<input id="pg-trigger-good-duration" type="number" min="1" max="100" value="10"></label>
        <label>Good Reward<input id="pg-trigger-good-reward" type="number" min="0" max="10" step="0.1" value="1"></label>
        <label>Warning Score<input id="pg-trigger-warning-score" type="number" min="0" max="0.5" step="0.01" value="0.4"></label>
        <label>Warning Reward<input id="pg-trigger-warning-reward" type="number" min="-10" max="0" step="0.1" value="-0.3"></label>
        <label>Falling Rate<input id="pg-trigger-falling-rate" type="number" min="-1" max="0" step="0.01" value="-0.05"></label>
        <label>Falling Reward<input id="pg-trigger-falling-reward" type="number" min="-10" max="0" step="0.1" value="-1"></label>
        <label>Collapse Score<input id="pg-trigger-collapse-score" type="number" min="0" max="0.3" step="0.01" value="0.1"></label>
        <label>Collapse Reward<input id="pg-trigger-collapse-reward" type="number" min="-20" max="0" step="0.1" value="-5"></label>
        <label>Recovery Bonus<input id="pg-trigger-recovery-bonus" type="number" min="0" max="10" step="0.1" value="2"></label>
        <label>Continuous α<input id="pg-reward-continuous-alpha" type="number" min="0" max="1" step="0.01" value="0.1"></label>
      </article>
      <article class="playground-card"><h3>22 · Reward-Kanäle & Episoden</h3>
        <label>Posture-Score Kanal<input id="pg-posture-score-channel" type="number" min="0" max="15" value="2"></label>
        <label>Reward-Event Kanal<input id="pg-reward-event-channel" type="number" min="0" max="15" value="3"></label>
        <label>Posture Current Scale<input id="pg-posture-current-scale" type="number" min="0" max="100" step="1" value="25"></label>
        <label>Event Current Scale<input id="pg-reward-event-scale" type="number" min="0" max="100" step="1" value="25"></label>
        <label><span><input id="pg-episode-termination-enabled" type="checkbox" checked> Episode-Terminierung</span></label>
        <label>Episode Max Ticks<input id="pg-episode-max-ticks" type="number" min="1" max="1000000" value="256"></label>
        <label><span><input id="pg-episode-reset-on-collapse" type="checkbox" checked> Reset bei Kollaps</span></label>
        <small>Score- und Event-Kanal bleiben getrennt von Target- und Action-Kanal. Playground-only, keine automatische EVID.</small>
      </article>
      <div class="playground-status" id="pg-status" data-state="idle">Katalog wird geladen …</div>
    </section>
    <section data-generated-panel="run" id="playground-run">
      <div class="playground-metrics" id="pg-metrics"></div>
      <div class="playground-viz-grid">
        <article class="playground-viz"><h3>Spike Raster</h3><canvas id="pg-raster" width="800" height="300"></canvas></article>
        <article class="playground-viz"><h3>Population Rate</h3><canvas id="pg-rate-canvas" width="800" height="300"></canvas></article>
        <article class="playground-viz"><h3>Topologie · neutrale 2D-Projektion</h3><canvas id="pg-topology-canvas" width="800" height="300"></canvas></article>
        <article class="playground-viz"><h3>Membranpotential · Stichprobe</h3><canvas id="pg-state-canvas" width="800" height="300"></canvas></article>
        <article class="playground-viz"><h3>Frequenzspektrum</h3><canvas id="pg-spectrum-canvas" width="800" height="300"></canvas></article>
        <article class="playground-viz"><h3>Degree-Verteilung</h3><canvas id="pg-degree-canvas" width="800" height="300"></canvas></article>
      </div>
      <div class="playground-analysis-grid">
        <article class="playground-analysis-card"><h3>Spike & Zeit</h3><pre id="pg-analysis-spike">—</pre></article>
        <article class="playground-analysis-card"><h3>Netzwerk & Dimensionen</h3><pre id="pg-analysis-network">—</pre></article>
        <article class="playground-analysis-card"><h3>Plastizität & Performance</h3><pre id="pg-analysis-plasticity">—</pre></article>
        <article class="playground-analysis-card"><h3>Input / Output / Neural Interface</h3><pre id="pg-analysis-io">—</pre></article>
      </div>
      <pre class="playground-status" id="pg-run-json">Noch kein Playground-Lauf.</pre>
    </section>
    <section data-generated-panel="sessions" id="playground-sessions"><div class="pg-neutral-note">Sessions bleiben lokal unter <code>playground_sessions/</code>, sind nicht kanonisch und werden von Git ignoriert.</div><div class="playground-session-list" id="pg-session-list">lade …</div></section>
    <section data-generated-panel="catalog" id="playground-catalog"><div class="playground-catalog" id="pg-catalog-grid"></div></section>
  `);
}

function neuralIOPayload(){
  const codec=byId("pg-neural-io-codec")?.value||"population_latency_v1";
  const raw=byId("pg-neural-io-payload")?.value??"";
  if(codec==="population_latency_v1"){
    const value=Number(raw);
    if(!Number.isFinite(value))throw new Error("Neural-I/O Scalar muss numerisch sein.");
    return value;
  }
  if(codec==="vector_population_v1"){
    let value;
    try{value=JSON.parse(raw);}catch{throw new Error("Vector Input muss gültiges JSON sein.");}
    if(!Array.isArray(value))throw new Error("Vector Input muss ein JSON-Array sein.");
    return value;
  }
  return raw;
}

function parseJsonArray(id, label){
  const raw=byId(id)?.value?.trim()||"[]";
  let value;
  try{value=JSON.parse(raw);}catch{throw new Error(`${label} muss gültiges JSON sein.`);}
  if(!Array.isArray(value))throw new Error(`${label} muss ein JSON-Array sein.`);
  return value;
}

function actionMapPayload(){
  const raw=byId("pg-action-to-input-map")?.value?.trim()||"auto";
  if(raw==="auto"||raw==="spatial")return raw;
  let value;
  try{value=JSON.parse(raw);}catch{throw new Error("Action → Input Map muss auto, spatial oder JSON sein.");}
  if(!Array.isArray(value))throw new Error("Action → Input Map muss ein JSON-Array sein.");
  return value;
}

function formPayload() {
  return {
    name: "dashboard_playground",
    neuron_model: byId("pg-neuron-model").value,
    synapse_model: byId("pg-synapse-model").value,
    weight: Number(byId("pg-weight").value),
    weight_decay: Number(byId("pg-weight-decay").value),
    weight_max_clamp: Number(byId("pg-weight-max-clamp").value),
    plasticity_rule: byId("pg-plasticity").value,
    topology: byId("pg-topology").value,
    stimulus: byId("pg-stimulus").value,
    readout: byId("pg-readout").value,
    n_neurons: Number(byId("pg-neurons").value),
    edge_budget: Number(byId("pg-edges").value),
    ticks: Number(byId("pg-ticks").value),
    dimensions: Number(byId("pg-dimensions").value),
    delay_ticks: Number(byId("pg-delay").value),
    radius: Number(byId("pg-radius").value),
    k_neighbors: Number(byId("pg-k").value),
    rewiring_probability: Number(byId("pg-rewire").value),
    modules: Number(byId("pg-modules").value),
    ensemble_runs: Number(byId("pg-ensemble").value),
    stimulus_current: Number(byId("pg-current").value),
    stimulus_rate_hz: Number(byId("pg-rate").value),
    seed: Number(byId("pg-seed").value),
    persist: byId("pg-persist").checked,
    pan_enabled: byId("pg-pan-enabled").checked,
    pan_dimensions: Number(byId("pg-pan-dimensions").value),
    pan_closed_loop: byId("pg-pan-closed-loop").checked,
    pan_feedback_gain: Number(byId("pg-pan-feedback-gain").value),
    pan_health_decay: Number(byId("pg-pan-health-decay").value),
    pan_apoptosis_threshold: Number(byId("pg-pan-apoptosis").value),
    pan_aging_threshold: 0.3,
    pan_bias_current: Number(byId("pg-pan-bias-current").value),
    clock_mode: byId("pg-clock-mode").value,
    clock_base_hz: Number(byId("pg-clock-base-hz").value),
    clock_event_batch_ms: Number(byId("pg-clock-event-batch").value),
    execution_mode: byId("pg-execution-mode").value,
    execution_initial_mode: byId("pg-execution-initial").value,
    execution_theta_high: Number(byId("pg-execution-high").value),
    execution_theta_low: Number(byId("pg-execution-low").value),
    execution_hysteresis: Number(byId("pg-execution-hysteresis").value),
    execution_min_dwell: Number(byId("pg-execution-dwell").value),
    execution_activity_window: Number(byId("pg-execution-window").value),
    execution_transition_mode: byId("pg-execution-transition").value,
    execution_sync_on_switch: byId("pg-execution-sync").checked,
    execution_log_transitions: byId("pg-execution-log").checked,
    execution_log_state_hash: true,
    growth_enabled: byId("pg-growth-enabled").checked,
    growth_activity_threshold: Number(byId("pg-growth-activity").value),
    growth_coactivation_threshold: Number(byId("pg-growth-coactivation").value),
    growth_information_threshold: Number(byId("pg-growth-info").value),
    growth_prune_threshold: Number(byId("pg-growth-prune").value),
    growth_max_synapses_per_neuron: Number(byId("pg-growth-max-synapses").value),
    growth_max_new_synapses_per_barrier: Number(byId("pg-growth-max-new").value),
    hardware_profile_name: byId("pg-hardware-profile").value,
    cuda_budget_mb: Number(byId("pg-cuda-budget").value),
    offload_enabled: byId("pg-offload-enabled").checked,
    offload_snapshot_interval: Number(byId("pg-offload-snapshot").value),
    thalamic_gating_enabled: byId("pg-thalamic-enabled").checked,
    thalamic_relay_threshold: Number(byId("pg-thalamic-threshold").value),
    thalamic_attention_gain: Number(byId("pg-thalamic-attention").value),
    thalamic_inhibition_gain: Number(byId("pg-thalamic-inhibition").value),
    cortical_layers_enabled: byId("pg-cortical-enabled").checked,
    cortical_layer_count: Number(byId("pg-cortical-layers").value),
    cortical_plasticity: byId("pg-cortical-plasticity").checked,
    cortical_learning_rate: Number(byId("pg-cortical-lr").value),
    behavior_learning_enabled: byId("pg-behavior-enabled").checked,
    behavior_action_count: Number(byId("pg-behavior-actions").value),
    behavior_target_action: Number(byId("pg-behavior-target").value),
    behavior_target_mode: byId("pg-behavior-target-mode").value,
    behavior_min_activity: Number(byId("pg-behavior-min-activity").value),
    behavior_learning_rate: Number(byId("pg-behavior-lr").value),
    behavior_epsilon: Number(byId("pg-behavior-epsilon").value),
    behavior_episode_ticks: Number(byId("pg-behavior-episode").value),
    behavior_bias_current: Number(byId("pg-behavior-bias").value),
    geometry_lambda_a: Number(byId("pg-geometry-lambda-a").value),
    geometry_lambda_b: Number(byId("pg-geometry-lambda-b").value),
    geometry_sigma: Number(byId("pg-geometry-sigma").value),
    geometry_p0: Number(byId("pg-geometry-p0").value),
    geometry_mode: byId("pg-geometry-mode").value,
    geometry_delay_velocity: Number(byId("pg-geometry-delay-velocity").value),
    neural_io_enabled: byId("pg-neural-io-enabled").checked,
    neural_io_input_channels: Number(byId("pg-neural-io-input-channels").value),
    neural_io_output_channels: Number(byId("pg-neural-io-output-channels").value),
    neural_io_input_codec: byId("pg-neural-io-codec").value,
    neural_io_output_decoder: byId("pg-neural-io-decoder").value,
    neural_io_input_payload: neuralIOPayload(),
    neural_io_window_ticks: Number(byId("pg-neural-io-window").value),
    neural_io_input_current: Number(byId("pg-neural-io-current").value),
    neural_io_input_role: byId("pg-neural-io-input-role").value,
    neural_io_output_role: byId("pg-neural-io-output-role").value,
    neural_io_phase: byId("pg-neural-io-phase").value,
    neural_io_correlation_id: "auto",
    neural_io_modality: byId("pg-neural-io-modality").value,
    neural_io_source_id: byId("pg-neural-io-source").value,
    closed_loop_preset: (catalogState?.closed_loop?.presets||[]).some(item=>item.name===byId("pg-user-preset-select")?.value) ? byId("pg-user-preset-select").value : "custom",
    input_topology: byId("pg-input-topology").value,
    input_channels: Number(byId("pg-input-channels").value),
    input_channel_map: parseJsonArray("pg-input-channel-map","Kanal-Map"),
    input_amplitude_per_channel: parseJsonArray("pg-input-amplitudes","Amplituden"),
    input_frequency_per_channel: parseJsonArray("pg-input-frequencies","Frequenzen"),
    input_phase_per_channel: parseJsonArray("pg-input-phases","Phasen"),
    input_noise_sigma: Number(byId("pg-input-noise").value),
    target_cue_channel: Number(byId("pg-target-cue-channel").value),
    reward_cue_channel: Number(byId("pg-reward-cue-channel").value),
    action_feedback_channel: Number(byId("pg-action-feedback-channel").value),
    posture_score_channel: Number(byId("pg-posture-score-channel").value),
    reward_event_channel: Number(byId("pg-reward-event-channel").value),
    posture_current_scale: Number(byId("pg-posture-current-scale").value),
    reward_event_scale: Number(byId("pg-reward-event-scale").value),
    posture_reward_enabled: byId("pg-posture-reward-enabled").checked,
    posture_weight_upright: Number(byId("pg-posture-weight-upright").value),
    posture_weight_height: Number(byId("pg-posture-weight-height").value),
    posture_weight_stability: Number(byId("pg-posture-weight-stability").value),
    posture_weight_symmetry: Number(byId("pg-posture-weight-symmetry").value),
    posture_target_height: Number(byId("pg-posture-target-height").value),
    posture_tilt_max: Number(byId("pg-posture-tilt-max").value),
    posture_velocity_max: Number(byId("pg-posture-velocity-max").value),
    trigger_good_score: Number(byId("pg-trigger-good-score").value),
    trigger_good_duration: Number(byId("pg-trigger-good-duration").value),
    trigger_good_reward: Number(byId("pg-trigger-good-reward").value),
    trigger_warning_score: Number(byId("pg-trigger-warning-score").value),
    trigger_warning_reward: Number(byId("pg-trigger-warning-reward").value),
    trigger_falling_rate: Number(byId("pg-trigger-falling-rate").value),
    trigger_falling_reward: Number(byId("pg-trigger-falling-reward").value),
    trigger_collapse_score: Number(byId("pg-trigger-collapse-score").value),
    trigger_collapse_reward: Number(byId("pg-trigger-collapse-reward").value),
    trigger_recovery_bonus: Number(byId("pg-trigger-recovery-bonus").value),
    reward_continuous_alpha: Number(byId("pg-reward-continuous-alpha").value),
    episode_termination_enabled: byId("pg-episode-termination-enabled").checked,
    episode_max_ticks: Number(byId("pg-episode-max-ticks").value),
    episode_reset_on_collapse: byId("pg-episode-reset-on-collapse").checked,
    pan_feedback_delay: Number(byId("pg-pan-feedback-delay").value),
    pan_feedback_source: byId("pg-pan-feedback-source").value,
    pan_feedback_target: byId("pg-pan-feedback-target").value,
    pan_feedback_nonlinearity: byId("pg-pan-feedback-nonlinearity").value,
    pan_feedback_threshold: Number(byId("pg-pan-feedback-threshold").value),
    pan_feedback_saturation: Number(byId("pg-pan-feedback-saturation").value),
    action_loop_enabled: byId("pg-action-loop-enabled").checked,
    action_loop_delay: Number(byId("pg-action-loop-delay").value),
    action_persistence: Number(byId("pg-action-persistence").value),
    action_to_input_map: actionMapPayload(),
    action_space_size: Number(byId("pg-action-space-size").value),
    action_coupling_strength: Number(byId("pg-action-coupling").value),
    action_noise: Number(byId("pg-action-noise").value),
    freeze_actions: byId("pg-freeze-actions")?.checked||false,
    frozen_action_sequence: lastResult?.closed_loop?.action_history||[],
    reward_signal_enabled: byId("pg-reward-enabled").checked,
    reward_magnitude: Number(byId("pg-reward-magnitude").value),
    reward_delay_ticks: Number(byId("pg-reward-delay").value),
    reward_shaping: byId("pg-reward-shaping").value,
    reward_baseline: Number(byId("pg-reward-baseline").value),
    reward_decay: Number(byId("pg-reward-decay").value),
    reward_channel: Number(byId("pg-reward-channel").value),
    freeze_rewards: byId("pg-freeze-rewards")?.checked||false,
    frozen_reward_sequence: lastResult?.closed_loop?.reward_history||[],
    parity_reference_source: "CPU_PYTHON_PLAYGROUND",
    parity_reference_commit: byId("pg-parity-reference-commit")?.value?.trim()||"",
    target_encoding: byId("pg-target-encoding").value,
    target_persistence: Number(byId("pg-target-persistence").value),
    target_cue_current: Number(byId("pg-target-cue-current").value),
    target_shuffle: byId("pg-target-shuffle").checked,
    target_predictability: byId("pg-target-predictability").value,
    credit_window: Number(byId("pg-credit-window").value),
    eligibility_trace_tau: Number(byId("pg-eligibility-tau").value),
    credit_assignment: byId("pg-credit-assignment").value,
    td_lambda: Number(byId("pg-td-lambda").value),
    gamma_discount: Number(byId("pg-gamma-discount").value),
    neuron_threshold_variance: Number(byId("pg-threshold-variance").value),
    neuron_tau_m_variance: Number(byId("pg-tau-m-variance").value),
    inhibitory_fraction: Number(byId("pg-inhibitory-fraction").value),
    gaba_strength: Number(byId("pg-gaba-strength").value),
    e_i_ratio: Number(byId("pg-e-i-ratio").value),
    delay_distribution: byId("pg-delay-distribution").value,
    delay_mean_ticks: Number(byId("pg-delay-mean").value),
    refractory_variance: Number(byId("pg-refractory-variance").value),
    adaptation_strength: Number(byId("pg-adaptation-strength").value),
    adaptation_tau: Number(byId("pg-adaptation-tau").value),
    oscillation_enabled: byId("pg-oscillation-enabled").checked,
    oscillation_frequency: Number(byId("pg-oscillation-frequency").value),
    geometry_input_coupling: byId("pg-geometry-input-coupling").checked,
    geometry_input_sigma: Number(byId("pg-geometry-input-sigma").value),
    sandbox_enabled: byId("pg-sandbox-enabled").checked,
    sandbox_physics: "stick_figure",
    sandbox_action_coupling: "direct",
    sandbox_sensor_noise: Number(byId("pg-sandbox-sensor-noise").value),
  };
}

function ctxFor(id) {
  const canvas = byId(id), ctx = canvas?.getContext("2d");
  if (!canvas || !ctx) return null;
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.strokeStyle=getComputedStyle(document.body).color;
  ctx.fillStyle=getComputedStyle(document.body).color;
  ctx.globalAlpha=.75;
  return {canvas,ctx};
}

function drawSeries(id, values) {
  const item=ctxFor(id); if(!item||!values?.length)return;
  const {canvas,ctx}=item; const max=Math.max(1,...values),min=Math.min(0,...values); const range=Math.max(max-min,1e-9);
  ctx.beginPath(); values.forEach((value,i)=>{const x=8+i/Math.max(values.length-1,1)*(canvas.width-16);const y=canvas.height-8-(value-min)/range*(canvas.height-16);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});ctx.stroke();
}

function drawRaster(result){
  const item=ctxFor("pg-raster");if(!item)return;const{canvas,ctx}=item;const spikes=result.monitors?.spikes||[],ticks=result.config?.ticks||1,n=result.config?.n_neurons||1;
  for(const spike of spikes.slice(0,10000)){const x=8+spike.tick/Math.max(ticks-1,1)*(canvas.width-16);const y=8+spike.neuron_id/Math.max(n-1,1)*(canvas.height-16);ctx.fillRect(x,y,1.5,1.5);}
}

function drawTopology(result){
  const item=ctxFor("pg-topology-canvas");if(!item)return;const{canvas,ctx}=item;const coords=result.topology?.coordinates||[],edges=result.topology?.edges||[];const xy=coords.map(p=>[Number(p[0]||0),Number(p[1]||p[2]||0)]);
  ctx.globalAlpha=.1;ctx.beginPath();for(const[a,b]of edges.slice(0,2500)){if(!xy[a]||!xy[b])continue;ctx.moveTo(8+xy[a][0]*(canvas.width-16),8+xy[a][1]*(canvas.height-16));ctx.lineTo(8+xy[b][0]*(canvas.width-16),8+xy[b][1]*(canvas.height-16));}ctx.stroke();ctx.globalAlpha=.8;for(const p of xy)ctx.fillRect(7+p[0]*(canvas.width-16),7+p[1]*(canvas.height-16),3,3);
}

function drawState(result){
  const samples=result.monitors?.state_samples||[];if(!samples.length)return;const values=samples.map(s=>Number(s.v?.[0]??0));drawSeries("pg-state-canvas",values);
}

function drawSpectrum(result){
  const values=(result.analysis?.spike_time?.spectral_power||[]).map(item=>Number(item.power||0));drawSeries("pg-spectrum-canvas",values);
}

function drawDegree(result){
  const hist=result.analysis?.network?.degree_histogram||{};const pairs=Object.entries(hist).sort((a,b)=>Number(a[0])-Number(b[0]));drawSeries("pg-degree-canvas",pairs.map(([,count])=>Number(count)));
}

function renderResult(result){
  lastResult=result;const m=result.metrics||{},a=result.analysis||{},net=a.network||{},dim=a.dimensionality||{};
  const values=[["Class",result.manifest?.class||"PLAYGROUND"],["Spikes",m.total_spikes??"—"],["Mean Hz",Number(m.mean_rate_hz||0).toFixed(2)],["Active",Number(m.active_fraction||0).toLocaleString(undefined,{style:"percent",maximumFractionDigits:1})],["Neuronen",result.topology?.neuron_count??"—"],["Kanten",result.topology?.edge_count??"—"],["Dimensionen",result.topology?.dimensions??"—"],["Eff. Dim.",Number(dim.effective_dimensionality||0).toFixed(2)]];
  byId("pg-metrics").innerHTML=values.map(([k,v])=>`<div class="playground-metric"><span>${k}</span><strong>${v}</strong></div>`).join("");
  byId("pg-analysis-spike").textContent=JSON.stringify(a.spike_time||{},null,2);
  byId("pg-analysis-network").textContent=JSON.stringify({network:net,dimensionality:dim,ensemble:result.ensemble||null,pan:result.pan||null,closed_loop:result.closed_loop||null,heterogeneity:result.heterogeneity||null,temporal_dynamics:result.temporal_dynamics||null,geometry:result.geometry||null,gates:result.gates||null,clock:result.clock||null,execution:result.execution||null,growth:result.growth||null,storage:result.storage||null},null,2);
  byId("pg-analysis-plasticity").textContent=JSON.stringify({plasticity:a.plasticity||{},performance:a.performance||{},pan:result.pan||null,growth:result.growth||null,behavioral_learning:result.behavioral_learning||null,credit_assignment:result.credit_assignment||null,closed_loop:result.closed_loop||null,thalamic_gating:result.thalamic_gating||null,cortical_organization:result.cortical_organization||null,storage:result.storage||null,hardware:result.hardware||null},null,2);
  byId("pg-analysis-io").textContent=JSON.stringify({neural_io:result.neural_io||{status:"disabled"},interfaces:result.interfaces||null},null,2);
  byId("pg-run-json").textContent=JSON.stringify({session_id:result.session_id,manifest:result.manifest,model:result.model,config:result.config,metrics:result.metrics,readout:result.readout},null,2);
  drawRaster(result);drawSeries("pg-rate-canvas",(result.monitors?.tick_spike_counts||[]).map(Number));drawTopology(result);drawState(result);drawSpectrum(result);drawDegree(result);
}


function drawLiveSandbox(world){
  const item=ctxFor("pg-live-sandbox-canvas");if(!item||!world?.joints)return;
  const{canvas,ctx}=item;
  const px=p=>[canvas.width/2+Number(p.x||0)*170,canvas.height-30-Number(p.y||0)*150];
  const links=[["head","neck"],["neck","hip"],["neck","shoulder_l"],["neck","shoulder_r"],["hip","knee_l"],["hip","knee_r"],["knee_l","foot_l"],["knee_r","foot_r"]];
  ctx.globalAlpha=.8;ctx.beginPath();for(const[a,b]of links){if(!world.joints[a]||!world.joints[b])continue;const pa=px(world.joints[a]),pb=px(world.joints[b]);ctx.moveTo(pa[0],pa[1]);ctx.lineTo(pb[0],pb[1]);}ctx.stroke();
  for(const joint of Object.values(world.joints)){const p=px(joint);ctx.fillRect(p[0]-3,p[1]-3,6,6);}
}

let liveMonitorHistory=[];
let liveMonitorPaused=false;
let liveMonitorWorld=null;
let liveZoomKind=null;

function prepareLiveTileCanvases(root){
  root.querySelectorAll(".pg-live-monitor-tile canvas").forEach(canvas=>{canvas.width=880;canvas.height=480;canvas.dataset.pgLiveHiDpi="true";});
}

function resizeLiveZoomCanvas(){
  const canvas=byId("pg-live-zoom-canvas");if(!canvas)return;
  const bounds=canvas.getBoundingClientRect();const ratio=Math.min(2,window.devicePixelRatio||1);const width=Math.max(640,Math.round(bounds.width*ratio));const height=Math.max(360,Math.round(bounds.height*ratio));
  if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;}
}

function refreshLiveZoom(){
  if(!liveZoomKind)return;
  const dialog=byId("pg-live-zoom"),source=byId(`pg-live-tile-${liveZoomKind}`),target=byId("pg-live-zoom-canvas");if(!dialog?.open||!source||!target)return;
  resizeLiveZoomCanvas();const ctx=target.getContext("2d");ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,target.width,target.height);ctx.drawImage(source,0,0,target.width,target.height);
}

function ensureLiveMonitor(){
  let dialog=byId("pg-live-monitor");if(dialog)return dialog;
  dialog=document.createElement("dialog");dialog.id="pg-live-monitor";dialog.className="pg-live-monitor";
  dialog.innerHTML=`<header><div><span class="workspace-kicker">PAN LIVE MONITOR</span><h2>Live-Session</h2><p id="pg-live-monitor-status">Bereit</p></div><button type="button" class="pg-live-monitor-close" aria-label="Monitor schließen">×</button></header><div class="pg-live-monitor-body"><div class="pg-live-monitor-metrics"><div class="pg-live-monitor-metric"><span>Tick</span><strong id="pg-live-monitor-tick">0</strong></div><div class="pg-live-monitor-metric"><span>Spikes</span><strong id="pg-live-monitor-spikes">0</strong></div><div class="pg-live-monitor-metric"><span>Aktion</span><strong id="pg-live-monitor-action">—</strong></div><div class="pg-live-monitor-metric"><span>Reward</span><strong id="pg-live-monitor-reward">0</strong></div><div class="pg-live-monitor-metric"><span>Engine</span><strong id="pg-live-monitor-engine">—</strong></div></div><div class="pg-live-monitor-visuals"><button class="pg-live-monitor-tile" data-pg-live-expand="reset"><span>Reset</span><canvas id="pg-live-tile-reset" width="220" height="120"></canvas></button><button class="pg-live-monitor-tile" data-pg-live-expand="figure"><span>PAN-Männchen</span><canvas id="pg-live-tile-figure" width="220" height="120"></canvas></button><button class="pg-live-monitor-tile" data-pg-live-expand="raster"><span>Spike Raster</span><canvas id="pg-live-tile-raster" width="220" height="120"></canvas></button><button class="pg-live-monitor-tile" data-pg-live-expand="rate"><span>Populationsrate</span><canvas id="pg-live-tile-rate" width="220" height="120"></canvas></button><button class="pg-live-monitor-tile" data-pg-live-expand="topology"><span>Topologie · live</span><canvas id="pg-live-tile-topology" width="220" height="120"></canvas></button><button class="pg-live-monitor-tile" data-pg-live-expand="input"><span>Input</span><canvas id="pg-live-tile-input" width="220" height="120"></canvas></button><button class="pg-live-monitor-tile" data-pg-live-expand="output"><span>Output</span><canvas id="pg-live-tile-output" width="220" height="120"></canvas></button><button class="pg-live-monitor-tile" data-pg-live-expand="membrane"><span>Membranpotential</span><canvas id="pg-live-tile-membrane" width="220" height="120"></canvas></button><button class="pg-live-monitor-tile" data-pg-live-expand="spectrum"><span>Spectrum</span><canvas id="pg-live-tile-spectrum" width="220" height="120"></canvas></button><button class="pg-live-monitor-tile" data-pg-live-expand="degree"><span>Degree</span><canvas id="pg-live-tile-degree" width="220" height="120"></canvas></button></div><div class="pg-live-monitor-grid"><section class="pg-live-monitor-panel"><h3>Aktivität / Spike-Verlauf</h3><canvas id="pg-live-monitor-chart" width="760" height="260"></canvas></section><section class="pg-live-monitor-panel"><h3>Parameter</h3><pre id="pg-live-monitor-params" class="pg-live-monitor-params">—</pre></section><section class="pg-live-monitor-panel"><h3>Session</h3><pre id="pg-live-monitor-state" class="pg-live-monitor-params">—</pre></section></div><div class="pg-live-monitor-actions"><button type="button" id="pg-live-monitor-start" class="pg-monitor-primary">Start</button><button type="button" id="pg-live-monitor-pause">Pause</button><button type="button" id="pg-live-monitor-step">+32 Ticks</button><button type="button" id="pg-live-monitor-input">Input</button><button type="button" id="pg-live-monitor-stop">Stop</button><button type="button" id="pg-live-monitor-reset">Reset Ansicht</button></div></div>`;
  document.body.append(dialog);prepareLiveTileCanvases(dialog);
  dialog.querySelector(".pg-live-monitor-close").addEventListener("click",()=>dialog.close());
  dialog.querySelector("#pg-live-monitor-start").addEventListener("click",()=>{liveMonitorPaused=false;startLiveLoop().catch(error=>updateLiveMonitor({error:String(error.message||error)}));});
  dialog.querySelector("#pg-live-monitor-pause").addEventListener("click",()=>{liveMonitorPaused=true;stopLiveLoop();updateLiveMonitor({status:"paused"});});
  dialog.querySelector("#pg-live-monitor-step").addEventListener("click",()=>stepLiveSession().catch(error=>updateLiveMonitor({error:String(error.message||error)})));
  dialog.querySelector("#pg-live-monitor-input").addEventListener("click",()=>injectLiveInput().catch(error=>updateLiveMonitor({error:String(error.message||error)})));
  dialog.querySelector("#pg-live-monitor-stop").addEventListener("click",()=>stopLiveSession().catch(error=>updateLiveMonitor({error:String(error.message||error)})));
  dialog.querySelector("#pg-live-monitor-reset").addEventListener("click",()=>{liveMonitorHistory=[];drawLiveMonitorVisuals({});updateLiveMonitor({status:"reset"});});
  dialog.querySelectorAll("[data-pg-live-expand]").forEach(tile=>tile.addEventListener("click",()=>{if(tile.dataset.pgLiveExpand==="reset"){resetForm();liveMonitorHistory=[];drawLiveMonitorVisuals({});return;}openLiveZoom(tile.dataset.pgLiveExpand);}));
  ensureLiveZoom();
  return dialog;
}

function drawLiveMonitorChart(){
  const canvas=byId("pg-live-monitor-chart"),ctx=canvas?.getContext("2d");if(!canvas||!ctx)return;
  ctx.clearRect(0,0,canvas.width,canvas.height);ctx.strokeStyle=getComputedStyle(document.body).getPropertyValue("--accent")||"#b23a1a";ctx.lineWidth=2;ctx.beginPath();
  const max=Math.max(1,...liveMonitorHistory.map(item=>item.spikes));liveMonitorHistory.forEach((item,index)=>{const x=10+index/Math.max(1,liveMonitorHistory.length-1)*(canvas.width-20);const y=canvas.height-10-(item.spikes/max)*(canvas.height-20);if(index===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});ctx.stroke();
}

const LIVE_TILE_TITLES={reset:"Live-Ansicht zurückgesetzt",figure:"PAN-Männchen",raster:"Spike Raster",rate:"Populationsrate",topology:"Topologie",input:"Input-Kanäle",output:"Output-Aktionen",membrane:"Membranpotential",spectrum:"Spectrum",degree:"Degree-Verteilung"};
function ensureLiveZoom(){
  if(byId("pg-live-zoom"))return;
  const dialog=document.createElement("dialog");dialog.id="pg-live-zoom";dialog.className="pg-live-zoom";dialog.innerHTML=`<header><div><span class="workspace-kicker">LIVE DETAIL VIEW</span><strong id="pg-live-zoom-title">Live-Grafik</strong><p id="pg-live-zoom-state">Bereit</p></div><button type="button" id="pg-live-zoom-close" aria-label="Grafik schließen">×</button></header><div class="pg-live-zoom-toolbar"><button type="button" id="pg-live-zoom-start">Start</button><button type="button" id="pg-live-zoom-pause">Pause</button><button type="button" id="pg-live-zoom-step">Schritt</button><button type="button" id="pg-live-zoom-input">Input senden</button><button type="button" id="pg-live-zoom-reset">Reset</button><button type="button" id="pg-live-zoom-stop">Stop</button></div><div class="pg-live-zoom-stage"><canvas id="pg-live-zoom-canvas" width="1600" height="900"></canvas></div>`;document.body.append(dialog);dialog.querySelector("#pg-live-zoom-close").addEventListener("click",()=>{liveZoomKind=null;dialog.close();});dialog.querySelector("#pg-live-zoom-start").addEventListener("click",()=>startLiveLoop().catch(error=>updateLiveZoomState(error.message)));dialog.querySelector("#pg-live-zoom-pause").addEventListener("click",()=>{stopLiveLoop();updateLiveZoomState("Pausiert");});dialog.querySelector("#pg-live-zoom-step").addEventListener("click",()=>stepLiveSession().catch(error=>updateLiveZoomState(error.message)));dialog.querySelector("#pg-live-zoom-input").addEventListener("click",()=>injectLiveInput().catch(error=>updateLiveZoomState(error.message)));dialog.querySelector("#pg-live-zoom-reset").addEventListener("click",()=>{resetForm();liveMonitorHistory=[];drawLiveMonitorVisuals({});updateLiveZoomState("Ansicht zurückgesetzt");});dialog.querySelector("#pg-live-zoom-stop").addEventListener("click",()=>stopLiveSession().catch(error=>updateLiveZoomState(error.message)));dialog.addEventListener("close",()=>{liveZoomKind=null;});window.addEventListener("resize",refreshLiveZoom);
}
function updateLiveZoomState(message){const node=byId("pg-live-zoom-state");if(node)node.textContent=String(message||((liveMonitorPaused||!liveLoopTimer)?"Pausiert":"Läuft"));}
function openLiveZoom(kind){
  ensureLiveZoom();const dialog=byId("pg-live-zoom"),source=byId(`pg-live-tile-${kind}`);if(!dialog||!source)return;liveZoomKind=kind;byId("pg-live-zoom-title").textContent=LIVE_TILE_TITLES[kind]||kind;dialog.showModal();resizeLiveZoomCanvas();refreshLiveZoom();updateLiveZoomState();
}
function drawTileSeries(id,values,color){
  const canvas=byId(id),ctx=canvas?.getContext("2d");if(!canvas||!ctx)return;ctx.clearRect(0,0,canvas.width,canvas.height);ctx.strokeStyle=color||getComputedStyle(document.body).getPropertyValue("--accent")||"#b23a1a";ctx.lineWidth=2;ctx.beginPath();const data=values.length?values:[0];const max=Math.max(1,...data);data.forEach((value,index)=>{const x=5+index/Math.max(1,data.length-1)*(canvas.width-10);const y=canvas.height-5-(Number(value)||0)/max*(canvas.height-10);if(index===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});ctx.stroke();
}
function drawLiveMonitorVisuals(payload={}){
  const reset=byId("pg-live-tile-reset"),resetCtx=reset?.getContext("2d");if(reset&&resetCtx){resetCtx.clearRect(0,0,reset.width,reset.height);resetCtx.strokeStyle=getComputedStyle(document.body).getPropertyValue("--accent")||"#b23a1a";resetCtx.lineWidth=6;resetCtx.beginPath();resetCtx.arc(reset.width/2,reset.height/2,28,.5,Math.PI*1.85);resetCtx.stroke();resetCtx.beginPath();resetCtx.moveTo(160,35);resetCtx.lineTo(190,35);resetCtx.lineTo(177,58);resetCtx.stroke();}
  const spikes=Array.isArray(payload.recent_spikes)?payload.recent_spikes:[];const counts=Array.isArray(payload.output_counts)?payload.output_counts:[];const degrees=Array.isArray(payload.degree_values)?payload.degree_values:counts;const history=liveMonitorHistory.map(item=>item.spikes);drawTileSeries("pg-live-tile-rate",history);drawTileSeries("pg-live-tile-spectrum",history.map((value,index)=>Math.abs(Math.sin(index*.45))*value));drawTileSeries("pg-live-tile-degree",degrees.length?degrees:[0],getComputedStyle(document.body).getPropertyValue("--indigo")||"#2f4a7a");
  const raster=byId("pg-live-tile-raster"),rasterCtx=raster?.getContext("2d");if(raster&&rasterCtx){rasterCtx.clearRect(0,0,raster.width,raster.height);rasterCtx.fillStyle=getComputedStyle(document.body).getPropertyValue("--accent")||"#b23a1a";spikes.slice(-160).forEach(item=>{rasterCtx.fillRect((Number(item.tick)||0)%100/100*raster.width,(Number(item.neuron_id)||0)%128/128*raster.height,2,2);});}
  const membrane=byId("pg-live-tile-membrane"),mctx=membrane?.getContext("2d");if(membrane&&mctx){mctx.clearRect(0,0,membrane.width,membrane.height);mctx.strokeStyle=getComputedStyle(document.body).getPropertyValue("--moss")||"#2f5d47";mctx.lineWidth=2;const mean=Number(payload.mean_v??-65),min=Number(payload.min_v??-70),max=Number(payload.max_v??30);const y=membrane.height-5-(mean-min)/Math.max(1,max-min)*(membrane.height-10);mctx.beginPath();mctx.moveTo(5,y);mctx.lineTo(membrane.width-5,y);mctx.stroke();}
  const inputValues=[Number(payload.input_active_neurons||0),Number(payload.input_peak||0)];drawTileSeries("pg-live-tile-input",inputValues,getComputedStyle(document.body).getPropertyValue("--accent")||"#b23a1a");drawTileSeries("pg-live-tile-output",counts.length?counts:[0],getComputedStyle(document.body).getPropertyValue("--moss")||"#2f5d47");
  const topology=byId("pg-live-tile-topology"),tctx=topology?.getContext("2d"),topologyData=payload.topology; if(topology&&tctx){tctx.clearRect(0,0,topology.width,topology.height);const coords=topologyData?.coordinates||[],edges=topologyData?.edges||[];if(coords.length){const xs=coords.map(point=>Number(point[0]||0)),ys=coords.map(point=>Number(point[1]??point[2]??0)),minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys),scaleX=value=>(value-minX)/Math.max(1e-9,maxX-minX)*(topology.width-12)+6,scaleY=value=>(value-minY)/Math.max(1e-9,maxY-minY)*(topology.height-12)+6;tctx.strokeStyle=getComputedStyle(document.body).getPropertyValue("--rule-3")||"#777";tctx.globalAlpha=.25;edges.slice(0,600).forEach(edge=>{const source=coords[edge[0]],target=coords[edge[1]];if(!source||!target)return;tctx.beginPath();tctx.moveTo(scaleX(Number(source[0]||0)),scaleY(Number(source[1]??source[2]??0)));tctx.lineTo(scaleX(Number(target[0]||0)),scaleY(Number(target[1]??target[2]??0)));tctx.stroke();});tctx.globalAlpha=.9;tctx.fillStyle=getComputedStyle(document.body).getPropertyValue("--indigo")||"#2f4a7a";coords.forEach(point=>tctx.fillRect(scaleX(Number(point[0]||0))-1,scaleY(Number(point[1]??point[2]??0))-1,3,3));}}
  if(payload.world)liveMonitorWorld=payload.world;drawLiveMonitorFigure(liveMonitorWorld,"pg-live-tile-figure");refreshLiveZoom();
}

function drawLiveMonitorFigure(world,targetId="pg-live-tile-figure"){
  const canvas=byId(targetId),ctx=canvas?.getContext("2d");if(!canvas||!ctx)return;ctx.clearRect(0,0,canvas.width,canvas.height);ctx.strokeStyle=getComputedStyle(document.body).getPropertyValue("--indigo")||"#2f4a7a";ctx.fillStyle=getComputedStyle(document.body).getPropertyValue("--accent")||"#b23a1a";ctx.lineWidth=4;
  const joints=world?.joints||{};const px=point=>[canvas.width/2+Number(point?.x||0)*120,canvas.height-35-Number(point?.y||0)*110];const links=[["head","neck"],["neck","hip"],["neck","shoulder_l"],["neck","shoulder_r"],["hip","knee_l"],["hip","knee_r"],["knee_l","foot_l"],["knee_r","foot_r"]];ctx.beginPath();links.forEach(([a,b])=>{if(!joints[a]||!joints[b])return;const pa=px(joints[a]),pb=px(joints[b]);ctx.moveTo(pa[0],pa[1]);ctx.lineTo(pb[0],pb[1]);});ctx.stroke();Object.values(joints).forEach(joint=>{const p=px(joint);ctx.beginPath();ctx.arc(p[0],p[1],5,0,Math.PI*2);ctx.fill();});
}

function updateLiveMonitor(payload={}){
  const state=payload.state||payload;const tick=Number(state.tick??payload.tick??0);const spikes=Number(state.total_spikes??payload.total_spikes??0);const actions=payload.actions||state.actions||[];const rewards=payload.rewards||state.rewards||[];
  if(Number.isFinite(spikes)){liveMonitorHistory.push({tick,spikes});if(liveMonitorHistory.length>120)liveMonitorHistory.shift();}
  const set=(id,value)=>{const node=byId(id);if(node)node.textContent=String(value);};set("pg-live-monitor-tick",tick);set("pg-live-monitor-spikes",spikes);set("pg-live-monitor-action",actions.length?actions[actions.length-1]:"—");set("pg-live-monitor-reward",rewards.length?Number(rewards[rewards.length-1]).toFixed(3):"0");set("pg-live-monitor-engine",state.execution?.current_engine||payload.execution?.current_engine||"—");set("pg-live-monitor-status",payload.error||((liveMonitorPaused||!liveLoopTimer)?"Pausiert":"Läuft"));
  const params={session_id:liveSessionId,tick,posture_score:payload.posture_score??payload.world?.posture_score??null,reward:payload.reward??null,reward_events:payload.reward_events||[],terminal:payload.terminal||null,pan_bias_current:byId("pg-pan-bias-current")?.value,feedback_gain:byId("pg-pan-feedback-gain")?.value,learning_rate:byId("pg-behavior-lr")?.value,epsilon:byId("pg-behavior-epsilon")?.value,edge_budget:byId("pg-edges")?.value};const paramsNode=byId("pg-live-monitor-params");if(paramsNode)paramsNode.textContent=JSON.stringify(params,null,2);const stateNode=byId("pg-live-monitor-state");if(stateNode)stateNode.textContent=JSON.stringify({state_digest:state.state_digest||payload.state_digest||null,input_queue_depth:state.input_queue_depth??payload.input_queue_depth??0,learning:state.learning||payload.learning||null},null,2);drawLiveMonitorChart();drawLiveMonitorVisuals(payload);drawLiveMonitorFigure(payload.world||state.world||null);updateLiveZoomState(payload.error);
}

async function createLiveSession(canRecover=true){
  const payload={...formPayload(),neuron_model:"pan_adex_5d",pan_enabled:true,thalamic_relay_threshold:0,pan_bias_current:Number(byId("pg-pan-bias-current").value),behavior_target_mode:byId("pg-behavior-target-mode").value};
  try{
    const result=await apiPost("/api/playground/live/create",payload);liveSessionId=result.session_id;liveMonitorHistory=[];liveMonitorWorld=null;const monitor=ensureLiveMonitor();if(!monitor.open)monitor.showModal();byId("pg-live-state").textContent=JSON.stringify(result,null,2);updateLiveMonitor(result.state||result);
  }catch(error){
    if(canRecover&&/maximum live Playground sessions reached/i.test(String(error.message||error))){await clearLiveSessions();return createLiveSession(false);}
    throw error;
  }
}
async function openLiveMonitor(){
  if(liveSessionId){const monitor=ensureLiveMonitor();if(!monitor.open)monitor.showModal();return;}
  await createLiveSession();
}
async function clearLiveSessions(){
  stopLiveLoop();
  let result;
  try{result=await apiPost("/api/playground/live/stop-all",{});}catch{
    const listing=await apiGet("/api/playground/live");
    const sessions=Array.isArray(listing?.sessions)?listing.sessions:[];
    await Promise.all(sessions.map(session=>apiPost(`/api/playground/live/${encodeURIComponent(session.session_id)}/stop`,{}).catch(()=>null)));
    result={classification:"PLAYGROUND_LIVE_SESSIONS_CLEARED",scientific_evidence:false,cleared:sessions.length,compatibility_cleanup:true};
  }
  liveSessionId=null;liveMonitorWorld=null;liveMonitorHistory=[];
  byId("pg-live-state").textContent=JSON.stringify(result,null,2);
  const monitor=byId("pg-live-monitor");if(monitor?.open)monitor.close();
}
async function stepLiveSession(){
  if(!liveSessionId)throw new Error("Zuerst Live-Session starten.");
  const result=await apiPost(`/api/playground/live/${encodeURIComponent(liveSessionId)}/step`,{ticks:32});
  try{const sandbox=await apiPost(`/api/playground/live/${encodeURIComponent(liveSessionId)}/sandbox`,{ticks:8});result.world=sandbox.world;liveMonitorWorld=sandbox.world;}catch{}
  try{Object.assign(result,await apiGet(`/api/playground/live/${encodeURIComponent(liveSessionId)}`));}catch{}
  byId("pg-live-state").textContent=JSON.stringify(result,null,2);updateLiveMonitor(result);
}
async function startLiveLoop(){
  if(!liveSessionId)throw new Error("Zuerst Live-Session starten.");
  if(liveLoopTimer)return;
  liveMonitorPaused=false;if(!byId("pg-live-monitor")?.open)ensureLiveMonitor().showModal();updateLiveMonitor({status:"running"});
  liveLoopTimer=setInterval(()=>{stepLiveSession().catch(error=>{byId("pg-live-state").textContent=String(error.message||error);stopLiveLoop();});},250);
}
function stopLiveLoop(){
  if(liveLoopTimer){clearInterval(liveLoopTimer);liveLoopTimer=null;liveMonitorPaused=true;updateLiveMonitor({status:"paused"});}
}

async function injectLiveInput(){
  if(!liveSessionId)throw new Error("Zuerst Live-Session starten.");
  let values;try{values=JSON.parse(byId("pg-live-input-values").value);}catch{throw new Error("Live Input muss gültiges JSON sein.");}
  if(!Array.isArray(values))throw new Error("Live Input muss ein Array sein.");
  const result=await apiPost(`/api/playground/live/${encodeURIComponent(liveSessionId)}/input`,{values,duration_ticks:16,gain:25});byId("pg-live-state").textContent=JSON.stringify(result,null,2);updateLiveMonitor(result);
}
async function stepLiveSandbox(){
  if(!liveSessionId)throw new Error("Zuerst Live-Session starten.");
  const result=await apiPost(`/api/playground/live/${encodeURIComponent(liveSessionId)}/sandbox`,{ticks:8});liveMonitorWorld=result.world||null;byId("pg-live-state").textContent=JSON.stringify(result,null,2);drawLiveSandbox(result.world);updateLiveMonitor(result);
}
async function stopLiveSession(){
  stopLiveLoop();
  if(!liveSessionId)return;
  const result=await apiPost(`/api/playground/live/${encodeURIComponent(liveSessionId)}/stop`,{});byId("pg-live-state").textContent=JSON.stringify(result,null,2);updateLiveMonitor(result);liveSessionId=null;liveMonitorPaused=true;
}

function renderNightStatus(result){
  const node=byId("pg-night-state");if(!node)return;
  const s=result?.status||result||{},pan=s.pan||{},execution=pan.execution||{};
  const compact={
    active:Boolean(result?.active),
    run_id:result?.run_id||s.run_id||null,
    episode:s.episode??0,
    max_episodes:s.max_episodes??0,
    elapsed_seconds:Number(s.elapsed_seconds||0).toFixed(1),
    mean_reward:Number(s.mean_reward||0).toFixed(4),
    total_reward:Number(s.total_reward||0).toFixed(3),
    task_counts:s.task_counts||{},
    knowledge_records:s.knowledge_records??0,
    relations:s.relations??0,
    total_spikes:pan.total_spikes??0,
    engine:execution.current_engine||null,
    errors:s.errors||[],
    last_error:result?.last_error||null,
  };
  node.textContent=JSON.stringify(compact,null,2);
  if(result?.active)startNightPolling();else stopNightPolling();
}
async function refreshNightStatus(){
  const result=await apiGet("/api/playground/night");renderNightStatus(result);return result;
}
function startNightPolling(){
  if(nightPollTimer)return;
  nightPollTimer=setInterval(()=>refreshNightStatus().catch(error=>{const node=byId("pg-night-state");if(node)node.textContent=String(error.message||error);}),2000);
}
function stopNightPolling(){if(nightPollTimer){clearInterval(nightPollTimer);nightPollTimer=null;}}
async function startNightRun(){
  const result=await apiPost("/api/playground/night/start",{
    hours:Number(byId("pg-night-hours").value),
    max_episodes:Number(byId("pg-night-episodes").value),
    checkpoint_seconds:Number(byId("pg-night-checkpoint").value),
    seed:Number(byId("pg-night-seed").value),
  });
  renderNightStatus(result);
}
async function stopNightRun(){
  const result=await apiPost("/api/playground/night/stop",{});renderNightStatus(result);
}

async function checkCpuDeterminism(){
  const node=byId("pg-cuda-compiler-state");
  if(node)node.textContent="CPU-Referenz wird zweimal mit identischem Seed ausgeführt …";
  const payload={...formPayload(),persist:false,ensemble_runs:1,freeze_actions:false,freeze_rewards:false,parity_reference_commit:""};
  const result=await apiPost("/api/playground/determinism",payload);
  if(node)node.textContent=JSON.stringify({
    classification:result.classification,
    passed:result.passed,
    spike_train_exact:result.spike_train_exact,
    projection_exact:result.projection_exact,
    fingerprint_first:result.fingerprint_first,
    fingerprint_second:result.fingerprint_second,
    reference:result.reference,
    parity_contract:catalogState?.cuda_parity||null,
    gpu_execution_status:catalogState?.pan?.cuda_backend_status||"UNKNOWN",
  },null,2);
  if(result.passed&&result.reference){
    lastResult=lastResult||{};
    lastResult.closed_loop={
      ...(lastResult.closed_loop||{}),
      action_history:result.reference.action_sequence||[],
      reward_history:result.reference.reward_sequence||[],
    };
  }
  return result;
}

function cudaRequestPayload(){
  return {
    ...formPayload(),
    target_sm:byId("pg-cuda-target-sm")?.value||"sm_86",
    ptx_version:byId("pg-cuda-ptx-version")?.value||"7.1",
    n_neurons:Number(byId("pg-cuda-neurons")?.value||256),
    block_size:Number(byId("pg-cuda-block-size")?.value||64),
    device_ordinal:Number(byId("pg-cuda-device")?.value||0),
    reference_commit:byId("pg-parity-reference-commit")?.value||"",
    rng_samples:Number(byId("pg-cuda-rng-samples")?.value||1000),
  };
}

async function refreshCudaStatus(){
  const node=byId("pg-cuda-stage-state");
  if(node)node.textContent="CUDA-Laufzeit wird geprüft …";
  const result=await apiGet("/api/playground/cuda/status");
  if(node)node.textContent=JSON.stringify({
    target_default:result.target_default,
    ptxas_available:result.ptxas_available,
    cuda_driver_available:result.cuda_driver_available,
    cuda_driver_error:result.cuda_driver_error,
    stages:result.stages,
    application_cpu:result.application_cpu,
    gpu_porting:result.gpu_porting,
    verification:result.verification,
  },null,2);
  return result;
}

async function runCudaPreflight(){
  const node=byId("pg-cuda-resource-state");
  if(node)node.textContent="ptxas + Driver-Load + Occupancy werden geprüft …";
  const result=await apiPost("/api/playground/cuda/preflight",cudaRequestPayload());
  if(node)node.textContent=JSON.stringify({
    execution_status:result.execution_status,
    ready_for_cooperative_launch:result.ready_for_cooperative_launch,
    ptxas:result.ptxas,
    cooperative:result.cooperative,
  },null,2);
  return result;
}

async function runCudaHardwareSmoke(){
  const node=byId("pg-cuda-parity-state");
  if(node)node.textContent="GPU-Kernel wird zweimal ausgeführt und gegen CPU-Gate-ABI verglichen …";
  const payload={...cudaRequestPayload(),n_neurons:Math.min(Number(byId("pg-cuda-neurons")?.value||64),4096)};
  const result=await apiPost("/api/playground/cuda/smoke",payload);
  const first=result.first||{},ptxas=first.ptxas||{};
  if(node)node.textContent=JSON.stringify({
    passed:result.passed,
    gpu_repeat_exact:result.gpu_repeat_exact,
    parity:result.parity,
    launch:first.launch,
    registers:ptxas.registers,
    shared_bytes:ptxas.shared_bytes,
    spill_store_bytes:ptxas.spill_store_bytes,
    spill_load_bytes:ptxas.spill_load_bytes,
    cleanup_contract:result.cleanup_contract,
  },null,2);
  const resources=byId("pg-cuda-resource-state");
  if(resources)resources.textContent=JSON.stringify({
    ptxas:first.ptxas||null,
    launch:first.launch||null,
  },null,2);
  return result;
}

async function runCudaRngParity(){
  const node=byId("pg-cuda-rng-state");
  if(node)node.textContent="ε-greedy-Hashpfad wird CPU ↔ CUDA verglichen …";
  const result=await apiPost("/api/playground/cuda/rng-parity",cudaRequestPayload());
  if(node)node.textContent=JSON.stringify(result,null,2);
  return result;
}

async function compileCudaGates(){
  const node=byId("pg-cuda-compiler-state");
  if(node)node.textContent="Gate-IR/PTX wird erzeugt …";
  const result=await apiPost("/api/playground/cuda/compile",{
    ...formPayload(),
    target_sm:byId("pg-cuda-target-sm")?.value||"sm_86",
    ptx_version:byId("pg-cuda-ptx-version")?.value||"7.1",
  });
  if(node)node.textContent=JSON.stringify({
    manifest:result.manifest,
    gate_ir:result.gate_ir,
    ptx_preview:String(result.ptx||"").split("\n").slice(0,80).join("\n"),
    cuda_preview:String(result.cuda_source||"").split("\n").slice(0,80).join("\n"),
  },null,2);
  return result;
}

async function runSession(){
  const status=byId("pg-status");status.dataset.state="running";status.textContent="Playground läuft …";
  try{const result=await apiPost("/api/playground/run",formPayload());renderResult(result);status.dataset.state="ok";status.textContent=`Lauf abgeschlossen · ${result.session_id} · PLAYGROUND · keine Evidenz`;window.MHRNWorkspaceArchitecture?.selectRoute?.("playground","run");if(result.persisted_path)await refreshSessions();}
  catch(error){status.dataset.state="error";status.textContent=`Playground fehlgeschlagen: ${error.message||error}`;}
}

async function runRobustness(){
  const status=byId("pg-status");status.dataset.state="running";status.textContent="Explorative Robustheitskontrollen laufen …";
  try{const result=await apiPost("/api/playground/robustness",{...formPayload(),persist:false,ensemble_runs:1});status.dataset.state="ok";status.textContent="Robustheitssuite abgeschlossen · nicht preregistriert · keine Evidenz";lastResult=result;byId("pg-run-json").textContent=JSON.stringify(result,null,2);window.MHRNWorkspaceArchitecture?.selectRoute?.("playground","run");}
  catch(error){status.dataset.state="error";status.textContent=`Robustheitssuite fehlgeschlagen: ${error.message||error}`;}
}

function setBuilderValue(key,value){
  const aliases={
    n_neurons:"neurons",edge_budget:"edges",dimensions:"dimensions",ticks:"ticks",weight:"weight",delay_ticks:"delay",radius:"radius",k_neighbors:"k",rewiring_probability:"rewire",modules:"modules",stimulus_current:"current",stimulus_rate_hz:"rate",seed:"seed",ensemble_runs:"ensemble",
    pan_dimensions:"pan-dimensions",pan_closed_loop:"pan-closed-loop",pan_health_decay:"pan-health-decay",pan_apoptosis_threshold:"pan-apoptosis",pan_bias_current:"pan-bias-current",
    cortical_layer_count:"cortical-layers",behavior_action_count:"behavior-actions",behavior_target_action:"behavior-target",behavior_episode_ticks:"behavior-episode",behavior_bias_current:"behavior-bias",
    input_amplitude_per_channel:"input-amplitudes",input_frequency_per_channel:"input-frequencies",input_phase_per_channel:"input-phases",input_channel_map:"input-channel-map",
    pan_feedback_gain:"pan-feedback-gain",pan_feedback_nonlinearity:"pan-feedback-nonlinearity",pan_feedback_saturation:"pan-feedback-saturation",
    action_loop_enabled:"action-loop-enabled",action_loop_delay:"action-loop-delay",action_persistence:"action-persistence",action_to_input_map:"action-to-input-map",action_space_size:"action-space-size",action_coupling_strength:"action-coupling",action_noise:"action-noise",
    reward_signal_enabled:"reward-enabled",reward_magnitude:"reward-magnitude",reward_delay_ticks:"reward-delay",reward_shaping:"reward-shaping",reward_baseline:"reward-baseline",reward_decay:"reward-decay",reward_channel:"reward-channel",
    target_encoding:"target-encoding",target_cue_channel:"target-cue-channel",target_cue_current:"target-cue-current",target_persistence:"target-persistence",target_shuffle:"target-shuffle",target_predictability:"target-predictability",
    credit_assignment:"credit-assignment",credit_window:"credit-window",eligibility_trace_tau:"eligibility-tau",td_lambda:"td-lambda",gamma_discount:"gamma-discount",
    neuron_threshold_variance:"threshold-variance",neuron_tau_m_variance:"tau-m-variance",inhibitory_fraction:"inhibitory-fraction",gaba_strength:"gaba-strength",e_i_ratio:"e-i-ratio",delay_distribution:"delay-distribution",delay_mean_ticks:"delay-mean",
    refractory_variance:"refractory-variance",adaptation_strength:"adaptation-strength",adaptation_tau:"adaptation-tau",oscillation_enabled:"oscillation-enabled",oscillation_frequency:"oscillation-frequency",
    input_topology:"input-topology",input_channels:"input-channels",input_noise_sigma:"input-noise",action_feedback_channel:"action-feedback-channel",reward_cue_channel:"reward-cue-channel",
    geometry_input_coupling:"geometry-input-coupling",geometry_input_sigma:"geometry-input-sigma",sandbox_enabled:"sandbox-enabled",sandbox_sensor_noise:"sandbox-sensor-noise",
    neuron_model:"neuron-model",synapse_model:"synapse-model",plasticity_rule:"plasticity",topology:"topology",readout:"readout",pan_enabled:"pan-enabled",behavior_learning_enabled:"behavior-enabled",stimulus:"stimulus",
    weight_decay:"weight-decay",weight_max_clamp:"weight-max-clamp",persist:"persist",clock_mode:"clock-mode",clock_base_hz:"clock-base-hz",clock_event_batch_ms:"clock-event-batch",execution_mode:"execution-mode",execution_initial_mode:"execution-initial",execution_theta_high:"execution-high",execution_theta_low:"execution-low",execution_hysteresis:"execution-hysteresis",execution_min_dwell:"execution-dwell",execution_activity_window:"execution-window",execution_transition_mode:"execution-transition",execution_sync_on_switch:"execution-sync",execution_log_transitions:"execution-log",growth_enabled:"growth-enabled",growth_activity_threshold:"growth-activity",growth_coactivation_threshold:"growth-coactivation",growth_information_threshold:"growth-info",growth_prune_threshold:"growth-prune",growth_max_synapses_per_neuron:"growth-max-synapses",growth_max_new_synapses_per_barrier:"growth-max-new",hardware_profile_name:"hardware-profile",cuda_budget_mb:"cuda-budget",offload_enabled:"offload-enabled",offload_snapshot_interval:"offload-snapshot",thalamic_gating_enabled:"thalamic-enabled",thalamic_relay_threshold:"thalamic-threshold",thalamic_attention_gain:"thalamic-attention",thalamic_inhibition_gain:"thalamic-inhibition",cortical_layers_enabled:"cortical-enabled",cortical_plasticity:"cortical-plasticity",cortical_learning_rate:"cortical-lr",behavior_target_mode:"behavior-target-mode",behavior_min_activity:"behavior-min-activity",behavior_learning_rate:"behavior-lr",behavior_epsilon:"behavior-epsilon",geometry_lambda_a:"geometry-lambda-a",geometry_lambda_b:"geometry-lambda-b",geometry_sigma:"geometry-sigma",geometry_p0:"geometry-p0",geometry_mode:"geometry-mode",geometry_delay_velocity:"geometry-delay-velocity",neural_io_enabled:"neural-io-enabled",neural_io_input_channels:"neural-io-input-channels",neural_io_output_channels:"neural-io-output-channels",neural_io_input_codec:"neural-io-codec",neural_io_output_decoder:"neural-io-decoder",neural_io_window_ticks:"neural-io-window",neural_io_input_current:"neural-io-current",neural_io_input_role:"neural-io-input-role",neural_io_output_role:"neural-io-output-role",neural_io_phase:"neural-io-phase",neural_io_modality:"neural-io-modality",neural_io_source_id:"neural-io-source",posture_score_channel:"posture-score-channel",reward_event_channel:"reward-event-channel",posture_current_scale:"posture-current-scale",reward_event_scale:"reward-event-scale",posture_reward_enabled:"posture-reward-enabled",posture_weight_upright:"posture-weight-upright",posture_weight_height:"posture-weight-height",posture_weight_stability:"posture-weight-stability",posture_weight_symmetry:"posture-weight-symmetry",posture_target_height:"posture-target-height",posture_tilt_max:"posture-tilt-max",posture_velocity_max:"posture-velocity-max",trigger_good_score:"trigger-good-score",trigger_good_duration:"trigger-good-duration",trigger_good_reward:"trigger-good-reward",trigger_warning_score:"trigger-warning-score",trigger_warning_reward:"trigger-warning-reward",trigger_falling_rate:"trigger-falling-rate",trigger_falling_reward:"trigger-falling-reward",trigger_collapse_score:"trigger-collapse-score",trigger_collapse_reward:"trigger-collapse-reward",trigger_recovery_bonus:"trigger-recovery-bonus",reward_continuous_alpha:"reward-continuous-alpha",episode_termination_enabled:"episode-termination-enabled",episode_max_ticks:"episode-max-ticks",episode_reset_on_collapse:"episode-reset-on-collapse",pan_feedback_delay:"pan-feedback-delay",pan_feedback_source:"pan-feedback-source",pan_feedback_target:"pan-feedback-target",pan_feedback_threshold:"pan-feedback-threshold",freeze_actions:"freeze-actions",freeze_rewards:"freeze-rewards",parity_reference_commit:"parity-reference-commit"
  };
  const id="pg-"+(aliases[key]||key.replaceAll("_","-"));
  const el=byId(id);if(!el)return;
  if(el.type==="checkbox")el.checked=Boolean(value);
  else if(Array.isArray(value))el.value=JSON.stringify(value);
  else el.value=String(value);
}

function readSavedPlaygroundPresets(){
  try{return JSON.parse(localStorage.getItem(PLAYGROUND_PRESETS_STORAGE)||"{}");}catch{return {};}
}

function writeSavedPlaygroundPresets(presets){localStorage.setItem(PLAYGROUND_PRESETS_STORAGE,JSON.stringify(presets));}
function allPlaygroundPresets(){
  const catalogPresets=Object.fromEntries((catalogState?.closed_loop?.presets||[]).map(item=>[item.name,{...item,source:"catalog"}]));
  return {...BUILTIN_PLAYGROUND_PRESETS,...catalogPresets,...readSavedPlaygroundPresets()};
}

function renderUserPresetOptions(){
  const select=byId("pg-user-preset-select");if(!select)return;
  const selected=select.value;
  const presets=allPlaygroundPresets();
  select.innerHTML=Object.entries(presets).map(([name,preset])=>`<option value="${playgroundEscape(name)}">${playgroundEscape(preset.label||name)} · ${preset.source==="catalog"?"Katalog":BUILTIN_PLAYGROUND_PRESETS[name]?"integriert":"Browser"}</option>`).join("");
  if(selected&&presets[selected])select.value=selected;else if(!select.value)select.value=presets[DEFAULT_PLAYGROUND_PRESET]?DEFAULT_PLAYGROUND_PRESET:"pan_exploration";
  const preset=presets[select.value];
  if(byId("pg-user-preset-description"))byId("pg-user-preset-description").textContent=preset?.description||"Preset auswählen oder eigene Einstellungen speichern.";
}

function applyUserPreset(){
  const name=byId("pg-user-preset-select")?.value;const preset=allPlaygroundPresets()[name];if(!preset)return;
  const settings=preset.source==="catalog"?resolvedPresetSettings(name):preset.settings||{};
  Object.entries(settings).forEach(([key,value])=>setBuilderValue(key,value));
  updateDefaultHints();
  if(byId("pg-user-preset-description"))byId("pg-user-preset-description").textContent=`${preset.description||name}\nQuelle: ${preset.source==="catalog"?"Presetkatalog":BUILTIN_PLAYGROUND_PRESETS[name]?"integriert":"lokal"}${preset.expected_success!=null?`\nErwartung: ${preset.expected_success}`:""}`;
}

function saveUserPreset(){
  const name=byId("pg-user-preset-name")?.value.trim();if(!name){byId("pg-user-preset-description").textContent="Bitte zuerst einen Namen vergeben.";return;}
  const key=name.toLowerCase().replace(/[^a-z0-9]+/g,"_").replace(/^_|_$/g,"")||`preset_${Date.now()}`;
  const presets=readSavedPlaygroundPresets();presets[key]={label:name,description:"Eigene lokal gespeicherte Playground-Konfiguration.",settings:formPayload(),saved_at:new Date().toISOString()};writeSavedPlaygroundPresets(presets);renderUserPresetOptions();byId("pg-user-preset-select").value=key;byId("pg-user-preset-description").textContent=`${name}\nLokal gespeichert.`;
}

function deleteUserPreset(){
  const select=byId("pg-user-preset-select");const name=select?.value;if(!name||BUILTIN_PLAYGROUND_PRESETS[name])return;
  const presets=readSavedPlaygroundPresets();delete presets[name];writeSavedPlaygroundPresets(presets);renderUserPresetOptions();
}

function resolvedPresetSettings(name,seen=new Set()){
  const presets=catalogState?.closed_loop?.presets||[];
  const preset=presets.find(item=>item.name===name);
  if(!preset||seen.has(name))return {};
  const settings={...(preset.settings||{})};
  const parent=settings.closed_loop_preset;
  delete settings.closed_loop_preset;
  return parent?{...resolvedPresetSettings(parent,new Set([...seen,name])),...settings}:settings;
}

function resetForm(){
  const values={neurons:"128",edges:"1024",weight:"4","weight-decay":"0","weight-max-clamp":"100",ticks:"256",dimensions:"5",delay:"1",radius:"0.35",k:"16",rewire:"0.15",modules:"2",current:"8",rate:"20",seed:"12345",ensemble:"1","pan-dimensions":"5","pan-feedback-gain":"0.05","pan-health-decay":"0.001","pan-apoptosis":"0.1","pan-bias-current":"10","geometry-lambda-a":"0.5","geometry-lambda-b":"0.5","geometry-sigma":"0.1","geometry-p0":"0.3","geometry-delay-velocity":"0.25","clock-base-hz":"100","clock-event-batch":"10","execution-high":"0.30","execution-low":"0.05","execution-hysteresis":"0.02","execution-dwell":"100","execution-window":"100","growth-activity":"0.25","growth-coactivation":"2","growth-info":"0.25","growth-prune":"0.05","growth-max-synapses":"128","growth-max-new":"8","cuda-budget":"2048","offload-snapshot":"1000","thalamic-threshold":"0","thalamic-attention":"1.15","thalamic-inhibition":"0.35","cortical-layers":"6","cortical-lr":"0.01","behavior-actions":"4","behavior-target":"0","behavior-min-activity":"0.01","behavior-lr":"0.2","behavior-epsilon":"0.2","behavior-episode":"16","behavior-bias":"3"};
  for(const[k,v]of Object.entries(values)){const el=byId(`pg-${k}`);if(el)el.value=v;}byId("pg-persist").checked=false;byId("pg-pan-enabled").checked=false;byId("pg-pan-closed-loop").checked=true;byId("pg-clock-mode").value="continuous";byId("pg-execution-mode").value="HYBRID_AUTO";byId("pg-execution-initial").value="EVENT_ONLY";byId("pg-execution-transition").value="clean";byId("pg-execution-sync").checked=true;byId("pg-execution-log").checked=true;byId("pg-growth-enabled").checked=false;byId("pg-offload-enabled").checked=false;byId("pg-hardware-profile").value="reference_cpu";byId("pg-thalamic-enabled").checked=false;byId("pg-behavior-target-mode").value="cycle";byId("pg-cortical-enabled").checked=false;byId("pg-cortical-plasticity").checked=true;byId("pg-behavior-enabled").checked=false;byId("pg-geometry-mode").value="mixed_additive";byId("pg-neural-io-enabled").checked=false;byId("pg-neural-io-payload").value="0.5";byId("pg-neural-io-input-channels").value="16";byId("pg-neural-io-output-channels").value="16";byId("pg-neural-io-window").value="16";byId("pg-neural-io-current").value="25";byId("pg-neural-io-input-role").value="GATEWAY_AFFERENT";byId("pg-neural-io-output-role").value="GATEWAY_EFFERENT";byId("pg-neural-io-phase").value="QUERY";byId("pg-neural-io-modality").value="digital";byId("pg-neural-io-source").value="playground.input";if(byId("pg-topology"))byId("pg-topology").value="mhrn_5d";
  const closedLoopDefaults={
    "input-topology":"uniform","input-channels":"1","input-channel-map":"[]","input-amplitudes":"[]","input-frequencies":"[]","input-phases":"[]","input-noise":"0","target-cue-channel":"0","reward-cue-channel":"0","action-feedback-channel":"0",
    "pan-feedback-delay":"0","pan-feedback-source":"population","pan-feedback-target":"all","pan-feedback-nonlinearity":"linear","pan-feedback-threshold":"0","pan-feedback-saturation":"100",
    "action-loop-delay":"1","action-persistence":"1","action-to-input-map":"auto","action-space-size":"4","action-coupling":"0","action-noise":"0","geometry-input-sigma":"0.2","sandbox-sensor-noise":"0.05",
    "target-encoding":"none","target-persistence":"1","target-cue-current":"0","target-predictability":"deterministic",
    "reward-magnitude":"1","reward-delay":"0","reward-shaping":"sparse","reward-baseline":"0","reward-decay":"0","reward-channel":"0",
    "credit-assignment":"none","credit-window":"64","eligibility-tau":"200","td-lambda":"0.9","gamma-discount":"0.95",
    "threshold-variance":"0","tau-m-variance":"0","inhibitory-fraction":"0","gaba-strength":"1","e-i-ratio":"1","delay-distribution":"fixed","delay-mean":"1","refractory-variance":"0","adaptation-strength":"0","adaptation-tau":"200","oscillation-frequency":"8"
  };
  Object.entries(closedLoopDefaults).forEach(([key,value])=>{const el=byId("pg-"+key);if(el)el.value=value;});
  ["pg-action-loop-enabled","pg-geometry-input-coupling","pg-sandbox-enabled","pg-target-shuffle","pg-reward-enabled","pg-oscillation-enabled"].forEach(id=>{const el=byId(id);if(el)el.checked=false;});
  const postureDefaults={posture_score_channel:2,reward_event_channel:3,posture_current_scale:25,reward_event_scale:25,posture_reward_enabled:false,posture_weight_upright:0.4,posture_weight_height:0.3,posture_weight_stability:0.2,posture_weight_symmetry:0.1,posture_target_height:1,posture_tilt_max:1,posture_velocity_max:5,trigger_good_score:0.85,trigger_good_duration:10,trigger_good_reward:1,trigger_warning_score:0.4,trigger_warning_reward:-0.3,trigger_falling_rate:-0.05,trigger_falling_reward:-1,trigger_collapse_score:0.1,trigger_collapse_reward:-5,trigger_recovery_bonus:2,reward_continuous_alpha:0.1,episode_termination_enabled:true,episode_max_ticks:256,episode_reset_on_collapse:true};Object.entries(postureDefaults).forEach(([key,value])=>setBuilderValue(key,value));
  if(catalogState&&byId("pg-user-preset-select")&&allPlaygroundPresets()[DEFAULT_PLAYGROUND_PRESET]){byId("pg-user-preset-select").value=DEFAULT_PLAYGROUND_PRESET;applyUserPreset();return;}
  updateDefaultHints();
}

async function refreshSessions(){
  const root=byId("pg-session-list");if(!root)return;
  try{const data=await apiGet("/api/playground/sessions"),sessions=data.sessions||[];root.innerHTML=sessions.length?sessions.map(s=>`<article class="playground-session"><div><strong>${s.name||s.session_id}</strong><small>${s.session_id} · ${s.created_at||""} · ${s.class||"PLAYGROUND"}</small></div><button type="button" data-pg-replay="${s.session_id}">Replay</button></article>`).join(""):"<p>Noch keine lokal gespeicherten Playground-Sessions.</p>";root.querySelectorAll("[data-pg-replay]").forEach(button=>button.addEventListener("click",async()=>{try{const result=await apiGet(`/api/playground/sessions/${encodeURIComponent(button.dataset.pgReplay)}`);renderResult(result);window.MHRNWorkspaceArchitecture?.selectRoute?.("playground","run");}catch(error){root.textContent=`Replay fehlgeschlagen: ${error.message}`;}}));}
  catch(error){root.textContent=`Sessions nicht verfügbar: ${error.message}`;}
}

function ensureCatalogInfoDialog(){
  let dialog=byId("pg-catalog-info-dialog");if(dialog)return dialog;
  dialog=document.createElement("dialog");dialog.id="pg-catalog-info-dialog";dialog.className="playground-catalog-dialog";dialog.innerHTML='<header><div><p id="pg-catalog-info-category">Component</p><h2 id="pg-catalog-info-title">—</h2></div><button type="button" id="pg-catalog-info-close" aria-label="Close component information">×</button></header><div id="pg-catalog-info-body" class="playground-catalog-dialog-body"></div>';
  document.body.append(dialog);dialog.querySelector("#pg-catalog-info-close").addEventListener("click",()=>dialog.close());return dialog;
}

function showCatalogInfo(item){
  activeCatalogInfo=item;const language=catalogLanguage();const dialog=ensureCatalogInfoDialog();const category=catalogCategoryTitle(item.categoryKey||item.category||"repo",language);const description=describeCatalogItem(item,category,language);byId("pg-catalog-info-category").textContent=category;byId("pg-catalog-info-title").textContent=item.label||item.name||"—";byId("pg-catalog-info-body").innerHTML=`<p>${playgroundEscape(description)}</p>${item.source?`<p><strong>${language==="de"?"Quelle":"Source"}:</strong> <code>${playgroundEscape(item.source)}</code></p>`:""}<p><strong>${language==="de"?"Grenze":"Boundary"}:</strong> ${language==="de"?"Explorativ. Der Katalogeintrag ist keine Instanzierung und erzeugt keine wissenschaftliche Evidenz.":"Exploratory. This catalog entry is not an instantiation and does not create scientific evidence."}</p>`;dialog.querySelector("#pg-catalog-info-close").setAttribute("aria-label",language==="de"?"Bausteininfo schließen":"Close component information");dialog.showModal();
}

function bindCatalogInfo(){
  const grid=byId("pg-catalog-grid");if(!grid||grid.dataset.infoBound)return;grid.dataset.infoBound="true";grid.addEventListener("click",event=>{const button=event.target.closest("[data-pg-catalog-info]");if(!button)return;const item=catalogInfoItems.get(button.dataset.pgCatalogInfo);if(item)showCatalogInfo(item);});
}

function renderCatalogCards(catalog){
  const panCandidates=(catalog.pan?.research_candidates||[]).map(item=>({name:item.id,note:item.question}));
  const panLiterature=(catalog.pan?.literature_context?.sources||[]).map(item=>({name:item.key,note:item.citation}));
  const geometryLiterature=(catalog.geometry?.literature_context?.sources||[]).map(item=>({name:item.key,note:item.citation}));
  const neuralIOCodecs=(catalog.neural_io?.codecs||[]).map(item=>({name:item.id,note:`${item.input_kind||""} · ${item.reconstruction_class||""}`}));
  const parityClasses=Object.entries(catalog.cuda_parity?.classes||{}).map(([name,item])=>({name,note:item.name||item.target_stage||""}));
  const groups=[["models",catalog.models],["topologies",catalog.topologies],["stimuli",catalog.stimuli],["synapses",catalog.synapses],["plasticity",catalog.plasticity],["readouts",catalog.readouts],["panCandidates",panCandidates],["panLiterature",panLiterature],["geometryLiterature",geometryLiterature],["neuralIO",neuralIOCodecs],["analyses",(catalog.analyses||[]).map(name=>({name}))],["robustness",(catalog.robustness_controls||[]).map(name=>({name}))],["cudaCompiler",(catalog.cuda_gate_compiler?.gate_types||[]).map(name=>({name,note:catalog.cuda_gate_compiler?.status||""}))],["cudaParity",parityClasses]];
  groups.push(["repo",PLAYGROUND_REPO_ELEMENTS.map(([name,category,description,source])=>({name,label:name,note:description,category,source}))]);
  catalogInfoItems=new Map();let itemIndex=0;const language=catalogLanguage();
  byId("pg-catalog-grid").innerHTML=groups.map(([categoryKey,items])=>{const title=catalogCategoryTitle(categoryKey,language);return `<article><h3>${playgroundEscape(title)}</h3>${(items||[]).map(item=>{const infoKey=String(itemIndex++);const info={...item,categoryKey};catalogInfoItems.set(infoKey,info);const description=describeCatalogItem(info,title,language);return `<button type="button" class="playground-chip" data-pg-catalog-info="${infoKey}" title="${playgroundEscape(description)}">${playgroundEscape(item.label||item.name)}</button>`;}).join("")}</article>`;}).join("");
}

function renderCatalog(catalog){
  catalogState=catalog;
  byId("pg-neuron-model").innerHTML=optionMarkup(catalog.models);
  byId("pg-synapse-model").innerHTML=optionMarkup(catalog.synapses);
  byId("pg-plasticity").innerHTML=optionMarkup(catalog.plasticity);
  byId("pg-readout").innerHTML=optionMarkup(catalog.readouts,"name");
  byId("pg-topology").innerHTML=optionMarkup(catalog.topologies,"name");
  byId("pg-stimulus").innerHTML=optionMarkup(catalog.stimuli,"name");
  byId("pg-neural-io-codec").innerHTML=(catalog.neural_io?.codecs||[]).filter(item=>item.available!==false).map(item=>`<option value="${item.id}">${item.id}</option>`).join("");
  byId("pg-neural-io-decoder").innerHTML=(catalog.neural_io?.decoders||[]).filter(item=>item.available!==false).map(item=>`<option value="${item.id}">${item.id}</option>`).join("");
  if([...byId("pg-topology").options].some(o=>o.value==="mhrn_5d"))byId("pg-topology").value="mhrn_5d";
  renderCatalogCards(catalog);bindCatalogInfo();
  const status=byId("pg-status");status.dataset.state="ok";status.textContent=`Bereit · bis ${catalog.limits.n_neurons} Neuronen · ${catalog.limits.edges} Kanten · ${catalog.limits.dimensions}D · scientific_evidence=false`;
}

export async function initPlayground(){
  const root=byId("tab-playground");if(!root)return;
  injectStyles();ensurePermanentBoundary(root);buildPanels(root);
  if(!root.dataset.languageBound){root.dataset.languageBound="true";document.addEventListener("mhrn:language-change",()=>{if(catalogState)renderCatalogCards(catalogState);const dialog=byId("pg-catalog-info-dialog");if(dialog?.open&&activeCatalogInfo)showCatalogInfo(activeCatalogInfo);});}
  byId("pg-run")?.addEventListener("click",runSession);byId("pg-cuda-status")?.addEventListener("click",()=>refreshCudaStatus().catch(error=>{const node=byId("pg-cuda-stage-state");if(node)node.textContent=String(error.message||error);}));byId("pg-cpu-determinism")?.addEventListener("click",()=>checkCpuDeterminism().catch(error=>{const node=byId("pg-cuda-compiler-state");if(node)node.textContent=String(error.message||error);}));byId("pg-cuda-compile")?.addEventListener("click",()=>compileCudaGates().catch(error=>{const node=byId("pg-cuda-compiler-state");if(node)node.textContent=String(error.message||error);}));byId("pg-cuda-preflight")?.addEventListener("click",()=>runCudaPreflight().catch(error=>{const node=byId("pg-cuda-resource-state");if(node)node.textContent=String(error.message||error);}));byId("pg-cuda-smoke")?.addEventListener("click",()=>runCudaHardwareSmoke().catch(error=>{const node=byId("pg-cuda-parity-state");if(node)node.textContent=String(error.message||error);}));byId("pg-cuda-rng")?.addEventListener("click",()=>runCudaRngParity().catch(error=>{const node=byId("pg-cuda-rng-state");if(node)node.textContent=String(error.message||error);}));byId("pg-user-preset-apply")?.addEventListener("click",applyUserPreset);byId("pg-user-preset-save")?.addEventListener("click",saveUserPreset);byId("pg-user-preset-delete")?.addEventListener("click",deleteUserPreset);byId("pg-user-preset-select")?.addEventListener("change",()=>{renderUserPresetOptions();applyUserPreset();});byId("pg-robustness")?.addEventListener("click",runRobustness);byId("pg-reset")?.addEventListener("click",resetForm);byId("pg-live-open")?.addEventListener("click",()=>openLiveMonitor().catch(error=>byId("pg-live-state").textContent=String(error.message||error)));byId("pg-live-clear")?.addEventListener("click",()=>clearLiveSessions().catch(error=>byId("pg-live-state").textContent=String(error.message||error)));byId("pg-night-start")?.addEventListener("click",()=>startNightRun().catch(error=>byId("pg-night-state").textContent=String(error.message||error)));byId("pg-night-stop")?.addEventListener("click",()=>stopNightRun().catch(error=>byId("pg-night-state").textContent=String(error.message||error)));byId("pg-night-refresh")?.addEventListener("click",()=>refreshNightStatus().catch(error=>byId("pg-night-state").textContent=String(error.message||error)));
  renderUserPresetOptions();
  try{renderCatalog(await apiGet("/api/playground/catalog"));renderUserPresetOptions();resetForm();}catch(error){const status=byId("pg-status");status.dataset.state="error";status.textContent=`Katalog nicht verfügbar: ${error.message}`;}
  byId("playground-builder")?.addEventListener("input", updateDefaultHints);
  byId("playground-builder")?.addEventListener("change", updateDefaultHints);
  initGuidedWorkspace({payload:formPayload,presets:()=>Object.fromEntries(Object.entries(allPlaygroundPresets()).map(([name,preset])=>[name,{...preset,settings:preset.source==="catalog"?resolvedPresetSettings(name):preset.settings}])),applyPreset:applyUserPreset,setValue:setBuilderValue,lastResult:()=>lastResult});
  await refreshSessions();
  try{await refreshNightStatus();}catch{ /* night manager is optional during partial deployments */ }
  try{await refreshCudaStatus();}catch{ /* CUDA toolkit/driver is optional */ }
  window.MHRNPlayground={run:runSession,runRobustness,checkCpuDeterminism,compileCudaGates,refreshCudaStatus,runCudaPreflight,runCudaHardwareSmoke,runCudaRngParity,refreshSessions,get catalog(){return catalogState;},get lastResult(){return lastResult;}};
}
