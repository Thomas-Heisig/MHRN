"use strict";

const RAW_MARKUP_PATTERN = /(<!--[\s\S]*?-->|<a\s+(?:id|name)\s*=\s*["']([^"']+)["']\s*>\s*<\/a>)/gi;

export function initPublicationReaderPolish() {
  const panel = document.getElementById("publication-panel");
  if (!panel || panel.dataset.readerPolishInitialised === "true") return;
  panel.dataset.readerPolishInitialised = "true";

  let activeReader = null;
  let readerObserver = null;
  let scheduled = false;

  const polish = () => {
    scheduled = false;
    const reader = panel.querySelector(".publication-reader");
    const article = panel.querySelector("#pub-reader-article");
    if (!reader || !article) return;

    normalizeReaderMarkup(article);
    relocateSelectionAssistant(panel, reader);

    if (reader === activeReader) return;
    activeReader = reader;
    readerObserver?.disconnect();

    readerObserver = new MutationObserver(() => {
      normalizeReaderMarkup(article);
      if (relocateSelectionAssistant(panel, reader)) readerObserver?.disconnect();
    });
    readerObserver.observe(reader, { childList: true, subtree: true });

    window.setTimeout(() => readerObserver?.disconnect(), 10000);
  };

  const schedule = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(polish);
  };

  const observer = new MutationObserver(schedule);
  observer.observe(panel, { childList: true });
  schedule();
}

export function normalizeReaderMarkup(article) {
  if (!article) return 0;
  const walker = document.createTreeWalker(article, NodeFilter.SHOW_TEXT);
  const candidates = [];

  while (walker.nextNode()) {
    const node = walker.currentNode;
    const parent = node.parentElement;
    if (!parent || parent.closest("pre, code, script, style, textarea, mjx-container")) continue;
    RAW_MARKUP_PATTERN.lastIndex = 0;
    if (RAW_MARKUP_PATTERN.test(node.nodeValue || "")) candidates.push(node);
  }

  let replacements = 0;
  for (const node of candidates) {
    const source = node.nodeValue || "";
    RAW_MARKUP_PATTERN.lastIndex = 0;
    let cursor = 0;
    let match;
    const fragment = document.createDocumentFragment();

    while ((match = RAW_MARKUP_PATTERN.exec(source))) {
      if (match.index > cursor) fragment.append(document.createTextNode(source.slice(cursor, match.index)));
      const token = match[0];
      if (!token.startsWith("<!--")) {
        const rawId = match[2] || "";
        const slug = slugify(rawId);
        if (slug) {
          const anchor = document.createElement("span");
          anchor.className = "pub-explicit-anchor";
          anchor.id = rawId;
          anchor.dataset.pubHeading = "explicit-anchor";
          anchor.dataset.pubSlug = slug;
          anchor.dataset.pubExplicitAnchor = rawId;
          anchor.setAttribute("aria-hidden", "true");
          fragment.append(anchor);
          replacements += 1;
        }
      } else {
        replacements += 1;
      }
      cursor = match.index + token.length;
    }

    if (cursor < source.length) fragment.append(document.createTextNode(source.slice(cursor)));
    node.replaceWith(fragment);
  }

  article.querySelectorAll("p").forEach((paragraph) => {
    const meaningfulText = (paragraph.textContent || "").trim();
    const anchors = [...paragraph.children].filter((child) => child.classList.contains("pub-explicit-anchor"));
    if (!meaningfulText && anchors.length && anchors.length === paragraph.children.length) {
      paragraph.replaceWith(...anchors);
    } else if (!meaningfulText && !paragraph.children.length) {
      paragraph.remove();
    }
  });

  return replacements;
}

function relocateSelectionAssistant(panel, reader) {
  const assistant = reader.querySelector(":scope > .pub-selection-assistant");
  if (!assistant) return false;
  panel.append(assistant);
  assistant.dataset.floatingSelectionAssistant = "true";
  return true;
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
