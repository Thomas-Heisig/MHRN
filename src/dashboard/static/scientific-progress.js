"use strict";

const SCIENCE_MANIFEST_URL = "/scientific-progress.json";

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[character]));
}

function percent(value) {
  const pct = Math.round(Math.max(0, Math.min(1, Number(value) || 0)) * 1000) / 10;
  return `${Number.isInteger(pct) ? pct.toFixed(0) : pct.toFixed(1)}%`;
}

function setVisible(element, visible) {
  if (!element) return;
  element.hidden = !visible;
  element.classList.toggle("mhrn-route-hidden", !visible);
  element.classList.toggle("mhrn-route-focus-hidden", !visible);
  element.setAttribute("aria-hidden", String(!visible));
  element.style.display = visible ? "" : "none";
  element.inert = !visible;
}

function showScientificReleaseView(panel) {
  const root = document.getElementById("tab-gate");
  if (!root || !panel) return;
  root.querySelectorAll("[data-release-view]").forEach((candidate) => setVisible(candidate, candidate === panel));
  root.querySelectorAll('.mhrn-context-nav[data-area="release"] button').forEach((button) => {
    const active = button.dataset.scienceReleaseRoute === "true";
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", String(active));
  });
  root.querySelectorAll('[data-workspace-views="release"] [data-workspace-view]').forEach((button) => {
    button.classList.toggle("active", button.dataset.workspaceView === "science");
  });
}

function injectStyles() {
  if (document.getElementById("mhrn-scientific-progress-styles")) return;
  const style = document.createElement("style");
  style.id = "mhrn-scientific-progress-styles";
  style.textContent = `
    .scientific-progress-panel{padding:16px;border:1px solid var(--rule);border-radius:var(--r-sm);background:var(--paper-2)}
    .scientific-progress-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;margin-bottom:12px}
    .scientific-progress-head h2,.scientific-progress-head h3{margin:.2rem 0}.scientific-progress-head p{margin:.3rem 0;max-width:88ch}
    .scientific-progress-score{min-width:130px;text-align:right}.scientific-progress-score strong{display:block;font-size:1.65rem}
    .scientific-progress-track{display:grid;grid-template-columns:repeat(11,minmax(86px,1fr));gap:7px;overflow-x:auto;padding:5px 0 10px}
    .scientific-stage-node{display:grid;grid-template-rows:auto auto auto auto;gap:5px;text-align:left;padding:9px;border:1px solid var(--rule);border-radius:8px;background:var(--paper);color:inherit;cursor:pointer}
    .scientific-stage-node:hover,.scientific-stage-node:focus-visible,.scientific-stage-node.is-selected{outline:2px solid var(--accent);outline-offset:1px}
    .scientific-stage-number{font-size:.72rem;opacity:.75}.scientific-stage-name{font-size:.78rem;font-weight:700;line-height:1.2;min-height:2.4em}
    .scientific-stage-bar{height:6px;background:var(--paper-3,#d9d9d9);border-radius:999px;overflow:hidden}.scientific-stage-fill{display:block;height:100%;background:currentColor;opacity:.7}
    .scientific-stage-meta{display:flex;justify-content:space-between;gap:4px;font-size:.68rem;opacity:.8}
    .scientific-progress-legend{display:flex;flex-wrap:wrap;gap:7px;margin:8px 0}.scientific-progress-legend span{padding:4px 7px;border:1px solid var(--rule);border-radius:999px;font-size:.72rem}
    .scientific-progress-detail{margin-top:12px;padding:13px;border-top:1px solid var(--rule)}
    .scientific-progress-detail h4{margin:.2rem 0}.scientific-progress-boundary{padding:9px;border-left:3px solid var(--accent);background:var(--paper)}
    .scientific-criteria{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px;margin:10px 0}.scientific-criterion{padding:8px;border:1px solid var(--rule);border-radius:7px}.scientific-criterion strong{float:right}.scientific-criterion small{display:block;clear:both;margin-top:5px;opacity:.75;overflow-wrap:anywhere}
    .scientific-integrity-note{margin-top:10px;font-size:.78rem;opacity:.85}
    .scientific-two-axis-note{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}.scientific-two-axis-note>div{padding:10px;border:1px solid var(--rule);border-radius:8px;background:var(--paper)}
    @media(max-width:900px){.scientific-progress-head{display:block}.scientific-progress-score{text-align:left;margin-top:8px}.scientific-progress-track{grid-template-columns:repeat(11,110px)}.scientific-two-axis-note{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);
}

function ensureRoutedScienceNavigation(panel) {
  const nav = document.querySelector('.mhrn-context-nav[data-area="release"]');
  if (!nav) return false;
  let button = nav.querySelector('[data-area-route="science"], [data-science-release-route="true"]');
  if (!button) {
    button = document.createElement("button");
    button.type = "button";
    button.setAttribute("role", "tab");
    button.dataset.scienceReleaseRoute = "true";
    button.textContent = "Wissenschaft";
    button.title = "Wissenschaftliche Reife der Stufen 0–10";
    const development = nav.querySelector('[data-area-route="development"]');
    if (development?.nextSibling) nav.insertBefore(button, development.nextSibling); else nav.append(button);
    button.addEventListener("click", () => showScientificReleaseView(panel));
  } else if (button.dataset.areaRoute === "science" && !button.dataset.scienceRouteBound) {
    button.dataset.scienceRouteBound = "true";
    button.addEventListener("click", () => showScientificReleaseView(panel));
  }
  button.dataset.scienceReleaseRoute = "true";
  return true;
}

function ensureReleaseView() {
  const nav = document.querySelector('[data-workspace-views="release"]');
  const board = document.querySelector(".release-board");
  if (!nav || !board) return null;

  let button = nav.querySelector('[data-workspace-view="science"]');
  if (!button) {
    button = document.createElement("button");
    button.type = "button";
    button.dataset.workspaceView = "science";
    button.textContent = "Wissenschaftliche Timeline";
    const development = nav.querySelector('[data-workspace-view="development"]');
    if (development?.nextSibling) nav.insertBefore(button, development.nextSibling); else nav.append(button);
  }

  let panel = board.querySelector('[data-release-view="science"]');
  if (!panel) {
    panel = document.createElement("section");
    panel.className = "release-view-panel scientific-timeline-view";
    panel.dataset.releaseView = "science";
    panel.dataset.workspacePanel = "";
    panel.hidden = true;
    board.append(panel);
  }
  if (!button.dataset.scienceRouteBound) {
    button.dataset.scienceRouteBound = "true";
    button.addEventListener("click", () => showScientificReleaseView(panel));
  }

  if (!ensureRoutedScienceNavigation(panel)) {
    const observer = new MutationObserver(() => {
      if (ensureRoutedScienceNavigation(panel)) observer.disconnect();
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }
  return panel;
}

function criterionMarkup(criterion) {
  const sources = Array.isArray(criterion.sources) ? criterion.sources : [];
  return `<div class="scientific-criterion" data-status="${escapeHtml(criterion.status)}">
    <span>${escapeHtml(criterion.label || criterion.id)}</span><strong>${escapeHtml(criterion.status)}</strong>
    ${sources.length ? `<small>${sources.map(escapeHtml).join(" · ")}</small>` : "<small>kein evidenztragender Nachweis eingetragen</small>"}
  </div>`;
}

function detailMarkup(stage) {
  const criteria = Array.isArray(stage.criteria) ? stage.criteria : [];
  const next = Array.isArray(stage.next_scientific_steps) ? stage.next_scientific_steps : [];
  return `<div class="scientific-progress-detail">
    <span class="workspace-kicker">SCIENTIFIC STAGE ${stage.stage}</span>
    <h4>${escapeHtml(stage.name)} · ${percent(stage.score)}</h4>
    <p class="scientific-progress-boundary"><strong>Claim-Grenze:</strong> ${escapeHtml(stage.claim_boundary)}</p>
    <div class="scientific-criteria">${criteria.map(criterionMarkup).join("")}</div>
    <h5>Nächste wissenschaftliche Schritte</h5>
    <ul>${next.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
  </div>`;
}

function renderScientificProgress(data) {
  const host = ensureReleaseView();
  if (!host) return;
  injectStyles();
  const stages = Array.isArray(data.stages) ? data.stages : [];
  const overall = stages.length ? stages.reduce((sum, stage) => sum + (Number(stage.score) || 0), 0) / stages.length : 0;

  host.innerHTML = `<section id="scientific-progress-timeline" class="scientific-progress-panel" aria-labelledby="scientific-progress-title">
    <header class="scientific-progress-head">
      <div><span class="workspace-kicker">SCIENTIFIC MATURITY</span><h2 id="scientific-progress-title">Wissenschaftliche Timeline · Stufen 0–10</h2><p>${escapeHtml(data.scope_note)}</p></div>
      <div class="scientific-progress-score"><span>Stage-Mittel</span><strong>${percent(overall)}</strong><small>keine Kognitionskennzahl</small></div>
    </header>
    <div class="scientific-two-axis-note"><div><strong>Technische Timeline</strong><p>Implementierung · Integration · Verification · Runtime/Persistenz</p></div><div><strong>Wissenschaftliche Timeline</strong><p>RQ/Hypothese · Protokoll · DATA · reviewte EVID · Replikation · Attribution</p></div></div>
    <div class="scientific-progress-legend"><span>RQ 15%</span><span>Protokoll 20%</span><span>DATA 20%</span><span>reviewte EVID 20%</span><span>Replikation 15%</span><span>Attribution 10%</span></div>
    <div class="scientific-progress-track" role="list" aria-label="Wissenschaftliche Reife je Entwicklungsstufe">
      ${stages.map((stage) => `<button type="button" class="scientific-stage-node ${stage.stage === 6 ? "is-selected" : ""}" data-scientific-stage="${stage.stage}" role="listitem" title="Stufe ${stage.stage}: ${escapeHtml(stage.name)}">
        <span class="scientific-stage-number">STUFE ${stage.stage}</span><span class="scientific-stage-name">${escapeHtml(stage.name)}</span>
        <span class="scientific-stage-bar"><span class="scientific-stage-fill" style="width:${percent(stage.score)}"></span></span>
        <span class="scientific-stage-meta"><b>${percent(stage.score)}</b><em>${escapeHtml(stage.status)}</em></span>
      </button>`).join("")}
    </div>
    <div id="scientific-progress-detail">${stages.length ? detailMarkup(stages.find((stage) => stage.stage === 6) || stages[0]) : ""}</div>
    <p class="scientific-integrity-note"><strong>Integritätsgrenze:</strong> ${escapeHtml(data.integrity_note)}</p>
  </section>`;

  host.addEventListener("click", (event) => {
    const button = event.target.closest("[data-scientific-stage]");
    if (!button) return;
    host.querySelectorAll(".scientific-stage-node").forEach((node) => node.classList.toggle("is-selected", node === button));
    const stage = stages.find((item) => String(item.stage) === String(button.dataset.scientificStage));
    const detail = host.querySelector("#scientific-progress-detail");
    if (stage && detail) detail.innerHTML = detailMarkup(stage);
  });
}

async function loadScientificProgress() {
  try {
    const response = await fetch(SCIENCE_MANIFEST_URL, { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    renderScientificProgress(await response.json());
  } catch (error) {
    console.warn("MHRN scientific timeline unavailable:", error);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => void loadScientificProgress(), { once: true });
} else {
  void loadScientificProgress();
}
