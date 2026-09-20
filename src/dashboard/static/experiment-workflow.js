"use strict";

import { ExperimentWorkflowPanel as BaseExperimentWorkflowPanel } from "./experiment-workflow-base.js?v=experiment-details-20260920a";

function byId(id) {
  return document.getElementById(id);
}

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = String(value ?? "");
  return div.innerHTML;
}

function renderRunStatus(counts = {}) {
  const completed = Number(counts.completed || 0);
  const failed = Number(counts.failed || 0);
  const running = Number(counts.running || 0);
  const total = completed + failed + running + Number(counts.not_started || 0);
  if (!total) {
    return '<span class="experiment-run-status is-empty" title="Noch nicht ausgeführt" aria-label="Noch nicht ausgeführt">— keine Läufe</span>';
  }
  const parts = [];
  if (completed) parts.push(`<span class="experiment-run-status is-complete" title="${completed} technisch abgeschlossen; kein Evidenzurteil" aria-label="${completed} technisch abgeschlossen; kein Evidenzurteil">✓✓ ${completed}</span>`);
  if (failed) parts.push(`<span class="experiment-run-status is-failed" title="${failed} fehlgeschlagen" aria-label="${failed} fehlgeschlagen">✕ ${failed}</span>`);
  if (running) parts.push(`<span class="experiment-run-status is-running" title="${running} läuft gerade" aria-label="${running} läuft gerade">◷ ${running}</span>`);
  return `<span class="experiment-run-summary" title="${total} Experimentläufe">${parts.join(" ")}<small>${total} Läufe</small></span>`;
}

const PROFILE_LABELS = Object.freeze({
  standard: "Registrierter Gesamtplan",
  controls: "Nur Kontrollen",
  treatments: "Nur Treatments",
  replication: "Replikation",
  sensitivity: "Sensitivität",
  pilot: "Pilot",
  short: "Kurzlauf",
});

export class ExperimentWorkflowPanel extends BaseExperimentWorkflowPanel {
  _ensureResearchUX() {
    super._ensureResearchUX();
    const question = this.elements.question;
    if (!question || byId("workflow-research-catalog")) return;

    const host = question.closest("label")?.parentElement;
    if (!host) return;
    const catalog = document.createElement("section");
    catalog.id = "workflow-research-catalog";
    catalog.className = "research-catalog-selector";
    catalog.innerHTML = `
      <div class="panel-title">
        <div>
          <h3>Research Catalog</h3>
          <p>Durchsuchbare Auswahl statt langer Pulldown-Liste. Operational = frozen/preregistered; Exploratory = protokollierter Lauf ohne Evidenz-Promotion.</p>
        </div>
        <span id="workflow-research-count" class="gate-badge pending">0 RQs</span>
      </div>
      <div class="research-catalog-controls">
        <input id="workflow-research-search" type="search" placeholder="RQ, Hypothese oder Begriff suchen …" autocomplete="off">
        <label class="research-catalog-check"><input id="workflow-research-operational" type="checkbox"> nur operational</label>
      </div>
      <div id="workflow-research-results" class="research-catalog-results" role="listbox" aria-label="Forschungsfragen"></div>
      <section id="workflow-research-detail" class="research-rq-detailbox" hidden aria-live="polite" aria-labelledby="workflow-research-detail-title">
        <div class="research-rq-detail-head">
          <div><span class="workspace-kicker">DETAILANSICHT</span><h4 id="workflow-research-detail-title">Forschungsfrage</h4></div>
          <button id="workflow-research-detail-close" type="button" class="icon-btn" aria-label="Detailansicht schließen" title="Detailansicht schließen">×</button>
        </div>
        <div id="workflow-research-detail-content" class="research-rq-detail-content"></div>
        <div class="research-rq-detail-actions">
          <small id="workflow-research-detail-note">Die Übergabe befüllt den kontrollierten Workflow; sie startet keinen Lauf automatisch.</small>
          <button id="workflow-research-detail-use" type="button" class="btn-primary">Zur Ausführung übernehmen</button>
        </div>
      </section>
      <section id="workflow-review-inbox" class="research-review-inbox" aria-label="Offene Human Reviews">
        <div class="research-review-head"><strong>Review Inbox</strong><span id="workflow-review-count" class="gate-badge pending">lädt …</span></div>
        <p>Offene Human Reviews können hier nachvollziehbar abgeschlossen werden. Reviewer, Entscheidung und Kommentar sind Pflicht; ein Review erzeugt niemals automatisch wissenschaftliche Evidenz.</p>
        <div class="research-review-controls">
          <input id="workflow-review-reviewer" type="text" placeholder="Reviewer / Verantwortlicher" autocomplete="name">
          <button id="workflow-review-refresh" type="button">Reviews aktualisieren</button>
        </div>
        <div id="workflow-review-list" class="research-review-list"></div>
      </section>
      <div class="research-dimension-control">
        <label>MSBA Projektions-Dimensionen
          <input id="workflow-projection-dimensions" type="number" min="1" max="32" value="5">
        </label>
        <small>1–32 Dimensionen für externe/MSBA-Projektionsräume. Der persistierte produktive SNN-Core bleibt aus Kompatibilitätsgründen derzeit 5D.</small>
      </div>
      <section class="research-gateway-experiment" aria-label="Gateway Experiment">
        <div class="research-review-head"><strong>Gateway Experiment</strong><span class="gate-badge pending">EXPERIMENTAL</span></div>
        <p class="research-gateway-intro">Dieses Experiment untersucht nur die periphere Gateway-Projektion. Der kanonische 5D-SNN-Core bleibt unveraendert; Aktivitaet, Plastizitaet und ein erzeugter Bericht sind kein Lern- oder Evidenznachweis.</p>
        <div class="research-gateway-controls">
          <label>Experiment ID<input id="workflow-gateway-experiment-id" type="text" placeholder="EXP-GW-..." autocomplete="off"></label>
          <label>Condition<select id="workflow-gateway-condition"><option value="frozen">Frozen</option><option value="random">Random</option><option value="shuffle">Shuffle</option><option value="plastic">Plastic</option></select></label>
          <label>Seed<input id="workflow-gateway-seed" type="number" value="101"></label>
          <button id="workflow-gateway-activate" type="button">Gateway aktivieren</button>
        </div>
        <details class="research-gateway-documentation">
          <summary>Versuchsbedingungen und Guard oeffnen</summary>
          <ul>
            <li><strong>Frozen</strong>: feste Ausgangstopologie als Kontrollbedingung.</li>
            <li><strong>Random</strong>: deterministische Zufallsgewichte fuer den angegebenen Seed.</li>
            <li><strong>Shuffle</strong>: deterministische Zielkanal-Permutation fuer den angegebenen Seed.</li>
            <li><strong>Plastic</strong>: nur mit registrierter, eingefrorener Preregistration, Human Review und mindestens drei unabhaengigen Seeds.</li>
          </ul>
          <p>Die Preregistration muss mindestens Forschungsfrage, Hypothese, Protocol-ID, alle vier Bedingungen, Seed-Strategie, Stop-, Ein-/Ausschlusskriterien, primaere Outcomes, KI-Grenzen und einen Freeze-Block enthalten. Fuer Plastic muss der Freeze-Block unveraenderlich nach dem ersten Lauf und Human Review verpflichtend machen.</p>
          <label>Preregistration JSON (nur fuer registrierte/frozen Protokolle)<textarea id="workflow-gateway-preregistration" rows="6" placeholder='{"research_question":"RQ-GW-...","hypothesis":"...","protocol_id":"...","conditions":[{"id":"frozen"},{"id":"random"},{"id":"shuffle"},{"id":"plastic"}],"seed_strategy":{"minimum_independent_seeds":3},"stopping_rule":"...","inclusion_criteria":["..."],"exclusion_criteria":["..."],"primary_outcomes":["..."],"ai_authority_boundaries":["no core mutation"],"freeze":{"status":"FROZEN","immutable_after_first_run":true,"human_review_required":true}}'></textarea></label>
        </details>
        <div class="research-gateway-report-row"><small id="workflow-gateway-message">Produktive Gateway-Plastizitaet bleibt gesperrt. Erst Aktivierung und danach Berichtserzeugung sind moeglich.</small><button id="workflow-gateway-report" type="button" disabled>Bericht erzeugen</button></div>
      </section>`;
    host.insertAdjacentElement("beforebegin", catalog);
    for (const [field, label] of Object.entries({domain: "Domain", status: "Status", evidence_status: "Evidenzpruefung", experiment_progress: "Versuchsfortschritt"})) {
      const wrapper = document.createElement("label");
      wrapper.textContent = label;
      const select = document.createElement("select");
      select.dataset.catalogFacet = field;
      select.setAttribute("aria-label", label);
      select.add(new Option("Alle", ""));
      select.addEventListener("change", () => this._renderResearchCatalog());
      wrapper.appendChild(select);
      catalog.querySelector(".research-catalog-controls").appendChild(wrapper);
    }

    const style = document.createElement("style");
    style.dataset.researchCatalogStyle = "true";
    style.textContent = `
      .research-catalog-selector{grid-column:1/-1;border:1px solid var(--border-color,#30363d);border-radius:12px;padding:14px;margin-bottom:10px}
      .research-catalog-controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:10px 0}
      .research-catalog-controls input[type=search]{flex:1 1 320px;min-width:220px}
      .research-catalog-check{display:flex!important;gap:7px;align-items:center!important;white-space:nowrap}
      .research-rq-badge{font-size:.72rem;padding:2px 6px;border-radius:999px;border:1px solid currentColor;white-space:nowrap}
      .research-rq-badge.operational{color:#3fb950}.research-rq-badge.exploratory{color:#d29922}
      .experiment-run-summary{display:inline-flex;align-items:center;gap:5px;white-space:nowrap;font-family:var(--font-mono,monospace);font-size:.68rem}
      .experiment-run-summary small{opacity:.75;font-family:inherit}
      .experiment-run-status{font-weight:800;white-space:nowrap}.experiment-run-status.is-complete{color:#3fb950}.experiment-run-status.is-failed{color:#f85149}.experiment-run-status.is-running{color:#d29922}.experiment-run-status.is-empty{color:var(--ink-4,#6e7681)}
      .research-dimension-control{display:flex;gap:12px;align-items:end;flex-wrap:wrap;margin-top:12px;padding-top:10px;border-top:1px solid var(--border-color,#30363d)}
      .research-dimension-control label{max-width:220px}.research-dimension-control small{max-width:680px;opacity:.8}
      .research-review-inbox{margin-top:14px;padding-top:12px;border-top:1px solid var(--border-color,#30363d)}
      .research-review-head,.research-review-controls,.research-review-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
      .research-review-head{justify-content:space-between}.research-review-controls{margin:8px 0}
      .research-review-controls input{min-width:240px;flex:1}.research-review-list{display:grid;gap:8px}
      .research-review-card{border:1px solid var(--border-color,#30363d);border-radius:9px;padding:10px}
      .research-review-card textarea{width:100%;min-height:72px;margin:8px 0;resize:vertical}
      .research-review-meta{font-size:.78rem;opacity:.75}.research-review-empty{opacity:.75;font-style:italic}
      .research-gateway-experiment{margin-top:14px;padding-top:12px;border-top:1px solid var(--border-color,#30363d)}
      .research-gateway-intro{max-width:850px;line-height:1.45}.research-gateway-documentation{margin:10px 0;padding:10px;border:1px solid var(--border-color,#30363d);border-radius:8px}.research-gateway-documentation summary{cursor:pointer;font-weight:700}.research-gateway-documentation ul{margin:8px 0;padding-left:20px}.research-gateway-documentation p{max-width:850px;line-height:1.4}.research-gateway-documentation textarea{display:block;width:100%;margin-top:5px;font-family:var(--font-mono,monospace);font-size:.8rem}
      .research-gateway-controls{display:flex;gap:10px;align-items:end;flex-wrap:wrap;margin:8px 0}
      .research-gateway-controls label{display:grid;gap:4px;min-width:140px}.research-gateway-controls input,.research-gateway-controls select{min-width:120px}
      .research-gateway-controls button,.research-gateway-report-row button{cursor:pointer}.research-gateway-experiment small{display:block;opacity:.78}.research-gateway-report-row{display:flex;gap:10px;align-items:center;justify-content:space-between;flex-wrap:wrap}.research-gateway-report-row button{margin-left:auto}
    `;
    document.head.appendChild(style);

    byId("workflow-research-search")?.addEventListener("input", () => this._renderResearchCatalog());
    byId("workflow-research-operational")?.addEventListener("change", () => this._renderResearchCatalog());
    byId("workflow-research-detail-close")?.addEventListener("click", () => this._closeResearchQuestionDetail());
    byId("workflow-research-detail-use")?.addEventListener("click", () => this._prepareResearchQuestionForExecution(this.researchDetailQuestionId));
    byId("workflow-review-refresh")?.addEventListener("click", () => this._loadReviewInbox());
    byId("workflow-review-list")?.addEventListener("click", (event) => this._handleReviewAction(event));
    byId("workflow-gateway-activate")?.addEventListener("click", () => this._activateGateway());
    byId("workflow-gateway-report")?.addEventListener("click", () => this._generateGatewayReport());
    this._loadReviewInbox();
    byId("workflow-projection-dimensions")?.addEventListener("change", (event) => {
      const value = Math.max(1, Math.min(32, Number(event.target.value) || 5));
      event.target.value = String(value);
      this._syncProjectionDimensions(value);
    });
  }

  async _activateGateway() {
    const message = byId("workflow-gateway-message");
    const activateButton = byId("workflow-gateway-activate");
    const reportButton = byId("workflow-gateway-report");
    const experimentId = (byId("workflow-gateway-experiment-id")?.value || "").trim();
    const condition = byId("workflow-gateway-condition")?.value || "frozen";
    const seed = Number(byId("workflow-gateway-seed")?.value || 101);
    if (!experimentId || !Number.isInteger(seed)) {
      if (message) message.textContent = "Experiment ID und ganzzahliger Seed sind erforderlich.";
      return;
    }
    const rawPreregistration = (byId("workflow-gateway-preregistration")?.value || "").trim();
    let preregistration;
    if (rawPreregistration) {
      try {
        preregistration = JSON.parse(rawPreregistration);
        if (!preregistration || typeof preregistration !== "object" || Array.isArray(preregistration)) throw new Error("Objekt erwartet");
      } catch (error) {
        if (message) message.textContent = `Preregistration JSON ist ungueltig: ${error.message || error}`;
        return;
      }
    } else if (condition === "plastic") {
      if (message) message.textContent = "Plastic ist ohne registrierte, eingefrorene Preregistration blockiert.";
      return;
    }
    if (activateButton) { activateButton.disabled = true; activateButton.textContent = "Pruefe …"; }
    try {
      const response = await fetch(`/api/experiments/${encodeURIComponent(experimentId)}/gateway/activate`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ condition, seed, experiment_mode: true, ...(preregistration ? { preregistration } : {}) }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
      this.gatewayExperimentId = experimentId;
      this.gatewayPreregistration = preregistration || null;
      if (reportButton) reportButton.disabled = false;
      if (message) message.textContent = `Gateway ${condition} aktiv: ${payload.gateway.state}. Produktiv: GESPERRT. Bericht kann jetzt erzeugt werden.`;
      document.dispatchEvent(new CustomEvent("mhrn:gateway-status-updated", { detail: payload }));
    } catch (error) {
      if (message) message.textContent = `Gateway-Start blockiert: ${error.message || error}`;
    } finally {
      if (activateButton) { activateButton.disabled = false; activateButton.textContent = "Gateway aktivieren"; }
    }
  }

  async _generateGatewayReport() {
    const message = byId("workflow-gateway-message");
    const button = byId("workflow-gateway-report");
    if (!this.gatewayExperimentId) {
      if (message) message.textContent = "Erst ein Gateway-Experiment aktivieren.";
      return;
    }
    if (button) { button.disabled = true; button.textContent = "Erzeuge …"; }
    try {
      const response = await fetch(`/api/experiments/${encodeURIComponent(this.gatewayExperimentId)}/gateway/report`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ preregistration: this.gatewayPreregistration }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
      if (message) message.textContent = `Gateway-Bericht erstellt. Evidenzstatus: nicht evidenzbildend.`;
      await this._openArtifact(payload.report);
    } catch (error) {
      if (message) message.textContent = `Bericht konnte nicht erstellt werden: ${error.message || error}`;
    } finally {
      if (button) { button.disabled = false; button.textContent = "Bericht erzeugen"; }
    }
  }

  async _loadReviewInbox() {
    const list = byId("workflow-review-list");
    const count = byId("workflow-review-count");
    if (!list) return;
    try {
      const response = await fetch("/api/research/reviews", { headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error(`Review inbox HTTP ${response.status}`);
      const payload = await response.json();
      this.reviewInbox = Array.isArray(payload.items) ? payload.items : [];
      if (count) {
        count.textContent = `${Number(payload.open || 0)} offen`;
        count.className = `gate-badge ${Number(payload.open || 0) ? "pending" : "success"}`;
      }
      if (!this.reviewInbox.length) {
        list.innerHTML = '<p class="research-review-empty">Keine offenen Human Reviews.</p>';
        return;
      }
      list.innerHTML = this.reviewInbox.map((item, index) => `
        <article class="research-review-card" data-review-index="${index}">
          <strong>${escapeHtml(item.title || item.artifact_path)}</strong>
          <div class="research-review-meta">${escapeHtml(item.research_question_id || item.kind || "review")} · ${escapeHtml(item.artifact_path || "")}</div>
          <p>${escapeHtml(item.summary || "Human Review erforderlich.")}</p>
          <textarea aria-label="Review-Kommentar" placeholder="Begründung / Review-Kommentar"></textarea>
          <div class="research-review-actions">
            <button type="button" data-review-decision="accepted_as_interpretation">Als Interpretation akzeptieren</button>
            <button type="button" data-review-decision="rejected">Ablehnen</button>
          </div>
        </article>`).join("");
    } catch (error) {
      list.innerHTML = `<p class="research-review-empty">Review Inbox nicht verfügbar: ${escapeHtml(error.message || error)}</p>`;
      if (count) count.textContent = "Fehler";
    }
  }

  async _handleReviewAction(event) {
    const button = event.target.closest?.("[data-review-decision]");
    if (!button) return;
    const card = button.closest("[data-review-index]");
    const item = this.reviewInbox?.[Number(card?.dataset.reviewIndex)];
    if (!item) return;
    const reviewer = (byId("workflow-review-reviewer")?.value || "").trim();
    const comments = (card.querySelector("textarea")?.value || "").trim();
    if (!reviewer || !comments) {
      window.alert("Reviewer und Review-Kommentar sind Pflicht.");
      return;
    }
    const review_status = button.dataset.reviewDecision;
    const body = item.kind === "artifact"
      ? { artifact_path: item.artifact_path, reviewer, comments, review_status }
      : { reviewer, comments, review_status };
    button.disabled = true;
    try {
      const response = await fetch(item.review_endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(body),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || payload.message || `HTTP ${response.status}`);
      await this._loadReviewInbox();
      document.dispatchEvent(new CustomEvent("mhrn:research-review-completed", { detail: payload }));
    } catch (error) {
      window.alert(`Review konnte nicht gespeichert werden: ${error.message || error}`);
    } finally {
      button.disabled = false;
    }
  }

  _configureConditionProfiles(preset = this.activePreset) {
    const select = this.elements.conditionProfile;
    if (!select) return;
    const profiles = preset?.profiles || { standard: preset?.conditions || "" };
    select.replaceChildren();
    for (const [key, value] of Object.entries(profiles)) {
      if (!value) continue;
      select.add(new Option(PROFILE_LABELS[key] || key, key));
    }
    if (!select.options.length) select.add(new Option("Standard", "standard"));
    select.value = "standard";
  }

  _renderQuestions() {
    super._renderQuestions();
    this._renderResearchCatalog();
  }

  _isOperational(questionId) {
    return this.protocols.some(
      (item) => item.research_question === questionId && item.preregistration,
    );
  }

  _matchingHypotheses(questionId) {
    return this.hypotheses.filter((item) => item.question_id === questionId);
  }

  _renderResearchCatalog() {
    const results = byId("workflow-research-results");
    const count = byId("workflow-research-count");
    if (!results) return;
    const search = (byId("workflow-research-search")?.value || "").trim().toLowerCase();
    const operationalOnly = Boolean(byId("workflow-research-operational")?.checked);
    const selected = this.elements.question?.value || "";
    const detailOpen = this.researchDetailQuestionId || "";
    const facets = [...document.querySelectorAll("[data-catalog-facet]")];
    for (const select of facets) {
      const value = select.value;
      const field = select.dataset.catalogFacet;
      const configured = this.facets?.[field];
      const options = Array.isArray(configured)
        ? configured
        : [...new Set(this.questions.map((item) => item[field]).filter(Boolean))].sort();
      select.replaceChildren(new Option("Alle", ""), ...options.map((item) => new Option(item, item)));
      select.value = options.includes(value) ? value : "";
    }
    const visible = this.questions.filter((question) => {
      const hypotheses = this._matchingHypotheses(question.id);
      const haystack = [question.id, question.label, ...hypotheses.map((item) => `${item.id} ${item.label}`)]
        .join(" ")
        .toLowerCase();
      if (facets.some((select) => select.value && question[select.dataset.catalogFacet] !== select.value)) return false;
      if (search && !haystack.includes(search)) return false;
      if (operationalOnly && !this._isOperational(question.id)) return false;
      return true;
    });
    if (count) count.textContent = `${visible.length} / ${this.questions.length} RQs`;
    results.innerHTML = visible
      .map((question) => {
        const operational = this._isOperational(question.id);
        const hypotheses = this._matchingHypotheses(question.id);
        const expanded = detailOpen === question.id;
        const hypothesisRows = hypotheses.length
          ? `<ul class="research-rq-hypothesis-list">${hypotheses.map((item) => `<li><strong>${escapeHtml(item.id)}</strong><span>${escapeHtml(item.label)}</span></li>`).join("")}</ul>`
          : '<span class="research-rq-empty">Keine Hypothese im Katalog verknüpft.</span>';
        return `<button type="button" class="research-rq-card ${selected === question.id ? "is-selected" : ""} ${expanded ? "is-detail-open" : ""}" data-rq-id="${escapeHtml(question.id)}" role="option" aria-selected="${selected === question.id}" aria-expanded="${expanded}" aria-controls="workflow-research-detail">
          <span class="research-rq-head">
            <span class="research-rq-identity"><strong>${escapeHtml(question.id)}</strong><small>${escapeHtml(question.status || "status unbekannt")}</small></span>
            <span class="research-rq-badge ${operational ? "operational" : "exploratory"}">${operational ? "OPERATIONAL" : "EXPLORATORY"}</span>
          </span>
          <span class="research-rq-question">${escapeHtml(question.label)}</span>
          <span class="research-rq-facts">
            <span><small>Domain</small><strong>${escapeHtml(question.domain || "—")}</strong></span>
            <span><small>Evidenz</small><strong>${escapeHtml(question.evidence_status || "none")}</strong></span>
            <span><small>Fortschritt</small><strong>${escapeHtml(question.experiment_progress || "not_run")}</strong></span>
            <span><small>Ausführung</small><strong>${escapeHtml(question.execution_status || (operational ? "Research Contract" : "exploratory"))}</strong></span>
          </span>
          <span class="research-rq-hypothesis-block"><small>Hypothesen</small>${hypothesisRows}</span>
          <span class="research-rq-foot"><span>${renderRunStatus(question.experiment_counts)}</span><strong>Details öffnen →</strong></span>
        </button>`;
      })
      .join("");
    results.querySelectorAll("[data-rq-id]").forEach((button) => {
      button.addEventListener("click", () => this._openResearchQuestionDetail(button.dataset.rqId));
    });
  }

  _researchQuestionProtocols(questionId) {
    return this.protocols.filter((item) => item.research_question === questionId);
  }

  _detailValue(value) {
    if (value == null || value === "") return "—";
    if (Array.isArray(value)) return value.length ? value.join(", ") : "—";
    if (typeof value === "object") return JSON.stringify(value);
    return String(value);
  }

  async _openResearchQuestionDetail(questionId) {
    const question = this.questions.find((item) => item.id === questionId);
    const detail = byId("workflow-research-detail");
    const content = byId("workflow-research-detail-content");
    const title = byId("workflow-research-detail-title");
    const useButton = byId("workflow-research-detail-use");
    const note = byId("workflow-research-detail-note");
    if (!question || !detail || !content) return;

    this.researchDetailQuestionId = questionId;
    const hypotheses = this._matchingHypotheses(questionId);
    const protocols = this._researchQuestionProtocols(questionId);
    const detailFields = [
      ["Domain", question.domain],
      ["Registry-Status", question.status],
      ["Operational", question.operational === true ? "ja" : "nein"],
      ["Workflow auswählbar", question.workflow_selectable === false ? "nein" : "ja"],
      ["Ausführungsstatus", question.execution_status],
      ["Evidenzstatus", question.evidence_status],
      ["Evidenz-IDs", question.evidence_ids],
      ["Versuchsfortschritt", question.experiment_progress],
      ["Manifest-Scan", question.manifest_scan_complete === false ? "unvollständig" : "vollständig"],
      ["Bewusstseinsinferenz", question.consciousness_inference],
    ];
    const protocolMarkup = protocols.length
      ? protocols.map((protocol) => `<article class="research-rq-protocol">
          <div><strong>${escapeHtml(protocol.id)}</strong><span>${escapeHtml(protocol.label || "")}</span></div>
          <dl>
            <div><dt>Preregistration</dt><dd>${escapeHtml(this._detailValue(protocol.preregistration))}</dd></div>
            <div><dt>Hypothese</dt><dd>${escapeHtml(this._detailValue(protocol.hypothesis))}</dd></div>
            <div><dt>Seeds</dt><dd>${escapeHtml(this._detailValue(protocol.default_seed_expression || protocol.minimum_independent_seeds))}</dd></div>
            <div><dt>Ticks</dt><dd>${escapeHtml(this._detailValue(protocol.default_ticks))}</dd></div>
          </dl>
        </article>`).join("")
      : '<p class="research-rq-empty">Kein eigener eingefrorener Research Contract verknüpft; eine explorative Übergabe bleibt an die bestehenden Workflow-Guards gebunden.</p>';
    const rawContext = { question, hypotheses, protocols };

    if (title) title.textContent = `${question.id} · ${question.label}`;
    content.innerHTML = `
      <section class="research-rq-detail-section">
        <span class="workspace-kicker">FORSCHUNGSFRAGE</span>
        <p class="research-rq-detail-question">${escapeHtml(question.label)}</p>
      </section>
      <dl class="research-rq-detail-grid">
        ${detailFields.map(([label, value]) => `<div><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(this._detailValue(value))}</dd></div>`).join("")}
      </dl>
      <section class="research-rq-detail-section">
        <h5>Hypothesen</h5>
        ${hypotheses.length ? `<div class="research-rq-detail-hypotheses">${hypotheses.map((item) => `<article><strong>${escapeHtml(item.id)}</strong><p>${escapeHtml(item.label)}</p></article>`).join("")}</div>` : '<p class="research-rq-empty">Keine Hypothese verknüpft.</p>'}
      </section>
      <section class="research-rq-detail-section">
        <h5>Research Contracts / Protokolle</h5>
        <div class="research-rq-protocols">${protocolMarkup}</div>
      </section>
      <section class="research-rq-detail-section">
        <div class="research-rq-experiment-head"><h5>Gespeicherte Experimente zu dieser Forschungsfrage</h5><span>${renderRunStatus(question.experiment_counts)}</span></div>
        <div id="workflow-rq-experiment-list" class="research-rq-experiment-list"><p class="research-rq-empty">Experimente werden geladen …</p></div>
      </section>
      <details class="research-rq-raw">
        <summary>Vollständige Katalogdaten anzeigen</summary>
        <pre>${escapeHtml(JSON.stringify(rawContext, null, 2))}</pre>
      </details>`;

    const blocked = question.workflow_selectable === false;
    if (useButton) useButton.disabled = blocked;
    if (note) note.textContent = blocked
      ? "Diese Forschungsfrage ist durch den Registry-/Governance-Vertrag für die Ausführung gesperrt."
      : "Übernimmt Forschungsfrage, Hypothese und den passenden Workflow. Es wird noch kein Lauf gestartet.";
    detail.hidden = false;
    document.querySelectorAll("[data-rq-id]").forEach((button) => {
      const expanded = button.dataset.rqId === questionId;
      button.classList.toggle("is-detail-open", expanded);
      button.setAttribute("aria-expanded", String(expanded));
    });
    await this._loadResearchQuestionExperiments(questionId);
    detail.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  async _loadResearchQuestionExperiments(questionId) {
    const root = byId("workflow-rq-experiment-list");
    if (!root) return;
    const read = async (url) => {
      const response = await fetch(url, { headers: { Accept: "application/json", "Cache-Control": "no-store" } });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    };
    try {
      const [activePayload, archivedPayload] = await Promise.all([
        read("/api/research/experiments"),
        read("/api/research/experiments/archive"),
      ]);
      const active = Array.isArray(activePayload.experiments) ? activePayload.experiments.map((item) => ({ ...item, _archive_state: "aktiv" })) : [];
      const archived = Array.isArray(archivedPayload.experiments) ? archivedPayload.experiments.filter((item) => item.archive_type !== "series").map((item) => ({ ...item, _archive_state: "archiviert" })) : [];
      const matches = [...active, ...archived].filter((item) => {
        const manifest = item.manifest && typeof item.manifest === "object" ? item.manifest : {};
        const questions = Array.isArray(manifest.research_questions)
          ? manifest.research_questions
          : [manifest.research_question].filter(Boolean);
        return questions.includes(questionId);
      });
      if (!matches.length) {
        root.innerHTML = '<p class="research-rq-empty">Keine gespeicherten Einzelexperimente für diese Forschungsfrage gefunden.</p>';
        return;
      }
      root.innerHTML = matches.map((item) => {
        const manifest = item.manifest && typeof item.manifest === "object" ? item.manifest : {};
        const experimentId = item.experiment_id || item.id || "Experiment";
        const hypotheses = Array.isArray(manifest.hypotheses) ? manifest.hypotheses : [manifest.hypothesis].filter(Boolean);
        return `<article class="research-rq-experiment">
          <div class="research-rq-experiment-summary">
            <div><strong>${escapeHtml(experimentId)}</strong><small>${escapeHtml(item._archive_state)}</small></div>
            <span>${escapeHtml(manifest.experiment_status || item.status || "unknown")}</span>
          </div>
          <dl>
            <div><dt>Hypothese</dt><dd>${escapeHtml(this._detailValue(hypotheses))}</dd></div>
            <div><dt>Protokoll</dt><dd>${escapeHtml(this._detailValue(manifest.protocol || manifest.protocol_id))}</dd></div>
            <div><dt>Seeds</dt><dd>${escapeHtml(this._detailValue(manifest.seeds))}</dd></div>
            <div><dt>Ticks</dt><dd>${escapeHtml(this._detailValue(manifest.ticks || manifest.requested_ticks))}</dd></div>
          </dl>
          <details><summary>Vollständige Experimentdaten</summary><pre>${escapeHtml(JSON.stringify(item, null, 2))}</pre></details>
        </article>`;
      }).join("");
    } catch (error) {
      root.innerHTML = `<p class="research-rq-empty">Experimentdaten konnten nicht geladen werden: ${escapeHtml(error.message || error)}</p>`;
    }
  }

  _closeResearchQuestionDetail() {
    this.researchDetailQuestionId = "";
    const detail = byId("workflow-research-detail");
    if (detail) detail.hidden = true;
    document.querySelectorAll("[data-rq-id]").forEach((button) => {
      button.classList.remove("is-detail-open");
      button.setAttribute("aria-expanded", "false");
    });
  }

  _prepareResearchQuestionForExecution(questionId) {
    const question = this.questions.find((item) => item.id === questionId);
    const note = byId("workflow-research-detail-note");
    if (!question) return;
    if (question.workflow_selectable === false) {
      if (note) note.textContent = "Übergabe blockiert: Diese Forschungsfrage ist im Registry-/Governance-Vertrag nicht ausführbar.";
      return;
    }
    this._selectResearchQuestion(questionId);
    const hypotheses = this._matchingHypotheses(questionId);
    if (this.elements.hypothesis && !this.elements.hypothesis.value && hypotheses[0]) {
      this.elements.hypothesis.value = hypotheses[0].id;
    }
    if (this.elements.title && !this.elements.title.value) this.elements.title.value = question.label || question.id;
    this._renderContract();
    if (note) note.textContent = "In den kontrollierten Ausführungs-Workflow übernommen. Der Lauf wurde nicht automatisch gestartet.";
    if (window.MHRNExperimentLab?.selectStage) {
      window.MHRNExperimentLab.selectStage("run", { scroll: true });
      window.setTimeout(() => this.elements.run?.focus(), 0);
    }
  }

  _selectResearchQuestion(questionId) {
    if (!questionId || !this.elements.question) return;
    this.elements.question.value = questionId;
    this._renderHypotheses();
    this._alignProtocolWithQuestion();
    if (!this._isOperational(questionId) && this.elements.protocol) {
      this.elements.protocol.value = "runtime_ticks_v1";
      this._applyProtocol();
    }
    this._renderContract();
    this._renderResearchCatalog();
  }

  _syncProjectionDimensions(value) {
    const marker = `MSBA projection_dimensions=${value}`;
    const notes = this.elements.notes;
    if (notes) {
      const lines = String(notes.value || "")
        .split("\n")
        .filter((line) => !line.startsWith("MSBA projection_dimensions="));
      lines.push(marker);
      notes.value = lines.filter(Boolean).join("\n");
    }
  }

  _applyProtocol() {
    super._applyProtocol();
    const operational = this._protocolContract(this.elements.protocol?.value);
    if (!operational) return;

    const profiles = operational.condition_profiles || {
      standard: (operational.conditions || [])
        .map((item) => `${item.id || item.condition_id || item}${item.role ? ` (${item.role})` : ""}`)
        .join("; "),
    };
    const defaultSeeds = operational.default_seed_expression;
    this.activePreset = {
      ...(this.activePreset || {}),
      question: operational.research_question,
      hypothesis: operational.hypothesis,
      title: operational.label || operational.id,
      ticks: String(operational.default_ticks ?? this.elements.ticks?.value ?? "100"),
      seeds: defaultSeeds || this.activePreset?.seeds || "101",
      conditions: profiles.standard || "",
      profiles,
    };

    if (this.elements.seeds && this.activePreset.seeds) this.elements.seeds.value = this.activePreset.seeds;
    if (this.elements.ticks && this.activePreset.ticks) this.elements.ticks.value = this.activePreset.ticks;
    this._configureConditionProfiles(this.activePreset);
    this._applyConditionProfile(this.activePreset);
    this._renderContract();
    this._renderResearchCatalog();
  }

  _renderContract() {
    super._renderContract();
    if (this.activeContract) return;
    const content = byId("workflow-contract-content");
    if (!content || !this.activePreset) return;
    content.innerHTML = `
      <details class="legacy-diagnostic-details" open>
        <summary><span>Exploratory / diagnostic protocol</span><small>keine automatische Evidenz-Promotion</small></summary>
        <div class="legacy-diagnostic-body">
          <p>${escapeHtml(this.activePreset.conditions || "")}</p>
          <p>Dieser Lauf kann die ausgewählte RQ/H protokolliert explorieren. Er besitzt aber keinen passenden eingefrorenen Research Contract und darf deshalb nicht als bestätigende Evidenz interpretiert werden.</p>
        </div>
      </details>`;
  }
}
