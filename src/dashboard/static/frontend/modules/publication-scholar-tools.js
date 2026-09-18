"use strict";

import { createSpeechControls, detectSpeechLanguage, stopSpeech } from "../../speech-reader.js";

const EASY_LANGUAGE_STATUS = "Leichte Sprache – vorbereitet, noch nicht veröffentlicht";

export function enhancePublicationScholarReader(container, {
  view,
  rootData,
  openDocument,
} = {}) {
  const reader = container.querySelector(".publication-reader");
  const article = container.querySelector("#pub-reader-article");
  const toolbar = container.querySelector(".pub-reader-toolbar");
  const toc = container.querySelector(".pub-reader-toc");
  if (!reader || !article || !toolbar || !toc || !view) return;

  stopSpeech();
  reader.classList.add("pub-scholar-reader");
  ensureScholarStyles();

  const sequence = publicationSequence(rootData);
  injectChapterNavigator(toc, sequence, view, openDocument);
  injectSpeechControls(toolbar, article);
  injectModeControls(toolbar, reader);
  injectSelectionAssistant(reader, article, view);
  injectBottomNavigation(article, sequence, view, openDocument);
}

function injectSpeechControls(toolbar, article) {
  const mount = document.createElement("div");
  mount.className = "pub-scholar-speech";
  toolbar.append(mount);

  createSpeechControls(mount, () => article.innerText || article.textContent || "", {
    label: "Dissertation vorlesen",
    showVoiceOptions: true,
    getSegments: () => speechSegments(article),
    onSegment: (segment) => {
      article.querySelectorAll(".pub-speech-active").forEach((node) => node.classList.remove("pub-speech-active"));
      const element = segment.element;
      if (!element?.isConnected) return;
      element.classList.add("pub-speech-active");
      element.scrollIntoView({ behavior: "smooth", block: "center" });
    },
  });
}

function speechSegments(article) {
  const selector = "h1,h2,h3,h4,p,li,blockquote,figcaption,th,td";
  return [...article.querySelectorAll(selector)]
    .filter((element) => !element.closest("pre") && !element.closest(".pub-reader-bottom-nav"))
    .map((element) => {
      const text = (element.innerText || element.textContent || "").replace(/\s+/g, " ").trim();
      return { text, lang: detectSpeechLanguage(text, "de-DE"), element };
    })
    .filter((segment) => segment.text.length > 1);
}

function injectModeControls(toolbar, reader) {
  const group = document.createElement("div");
  group.className = "pub-scholar-modes";
  group.setAttribute("role", "group");
  group.setAttribute("aria-label", "Darstellung");
  group.innerHTML = `
    <button type="button" class="active" data-pub-width="full" title="Gesamte verfügbare Breite nutzen">Vollbreite</button>
    <button type="button" data-pub-width="focus" title="Kompaktere Lesebreite">Fokus</button>
    <button type="button" disabled title="${EASY_LANGUAGE_STATUS}">Leichte Sprache · geplant</button>`;
  toolbar.append(group);
  group.addEventListener("click", (event) => {
    const button = event.target.closest("[data-pub-width]");
    if (!button) return;
    group.querySelectorAll("[data-pub-width]").forEach((candidate) => candidate.classList.toggle("active", candidate === button));
    reader.dataset.readingWidth = button.dataset.pubWidth;
  });
}

function injectSelectionAssistant(reader, article, view) {
  const panel = document.createElement("div");
  panel.className = "pub-selection-assistant";
  panel.hidden = true;
  panel.innerHTML = `
    <div><span>MARKIERTER TEXT</span><strong id="pub-selection-preview"></strong></div>
    <button type="button" data-pub-selection-ai>Ask KI</button>
    <button type="button" data-pub-selection-clear aria-label="Markierung schließen">×</button>`;
  reader.append(panel);

  let selectedText = "";
  const update = () => {
    const selection = window.getSelection();
    const text = selection?.toString().replace(/\s+/g, " ").trim() || "";
    if (!text || !selection?.rangeCount) {
      selectedText = "";
      panel.hidden = true;
      return;
    }
    const range = selection.getRangeAt(0);
    const common = range.commonAncestorContainer.nodeType === Node.ELEMENT_NODE
      ? range.commonAncestorContainer
      : range.commonAncestorContainer.parentElement;
    if (!common || !article.contains(common)) {
      selectedText = "";
      panel.hidden = true;
      return;
    }
    selectedText = text.slice(0, 6000);
    panel.hidden = false;
    const preview = panel.querySelector("#pub-selection-preview");
    preview.textContent = selectedText.length > 180 ? `${selectedText.slice(0, 180)}…` : selectedText;
  };

  article.addEventListener("mouseup", () => queueMicrotask(update));
  article.addEventListener("keyup", () => queueMicrotask(update));
  panel.querySelector("[data-pub-selection-clear]").addEventListener("click", () => {
    window.getSelection()?.removeAllRanges();
    selectedText = "";
    panel.hidden = true;
  });
  panel.querySelector("[data-pub-selection-ai]").addEventListener("click", () => {
    if (!selectedText) return;
    document.dispatchEvent(new CustomEvent("brain5d:ask-ai", {
      detail: {
        prompt: `Analysiere den folgenden markierten Ausschnitt aus der wissenschaftlichen Publikation. Erkläre ihn präzise, prüfe Behauptungen kritisch und trenne dokumentierten Inhalt, DATA/EVIDENCE und Interpretation.\n\nQuelle: ${view.source}/${view.path}\n\nMarkierter Text:\n${selectedText}`,
        source: view.source,
        path: view.path,
        selection: selectedText,
      },
    }));
    panel.hidden = true;
  });
}

function injectChapterNavigator(toc, sequence, view, openDocument) {
  if (!sequence.length) return;
  const section = document.createElement("section");
  section.className = "pub-scholar-chapters";
  const currentIndex = sequence.findIndex((item) => item.source === view.source && item.path === view.path);
  section.innerHTML = `
    <div class="pub-reader-toc-head"><strong>Kapitel / Dokumente</strong><span>${sequence.length}</span></div>
    <nav class="pub-scholar-chapter-list">
      ${sequence.map((item, index) => `<button type="button" data-pub-sequence="${index}"${index === currentIndex ? ' class="active" aria-current="page"' : ""}><span>${String(index + 1).padStart(2, "0")}</span><strong>${escapeHtml(item.label)}</strong></button>`).join("")}
    </nav>`;
  toc.prepend(section);
  section.addEventListener("click", (event) => {
    const button = event.target.closest("[data-pub-sequence]");
    if (!button) return;
    const item = sequence[Number(button.dataset.pubSequence)];
    if (item) openDocument(item);
  });
}

function injectBottomNavigation(article, sequence, view, openDocument) {
  if (!sequence.length) return;
  const index = sequence.findIndex((item) => item.source === view.source && item.path === view.path);
  const previous = index > 0 ? sequence[index - 1] : null;
  const next = index >= 0 && index < sequence.length - 1 ? sequence[index + 1] : (index < 0 ? sequence[0] : null);
  const nav = document.createElement("nav");
  nav.className = "pub-reader-bottom-nav";
  nav.setAttribute("aria-label", "Weiterlesen");
  nav.innerHTML = `
    ${previous ? `<button type="button" data-direction="previous"><span>← Zurück</span><strong>${escapeHtml(previous.label)}</strong></button>` : '<span class="pub-reader-nav-spacer"></span>'}
    ${next ? `<button type="button" data-direction="next"><span>Weiter →</span><strong>${escapeHtml(next.label)}</strong></button>` : '<div class="pub-reader-finished"><span>ENDE</span><strong>Aktuelle Fassung vollständig durchlaufen</strong></div>'}`;
  article.append(nav);
  nav.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-direction]");
    if (!button) return;
    const item = button.dataset.direction === "previous" ? previous : next;
    if (item) openDocument(item);
  });
}

function publicationSequence(rootData) {
  const explicit = Array.isArray(rootData?.documents) ? rootData.documents : [];
  if (explicit.length) {
    return explicit
      .filter((item) => item && item.kind === "reader" && typeof item.path === "string")
      .map((item) => {
        const normalized = normalizePath(item.path);
        const source = item.source === "docs" ? "docs" : "research";
        const path = normalized.startsWith(`${source}/`) ? normalized.slice(source.length + 1) : normalized;
        return {
          source,
          path,
          label: item.label || basename(path),
          role: item.role || "document",
        };
      });
  }

  const markdown = rootData?.content || "";
  const rootPath = rootData?.entrypoint_path || rootData?.readme_path || "publications/CURRENT.md";
  const root = normalizeRoot(rootPath);
  const base = dirname(root);
  const seen = new Set();
  const items = [];
  const regex = /\[([^\]]+)\]\(([^)]+\.md)(?:#[^)]+)?\)/gi;
  let match;
  while ((match = regex.exec(String(markdown || "")))) {
    const label = stripMarkdown(match[1]);
    const raw = decodeSafe(match[2].trim());
    const repoPath = normalizePath(`${base}/${raw}`);
    let source = "research";
    let path = repoPath;
    if (repoPath.startsWith("research/")) path = repoPath.slice(9);
    else if (repoPath.startsWith("docs/")) { source = "docs"; path = repoPath.slice(5); }
    else continue;
    const key = `${source}:${path}`;
    if (seen.has(key)) continue;
    seen.add(key);
    items.push({ source, path, label: label || basename(path), role: "linked" });
  }
  return items;
}

function normalizeRoot(path) {
  const normalized = normalizePath(path || "research/publications/README.md");
  return normalized.startsWith("research/") || normalized.startsWith("docs/") ? normalized : `research/${normalized}`;
}

function normalizePath(value) {
  const stack = [];
  String(value || "").replace(/\\/g, "/").split("/").forEach((part) => {
    if (!part || part === ".") return;
    if (part === "..") { stack.pop(); return; }
    stack.push(part);
  });
  return stack.join("/");
}

function dirname(path) {
  const index = path.lastIndexOf("/");
  return index < 0 ? "" : path.slice(0, index);
}

function basename(path) {
  return String(path || "").split("/").pop() || path;
}

function stripMarkdown(value) {
  return String(value || "").replace(/[*_`~]/g, "").trim();
}

function decodeSafe(value) {
  try { return decodeURIComponent(value); } catch (_) { return value; }
}

function escapeHtml(value) {
  return String(value ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function ensureScholarStyles() {
  if (document.getElementById("publication-scholar-styles")) return;
  const style = document.createElement("style");
  style.id = "publication-scholar-styles";
  style.textContent = `
    .pub-scholar-reader { --pub-sticky-top: 72px; }
    .pub-scholar-reader .pub-reader-hero { position: sticky; top: var(--pub-sticky-top); z-index: 23; border-radius: 0; padding: 12px 22px; align-items: center; box-shadow: 0 1px 0 var(--pub-border); }
    .pub-scholar-reader .pub-reader-hero h1 { font-size: clamp(1.15rem,1.7vw,1.55rem); }
    .pub-scholar-reader .pub-reader-eyebrow, .pub-scholar-reader .pub-reader-badges { display: none; }
    .pub-scholar-reader .pub-reader-toolbar { top: calc(var(--pub-sticky-top) + 72px); z-index: 24; grid-template-columns: auto minmax(160px,.65fr) minmax(240px,.7fr) auto auto; }
    .pub-scholar-reader .pub-reader-layout { grid-template-columns: clamp(250px,21vw,340px) minmax(0,1fr); }
    .pub-scholar-reader .pub-reader-toc { top: calc(var(--pub-sticky-top) + 132px); max-height: calc(100vh - var(--pub-sticky-top) - 150px); padding-bottom: 40px; }
    .pub-scholar-reader .pub-reader-article { width: 100%; max-width: none; padding: clamp(30px,3vw,54px) clamp(28px,4vw,72px) 84px; font-size: 1.02rem; line-height: 1.72; }
    .pub-scholar-reader[data-reading-width="focus"] .pub-reader-article { max-width: 980px; }
    .pub-scholar-reader .pub-reader-document { width: 100%; min-width: 0; }
    .pub-scholar-speech { min-width: max-content; }
    .pub-scholar-speech .speech-reader-controls { display:flex; align-items:center; gap:6px; }
    .pub-scholar-speech button, .pub-scholar-speech summary, .pub-scholar-modes button { min-height:34px; padding:6px 9px; border:1px solid var(--pub-border); border-radius:8px; background:var(--pub-surface); color:inherit; cursor:pointer; font:inherit; font-size:.78rem; }
    .pub-scholar-speech .speech-reader-options { position:relative; }
    .pub-scholar-speech .speech-reader-options > summary { list-style:none; }
    .pub-scholar-speech .speech-reader-options-panel { position:absolute; right:0; top:calc(100% + 8px); z-index:60; width:min(420px,80vw); display:grid; gap:10px; padding:14px; border:1px solid var(--pub-border); border-radius:12px; background:var(--pub-surface); box-shadow:0 12px 36px rgba(0,0,0,.18); }
    .pub-scholar-speech .speech-reader-options-panel label { display:grid; gap:5px; font-size:.76rem; }
    .pub-scholar-speech select { min-width:250px; max-width:100%; padding:7px; border:1px solid var(--pub-border); border-radius:7px; background:var(--pub-surface); color:inherit; }
    .pub-scholar-speech .speech-reader-status { color:var(--pub-muted); font-size:.72rem; min-width:56px; }
    .pub-scholar-modes { display:flex; gap:5px; }
    .pub-scholar-modes button.active { border-color:var(--pub-accent); box-shadow:inset 0 -2px 0 var(--pub-accent); }
    .pub-scholar-modes button:disabled { opacity:.5; cursor:not-allowed; }
    .pub-scholar-chapters { padding-bottom:16px; margin-bottom:14px; border-bottom:1px solid var(--pub-border); }
    .pub-scholar-chapter-list { display:grid!important; grid-template-columns:1fr!important; max-height:42vh; overflow:auto; gap:2px!important; }
    .pub-scholar-chapter-list button { display:grid; grid-template-columns:28px minmax(0,1fr); gap:7px; align-items:start; width:100%; padding:7px 8px; border:0; border-radius:7px; background:transparent; color:var(--pub-muted); text-align:left; cursor:pointer; }
    .pub-scholar-chapter-list button:hover,.pub-scholar-chapter-list button.active { color:var(--pub-text); background:var(--pub-soft); }
    .pub-scholar-chapter-list button.active { box-shadow:inset 3px 0 0 var(--pub-accent); }
    .pub-scholar-chapter-list button span { font:600 .65rem/1.5 var(--font-mono,monospace); color:var(--pub-accent); }
    .pub-scholar-chapter-list button strong { font-size:.76rem; line-height:1.35; }
    .pub-reader-bottom-nav { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:70px; padding-top:24px; border-top:1px solid var(--pub-border); }
    .pub-reader-bottom-nav button,.pub-reader-finished { min-height:88px; display:grid; gap:5px; align-content:center; padding:14px 18px; border:1px solid var(--pub-border); border-radius:12px; background:var(--pub-soft); color:inherit; text-align:left; cursor:pointer; }
    .pub-reader-bottom-nav button[data-direction="next"] { text-align:right; }
    .pub-reader-bottom-nav button:hover { border-color:var(--pub-accent); }
    .pub-reader-bottom-nav span { color:var(--pub-accent); font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; }
    .pub-reader-finished { grid-column:2; text-align:right; cursor:default; }
    .pub-speech-active { position:relative; border-radius:5px; background:color-mix(in srgb,var(--pub-accent) 12%,transparent); box-shadow:0 0 0 5px color-mix(in srgb,var(--pub-accent) 12%,transparent); transition:background .15s ease; }
    .pub-selection-assistant { position:sticky; bottom:16px; z-index:55; margin:0 auto 16px; width:min(900px,calc(100% - 40px)); display:grid; grid-template-columns:minmax(0,1fr) auto auto; gap:10px; align-items:center; padding:10px 12px; border:1px solid var(--pub-accent); border-radius:12px; background:color-mix(in srgb,var(--pub-surface) 96%,transparent); box-shadow:0 10px 30px rgba(0,0,0,.18); backdrop-filter:blur(10px); }
    .pub-selection-assistant[hidden] { display:none; }
    .pub-selection-assistant div { min-width:0; display:grid; gap:2px; }
    .pub-selection-assistant span { color:var(--pub-accent); font:700 .65rem/1.2 var(--font-mono,monospace); letter-spacing:.08em; }
    .pub-selection-assistant strong { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:.82rem; }
    .pub-selection-assistant button { min-height:34px; padding:6px 10px; border:1px solid var(--pub-border); border-radius:8px; background:var(--pub-surface); color:inherit; cursor:pointer; }
    .pub-selection-assistant [data-pub-selection-ai] { background:var(--pub-accent); color:#fff; border-color:var(--pub-accent); }
    @media(max-width:1250px){.pub-scholar-reader .pub-reader-toolbar{grid-template-columns:auto 1fr minmax(260px,1fr);}.pub-scholar-speech,.pub-scholar-modes{grid-column:auto/span 1}.pub-scholar-reader .pub-reader-layout{grid-template-columns:260px minmax(0,1fr)}}
    @media(max-width:900px){.pub-scholar-reader .pub-reader-hero{position:relative;top:auto}.pub-scholar-reader .pub-reader-toolbar{position:sticky;top:var(--pub-sticky-top);grid-template-columns:1fr 1fr}.pub-scholar-reader .pub-reader-search{grid-column:1/-1}.pub-scholar-reader .pub-reader-layout{grid-template-columns:1fr}.pub-scholar-reader .pub-reader-toc{position:relative;top:auto;max-height:420px}.pub-scholar-chapter-list{max-height:300px}.pub-selection-assistant{grid-template-columns:1fr auto}.pub-selection-assistant [data-pub-selection-clear]{display:none}.pub-reader-bottom-nav{grid-template-columns:1fr}.pub-reader-finished{grid-column:1}}
  `;
  document.head.append(style);
}
