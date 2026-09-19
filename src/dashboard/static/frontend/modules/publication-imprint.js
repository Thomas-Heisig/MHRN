"use strict";

const ENDPOINT = "/api/publication/imprint";

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderValue(value, fallback = "Nicht öffentlich hinterlegt") {
  return value ? escapeHtml(value) : `<span class="pub-imprint-missing">${escapeHtml(fallback)}</span>`;
}

function externalLink(label, url) {
  if (!url) return "";
  return `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(label)}</a>`;
}

function renderList(items) {
  return `<ul>${(items || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function renderImprint(data) {
  const provider = data.provider || {};
  const editorial = data.editorial_responsibility || {};
  const project = data.project || {};
  const privacy = data.privacy || {};
  const rights = data.content_and_licenses || {};
  const missing = data.required_before_public_internet || [];
  const internetReady = Boolean(data.public_internet_ready);
  const releaseReady = Boolean(data.public_release_ready);
  const statusClass = internetReady ? "is-ready" : releaseReady ? "is-partial" : "is-incomplete";
  const statusLabel = internetReady
    ? "öffentliche Dashboard-Bereitstellung vollständig"
    : releaseReady
      ? "öffentliche Projektfreigabe möglich · Hosting-Datenschutz offen"
      : "vor öffentlicher Bereitstellung vervollständigen";

  return `
    <section class="pub-imprint-page" aria-labelledby="pub-imprint-title">
      <header class="pub-imprint-hero">
        <div>
          <span class="workspace-kicker">PROJEKTIDENTITÄT · RECHTLICHES</span>
          <h1 id="pub-imprint-title">Impressum &amp; Rechtliche Hinweise</h1>
          <p>Transparente Anbieter-, Autoren-, Projekt-, Lizenz- und Datenschutzinformationen für MHRN und die Publikationsoberfläche.</p>
        </div>
        <span class="pub-imprint-status ${statusClass}">${statusLabel}</span>
      </header>

      ${!internetReady ? `
        <section class="pub-imprint-warning" role="status">
          <strong>Anbieter- und Verantwortlichkeitsangaben sind vollständig hinterlegt.</strong>
          <p>Für GitHub-/Zenodo-Veröffentlichungen sind die öffentlichen Identitäts- und Kontaktangaben vorhanden. Vor einer eigenständig öffentlich gehosteten Dashboard-Instanz müssen nur noch die tatsächlichen Hosting-, Proxy- und Logging-Datenschutzhinweise ergänzt werden.</p>
        </section>` : ""}

      <div class="pub-imprint-grid">
        <article>
          <h2>Diensteanbieter / Projektverantwortung</h2>
          <dl>
            <div><dt>Name</dt><dd>${renderValue(provider.name)}</dd></div>
            <div><dt>Funktion</dt><dd>${renderValue(provider.role)}</dd></div>
            <div><dt>Rechtsform</dt><dd>${renderValue(provider.legal_entity, "Privatperson")}</dd></div>
            <div><dt>Anschrift</dt><dd>${renderValue(provider.postal_address, "Pflichtfeld vor öffentlicher Bereitstellung")}</dd></div>
            <div><dt>E-Mail</dt><dd>${renderValue(provider.email, "Pflichtfeld vor öffentlicher Bereitstellung")}</dd></div>
            <div><dt>Telefon</dt><dd>${renderValue(provider.phone, "nur falls als Kontaktweg angegeben")}</dd></div>
            <div><dt>Register</dt><dd>${renderValue(provider.register, "nicht angegeben / ggf. nicht einschlägig")}</dd></div>
            <div><dt>USt-IdNr.</dt><dd>${renderValue(provider.vat_id, "nicht angegeben / ggf. nicht einschlägig")}</dd></div>
          </dl>
        </article>

        <article>
          <h2>Redaktionell verantwortlich</h2>
          <p>Sofern für einzelne publizistische Inhalte § 18 Abs. 2 MStV anwendbar ist:</p>
          <dl>
            <div><dt>Name</dt><dd>${renderValue(editorial.name)}</dd></div>
            <div><dt>Anschrift</dt><dd>${renderValue(editorial.postal_address, "vor öffentlicher Bereitstellung ergänzen, falls anwendbar")}</dd></div>
          </dl>
        </article>

        <article>
          <h2>Projekt &amp; wissenschaftliche Identität</h2>
          <dl>
            <div><dt>Projekt</dt><dd>${escapeHtml(project.short_name || "MHRN")} — ${escapeHtml(project.title || "")}</dd></div>
            <div><dt>Autor</dt><dd>Thomas Heisig</dd></div>
            <div><dt>ORCID</dt><dd>${externalLink("0009-0002-9589-1872", project.orcid)}</dd></div>
            <div><dt>GitHub</dt><dd>${externalLink("Thomas-Heisig/MHRN", project.repository)}</dd></div>
            <div><dt>OSF</dt><dd>${externalLink("OSF-Projekt", project.osf)}</dd></div>
            <div><dt>Publikation</dt><dd>${escapeHtml(project.publication_status || "")}</dd></div>
          </dl>
        </article>

        <article>
          <h2>Lizenzen &amp; Rechte</h2>
          <p><strong>Software:</strong> ${escapeHtml(rights.software || project.software_license || "MIT")}</p>
          <p><strong>Wissenschaftliche Inhalte:</strong> ${escapeHtml(rights.scientific_content || "")}</p>
          <p><strong>Fremdmaterial:</strong> ${escapeHtml(rights.third_party_material || "")}</p>
        </article>

        <article>
          <h2>Datenschutz &amp; lokale Speicherung</h2>
          <p>${escapeHtml(privacy.principle || "Datenschutz und Datensparsamkeit sind Projektprinzipien.")}</p>
          <p>Die Dashboard-Oberfläche verwendet Browser-LocalStorage für lokale Bedien- und Darstellungszustände. Drittanbieter-Analytics sind in der hinterlegten Projektkonfiguration nicht als aktiviert ausgewiesen.</p>
          ${renderList(privacy.browser_local_storage_purposes || [])}
          <p><strong>Server-Logging:</strong> ${escapeHtml(privacy.server_logging || "abhängig vom tatsächlichen Deployment")}</p>
          <p><strong>Externe Dienste:</strong> ${escapeHtml(privacy.external_services || "")}</p>
          <p class="pub-imprint-note">${escapeHtml(privacy.public_deployment_note || "")}</p>
        </article>

        <article>
          <h2>Kontakt &amp; Sicherheitsmeldungen</h2>
          <ul class="pub-imprint-links">
            ${(data.contact_channels || []).map((item) => `<li>${externalLink(item.label, item.url)}</li>`).join("")}
          </ul>
          <p>GitHub-Issues sind ein öffentlicher Projektkanal und ersetzen keine gesetzlich erforderliche Kontakt-E-Mail im Impressum.</p>
        </article>

        <article>
          <h2>Wissenschaftliche Aussagegrenze</h2>
          <p>${escapeHtml(project.scientific_boundary || "")}</p>
          <p>DOI, Indexierung, Downloads, Zitierungen und technische Reproduzierbarkeit sind nicht automatisch Human Review, akzeptierte EVID oder unabhängige Replikation.</p>
        </article>

        <article>
          <h2>Rechtsgrundlagen / Orientierung</h2>
          <ul class="pub-imprint-links">
            ${(data.legal_references || []).map((item) => `<li>${externalLink(item.label, item.url)}</li>`).join("")}
          </ul>
          <p class="pub-imprint-note">Diese Projektseite dokumentiert die hinterlegten Angaben und ersetzt keine individuelle Rechtsberatung.</p>
        </article>
      </div>

      ${missing.length ? `
        <section class="pub-imprint-checklist">
          <h2>Vor öffentlicher Internetbereitstellung noch zu ergänzen</h2>
          ${renderList(missing)}
        </section>` : ""}
    </section>
  `;
}

export function initPublicationImprint() {
  const panel = document.getElementById("publication-imprint-panel");
  if (!panel || panel.dataset.imprintInitialised === "true") return;
  panel.dataset.imprintInitialised = "true";

  const load = async () => {
    panel.innerHTML = '<div class="publication-loading">Lade Impressum &amp; Rechtliches …</div>';
    try {
      const response = await fetch(ENDPOINT, { headers: { Accept: "application/json" }, cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      panel.innerHTML = renderImprint(data);
    } catch (error) {
      panel.innerHTML = `<section class="pub-imprint-warning"><strong>Impressum konnte nicht geladen werden.</strong><p>${escapeHtml(error.message)}</p></section>`;
    }
  };

  void load();
}
