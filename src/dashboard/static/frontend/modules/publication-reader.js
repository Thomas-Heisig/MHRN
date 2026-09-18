/**
 * MHRN Dashboard — Publication Reader
 *
 * Purpose-built reader for the canonical scientific publication. Markdown
 * chapters stay inside the publication workspace with reader history; other
 * repository files use the canonical File Viewer; external links stay normal
 * browser links.
 */

"use strict";

import { createSpeechControls } from "../../speech-reader.js";

const CURRENT_PUBLICATION_ENDPOINT = "/api/publication/current";
const REPOSITORY_BLOB_ROOT = "https://github.com/Thomas-Heisig/MHRN/blob/main/";
const READER_EXTENSIONS = /\.(?:md|markdown|txt)$/i;
const IMAGE_EXTENSIONS = /\.(?:png|jpe?g|gif|webp|svg|bmp)$/i;
const readerStates = new WeakMap();

export async function initPublicationPanel() {
  const container = document.getElementById("publication-panel");
  if (!container || container.dataset.publicationReaderInitialised === "true") return;

  container.dataset.publicationReaderInitialised = "true";
  // Inject reader styles immediately so there's no flash of unstyled content
  ensureReaderStyles();

  const state = {
    rootData: null,
    views: [],
    index: -1,
    loading: false,
    searchMatches: [],
    searchIndex: -1,
  };
  readerStates.set(container, state);

  container.addEventListener("click", (event) => handleReaderClick(container, event));
  container.addEventListener("input", (event) => handleReaderInput(container, event));
  container.addEventListener("keydown", (event) => handleReaderKeydown(container, event));

  const activate = () => {
    const areaActive = document.body?.dataset.currentArea === "publication";
    const tab = document.getElementById("tab-publication");
    const tabActive = Boolean(tab && tab.classList.contains("active") && !tab.hidden);
    if ((areaActive || tabActive) && !state.rootData && !state.loading) loadCurrentPublication(container);
  };

  document.addEventListener("click", (event) => {
    if (event.target.closest('[data-mhrn-area="publication"]')) queueMicrotask(activate);
  });

  const bodyObserver = new MutationObserver(activate);
  bodyObserver.observe(document.body, {
    attributes: true,
    attributeFilter: ["data-current-area", "data-current-route", "data-current-tab"],
  });

  const tab = document.getElementById("tab-publication");
  if (tab) {
    const tabObserver = new MutationObserver(activate);
    tabObserver.observe(tab, { attributes: true, attributeFilter: ["class", "hidden", "style"] });
  }

  activate();
}

async function loadCurrentPublication(container, { force = false } = {}) {
  const state = readerStates.get(container);
  if (!state || state.loading || (state.rootData && !force)) return;
  state.loading = true;
  renderLoading(container, "Publikation wird geladen …");

  try {
    const response = await fetch(CURRENT_PUBLICATION_ENDPOINT, {
      headers: { Accept: "application/json" },
      cache: "no-store",
    });
    if (!response.ok) {
      const detail = await response.json().catch(() => ({}));
      throw new Error(detail.error || `HTTP ${response.status}`);
    }
    const data = await response.json();
    if (data.error) throw new Error(data.error);
    if (typeof data.content !== "string") throw new Error("Publikationsinhalt fehlt in der API-Antwort.");

    const rootRef = sourceReference(data.entrypoint_path || data.readme_path || "publications/CURRENT.md", "research");
    const rootView = {
      source: rootRef.source,
      path: rootRef.path,
      title: data.document_title || firstHeading(data.content) || data.title || "Wissenschaftliche Publikation",
      content: data.content,
      kind: "markdown",
      root: true,
    };

    state.rootData = data;
    state.views = [rootView];
    state.index = 0;
    state.searchMatches = [];
    state.searchIndex = -1;
    renderReader(container);
  } catch (error) {
    renderError(container, error);
  } finally {
    state.loading = false;
  }
}

function renderLoading(container, message) {
  container.innerHTML = `
    <div class="pub-reader-state" role="status" aria-live="polite">
      <span class="pub-reader-spinner" aria-hidden="true"></span>
      <strong>${escapeHtml(message)}</strong>
      <span>Reader, Verweise und Dokumentstruktur werden vorbereitet.</span>
    </div>`;
}

function renderError(container, error) {
  container.innerHTML = `
    <div class="pub-reader-state pub-reader-state-error" role="alert">
      <strong>Publikation konnte nicht geladen werden</strong>
      <span>${escapeHtml(error?.message || String(error))}</span>
      <button type="button" class="pub-reader-button" data-pub-action="retry">Erneut laden</button>
    </div>`;
}

function renderReader(container) {
  const state = readerStates.get(container);
  if (!state?.rootData || state.index < 0) return;

  const data = state.rootData;
  const view = state.views[state.index];
  const rendered = renderPublicationMarkdown(view.content, view);
  const words = countWords(view.content);
  const readMinutes = Math.max(1, Math.ceil(words / 220));
  const isRoot = state.index === 0;
  const sourceLabel = view.source === "docs" ? "docs" : "research";
  const safeDigest = typeof data.sha256 === "string" ? data.sha256 : "";

  container.innerHTML = `
    <section class="publication-reader" id="publication-reader" aria-label="Publication Reader">
      <div class="pub-reader-progress" aria-hidden="true"><span id="pub-reading-progress"></span></div>
      <header class="pub-reader-hero">
        <div class="pub-reader-identity">
          <span class="pub-reader-eyebrow">WISSENSCHAFTLICHE HAUPTARBEIT</span>
          <h1>${escapeHtml(view.root ? (data.document_title || view.title) : view.title)}</h1>
          ${view.root && data.title && data.title !== data.document_title ? `<p class="pub-reader-catalog-title">${escapeHtml(data.title)}</p>` : ""}
          <div class="pub-reader-badges" aria-label="Publikationsmetadaten">
            ${data.edition ? `<span>Edition ${escapeHtml(data.edition)}</span>` : ""}
            ${data.publication ? `<span>${escapeHtml(data.publication)}</span>` : ""}
            ${data.author ? `<span>${escapeHtml(data.author)}</span>` : ""}
            ${data.date ? `<span>${escapeHtml(data.date)}</span>` : ""}
            <span>${words.toLocaleString("de-DE")} Wörter</span>
            <span>ca. ${readMinutes} Min.</span>
          </div>
        </div>
        <div class="pub-reader-primary-actions">
          <button type="button" class="pub-reader-button pub-reader-button-primary" data-pub-action="open-file">Im File Viewer</button>
          <button type="button" class="pub-reader-button" data-pub-action="print">Drucken</button>
          <button type="button" class="pub-reader-button" data-pub-action="refresh">Aktualisieren</button>
        </div>
      </header>

      <div class="pub-reader-toolbar" aria-label="Lesewerkzeuge">
        <div class="pub-reader-history" aria-label="Dokumentnavigation">
          <button type="button" class="pub-reader-icon-button" data-pub-action="back" ${state.index <= 0 ? "disabled" : ""} aria-label="Zurück">←</button>
          <button type="button" class="pub-reader-icon-button" data-pub-action="home" ${isRoot ? "disabled" : ""} aria-label="Zum Publikationsindex">⌂</button>
          <button type="button" class="pub-reader-icon-button" data-pub-action="forward" ${state.index >= state.views.length - 1 ? "disabled" : ""} aria-label="Vorwärts">→</button>
        </div>
        <div class="pub-reader-speech" id="pub-reader-speech-mount"></div>
        <div class="pub-reader-location" title="${escapeHtml(`${sourceLabel}/${view.path}`)}">
          <span>${escapeHtml(sourceLabel)}</span><strong>/</strong><code>${escapeHtml(view.path)}</code>
        </div>
        <label class="pub-reader-search">
          <span class="sr-only">Im Dokument suchen</span>
          <input type="search" id="pub-reader-search" placeholder="Im Dokument suchen …" autocomplete="off" />
          <output id="pub-search-count" aria-live="polite"></output>
          <button type="button" data-pub-action="search-prev" aria-label="Vorheriger Treffer">↑</button>
          <button type="button" data-pub-action="search-next" aria-label="Nächster Treffer">↓</button>
        </label>
      </div>

      <div class="pub-reader-layout">
        <aside class="pub-reader-toc" aria-label="Inhaltsverzeichnis">
          <div class="pub-reader-toc-head"><strong>Inhalt</strong><span>${rendered.headings.length} Abschnitte</span></div>
          ${renderToc(rendered.headings)}
          ${renderPublicationLibrary(data, view)}
          <div class="pub-reader-toc-meta">
            <button type="button" data-pub-action="copy-path">Pfad kopieren</button>
            ${safeDigest ? `<button type="button" data-pub-action="copy-digest">SHA-256 kopieren</button>` : ""}
          </div>
        </aside>

        <main class="pub-reader-document">
          ${!isRoot ? `
            <div class="pub-reader-document-banner">
              <div><span>VERKNÜPFTES DOKUMENT</span><strong>${escapeHtml(view.title)}</strong></div>
              <button type="button" data-pub-action="home">Zum Publikationsindex</button>
            </div>` : ""}
          <article class="pub-reader-article" id="pub-reader-article" data-source="${escapeHtml(view.source)}" data-path="${escapeHtml(view.path)}">
            ${rendered.html}
          </article>
        </main>
      </div>

      ${renderReaderFooter(data, view)}
      <div class="pub-reader-toast" id="pub-reader-toast" role="status" aria-live="polite"></div>
    </section>`;

  wireHeadingObserver(container);
  wireReadingProgress(container);
  wireSpeechControls(container);
}

function renderToc(headings) {
  const visible = headings.filter((heading) => heading.level <= 3);
  if (!visible.length) return '<p class="pub-reader-toc-empty">Keine Überschriften erkannt.</p>';
  return `<nav>${visible.map((heading) => `
    <a href="#${escapeHtml(heading.id)}" data-pub-anchor="${escapeHtml(heading.slug)}" data-level="${heading.level}">
      <span>${escapeHtml(heading.text)}</span>
    </a>`).join("")}</nav>`;
}

function renderPublicationLibrary(data, view) {
  const groups = [
    ["Kapitel", Array.isArray(data.chapters) ? data.chapters : []],
    ["Anhänge & Register", Array.isArray(data.attachments) ? data.attachments : []],
    ["Editionen", Array.isArray(data.history) ? data.history : []],
  ];
  const currentKey = `${view.source}:${view.path}`;
  const sections = groups.map(([title, items]) => {
    if (!items.length) return "";
    const buttons = items.map((item) => {
      const source = item.source === "docs" ? "docs" : "research";
      const path = stripResearchPrefix(String(item.path || ""));
      const key = `${source}:${path}`;
      const readable = item.kind === "reader" || READER_EXTENSIONS.test(path);
      const attrs = readable
        ? `data-pub-reader-link="${escapeHtml(path)}" data-pub-source="${escapeHtml(source)}"`
        : `data-pub-file="${escapeHtml(path)}" data-pub-source="${escapeHtml(source)}"`;
      return `<button type="button" class="pub-reader-library-item${key === currentKey ? " active" : ""}" ${attrs}${key === currentKey ? ' aria-current="page"' : ""}><strong>${escapeHtml(String(item.label || basename(path)))}</strong><span>${escapeHtml(String(item.format || item.role || ""))}</span></button>`;
    }).join("");
    return `<section class="pub-reader-library"><div class="pub-reader-toc-head"><strong>${escapeHtml(title)}</strong><span>${items.length}</span></div><div class="pub-reader-library-list">${buttons}</div></section>`;
  }).join("");
  return sections;
}

function renderReaderFooter(data, view) {
  const exportsList = Array.isArray(data.exports) ? data.exports : [];
  const report = data.forschungsbericht;
  const source = `${view.source}/${view.path}`;
  return `
    <footer class="pub-reader-footer">
      <section>
        <span class="pub-reader-footer-label">Quelle</span>
        <code>${escapeHtml(source)}</code>
        ${data.sha256 ? `<small>SHA-256 ${escapeHtml(data.sha256)}</small>` : ""}
      </section>
      ${report?.path ? `
        <section>
          <span class="pub-reader-footer-label">Forschungsbericht</span>
          <strong>${escapeHtml(basename(report.path))}</strong>
          ${report.sha256 ? `<small>SHA-256 ${escapeHtml(report.sha256)}</small>` : ""}
          <button type="button" data-pub-source="research" data-pub-file="${escapeHtml(stripResearchPrefix(report.path))}">Im File Viewer öffnen</button>
        </section>` : ""}
      ${exportsList.length ? `
        <section>
          <span class="pub-reader-footer-label">Exporte</span>
          <div class="pub-reader-export-list">
            ${exportsList.map((item) => `<a href="/api/research-files/${encodeURI(String(item.path || ""))}" target="_blank" rel="noopener" download>${escapeHtml(String(item.format || "Datei").toUpperCase())}${item.size_bytes != null ? ` · ${formatBytes(item.size_bytes)}` : ""}</a>`).join("")}
          </div>
        </section>` : ""}
    </footer>`;
}

async function handleReaderClick(container, event) {
  const actionNode = event.target.closest("[data-pub-action]");
  if (actionNode) {
    event.preventDefault();
    await runReaderAction(container, actionNode.dataset.pubAction);
    return;
  }

  const anchor = event.target.closest("[data-pub-anchor]");
  if (anchor) {
    event.preventDefault();
    scrollToPublicationAnchor(container, anchor.dataset.pubAnchor);
    return;
  }

  const readerLink = event.target.closest("[data-pub-reader-link]");
  if (readerLink) {
    event.preventDefault();
    await openReaderDocument(container, {
      source: readerLink.dataset.pubSource,
      path: readerLink.dataset.pubReaderLink,
      anchor: readerLink.dataset.pubTargetAnchor || "",
      label: readerLink.textContent?.trim() || "",
    });
    return;
  }

  const fileLink = event.target.closest("[data-pub-file]");
  if (fileLink) {
    event.preventDefault();
    await openInFileViewer(fileLink.dataset.pubSource || "research", fileLink.dataset.pubFile);
  }
}

function handleReaderInput(container, event) {
  if (event.target.id === "pub-reader-search") updateSearch(container, event.target.value);
}

function handleReaderKeydown(container, event) {
  if (event.target.id === "pub-reader-search") {
    if (event.key === "Enter") {
      event.preventDefault();
      moveSearch(container, event.shiftKey ? -1 : 1);
    } else if (event.key === "Escape") {
      event.target.value = "";
      updateSearch(container, "");
      event.target.blur();
    }
    return;
  }
  if (event.key === "/" && !event.ctrlKey && !event.metaKey && !event.altKey) {
    event.preventDefault();
    container.querySelector("#pub-reader-search")?.focus();
  }
}

async function runReaderAction(container, action) {
  const state = readerStates.get(container);
  if (!state) return;

  if (action === "retry") return loadCurrentPublication(container, { force: true });
  if (action === "refresh") {
    state.rootData = null;
    state.views = [];
    state.index = -1;
    return loadCurrentPublication(container, { force: true });
  }
  if (action === "back" && state.index > 0) { state.index -= 1; return renderReader(container); }
  if (action === "forward" && state.index < state.views.length - 1) { state.index += 1; return renderReader(container); }
  if (action === "home" && state.index !== 0) { state.index = 0; return renderReader(container); }
  if (action === "open-file") {
    const view = state.views[state.index];
    return openInFileViewer(view.source, view.path);
  }
  if (action === "print") return window.print();
  if (action === "copy-path") {
    const view = state.views[state.index];
    await copyText(`${view.source}/${view.path}`);
    return showToast(container, "Pfad kopiert.");
  }
  if (action === "copy-digest" && state.rootData?.sha256) {
    await copyText(state.rootData.sha256);
    return showToast(container, "SHA-256 kopiert.");
  }
  if (action === "search-next") return moveSearch(container, 1);
  if (action === "search-prev") return moveSearch(container, -1);
}

async function openReaderDocument(container, ref) {
  if (!ref?.path || !["research", "docs"].includes(ref.source)) return;
  const state = readerStates.get(container);
  if (!state) return;

  const current = state.views[state.index];
  if (current?.source === ref.source && current?.path === ref.path) {
    if (ref.anchor) scrollToPublicationAnchor(container, ref.anchor);
    return;
  }

  showToast(container, `Öffne ${basename(ref.path)} …`);
  try {
    const response = await fetch(`/api/files/preview/${encodeURIComponent(ref.path)}?source=${encodeURIComponent(ref.source)}`, {
      headers: { Accept: "application/json" },
      cache: "no-store",
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const descriptor = await response.json();
    if (typeof descriptor.content !== "string") throw new Error("Dokument ist nicht als Text lesbar.");

    const view = {
      source: ref.source,
      path: ref.path,
      title: firstHeading(descriptor.content) || ref.label || basename(ref.path),
      content: descriptor.content,
      kind: descriptor.kind || "markdown",
      root: false,
    };
    state.views = state.views.slice(0, state.index + 1);
    state.views.push(view);
    state.index += 1;
    state.searchMatches = [];
    state.searchIndex = -1;
    renderReader(container);
    requestAnimationFrame(() => {
      if (ref.anchor) scrollToPublicationAnchor(container, ref.anchor);
      else container.querySelector(".pub-reader-hero")?.scrollIntoView({ block: "start" });
    });
  } catch (error) {
    showToast(container, `Inline-Reader nicht verfügbar: ${error.message}. Öffne File Viewer …`, true);
    await openInFileViewer(ref.source, ref.path);
  }
}

async function openInFileViewer(source, path) {
  if (!["research", "docs"].includes(source) || !path) return;

  const popupToggle = document.getElementById("fm-popup-toggle");
  const popupPreferred = popupToggle ? popupToggle.checked : localStorage.getItem("mhrn-fm-popup") !== "false";

  if (!popupPreferred) {
    if (typeof window.selectRoute === "function") {
      window.selectRoute("files", "browse");
      await nextFrame();
    } else {
      document.querySelector('[data-mhrn-area="files"]')?.click();
      await nextFrame();
    }
  }

  if (typeof window.openBrain5DFile === "function") {
    await window.openBrain5DFile(source, path);
    return;
  }
  document.dispatchEvent(new CustomEvent("brain5d:open-file", { detail: { source, path } }));
}

export function renderPublicationMarkdown(markdown, view) {
  const lines = String(markdown || "").replace(/\r\n?/g, "\n").split("\n");
  const html = [];
  const headings = [];
  const slugCounts = new Map();
  let paragraph = [];
  let listType = null;
  let codeFence = null;
  let codeLines = [];

  const flushParagraph = () => {
    if (!paragraph.length) return;
    html.push(`<p>${renderInline(paragraph.join(" "), view)}</p>`);
    paragraph = [];
  };
  const closeList = () => {
    if (!listType) return;
    html.push(`</${listType}>`);
    listType = null;
  };
  const closeBlocks = () => { flushParagraph(); closeList(); };

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];

    if (codeFence) {
      if (/^```\s*$/.test(line)) {
        html.push(`<pre class="pub-code"><code${codeFence ? ` data-language="${escapeHtml(codeFence)}"` : ""}>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
        codeFence = null;
        codeLines = [];
      } else codeLines.push(line);
      continue;
    }

    const fence = line.match(/^```\s*([^\s`]*)\s*$/);
    if (fence) {
      closeBlocks();
      codeFence = fence[1] || "text";
      codeLines = [];
      continue;
    }

    if (!line.trim()) { closeBlocks(); continue; }

    const detailsOpen = line.trim().match(/^<details(?:\s[^>]*)?>$/i);
    const detailsClose = /^<\/details>$/i.test(line.trim());
    const summary = line.trim().match(/^<summary>(.*?)<\/summary>$/i);
    if (detailsOpen || detailsClose || summary) {
      closeBlocks();
      if (detailsOpen) html.push("<details class=\"pub-details\">");
      else if (detailsClose) html.push("</details>");
      else html.push(`<summary>${renderInline(summary[1], view)}</summary>`);
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+?)\s*#*\s*$/);
    if (heading) {
      closeBlocks();
      const level = heading[1].length;
      const text = stripMarkdownText(heading[2]);
      const baseSlug = slugify(text) || `section-${headings.length + 1}`;
      const seen = slugCounts.get(baseSlug) || 0;
      slugCounts.set(baseSlug, seen + 1);
      const slug = seen ? `${baseSlug}-${seen + 1}` : baseSlug;
      const id = `pub-${slug}`;
      headings.push({ level, text, slug, id });
      html.push(`<h${level} id="${id}" data-pub-heading data-pub-slug="${escapeHtml(slug)}">${renderInline(heading[2], view)}<button type="button" class="pub-heading-link" data-pub-anchor="${escapeHtml(slug)}" aria-label="Zu Abschnitt ${escapeHtml(text)}">#</button></h${level}>`);
      continue;
    }

    if (/^\s*(?:---+|___+|\*\*\*+)\s*$/.test(line)) { closeBlocks(); html.push("<hr>"); continue; }

    if (isTableRow(line) && index + 1 < lines.length && isTableSeparator(lines[index + 1])) {
      closeBlocks();
      const header = splitTableRow(line);
      const alignments = splitTableRow(lines[index + 1]).map(parseTableAlignment);
      const rows = [];
      index += 2;
      while (index < lines.length && isTableRow(lines[index]) && lines[index].trim()) {
        rows.push(splitTableRow(lines[index]));
        index += 1;
      }
      index -= 1;
      html.push(renderTable(header, rows, alignments, view));
      continue;
    }

    const unordered = line.match(/^\s*[-+*]\s+(.+)$/);
    const ordered = line.match(/^\s*\d+[.)]\s+(.+)$/);
    if (unordered || ordered) {
      flushParagraph();
      const nextType = unordered ? "ul" : "ol";
      if (listType !== nextType) { closeList(); listType = nextType; html.push(`<${listType}>`); }
      const item = (unordered || ordered)[1];
      const task = item.match(/^\[([ xX])\]\s+(.+)$/);
      if (task) html.push(`<li class="pub-task"><input type="checkbox" disabled ${task[1].toLowerCase() === "x" ? "checked" : ""}><span>${renderInline(task[2], view)}</span></li>`);
      else html.push(`<li>${renderInline(item, view)}</li>`);
      continue;
    }

    const quote = line.match(/^\s*>\s?(.*)$/);
    if (quote) { closeBlocks(); html.push(`<blockquote><p>${renderInline(quote[1], view)}</p></blockquote>`); continue; }

    paragraph.push(line.trim());
  }

  if (codeFence) html.push(`<pre class="pub-code"><code data-language="${escapeHtml(codeFence)}">${escapeHtml(codeLines.join("\n"))}</code></pre>`);
  closeBlocks();
  return { html: html.join("\n"), headings };
}

function renderInline(raw, view) {
  const text = String(raw || "");
  const tokenPattern = /(`[^`\n]+`|!?\[[^\]\n]*\]\([^)\n]+\))/g;
  let output = "";
  let cursor = 0;
  let match;

  while ((match = tokenPattern.exec(text))) {
    output += renderPlainInline(text.slice(cursor, match.index));
    const token = match[0];
    output += token.startsWith("`")
      ? `<code>${escapeHtml(token.slice(1, -1))}</code>`
      : renderMarkdownLinkToken(token, view);
    cursor = match.index + token.length;
  }
  output += renderPlainInline(text.slice(cursor));
  return output;
}

function renderPlainInline(value) {
  let text = escapeHtml(value);
  text = text.replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>");
  text = text.replace(/___(.+?)___/g, "<strong><em>$1</em></strong>");
  text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  text = text.replace(/__(.+?)__/g, "<strong>$1</strong>");
  text = text.replace(/~~(.+?)~~/g, "<del>$1</del>");
  text = text.replace(/(^|[^*])\*([^*]+?)\*(?!\*)/g, "$1<em>$2</em>");
  return text;
}

function renderMarkdownLinkToken(token, view) {
  const image = token.startsWith("!");
  const match = token.match(/^!?\[([^\]]*)\]\(([^)]+)\)$/);
  if (!match) return escapeHtml(token);
  const label = match[1];
  const target = stripMarkdownLinkTitle(match[2]);
  const resolved = resolvePublicationTarget(target, view);

  if (image) {
    if (resolved.kind === "external") return `<img src="${escapeHtml(resolved.href)}" alt="${escapeHtml(label)}" loading="lazy">`;
    if (resolved.kind === "file" && IMAGE_EXTENSIONS.test(resolved.path)) {
      const src = `/api/files/raw/${encodeURIComponent(resolved.path)}?source=${encodeURIComponent(resolved.source)}`;
      return `<figure><img src="${src}" alt="${escapeHtml(label)}" loading="lazy">${label ? `<figcaption>${escapeHtml(label)}</figcaption>` : ""}</figure>`;
    }
    return `<span class="pub-missing-image">[Bild: ${escapeHtml(label)}]</span>`;
  }

  if (resolved.kind === "anchor") return `<a href="#pub-${escapeHtml(resolved.anchor)}" data-pub-anchor="${escapeHtml(resolved.anchor)}">${renderPlainInline(label)}</a>`;
  if (resolved.kind === "reader") return `<a href="#" data-pub-reader-link="${escapeHtml(resolved.path)}" data-pub-source="${escapeHtml(resolved.source)}"${resolved.anchor ? ` data-pub-target-anchor="${escapeHtml(resolved.anchor)}"` : ""}>${renderPlainInline(label)}</a>`;
  if (resolved.kind === "file") return `<a href="#" data-pub-file="${escapeHtml(resolved.path)}" data-pub-source="${escapeHtml(resolved.source)}">${renderPlainInline(label)}</a>`;
  return `<a href="${escapeHtml(resolved.href)}" target="_blank" rel="noopener noreferrer">${renderPlainInline(label)}</a>`;
}

export function resolvePublicationTarget(rawTarget, view) {
  const target = String(rawTarget || "").trim();
  if (!target) return { kind: "external", href: "#" };
  if (target.startsWith("#")) return { kind: "anchor", anchor: slugify(decodeSafe(target.slice(1))) };
  if (/^(?:https?:|mailto:|tel:)/i.test(target)) return { kind: "external", href: target };
  if (target.startsWith("/")) return { kind: "external", href: target };

  const hashIndex = target.indexOf("#");
  const pathPart = decodeSafe((hashIndex >= 0 ? target.slice(0, hashIndex) : target).split("?")[0]);
  const anchor = hashIndex >= 0 ? slugify(decodeSafe(target.slice(hashIndex + 1))) : "";
  if (!pathPart) return { kind: "anchor", anchor };

  const currentSource = view?.source === "docs" ? "docs" : "research";
  const currentPath = String(view?.path || "").replace(/^\/+/, "");
  const repoCurrent = `${currentSource}/${currentPath}`;
  const base = dirname(repoCurrent);
  const repoPath = normalizeRepoPath(`${base}/${pathPart}`);

  if (repoPath.startsWith("research/")) {
    const path = repoPath.slice("research/".length);
    return { kind: READER_EXTENSIONS.test(path) ? "reader" : "file", source: "research", path, anchor };
  }
  if (repoPath.startsWith("docs/")) {
    const path = repoPath.slice("docs/".length);
    return { kind: READER_EXTENSIONS.test(path) ? "reader" : "file", source: "docs", path, anchor };
  }
  return { kind: "external", href: `${REPOSITORY_BLOB_ROOT}${encodeURI(repoPath)}${anchor ? `#${encodeURIComponent(anchor)}` : ""}` };
}

function normalizeRepoPath(value) {
  const parts = String(value || "").replace(/\\/g, "/").split("/");
  const stack = [];
  for (const part of parts) {
    if (!part || part === ".") continue;
    if (part === "..") { if (stack.length) stack.pop(); continue; }
    stack.push(part);
  }
  return stack.join("/");
}

function sourceReference(path, fallbackSource = "research") {
  const normalized = normalizeRepoPath(String(path || ""));
  if (normalized.startsWith("research/")) return { source: "research", path: normalized.slice(9) };
  if (normalized.startsWith("docs/")) return { source: "docs", path: normalized.slice(5) };
  return { source: fallbackSource, path: normalized };
}

function stripResearchPrefix(path) {
  const normalized = normalizeRepoPath(path);
  return normalized.startsWith("research/") ? normalized.slice(9) : normalized;
}

function isTableRow(line) {
  const trimmed = line.trim();
  return trimmed.includes("|") && !trimmed.startsWith("```");
}

function isTableSeparator(line) {
  const cells = splitTableRow(line);
  return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell.trim()));
}

function splitTableRow(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((cell) => cell.trim());
}

function parseTableAlignment(cell) {
  const trimmed = cell.trim();
  if (trimmed.startsWith(":") && trimmed.endsWith(":")) return "center";
  if (trimmed.endsWith(":")) return "right";
  return "left";
}

function renderTable(header, rows, alignments, view) {
  const cells = header.map((cell, index) => `<th style="text-align:${alignments[index] || "left"}">${renderInline(cell, view)}</th>`).join("");
  const body = rows.map((row) => `<tr>${header.map((_, index) => `<td style="text-align:${alignments[index] || "left"}">${renderInline(row[index] || "", view)}</td>`).join("")}</tr>`).join("");
  return `<div class="pub-table-wrap"><table><thead><tr>${cells}</tr></thead><tbody>${body}</tbody></table></div>`;
}

function updateSearch(container, query) {
  clearSearchHighlights(container);
  const state = readerStates.get(container);
  if (!state) return;
  const needle = String(query || "").trim();
  if (needle.length < 2) {
    state.searchMatches = [];
    state.searchIndex = -1;
    setSearchCount(container, "");
    return;
  }

  const article = container.querySelector("#pub-reader-article");
  if (!article) return;
  const lowerNeedle = needle.toLocaleLowerCase("de-DE");
  const walker = document.createTreeWalker(article, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      const parent = node.parentElement;
      if (!parent || parent.closest("pre, code, script, style, mark")) return NodeFilter.FILTER_REJECT;
      return node.nodeValue?.toLocaleLowerCase("de-DE").includes(lowerNeedle) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    },
  });
  const nodes = [];
  while (walker.nextNode() && nodes.length < 250) nodes.push(walker.currentNode);

  const matches = [];
  for (const node of nodes) {
    const text = node.nodeValue || "";
    const lower = text.toLocaleLowerCase("de-DE");
    const fragment = document.createDocumentFragment();
    let cursor = 0;
    let found = lower.indexOf(lowerNeedle, cursor);
    while (found >= 0) {
      fragment.append(document.createTextNode(text.slice(cursor, found)));
      const mark = document.createElement("mark");
      mark.dataset.pubSearch = "true";
      mark.textContent = text.slice(found, found + needle.length);
      fragment.append(mark);
      matches.push(mark);
      cursor = found + needle.length;
      found = lower.indexOf(lowerNeedle, cursor);
    }
    fragment.append(document.createTextNode(text.slice(cursor)));
    node.replaceWith(fragment);
  }

  state.searchMatches = matches;
  state.searchIndex = matches.length ? 0 : -1;
  setSearchCount(container, matches.length ? `1 / ${matches.length}` : "0 Treffer");
  if (matches.length) focusSearchMatch(container, 0, false);
}

function clearSearchHighlights(container) {
  container.querySelectorAll("mark[data-pub-search]").forEach((mark) => mark.replaceWith(document.createTextNode(mark.textContent || "")));
  container.querySelector("#pub-reader-article")?.normalize();
}

function moveSearch(container, delta) {
  const state = readerStates.get(container);
  if (!state?.searchMatches.length) return;
  state.searchIndex = (state.searchIndex + delta + state.searchMatches.length) % state.searchMatches.length;
  focusSearchMatch(container, state.searchIndex, true);
}

function focusSearchMatch(container, index, scroll) {
  const state = readerStates.get(container);
  if (!state?.searchMatches.length) return;
  state.searchMatches.forEach((mark, idx) => mark.classList.toggle("active", idx === index));
  const active = state.searchMatches[index];
  if (scroll) active?.scrollIntoView({ behavior: "smooth", block: "center" });
  setSearchCount(container, `${index + 1} / ${state.searchMatches.length}`);
}

function setSearchCount(container, value) {
  const output = container.querySelector("#pub-search-count");
  if (output) output.value = value;
}

function scrollToPublicationAnchor(container, slug) {
  const normalized = slugify(slug);
  const heading = Array.from(container.querySelectorAll("[data-pub-heading]")).find((node) => node.dataset.pubSlug === normalized);
  if (!heading) return;
  heading.scrollIntoView({ behavior: "smooth", block: "start" });
  container.querySelectorAll(".pub-reader-toc a").forEach((link) => link.classList.toggle("active", link.dataset.pubAnchor === normalized));
}

function wireHeadingObserver(container) {
  if (!("IntersectionObserver" in window)) return;
  const links = new Map(Array.from(container.querySelectorAll(".pub-reader-toc a[data-pub-anchor]")).map((link) => [link.dataset.pubAnchor, link]));
  const observer = new IntersectionObserver((entries) => {
    const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
    if (!visible) return;
    const slug = visible.target.dataset.pubSlug;
    links.forEach((link, key) => link.classList.toggle("active", key === slug));
  }, { rootMargin: "-18% 0px -72% 0px", threshold: [0, 1] });
  container.querySelectorAll("[data-pub-heading]").forEach((heading) => observer.observe(heading));
}

function wireReadingProgress(container) {
  const bar = container.querySelector("#pub-reading-progress");
  const article = container.querySelector("#pub-reader-article");
  if (!bar || !article) return;
  const update = () => {
    const rect = article.getBoundingClientRect();
    const total = Math.max(1, article.offsetHeight - window.innerHeight * 0.65);
    const progressed = Math.min(total, Math.max(0, -rect.top + window.innerHeight * 0.18));
    bar.style.width = `${Math.round((progressed / total) * 100)}%`;
  };
  window.addEventListener("scroll", update, { passive: true });
  update();
}

function wireSpeechControls(container) {
  const mount = container.querySelector("#pub-reader-speech-mount");
  const article = container.querySelector("#pub-reader-article");
  if (!mount || !article) return;
  const getText = () => article.innerText || article.textContent || "";
  createSpeechControls(mount, getText, { label: "Publikation vorlesen", showVoiceOptions: true });
}

function showToast(container, message, isError = false) {
  const toast = container.querySelector("#pub-reader-toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.toggle("error", isError);
  toast.classList.add("visible");
  window.clearTimeout(Number(toast.dataset.timer || 0));
  const timer = window.setTimeout(() => toast.classList.remove("visible"), 3200);
  toast.dataset.timer = String(timer);
}

async function copyText(value) {
  if (navigator.clipboard?.writeText) return navigator.clipboard.writeText(value);
  const input = document.createElement("textarea");
  input.value = value;
  input.style.position = "fixed";
  input.style.opacity = "0";
  document.body.append(input);
  input.select();
  document.execCommand("copy");
  input.remove();
}

function firstHeading(markdown) {
  const match = String(markdown || "").match(/^#\s+(.+)$/m);
  return match ? stripMarkdownText(match[1]) : "";
}

function stripMarkdownText(value) {
  return String(value || "")
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/[`*_~]/g, "")
    .trim();
}

function stripMarkdownLinkTitle(value) {
  return String(value || "").trim().replace(/\s+(?:"[^"]*"|'[^']*')\s*$/, "").replace(/^<|>$/g, "");
}

function slugify(value) {
  return String(value || "")
    .trim()
    .toLocaleLowerCase("de-DE")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function dirname(path) {
  const normalized = String(path || "").replace(/\\/g, "/");
  const index = normalized.lastIndexOf("/");
  return index >= 0 ? normalized.slice(0, index) : "";
}

function basename(path) {
  const parts = String(path || "").replace(/\\/g, "/").split("/");
  return parts[parts.length - 1] || path;
}

function decodeSafe(value) {
  try { return decodeURIComponent(value); } catch { return value; }
}

function countWords(value) {
  return (String(value || "").match(/[\p{L}\p{N}][\p{L}\p{N}'’-]*/gu) || []).length;
}

function formatBytes(bytes) {
  const value = Number(bytes);
  if (!Number.isFinite(value)) return "—";
  if (value < 1024) return `${value} B`;
  if (value < 1024 * 1024) return `${(value / 1024).toFixed(1)} KiB`;
  return `${(value / (1024 * 1024)).toFixed(1)} MiB`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function nextFrame() {
  return new Promise((resolve) => requestAnimationFrame(() => resolve()));
}

function ensureReaderStyles() {
  if (document.getElementById("publication-reader-styles")) return;
  const style = document.createElement("style");
  style.id = "publication-reader-styles";
  style.textContent = `
    #publication-panel { padding: 0; }
    .publication-reader { --pub-accent: var(--accent, #275df5); --pub-text: var(--ink, #18202b); --pub-muted: var(--ink-3, #667085); --pub-border: var(--rule, #d9dee7); --pub-surface: var(--paper-2, #ffffff); --pub-soft: color-mix(in srgb, var(--paper-3) 42%, transparent); color: var(--pub-text); position: relative; min-width: 0; }
    .pub-reader-progress { position: sticky; top: 0; z-index: 25; height: 3px; background: transparent; }
    .pub-reader-progress span { display: block; width: 0; height: 100%; background: var(--pub-accent); transition: width 120ms linear; }
    .pub-reader-hero { display: flex; justify-content: space-between; gap: clamp(12px, 1.5vw, 24px); align-items: flex-start; padding: clamp(16px, 1.8vw, 28px) clamp(18px, 2vw, 30px) clamp(14px, 1.4vw, 22px); border: 1px solid var(--pub-border); border-radius: 14px 14px 0 0; background: var(--pub-surface); }
    .pub-reader-identity { min-width: 0; }
    .pub-reader-eyebrow { display: block; margin-bottom: 8px; color: var(--pub-accent); font: 700 .72rem/1.2 var(--font-mono, monospace); letter-spacing: .12em; }
    .pub-reader-hero h1 { margin: 0; max-width: 980px; font-size: clamp(1.5rem, 2.4vw, 2.35rem); line-height: 1.08; letter-spacing: -.025em; }
    .pub-reader-badges { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 14px; }
    .pub-reader-badges span { padding: 5px 9px; border: 1px solid var(--pub-border); border-radius: 999px; color: var(--pub-muted); background: var(--pub-soft); font-size: .78rem; }
    .pub-reader-primary-actions { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; }
    .pub-reader-button, .pub-reader-icon-button, .pub-reader-toolbar button, .pub-reader-footer button, .pub-reader-document-banner button, .pub-reader-toc-meta button { border: 1px solid var(--pub-border); border-radius: 9px; background: var(--pub-surface); color: inherit; min-height: 36px; padding: 7px 11px; cursor: pointer; font: inherit; }
    .pub-reader-button:hover, .pub-reader-icon-button:hover:not(:disabled), .pub-reader-toolbar button:hover, .pub-reader-footer button:hover, .pub-reader-document-banner button:hover, .pub-reader-toc-meta button:hover { border-color: var(--pub-accent); }
    .pub-reader-button-primary { background: var(--pub-accent); color: #fff; border-color: var(--pub-accent); }
    .pub-reader-icon-button { width: 38px; padding: 0; font-size: 1.05rem; }
    .pub-reader-icon-button:disabled, .pub-reader-button:disabled { opacity: .38; cursor: default; }
    .pub-reader-toolbar { position: sticky; top: 3px; z-index: 20; display: flex; flex-wrap: wrap; gap: clamp(6px, 0.8vw, 12px); align-items: center; padding: clamp(6px, 0.7vw, 10px) clamp(10px, 1vw, 14px); border: 1px solid var(--pub-border); border-top: 0; background: color-mix(in srgb, var(--pub-surface) 94%, transparent); backdrop-filter: blur(12px); }
    .pub-reader-history { display: flex; gap: 6px; flex-shrink: 0; }
    .pub-reader-location { min-width: 0; display: flex; gap: 5px; align-items: center; color: var(--pub-muted); overflow: hidden; font-size: .78rem; flex: 1 1 140px; }
    .pub-reader-location span { color: var(--pub-accent); font-weight: 700; }
    .pub-reader-location code { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; background: none; padding: 0; }
    .pub-reader-search { display: grid; grid-template-columns: minmax(0, 1fr) auto 32px 32px; align-items: center; border: 1px solid var(--pub-border); border-radius: 10px; background: var(--pub-surface); overflow: hidden; flex: 2 1 200px; }
    .pub-reader-search:focus-within { border-color: var(--pub-accent); box-shadow: 0 0 0 2px color-mix(in srgb, var(--pub-accent) 16%, transparent); }
    .pub-reader-search input { min-width: 0; width: 100%; border: 0; outline: 0; padding: 8px 10px; color: inherit; background: transparent; }
    .pub-reader-search output { color: var(--pub-muted); font-size: .72rem; white-space: nowrap; }
    .pub-reader-search button { min-height: 34px; padding: 0; border-width: 0 0 0 1px; border-radius: 0; }
    .pub-reader-speech { display: flex; align-items: center; flex-shrink: 0; }
    .pub-reader-speech .speech-reader-controls { display: inline-flex; align-items: center; gap: 3px; }
    .pub-reader-speech .speech-reader-controls button { width: 30px; height: 30px; padding: 0; border: 1px solid var(--pub-border); border-radius: 7px; background: var(--pub-surface); color: var(--pub-text); font-size: .8rem; cursor: pointer; display: grid; place-items: center; transition: background .12s, color .12s; }
    .pub-reader-speech .speech-reader-controls button:hover:not(:disabled) { background: var(--pub-soft); border-color: var(--pub-accent); }
    .pub-reader-speech .speech-reader-controls button:disabled { opacity: .35; cursor: default; }
    .pub-reader-speech .speech-reader-status { font-size: .6rem; color: var(--pub-muted); min-width: 5ch; margin-left: 3px; white-space: nowrap; }
    .pub-reader-layout { display: grid; grid-template-columns: minmax(140px, 200px) minmax(0, 1fr); align-items: start; border: 1px solid var(--pub-border); border-top: 0; background: var(--pub-surface); }
    .pub-reader-toc { position: sticky; top: 0; max-height: calc(100vh - 50px); overflow-y: auto; padding: clamp(10px, 1vw, 16px) clamp(6px, 0.8vw, 12px) clamp(12px, 1.2vw, 20px); border-right: 1px solid var(--pub-border); }
    .pub-reader-toc-head { display: flex; justify-content: space-between; gap: 8px; align-items: baseline; padding: 0 6px 10px; }
    .pub-reader-toc-head span { color: var(--pub-muted); font-size: .72rem; }
    .pub-reader-toc nav { display: grid; gap: 2px; }
    .pub-reader-toc a { display: block; padding: 7px 9px; border-radius: 8px; color: var(--pub-muted); text-decoration: none; font-size: .82rem; line-height: 1.35; }
    .pub-reader-toc a[data-level="2"] { padding-left: 18px; }
    .pub-reader-toc a[data-level="3"] { padding-left: 29px; font-size: .76rem; }
    .pub-reader-toc a:hover, .pub-reader-toc a.active { color: var(--pub-text); background: var(--pub-soft); }
    .pub-reader-toc a.active { box-shadow: inset 3px 0 0 var(--pub-accent); }
    .pub-reader-toc-meta { display: grid; gap: 6px; margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--pub-border); }
    .pub-reader-toc-meta button { min-height: 31px; text-align: left; color: var(--pub-muted); font-size: .74rem; }
    .pub-reader-document { min-width: 0; }
    .pub-reader-document-banner { display: flex; justify-content: space-between; gap: 16px; align-items: center; padding: 13px 24px; border-bottom: 1px solid var(--pub-border); background: var(--pub-soft); }
    .pub-reader-document-banner div { min-width: 0; display: grid; gap: 3px; }
    .pub-reader-document-banner span { color: var(--pub-accent); font: 700 .66rem/1.2 var(--font-mono, monospace); letter-spacing: .08em; }
    .pub-reader-document-banner strong { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .pub-reader-article { width: 100%; max-width: 100%; margin: 0; padding: clamp(18px, 2vw, 28px) clamp(20px, 2.5vw, 32px) clamp(40px, 5vw, 60px) clamp(20px, 2.5vw, 32px); font-size: clamp(0.88rem, 1vw, 1rem); line-height: 1.7; overflow-wrap: break-word; word-wrap: break-word; hyphens: auto; }
    .pub-reader-article h1, .pub-reader-article h2, .pub-reader-article h3, .pub-reader-article h4, .pub-reader-article h5, .pub-reader-article h6 { scroll-margin-top: 82px; line-height: 1.2; letter-spacing: -.015em; }
    .pub-reader-article h1 { margin: 0 0 clamp(16px, 1.8vw, 28px); font-size: clamp(1.4rem, 2.2vw, 2.2rem); }
    .pub-reader-article h2 { margin: 2em 0 .65em; padding-bottom: .3em; border-bottom: 1px solid var(--pub-border); font-size: clamp(1.15rem, 1.6vw, 1.55rem); }
    .pub-reader-article h3 { margin: 1.7em 0 .55em; font-size: clamp(1.05rem, 1.3vw, 1.2rem); }
    .pub-reader-article h4 { margin: 1.4em 0 .45em; font-size: clamp(0.95rem, 1.1vw, 1.06rem); }
    .pub-reader-article p { margin: 0 0 0.85em; }
    .pub-reader-article a { color: var(--pub-accent); text-underline-offset: 3px; }
    .pub-reader-article a[data-pub-reader-link]::after { content: " ↗"; font-size: .72em; text-decoration: none; }
    .pub-reader-article code { padding: .13em .35em; border: 1px solid var(--pub-border); border-radius: 5px; background: var(--pub-soft); font-family: var(--font-mono, ui-monospace, monospace); font-size: .88em; }
    .pub-reader-article pre { overflow-x: auto; max-width: 100%; }
    .pub-reader-article .pub-code { overflow-x: auto; max-width: 100%; margin: 1.2em 0 1.6em; padding: 16px 18px; border: 1px solid var(--pub-border); border-radius: 12px; background: var(--pub-soft); line-height: 1.5; }
    .pub-reader-article .pub-code code { padding: 0; border: 0; background: transparent; }
    .pub-reader-article blockquote { margin: 1.35em 0; padding: 12px 18px; border-left: 4px solid var(--pub-accent); background: var(--pub-soft); color: var(--pub-muted); }
    .pub-reader-article blockquote p { margin: 0; }
    .pub-reader-article ul, .pub-reader-article ol { margin: .4em 0 1.2em; padding-left: 1.6em; }
    .pub-reader-article li { margin: .35em 0; }
    .pub-reader-article .pub-task { list-style: none; margin-left: -1.3em; display: flex; gap: 8px; align-items: flex-start; }
    .pub-reader-article hr { border: 0; border-top: 1px solid var(--pub-border); margin: 2.3em 0; }
    .pub-reader-article img { display: block; max-width: 100%; height: auto; margin: 1em auto; border-radius: 10px; overflow: hidden; }
    .pub-reader-article figure { margin: 1.4em 0; }
    .pub-reader-article figcaption { color: var(--pub-muted); text-align: center; font-size: .8rem; }
    .pub-reader-article details.pub-details { margin: 1em 0; padding: 10px 14px; border: 1px solid var(--pub-border); border-radius: 10px; background: var(--pub-soft); }
    .pub-reader-article details.pub-details > summary { cursor: pointer; font-weight: 700; }
    .pub-heading-link { opacity: 0; margin-left: 8px; padding: 0; border: 0; background: none; color: var(--pub-accent); cursor: pointer; font: inherit; }
    .pub-reader-article h1:hover .pub-heading-link, .pub-reader-article h2:hover .pub-heading-link, .pub-reader-article h3:hover .pub-heading-link { opacity: .65; }
    .pub-table-wrap { overflow-x: auto; max-width: 100%; margin: 1.2em 0 1.7em; border: 1px solid var(--pub-border); border-radius: 10px; }
    .pub-reader-article table { width: 100%; max-width: 100%; border-collapse: collapse; font-size: .9rem; overflow-wrap: break-word; }
    .pub-reader-article th, .pub-reader-article td { padding: 10px 12px; border-bottom: 1px solid var(--pub-border); vertical-align: top; }
    .pub-reader-article th { background: var(--pub-soft); }
    .pub-reader-article tr:last-child td { border-bottom: 0; }
    .pub-reader-article mark[data-pub-search] { padding: .05em .15em; border-radius: 3px; }
    .pub-reader-article mark[data-pub-search].active { outline: 2px solid var(--pub-accent); }
    .pub-reader-footer { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(8px, 0.8vw, 12px); padding: clamp(10px, 1vw, 16px); border: 1px solid var(--pub-border); border-top: 0; border-radius: 0 0 14px 14px; background: var(--pub-soft); }
    .pub-reader-footer section { min-width: 0; display: grid; align-content: start; gap: 4px; padding: clamp(8px, 0.9vw, 14px); border: 1px solid var(--pub-border); border-radius: 8px; background: var(--pub-surface); }
    .pub-reader-footer-label { color: var(--pub-muted); font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; }
    .pub-reader-footer code, .pub-reader-footer small { overflow-wrap: anywhere; color: var(--pub-muted); font-size: .72rem; }
    .pub-reader-export-list { display: flex; flex-wrap: wrap; gap: 6px; }
    .pub-reader-export-list a { padding: 6px 8px; border: 1px solid var(--pub-border); border-radius: 7px; color: inherit; text-decoration: none; font-size: .78rem; }
    .pub-reader-state { min-height: 200px; display: grid; place-items: center; align-content: center; gap: 8px; padding: clamp(24px, 3vw, 42px); border: 1px solid var(--pub-border, #d9dee7); border-radius: 14px; text-align: center; color: var(--pub-muted, #667085); }
    .pub-reader-state strong { color: var(--pub-text, #18202b); font-size: 1.05rem; }
    .pub-reader-state-error { border-style: dashed; }
    .pub-reader-spinner { width: 26px; height: 26px; border: 3px solid var(--pub-border, #d9dee7); border-top-color: var(--pub-accent, #275df5); border-radius: 50%; animation: pub-spin .7s linear infinite; }
    .pub-reader-toast { position: fixed; right: clamp(12px, 1.5vw, 24px); bottom: clamp(12px, 1.5vw, 24px); z-index: 80; max-width: min(380px, calc(100vw - 32px)); padding: 8px 12px; border: 1px solid var(--pub-border); border-radius: 8px; background: var(--pub-text); color: var(--pub-surface); opacity: 0; transform: translateY(6px); pointer-events: none; transition: .15s ease; }
    .pub-reader-toast.visible { opacity: 1; transform: translateY(0); }
    .pub-reader-toast.error { border-color: #c24141; }
    .pub-reader-toc-empty { padding: 8px; color: var(--pub-muted); font-size: .8rem; }
    .sr-only { position: absolute !important; width: 1px !important; height: 1px !important; padding: 0 !important; margin: -1px !important; overflow: hidden !important; clip: rect(0,0,0,0) !important; white-space: nowrap !important; border: 0 !important; }
    @keyframes pub-spin { to { transform: rotate(360deg); } }
    @media (max-width: 1050px) {
      .pub-reader-toolbar { grid-template-columns: auto 1fr; }
      .pub-reader-search { grid-column: 1 / -1; }
      .pub-reader-layout { grid-template-columns: 1fr; }
      .pub-reader-toc { position: relative; top: auto; max-height: 260px; border-right: 0; border-bottom: 1px solid var(--pub-border); }
      .pub-reader-toc nav { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .pub-reader-footer { grid-template-columns: 1fr; }
    }
    @media (max-width: 720px) {
      .pub-reader-hero { flex-direction: column; padding: 20px; }
      .pub-reader-primary-actions { justify-content: flex-start; }
      .pub-reader-toolbar { grid-template-columns: 1fr; }
      .pub-reader-history { order: 1; }
      .pub-reader-location { order: 2; }
      .pub-reader-search { order: 3; grid-column: auto; }
      .pub-reader-toc nav { grid-template-columns: 1fr; }
      .pub-reader-article { padding: 20px 16px 40px; }
      .pub-reader-document-banner { align-items: flex-start; flex-direction: column; }
    }
    @media print {
      .pub-reader-progress, .pub-reader-toolbar, .pub-reader-toc, .pub-reader-primary-actions, .pub-reader-document-banner button, .pub-reader-footer button, .pub-reader-toast { display: none !important; }
      .pub-reader-layout { display: block; border: 0; }
      .pub-reader-hero, .pub-reader-footer { border: 0; }
      .pub-reader-article { width: 100%; max-width: none; padding: 16px 0; }
    }
  `;
  document.head.append(style);
}
