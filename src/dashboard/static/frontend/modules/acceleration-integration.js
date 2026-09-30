"use strict";

const STATUS_LABELS = {
  integrated: "integriert",
  software_verified: "Software verifiziert",
  pending: "Hardware ausstehend",
  passed: "physisch akzeptiert",
  failed: "fehlgeschlagen",
  blocked: "blockiert",
  unavailable: "nicht verfügbar",
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[character]));
}

async function readJson(url) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
  return response.json();
}

function statusClass(status) {
  if (status === "integrated" || status === "software_verified" || status === "passed") return "ok";
  if (status === "failed" || status === "unavailable") return "bad";
  return "pending";
}

function injectStyles() {
  if (document.getElementById("mhrn-acceleration-integration-styles")) return;
  const style = document.createElement("style");
  style.id = "mhrn-acceleration-integration-styles";
  style.textContent = `
    .mhrn-accel-panel{margin:14px 0;padding:14px;border:1px solid var(--rule);border-radius:var(--r-md);background:var(--paper-2)}
    .mhrn-accel-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;margin-bottom:12px}
    .mhrn-accel-head h3{margin:.2rem 0}.mhrn-accel-head p{margin:.2rem 0;max-width:88ch}
    .mhrn-accel-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:9px}
    .mhrn-accel-card{padding:10px;border:1px solid var(--rule);border-radius:8px;background:var(--paper)}
    .mhrn-accel-card h4{margin:0 0 6px}.mhrn-accel-card p{margin:4px 0}
    .mhrn-accel-state{display:inline-flex;padding:2px 7px;border-radius:999px;border:1px solid var(--rule);font-size:.78rem}
    .mhrn-accel-state.ok{font-weight:700}.mhrn-accel-state.bad{font-weight:700}
    .mhrn-accel-meta{display:grid;grid-template-columns:max-content 1fr;gap:4px 10px;margin-top:10px;font-size:.85rem}
    .mhrn-accel-meta dt{font-weight:700}.mhrn-accel-meta dd{margin:0;overflow-wrap:anywhere}
    .mhrn-accel-actions{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}
    .mhrn-accel-boundary{padding:9px;border-left:3px solid var(--accent);background:var(--paper)}
  `;
  document.head.append(style);
}

function panel(id, parent, title, intro) {
  if (!parent) return null;
  let node = document.getElementById(id);
  if (node) return node;
  node = document.createElement("section");
  node.id = id;
  node.className = "mhrn-accel-panel";
  node.innerHTML = `
    <div class="mhrn-accel-head">
      <div><span class="workspace-kicker">CUDA · FE-3</span><h3>${escapeHtml(title)}</h3><p>${escapeHtml(intro)}</p></div>
      <button type="button" data-accel-refresh>Aktualisieren</button>
    </div>
    <div data-accel-body>Lade kanonischen Integrationsstatus …</div>
  `;
  parent.append(node);
  return node;
}

function ensurePanels() {
  const playgroundHost = document.getElementById("pg-mhrn-integration") || document.getElementById("tab-playground");
  const releaseHost = document.querySelector('[data-release-view="development"]');
  const scienceHost = document.getElementById("mhrn-scientific-metrics");
  const oldHost = document.querySelector('#tab-old [data-area-overview="old"]') || document.getElementById("tab-old");
  return {
    playground: panel(
      "mhrn-acceleration-playground",
      playgroundHost,
      "Playground → MHRN Integrationsbrücke",
      "Welche Playground-Bausteine bereits kanonisch sind und welches Gate als Nächstes fehlt."
    ),
    release: panel(
      "mhrn-acceleration-release",
      releaseHost,
      "CUDA / FE-3 Engineering Acceptance",
      "Release-Sicht auf Backend-Vertrag, FE-3-Manifest und physische Hardware-Abnahme."
    ),
    science: panel(
      "mhrn-acceleration-science",
      scienceHost,
      "Backend-Parität: Evidenzgrenze",
      "Engineering Verification bleibt getrennt von wissenschaftlichen DATA/EVID."
    ),
    old: panel(
      "mhrn-acceleration-old",
      oldHost,
      "Archivierte Integrationsflächen",
      "OLD bleibt funktionsfähig, ist aber kein automatischer Promotion-Pfad in den MHRN-Core."
    ),
  };
}

function waveMarkup(waves) {
  return `<div class="mhrn-accel-grid">${(waves || []).map((wave) => `
    <article class="mhrn-accel-card" data-accel-wave="${escapeHtml(wave.id)}">
      <h4>${escapeHtml(wave.label)}</h4>
      <span class="mhrn-accel-state ${statusClass(wave.status)}">${escapeHtml(STATUS_LABELS[wave.status] || wave.status)}</span>
    </article>
  `).join("")}</div>`;
}

function hardwareMarkup(acceleration) {
  const hardware = acceleration.hardware_acceptance || {};
  const manifest = acceleration.fe3_manifest || {};
  const backend = acceleration.backend || {};
  const caps = backend.capabilities || {};
  return `
    <div class="mhrn-accel-boundary"><strong>Interpretationsgrenze:</strong> ${escapeHtml(acceleration.provenance_rule)} Keine Anzeige in diesem Panel erzeugt DATA oder EVID.</div>
    ${waveMarkup(acceleration.waves)}
    <dl class="mhrn-accel-meta">
      <dt>FE-3 Manifest</dt><dd>${escapeHtml(manifest.status)} · ${escapeHtml(manifest.manifest_sha256 || "—")}</dd>
      <dt>CUDA Backend</dt><dd>${escapeHtml(backend.backend_version || backend.status || "—")}</dd>
      <dt>Live Input</dt><dd>${caps.supports_live_external_input === true ? "ja" : "nein"}</dd>
      <dt>Grenzen</dt><dd>${escapeHtml(caps.max_neurons || "—")} Neuronen · ${escapeHtml(caps.max_edges || "—")} Kanten · ${escapeHtml(caps.max_ticks || "—")} Ticks</dd>
      <dt>Plasticity</dt><dd>${escapeHtml(caps.plasticity_semantics || "—")}</dd>
      <dt>Hardware</dt><dd><span class="mhrn-accel-state ${statusClass(hardware.status)}">${escapeHtml(STATUS_LABELS[hardware.status] || hardware.status || "—")}</span> ${escapeHtml(hardware.gpu_identity || "")}</dd>
      <dt>Artefakt</dt><dd>${escapeHtml(hardware.artifact || "noch kein HARDWARE_ACCEPTANCE_<date>.json")}</dd>
      <dt>Nächstes Gate</dt><dd>${escapeHtml(acceleration.next_gate || "—")}</dd>
    </dl>
  `;
}

function scienceMarkup(acceleration) {
  const hardware = acceleration.hardware_acceptance || {};
  return `
    <div class="mhrn-accel-boundary">
      <strong>Kein Evidenzsprung.</strong> FE-3 und CUDA-Parität sind Engineering Verification. Selbst ein grünes physisches Artefakt wird nicht automatisch DATA/EVID.
    </div>
    <div class="mhrn-accel-grid">
      <article class="mhrn-accel-card"><h4>Softwarepfad</h4><span class="mhrn-accel-state ${acceleration.software_path_closed ? "ok" : "pending"}">${acceleration.software_path_closed ? "geschlossen" : "offen"}</span></article>
      <article class="mhrn-accel-card"><h4>Physische FE-3-Abnahme</h4><span class="mhrn-accel-state ${statusClass(hardware.status)}">${escapeHtml(STATUS_LABELS[hardware.status] || hardware.status)}</span></article>
      <article class="mhrn-accel-card"><h4>Scientific status</h4><span class="mhrn-accel-state pending">keine DATA / keine EVID</span></article>
    </div>
  `;
}

function oldMarkup(catalog) {
  const old = (catalog?.candidates || []).find((item) => item.element_id === "old_frontend_views");
  const routes = old?.old_routes || [];
  return `
    <div class="mhrn-accel-boundary"><strong>OLD-Regel:</strong> Aufbewahren statt löschen. Reaktivierung erfolgt explizit; Archivansichten werden nicht stillschweigend kanonisch.</div>
    <p><strong>${routes.length}</strong> Integrations-/Kompatibilitätsrouten sind im Promotion-Katalog ausdrücklich als OLD markiert.</p>
    <p>${escapeHtml(routes.join(", ") || "Keine expliziten OLD-Routen gemeldet.")}</p>
  `;
}

async function refresh(panels) {
  const [integration, catalog] = await Promise.all([
    readJson("/api/integration/status"),
    readJson("/api/playground/integration"),
  ]);
  const acceleration = integration.acceleration;
  if (!acceleration) throw new Error("/api/integration/status enthält keinen acceleration-Block");

  if (panels.playground) panels.playground.querySelector("[data-accel-body]").innerHTML = hardwareMarkup(acceleration);
  if (panels.release) panels.release.querySelector("[data-accel-body]").innerHTML = hardwareMarkup(acceleration);
  if (panels.science) panels.science.querySelector("[data-accel-body]").innerHTML = scienceMarkup(acceleration);
  if (panels.old) panels.old.querySelector("[data-accel-body]").innerHTML = oldMarkup(catalog);
}

export function initAccelerationIntegrationStatus() {
  injectStyles();
  const panels = ensurePanels();
  const roots = Object.values(panels).filter(Boolean);
  if (!roots.length) return;

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-accel-refresh]");
    if (button && roots.some((root) => root.contains(button))) {
      refresh(panels).catch((error) => {
        roots.forEach((root) => {
          const body = root.querySelector("[data-accel-body]");
          if (body) body.textContent = `Integrationsstatus nicht verfügbar: ${error.message || error}`;
        });
      });
    }
  });

  refresh(panels).catch((error) => {
    roots.forEach((root) => {
      const body = root.querySelector("[data-accel-body]");
      if (body) body.textContent = `Integrationsstatus nicht verfügbar: ${error.message || error}`;
    });
  });
}
