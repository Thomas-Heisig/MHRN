"use strict";

import { enhancePublicationScholarReader } from "./publication-scholar-tools.js";

let rootDataPromise = null;

const WINDOWS_VOICE_HINTS = {
  de: ["katja", "conrad", "heda", "stefan"],
  en: ["jenny", "aria", "guy", "ryan", "sonia", "zira", "david", "mark"],
};

function speechBaseLang(lang) {
  return String(lang || "").toLowerCase().startsWith("en") ? "en" : "de";
}

function voiceBelongsToLanguage(voice, lang) {
  const wanted = speechBaseLang(lang);
  const voiceLang = String(voice?.lang || "").toLowerCase();
  const name = String(voice?.name || "").toLowerCase();
  if (voiceLang.startsWith(`${wanted}-`) || voiceLang === wanted) return true;
  return WINDOWS_VOICE_HINTS[wanted].some((hint) => name.includes(hint));
}

function voiceRank(voice, lang) {
  const name = String(voice?.name || "").toLowerCase();
  const voiceLang = String(voice?.lang || "").toLowerCase();
  const wanted = speechBaseLang(lang);
  let score = 0;
  if (voiceLang.startsWith(`${wanted}-`) || voiceLang === wanted) score += 100;
  if (/microsoft/.test(name)) score += 70;
  if (/natural|neural|online/.test(name)) score += 80;
  if (WINDOWS_VOICE_HINTS[wanted].some((hint) => name.includes(hint))) score += 65;
  if (voice?.default) score += 10;
  if (voice?.localService) score += 4;
  return score;
}

function refreshPublicationVoiceSelectors(reader) {
  if (!reader || !("speechSynthesis" in window)) return;
  const allVoices = [...(window.speechSynthesis.getVoices?.() || [])];
  if (!allVoices.length) return;

  reader.querySelectorAll(".speech-reader-voice").forEach((select) => {
    const lang = select.dataset.speechLang || "de-DE";
    const previous = select.value;
    const voices = allVoices
      .filter((voice) => voiceBelongsToLanguage(voice, lang))
      .sort((left, right) => voiceRank(right, lang) - voiceRank(left, lang) || String(left.name).localeCompare(String(right.name)));
    if (!voices.length) return;

    select.replaceChildren(...voices.map((voice) => {
      const option = document.createElement("option");
      option.value = voice.name;
      const name = String(voice.name || "Systemstimme");
      const quality = /natural|neural|online/i.test(name) || /microsoft/i.test(name) ? " ★" : "";
      option.textContent = `${name} · ${voice.lang || "System"}${quality}`;
      return option;
    }));

    if (previous && voices.some((voice) => voice.name === previous)) select.value = previous;
  });
}

function installVoiceRefresh(reader) {
  if (!reader || reader.dataset.voiceRefreshInstalled === "true") return;
  reader.dataset.voiceRefreshInstalled = "true";

  const panel = reader.querySelector(".speech-reader-options-panel");
  if (panel && !panel.querySelector("[data-speech-refresh]")) {
    const refresh = document.createElement("button");
    refresh.type = "button";
    refresh.className = "speech-reader-refresh";
    refresh.dataset.speechRefresh = "true";
    refresh.textContent = "Stimmen neu laden";
    refresh.title = "System- und Microsoft-Stimmen erneut aus Windows/Chromium einlesen";
    refresh.addEventListener("click", () => refreshPublicationVoiceSelectors(reader));
    panel.append(refresh);
  }

  refreshPublicationVoiceSelectors(reader);
  [180, 700, 1800, 3500].forEach((delay) => {
    window.setTimeout(() => {
      if (reader.isConnected) refreshPublicationVoiceSelectors(reader);
    }, delay);
  });

  const synth = window.speechSynthesis;
  if (typeof synth?.addEventListener === "function") {
    const listener = () => {
      if (!reader.isConnected) {
        synth.removeEventListener("voiceschanged", listener);
        return;
      }
      refreshPublicationVoiceSelectors(reader);
    };
    synth.addEventListener("voiceschanged", listener);
  }
}

export function initPublicationScholarTools() {
  const container = document.getElementById("publication-panel");
  if (!container || container.dataset.scholarBootstrap === "true") return;
  container.dataset.scholarBootstrap = "true";

  const loadRootData = () => {
    if (!rootDataPromise) {
      rootDataPromise = fetch("/api/publication/current", {
        headers: { Accept: "application/json" },
        cache: "no-cache",
      })
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

  let enhanceScheduled = false;
  let lastReader = null;

  const consolidateSpeechControls = (reader) => {
    const canonicalMount = reader.querySelector("#pub-reader-speech-mount");
    const enhancedMount = reader.querySelector(".pub-scholar-speech");
    const enhancedControls = enhancedMount?.querySelector(".speech-reader-controls");
    if (!canonicalMount || !enhancedControls) return;

    canonicalMount.replaceChildren(enhancedControls);
    enhancedMount.remove();
    installVoiceRefresh(reader);
  };

  const enhance = async () => {
    enhanceScheduled = false;
    const reader = container.querySelector(".publication-reader");
    const article = container.querySelector("#pub-reader-article");
    if (!reader || !article || reader === lastReader || reader.dataset.scholarEnhanced === "true") return;

    reader.dataset.scholarEnhanced = "loading";
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
    consolidateSpeechControls(reader);
    reader.dataset.scholarEnhanced = "true";
    lastReader = reader;
  };

  const scheduleEnhance = () => {
    if (enhanceScheduled) return;
    enhanceScheduled = true;
    requestAnimationFrame(() => void enhance());
  };

  const observer = new MutationObserver(scheduleEnhance);
  observer.observe(container, { childList: true });
  scheduleEnhance();

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
