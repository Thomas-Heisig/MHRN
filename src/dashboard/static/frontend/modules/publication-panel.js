/**
 * MHRN Dashboard — Publication Panel
 *
 * Loads and displays the current scientific publication (Forschungsbericht)
 * from the backend API and renders it as formatted markdown inside the
 * Overview → Publikation sub-tab.
 */

"use strict";

export async function initPublicationPanel() {
  const container = document.getElementById("publication-panel");
  if (!container || container.dataset.initialised === "true") return;
  container.dataset.initialised = "true";

  await loadPublication(container);

  // Re-load when the sub-tab becomes visible (user clicks the tab)
  const subtab = document.querySelector('.overview-subtab[data-subtab="publication"]');
  if (subtab) {
    subtab.addEventListener("click", () => {
      // Only reload if content is missing (e.g. after error)
      if (!container.querySelector(".publication-content")) {
        loadPublication(container);
      }
    });
  }
}

async function loadPublication(container) {
  container.innerHTML = '<div class="publication-loading">Lade aktuelle Publikation …</div>';

  try {
    const resp = await fetch("/api/publication/current");
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ error: resp.statusText }));
      container.innerHTML = `<div class="publication-error">Fehler beim Laden: ${err.error || resp.statusText}</div>`;
      return;
    }

    const data = await resp.json();

    if (data.error) {
      container.innerHTML = `<div class="publication-error">${data.error}</div>`;
      return;
    }

    renderPublication(container, data);
  } catch (err) {
    container.innerHTML = `<div class="publication-error">Netzwerkfehler: ${err.message}</div>`;
  }
}

function renderPublication(container, data) {
  const { publication, title, edition, readme_path, sha256, content, forschungsbericht, exports: exportsList } = data;

  // Build header
  let html = `
    <div class="publication-header">
      <div class="publication-meta">
        <span class="workspace-kicker">AKTUELLE PUBLIKATION</span>
        <h2>${escapeHtml(title)}</h2>
        <p class="publication-edition">Edition ${escapeHtml(edition)} · ${escapeHtml(publication)}</p>
      </div>
      <div class="publication-actions">
        <span class="publication-digest" title="SHA-256 des README">${sha256.slice(0, 16)}…</span>
        <button type="button" class="btn-secondary" id="pub-open-fv" title="Im File Viewer öffnen">📂 Im File Viewer</button>
      </div>
    </div>
    <div class="publication-body">`;

  // Render markdown content — pass readme_path so relative links resolve correctly
  html += renderSafeMarkdown(content, readme_path);

  html += `</div>`;

  // Footer with exports and links
  html += `<div class="publication-footer">`;

  if (forschungsbericht) {
    html += `<div class="publication-related">
      <strong>Forschungsbericht</strong>
      <span>SHA-256: ${forschungsbericht.sha256.slice(0, 16)}…</span>
      <button type="button" class="btn-secondary btn-sm" data-pub-path="${escapeHtml(forschungsbericht.path)}">Im File Viewer öffnen</button>
    </div>`;
  }

  if (exportsList && exportsList.length > 0) {
    html += `<div class="publication-exports">
      <strong>Exportformate</strong>
      <div class="publication-export-list">`;
    for (const exp of exportsList) {
      html += `<a href="/api/research-files/${exp.path}" class="btn-secondary btn-sm" download target="_blank">📥 ${exp.format.toUpperCase()} (${formatBytes(exp.size_bytes)})</a>`;
    }
    html += `</div></div>`;
  }

  html += `<div class="publication-source">
    <strong>Quelle</strong>
    <code>${escapeHtml(readme_path)}</code>
  </div>`;

  html += `</div>`;

  container.innerHTML = html;

  // Wire up "Im File Viewer" buttons
  const openFvBtn = document.getElementById("pub-open-fv");
  if (openFvBtn) {
    openFvBtn.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("brain5d:open-file", {
        detail: { source: "research", path: readme_path }
      }));
    });
  }

  // Wire up internal publication links (section-*.md, MANUSCRIPT.md, etc.)
  container.querySelectorAll(".pub-internal-link").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const path = link.dataset.pubLink;
      if (path) {
        window.dispatchEvent(new CustomEvent("brain5d:open-file", {
          detail: { source: "research", path }
        }));
      }
    });
  });

  container.querySelectorAll("[data-pub-path]").forEach((btn) => {
    btn.addEventListener("click", () => {
      window.dispatchEvent(new CustomEvent("brain5d:open-file", {
        detail: { source: "research", path: btn.dataset.pubPath }
      }));
    });
  });
}

/**
 * Render a safe subset of Markdown to HTML.
 * Supports: headings, bold, italic, inline code, code fences, links, lists, blockquotes, paragraphs.
 * @param {string} md - The markdown content
 * @param {string} [basePath] - The directory path of the source file, for resolving relative links
 */
function renderSafeMarkdown(md, basePath) {
  if (!md) return "";
  // Store basePath for link resolution (used in the link regex below)
  // Normalize backslashes to forward slashes for cross-platform compatibility
  const normalizedBase = basePath ? basePath.replace(/\\/g, '/') : '';
  const linkBasePath = normalizedBase ? normalizedBase.replace(/\/[^/]+$/, '') : '';

  let html = md;

  // Escape HTML entities first
  html = escapeHtml(html);

  // Code fences (``` ... ```) — must come before other transformations
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
    const langAttr = lang ? ` class="language-${escapeHtml(lang)}"` : "";
    return `<pre><code${langAttr}>${code.trim()}</code></pre>`;
  });

  // Inline code
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");

  // Headings (h1-h3)
  html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>");
  html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>");
  html = html.replace(/^# (.+)$/gm, "<h1>$1</h1>");

  // Blockquotes
  html = html.replace(/^&gt; (.+)$/gm, "<blockquote>$1</blockquote>");

  // Bold and italic
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>");
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, text, url) => {
    const trimmed = url.trim();
    if (trimmed.startsWith("http")) {
      return `<a href="${escapeHtml(trimmed)}" target="_blank" rel="noopener">${escapeHtml(text)}</a>`;
    }
    // Relative link — open via File Viewer or download
    const isDownload = /\.(pdf|docx)$/i.test(trimmed);
    if (isDownload) {
      const fullPath = linkBasePath ? `${linkBasePath}/${trimmed}` : trimmed;
      return `<a href="/api/research-files/${fullPath}" download target="_blank">${escapeHtml(text)}</a>`;
    }
    // Relative link to .md / .json — open in File Viewer
    const dataPath = linkBasePath ? `${linkBasePath}/${trimmed}` : trimmed;
    return `<a href="#" class="pub-internal-link" data-pub-link="${escapeHtml(dataPath)}">${escapeHtml(text)}</a>`;
  });

  // Unordered lists
  html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
  html = html.replace(/(<li>.*<\/li>\n?)+/g, "<ul>$&</ul>");

  // Horizontal rules
  html = html.replace(/^---$/gm, "<hr>");

  // Paragraphs: wrap remaining lines
  const lines = html.split("\n");
  html = lines.map((line) => {
    const trimmed = line.trim();
    if (!trimmed) return "";
    if (trimmed.startsWith("<h") || trimmed.startsWith("<pre") || trimmed.startsWith("<ul") || trimmed.startsWith("<li") || trimmed.startsWith("<blockquote") || trimmed.startsWith("<hr") || trimmed.startsWith("</")) {
      return trimmed;
    }
    return `<p>${trimmed}</p>`;
  }).join("\n");

  return html;
}

function escapeHtml(str) {
  if (typeof str !== "string") return String(str || "");
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function formatBytes(bytes) {
  if (bytes == null) return "—";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}
