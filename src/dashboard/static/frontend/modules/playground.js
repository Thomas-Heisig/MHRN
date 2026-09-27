"use strict";

import { apiGet, apiPost, byId } from "../core/api.js";

let lastResult = null;
let catalogState = null;
let liveSessionId = null;
let liveLoopTimer = null;

const PLAYGROUND_DEFAULT_HINTS = {
  "pg-weight": "4", "pg-dimensions": "5", "pg-neurons": "128", "pg-edges": "1024",
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
    #tab-playground .workspace-header p{max-width:72rem}
    .pg-permanent-boundary{position:sticky;top:var(--mhrn-sticky-offset,70px);z-index:6;display:flex;gap:.7rem;align-items:flex-start;margin:.5rem 0 .85rem;padding:.75rem .9rem;border:1px solid color-mix(in srgb,#efb45e 65%,transparent);border-radius:12px;background:color-mix(in srgb,var(--panel-bg,#111) 94%,#efb45e 6%);box-shadow:0 6px 18px rgba(0,0,0,.12)}
    .pg-permanent-boundary strong{display:block}.pg-permanent-boundary p{margin:.2rem 0 0;opacity:.78;font-size:.73rem}
    .playground-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem}
    .playground-card,.playground-viz,.playground-analysis-card{border:1px solid var(--line,rgba(127,127,127,.2));border-radius:12px;padding:.8rem;background:rgba(127,127,127,.035)}
    .playground-card h3,.playground-viz h3,.playground-analysis-card h3{margin:.05rem 0 .65rem;font-size:.84rem}
    .playground-card label{display:grid;gap:.25rem;margin:.48rem 0;font-size:.7rem;opacity:.9}.playground-card small{display:block;opacity:.65;line-height:1.4}
      .playground-card label.pg-non-default{outline:1px dotted color-mix(in srgb,currentColor 45%,transparent);outline-offset:3px}
    .playground-card input,.playground-card select,.playground-card textarea{width:100%;padding:.45rem .5rem;border:1px solid var(--line,rgba(127,127,127,.25));border-radius:8px;background:rgba(0,0,0,.12);color:inherit}.playground-card textarea{min-height:72px;resize:vertical;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.67rem}
    .playground-actions{display:flex;flex-wrap:wrap;gap:.5rem;margin:.9rem 0}.playground-actions button{padding:.58rem .8rem;border-radius:8px;border:1px solid var(--line,rgba(127,127,127,.3));background:rgba(127,127,127,.1);color:inherit;cursor:pointer}.playground-actions .primary{font-weight:700;border-color:currentColor}
    .playground-status{padding:.65rem .75rem;border-radius:9px;background:rgba(127,127,127,.06);font-size:.72rem;white-space:pre-wrap;overflow:auto}.playground-status[data-state="error"]{color:#ef8b8b}.playground-status[data-state="ok"]{color:#51d6ad}
    .playground-metrics{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:.5rem;margin:.8rem 0}.playground-metric{padding:.65rem;border:1px solid var(--line,rgba(127,127,127,.2));border-radius:10px}.playground-metric span{display:block;font-size:.58rem;opacity:.62;text-transform:uppercase}.playground-metric strong{display:block;margin-top:.2rem;font-size:.9rem}
    .playground-viz-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.7rem}.playground-viz{min-height:260px}.playground-viz canvas{width:100%;height:210px;display:block}
    .playground-analysis-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.65rem;margin-top:.75rem}.playground-analysis-card pre{font-size:.65rem;max-height:260px;overflow:auto;white-space:pre-wrap}
    .playground-session-list{display:grid;gap:.55rem}.playground-session{display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:.7rem;border:1px solid var(--line,rgba(127,127,127,.2));border-radius:10px}.playground-session small{display:block;opacity:.65}
    .playground-catalog{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.65rem}.playground-catalog article{padding:.75rem;border:1px solid var(--line,rgba(127,127,127,.2));border-radius:10px}.playground-chip{display:inline-flex;margin:.15rem;padding:.22rem .4rem;border-radius:999px;border:1px solid var(--line,rgba(127,127,127,.22));font-size:.63rem}
    .pg-neutral-note{padding:.65rem .75rem;margin:.65rem 0;border-left:3px solid currentColor;background:rgba(127,127,127,.05);font-size:.72rem;opacity:.82}
    @media(max-width:1150px){.playground-grid{grid-template-columns:1fr 1fr}.playground-metrics{grid-template-columns:repeat(4,1fr)}}@media(max-width:760px){.playground-grid,.playground-viz-grid,.playground-analysis-grid,.playground-catalog{grid-template-columns:1fr}.playground-metrics{grid-template-columns:repeat(2,1fr)}}
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
      <div class="playground-grid">
        <article class="playground-card"><h3>01 · Neuronen & Synapsen</h3>
          <label>Neuronmodell<select id="pg-neuron-model"></select></label>
          <label>Synapsenmodell<select id="pg-synapse-model"></select></label>
          <label>Startgewicht<input id="pg-weight" type="number" min="0" max="100" step="0.1" value="4"></label>
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
          <label>Aktionen<input id="pg-behavior-actions" type="number" min="2" max="16" value="4"></label>
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
      .playground-settings-reference{margin-top:.8rem;border:1px solid var(--line,rgba(127,127,127,.2));border-radius:12px;padding:.8rem;background:rgba(127,127,127,.025)}.playground-settings-reference header{display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;margin-bottom:.65rem}.playground-settings-reference h3{margin:0;font-size:.9rem}.playground-settings-reference p{margin:.25rem 0 0;opacity:.68;font-size:.68rem;line-height:1.4}.playground-settings-reference-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.6rem}.playground-settings-reference article{min-width:0;padding:.65rem;border:1px solid var(--line,rgba(127,127,127,.18));border-radius:9px;background:rgba(127,127,127,.035)}.playground-settings-reference article h4{margin:0 0 .45rem;font-size:.72rem}.playground-settings-reference dl{display:grid;grid-template-columns:minmax(7rem,auto) 1fr;gap:.28rem .5rem;margin:0;font-size:.62rem;line-height:1.35}.playground-settings-reference dt{color:inherit;font-weight:700}.playground-settings-reference dd{margin:0;opacity:.72;overflow-wrap:anywhere}.playground-settings-option{display:inline-block;margin:.08rem .18rem .08rem 0;padding:.12rem .28rem;border:1px solid var(--line,rgba(127,127,127,.18));border-radius:999px;font-size:.58rem}
        </article>
      </div>
        <section class="playground-settings-reference" id="pg-settings-reference" aria-labelledby="pg-settings-reference-title">
          <header><div><h3 id="pg-settings-reference-title">Alle Einstellungsmöglichkeiten</h3><p>Vollständige Auswahlübersicht für den Playground. Katalogoptionen, feste Auswahlwerte, Schalter und gültige Wertebereiche.</p></div><span class="playground-chip">explorativ · keine EVID</span></header>
          <div class="playground-settings-reference-grid" id="pg-settings-reference-grid"><p>Katalog wird geladen …</p></div>
        </section>
      <div class="playground-actions"><button type="button" class="primary" id="pg-run">▶ Playground starten</button><button type="button" id="pg-robustness">Robustheitskontrollen</button><button type="button" id="pg-reset">Standardwerte</button></div>
        @media(max-width:1150px){.playground-grid{grid-template-columns:1fr 1fr}.playground-metrics{grid-template-columns:repeat(4,1fr)}.playground-settings-reference-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:760px){.playground-grid,.playground-viz-grid,.playground-analysis-grid,.playground-catalog,.playground-settings-reference-grid{grid-template-columns:1fr}.playground-metrics{grid-template-columns:repeat(2,1fr)}}
      <article class="playground-card"><h3>10 · PAN Live Session & Sandbox</h3><div class="playground-actions"><button type="button" id="pg-live-create">Live starten</button><button type="button" id="pg-live-step">+32 Ticks</button><button type="button" id="pg-live-auto">Auto Start</button><button type="button" id="pg-live-auto-stop">Auto Stop</button><button type="button" id="pg-live-input">Input zeigen</button><button type="button" id="pg-live-sandbox">Sandbox +8</button><button type="button" id="pg-live-stop">Stop</button></div><label>Live Input (JSON-Array)<textarea id="pg-live-input-values">[1,0,-1,0.5]</textarea></label><canvas id="pg-live-sandbox-canvas" width="800" height="360"></canvas><pre id="pg-live-state">Noch keine Live-Session.</pre></article>
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

function formPayload() {
  return {
    name: "dashboard_playground",
    neuron_model: byId("pg-neuron-model").value,
    synapse_model: byId("pg-synapse-model").value,
    weight: Number(byId("pg-weight").value),
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
  byId("pg-analysis-network").textContent=JSON.stringify({network:net,dimensionality:dim,ensemble:result.ensemble||null,pan:result.pan||null,geometry:result.geometry||null,gates:result.gates||null,clock:result.clock||null,execution:result.execution||null,growth:result.growth||null,storage:result.storage||null},null,2);
  byId("pg-analysis-plasticity").textContent=JSON.stringify({plasticity:a.plasticity||{},performance:a.performance||{},pan:result.pan||null,growth:result.growth||null,behavioral_learning:result.behavioral_learning||null,thalamic_gating:result.thalamic_gating||null,cortical_organization:result.cortical_organization||null,storage:result.storage||null,hardware:result.hardware||null},null,2);
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

async function createLiveSession(){
  const payload={...formPayload(),neuron_model:"pan_adex_5d",pan_enabled:true,thalamic_relay_threshold:0,pan_bias_current:Number(byId("pg-pan-bias-current").value),behavior_target_mode:byId("pg-behavior-target-mode").value};
  const result=await apiPost("/api/playground/live/create",payload);liveSessionId=result.session_id;byId("pg-live-state").textContent=JSON.stringify(result,null,2);
}
async function stepLiveSession(){
  if(!liveSessionId)throw new Error("Zuerst Live-Session starten.");
  const result=await apiPost(`/api/playground/live/${encodeURIComponent(liveSessionId)}/step`,{ticks:32});byId("pg-live-state").textContent=JSON.stringify(result,null,2);
}
async function startLiveLoop(){
  if(!liveSessionId)throw new Error("Zuerst Live-Session starten.");
  if(liveLoopTimer)return;
  liveLoopTimer=setInterval(()=>{stepLiveSession().catch(error=>{byId("pg-live-state").textContent=String(error.message||error);stopLiveLoop();});},250);
}
function stopLiveLoop(){
  if(liveLoopTimer){clearInterval(liveLoopTimer);liveLoopTimer=null;}
}

async function injectLiveInput(){
  if(!liveSessionId)throw new Error("Zuerst Live-Session starten.");
  let values;try{values=JSON.parse(byId("pg-live-input-values").value);}catch{throw new Error("Live Input muss gültiges JSON sein.");}
  if(!Array.isArray(values))throw new Error("Live Input muss ein Array sein.");
  const result=await apiPost(`/api/playground/live/${encodeURIComponent(liveSessionId)}/input`,{values,duration_ticks:16,gain:25});byId("pg-live-state").textContent=JSON.stringify(result,null,2);
}
async function stepLiveSandbox(){
  if(!liveSessionId)throw new Error("Zuerst Live-Session starten.");
  const result=await apiPost(`/api/playground/live/${encodeURIComponent(liveSessionId)}/sandbox`,{ticks:8});byId("pg-live-state").textContent=JSON.stringify(result,null,2);drawLiveSandbox(result.world);
}
async function stopLiveSession(){
  stopLiveLoop();
  if(!liveSessionId)return;
  const result=await apiPost(`/api/playground/live/${encodeURIComponent(liveSessionId)}/stop`,{});byId("pg-live-state").textContent=JSON.stringify(result,null,2);liveSessionId=null;
}

async function runSession(){
  const status=byId("pg-status");status.dataset.state="running";status.textContent="Playground läuft …";
  try{const result=await apiPost("/api/playground/run",formPayload());renderResult(result);status.dataset.state="ok";status.textContent=`Lauf abgeschlossen · ${result.session_id} · PLAYGROUND · keine Evidenz`;window.MHRNWorkspaceArchitecture?.selectRoute?.("playground","run");if(result.persisted_path)await refreshSessions();}
  catch(error){status.dataset.state="error";status.textContent=`Playground fehlgeschlagen: ${error.message||error}`;}
}

async function runRobustness(){
  const status=byId("pg-status");status.dataset.state="running";status.textContent="Explorative Robustheitskontrollen laufen …";
  try{const result=await apiPost("/api/playground/robustness",{...formPayload(),persist:false,ensemble_runs:1});status.dataset.state="ok";status.textContent="Robustheitssuite abgeschlossen · nicht preregistriert · keine Evidenz";byId("pg-run-json").textContent=JSON.stringify(result,null,2);window.MHRNWorkspaceArchitecture?.selectRoute?.("playground","run");}
  catch(error){status.dataset.state="error";status.textContent=`Robustheitssuite fehlgeschlagen: ${error.message||error}`;}
}

function resetForm(){
  const values={neurons:"128",edges:"1024",weight:"4",ticks:"256",dimensions:"5",delay:"1",radius:"0.35",k:"16",rewire:"0.15",modules:"2",current:"8",rate:"20",seed:"12345",ensemble:"1","pan-dimensions":"5","pan-feedback-gain":"0.05","pan-health-decay":"0.001","pan-apoptosis":"0.1","pan-bias-current":"10","geometry-lambda-a":"0.5","geometry-lambda-b":"0.5","geometry-sigma":"0.1","geometry-p0":"0.3","geometry-delay-velocity":"0.25","clock-base-hz":"100","clock-event-batch":"10","execution-high":"0.30","execution-low":"0.05","execution-hysteresis":"0.02","execution-dwell":"100","execution-window":"100","growth-activity":"0.25","growth-coactivation":"2","growth-info":"0.25","growth-prune":"0.05","growth-max-synapses":"128","growth-max-new":"8","cuda-budget":"2048","offload-snapshot":"1000","thalamic-threshold":"0","thalamic-attention":"1.15","thalamic-inhibition":"0.35","cortical-layers":"6","cortical-lr":"0.01","behavior-actions":"4","behavior-target":"0","behavior-min-activity":"0.01","behavior-lr":"0.2","behavior-epsilon":"0.2","behavior-episode":"16","behavior-bias":"3"};
  for(const[k,v]of Object.entries(values)){const el=byId(`pg-${k}`);if(el)el.value=v;}byId("pg-persist").checked=false;byId("pg-pan-enabled").checked=false;byId("pg-pan-closed-loop").checked=true;byId("pg-clock-mode").value="continuous";byId("pg-execution-mode").value="HYBRID_AUTO";byId("pg-execution-initial").value="EVENT_ONLY";byId("pg-execution-transition").value="clean";byId("pg-execution-sync").checked=true;byId("pg-execution-log").checked=true;byId("pg-growth-enabled").checked=false;byId("pg-offload-enabled").checked=false;byId("pg-hardware-profile").value="reference_cpu";byId("pg-thalamic-enabled").checked=false;byId("pg-behavior-target-mode").value="cycle";byId("pg-cortical-enabled").checked=false;byId("pg-cortical-plasticity").checked=true;byId("pg-behavior-enabled").checked=false;byId("pg-geometry-mode").value="mixed_additive";byId("pg-neural-io-enabled").checked=false;byId("pg-neural-io-payload").value="0.5";byId("pg-neural-io-input-channels").value="16";byId("pg-neural-io-output-channels").value="16";byId("pg-neural-io-window").value="16";byId("pg-neural-io-current").value="25";byId("pg-neural-io-input-role").value="GATEWAY_AFFERENT";byId("pg-neural-io-output-role").value="GATEWAY_EFFERENT";byId("pg-neural-io-phase").value="QUERY";byId("pg-neural-io-modality").value="digital";byId("pg-neural-io-source").value="playground.input";if(byId("pg-topology"))byId("pg-topology").value="mhrn_5d";
  updateDefaultHints();
}

async function refreshSessions(){
  const root=byId("pg-session-list");if(!root)return;
  try{const data=await apiGet("/api/playground/sessions"),sessions=data.sessions||[];root.innerHTML=sessions.length?sessions.map(s=>`<article class="playground-session"><div><strong>${s.name||s.session_id}</strong><small>${s.session_id} · ${s.created_at||""} · ${s.class||"PLAYGROUND"}</small></div><button type="button" data-pg-replay="${s.session_id}">Replay</button></article>`).join(""):"<p>Noch keine lokal gespeicherten Playground-Sessions.</p>";root.querySelectorAll("[data-pg-replay]").forEach(button=>button.addEventListener("click",async()=>{try{const result=await apiGet(`/api/playground/sessions/${encodeURIComponent(button.dataset.pgReplay)}`);renderResult(result);window.MHRNWorkspaceArchitecture?.selectRoute?.("playground","run");}catch(error){root.textContent=`Replay fehlgeschlagen: ${error.message}`;}}));}
  catch(error){root.textContent=`Sessions nicht verfügbar: ${error.message}`;}
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
  const panCandidates=(catalog.pan?.research_candidates||[]).map(item=>({name:item.id,note:item.question}));
  const panLiterature=(catalog.pan?.literature_context?.sources||[]).map(item=>({name:item.key,note:item.citation}));
  const geometryLiterature=(catalog.geometry?.literature_context?.sources||[]).map(item=>({name:item.key,note:item.citation}));
  const neuralIOCodecs=(catalog.neural_io?.codecs||[]).map(item=>({name:item.id,note:`${item.input_kind||""} · ${item.reconstruction_class||""}`}));
  const groups=[["Neuronmodelle",catalog.models],["Topologien",catalog.topologies],["Stimuli",catalog.stimuli],["Synapsen",catalog.synapses],["Plastizität",catalog.plasticity],["Readouts",catalog.readouts],["PAN Research Candidates",panCandidates],["PAN Literaturkontext",panLiterature],["Geometrie Literaturkontext",geometryLiterature],["Neural I/O Codecs",neuralIOCodecs],["Analysen",(catalog.analyses||[]).map(name=>({name}))],["Robustheit",(catalog.robustness_controls||[]).map(name=>({name}))]];
  byId("pg-catalog-grid").innerHTML=groups.map(([title,items])=>`<article><h3>${title}</h3>${(items||[]).map(item=>`<span class="playground-chip" title="${item.note||""}">${item.label||item.name}</span>`).join("")}</article>`).join("");
  const settingGroups = [
    ["Katalogauswahl", [
      ["Neuronmodell", (catalog.models || []).map(item => item.label || item.name).join(" · ")],
      ["Synapsenmodell", (catalog.synapses || []).map(item => item.label || item.name).join(" · ")],
      ["Plastizität", (catalog.plasticity || []).map(item => item.label || item.name).join(" · ")],
      ["Topologie", (catalog.topologies || []).map(item => item.name).join(" · ")],
      ["Stimulus", (catalog.stimuli || []).map(item => item.name).join(" · ")],
      ["Readout", (catalog.readouts || []).map(item => item.name).join(" · ")],
    ]],
    ["Topologie & Geometrie", [
      ["Neuronen", "2–1024 · Standard 128"], ["Kanten", "Neuronen–20.000 · Standard 1024"],
      ["Dimensionen", "1–32 · Standard 5"], ["Gewicht", "0–100 · Standard 4"],
      ["Radius", "0.001–2 · Standard 0.35"], ["k Nachbarn", "1–64 · Standard 16"],
      ["Module", "1–32 · Standard 2"], ["Geometrie-Modus", "mixed_additive · shortcut_union"],
      ["λa / λb", "0–10 · Standard 0.5 / 0.5"], ["σ", "0.001–2 · Standard 0.1"], ["p0", "0–1 · Standard 0.3"],
    ]],
    ["Stimulus & Lauf", [
      ["Ticks", "1–2048 · Standard 256"], ["Strom", "0–500 · Standard 8"], ["Rate", "0–1000 Hz · Standard 20"],
      ["Seed", "0+ · Standard 12345"], ["Seed-Ensemble", "1–8 · Standard 1"], ["Delay", "1–64 Ticks · Standard 1"],
      ["Rewiring", "0–1 · Standard 0.15"], ["Session speichern", "an / aus"],
    ]],
    ["PAN & Geometrieparameter", [
      ["PAN", "an / aus"], ["PAN-Dimensionen", "5–32 · Standard 5"], ["Closed Loop", "an / aus"],
      ["Feedback-Gain", "0–5 · Standard 0.05"], ["Health-Decay", "0–1 · Standard 0.001"],
      ["Apoptose", "0–1 · Standard 0.1"], ["PAN Bias", "0–500 · Standard 10"], ["XYZ-Geschwindigkeit", "0.001–10 · Standard 0.25"],
    ]],
    ["Runtime & Wachstum", [
      ["Clock", "continuous · dual"], ["Base Hz", "1–10.000 · Standard 100"], ["Event Batch", "0.05–1000 ms · Standard 10"],
      ["Execution", "HYBRID_AUTO · EVENT_ONLY · TICK_ONLY"], ["Initial Engine", "EVENT_ONLY · TICK_ONLY"],
      ["Transition", "clean · debug · fast"], ["θ high / low", "0–1 · Standard 0.30 / 0.05"], ["Hysterese", "0–0.5 · Standard 0.02"],
      ["Dwell / Fenster", "0–2048 / 1–2048 · Standard 100 / 100"], ["Wachstum", "an / aus"], ["Wachstumsschwellen", "Aktivität · Co-Aktivierung · Info · Prune"],
      ["Hardware", "reference_cpu · cuda_8gb_balanced_plan"], ["CUDA-Budget", "128–16.384 MiB · Standard 2048"], ["SSD-Offload", "an / aus"],
    ]],
    ["Lernen & I/O", [
      ["Thalamus", "an / aus · Relay 0–1 · Attention 0–4 · Inhibition 0–1"], ["Kortex", "an / aus · 2–12 Schichten"],
      ["Layer Lernrate", "0–1 · Standard 0.01"], ["Verhalten lernen", "an / aus"], ["Aktionen", "2–16 · Standard 4"],
      ["Zielaktion", "0–15 · Standard 0"], ["Zielmodus", "cycle · fixed"], ["Policy-Lernrate", "0.001–1 · Standard 0.2"],
      ["Exploration ε", "0–1 · Standard 0.2"], ["Episode", "1–2048 Ticks · Standard 16"], ["Policy Bias", "0–100 · Standard 3"],
      ["Neural I/O", "an / aus · Codec · Decoder · Rollen · Phase · Payload"], ["I/O-Kanäle", "1–256 · Standard 16"],
    ]],
  ];
  byId("pg-settings-reference-grid").innerHTML=settingGroups.map(([title,items])=>`<article><h4>${title}</h4><dl>${items.map(([label,value])=>`<dt>${label}</dt><dd>${value}</dd>`).join("")}</dl></article>`).join("");
  const status=byId("pg-status");status.dataset.state="ok";status.textContent=`Bereit · bis ${catalog.limits.n_neurons} Neuronen · ${catalog.limits.edges} Kanten · ${catalog.limits.dimensions}D · scientific_evidence=false`;
}

export async function initPlayground(){
  const root=byId("tab-playground");if(!root)return;
  injectStyles();ensurePermanentBoundary(root);buildPanels(root);
  byId("pg-run")?.addEventListener("click",runSession);byId("pg-robustness")?.addEventListener("click",runRobustness);byId("pg-reset")?.addEventListener("click",resetForm);byId("pg-live-create")?.addEventListener("click",()=>createLiveSession().catch(error=>byId("pg-live-state").textContent=String(error.message||error)));byId("pg-live-step")?.addEventListener("click",()=>stepLiveSession().catch(error=>byId("pg-live-state").textContent=String(error.message||error)));byId("pg-live-auto")?.addEventListener("click",()=>startLiveLoop().catch(error=>byId("pg-live-state").textContent=String(error.message||error)));byId("pg-live-auto-stop")?.addEventListener("click",stopLiveLoop);byId("pg-live-input")?.addEventListener("click",()=>injectLiveInput().catch(error=>byId("pg-live-state").textContent=String(error.message||error)));byId("pg-live-sandbox")?.addEventListener("click",()=>stepLiveSandbox().catch(error=>byId("pg-live-state").textContent=String(error.message||error)));byId("pg-live-stop")?.addEventListener("click",()=>stopLiveSession().catch(error=>byId("pg-live-state").textContent=String(error.message||error)));
  try{renderCatalog(await apiGet("/api/playground/catalog"));resetForm();}catch(error){const status=byId("pg-status");status.dataset.state="error";status.textContent=`Katalog nicht verfügbar: ${error.message}`;}
  byId("playground-builder")?.addEventListener("input", updateDefaultHints);
  byId("playground-builder")?.addEventListener("change", updateDefaultHints);
  await refreshSessions();
  window.MHRNPlayground={run:runSession,runRobustness,refreshSessions,get catalog(){return catalogState;},get lastResult(){return lastResult;}};
}
