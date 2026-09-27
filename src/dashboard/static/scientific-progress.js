"use strict";

const SCIENCE_MANIFEST_URL = "/scientific-progress.json";
const SCIENTIFIC_STATUS_MARKERS = {
  met: "✓", partial: "◐", open: "○",
  advanced: "✓", active: "◐", early: "◐", planned: "○", frontier: "○",
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[character]));
}

function percent(value) {
  const pct = Math.round(Math.max(0, Math.min(1, Number(value) || 0)) * 1000) / 10;
  return `${Number.isInteger(pct) ? pct.toFixed(0) : pct.toFixed(1)}%`;
}

function statusMarkup(status) {
  const label = String(status ?? "open");
  const key = label.toLowerCase();
  const marker = SCIENTIFIC_STATUS_MARKERS[key] || "·";
  const classKey = Object.prototype.hasOwnProperty.call(SCIENTIFIC_STATUS_MARKERS, key) ? key : "unknown";
  return `<span class="scientific-status-mark scientific-status-${classKey}">${marker}</span><span>${escapeHtml(label)}</span>`;
}

function directoryEntryPoint(path) {
  if (path === "research/protocols") return "protocols/COGNITION_CONSCIOUSNESS.md";
  if (path.startsWith("research/experiments/")) return `${path.slice("research/".length)}/manifest.json`;
  if (path.startsWith("research/publications/")) return `${path.slice("research/".length)}/README.md`;
  return null;
}

function registryEntryPoint(identifier) {
  if (/^CLAIM-[A-Z0-9-]+$/.test(identifier)) return "registry/claims.yaml";
  if (/^EVID-\d{4}-\d+$/.test(identifier)) return identifier === "EVID-2026-17" ? "registry/evidence/retired_ids.json" : `registry/evidence/${identifier}.json`;
  const families = [
    ["MEM", "behavior_memory"], ["WM", "behavior_memory"], ["CNS", "cognition"],
    ["EMB", "connectome"], ["GW", "gateway"], ["META", "meta"],
    ["MSBA", "msba"], ["SAFE", "safety"],
  ];
  const family = families.find(([prefix]) => identifier.startsWith(`H-${prefix}-`) || identifier.startsWith(`RQ-${prefix}-`))?.[1];
  if (identifier.startsWith("H-EVAL-")) return "registry/hypotheses.empirical.yaml";
  if (identifier.startsWith("H-")) return family ? `registry/hypotheses.${family}.yaml` : "registry/hypotheses.yaml";
  if (identifier.startsWith("RQ-EVAL-")) return "registry/questions.empirical.yaml";
  if (identifier.startsWith("RQ-")) return family ? `registry/questions.${family}.yaml` : "registry/questions.yaml";
  return null;
}

function sourceMarkup(source) {
  const label = String(source ?? "");
  const normalized = label.replaceAll("\\", "/");
  const match = normalized.match(/^\/?(research|docs)\/(.+)$/);
  let target = null;
  if (match) {
    const filePath = /\.[A-Za-z0-9]{1,12}$/.test(match[2]) ? match[2] : directoryEntryPoint(normalized);
    if (filePath) target = { kind: match[1], path: filePath, directory: filePath !== match[2] };
  } else {
    const registryPath = registryEntryPoint(normalized.trim());
    if (registryPath) target = { kind: "research", path: registryPath, directory: false };
  }
  if (!target) return `<span class="scientific-source-text">${escapeHtml(label)}</span>`;
  return `<button type="button" class="scientific-source-link${target.directory ? " scientific-source-directory-link" : ""}" data-scientific-source-kind="${target.kind}" data-scientific-source-path="${escapeHtml(target.path)}" title="${target.directory ? "Ordnerreferenz öffnen" : "Im File Viewer öffnen"}">${escapeHtml(label)}</button>`;
}

function referenceGroupMarkup(title, references) {
  const unique = [...new Set(references)];
  return `<div class="scientific-reference-group"><h5>${escapeHtml(title)}</h5><div class="scientific-reference-links">${unique.length ? unique.map(sourceMarkup).join("") : '<span class="scientific-source-text">Keine registrierte Referenz</span>'}</div></div>`;
}

function referencePanelMarkup(stage, criteria) {
  const sourceValues = criteria.flatMap((criterion) => Array.isArray(criterion.sources) ? criterion.sources : []);
  const serialized = JSON.stringify(stage);
  const claims = serialized.match(/CLAIM-[A-Z0-9-]+/g) || [];
  const evidence = serialized.match(/EVID-\d{4}-\d+/g) || [];
  const hypotheses = serialized.match(/H-[A-Z0-9-]+/g) || [];
  const experiments = sourceValues.filter((source) => String(source).replaceAll("\\", "/").startsWith("research/experiments/"));
  return `<section class="scientific-reference-panel" aria-label="Wissenschaftliche Register"><div class="scientific-reference-columns">${referenceGroupMarkup("Claims & EVID", [...claims, ...evidence])}${referenceGroupMarkup("Experimente & Hypothesen", [...experiments, ...hypotheses])}</div></section>`;
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
    .scientific-stage-meta{display:flex;justify-content:space-between;gap:4px;font-size:.68rem;opacity:.8}.scientific-stage-meta em{display:inline-flex;align-items:center;gap:3px;font-style:normal}
    .scientific-progress-legend{display:flex;flex-wrap:wrap;gap:7px;margin:8px 0}.scientific-progress-legend span{padding:4px 7px;border:1px solid var(--rule);border-radius:999px;font-size:.72rem}
    .scientific-progress-status-legend{display:flex;flex-wrap:wrap;gap:7px;margin:8px 0}.scientific-progress-status-legend>span{display:inline-flex;align-items:center;gap:4px;padding:4px 7px;border:1px solid var(--rule);border-radius:999px;font-size:.72rem}.scientific-progress-status-legend .scientific-status-mark{padding:0;border:0}
    .scientific-progress-detail{margin-top:12px;padding:13px;border-top:1px solid var(--rule)}
    .scientific-progress-detail h4{margin:.2rem 0}.scientific-progress-boundary{padding:9px;border-left:3px solid var(--accent);background:var(--paper)}
    .scientific-reference-panel{margin:10px 0;padding-top:10px;border-top:1px solid var(--rule)}.scientific-reference-columns{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.scientific-reference-group{min-height:76px;padding:8px;border:1px solid var(--rule);border-radius:6px;background:var(--paper)}.scientific-reference-group h5{margin:0 0 7px;font-size:.68rem}.scientific-reference-links{display:flex;flex-wrap:wrap;gap:4px}
    .scientific-criteria{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px;margin:10px 0}.scientific-criterion{padding:8px;border:1px solid var(--rule);border-radius:7px}.scientific-criterion strong{float:right;display:inline-flex;align-items:center;gap:4px}.scientific-status-mark{display:inline-grid;place-items:center;width:1em;height:1em;font-weight:800}.scientific-status-met{color:var(--moss,#3d8b5c)}.scientific-status-partial{color:var(--amber,#a47720)}.scientific-status-open{color:var(--ink-4,#777)}.scientific-criterion small{display:block;clear:both;margin-top:5px;opacity:.75;overflow-wrap:anywhere}
    .scientific-integrity-note{margin-top:10px;font-size:.78rem;opacity:.85}
    .scientific-two-axis-note{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:12px 0}.scientific-two-axis-note>div{min-height:76px;padding:10px;border:1px solid var(--rule);border-radius:8px;background:var(--paper)}.scientific-two-axis-note strong{display:block;margin-bottom:5px}.scientific-two-axis-note p{margin:0;font-size:.74rem;line-height:1.45}
    .scientific-criterion{display:grid;grid-template-rows:auto minmax(34px,auto);gap:8px;min-height:112px}.scientific-criterion-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;min-height:2.5em}.scientific-criterion-label{font-size:.74rem;line-height:1.35}.scientific-criterion-status{display:inline-flex;align-items:center;gap:4px;flex-shrink:0;font-size:.68rem}.scientific-criterion-sources{display:flex;flex-wrap:wrap;align-content:flex-start;gap:4px;margin:0;padding-top:7px;border-top:1px solid var(--rule)}.scientific-source-link,.scientific-source-text{max-width:100%;padding:2px 5px;border:1px solid var(--rule);border-radius:3px;background:var(--paper-3);color:var(--ink-3);font:500 .58rem/1.35 var(--font-mono);overflow-wrap:anywhere;text-align:left}.scientific-source-link{cursor:pointer;text-decoration:underline;text-underline-offset:2px}.scientific-source-directory-link{border-style:dashed}.scientific-source-link:hover,.scientific-source-link:focus-visible{border-color:var(--accent);color:var(--accent-2);background:var(--accent-wash)}
    @media(max-width:900px){.scientific-progress-head{display:block}.scientific-progress-score{text-align:left;margin-top:8px}.scientific-progress-track{grid-template-columns:repeat(11,110px)}.scientific-two-axis-note,.scientific-reference-columns{grid-template-columns:1fr}}
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
    <div class="scientific-criterion-head"><span class="scientific-criterion-label">${escapeHtml(criterion.label || criterion.id)}</span><strong class="scientific-criterion-status">${statusMarkup(criterion.status)}</strong></div>
    <div class="scientific-criterion-sources">${sources.length ? sources.map(sourceMarkup).join("") : '<span class="scientific-source-text">kein evidenztragender Nachweis eingetragen</span>'}</div>
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
    ${referencePanelMarkup(stage, criteria)}
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
    <div class="scientific-progress-status-legend" aria-label="Statusmarker der wissenschaftlichen Kriterien"><span>${statusMarkup("met")}</span><span>${statusMarkup("partial")}</span><span>${statusMarkup("open")}</span></div>
    <div class="scientific-two-axis-note"><div><strong>Technische Timeline</strong><p>Implementierung · Integration · Verification · Runtime/Persistenz</p></div><div><strong>Wissenschaftliche Timeline</strong><p>RQ/Hypothese · Protokoll · DATA · reviewte EVID · Replikation · Attribution</p></div></div>
    <div class="scientific-progress-legend"><span>RQ 15%</span><span>Protokoll 20%</span><span>DATA 20%</span><span>reviewte EVID 20%</span><span>Replikation 15%</span><span>Attribution 10%</span></div>
    <div class="scientific-progress-track" role="list" aria-label="Wissenschaftliche Reife je Entwicklungsstufe">
      ${stages.map((stage) => `<button type="button" class="scientific-stage-node ${stage.stage === 6 ? "is-selected" : ""}" data-scientific-stage="${stage.stage}" role="listitem" title="Stufe ${stage.stage}: ${escapeHtml(stage.name)}">
        <span class="scientific-stage-number">STUFE ${stage.stage}</span><span class="scientific-stage-name">${escapeHtml(stage.name)}</span>
        <span class="scientific-stage-bar"><span class="scientific-stage-fill" style="width:${percent(stage.score)}"></span></span>
        <span class="scientific-stage-meta"><b>${percent(stage.score)}</b><em>${statusMarkup(stage.status)}</em></span>
      </button>`).join("")}
    </div>
    <div id="scientific-progress-detail">${stages.length ? detailMarkup(stages.find((stage) => stage.stage === 6) || stages[0]) : ""}</div>
    <p class="scientific-integrity-note"><strong>Integritätsgrenze:</strong> ${escapeHtml(data.integrity_note)}</p>
  </section>`;

  host.addEventListener("click", (event) => {
    const source = event.target.closest("[data-scientific-source-path]");
    if (source) {
      document.dispatchEvent(new CustomEvent("brain5d:open-file", {
        detail: { source: source.dataset.scientificSourceKind, path: source.dataset.scientificSourcePath },
      }));
      return;
    }
    const button = event.target.closest("[data-scientific-stage]");
    if (!button) return;
    host.querySelectorAll(".scientific-stage-node").forEach((node) => node.classList.toggle("is-selected", node === button));
    const stage = stages.find((item) => String(item.stage) === String(button.dataset.scientificStage));
    const detail = host.querySelector("#scientific-progress-detail");
    if (stage && detail) detail.innerHTML = detailMarkup(stage);
  });
}

async function loadScientificProgress() {
  ensureReleaseView();
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
