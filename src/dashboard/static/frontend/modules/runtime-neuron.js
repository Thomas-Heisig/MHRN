"use strict";

const state = {
  index: 0,
  total: 0,
  neuron: null,
  timer: null,
  lastSpike: null,
  lastRuntimeTick: null,
  inFlight: false,
};
const $ = (id) => document.getElementById(id);

async function readJson(url) {
  const response = await fetch(url, { cache: "no-store", headers: { Accept: "application/json" } });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
  return payload;
}

function fmt(value, digits = 3) {
  if (value === null || value === undefined) return "—";
  if (typeof value === "number") return Number.isInteger(value) ? String(value) : value.toFixed(digits);
  return String(value);
}

function kv(label, value, digits = 3) {
  return `<div class="runtime-neuron-kv"><span>${label}</span><strong>${fmt(value, digits)}</strong></div>`;
}

function ensurePanel() {
  const root = $("tab-wesen");
  if (!root || $("mhrn-runtime-neuron")) return;
  const panel = document.createElement("section");
  panel.id = "mhrn-runtime-neuron";
  panel.className = "card runtime-neuron-panel";
  panel.hidden = true;
  panel.dataset.mhrnRoute = "wesen:neuron";
  panel.innerHTML = `
    <header class="runtime-neuron-head">
      <div><span class="workspace-kicker">RUNTIME & WESEN · SINGLE CELL</span><h2>Einzelnes Neuron</h2><p>Read-only Darstellung eines realen Live-Neurons aus dem laufenden Netzwerk. Keine simulierten UI-Daten.</p></div>
      <div class="runtime-neuron-badges"><span id="rn-model" class="runtime-neuron-badge">—</span><span id="rn-type" class="runtime-neuron-badge">—</span><span id="rn-state" class="runtime-neuron-badge">—</span></div>
    </header>
    <div class="runtime-neuron-toolbar">
      <label>Neuron index<input id="rn-index" type="number" min="0" value="0"></label>
      <label>Neuron ID<input id="rn-id" type="text" readonly value="—"></label>
      <button id="rn-prev" type="button">← Vorheriges</button><button id="rn-next" type="button">Nächstes →</button><button id="rn-refresh" type="button">↻ Aktualisieren</button>
    </div>
    <div class="runtime-neuron-layout">
      <div id="rn-visual" class="runtime-neuron-visual" data-spiked="false" data-refractory="false">
        <svg viewBox="0 0 560 520" role="img" aria-label="Schematische Darstellung des ausgewählten Neurons">
          <path class="rn-dendrite" d="M210 255 C130 210 95 145 55 95 M205 265 C120 280 80 330 42 385 M220 230 C180 160 180 105 165 55 M220 290 C180 345 160 410 145 470"/>
          <path class="rn-axon" d="M345 260 C410 260 440 230 505 220 M505 220 L535 190 M505 220 L535 250"/>
          <circle class="rn-pulse" cx="280" cy="260" r="108"/><circle class="rn-soma" cx="280" cy="260" r="88"/><circle class="rn-nucleus" cx="280" cy="260" r="38"/>
          <text x="280" y="247" text-anchor="middle">membrane</text><text id="rn-svg-v" x="280" y="270" text-anchor="middle">v = —</text><text id="rn-svg-threshold" x="280" y="291" text-anchor="middle">threshold = —</text>
          <text x="40" y="35">input / dendrites</text><text x="400" y="175">axon / output</text>
        </svg>
        <div class="runtime-neuron-meter-stack">
          <div class="runtime-neuron-meter"><span>Membran</span><div class="runtime-neuron-meter-track"><div id="rn-v-meter" class="runtime-neuron-meter-fill"></div></div><strong id="rn-v-meter-label">—</strong></div>
          <div class="runtime-neuron-meter"><span>Energie</span><div class="runtime-neuron-meter-track"><div id="rn-energy-meter" class="runtime-neuron-meter-fill"></div></div><strong id="rn-energy-meter-label">—</strong></div>
          <div class="runtime-neuron-meter"><span>Threshold Δ</span><div class="runtime-neuron-meter-track"><div id="rn-threshold-meter" class="runtime-neuron-meter-fill"></div></div><strong id="rn-threshold-meter-label">—</strong></div>
        </div>
      </div>
      <div class="runtime-neuron-detail">
        <section class="runtime-neuron-section"><header><h3>Zellzustand</h3><span>live runtime</span></header><div id="rn-cell-state" class="runtime-neuron-grid"></div></section>
        <section class="runtime-neuron-section"><header><h3>Input, Spike & Reset</h3><span>causal state</span></header><div id="rn-spike-state" class="runtime-neuron-grid"></div></section>
        <section class="runtime-neuron-section"><header><h3>Plastizität & Regulation</h3><span>integrated mechanisms</span></header><div id="rn-learning-state" class="runtime-neuron-grid"></div></section>
        <section class="runtime-neuron-section"><header><h3>Modell & Provenienz</h3><span>versioned</span></header><div id="rn-provenance" class="runtime-neuron-grid"></div><div id="rn-config" class="runtime-neuron-config"></div></section>
        <div id="rn-status" class="runtime-neuron-status">Bereit.</div>
        <div class="runtime-neuron-boundary">Diese Ansicht ist Beobachtung/Debugging. Sie verändert den Zellzustand nicht und ist kein Beleg biologischer Äquivalenz.</div>
      </div>
    </div>`;
  root.appendChild(panel);
  $("rn-prev")?.addEventListener("click", () => setIndex(state.index - 1));
  $("rn-next")?.addEventListener("click", () => setIndex(state.index + 1));
  $("rn-refresh")?.addEventListener("click", refresh);
  $("rn-index")?.addEventListener("change", (event) => setIndex(Number(event.target.value)));
}

function isActiveRoute() {
  return document.body.dataset.currentArea === "wesen" && document.body.dataset.currentRoute === "neuron";
}

function syncPolling() {
  if (isActiveRoute()) {
    refresh();
    if (!state.timer) {
      state.timer = setInterval(() => {
        if (isActiveRoute()) refresh();
      }, 750);
    }
    return;
  }
  if (state.timer) {
    clearInterval(state.timer);
    state.timer = null;
  }
}

function setIndex(value) {
  const max = Math.max(0, state.total - 1);
  state.index = Math.max(0, Math.min(max, Number.isFinite(value) ? Math.trunc(value) : 0));
  if ($("rn-index")) $("rn-index").value = String(state.index);
  refresh();
}

function meter(id, labelId, ratio, label) {
  const fill = $(id); const out = $(labelId);
  if (fill) fill.style.width = `${Math.max(0, Math.min(100, ratio * 100))}%`;
  if (out) out.textContent = label;
}

function render(neuron, total) {
  state.neuron = neuron; state.total = total;
  const model = neuron.model || neuron.model_provenance?.id || "unknown";
  const maturity = neuron.model_provenance?.canonical ? "canonical" : (model === "lif-current-v1" ? "experimental" : "configured");
  $("rn-model").textContent = model; $("rn-model").dataset.state = maturity;
  $("rn-type").textContent = neuron.neuron_type || "unknown";
  const ref = neuron.refractory_active ? "refractory" : (neuron.enabled ? "active" : "disabled");
  $("rn-state").textContent = ref; $("rn-state").dataset.state = ref;
  $("rn-id").value = String(neuron.neuron_id); $("rn-index").max = String(Math.max(0,total-1)); $("rn-index").value = String(state.index);
  $("rn-visual").dataset.refractory = String(Boolean(neuron.refractory_active));
  const spikedNow = neuron.last_spike === neuron.runtime_tick && neuron.last_spike !== state.lastSpike;
  $("rn-visual").dataset.spiked = String(spikedNow); state.lastSpike = neuron.last_spike;
  $("rn-svg-v").textContent = `v = ${fmt(neuron.v)} mV`; $("rn-svg-threshold").textContent = `threshold = ${fmt(neuron.current_threshold)} mV`;
  const threshold = Number(neuron.current_threshold ?? 30); const v = Number(neuron.v ?? -65);
  meter("rn-v-meter","rn-v-meter-label",(v + 90) / (threshold + 90),`${fmt(v)} mV`);
  meter("rn-energy-meter","rn-energy-meter-label",Number(neuron.energy ?? 0),fmt(neuron.energy));
  meter("rn-threshold-meter","rn-threshold-meter-label",(Number(neuron.threshold_adaptation ?? 0)+10)/20,fmt(neuron.threshold_adaptation));
  $("rn-cell-state").innerHTML = [kv("v",neuron.v),kv("u",neuron.u),kv("threshold",neuron.current_threshold),kv("energy",neuron.energy),kv("coordinates",`[${[neuron.x1,neuron.x2,neuron.x3,neuron.x4,neuron.x5].join(", ")}]`),kv("enabled",neuron.enabled)].join("");
  $("rn-spike-state").innerHTML = [kv("spike count",neuron.spike_count),kv("last spike tick",neuron.last_spike),kv("refractory",neuron.refractory_active),kv("refractory remaining",neuron.refractory_remaining_ticks),kv("external current",neuron.last_external_current),kv("synaptic current",neuron.last_synaptic_current),kv("input cell",neuron.is_input),kv("output cell",neuron.is_output),kv("runtime tick",neuron.runtime_tick)].join("");
  $("rn-learning-state").innerHTML = [kv("threshold adaptation",neuron.threshold_adaptation),kv("pre trace",neuron.pre_trace),kv("post trace",neuron.post_trace),kv("firing-rate estimate",neuron.firing_rate_estimate),kv("homeostasis",neuron.config?.enable_homeostasis),kv("energy dynamics",neuron.config?.enable_energy_dynamics),kv("traces",neuron.config?.enable_traces),kv("threshold adaptation enabled",neuron.config?.enable_threshold_adaptation)].join("");
  $("rn-provenance").innerHTML = [kv("model",model),kv("family",neuron.model_provenance?.family),kv("version",neuron.model_provenance?.version),kv("canonical",neuron.model_provenance?.canonical),kv("switch count",neuron.model_switch_count),kv("last switch tick",neuron.last_model_switch_tick)].join("");
  const cfg = neuron.config || {};
  $("rn-config").innerHTML = Object.entries(cfg).map(([key,value]) => kv(key,value)).join("");
  const runtimeTick = Number(neuron.runtime_tick ?? 0);
  const deltaTick = state.lastRuntimeTick === null ? 0 : runtimeTick - state.lastRuntimeTick;
  state.lastRuntimeTick = runtimeTick;
  const moving = deltaTick > 0 ? "RUNNING" : "IDLE/UNCHANGED";
  $("rn-status").dataset.state = deltaTick > 0 ? "ok" : "idle";
  $("rn-status").textContent = `${moving} · Tick ${runtimeTick} · Δtick ${deltaTick} · Neuron ${state.index + 1} / ${total} · ID ${neuron.neuron_id} · live_runtime`;
}

async function refresh() {
  if (state.inFlight || !$("mhrn-runtime-neuron")) return;
  const status = $("rn-status");
  state.inFlight = true;
  try {
    if (status && state.lastRuntimeTick === null) { status.dataset.state = "ok"; status.textContent = "Live-Neuron wird gelesen …"; }
    const payload = await readJson(`/api/network/neurons?limit=1&offset=${state.index}`);
    const neuron = payload.neurons?.[0];
    if (!neuron) throw new Error("Neuron an diesem Index nicht vorhanden");
    render(neuron, payload.total || 0);
  } catch (error) {
    if (status) { status.dataset.state = "error"; status.textContent = `Neuron nicht verfügbar: ${error.message}`; }
  } finally {
    state.inFlight = false;
  }
}

export function initRuntimeNeuron() {
  ensurePanel();
  const observer = new MutationObserver(syncPolling);
  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ["data-current-area", "data-current-route"],
  });
  document.addEventListener("click", (event) => {
    if (event.target.closest('[data-area-route="neuron"], [data-route-card="neuron"]')) {
      setTimeout(syncPolling, 0);
    }
  });
  window.addEventListener("beforeunload", () => state.timer && clearInterval(state.timer), { once: true });
  syncPolling();
}
