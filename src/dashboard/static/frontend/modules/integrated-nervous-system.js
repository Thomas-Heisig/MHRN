"use strict";

const REFRESH_MS = 5000;
let timer = null;

async function readJson(url) {
  const response = await fetch(url, { cache: "no-store", headers: { Accept: "application/json" } });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
  return payload;
}

function ensurePanel() {
  const feedback = document.getElementById("embodiment-feedback-state");
  const host = feedback?.closest(".being-zone") || feedback?.parentElement?.parentElement;
  if (!host) return null;
  let panel = document.getElementById("stage5-integrated-nervous-system");
  if (panel) return panel;
  panel = document.createElement("section");
  panel.id = "stage5-integrated-nervous-system";
  panel.className = "panel compact-panel";
  panel.setAttribute("aria-label", "Stage 5 integriertes künstliches Nervensystem");
  panel.innerHTML = `
    <h4>Stage 5 · Integriertes Nervensystem</h4>
    <dl class="metric-list">
      <div><dt>Sensorik</dt><dd data-stage5="sensor">—</dd></div>
      <div><dt>Interozeption</dt><dd data-stage5="interoception">—</dd></div>
      <div><dt>Aktorik</dt><dd data-stage5="actuator">—</dd></div>
      <div><dt>Feedback</dt><dd data-stage5="feedback">—</dd></div>
      <div><dt>Ressourcen</dt><dd data-stage5="resources">—</dd></div>
    </dl>
    <p data-stage5="boundary">Engineering-Projektion; keine automatische EVID-Freigabe.</p>`;
  host.append(panel);
  return panel;
}

function set(panel, key, value, title = "") {
  const node = panel.querySelector(`[data-stage5="${key}"]`);
  if (!node) return;
  node.textContent = value;
  if (title) node.title = title;
}

function stageStatus(stage) {
  if (!stage) return "unbekannt";
  if (stage.implemented === false) return "Adapter fehlt";
  if (stage.enabled) return "aktiv";
  return "bereit · deaktiviert";
}

async function refresh() {
  const panel = ensurePanel();
  if (!panel) return;
  try {
    const [state, pipeline, connections] = await Promise.all([
      readJson("/api/embodiment/state"),
      readJson("/api/embodiment/pipeline"),
      readJson("/api/embodiment/connections"),
    ]);
    const stages = pipeline?.stages || {};
    set(panel, "sensor", stageStatus(stages.sensor), "Live-Status aus /api/embodiment/pipeline");
    set(panel, "actuator", stageStatus(stages.actuator), "Autorisierte Aktorik; Verfügbarkeit ist kein Freigabeersatz.");
    set(panel, "feedback", state?.last_observation_state ? "Rückmeldung empfangen" : stageStatus(stages.feedback));

    const metrics = state?.metrics || state || {};
    const resourceBits = [];
    if (Number.isFinite(Number(metrics.cpu_percent))) resourceBits.push(`CPU ${Number(metrics.cpu_percent).toFixed(1)}%`);
    if (Number.isFinite(Number(metrics.memory_percent))) resourceBits.push(`RAM ${Number(metrics.memory_percent).toFixed(1)}%`);
    set(panel, "resources", resourceBits.length ? resourceBits.join(" · ") : "Telemetrie abhängig vom Adapter");

    const connectionItems = Array.isArray(connections) ? connections : (connections?.connections || []);
    const internal = connectionItems.filter((item) => item?.kind === "sensor" || item?.relationship === "observable").length;
    set(panel, "interoception", internal ? `${internal} beobachtbare Verbindung(en)` : "typed · keine erfundenen Werte");
    set(panel, "boundary", "Live-APIs + Stage-5 Engineering-Vertrag · Real-Device/Langzeit und EVID bleiben getrennt.");
  } catch (error) {
    set(panel, "boundary", `Stage-5 Runtime-Projektion nicht verfügbar: ${error.message}`);
  }
}

export function initIntegratedNervousSystem() {
  void refresh();
  if (timer) return;
  timer = window.setInterval(refresh, REFRESH_MS);
  window.addEventListener("beforeunload", () => {
    if (timer) clearInterval(timer);
    timer = null;
  }, { once: true });
}
