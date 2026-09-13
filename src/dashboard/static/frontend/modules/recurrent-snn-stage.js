"use strict";

const ROUTES = Object.freeze({
  science: ["recurrent", "Rekurrentes SNN", "network", "view", "recurrent"],
  wesen: ["recurrent", "Rekurrenz", "wesen", "focus", "#mhrn-runtime-recurrent"],
  control: ["recurrent", "Rekurrenz-Parameter", "settings", "focus", "#mhrn-recurrent-control"],
});

const EDITABLE = Object.freeze([
  "network.initial_connections_per_neuron",
  "network.neighbour_radius",
  "neuron.refractory_ticks",
]);

const state = {
  timer: null,
  lastTick: null,
  inFlight: false,
  parameters: {},
  pending: {},
};
const $ = (id) => document.getElementById(id);

async function json(url, options = {}) {
  const response = await fetch(url, {
    cache: "no-store",
    ...options,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  const payload = await response.json();
  if (!response.ok || payload.ok === false) {
    throw new Error(payload.error || payload.message || `HTTP ${response.status}`);
  }
  return payload;
}

function fmt(value, digits = 3) {
  if (value === null || value === undefined) return "—";
  if (typeof value === "number") return Number.isInteger(value) ? String(value) : value.toFixed(digits);
  return String(value);
}

function kv(label, value) {
  return `<div class="small-snn-kv"><span>${label}</span><strong>${fmt(value)}</strong></div>`;
}

function addOverviewCard(areaId, route, architecture) {
  const grid = document.querySelector(`[data-area-overview="${areaId}"] .mhrn-area-route-grid`);
  if (!grid || grid.querySelector(`[data-route-card="${route[0]}"]`)) return;
  const button = document.createElement("button");
  button.type = "button";
  button.dataset.routeCard = route[0];
  button.title = `${route[1]} öffnen`;
  button.innerHTML = `<span>S2</span><strong>${route[1]}</strong>`;
  grid.appendChild(button);
  button.addEventListener("click", () => architecture.selectRoute(areaId, route[0]));
}

function addRoute(areaId, route) {
  const architecture = window.MHRNWorkspaceArchitecture;
  const routes = architecture?.areas?.[areaId]?.routes;
  if (!architecture?.selectRoute || !Array.isArray(routes)) return false;
  if (!routes.some(([id]) => id === route[0])) {
    const anchorId = "snn";
    const index = routes.findIndex(([id]) => id === anchorId);
    routes.splice(index >= 0 ? index + 1 : routes.length, 0, [...route]);
  }
  document.querySelectorAll(`.mhrn-context-nav[data-area="${areaId}"]`).forEach((nav) => {
    if (nav.querySelector(`[data-area-route="${route[0]}"]`)) return;
    const button = document.createElement("button");
    button.type = "button";
    button.setAttribute("role", "tab");
    button.dataset.areaRoute = route[0];
    button.textContent = route[1];
    button.title = route[1];
    nav.appendChild(button);
    button.addEventListener("click", () => architecture.selectRoute(areaId, route[0]));
  });
  addOverviewCard(areaId, route, architecture);
  return true;
}

function ensureRoutes() {
  return Object.entries(ROUTES).every(([area, route]) => addRoute(area, route));
}

function ensureSciencePanel() {
  const root = $("tab-network");
  if (!root || $("mhrn-recurrent-science")) return;
  const panel = document.createElement("section");
  panel.id = "mhrn-recurrent-science";
  panel.className = "card small-snn-panel";
  panel.dataset.networkView = "recurrent";
  panel.hidden = true;
  panel.innerHTML = `
    <header class="small-snn-head"><div><span class="workspace-kicker">STAGE 2 · RECURRENT SPIKING NETWORK</span><h2>Stabiles rekurrentes SNN</h2><p>Rekurrente Konnektivität, begrenzte Spike-Dynamik und lange deterministische Runs.</p></div><span class="small-snn-stage-badge">Stage 2</span></header>
    <div class="small-snn-boundary">Engineering-Verifikation. Kein Nachweis biologischer Äquivalenz, Kognition oder Stabilität beliebiger rekurrenter Netze.</div>
    <div id="recurrent-science-summary" class="small-snn-summary"></div>
    <div class="small-snn-grid">
      <section><h3>Live-Netz</h3><div id="recurrent-science-graph" class="small-snn-graph"></div></section>
      <section><h3>Stage-2 Contract</h3><div class="small-snn-contract"><strong>A → B → C → D → A</strong><span>20.000 ticks reference run</span><span>bounded event queue</span><span>deterministic replay identity</span><span>restart/restore independently verified</span><span>RQ-SNN-001: 100.000 ticks/run research DATA</span></div><div class="small-snn-actions"><button type="button" data-route-jump="wesen:recurrent">Runtime ansehen</button><button type="button" data-route-jump="control:recurrent">Rekurrenz-Parameter</button><button type="button" data-route-jump="release:development">Release-Entwicklung</button></div></section>
    </div>
    <div id="recurrent-science-status" class="small-snn-status">lade …</div>`;
  root.appendChild(panel);
}

function ensureRuntimePanel() {
  const root = $("tab-wesen");
  if (!root || $("mhrn-runtime-recurrent")) return;
  const panel = document.createElement("section");
  panel.id = "mhrn-runtime-recurrent";
  panel.className = "card small-snn-panel runtime-snn-panel";
  panel.dataset.mhrnRoute = "wesen:recurrent";
  panel.hidden = true;
  panel.innerHTML = `
    <header class="small-snn-head"><div><span class="workspace-kicker">RUNTIME & WESEN · STAGE 2</span><h2>Rekurrenz Live</h2><p>Read-only Beobachtung des real laufenden Netzwerks mit Tick, Aktivität, Queue und rückgekoppelten Kanten im sichtbaren Ausschnitt.</p></div><button id="recurrent-runtime-refresh" type="button">↻ Aktualisieren</button></header>
    <div id="recurrent-runtime-summary" class="small-snn-summary"></div>
    <div id="recurrent-runtime-graph" class="small-snn-graph small-snn-graph--large"></div>
    <div id="recurrent-runtime-status" class="small-snn-status">lade …</div>
    <div class="small-snn-boundary">Nur Beobachtung. Die Ansicht erzeugt keine Rekurrenz und verändert weder Topologie noch Zellzustand.</div>`;
  root.appendChild(panel);
  $("recurrent-runtime-refresh")?.addEventListener("click", refreshRuntime);
}

function ensureControlPanel() {
  const root = $("tab-settings");
  if (!root || $("mhrn-recurrent-control")) return;
  const panel = document.createElement("section");
  panel.id = "mhrn-recurrent-control";
  panel.className = "card small-snn-panel";
  panel.dataset.mhrnRoute = "control:recurrent";
  panel.hidden = true;
  panel.innerHTML = `
    <header class="small-snn-head"><div><span class="workspace-kicker">CONTROL · STAGE 2</span><h2>Rekurrenz-Parameter</h2><p>Relevante Konstruktionsparameter werden ausschließlich als Pending Changes vorbereitet.</p></div><span id="recurrent-pending" class="small-snn-stage-badge">0 pending</span></header>
    <div id="recurrent-control-fields" class="small-snn-control-fields"></div>
    <div class="small-snn-actions"><button id="recurrent-stage" type="button">Stage changes</button><button id="recurrent-apply" type="button" class="btn-primary">Apply</button><button type="button" data-route-jump="control:parameters">Alle Parameter</button><button type="button" data-route-jump="science:recurrent">Wissenschaft</button></div>
    <div id="recurrent-control-status" class="small-snn-status">lade …</div>
    <div class="small-snn-boundary">Topologie-, Radius- und Refraktäränderungen sind wissenschaftlich sensitiv. Ein neuer Run/Restart ist erforderlich.</div>`;
  root.appendChild(panel);
  $("recurrent-stage")?.addEventListener("click", stageControl);
  $("recurrent-apply")?.addEventListener("click", applyControl);
}

function graphSvg(neurons, synapses) {
  const nodes = neurons.slice(0, 12);
  if (!nodes.length) return "<p>Keine Neuronen verfügbar.</p>";
  const ids = new Set(nodes.map((neuron) => neuron.neuron_id));
  const links = synapses
    .filter((synapse) => ids.has(synapse.source_id) && ids.has(synapse.target_id))
    .slice(0, 40);
  const width = 720;
  const height = 330;
  const cx = width / 2;
  const cy = height / 2;
  const radius = 120;
  const pos = new Map(
    nodes.map((neuron, index) => [
      neuron.neuron_id,
      {
        x: cx + Math.cos((index / nodes.length) * Math.PI * 2) * radius,
        y: cy + Math.sin((index / nodes.length) * Math.PI * 2) * radius,
      },
    ]),
  );
  const edges = links
    .map((synapse) => {
      const source = pos.get(synapse.source_id);
      const target = pos.get(synapse.target_id);
      return `<line x1="${source.x}" y1="${source.y}" x2="${target.x}" y2="${target.y}"/><text x="${(source.x + target.x) / 2}" y="${(source.y + target.y) / 2}" class="small-snn-edge-label">w ${fmt(synapse.weight, 2)} · d ${synapse.delay}</text>`;
    })
    .join("");
  const circles = nodes
    .map((neuron) => {
      const point = pos.get(neuron.neuron_id);
      const active = neuron.active ? " active" : "";
      return `<g class="small-snn-node${active}"><circle cx="${point.x}" cy="${point.y}" r="20"/><text x="${point.x}" y="${point.y + 4}" text-anchor="middle">${neuron.spike_count}</text><title>ID ${neuron.neuron_id} · v ${fmt(neuron.v)} · spikes ${neuron.spike_count}</title></g>`;
    })
    .join("");
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Live recurrent SNN topology"><g class="small-snn-edges">${edges}</g>${circles}</svg>`;
}

async function loadNetwork(limit = 12) {
  const [summary, neurons, synapses] = await Promise.all([
    json("/api/network/summary"),
    json(`/api/network/neurons?limit=${limit}&offset=0`),
    json("/api/network/synapses?limit=160&offset=0"),
  ]);
  return {
    summary,
    neurons: neurons.neurons || [],
    synapses: synapses.synapses || [],
  };
}

function recurrentEdges(neurons, synapses) {
  const visible = new Set(neurons.map((neuron) => neuron.neuron_id));
  const adjacency = new Map();
  for (const synapse of synapses) {
    if (!visible.has(synapse.source_id) || !visible.has(synapse.target_id)) continue;
    if (!adjacency.has(synapse.source_id)) adjacency.set(synapse.source_id, new Set());
    adjacency.get(synapse.source_id).add(synapse.target_id);
  }
  let reciprocal = 0;
  for (const [source, targets] of adjacency) {
    for (const target of targets) {
      if (source < target && adjacency.get(target)?.has(source)) reciprocal += 1;
    }
  }
  return reciprocal;
}

function summaryHtml(data) {
  const summary = data.summary;
  return [
    kv("Neuronen", summary.neuron_count),
    kv("Synapsen", summary.synapse_count),
    kv("Aktive Neuronen", summary.active_neurons),
    kv("Spikes gesamt", summary.total_spikes),
    kv("Event queue", summary.queue_depth),
    kv("Tick", summary.current_tick),
    kv("reziproke Paare · Ausschnitt", recurrentEdges(data.neurons, data.synapses)),
    kv("mean v", summary.mean_v),
  ].join("");
}

async function refreshScience() {
  if (document.body.dataset.currentArea !== "science" || document.body.dataset.currentRoute !== "recurrent") return;
  try {
    const data = await loadNetwork();
    $("recurrent-science-summary").innerHTML = summaryHtml(data);
    $("recurrent-science-graph").innerHTML = graphSvg(data.neurons, data.synapses);
    $("recurrent-science-status").textContent = `Quelle live_runtime · Tick ${data.summary.current_tick} · Stage-2 reference: 20.000 ticks · RQ-SNN-001: 100.000 ticks/run DATA`;
  } catch (error) {
    $("recurrent-science-status").textContent = `Nicht verfügbar: ${error.message}`;
  }
}

async function refreshRuntime() {
  if (
    document.body.dataset.currentArea !== "wesen" ||
    document.body.dataset.currentRoute !== "recurrent" ||
    state.inFlight
  ) return;
  state.inFlight = true;
  try {
    const data = await loadNetwork();
    $("recurrent-runtime-summary").innerHTML = summaryHtml(data);
    $("recurrent-runtime-graph").innerHTML = graphSvg(data.neurons, data.synapses);
    const tick = Number(data.summary.current_tick ?? 0);
    const deltaTick = state.lastTick === null ? 0 : tick - state.lastTick;
    state.lastTick = tick;
    const moving = deltaTick > 0 ? "RUNNING" : "IDLE/UNCHANGED";
    const status = $("recurrent-runtime-status");
    status.dataset.state = deltaTick > 0 ? "ok" : "idle";
    status.textContent = `${moving} · Tick ${tick} · Δtick ${deltaTick} · queue ${data.summary.queue_depth} · spikes ${data.summary.total_spikes} · live_runtime`;
  } catch (error) {
    const status = $("recurrent-runtime-status");
    status.dataset.state = "error";
    status.textContent = `Nicht verfügbar: ${error.message}`;
  } finally {
    state.inFlight = false;
  }
}

function effective(name) {
  return state.pending[name]?.proposed_value ?? state.parameters[name]?.value;
}

function renderControl() {
  const holder = $("recurrent-control-fields");
  if (!holder) return;
  holder.innerHTML = EDITABLE.map((name) => {
    const parameter = state.parameters[name];
    if (!parameter) return `<label><span>${name}</span><input disabled value="not exposed"></label>`;
    const pending = state.pending[name] ? " · pending" : "";
    return `<label><span>${name}${pending}</span><input type="number" data-recurrent-param="${name}" value="${effective(name)}" min="${parameter.min ?? ""}" max="${parameter.max ?? ""}" step="any"><small>${parameter.description || ""}</small></label>`;
  }).join("");
  const count = Object.keys(state.pending).filter((name) => EDITABLE.includes(name)).length;
  $("recurrent-pending").textContent = `${count} pending`;
}

async function refreshControl() {
  if (document.body.dataset.currentArea !== "control" || document.body.dataset.currentRoute !== "recurrent") return;
  try {
    const [parameters, pending] = await Promise.all([
      json("/api/parameters"),
      json("/api/parameters/pending"),
    ]);
    state.parameters = parameters.parameters || {};
    state.pending = pending.pending || {};
    renderControl();
    $("recurrent-control-status").textContent = "Recurrent-network settings synchronized.";
  } catch (error) {
    $("recurrent-control-status").textContent = `Nicht verfügbar: ${error.message}`;
  }
}

async function stageControl() {
  const inputs = [...document.querySelectorAll("[data-recurrent-param]")];
  const proposals = [];
  for (const input of inputs) {
    const name = input.dataset.recurrentParam;
    const value = Number(input.value);
    if (!Number.isFinite(value)) continue;
    if (value !== effective(name)) proposals.push([name, value]);
  }
  try {
    for (const [name, value] of proposals) {
      await json(`/api/parameters/${encodeURIComponent(name)}/pending`, {
        method: "POST",
        body: JSON.stringify({ value }),
      });
    }
    await refreshControl();
    $("recurrent-control-status").textContent = proposals.length
      ? `${proposals.length} Änderung(en) vorgemerkt.`
      : "Keine Änderungen.";
  } catch (error) {
    $("recurrent-control-status").textContent = `Stage failed: ${error.message}`;
  }
}

async function applyControl() {
  const names = Object.keys(state.pending).filter((name) => EDITABLE.includes(name));
  if (!names.length) return;
  try {
    await json("/api/parameters/pending/apply", {
      method: "POST",
      body: JSON.stringify({ names }),
    });
    await refreshControl();
    $("recurrent-control-status").textContent = `${names.length} Rekurrenz-Parameter angewendet. Neuer Run/Restart erforderlich.`;
  } catch (error) {
    $("recurrent-control-status").textContent = `Apply failed: ${error.message}`;
  }
}

function routeRefresh() {
  const area = document.body.dataset.currentArea;
  const route = document.body.dataset.currentRoute;
  if (route !== "recurrent") return;
  if (area === "science") refreshScience();
  if (area === "wesen") refreshRuntime();
  if (area === "control") refreshControl();
}

function syncPolling() {
  const area = document.body.dataset.currentArea;
  const route = document.body.dataset.currentRoute;
  const liveRoute = route === "recurrent" && (area === "science" || area === "wesen");
  if (route === "recurrent") routeRefresh();
  if (liveRoute && !state.timer) {
    state.timer = setInterval(routeRefresh, 1000);
    return;
  }
  if (!liveRoute && state.timer) {
    clearInterval(state.timer);
    state.timer = null;
  }
}

export function initRecurrentSNNStage() {
  if (!ensureRoutes()) return;
  ensureSciencePanel();
  ensureRuntimePanel();
  ensureControlPanel();
  const observer = new MutationObserver(syncPolling);
  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ["data-current-area", "data-current-route"],
  });
  document.addEventListener("click", (event) => {
    if (event.target.closest('[data-area-route="recurrent"], [data-route-card="recurrent"]')) {
      setTimeout(syncPolling, 0);
    }
  });
  window.addEventListener(
    "beforeunload",
    () => state.timer && clearInterval(state.timer),
    { once: true },
  );
  syncPolling();
}
