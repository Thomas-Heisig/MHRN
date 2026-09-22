"use strict";

const STORAGE_KEY = "mhrn-ui-language-v1";
const DEFAULT_LANGUAGE = "en";
const SUPPORTED_LANGUAGES = Object.freeze(["en", "de"]);
const TRANSLATABLE_ATTRIBUTES = Object.freeze(["title", "aria-label", "placeholder"]);

const STRINGS = Object.freeze({
  "language.label": { en: "Language", de: "Sprache" },
  "language.english": { en: "English", de: "Englisch" },
  "language.german": { en: "German", de: "Deutsch" },
  "publication.translation.original": { en: "Original language: German", de: "Originalsprache: Deutsch" },
  "publication.translation.assisted": {
    en: "English scientific translation · AI-assisted · pending human language review",
    de: "Englische wissenschaftliche Übersetzung · KI-unterstützt · menschliche Sprachprüfung ausstehend",
  },
  "publication.translation.source": {
    en: "Scientific claims, identifiers, citations, DATA/EVID status and source references are unchanged by translation.",
    de: "Wissenschaftliche Aussagen, Kennungen, Zitationen, DATA/EVID-Status und Quellenverweise werden durch die Übersetzung nicht verändert.",
  },
});

const PHRASE_PAIRS = Object.freeze([
  ["Mehrskaliges homöostatisches Rekurrenznetzwerk", "Multi-Scale Homeostatic Recurrence Network"],
  ["Wissenschaftliche Hauptarbeit", "Scientific Main Work"],
  ["Aktuelle Fassung der wissenschaftlichen Abhandlung", "Current edition of the scientific treatise"],
  ["Wissenschaftliche Arbeit", "Scientific Work"],
  ["Wissenschaftliche Grenze", "Scientific Boundary"],
  ["Wissenschaftliche Aussagegrenze", "Scientific Claim Boundary"],
  ["Wissenschaftliche Infrastruktur", "Scientific Infrastructure"],
  ["Wissenschaftliche Reife", "Scientific Maturity"],
  ["Wissenschaftliche Timeline", "Scientific Timeline"],
  ["Technische Timeline", "Engineering Timeline"],
  ["Forschungsfrage & Hypothese", "Research Question & Hypothesis"],
  ["Frage & Hypothese", "Question & Hypothesis"],
  ["Wähle die Forschungsfrage, die dazugehörige Hypothese und den wissenschaftlichen Kontext.", "Select the research question, its associated hypothesis, and the scientific context."],
  ["Versuchsplan & Research Contract", "Experimental Plan & Research Contract"],
  ["Definiere Protokoll, Seeds, Ticks, Bedingungen, Titel und reproduzierbare Randbedingungen.", "Define protocol, seeds, ticks, conditions, title, and reproducible boundary conditions."],
  ["Kontrollierte Ausführung", "Controlled Execution"],
  ["Starte Einzel- oder Batchläufe und beobachte ausschließlich den aktuellen Ausführungszustand.", "Start single or batch runs and observe only the current execution state."],
  ["Läufe, Reihen & Archiv", "Runs, Series & Archive"],
  ["Ordne aktive Experimente, Experimentreihen und archivierte Versuche in zeitlicher Reihenfolge.", "Organize active experiments, experiment series, and archived runs chronologically."],
  ["Ergebnisse & Artefakte", "Results & Artifacts"],
  ["Öffne Bericht, Summary, Statistik und Rohdaten des zuletzt abgeschlossenen Laufs.", "Open the report, summary, statistics, and raw data of the most recently completed run."],
  ["Review, Interpretation & Evidenzgrenze", "Review, Interpretation & Evidence Boundary"],
  ["Human Review, neue Forschungsfragen und Evidenzgrenzen bleiben von Rohdaten und AI-Interpretation getrennt.", "Human review, new research questions, and evidence boundaries remain separate from raw data and AI interpretation."],
  ["Experiment-Labor Schritte", "Experiment Lab Steps"],
  ["Experiment-Labor", "Experiment Lab"],
  ["Experimentablauf", "Experiment Workflow"],
  ["Die zentrale Arbeitsfläche für registrierte, reproduzierbare Experimente – in der tatsächlichen Reihenfolge des wissenschaftlichen Ablaufs.", "The central workspace for registered, reproducible experiments — ordered by the actual scientific workflow."],
  ["Vom Forschungsziel bis zur überprüften Evidenz – ohne vermischte Arbeitsflächen.", "From research objective to reviewed evidence — without mixed work surfaces."],
  ["Quelle", "Source"],
  ["Grenze", "Boundary"],
  ["Frage", "Question"],
  ["Fragen", "Questions"],
  ["Hypothese", "Hypothesis"],
  ["Versuchsplan", "Experimental Plan"],
  ["Ausführen", "Execute"],
  ["Ausführung", "Execution"],
  ["Läufe & Reihen", "Runs & Series"],
  ["Ergebnisse", "Results"],
  ["Review & Evidenz", "Review & Evidence"],
  ["Evidenz & Analyse", "Evidence & Analysis"],
  ["Messung, Experiment, Analyse, Registry und Dateien mit expliziter Evidenzgrenze.", "Measurement, experiments, analysis, registry, and files with an explicit evidence boundary."],
  ["Observatory für Messwerte und UNKNOWN-Zustände nutzen.", "Use Observatory for measurements and UNKNOWN states."],
  ["Kausale Aussagen nur aus registrierten kontrollierten Läufen ableiten.", "Derive causal claims only from registered controlled runs."],
  ["Dateien immer im zentralen File Viewer öffnen.", "Always open files in the central File Viewer."],
  ["Wissenschaft", "Science"],
  ["Experimente", "Experiments"],
  ["Netzwerk", "Network"],
  ["Dynamik", "Dynamics"],
  ["Inspektor", "Inspector"],
  ["Daten", "Data"],
  ["Übersicht", "Overview"],
  ["Publikation", "Publication"],
  ["Einfach erklärt", "Plain-language Guide"],
  ["Impressum & Rechtliches", "Legal Notice & Privacy"],
  ["Projektidentität · Rechtliches", "Project Identity · Legal"],
  ["Projektidentität", "Project Identity"],
  ["Rechtliche Hinweise", "Legal Information"],
  ["Inhalt", "Contents"],
  ["Abschnitte", "Sections"],
  ["Kapitel", "Chapters"],
  ["Anhänge & Register", "Appendices & Registers"],
  ["Editionen", "Editions"],
  ["Aktuelle Arbeitsfassung", "Current Working Edition"],
  ["Vorgänger", "Predecessor"],
  ["Gesamtmanuskript", "Full Manuscript"],
  ["Im File Viewer", "Open in File Viewer"],
  ["Im File Viewer öffnen", "Open in File Viewer"],
  ["Drucken", "Print"],
  ["Aktualisieren", "Refresh"],
  ["Erneut laden", "Reload"],
  ["Zurück", "Back"],
  ["Vorwärts", "Forward"],
  ["Zum Publikationsindex", "To Publication Index"],
  ["Dokumentnavigation", "Document Navigation"],
  ["Lesewerkzeuge", "Reading Tools"],
  ["Im Dokument suchen", "Search Document"],
  ["Vorheriger Treffer", "Previous Match"],
  ["Nächster Treffer", "Next Match"],
  ["Keine Überschriften erkannt.", "No headings detected."],
  ["Verknüpftes Dokument", "Linked Document"],
  ["Pfad kopieren", "Copy Path"],
  ["kopieren", "copy"],
  ["Pfad kopiert.", "Path copied."],
  ["Wörter", "words"],
  ["ca.", "approx."],
  ["Publikationsmetadaten", "Publication Metadata"],
  ["Publikation wird geladen", "Loading publication"],
  ["Reader, Verweise und Dokumentstruktur werden vorbereitet.", "Preparing reader, references, and document structure."],
  ["Publikation konnte nicht geladen werden", "Publication could not be loaded"],
  ["Publikationsinhalt fehlt in der API-Antwort.", "Publication content is missing from the API response."],
  ["Wissenschaftliche Publikation", "Scientific Publication"],
  ["Lade aktuelle Publikation", "Loading current publication"],
  ["Lade einfache Erklärung", "Loading plain-language guide"],
  ["Lade Impressum & Rechtliches", "Loading legal notice & privacy"],
  ["Forschungsbericht", "Research Report"],
  ["Exporte", "Exports"],
  ["Status", "Status"],
  ["System & Betrieb", "System & Operations"],
  ["Kompakte Betriebsübersicht ohne doppelte Detailansichten.", "Compact operational overview without duplicated detail views."],
  ["Systemzustand & Steuerung", "System State & Control"],
  ["Organe", "Organs"],
  ["Gedächtnis", "Memory"],
  ["Struktur", "Structure"],
  ["Aktivität und Regulation", "Activity and Regulation"],
  ["Aktive Neuronen", "Active Neurons"],
  ["Stille Neuronen", "Silent Neurons"],
  ["Feuerrate", "Firing Rate"],
  ["Synchronität", "Synchrony"],
  ["Aufmerksamkeit", "Attention"],
  ["Lebende Komponenten", "Live Components"],
  ["Gedächtnis des Systems", "System Memory"],
  ["Plastizität", "Plasticity"],
  ["Wachstum und Umbau", "Growth and Remodeling"],
  ["Aktueller Snapshot", "Current Snapshot"],
  ["Dateiinhalt", "File content"],
  ["Datei", "File"],
  ["Größe", "Size"],
  ["Netzwerk-Visualisierung", "Network Visualization"],
  ["5D Netzwerk-Projektion", "5D Network Projection"],
  ["Echtzeit-5D-Projektion aus Live-Runtime oder Snapshot.", "Real-time 5D projection from live runtime or snapshot."],
  ["Gewichte", "Weights"],
  ["Auflösung", "Resolution"],
  ["Keine Live-Verbindung.", "No live connection."],
  ["Eingang / Ausgang", "Input / Output"],
  ["Input-Output Fluss", "Input-Output Flow"],
  ["Gemessene Input- und Output-Raten des Netzwerks.", "Measured network input and output rates."],
  ["Neuronale Populationen", "Neural Populations"],
  ["Verteilung und E/I-Verhältnis der aktiven Neuronen.", "Distribution and E/I ratio of active neurons."],
  ["Spike-Muster", "Spike Patterns"],
  ["Zeitliche Abfolge der Spikes über alle Neuronen.", "Temporal sequence of spikes across all neurons."],
  ["Feuerraten-Histogramm", "Firing-rate Histogram"],
  ["Verteilung der mittleren Feuerraten über alle Neuronen.", "Distribution of mean firing rates across all neurons."],
  ["Netzwerk-Analyse", "Network Analysis"],
  ["Detaillierte Einblicke in Netzwerk-Topologie und Zustand.", "Detailed views of network topology and state."],
  ["Alle Neuronen mit aktuellen Zustandswerten.", "All neurons with current state values."],
  ["Hilfe zur aktuellen Ansicht", "Help for current view"],
  ["Hilfe", "Help"],
  ["Kontrastmodus", "Contrast Mode"],
  ["Größere Bedienelemente", "Larger Controls"],
  ["Barrierearme Darstellung", "Accessible Display"],
  ["Research Chat öffnen", "Open Research Chat"],
  ["Zur vorherigen Ansicht", "Back to previous view"],
  ["Zur Übersicht", "Go to overview"],
  ["Benachrichtigungen", "Notifications"],
  ["Bereit · keine Ereignisse", "Ready · no events"],
  ["bereit", "ready"],
  ["kein Lauf", "no run"],
  ["kein aktueller Signalfluss", "no current signal flow"],
  ["Spracheingabe", "Speech Input"],
  ["Vorlesen", "Read Aloud"],
  ["Senden", "Send"],
  ["Kurz", "Short"],
  ["Ausführlich", "Detailed"],
  ["Wissenschaftlich", "Scientific"],
  ["Chat-Einstellungen", "Chat Settings"],
  ["Verbindung prüfen", "Check Connection"],
  ["Anbieter", "Provider"],
  ["Modell", "Model"],
  ["Lokales Fallback (eingebaut)", "Local fallback (built in)"],
  ["Vision aktivieren", "Enable Vision"],
  ["Tools aktivieren", "Enable Tools"],
  ["Prompts", "Prompts"],
  ["System Prompt", "System Prompt"],
  ["Übergabeprompt", "Handoff Prompt"],
  ["Standardwerte", "Defaults"],
  ["Settings speichern", "Save Settings"],
  ["Zurück zum Chat", "Back to Chat"],
  ["Der Assistent darf lesen und erklären. Ausführung und Änderungen benötigen weiterhin die expliziten System-Workflows.", "The assistant may read and explain. Execution and changes still require the explicit system workflows."],
  ["Der Chat liest Research und Docs. Experimente werden nur über einen bestätigten, strukturierten Workflow ausgeführt.", "The chat reads Research and Docs. Experiments are executed only through a confirmed, structured workflow."],
]);

const DE_TO_EN = [...PHRASE_PAIRS].sort((a, b) => b[0].length - a[0].length);
const EN_TO_DE = [...PHRASE_PAIRS].map(([de, en]) => [en, de]).sort((a, b) => b[0].length - a[0].length);

const textOrigins = new WeakMap();
const attributeOrigins = new WeakMap();
const translationCache = new Map();
let currentLanguage = DEFAULT_LANGUAGE;
let mutating = false;
let observer = null;
let observerFrame = 0;

const OBSERVER_OPTIONS = Object.freeze({
  childList: true,
  subtree: true,
  characterData: true,
  attributes: true,
  attributeFilter: TRANSLATABLE_ATTRIBUTES,
});

function observeBody() {
  if (observer && document.body) observer.observe(document.body, OBSERVER_OPTIONS);
}

function normalizeLanguage(value) {
  return String(value || "").toLowerCase().startsWith("de") ? "de" : "en";
}

function storedLanguage() {
  try {
    const value = localStorage.getItem(STORAGE_KEY);
    if (SUPPORTED_LANGUAGES.includes(value)) return value;
  } catch (_) {}
  return DEFAULT_LANGUAGE;
}

function replacementTable(language) {
  return language === "de" ? EN_TO_DE : DE_TO_EN;
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function replaceWholePhrase(value, from, to) {
  const escaped = escapeRegExp(from);
  const startsWithWord = /^[\\p{L}\\p{N}_]/u.test(from);
  const endsWithWord = /[\\p{L}\\p{N}_]$/u.test(from);
  const prefix = startsWithWord ? "(?<![\\p{L}\\p{N}_])" : "";
  const suffix = endsWithWord ? "(?![\\p{L}\\p{N}_])" : "";
  return value.replace(new RegExp(`${prefix}${escaped}${suffix}`, "gu"), to);
}

function translateFragment(value, language = currentLanguage) {
  const source = String(value ?? "");
  const cacheKey = `${language}\u0000${source}`;
  const cached = translationCache.get(cacheKey);
  if (cached !== undefined) return cached;
  let output = source;
  for (const [from, to] of replacementTable(language)) {
    output = replaceWholePhrase(output, from, to);
  }
  translationCache.set(cacheKey, output);
  return output;
}

function isExcluded(node) {
  const element = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
  return Boolean(element?.closest(
    "script, style, code, pre, textarea, [data-i18n-skip], .project-title, .project-subtitle, #pub-reader-article, .markdown-body, .fm-document-body, .file-content"
  ));
}

function translateTextNode(node) {
  if (!node?.nodeValue || isExcluded(node)) return;
  if (!textOrigins.has(node)) textOrigins.set(node, node.nodeValue);
  const source = textOrigins.get(node);
  const translated = translateFragment(source, currentLanguage);
  if (translated !== node.nodeValue) node.nodeValue = translated;
}

function translateAttributes(element) {
  if (!(element instanceof Element) || isExcluded(element)) return;
  let origins = attributeOrigins.get(element);
  if (!origins) {
    origins = new Map();
    attributeOrigins.set(element, origins);
  }
  for (const name of TRANSLATABLE_ATTRIBUTES) {
    if (!element.hasAttribute(name)) continue;
    if (!origins.has(name)) origins.set(name, element.getAttribute(name));
    const source = origins.get(name);
    const translated = translateFragment(source, currentLanguage);
    if (translated !== element.getAttribute(name)) element.setAttribute(name, translated);
  }
}

function translateTree(root = document.body) {
  if (!root) return;
  mutating = true;
  try {
    if (root.nodeType === Node.TEXT_NODE) {
      translateTextNode(root);
      return;
    }
    if (root instanceof Element) translateAttributes(root);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.nodeType === Node.TEXT_NODE) translateTextNode(node);
      else translateAttributes(node);
    }
  } finally {
    mutating = false;
  }
}

function ensureLanguageSwitch() {
  const host = document.querySelector(".topbar-right");
  if (!host) return null;
  let group = document.getElementById("mhrn-language-switch");
  if (group) return group;

  group = document.createElement("div");
  group.id = "mhrn-language-switch";
  group.className = "mhrn-language-switch";
  group.setAttribute("role", "group");
  group.setAttribute("aria-label", t("language.label"));
  group.innerHTML = `
    <span class="mhrn-language-switch-label" aria-hidden="true">LANG</span>
    <button type="button" data-mhrn-language="en" title="English" aria-label="English">EN</button>
    <button type="button" data-mhrn-language="de" title="Deutsch" aria-label="Deutsch">DE</button>`;

  host.insertBefore(group, host.firstChild);
  group.addEventListener("click", (event) => {
    const button = event.target.closest("[data-mhrn-language]");
    if (!button) return;
    setLanguage(button.dataset.mhrnLanguage);
  });
  return group;
}

function syncLanguageSwitch() {
  const group = ensureLanguageSwitch();
  if (!group) return;
  group.setAttribute("aria-label", t("language.label"));
  group.querySelectorAll("[data-mhrn-language]").forEach((button) => {
    const active = button.dataset.mhrnLanguage === currentLanguage;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
}

export function t(key, fallback = "") {
  const entry = STRINGS[key];
  return entry?.[currentLanguage] ?? entry?.en ?? fallback ?? key;
}

export function getLanguage() {
  return currentLanguage;
}

export function getLocale(language = currentLanguage) {
  return normalizeLanguage(language) === "de" ? "de-DE" : "en-US";
}

export function translateUiText(value, language = currentLanguage) {
  return translateFragment(value, normalizeLanguage(language));
}

export function setLanguage(language, { persist = true, announce = true } = {}) {
  const next = normalizeLanguage(language);
  const changed = next !== currentLanguage;
  currentLanguage = next;
  document.documentElement.lang = next;
  document.body?.setAttribute("data-ui-language", next);

  if (persist) {
    try { localStorage.setItem(STORAGE_KEY, next); } catch (_) {}
  }

  if (changed) {
    const activeObserver = observer;
    activeObserver?.disconnect();
    try {
      translateTree(document.body);
      syncLanguageSwitch();
    } finally {
      if (activeObserver && document.body) observeBody();
    }
  } else {
    syncLanguageSwitch();
  }

  if (changed && announce) {
    document.dispatchEvent(new CustomEvent("mhrn:language-change", {
      detail: { language: next, locale: getLocale(next) },
    }));
  }
  return next;
}

export function initI18n() {
  currentLanguage = storedLanguage();
  document.documentElement.lang = currentLanguage;
  document.body?.setAttribute("data-ui-language", currentLanguage);
  ensureLanguageSwitch();
  translateTree(document.body);
  syncLanguageSwitch();

  if (!observer && document.body) {
    observer = new MutationObserver((records) => {
      if (mutating || observerFrame) return;
      observerFrame = requestAnimationFrame(() => {
        observerFrame = 0;
        if (!observer || mutating) return;
        observer.disconnect();
        try {
          for (const record of records) {
            if (record.type === "characterData") {
              textOrigins.delete(record.target);
              translateTree(record.target);
            } else if (record.type === "attributes") {
              attributeOrigins.delete(record.target);
              translateTree(record.target);
            } else {
              record.addedNodes.forEach((node) => translateTree(node));
            }
          }
        } finally {
          observeBody();
        }
      });
    });
    observeBody();
  }

  window.MHRNI18n = {
    getLanguage,
    getLocale,
    setLanguage,
    t,
    translateUiText,
    defaultLanguage: DEFAULT_LANGUAGE,
    supportedLanguages: [...SUPPORTED_LANGUAGES],
  };

  document.dispatchEvent(new CustomEvent("mhrn:language-ready", {
    detail: { language: currentLanguage, locale: getLocale() },
  }));
}
