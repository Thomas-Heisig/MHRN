"use strict";

const SCIENCE_MANIFEST_URL = "/scientific-progress.json";

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[character]));
}

function percent(value) {
  return `${Math.round(Math.max(0, Math.min(1, Number(value) || 0)) * 100)}%`;
}

function injectStyles() {
  if (document.getElementById("mhrn-scientific-progress-styles")) return;
  const style = document.createElement("style");
  style.id = "mhrn-scientific-progress-styles";
  style.textContent = `
    .scientific-progress-panel{margin:18px 14px;padding:16px;border:1px solid var(--rule);border-radius:var(--r-sm);background:var(--paper-2)}
    .scientific-progress-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;margin-bottom:12px}
    .scientific-progress-head h3{margin:.2rem 0}.scientific-progress-head p{margin:.3rem 0;max-width:84ch}
    .scientific-progress-score{min-width:110px;text-align:right}.scientific-progress-score strong{display:block;font-size:1.65rem}
    .scientific-progress-track{display:grid;grid-template-columns:repeat(11,minmax(86px,1fr));gap:7px;overflow-x:auto;padding:5px 0 10px}
    .scientific-stage-node{display:grid;grid-template-rows:auto auto auto auto;gap:5px;text-align:left;padding:9px;border:1px solid var(--rule);border-radius:8px;background:var(--paper);color:inherit;cursor:pointer}
    .scientific-stage-node:hover,.scientific-stage-node:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
    .scientific-stage-number{font-size:.72rem;opacity:.75}.scientific-stage-name{font-size:.78rem;font-weight:700;line-height:1.2;min-height:2.4em}
    .scientific-stage-bar{height:6px;background:var(--paper-3,#d9d9d9);border-radius:999px;overflow:hidden}.scientific-stage-fill{display:block;height:100%;background:currentColor;opacity:.7}
    .scientific-stage-meta{display:flex;justify-content:space-between;gap:4px;font-size:.68rem;opacity:.8}
    .scientific-progress-legend{display:flex;flex-wrap:wrap;gap:7px;margin:8px 0}.scientific-progress-legend span{padding:4px 7px;border:1px solid var(--rule);border-radius:999px;font-size:.72rem}
    .scientific-progress-detail{margin-top:12px;padding:13px;border-top:1px solid var(--rule)}
    .scientific-progress-detail h4{margin:.2rem 0}.scientific-progress-boundary{padding:9px;border-left:3px solid var(--accent);background:var(--paper)}
    .scientific-criteria{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px;margin:10px 0}.scientific-criterion{padding:8px;border:1px solid var(--rule);border-radius:7px}.scientific-criterion strong{float:right}.scientific-criterion small{display:block;clear:both;margin-top:5px;opacity:.75;overflow-wrap:anywhere}
    .scientific-integrity-note{margin-top:10px;font-size:.78rem;opacity:.85}
    @media(max-width:900px){.scientific-progress-head{display:block}.scientific-progress-score{text-align:left;margin-top:8px}.scientific-progress-track{grid-template-columns:repeat(11,110px)}}
  `;
  document.head.appendChild(style);
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
  const host = document.querySelector(".development-timeline-panel");
  if (!host) return;
  document.getElementById("scientific-progress-timeline")?.remove();
  injectStyles();

  const stages = Array.isArray(data.stages) ? data.stages : [];
  const overall = stages.length ? stages.reduce((sum, stage) => sum + (Number(stage.score) || 0), 0) / stages.length : 0;
  const section = document.createElement("section");
  section.id = "scientific-progress-timeline";
  section.className = "scientific-progress-panel";
  section.setAttribute("aria-labelledby", "scientific-progress-title");
  section.innerHTML = `<header class="scientific-progress-head">
    <div><span class="workspace-kicker">SCIENTIFIC MATURITY</span><h3 id="scientific-progress-title">Wissenschaftliche Timeline · Stufen 0–10</h3><p>${escapeHtml(data.scope_note)}</p></div>
    <div class="scientific-progress-score"><span>Stage-Mittel</span><strong>${percent(overall)}</strong><small>keine Kognitionskennzahl</small></div>
  </header>
  <div class="scientific-progress-legend">
    <span>RQ 15%</span><span>Protokoll 20%</span><span>DATA 20%</span><span>reviewte EVID 20%</span><span>Replikation 15%</span><span>Attribution 10%</span>
  </div>
  <div class="scientific-progress-track" role="list" aria-label="Wissenschaftliche Reife je Entwicklungsstufe">
    ${stages.map((stage) => `<button type="button" class="scientific-stage-node" data-scientific-stage="${stage.stage}" role="listitem" title="Stufe ${stage.stage}: ${escapeHtml(stage.name)}">
      <span class="scientific-stage-number">STUFE ${stage.stage}</span><span class="scientific-stage-name">${escapeHtml(stage.name)}</span>
      <span class="scientific-stage-bar"><span class="scientific-stage-fill" style="width:${percent(stage.score)}"></span></span>
      <span class="scientific-stage-meta"><b>${percent(stage.score)}</b><em>${escapeHtml(stage.status)}</em></span>
    </button>`).join("")}
  </div>
  <div id="scientific-progress-detail">${stages.length ? detailMarkup(stages.find((stage) => stage.stage === 6) || stages[0]) : ""}</div>
  <p class="scientific-integrity-note"><strong>Integritätsgrenze:</strong> ${escapeHtml(data.integrity_note)}</p>`;

  const stageList = host.querySelector(".development-stage-list");
  if (stageList) host.insertBefore(section, stageList); else host.appendChild(section);
  section.addEventListener("click", (event) => {
    const button = event.target.closest("[data-scientific-stage]");
    if (!button) return;
    const stage = stages.find((item) => String(item.stage) === String(button.dataset.scientificStage));
    const detail = section.querySelector("#scientific-progress-detail");
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
