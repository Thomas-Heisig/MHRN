"use strict";

const VOICE_STORAGE_KEY = "mhrn.speech.voices.v2";
const RATE_STORAGE_KEY = "mhrn.speech.rate.v2";
const NATURAL_NAMES = {
  de: ["katja", "conrad", "amala", "bernd", "christa", "detlef", "elke", "fiona"],
  en: ["jenny", "aria", "guy", "ryan", "sonia", "davis", "amber", "ashley", "emma", "brian", "christopher", "eric", "jacob", "nancy", "sara"],
  fr: ["henri", "charlotte", "remi", "josephine"],
  es: ["elvira", "dalia", "alvaro", "marisol"],
  it: ["diego", "isabella", "imelda", "cosimo"],
};

const NATURAL_KEYWORDS = /natural|neural|online|premium|enhanced|wavenet|studio|ultra/i;

let activeSession = null;

function supported() {
  return typeof window !== "undefined" && "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;
}

export function cleanSpeechText(value) {
  return String(value || "")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/https?:\/\/\S+/g, "")
    .replace(/[#*_`~]+/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function splitSpeechText(value, limit = 260) {
  const text = cleanSpeechText(value);
  if (!text) return [];
  const sentences = text.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [text];
  const chunks = [];
  let current = "";
  for (const sentence of sentences) {
    const candidate = `${current} ${sentence}`.trim();
    if (current && candidate.length > limit) {
      chunks.push(current);
      current = sentence.trim();
    } else {
      current = candidate;
    }
  }
  if (current) chunks.push(current);
  return chunks.flatMap((chunk) => {
    if (chunk.length <= limit) return [chunk];
    const words = chunk.split(/\s+/);
    const result = [];
    let part = "";
    for (const word of words) {
      const candidate = `${part} ${word}`.trim();
      if (part && candidate.length > limit) {
        result.push(part);
        part = word;
      } else {
        part = candidate;
      }
    }
    if (part) result.push(part);
    return result;
  });
}

function baseLang(lang) {
  const l = String(lang || "de-DE").toLowerCase();
  if (l.startsWith("en")) return "en";
  if (l.startsWith("fr")) return "fr";
  if (l.startsWith("es")) return "es";
  if (l.startsWith("it")) return "it";
  return "de";
}

export function detectSpeechLanguage(value, fallback = "de-DE") {
  const text = ` ${cleanSpeechText(value).toLowerCase()} `;
  if (!text.trim()) return fallback;
  const english = [" the ", " and ", " of ", " to ", " in ", " is ", " are ", " with ", " this ", " that ", " from ", " results ", " discussion ", " abstract "];
  const german = [" der ", " die ", " das ", " und ", " von ", " zu ", " ist ", " sind ", " mit ", " diese ", " dass ", " aus ", " ergebnisse ", " diskussion ", " zusammenfassung "];
  const score = (terms) => terms.reduce((sum, term) => sum + (text.includes(term) ? 1 : 0), 0);
  const englishScore = score(english);
  const germanScore = score(german);
  if (englishScore > germanScore + 1) return "en-US";
  if (germanScore > englishScore) return "de-DE";
  return fallback;
}

function getStoredPreferences() {
  try {
    return JSON.parse(localStorage.getItem(VOICE_STORAGE_KEY) || "{}") || {};
  } catch (_) {
    return {};
  }
}

function saveStoredPreference(lang, name) {
  const preferences = getStoredPreferences();
  preferences[baseLang(lang)] = name || "";
  try { localStorage.setItem(VOICE_STORAGE_KEY, JSON.stringify(preferences)); } catch (_) {}
}

function getStoredRate() {
  const value = Number(localStorage.getItem(RATE_STORAGE_KEY));
  return Number.isFinite(value) && value >= 0.6 && value <= 1.5 ? value : 0.96;
}

function saveStoredRate(value) {
  try { localStorage.setItem(RATE_STORAGE_KEY, String(value)); } catch (_) {}
}

export function listSpeechVoices(lang = "") {
  if (!supported()) return [];
  const voices = window.speechSynthesis.getVoices() || [];
  if (!lang) return [...voices];
  const wanted = baseLang(lang);
  return voices.filter((voice) => baseLang(voice.lang) === wanted);
}

function voiceScore(voice, lang) {
  const wanted = baseLang(lang);
  const name = String(voice.name || "").toLowerCase();
  const voiceLang = String(voice.lang || "").toLowerCase();
  let score = 0;
  if (baseLang(voiceLang) === wanted) score += 100;
  if (voiceLang === String(lang || "").toLowerCase()) score += 25;
  if (NATURAL_KEYWORDS.test(name)) score += 60;
  if (NATURAL_NAMES[wanted]?.some((candidate) => name.includes(candidate))) score += 55;
  if (/microsoft/.test(name)) score += 22;
  if (/google/.test(name)) score += 18;
  if (/apple|siri/.test(name)) score += 15;
  if (/amazon|alexa/.test(name)) score += 14;
  if (voice.default) score += 8;
  if (voice.localService) score += 4;
  return score;
}

export function chooseSpeechVoice(lang = "de-DE", preferredName = "") {
  const voices = listSpeechVoices(lang);
  if (!voices.length) return null;
  const stored = preferredName || getStoredPreferences()[baseLang(lang)] || "";
  if (stored) {
    const exact = voices.find((voice) => voice.name === stored);
    if (exact) return exact;
  }
  return [...voices].sort((left, right) => voiceScore(right, lang) - voiceScore(left, lang))[0] || null;
}

function normalizeSegments(value, fallbackLang = "de-DE") {
  const source = Array.isArray(value) ? value : [{ text: value }];
  const normalized = [];
  source.forEach((segment, segmentIndex) => {
    const text = typeof segment === "string" ? segment : segment?.text;
    const clean = cleanSpeechText(text);
    if (!clean) return;
    const lang = segment?.lang || detectSpeechLanguage(clean, fallbackLang);
    splitSpeechText(clean).forEach((chunk, chunkIndex) => normalized.push({
      text: chunk,
      lang,
      element: segment?.element || null,
      segmentIndex,
      chunkIndex,
      metadata: segment?.metadata || null,
    }));
  });
  return normalized;
}

export function stopSpeech() {
  if (!supported()) return;
  window.speechSynthesis.cancel();
  if (activeSession) activeSession.onState("stopped");
  activeSession = null;
}

export function pauseSpeech() {
  if (!supported() || !activeSession) return false;
  window.speechSynthesis.pause();
  activeSession.onState("paused");
  return true;
}

export function resumeSpeech() {
  if (!supported() || !activeSession) return false;
  window.speechSynthesis.resume();
  activeSession.onState("speaking");
  return true;
}

export function speakSegments(value, {
  onState = () => {},
  onSegment = () => {},
  lang = "de-DE",
  rate = getStoredRate(),
  preferredVoices = {},
} = {}) {
  if (!supported()) {
    onState("unsupported");
    return false;
  }
  const segments = normalizeSegments(value, lang);
  if (!segments.length) {
    onState("empty");
    return false;
  }
  stopSpeech();
  const session = { segments, index: 0, onState, onSegment, rate };
  activeSession = session;

  const speakNext = () => {
    if (activeSession !== session) return;
    if (session.index >= session.segments.length) {
      activeSession = null;
      session.onState("done");
      return;
    }
    const segment = session.segments[session.index++];
    const utterance = new SpeechSynthesisUtterance(segment.text);
    utterance.lang = segment.lang;
    utterance.rate = rate;
    utterance.pitch = 1;
    const voice = chooseSpeechVoice(segment.lang, preferredVoices[baseLang(segment.lang)] || "");
    if (voice) utterance.voice = voice;
    utterance.onstart = () => {
      session.onSegment(segment, session.index - 1, session.segments.length);
      session.onState("speaking");
    };
    utterance.onend = speakNext;
    utterance.onerror = (event) => {
      if (event.error === "interrupted" || event.error === "canceled") return;
      if (activeSession === session) {
        activeSession = null;
        session.onState("error");
      }
    };
    window.speechSynthesis.speak(utterance);
  };
  speakNext();
  return true;
}

export function speakText(value, { onState = () => {}, lang = "de-DE", rate = getStoredRate(), onSegment = () => {} } = {}) {
  return speakSegments([{ text: value, lang }], { onState, onSegment, lang, rate });
}

function voiceOptionMarkup(lang, selectedName) {
  const voices = listSpeechVoices(lang).sort((left, right) => voiceScore(right, lang) - voiceScore(left, lang));
  if (!voices.length) return '<option value="">Keine passende Stimme gefunden</option>';
  return voices.map((voice) => {
    const quality = NATURAL_KEYWORDS.test(voice.name) || NATURAL_NAMES[baseLang(lang)]?.some((name) => voice.name.toLowerCase().includes(name)) ? " ★" : "";
    return `<option value="${escapeAttribute(voice.name)}"${voice.name === selectedName ? " selected" : ""}>${escapeText(voice.name)} · ${escapeText(voice.lang)}${quality}</option>`;
  }).join("");
}

function escapeText(value) {
  const node = document.createElement("span");
  node.textContent = String(value || "");
  return node.innerHTML;
}

function escapeAttribute(value) {
  return escapeText(value).replace(/"/g, "&quot;");
}

export function createSpeechControls(mount, getText, {
  label = "Text vorlesen",
  includeStart = true,
  getSegments = null,
  onSegment = () => {},
  showVoiceOptions = false,
  lang = "de-DE",
} = {}) {
  const controls = document.createElement("div");
  controls.className = "speech-reader-controls";
  controls.setAttribute("role", "group");
  controls.setAttribute("aria-label", label);
  controls.innerHTML = `${includeStart ? `<button type="button" class="speech-reader-start" title="${label}">▶ Vorlesen</button>` : ""}
    <button type="button" class="speech-reader-pause" title="Vorlesen pausieren" disabled>Pause</button>
    <button type="button" class="speech-reader-stop" title="Vorlesen anhalten" disabled>Stopp</button>
    ${showVoiceOptions ? `<details class="speech-reader-options"><summary>Stimmen</summary><div class="speech-reader-options-panel">
      <label>Deutsch<select class="speech-reader-voice" data-speech-lang="de-DE"></select></label>
      <label>English<select class="speech-reader-voice" data-speech-lang="en-US"></select></label>
      <label>Français<select class="speech-reader-voice" data-speech-lang="fr-FR"></select></label>
      <label>Español<select class="speech-reader-voice" data-speech-lang="es-ES"></select></label>
      <label>Italiano<select class="speech-reader-voice" data-speech-lang="it-IT"></select></label>
      <label>Tempo<input class="speech-reader-rate" type="range" min="0.7" max="1.25" step="0.05" value="${getStoredRate()}"><output>${getStoredRate().toFixed(2)}×</output></label>
      <small>★ bevorzugt natürliche/neuronale Systemstimmen. Unter Windows werden insbesondere Katja/Conrad/Amala/Bernd (DE), Jenny/Aria/Guy/Ryan/Davis/Amber/Emma/Brian (EN), Henri/Charlotte (FR), Elvira/Alvaro (ES) und Diego/Isabella (IT) priorisiert.</small>
    </div></details>` : ""}
    <span class="speech-reader-status" role="status" aria-live="polite"></span>`;
  mount.append(controls);
  const start = controls.querySelector(".speech-reader-start");
  const pause = controls.querySelector(".speech-reader-pause");
  const stop = controls.querySelector(".speech-reader-stop");
  const status = controls.querySelector(".speech-reader-status");
  const rateInput = controls.querySelector(".speech-reader-rate");
  let paused = false;

  const selectedVoices = getStoredPreferences();
  const populateVoices = () => {
    controls.querySelectorAll(".speech-reader-voice").forEach((select) => {
      const speechLang = select.dataset.speechLang;
      const chosen = selectedVoices[baseLang(speechLang)] || chooseSpeechVoice(speechLang)?.name || "";
      select.innerHTML = voiceOptionMarkup(speechLang, chosen);
      if (chosen) select.value = chosen;
    });
  };
  populateVoices();
  if (supported() && "onvoiceschanged" in window.speechSynthesis) {
    window.speechSynthesis.addEventListener?.("voiceschanged", populateVoices, { once: true });
  }

  const setState = (state) => {
    const active = state === "speaking" || state === "paused";
    pause.disabled = !active;
    stop.disabled = !active;
    if (state === "speaking") { status.textContent = "Liest vor"; pause.textContent = "Pause"; paused = false; }
    if (state === "paused") { status.textContent = "Pausiert"; pause.textContent = "Weiter"; paused = true; }
    if (state === "done") { status.textContent = "Fertig"; pause.textContent = "Pause"; paused = false; }
    if (state === "stopped") { status.textContent = "Angehalten"; pause.textContent = "Pause"; paused = false; }
    if (state === "empty") status.textContent = "Kein lesbarer Text";
    if (state === "unsupported") status.textContent = "Vorlesen wird hier nicht unterstützt";
    if (state === "error") status.textContent = "Vorlesen konnte nicht gestartet werden";
  };

  const startReading = () => {
    const payload = typeof getSegments === "function" ? getSegments() : getText();
    const rate = Number(rateInput?.value || getStoredRate());
    return speakSegments(payload, { onState: setState, onSegment, lang, rate, preferredVoices: selectedVoices });
  };
  start?.addEventListener("click", startReading);
  pause.addEventListener("click", () => {
    if (!supported()) return;
    if (paused) resumeSpeech();
    else pauseSpeech();
  });
  stop.addEventListener("click", stopSpeech);
  controls.querySelectorAll(".speech-reader-voice").forEach((select) => {
    select.addEventListener("change", () => {
      const key = baseLang(select.dataset.speechLang);
      selectedVoices[key] = select.value;
      saveStoredPreference(select.dataset.speechLang, select.value);
    });
  });
  rateInput?.addEventListener("input", () => {
    const rate = Number(rateInput.value);
    rateInput.nextElementSibling.textContent = `${rate.toFixed(2)}×`;
    saveStoredRate(rate);
  });
  if (!supported() && start) start.disabled = true;
  return { start: startReading, stop: stopSpeech, element: controls };
}
