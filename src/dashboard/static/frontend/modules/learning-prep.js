"use strict";

import { apiGet, apiPost } from "../core/api.js";

let refreshTimer = null;
let latestPlans = [];

const SHA256_RE = /^(?:sha256:)?[a-f0-9]{64}$/i;
const WORKFLOW_STEPS = [
  ["proposal", "Proposal"],
  ["approved", "Approval"],
  ["provenance", "Source-Provenienz"],
  ["preregistered", "Präregistrierung"],
  ["runner_frozen", "Runner-Freeze"],
  ["authorized", "Autorisierung"],
  ["executed", "Ausführung"],
  ["evidence", "DATA → Human Review → EVID"],
];

function escapeHtml(value) {
  const span = document.createElement("span");
  span.textContent = value === null || value === undefined ? "" : String(value);
  return span.innerHTML;
}

function planIdDefault() {
  const stamp = new Date().toISOString().replace(/[-:TZ.]/g, "").slice(0, 14);
  return `LP-${stamp}`;
}

function sourceRowMarkup(source = {}, index = 0) {
  const sourceId = source.source_id || (index === 0 ? "SRC-001" : `SRC-${String(index + 1).padStart(3, "0")}`);
  const digest = source.digest || "";
  const origin = source.origin || "research_artifact";
  const partition = source.partition || "train";
  return `
    <fieldset class="learning-source-row" data-learning-source-row>
      <legend>Quelle ${index + 1}</legend>
      <label>Source-ID<input data-source-field="source_id" required value="${escapeHtml(sourceId)}" placeholder="z. B. CL-002-EVID"></label>
      <label>Source Digest (SHA-256)<input data-source-field="digest" required value="${escapeHtml(digest)}" placeholder="sha256:… (64 Hex-Zeichen)" spellcheck="false" autocomplete="off"></label>
      <label>Origin<input data-source-field="origin" required value="${escapeHtml(origin)}"></label>
      <label>Partition<select data-source-field="partition" required>
        ${["train", "validation", "holdout"].map((value) => `<option value="${value}"${partition === value ? " selected" : ""}>${value}</option>`).join("")}
      </select></label>
      <button type="button" class="btn-secondary learning-source-remove" data-remove-source ${index === 0 ? "disabled" : ""}>Quelle entfernen</button>
    </fieldset>`;
}

function ensurePanel() {
  let panel = document.getElementById("mhrn-learning-prep");
  if (panel) return panel;
  const workspace = document.getElementById("tab-control");
  if (!workspace) return null;
  panel = document.createElement("section");
  panel.id = "mhrn-learning-prep";
  panel.className = "mhrn-learning-prep card";
  panel.dataset.panelInfo = "Nicht-ausführende Lernvorbereitung. Proposal und Approval bleiben getrennte, append-only Artefakte. Source-Provenienz wird auditiert; Präregistrierung, Runner-Freeze, Autorisierung und Ausführung bleiben nachgelagerte Gates.";
  panel.innerHTML = `
    <header>
      <div>
        <span class="workspace-kicker">LEARNING PREPARATION · GUARDED</span>
        <h2>Lern-Vorbereitung</h2>
        <p>Proposal, Approval und Provenienz sichtbar trennen. Kein Schritt in diesem Panel führt Lernen aus.</p>
      </div>
      <span id="learning-prep-badge" class="maturity-state pending">lade …</span>
    </header>
    <div class="learning-prep-boundary">
      <strong>Governance-Grenze</strong>
      <span>Approval ≠ Ausführung. Präregistrierung → Runner-Freeze → Autorisierung → Ausführung bleiben separate Schritte. Keine direkte Gewichts-, Spike-, Current- oder Reward-Manipulation.</span>
    </div>
    <div class="learning-prep-grid">
      <section class="learning-prep-section learning-prep-plans">
        <h3>Plan-Historie & Audit</h3>
        <div id="learning-prep-detail" class="learning-prep-detail">lade …</div>
      </section>
      <section class="learning-prep-section">
        <h3>Neues Proposal / Revision</h3>
        <form id="learning-prep-create-form" class="learning-prep-form">
          <label>Plan-ID<input id="learning-plan-id" required value="${planIdDefault()}"></label>
          <label>Objective-ID<input id="learning-objective-id" required value="OBJ-001"></label>
          <label class="learning-prep-wide">Zielbeschreibung<textarea id="learning-objective-description" required rows="2" placeholder="Kontrolliert prüfbares Lernziel"></textarea></label>
          <label>Success Metric<input id="learning-success-metric" required placeholder="retention_ratio >= 0.95"></label>
          <label>Evaluation Question<input id="learning-evaluation-question" required placeholder="Bleibt Retention auf Holdout erhalten?"></label>

          <div class="learning-prep-wide learning-sources-editor">
            <div class="learning-sources-editor-head">
              <div>
                <strong>Source-Provenienz</strong>
                <small>Nur konkrete SHA-256-Digests. Beschreibungstexte oder Platzhalter werden nicht gespeichert.</small>
              </div>
              <button type="button" class="btn-secondary" id="learning-add-source">+ Quelle hinzufügen</button>
            </div>
            <div id="learning-source-list" class="learning-source-list">${sourceRowMarkup({}, 0)}</div>
          </div>

          <label>Baseline Protocol<input id="learning-baseline-protocol" required value="baseline"></label>
          <label>Exposure Protocol<input id="learning-exposure-protocol" required value="exposure"></label>
          <label>Evaluation Protocol<input id="learning-evaluation-protocol" required value="holdout"></label>
          <label>Stopping Rule<input id="learning-stopping-rule" required value="fixed episodes"></label>
          <label class="learning-prep-wide">Controls<input id="learning-controls" required value="learning_off" placeholder="learning_off, shuffled"></label>
          <button type="submit" class="btn-primary">Proposal append-only speichern</button>
        </form>
        <div id="learning-prep-create-result" class="learning-prep-result" aria-live="polite"></div>
      </section>
      <section class="learning-prep-section">
        <h3>Human Approval</h3>
        <p class="learning-prep-help">Approval speichert nur Freigabe-Metadaten. Es startet weder Runner noch Lernen.</p>
        <form id="learning-prep-approve-form" class="learning-prep-form learning-prep-approve-form">
          <label>Plan-ID<input id="learning-approve-plan-id" required placeholder="LP-..."></label>
          <label>Freigegeben durch<input id="learning-approved-by" required placeholder="Operator / Reviewer"></label>
          <button type="submit" class="btn-success">Plan freigeben</button>
        </form>
        <div id="learning-prep-approve-result" class="learning-prep-result" aria-live="polite"></div>
      </section>
    </div>`;
  const anchor = workspace.querySelector(":scope > header");
  if (anchor) anchor.insertAdjacentElement("afterend", panel); else workspace.prepend(panel);
  panel.querySelector("#learning-prep-create-form")?.addEventListener("submit", createProposal);
  panel.querySelector("#learning-prep-approve-form")?.addEventListener("submit", approveProposal);
  panel.querySelector("#learning-add-source")?.addEventListener("click", () => addSourceRow());
  bindSourceRowActions(panel);
  return panel;
}

function value(id) {
  return document.getElementById(id)?.value?.trim() || "";
}

function proposalOf(artifact) {
  return artifact?.proposal && typeof artifact.proposal === "object" ? artifact.proposal : artifact;
}

function planIdOf(artifact) {
  const proposal = proposalOf(artifact);
  return proposal?.plan_id || artifact?.plan_id || artifact?.id || "—";
}

function statusOf(artifact) {
  if (artifact?.status) return String(artifact.status);
  if (artifact?.approved_by || artifact?.proposal) return "approved";
  return "proposal";
}

function digestOf(artifact) {
  return artifact?.digest || artifact?.content_digest || "—";
}

function sourcesOf(artifact) {
  const sources = proposalOf(artifact)?.sources;
  return Array.isArray(sources) ? sources : [];
}

function isSha256Digest(digest) {
  return SHA256_RE.test(String(digest || "").trim());
}

function provenanceAudit(artifact) {
  const sources = sourcesOf(artifact);
  const invalid = sources.filter((source) => !isSha256Digest(source?.digest));
  return {
    total: sources.length,
    invalid,
    valid: sources.length > 0 && invalid.length === 0,
  };
}

function shortDigest(digest) {
  const text = String(digest || "—");
  if (text.length <= 28) return text;
  return `${text.slice(0, 16)}…${text.slice(-10)}`;
}

function artifactSortValue(artifact) {
  return statusOf(artifact) === "approved" ? 1 : 0;
}

function groupArtifacts(plans) {
  const groups = new Map();
  plans.forEach((artifact) => {
    const id = planIdOf(artifact);
    if (!groups.has(id)) groups.set(id, []);
    groups.get(id).push(artifact);
  });
  return Array.from(groups.entries()).map(([id, artifacts]) => ({
    id,
    artifacts: artifacts.sort((a, b) => artifactSortValue(a) - artifactSortValue(b)),
  }));
}

function renderSourceAudit(artifact) {
  const audit = provenanceAudit(artifact);
  if (!audit.total) {
    return `<div class="learning-provenance-alert invalid"><strong>Source-Provenienz fehlt</strong><span>Kein Quellen-Digest registriert. Nachgelagerte Gates bleiben gesperrt.</span></div>`;
  }
  const rows = sourcesOf(artifact).map((source) => {
    const valid = isSha256Digest(source?.digest);
    return `<li class="${valid ? "valid" : "invalid"}">
      <span><strong>${escapeHtml(source?.source_id || "Quelle")}</strong><small>${escapeHtml(source?.origin || "—")} · ${escapeHtml(source?.partition || "—")}</small></span>
      <code title="${escapeHtml(source?.digest || "")}">${escapeHtml(shortDigest(source?.digest))}</code>
      <span class="learning-digest-state">${valid ? "SHA-256 ✓" : "KEIN SHA-256"}</span>
    </li>`;
  }).join("");
  return `
    <div class="learning-provenance-alert ${audit.valid ? "valid" : "invalid"}">
      <strong>${audit.valid ? "Provenienzkette vollständig" : "Provenienzkette unterbrochen"}</strong>
      <span>${audit.valid ? `${audit.total} konkrete SHA-256-Digest(s) registriert.` : `${audit.invalid.length} von ${audit.total} Source-Digest(s) sind Platzhalter oder ungültig.`}</span>
    </div>
    <ul class="learning-source-audit">${rows}</ul>`;
}

function renderWorkflow(group) {
  const approved = group.artifacts.some((artifact) => statusOf(artifact) === "approved");
  const representative = group.artifacts.find((artifact) => statusOf(artifact) === "approved") || group.artifacts[0];
  const provenanceValid = provenanceAudit(representative).valid;
  const states = {
    proposal: group.artifacts.length > 0 ? "done" : "locked",
    approved: approved ? "done" : "current",
    provenance: provenanceValid ? "done" : "blocked",
    preregistered: "locked",
    runner_frozen: "locked",
    authorized: "locked",
    executed: "locked",
    evidence: "locked",
  };
  return `<ol class="learning-workflow" aria-label="Learning Governance Workflow">
    ${WORKFLOW_STEPS.map(([key, label]) => {
      const state = states[key];
      const stateLabel = state === "done" ? "erfüllt" : state === "blocked" ? "blockiert" : state === "current" ? "nächster Gate" : "gesperrt";
      return `<li class="${state}"><span class="learning-workflow-dot" aria-hidden="true"></span><span><strong>${escapeHtml(label)}</strong><small>${stateLabel}</small></span></li>`;
    }).join("")}
  </ol>`;
}

function renderArtifact(artifact) {
  const proposal = proposalOf(artifact);
  const status = statusOf(artifact);
  const objective = proposal?.objective?.description || proposal?.objective || "—";
  const artifactDigest = digestOf(artifact);
  const proposalDigest = proposal?.digest || (status === "proposal" ? artifactDigest : "—");
  const authority = artifact?.runtime_authority || proposal?.authority || "proposal_only";
  return `<article class="learning-artifact ${escapeHtml(status)}">
    <header>
      <div><strong>${status === "approved" ? "Approved Plan" : "Proposal"}</strong><small>${status === "approved" ? `freigegeben durch ${escapeHtml(artifact?.approved_by || "—")}` : "append-only Ausgangsversion"}</small></div>
      <span class="learning-status-pill ${escapeHtml(status)}">${escapeHtml(status)}</span>
    </header>
    <p>${escapeHtml(typeof objective === "object" ? JSON.stringify(objective) : objective)}</p>
    <dl class="learning-artifact-meta">
      <dt>Artifact Digest</dt><dd><code title="${escapeHtml(artifactDigest)}">${escapeHtml(shortDigest(artifactDigest))}</code></dd>
      <dt>Proposal Digest</dt><dd><code title="${escapeHtml(proposalDigest)}">${escapeHtml(shortDigest(proposalDigest))}</code></dd>
      <dt>Runtime authority</dt><dd>${escapeHtml(authority)}</dd>
      <dt>Executed</dt><dd>${artifact?.executed === true ? "true" : "false"}</dd>
    </dl>
  </article>`;
}

function nextRevisionId(baseId) {
  const ids = new Set(latestPlans.map(planIdOf));
  const root = String(baseId).replace(/-R\d+$/i, "");
  let revision = 2;
  while (ids.has(`${root}-R${revision}`)) revision += 1;
  return `${root}-R${revision}`;
}

function renderPlanGroup(group) {
  const approved = group.artifacts.some((artifact) => statusOf(artifact) === "approved");
  const representative = group.artifacts.find((artifact) => statusOf(artifact) === "approved") || group.artifacts[0];
  const audit = provenanceAudit(representative);
  return `<section class="learning-plan-group" data-plan-id="${escapeHtml(group.id)}">
    <header class="learning-plan-group-head">
      <div><span class="workspace-kicker">PLAN</span><h4>${escapeHtml(group.id)}</h4></div>
      <div class="learning-plan-state-stack">
        <span class="learning-status-pill ${approved ? "approved" : "proposal"}">${approved ? "approved" : "proposal"}</span>
        <span class="learning-status-pill ${audit.valid ? "provenance-ok" : "provenance-broken"}">${audit.valid ? "provenance ok" : "provenance offen"}</span>
      </div>
    </header>
    <div class="learning-artifact-list">${group.artifacts.map(renderArtifact).join("")}</div>
    ${renderSourceAudit(representative)}
    <div class="learning-workflow-wrap"><h5>Governance-Workflow</h5>${renderWorkflow(group)}</div>
    <div class="learning-plan-actions">
      ${approved ? "" : `<button type="button" class="btn-success" data-approve-plan="${escapeHtml(group.id)}">Für Approval übernehmen</button>`}
      ${audit.valid ? "" : `<button type="button" class="btn-secondary" data-revise-plan="${escapeHtml(group.id)}">Korrigierte Revision anlegen</button>`}
    </div>
  </section>`;
}

function renderPlans(payload) {
  const target = document.getElementById("learning-prep-detail");
  if (!target) return;
  const plans = Array.isArray(payload?.plans) ? payload.plans : [];
  latestPlans = plans;
  const groups = groupArtifacts(plans);
  const badge = document.getElementById("learning-prep-badge");
  if (badge) badge.textContent = `${plans.length} Artefakt(e) · ${groups.length} Plan/Pläne`;
  if (!plans.length) {
    target.innerHTML = "<p>Keine gespeicherten Lernvorbereitungen.</p>";
    return;
  }
  target.innerHTML = groups.map(renderPlanGroup).join("");
  target.querySelectorAll("[data-approve-plan]").forEach((button) => button.addEventListener("click", () => {
    const input = document.getElementById("learning-approve-plan-id");
    if (input) input.value = button.dataset.approvePlan || "";
    document.getElementById("learning-prep-approve-form")?.scrollIntoView({ behavior: "smooth", block: "center" });
  }));
  target.querySelectorAll("[data-revise-plan]").forEach((button) => button.addEventListener("click", () => prepareRevision(button.dataset.revisePlan || "")));
}

function bindSourceRowActions(root = document) {
  root.querySelectorAll?.("[data-remove-source]").forEach((button) => {
    if (button.dataset.bound === "1") return;
    button.dataset.bound = "1";
    button.addEventListener("click", () => {
      const row = button.closest("[data-learning-source-row]");
      if (!row || button.disabled) return;
      row.remove();
      renumberSourceRows();
    });
  });
}

function renumberSourceRows() {
  const rows = document.querySelectorAll("#learning-source-list [data-learning-source-row]");
  rows.forEach((row, index) => {
    const legend = row.querySelector("legend");
    if (legend) legend.textContent = `Quelle ${index + 1}`;
    const remove = row.querySelector("[data-remove-source]");
    if (remove) remove.disabled = rows.length === 1;
  });
}

function addSourceRow(source = {}) {
  const list = document.getElementById("learning-source-list");
  if (!list) return;
  const index = list.querySelectorAll("[data-learning-source-row]").length;
  list.insertAdjacentHTML("beforeend", sourceRowMarkup(source, index));
  bindSourceRowActions(list);
  renumberSourceRows();
}

function resetSourceRows(sources) {
  const list = document.getElementById("learning-source-list");
  if (!list) return;
  const values = Array.isArray(sources) && sources.length ? sources : [{}];
  list.innerHTML = values.map((source, index) => sourceRowMarkup(source, index)).join("");
  bindSourceRowActions(list);
  renumberSourceRows();
}

function collectSources() {
  return Array.from(document.querySelectorAll("#learning-source-list [data-learning-source-row]")).map((row) => {
    const field = (name) => row.querySelector(`[data-source-field="${name}"]`)?.value?.trim() || "";
    return {
      source_id: field("source_id"),
      digest: field("digest"),
      origin: field("origin"),
      partition: field("partition"),
    };
  });
}

function markDigestValidation(sources) {
  const rows = Array.from(document.querySelectorAll("#learning-source-list [data-learning-source-row]"));
  let firstInvalid = null;
  rows.forEach((row, index) => {
    const input = row.querySelector('[data-source-field="digest"]');
    const valid = isSha256Digest(sources[index]?.digest);
    input?.classList.toggle("learning-digest-invalid", !valid);
    input?.setAttribute("aria-invalid", valid ? "false" : "true");
    if (!valid && !firstInvalid) firstInvalid = input;
  });
  return firstInvalid;
}

function prepareRevision(planId) {
  const artifact = latestPlans.find((item) => planIdOf(item) === planId);
  if (!artifact) return;
  const proposal = proposalOf(artifact);
  const objective = proposal?.objective || {};
  const set = (id, fieldValue) => {
    const input = document.getElementById(id);
    if (input) input.value = fieldValue ?? "";
  };
  const revisionId = nextRevisionId(planId);
  set("learning-plan-id", revisionId);
  set("learning-objective-id", objective.objective_id || "OBJ-001");
  set("learning-objective-description", objective.description || "");
  set("learning-success-metric", objective.success_metric || "");
  set("learning-evaluation-question", objective.evaluation_question || "");
  set("learning-baseline-protocol", proposal?.baseline_protocol || "baseline");
  set("learning-exposure-protocol", proposal?.exposure_protocol || "exposure");
  set("learning-evaluation-protocol", proposal?.evaluation_protocol || "holdout");
  set("learning-stopping-rule", proposal?.stopping_rule || "fixed episodes");
  set("learning-controls", Array.isArray(proposal?.controls) ? proposal.controls.join(", ") : "learning_off");
  resetSourceRows(proposal?.sources || []);
  const result = document.getElementById("learning-prep-create-result");
  if (result) result.textContent = `Revision vorbereitet: ${revisionId}. Ersetze ungültige Source-Digests durch die konkreten Manifest-Hashes; der historische Eintrag bleibt unverändert.`;
  document.getElementById("learning-prep-create-form")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function refresh() {
  const panel = ensurePanel();
  if (!panel || panel.hidden) return;
  try {
    renderPlans(await apiGet("/api/learning/preparation"));
  } catch (error) {
    const target = document.getElementById("learning-prep-detail");
    if (target) target.textContent = `Nicht verfügbar: ${error.message}`;
    const badge = document.getElementById("learning-prep-badge");
    if (badge) badge.textContent = "unavailable";
  }
}

async function createProposal(event) {
  event.preventDefault();
  const result = document.getElementById("learning-prep-create-result");
  const sources = collectSources();
  const firstInvalid = markDigestValidation(sources);
  if (!sources.length || firstInvalid) {
    if (result) result.textContent = "Nicht gespeichert: Jeder Source Digest muss ein konkreter SHA-256 sein (64 Hex-Zeichen, optional mit Präfix sha256:). Platzhalter und Beschreibungstexte sind nicht zulässig.";
    firstInvalid?.focus();
    return;
  }
  const payload = {
    action: "create",
    plan_id: value("learning-plan-id"),
    objective: {
      objective_id: value("learning-objective-id"),
      description: value("learning-objective-description"),
      success_metric: value("learning-success-metric"),
      evaluation_question: value("learning-evaluation-question"),
    },
    sources,
    baseline_protocol: value("learning-baseline-protocol"),
    exposure_protocol: value("learning-exposure-protocol"),
    evaluation_protocol: value("learning-evaluation-protocol"),
    stopping_rule: value("learning-stopping-rule"),
    controls: value("learning-controls").split(",").map((item) => item.trim()).filter(Boolean),
  };
  if (result) result.textContent = "Proposal wird append-only gespeichert …";
  try {
    const response = await apiPost("/api/learning/preparation", payload);
    if (result) result.textContent = `Gespeichert: ${response.status || "created"}. Source-Provenienz ist konkret; keine Lern-Ausführung wurde gestartet.`;
    const approve = document.getElementById("learning-approve-plan-id");
    if (approve) approve.value = payload.plan_id;
    await refresh();
  } catch (error) {
    if (result) result.textContent = `Fehler: ${error.message}`;
  }
}

async function approveProposal(event) {
  event.preventDefault();
  const result = document.getElementById("learning-prep-approve-result");
  const planId = value("learning-approve-plan-id");
  const related = latestPlans.find((item) => planIdOf(item) === planId && statusOf(item) === "proposal");
  const audit = related ? provenanceAudit(related) : null;
  const payload = {
    action: "approve",
    plan_id: planId,
    approved_by: value("learning-approved-by"),
  };
  if (result) {
    result.textContent = audit && !audit.valid
      ? "Approval wird append-only gespeichert. Achtung: Die Source-Provenienz dieses historischen Proposals ist unvollständig; Präregistrierung bleibt im Frontend blockiert."
      : "Approval wird append-only gespeichert …";
  }
  try {
    const response = await apiPost("/api/learning/preparation", payload);
    if (result) result.textContent = `Freigabe gespeichert: ${response.status || "approved"}. Der Plan bleibt nicht-ausführend; Präregistrierung, Freeze und Autorisierung sind weiterhin separate Gates.`;
    await refresh();
  } catch (error) {
    if (result) result.textContent = `Fehler: ${error.message}`;
  }
}

export function initLearningPrep() {
  ensurePanel();
  refresh();
  if (refreshTimer) clearInterval(refreshTimer);
  refreshTimer = window.setInterval(refresh, 30000);
}
