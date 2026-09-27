"use strict";

import { apiGet, apiPost, byId } from "../core/api.js";

let lastResult = null;
let catalogState = null;

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
    .playground-card input,.playground-card select{width:100%;padding:.45rem .5rem;border:1px solid var(--line,rgba(127,127,127,.25));border-radius:8px;background:rgba(0,0,0,.12);color:inherit}
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
          <label>Plastizität<select id="pg-plasticity"></select></label>
          <label>Readout<select id="pg-readout"></select></label>
          <small>Enthält Izhikevich RS/FS/IB/CH/LTS/Resonator/Sensory/Motor, LIF, AdEx, HH Na/K/Ca und Multi-Compartment.</small>
        </article>
        <article class="playground-card"><h3>02 · Geometrie & Netzwerk</h3>
          <label>Topologie<select id="pg-topology"></select></label>
          <label>Dimensionen (Generic N-D)<input id="pg-dimensions" type="number" min="1" max="32" value="5"></label>
          <label>Neuronen<input id="pg-neurons" type="number" min="2" max="1024" value="128"></label>
          <label>Kanten<input id="pg-edges" type="number" min="2" max="20000" value="512"></label>
          <small>MHRN 5D verwendet explizit x/y/z/d4/d5 und den kanonischen <code>pack_coords</code>-Vertrag. Generic N-D reicht bis 32D.</small>
        </article>
        <article class="playground-card"><h3>03 · Konnektivität</h3>
          <label>Radius<input id="pg-radius" type="number" min="0.001" max="2" step="0.01" value="0.35"></label>
          <label>k Nachbarn<input id="pg-k" type="number" min="1" max="64" value="8"></label>
          <label>Rewiring-Wahrscheinlichkeit<input id="pg-rewire" type="number" min="0" max="1" step="0.01" value="0.15"></label>
          <label>Module<input id="pg-modules" type="number" min="1" max="32" value="4"></label>
          <label>Delay (Ticks)<input id="pg-delay" type="number" min="1" max="64" value="1"></label>
        </article>
        <article class="playground-card"><h3>04 · Stimulus & Lauf</h3>
          <label>Stimulus<select id="pg-stimulus"></select></label>
          <label>Ticks<input id="pg-ticks" type="number" min="1" max="2048" value="256"></label>
          <label>Strom<input id="pg-current" type="number" min="0" max="500" step="0.5" value="12"></label>
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
          <small>PAN ist eine nicht-kanonische Explorationsschicht. D4 nutzt aktuell einen Surprise-Proxy, keine validierte PID.</small>
        </article>
      </div>
      <div class="playground-actions"><button type="button" class="primary" id="pg-run">▶ Playground starten</button><button type="button" id="pg-robustness">Robustheitskontrollen</button><button type="button" id="pg-reset">Standardwerte</button></div>
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
      </div>
      <pre class="playground-status" id="pg-run-json">Noch kein Playground-Lauf.</pre>
    </section>
    <section data-generated-panel="sessions" id="playground-sessions"><div class="pg-neutral-note">Sessions bleiben lokal unter <code>playground_sessions/</code>, sind nicht kanonisch und werden von Git ignoriert.</div><div class="playground-session-list" id="pg-session-list">lade …</div></section>
    <section data-generated-panel="catalog" id="playground-catalog"><div class="playground-catalog" id="pg-catalog-grid"></div></section>
  `);
}

function formPayload() {
  return {
    name: "dashboard_playground",
    neuron_model: byId("pg-neuron-model").value,
    synapse_model: byId("pg-synapse-model").value,
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
  byId("pg-analysis-network").textContent=JSON.stringify({network:net,dimensionality:dim,ensemble:result.ensemble||null,pan:result.pan||null},null,2);
  byId("pg-analysis-plasticity").textContent=JSON.stringify({plasticity:a.plasticity||{},performance:a.performance||{},pan:result.pan||null},null,2);
  byId("pg-run-json").textContent=JSON.stringify({session_id:result.session_id,manifest:result.manifest,model:result.model,config:result.config,metrics:result.metrics,readout:result.readout},null,2);
  drawRaster(result);drawSeries("pg-rate-canvas",(result.monitors?.tick_spike_counts||[]).map(Number));drawTopology(result);drawState(result);drawSpectrum(result);drawDegree(result);
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
  const values={neurons:"128",edges:"512",ticks:"256",dimensions:"5",delay:"1",radius:"0.35",k:"8",rewire:"0.15",modules:"4",current:"12",rate:"20",seed:"12345",ensemble:"1","pan-dimensions":"5","pan-feedback-gain":"0.05","pan-health-decay":"0.001","pan-apoptosis":"0.1"};
  for(const[k,v]of Object.entries(values)){const el=byId(`pg-${k}`);if(el)el.value=v;}byId("pg-persist").checked=false;byId("pg-pan-enabled").checked=false;byId("pg-pan-closed-loop").checked=true;if(byId("pg-topology"))byId("pg-topology").value="mhrn_5d";
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
  if([...byId("pg-topology").options].some(o=>o.value==="mhrn_5d"))byId("pg-topology").value="mhrn_5d";
  const panCandidates=(catalog.pan?.research_candidates||[]).map(item=>({name:item.id,note:item.question}));
  const panLiterature=(catalog.pan?.literature_context?.sources||[]).map(item=>({name:item.key,note:item.citation}));
  const groups=[["Neuronmodelle",catalog.models],["Topologien",catalog.topologies],["Stimuli",catalog.stimuli],["Synapsen",catalog.synapses],["Plastizität",catalog.plasticity],["Readouts",catalog.readouts],["PAN Research Candidates",panCandidates],["PAN Literaturkontext",panLiterature],["Analysen",(catalog.analyses||[]).map(name=>({name}))],["Robustheit",(catalog.robustness_controls||[]).map(name=>({name}))]];
  byId("pg-catalog-grid").innerHTML=groups.map(([title,items])=>`<article><h3>${title}</h3>${(items||[]).map(item=>`<span class="playground-chip" title="${item.note||""}">${item.label||item.name}</span>`).join("")}</article>`).join("");
  const status=byId("pg-status");status.dataset.state="ok";status.textContent=`Bereit · bis ${catalog.limits.n_neurons} Neuronen · ${catalog.limits.edges} Kanten · ${catalog.limits.dimensions}D · scientific_evidence=false`;
}

export async function initPlayground(){
  const root=byId("tab-playground");if(!root)return;
  injectStyles();ensurePermanentBoundary(root);buildPanels(root);
  byId("pg-run")?.addEventListener("click",runSession);byId("pg-robustness")?.addEventListener("click",runRobustness);byId("pg-reset")?.addEventListener("click",resetForm);
  try{renderCatalog(await apiGet("/api/playground/catalog"));}catch(error){const status=byId("pg-status");status.dataset.state="error";status.textContent=`Katalog nicht verfügbar: ${error.message}`;}
  await refreshSessions();
  window.MHRNPlayground={run:runSession,runRobustness,refreshSessions,get catalog(){return catalogState;},get lastResult(){return lastResult;}};
}
