"use strict";

const MODEL_CATALOG = Object.freeze({
  "izhikevich-2003": Object.freeze({
    label: "Izhikevich 2003",
    maturity: "canonical",
    version: "mhrn-1.0",
    equation: "Quadratic integrate-and-fire with recovery variable",
    note: "Canonical Stage-0 software reference model.",
    fields: [
      "neuron.a",
      "neuron.b",
      "neuron.c",
      "neuron.d",
      "neuron.initial_v",
      "neuron.initial_u",
      "neuron.izhikevich_threshold",
    ],
  }),
  "lif-current-v1": Object.freeze({
    label: "Current-based LIF",
    maturity: "experimental",
    version: "mhrn-1.0",
    equation: "Current-based leaky integrate-and-fire",
    note: "Alternative experimental treatment for matched model comparisons.",
    fields: [
      "neuron.initial_v",
      "neuron.lif_resting_potential",
      "neuron.lif_tau_m_ms",
      "neuron.lif_resistance",
      "neuron.lif_threshold",
      "neuron.lif_reset",
    ],
  }),
});

const COMMON_FIELDS = Object.freeze([
  "neuron.refractory_ticks",
  "neuron.enable_threshold_adaptation",
  "neuron.enable_energy_dynamics",
  "neuron.enable_traces",
  "neuron.enable_homeostasis",
]);

const FIELD_LABELS = Object.freeze({
  "neuron.a": "a · recovery time scale",
  "neuron.b": "b · recovery sensitivity",
  "neuron.c": "c · reset potential",
  "neuron.d": "d · recovery reset increment",
  "neuron.initial_v": "Initial membrane potential",
  "neuron.initial_u": "Initial recovery variable",
  "neuron.izhikevich_threshold": "Spike threshold",
  "neuron.lif_resting_potential": "Resting potential",
  "neuron.lif_tau_m_ms": "Membrane time constant",
  "neuron.lif_resistance": "Input resistance",
  "neuron.lif_threshold": "Spike threshold",
  "neuron.lif_reset": "Reset potential",
  "neuron.refractory_ticks": "Absolute refractory ticks",
  "neuron.enable_threshold_adaptation": "Threshold adaptation",
  "neuron.enable_energy_dynamics": "Energy dynamics",
  "neuron.enable_traces": "STDP traces",
  "neuron.enable_homeostasis": "Homeostatic regulation",
});

const ROUTE_ID = "cellmodel";
const ROUTE = Object.freeze([ROUTE_ID, "Cell Model", "network", "view", ROUTE_ID]);
const ROUTER_STORAGE_KEY = "mhrn-workspace-router-v1";

const state = {
  parameters: {},
  pending: {},
  busy: false,
};

function byId(id) {
  return document.getElementById(id);
}

function escapeHtml(value) {
  const node = document.createElement("div");
  node.textContent = value == null ? "" : String(value);
  return node.innerHTML;
}

async function readJson(url, options = {}) {
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

function effectiveValue(name) {
  const change = state.pending[name];
  if (change && Object.hasOwn(change, "proposed_value")) return change.proposed_value;
  return state.parameters[name]?.value;
}

function setStatus(message, kind = "ok") {
  const node = byId("science-neuron-status");
  if (!node) return;
  node.textContent = message;
  node.dataset.state = kind;
}

function parseValue(raw, parameter) {
  if (typeof parameter.value === "boolean") return Boolean(raw);
  if (typeof parameter.value === "number") {
    const value = Number(raw);
    if (!Number.isFinite(value)) throw new Error("must be a finite number");
    if (parameter.min != null && value < Number(parameter.min)) throw new Error(`must be >= ${parameter.min}`);
    if (parameter.max != null && value > Number(parameter.max)) throw new Error(`must be <= ${parameter.max}`);
    return Number.isInteger(parameter.value) ? Math.trunc(value) : value;
  }
  return String(raw);
}

function renderField(name) {
  const parameter = state.parameters[name];
  const label = FIELD_LABELS[name] || name;
  if (!parameter) {
    return `<label class="neuron-model-field neuron-model-field--missing"><span>${escapeHtml(label)}</span><input disabled value="not exposed"></label>`;
  }
  const value = effectiveValue(name);
  const pending = state.pending[name] ? '<small class="neuron-field-pending">pending</small>' : "";
  if (typeof parameter.value === "boolean") {
    return `<label class="neuron-model-field neuron-model-field--toggle" title="${escapeHtml(parameter.description || name)}"><span>${escapeHtml(label)} ${pending}</span><input type="checkbox" data-science-neuron-parameter="${escapeHtml(name)}" ${value ? "checked" : ""}></label>`;
  }
  const min = parameter.min != null ? ` min="${escapeHtml(parameter.min)}"` : "";
  const max = parameter.max != null ? ` max="${escapeHtml(parameter.max)}"` : "";
  const step = Number.isInteger(parameter.value) ? "1" : "any";
  const unit = parameter.unit ? `<small>${escapeHtml(parameter.unit)}</small>` : "";
  return `<label class="neuron-model-field" title="${escapeHtml(parameter.description || name)}"><span>${escapeHtml(label)} ${pending}</span><div class="neuron-model-field__input"><input type="number" data-science-neuron-parameter="${escapeHtml(name)}" value="${escapeHtml(value)}" step="${step}"${min}${max}>${unit}</div></label>`;
}

function render() {
  const select = byId("science-neuron-model-select");
  const fields = byId("science-neuron-fields");
  if (!select || !fields) return;

  const configured = effectiveValue("neuron.model");
  if (!select.dataset.userTouched && configured && Object.hasOwn(MODEL_CATALOG, configured)) {
    select.value = configured;
  }
  const model = Object.hasOwn(MODEL_CATALOG, select.value) ? select.value : "izhikevich-2003";
  const descriptor = MODEL_CATALOG[model];

  byId("science-neuron-maturity").textContent = descriptor.maturity;
  byId("science-neuron-maturity").dataset.maturity = descriptor.maturity;
  byId("science-neuron-version").textContent = descriptor.version;
  byId("science-neuron-equation").textContent = descriptor.equation;
  byId("science-neuron-note").textContent = `${descriptor.note} Model or construction changes are scientifically sensitive and require a new run/restart; they do not constitute biological validation.`;
  fields.innerHTML = [...descriptor.fields, ...COMMON_FIELDS].map(renderField).join("");

  const pendingCount = Object.keys(state.pending).filter((name) => name.startsWith("neuron.")).length;
  byId("science-neuron-pending-count").textContent = String(pendingCount);
  setStatus(
    pendingCount
      ? `${pendingCount} neuron change(s) pending review/application.`
      : "Cell-model settings synchronized with the active configuration.",
    pendingCount ? "warning" : "ok"
  );
}

async function refresh() {
  try {
    const [parameters, pending] = await Promise.all([
      readJson("/api/parameters"),
      readJson("/api/parameters/pending"),
    ]);
    state.parameters = parameters.parameters || {};
    state.pending = pending.pending || {};
    render();
  } catch (error) {
    setStatus(`Cell-model parameters unavailable: ${error.message}`, "error");
  }
}

async function stageChanges() {
  if (state.busy) return;
  const select = byId("science-neuron-model-select");
  const fields = byId("science-neuron-fields");
  if (!select || !fields) return;
  const model = select.value;
  if (!Object.hasOwn(MODEL_CATALOG, model)) {
    setStatus(`Unsupported neuron model: ${model}`, "error");
    return;
  }
  if (!state.parameters["neuron.model"]) {
    setStatus("neuron.model is not exposed by the runtime configuration.", "error");
    return;
  }

  const proposals = [];
  if (effectiveValue("neuron.model") !== model) proposals.push(["neuron.model", model]);
  for (const input of fields.querySelectorAll("[data-science-neuron-parameter]")) {
    const name = input.dataset.scienceNeuronParameter;
    const parameter = state.parameters[name];
    if (!name || !parameter) continue;
    try {
      const value = typeof parameter.value === "boolean" ? Boolean(input.checked) : parseValue(input.value, parameter);
      if (value !== effectiveValue(name)) proposals.push([name, value]);
    } catch (error) {
      setStatus(`${name}: ${error.message}`, "error");
      input.focus();
      return;
    }
  }
  if (!proposals.length) {
    setStatus("No neuron changes to stage.", "ok");
    return;
  }

  state.busy = true;
  byId("science-neuron-stage").disabled = true;
  try {
    for (const [name, value] of proposals) {
      await readJson(`/api/parameters/${encodeURIComponent(name)}/pending`, {
        method: "POST",
        body: JSON.stringify({ value }),
      });
    }
    delete select.dataset.userTouched;
    await refresh();
    setStatus(`Staged ${proposals.length} change(s). Review the pending count, then apply or apply+save.`, "warning");
  } catch (error) {
    setStatus(`Failed to stage neuron changes: ${error.message}`, "error");
  } finally {
    state.busy = false;
    byId("science-neuron-stage").disabled = false;
  }
}

async function applyChanges(saveProfile = false) {
  if (state.busy) return;
  const names = Object.keys(state.pending).filter((name) => name.startsWith("neuron."));
  if (!names.length) {
    setStatus("No pending neuron changes to apply.", "ok");
    return;
  }
  state.busy = true;
  try {
    const endpoint = saveProfile ? "/api/parameters/pending/save-profile" : "/api/parameters/pending/apply";
    await readJson(endpoint, { method: "POST", body: JSON.stringify({ names }) });
    await refresh();
    setStatus(`${names.length} neuron change(s) applied${saveProfile ? " and saved to profile" : ""}. Start a new run/restart before interpreting results.`, "warning");
  } catch (error) {
    setStatus(`Apply failed: ${error.message}`, "error");
  } finally {
    state.busy = false;
  }
}

async function cancelChanges() {
  if (state.busy) return;
  const names = Object.keys(state.pending).filter((name) => name.startsWith("neuron."));
  if (!names.length) {
    setStatus("No pending neuron changes to cancel.", "ok");
    return;
  }
  state.busy = true;
  try {
    await readJson("/api/parameters/pending/cancel", { method: "POST", body: JSON.stringify({ names }) });
    await refresh();
    setStatus(`Cancelled ${names.length} pending neuron change(s).`, "ok");
  } catch (error) {
    setStatus(`Cancel failed: ${error.message}`, "error");
  } finally {
    state.busy = false;
  }
}

function ensureStylesheet() {
  if (document.querySelector('link[data-neuron-model-settings]')) return;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = "/neuron-model-settings.css";
  link.dataset.neuronModelSettings = "true";
  document.head.appendChild(link);
}

function addContextRouteButton(nav, architecture) {
  if (!nav || nav.querySelector(`[data-area-route="${ROUTE_ID}"]`)) return;
  const button = document.createElement("button");
  button.type = "button";
  button.setAttribute("role", "tab");
  button.dataset.areaRoute = ROUTE_ID;
  button.title = "Stage 0 single-neuron model and settings";
  button.textContent = "Cell Model";
  const networkButton = nav.querySelector('[data-area-route="network"]');
  if (networkButton?.nextSibling) nav.insertBefore(button, networkButton.nextSibling);
  else nav.appendChild(button);
  button.addEventListener("click", () => architecture.selectRoute("science", ROUTE_ID));
}

function addOverviewRouteCard(architecture) {
  const grid = document.querySelector('[data-area-overview="science"] .mhrn-area-route-grid');
  if (!grid || grid.querySelector(`[data-route-card="${ROUTE_ID}"]`)) return;
  const button = document.createElement("button");
  button.type = "button";
  button.dataset.routeCard = ROUTE_ID;
  button.title = "Cell Model öffnen";
  button.innerHTML = '<span>04</span><strong>Cell Model</strong>';
  const networkCard = grid.querySelector('[data-route-card="network"]');
  if (networkCard?.nextSibling) grid.insertBefore(button, networkCard.nextSibling);
  else grid.appendChild(button);
  button.addEventListener("click", () => architecture.selectRoute("science", ROUTE_ID));
}

function ensureSettingsNavigationFallback(architecture) {
  const nav = document.querySelector(".brain5d-primary-nav");
  if (!nav || nav.querySelector('[data-mhrn-area="settings"]')) return;
  const button = document.createElement("button");
  button.type = "button";
  button.dataset.mhrnArea = "settings";
  button.title = "Settings: App & Integrationen";
  button.innerHTML = '<span class="mhrn-nav-number">06</span><span class="mhrn-nav-icon">S</span><span class="mhrn-nav-copy"><strong>Settings</strong><span>App & Integrationen</span></span>';
  nav.appendChild(button);
  button.addEventListener("click", () => architecture.selectRoute("settings", "overview"));
}

function ensureCanonicalRoute() {
  const architecture = window.MHRNWorkspaceArchitecture;
  const routes = architecture?.areas?.science?.routes;
  if (!architecture?.selectRoute || !Array.isArray(routes)) return false;

  if (!routes.some(([id]) => id === ROUTE_ID)) {
    const networkIndex = routes.findIndex(([id]) => id === "network");
    routes.splice(networkIndex >= 0 ? networkIndex + 1 : routes.length, 0, [...ROUTE]);
  }

  document.querySelectorAll('.mhrn-context-nav[data-area="science"]').forEach((nav) => {
    addContextRouteButton(nav, architecture);
  });
  addOverviewRouteCard(architecture);
  ensureSettingsNavigationFallback(architecture);
  return true;
}

function ensureWorkbench() {
  ensureStylesheet();
  const root = byId("tab-network");
  if (!root) return false;

  if (!byId("mhrn-neuron-model-science")) {
    const panel = document.createElement("section");
    panel.className = "card neuron-model-settings";
    panel.id = "mhrn-neuron-model-science";
    panel.dataset.networkView = ROUTE_ID;
    panel.hidden = true;
    panel.innerHTML = `
      <header class="panel-title neuron-model-settings__header">
        <div>
          <span class="workspace-kicker">STAGE 0 · SINGLE CELL</span>
          <h2>Neuron / Cell Model</h2>
          <p class="panel-subtitle">Model selection and scientifically sensitive single-cell settings.</p>
        </div>
        <div class="neuron-model-provenance" aria-label="Model provenance">
          <span id="science-neuron-maturity" class="neuron-model-badge">unknown</span>
          <span><b id="science-neuron-version">—</b><small>implementation</small></span>
          <span><b id="science-neuron-pending-count">0</b><small>pending</small></span>
        </div>
      </header>
      <div class="neuron-model-selector-row">
        <label for="science-neuron-model-select">Dynamics model
          <select id="science-neuron-model-select">
            <option value="izhikevich-2003">Izhikevich 2003 · canonical</option>
            <option value="lif-current-v1">Current-based LIF · experimental</option>
          </select>
        </label>
        <div class="neuron-model-equation"><span>Equation family</span><strong id="science-neuron-equation">—</strong></div>
      </div>
      <div id="science-neuron-note" class="neuron-model-warning" role="note"></div>
      <div class="neuron-model-shortcuts" aria-label="Related settings">
        <button type="button" class="btn-secondary" data-route-jump="control:parameters">Alle Parameter</button>
        <button type="button" class="btn-secondary" data-route-jump="settings:overview">App Settings</button>
      </div>
      <div id="science-neuron-fields" class="neuron-model-fields" aria-live="polite"></div>
      <div class="neuron-model-actions neuron-model-actions--science">
        <span id="science-neuron-status" class="neuron-model-status">Loading Stage-0 cell-model configuration …</span>
        <button id="science-neuron-cancel" type="button" class="btn-secondary">Cancel pending</button>
        <button id="science-neuron-stage" type="button" class="btn-secondary">Stage changes</button>
        <button id="science-neuron-apply" type="button" class="btn-primary">Apply</button>
        <button id="science-neuron-save" type="button" class="btn-primary">Apply + Save Profile</button>
      </div>`;
    root.appendChild(panel);
  }
  return true;
}

function bind() {
  const select = byId("science-neuron-model-select");
  if (!select || select.dataset.bound === "true") return;
  select.dataset.bound = "true";
  select.addEventListener("input", () => {
    select.dataset.userTouched = "true";
    render();
  });
  byId("science-neuron-stage")?.addEventListener("click", stageChanges);
  byId("science-neuron-apply")?.addEventListener("click", () => applyChanges(false));
  byId("science-neuron-save")?.addEventListener("click", () => applyChanges(true));
  byId("science-neuron-cancel")?.addEventListener("click", cancelChanges);

  document.addEventListener("click", (event) => {
    const routeButton = event.target.closest(`[data-area-route="${ROUTE_ID}"], [data-route-card="${ROUTE_ID}"]`);
    if (routeButton) queueMicrotask(refresh);
  });
}

function restoreCellModelRouteIfRequested() {
  try {
    const saved = JSON.parse(localStorage.getItem(ROUTER_STORAGE_KEY) || "null");
    if (saved?.area === "science" && saved?.route === ROUTE_ID) {
      window.MHRNWorkspaceArchitecture?.selectRoute?.("science", ROUTE_ID);
    }
  } catch (_) {}
}

export function initNeuronModelScience() {
  if (!ensureCanonicalRoute()) return;
  if (!ensureWorkbench()) return;
  bind();
  refresh();
  restoreCellModelRouteIfRequested();
}
