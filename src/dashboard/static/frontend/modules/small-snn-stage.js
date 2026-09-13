"use strict";

const ROUTES = Object.freeze({
  science: ["snn", "Kleines SNN", "network", "view", "snn"],
  wesen: ["snn", "SNN", "wesen", "focus", "#mhrn-runtime-snn"],
  control: ["snn", "SNN-Parameter", "settings", "focus", "#mhrn-small-snn-control"],
});

const EDITABLE = Object.freeze([
  "network.initial_connections_per_neuron",
  "network.neighbour_radius",
]);

const state = {
  timer: null,
  parameters: {},
  pending: {},
  runtimeLastTick: null,
  runtimeInFlight: false,
};
const $ = (id) => document.getElementById(id);

async function json(url, options = {}) {
  const response = await fetch(url, {
    cache: "no-store",
    ...options,
    headers: { Accept: "application/json", "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const payload = await response.json();
  if (!response.ok || payload.ok === false) throw new Error(payload.error || payload.message || `HTTP ${response.status}`);
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
  button.innerHTML = `<span>S1</span><strong>${route[1]}</strong>`;
  grid.appendChild(button);
  button.addEventListener("click", () => architecture.selectRoute(areaId, route[0]));
}

function addRoute(areaId, route) {
  const architecture = window.MHRNWorkspaceArchitecture;
  const routes = architecture?.areas?.[areaId]?.routes;
  if (!architecture?.selectRoute || !Array.isArray(routes)) return false;
  if (!routes.some(([id]) => id === route[0])) {
    const anchorId = areaId === "science" ? "network" : areaId === "wesen" ? "neuron" : "parameters";
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
  if (!root || $("mhrn-small-snn-science")) return;
  const panel = document.createElement("section");
  panel.id = "mhrn-small-snn-science";
  panel.className = "card small-snn-panel";
  panel.dataset.networkView = "snn";
  panel.hidden = true;
  panel.innerHTML = `
    <header class="small-snn-head"><div><span class="workspace-kicker">STAGE 1 · COUPLED SPIKING NETWORK</span><h2>Kleines SNN</h2><p>Mehrere gekoppelte Neuronen, explizite Synapsen, Delays und kausale Spike-Ausbreitung.</p></div><span class="small-snn-stage-badge">Stage 1</span></header>
    <div class="small-snn-boundary">Software-Verifikation eines kleinen SNN. Kein Nachweis biologischer Äquivalenz, Kognition oder großskaliger Traktabilität.</div>
    <div id="small-snn-science-summary" class="small-snn-summary"></div>
    <div class="small-snn-grid"><section><h3>Live-Netz</h3><div id="small-snn-science-graph" class="small-snn-graph"></div></section><section><h3>Stage-1 Contract</h3><div class="small-snn-contract"><strong>A → B → C</strong><span>Delay 1 + 2 ticks</span><span>deterministic replay</span><span>batch/tick equivalence</span><span>sparse explicit topology</span></div><div class="small-snn-actions"><button type="button" data-route-jump="wesen:snn">Runtime ansehen</button><button type="button" data-route-jump="control:snn">SNN-Parameter</button><button type="button" data-route-jump="release:development">Release-Entwicklung</button></div></section></div>
    <div id="small-snn-science-status" class="small-snn-status">lade …</div>`;
  root.appendChild(panel);
}

function ensureRuntimePanel() {
  const root = $("tab-wesen");
  if (!root || $("mhrn-runtime-snn")) return;
  const panel = document.createElement("section");
  panel.id = "mhrn-runtime-snn";
  panel.className = "card small-snn-panel runtime-snn-panel";
  panel.dataset.mhrnRoute = "wesen:snn";
  panel.hidden = true;
  panel.innerHTML = `
    <header class="small-snn-head"><div><span class="workspace-kicker">RUNTIME & WESEN · STAGE 1</span><h2>SNN Live</h2><p>Read-only Ansicht des realen laufenden Netzwerks: Neuronen, Synapsen, Aktivität und Event-Queue.</p></div><button id="small-snn-runtime-refresh" type="button">↻ Aktualisieren</button></header>
    <div id="small-snn-runtime-summary" class="small-snn-summary"></div>
    <div id="small-snn-runtime-graph" class="small-snn-graph small-snn-graph--large"></div>
    <div id="small-snn-runtime-status" class="small-snn-status">lade …</div>
    <div class="small-snn-boundary">Nur Beobachtung. Diese Ansicht verändert weder Topologie noch Zellzustände.</div>`;
  root.appendChild(panel);
  $("small-snn-runtime-refresh")?.addEventListener("click", refreshRuntime);
}

function ensureControlPanel() {
  const root = $("tab-settings");
  if (!root || $("mhrn-small-snn-control")) return;
  const panel = document.createElement("section");
  panel.id = "mhrn-small-snn-control";
  panel.className = "card small-snn-panel";
  panel.dataset.mhrnRoute = "control:snn";
  panel.hidden = true;
  panel.innerHTML = `
    <header class="small-snn-head"><div><span class="workspace-kicker">CONTROL · STAGE 1</span><h2>SNN-Parameter</h2><p>Konstruktionsparameter werden ausschließlich als Pending Changes vorbereitet.</p></div><span id="small-snn-pending" class="small-snn-stage-badge">0 pending</span></header>
    <div id="small-snn-control-fields" class="small-snn-control-fields"></div>
    <div class="small-snn-actions"><button id="small-snn-stage" type="button">Stage changes</button><button id="small-snn-apply" type="button" class="btn-primary">Apply</button><button type="button" data-route-jump="control:parameters">Alle Parameter</button><button type="button" data-route-jump="science:snn">Wissenschaft</button></div>
    <div id="small-snn-control-status" class="small-snn-status">lade …</div>
    <div class="small-snn-boundary">Änderungen an Netzwerkaufbau oder Radius sind wissenschaftlich sensitiv und erfordern einen neuen Run/Restart.</div>`;
  root.appendChild(panel);
  $("small-snn-stage")?.addEventListener("click", stageControl);
  $("small-snn-apply")?.addEventListener("click", applyControl);
}

function graphSvg(neurons, synapses) {
  const nodes = neurons.slice(0, 12);
  if (!nodes.length) return "<p>Keine Neuronen verfügbar.</p>";
  const ids = new Set(nodes.map((n) => n.neuron_id));
  const links = synapses.filter((s) => ids.has(s.source_id) && ids.has(s.target_id)).slice(0, 30);
  const width = 720, height = 330, cx = width / 2, cy = height / 2, radius = 120;
  const pos = new Map(nodes.map((n, i) => [n.neuron_id, { x: cx + Math.cos((i / nodes.length) * Math.PI * 2) * radius, y: cy + Math.sin((i / nodes.length) * Math.PI * 2) * radius }]));
  const edges = links.map((s) => { const a = pos.get(s.source_id), b = pos.get(s.target_id); return `<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"/><text x="${(a.x+b.x)/2}" y="${(a.y+b.y)/2}" class="small-snn-edge-label">w ${fmt(s.weight,2)} · d ${s.delay}</text>`; }).join("");
  const circles = nodes.map((n) => { const p = pos.get(n.neuron_id); const active = n.active ? " active" : ""; return `<g class="small-snn-node${active}"><circle cx="${p.x}" cy="${p.y}" r="20"/><text x="${p.x}" y="${p.y+4}" text-anchor="middle">${n.spike_count}</text><title>ID ${n.neuron_id} · v ${fmt(n.v)} · spikes ${n.spike_count}</title></g>`; }).join("");
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Live small SNN topology"><g class="small-snn-edges">${edges}</g>${circles}</svg>`;
}

async function loadNetwork(limit = 12) {
  const [summary, neurons, synapses] = await Promise.all([
    json("/api/network/summary"),
    json(`/api/network/neurons?limit=${limit}&offset=0`),
    json("/api/network/synapses?limit=120&offset=0"),
  ]);
  return { summary, neurons: neurons.neurons || [], synapses: synapses.synapses || [] };
}

function summaryHtml(s) {
  return [kv("Neuronen", s.neuron_count), kv("Synapsen", s.synapse_count), kv("Aktive Neuronen", s.active_neurons), kv("Spikes gesamt", s.total_spikes), kv("Event queue", s.queue_depth), kv("Tick", s.current_tick), kv("mean v", s.mean_v), kv("mean energy", s.mean_energy)].join("");
}

async function refreshScience() {
  if (document.body.dataset.currentArea !== "science" || document.body.dataset.currentRoute !== "snn") return;
  try {
    const data = await loadNetwork();
    $("small-snn-science-summary").innerHTML = summaryHtml(data.summary);
    $("small-snn-science-graph").innerHTML = graphSvg(data.neurons, data.synapses);
    $("small-snn-science-status").textContent = `Quelle live_runtime · Tick ${data.summary.current_tick} · ${data.neurons.length} Neuronen visualisiert · ${data.synapses.length} Synapsen gelesen`;
  } catch (error) { $("small-snn-science-status").textContent = `Nicht verfügbar: ${error.message}`; }
}

async function refreshRuntime() {
  if (document.body.dataset.currentArea !== "wesen" || document.body.dataset.currentRoute !== "snn" || state.runtimeInFlight) return;
  state.runtimeInFlight = true;
  try {
    const data = await loadNetwork();
    $("small-snn-runtime-summary").innerHTML = summaryHtml(data.summary);
    $("small-snn-runtime-graph").innerHTML = graphSvg(data.neurons, data.synapses);
    const currentTick = Number(data.summary.current_tick ?? 0);
    const deltaTick = state.runtimeLastTick === null ? 0 : currentTick - state.runtimeLastTick;
    state.runtimeLastTick = currentTick;
    const moving = deltaTick > 0 ? "RUNNING" : "IDLE/UNCHANGED";
    const status = $("small-snn-runtime-status");
    status.dataset.state = deltaTick > 0 ? "ok" : "idle";
    status.textContent = `${moving} · Tick ${currentTick} · Δtick ${deltaTick} · queue ${data.summary.queue_depth} · total spikes ${data.summary.total_spikes} · live_runtime`;
  } catch (error) {
    const status = $("small-snn-runtime-status");
    status.dataset.state = "error";
    status.textContent = `Nicht verfügbar: ${error.message}`;
  } finally {
    state.runtimeInFlight = false;
  }
}

function effective(name) {
  return state.pending[name]?.proposed_value ?? state.parameters[name]?.value;
}

function renderControl() {
  const holder = $("small-snn-control-fields");
  if (!holder) return;
  holder.innerHTML = EDITABLE.map((name) => {
    const p = state.parameters[name];
    if (!p) return `<label><span>${name}</span><input disabled value="not exposed"></label>`;
    const pending = state.pending[name] ? " · pending" : "";
    return `<label><span>${name}${pending}</span><input type="number" data-small-snn-param="${name}" value="${effective(name)}" min="${p.min ?? ""}" max="${p.max ?? ""}" step="any"><small>${p.description || ""}</small></label>`;
  }).join("");
  const count = Object.keys(state.pending).filter((name) => EDITABLE.includes(name)).length;
  $("small-snn-pending").textContent = `${count} pending`;
}

async function refreshControl() {
  if (document.body.dataset.currentArea !== "control" || document.body.dataset.currentRoute !== "snn") return;
  try {
    const [parameters, pending] = await Promise.all([json("/api/parameters"), json("/api/parameters/pending")]);
    state.parameters = parameters.parameters || {};
    state.pending = pending.pending || {};
    renderControl();
    $("small-snn-control-status").textContent = "SNN construction settings synchronized.";
  } catch (error) { $("small-snn-control-status").textContent = `Nicht verfügbar: ${error.message}`; }
}

async function stageControl() {
  const inputs = [...document.querySelectorAll("[data-small-snn-param]")];
  const proposals = [];
  for (const input of inputs) {
    const name = input.dataset.smallSnnParam;
    const value = Number(input.value);
    if (!Number.isFinite(value)) continue;
    if (value !== effective(name)) proposals.push([name, value]);
  }
  try {
    for (const [name, value] of proposals) await json(`/api/parameters/${encodeURIComponent(name)}/pending`, { method: "POST", body: JSON.stringify({ value }) });
    await refreshControl();
    $("small-snn-control-status").textContent = proposals.length ? `${proposals.length} Änderung(en) vorgemerkt.` : "Keine Änderungen.";
  } catch (error) { $("small-snn-control-status").textContent = `Stage failed: ${error.message}`; }
}

async function applyControl() {
  const names = Object.keys(state.pending).filter((name) => EDITABLE.includes(name));
  if (!names.length) return;
  try {
    await json("/api/parameters/pending/apply", { method: "POST", body: JSON.stringify({ names }) });
    await refreshControl();
    $("small-snn-control-status").textContent = `${names.length} SNN-Parameter angewendet. Neuer Run/Restart erforderlich.`;
  } catch (error) { $("small-snn-control-status").textContent = `Apply failed: ${error.message}`; }
}

function routeRefresh() {
  const area = document.body.dataset.currentArea;
  const route = document.body.dataset.currentRoute;
  if (route !== "snn") return;
  if (area === "science") refreshScience();
  if (area === "wesen") refreshRuntime();
  if (area === "control") refreshControl();
}

function syncPolling() {
  const area = document.body.dataset.currentArea;
  const route = document.body.dataset.currentRoute;
  const liveRoute = route === "snn" && (area === "science" || area === "wesen");
  if (route === "snn") routeRefresh();
  if (liveRoute && !state.timer) {
    state.timer = setInterval(routeRefresh, 900);
    return;
  }
  if (!liveRoute && state.timer) {
    clearInterval(state.timer);
    state.timer = null;
  }
}

export function initSmallSNNStage() {
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
    if (event.target.closest('[data-area-route="snn"], [data-route-card="snn"]')) setTimeout(syncPolling, 0);
  });
  window.addEventListener("beforeunload", () => state.timer && clearInterval(state.timer), { once: true });
  syncPolling();
}
