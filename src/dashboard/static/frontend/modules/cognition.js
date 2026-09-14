/** Existing cognition surface: consume summary and prediction endpoints separately. */
import { apiGet, apiPost } from "../core/api.js";
import { displayValue, memorySummary, predictionRows } from "./cognition-contract.js";

let timer = null;
let refreshing = false;
let writing = false;
const escape = (value) => displayValue(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
const row = (name, value) => `<dt>${escape(name)}</dt><dd>${escape(value)}</dd>`;

function ensurePanel() {
  let panel = document.getElementById("mhrn-cognition");
  if (panel) return panel;
  const host = document.getElementById("tab-wesen");
  if (!host) return null;
  panel = document.createElement("section");
  panel.id = "mhrn-cognition";
  panel.className = "mhrn-cognition card";
  panel.innerHTML = `
    <header><h2>Kognition: Ged\u00e4chtnis und Weltmodell</h2><span id="cognition-state-badge" class="maturity-state pending">Unbekannt</span><button type="button" data-refresh>Aktualisieren</button></header>
    <p>Technische Referenzkomponenten. Kein Nachweis neuronalen semantischen Ged\u00e4chtnisses oder eines mehrschrittigen Weltmodells.</p>
    <p data-message role="status" aria-live="polite"></p>
    <div class="cognition-grid">
      <article class="cognition-section"><h4>Zustand</h4><div id="cognition-state-detail" class="cognition-detail" data-state>Wird geladen \u2026</div></article>
      <article class="cognition-section"><h4>Ged\u00e4chtnis</h4><div id="cognition-memory-detail" class="cognition-detail" data-memory>Wird geladen \u2026</div></article>
      <article class="cognition-section"><h4>Weltmodell</h4><div id="cognition-world-model-detail" class="cognition-detail" data-world>Wird geladen \u2026</div></article>
    </div>`;
  const anchor = host.querySelector(":scope > .wesen-subnav") || host.querySelector(":scope > header");
  if (anchor) anchor.insertAdjacentElement("afterend", panel);
  else host.prepend(panel);
  panel.querySelector("[data-refresh]").addEventListener("click", () => refresh(true));
  return panel;
}

function renderState(panel, payload) {
  panel.querySelector("#cognition-state-badge").textContent = displayValue(payload.status);
  panel.querySelector("[data-state]").innerHTML = `<dl>${row("Status", payload.status ?? null)}${row("Verf\u00fcgbar", payload.available ?? null)}</dl>`;
}

function renderMemory(panel, payload) {
  const node = panel.querySelector("[data-memory]");
  const memory = memorySummary(payload);
  if (!memory) { node.textContent = "Ged\u00e4chtnisdaten nicht verf\u00fcgbar."; return; }
  node.innerHTML = `<dl>${row("Episoden", memory.episodeCount)}${row("Arbeitsspeicher", memory.workingCount)}${row("Vorhersagedatens\u00e4tze", memory.predictionCount)}${row("Integrit\u00e4tsdigest", memory.integrityDigest?.slice(0, 16))}</dl>
    <label><input type="checkbox" id="cognition-read-enabled" data-control="read_enabled" ${memory.readEnabled ? "checked" : ""} ${(memory.readEnabled === null || memory.writeEnabled === null) ? "disabled" : ""}> Episoden lesen</label>
    <label><input type="checkbox" id="cognition-write-enabled" data-control="write_enabled" ${memory.writeEnabled ? "checked" : ""} ${(memory.readEnabled === null || memory.writeEnabled === null) ? "disabled" : ""}> Episoden schreiben</label>
    <p>Speicherschalter steuern nicht das Pr\u00e4diktorlernen.</p>`;
  node.querySelectorAll("[data-control]").forEach((input) => input.addEventListener("change", async () => {
    writing = true;
    node.querySelectorAll("input").forEach((control) => { control.disabled = true; });
    const body = { read_enabled: memory.readEnabled, write_enabled: memory.writeEnabled, [input.dataset.control]: input.checked };
    try {
      await apiPost("/api/cognition/memory/controls", body);
      panel.querySelector("[data-message]").textContent = "Speichereinstellung vom Server best\u00e4tigt.";
    } catch (error) {
      panel.querySelector("[data-message]").textContent = `Nicht gespeichert: ${error.message || error}`;
    } finally {
      writing = false;
      await refresh(true);
    }
  }));
}

function renderWorld(panel, model, predictions) {
  const rows = predictionRows(predictions);
  const header = `<dl>${row("Status", model?.status ?? null)}${row("Modellversion", model?.model?.model_version ?? null)}${row("Bedingung", model?.condition ?? null)}</dl>`;
  const boundary = "<p>Fehlerwert: Legacy-Telemetrie mit gemischten Einheiten, keine Genauigkeit. Unsicherheit: nicht kalibrierte St\u00fctzh\u00e4ufigkeit.</p>";
  let content;
  if (rows === null) content = "<p>Vorhersagedaten nicht verf\u00fcgbar.</p>";
  else if (!rows.length) content = "<p>Keine gespeicherten Vorhersagen.</p>";
  else content = `<div class="table-scroll"><table><thead><tr><th>Tick</th><th>Vorhersage</th><th>Beobachtung</th><th>Fehler</th></tr></thead><tbody>${rows.map((item) => `<tr><td>${escape(item.tick)} \u2192 ${escape(item.targetTick)}</td><td>${escape(item.predicted)}</td><td>${escape(item.actual)}</td><td>${escape(item.error)}</td></tr>`).join("")}</tbody></table></div>`;
  panel.querySelector("[data-world]").innerHTML = header + boundary + content;
}

async function refresh(force = false) {
  const panel = ensurePanel();
  if (!panel || refreshing || writing || document.hidden) return;
  if (!force && panel.getClientRects().length === 0) return;
  refreshing = true;
  try {
    const results = await Promise.allSettled([
      apiGet("/api/cognition/state"),
      apiGet("/api/cognition/memory"),
      apiGet("/api/cognition/world-model"),
      apiGet("/api/cognition/predictions?limit=20"),
    ]);
    const [state, memory, model, predictions] = results;
    if (state.status === "fulfilled") renderState(panel, state.value);
    else panel.querySelector("[data-state]").textContent = "Zustand nicht verf\u00fcgbar.";
    if (memory.status === "fulfilled" && !writing) renderMemory(panel, memory.value);
    else if (memory.status !== "fulfilled") panel.querySelector("[data-memory]").textContent = "Ged\u00e4chtnisdaten nicht verf\u00fcgbar.";
    renderWorld(panel, model.status === "fulfilled" ? model.value : null, predictions.status === "fulfilled" ? predictions.value : null);
  } finally { refreshing = false; }
}

export function initCognition() {
  if (timer !== null) return;
  ensurePanel();
  refresh(true);
  timer = window.setInterval(refresh, 5000);
}
