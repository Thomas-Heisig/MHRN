"use strict";

import { enhancePublicationScholarReader } from "./publication-scholar-tools.js";

let rootDataPromise = null;

export function initPublicationScholarTools() {
  const container = document.getElementById("publication-panel");
  if (!container || container.dataset.scholarBootstrap === "true") return;
  container.dataset.scholarBootstrap = "true";

  const loadRootData = () => {
    if (!rootDataPromise) {
      rootDataPromise = fetch("/api/publication/current", { headers: { Accept: "application/json" }, cache: "no-store" })
        .then((response) => {
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          return response.json();
        })
        .catch(() => null);
    }
    return rootDataPromise;
  };

  const openDocument = (reference) => {
    if (!reference?.path || !["research", "docs"].includes(reference.source)) return;
    const proxy = document.createElement("a");
    proxy.href = "#";
    proxy.hidden = true;
    proxy.dataset.pubReaderLink = reference.path;
    proxy.dataset.pubSource = reference.source;
    if (reference.anchor) proxy.dataset.pubTargetAnchor = reference.anchor;
    proxy.textContent = reference.label || reference.path;
    container.append(proxy);
    proxy.click();
    proxy.remove();
  };

  const enhance = async () => {
    const reader = container.querySelector(".publication-reader");
    const article = container.querySelector("#pub-reader-article");
    if (!reader || !article || reader.dataset.scholarEnhanced === "true") return;
    reader.dataset.scholarEnhanced = "true";
    const rootData = await loadRootData();
    if (!reader.isConnected || !article.isConnected) return;
    enhancePublicationScholarReader(container, {
      rootData,
      view: {
        source: article.dataset.source || "research",
        path: article.dataset.path || "publications/README.md",
      },
      openDocument,
    });
  };

  const observer = new MutationObserver(() => queueMicrotask(enhance));
  observer.observe(container, { childList: true, subtree: true });
  queueMicrotask(enhance);

  // Fix the publication -> canonical File Viewer bridge in capture phase.
  // The original reader referenced window.selectRoute, while the router's public
  // contract is window.MHRNWorkspaceArchitecture.selectRoute.
  container.addEventListener("click", async (event) => {
    const button = event.target.closest('[data-pub-action="open-file"]');
    if (!button) return;
    const article = container.querySelector("#pub-reader-article");
    if (!article) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    const source = article.dataset.source || "research";
    const path = article.dataset.path;
    if (!path) return;
    const popupToggle = document.getElementById("fm-popup-toggle");
    const popupPreferred = popupToggle ? popupToggle.checked : localStorage.getItem("mhrn-fm-popup") !== "false";
    if (!popupPreferred) {
      window.MHRNWorkspaceArchitecture?.selectRoute?.("files", "browse");
      await new Promise((resolve) => requestAnimationFrame(resolve));
    }
    if (typeof window.openBrain5DFile === "function") await window.openBrain5DFile(source, path);
    else document.dispatchEvent(new CustomEvent("brain5d:open-file", { detail: { source, path } }));
  }, true);

  // Selected dissertation text -> existing Research Chat. No second AI surface.
  document.addEventListener("brain5d:ask-ai", (event) => {
    const prompt = String(event.detail?.prompt || "").trim();
    if (!prompt) return;
    const input = document.getElementById("research-chat-input");
    const form = document.getElementById("research-chat-form");
    const toggle = document.getElementById("chat-toggle");
    if (!input || !form || !toggle) return;
    const modal = document.getElementById("research-chat");
    if (modal?.hidden) toggle.click();
    input.value = prompt;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.focus();
    form.requestSubmit();
  });
}
