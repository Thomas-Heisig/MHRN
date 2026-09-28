// Guided controls share the existing Playground form and API contract.
const $ = (id) => document.getElementById(id);
const escape = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const groups = [
  [
    "Modell & Netzwerk",
    "Zellen, Verbindungen und zeitliche Dynamik",
    [1, 2, 3, 15],
  ],
  ["Lauf & Stimulus", "Eingabe, Seed und Ausführung festlegen", [4, 7]],
  ["PAN-Kern", "Hyperzustand, Geometrie und Feedback", [5, 6]],
  [
    "Lernen & Closed Loop",
    "Kanäle, Aktionen, Ziele und Kredit-Zuweisung",
    [8, 10, 11, 12, 13, 14],
  ],
  ["Anwendung", "Körperhaltung, Reward-Ereignisse und Episoden", [20, 21, 22]],
  [
    "Operationen",
    "Neural I/O, Live-Monitor, CUDA und Nachtlauf",
    [9, 17, 18, 19],
  ],
];
const channelFields = [
  "pg-input-amplitudes",
  "pg-input-frequencies",
  "pg-input-phases",
];
const limits = [
  [0, 500, 0],
  [1, 200, 20],
  [0, Math.PI * 2, 0],
];
const help = {
  "pg-pan-feedback-threshold":
    "Schwelle für das konfigurierte Feedback-Routing. Zusammen mit Quelle, Nichtlinearität und Sättigung betrachten.",
  "pg-inhibitory-fraction":
    "Anteil inhibitorischer Neuronen. Ohne GABA-Stärke entsteht daraus keine inhibitorische Wirkung.",
  "pg-gaba-strength":
    "Stärke der inhibitorischen Kopplung; 0 deaktiviert deren Wirkung.",
  "pg-behavior-epsilon":
    "Explorationswahrscheinlichkeit: 0 nutzt die bevorzugte Aktion, 1 exploriert immer.",
  "pg-seed":
    "Ein fester Seed macht gleiche CPU-Konfigurationen reproduzierbar. Modell- und Hardware-Parität separat prüfen.",
  "pg-action-to-input-map":
    "auto erzeugt die Zuordnung im Backend. Alternativ eine JSON-Matrix mit einer Zeile je Aktion eingeben.",
  "pg-threshold-variance":
    "Streuung der Neuronenschwellen. 0 lässt alle Schwellen identisch.",
  "pg-tau-m-variance":
    "Streuung der Membranzeitkonstanten. Mit identischem Seed gegen 0 vergleichen.",
};

export function initGuidedWorkspace({
  payload,
  presets,
  applyPreset,
  setValue,
  lastResult,
}) {
  const root = $("playground-builder");
  if (!root || root.dataset.guided) return;
  root.dataset.guided = "true";
  const style = document.createElement("style");
  style.textContent = `
    #playground-run .playground-analysis-card{min-width:0}#playground-run .playground-analysis-card pre{max-width:100%;overflow:auto}
    .pg-page-intro{padding:18px 0 12px;border-bottom:1px solid var(--rule);margin-bottom:16px}.pg-page-intro h2{font-size:1.35rem;margin:0 0 6px}.pg-page-intro p{color:var(--ink-3);max-width:75ch;line-height:1.5}
    .pg-group{margin:12px 0;border:1px solid var(--rule-2);border-radius:8px;background:var(--paper-2);overflow:hidden}.pg-group>summary{padding:16px;cursor:pointer;font-size:1rem;font-weight:650}.pg-group>summary small{display:block;font-size:.75rem;font-weight:400;color:var(--ink-3);margin:5px 0 0 18px}.pg-group-body{padding:0 12px 12px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.pg-group-body>*{min-width:0}.pg-group-body>.playground-card{border-top:1px solid var(--rule)}.pg-group-body>.pg-wide{grid-column:1/-1}.pg-section-reset{float:right;font-size:.65rem;padding:3px 7px}
    #tab-playground button{cursor:pointer}#tab-playground button:disabled{opacity:.5;cursor:not-allowed}#tab-playground :focus-visible{outline:2px solid var(--accent);outline-offset:3px}
    .pg-tools{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}.pg-tools button,.pg-page-intro button{min-height:36px;padding:7px 12px}.pg-preset-grid{max-height:360px;overflow:auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin:12px 0}.pg-preset-card{border:1px solid var(--rule);border-radius:6px;padding:14px;background:var(--paper-2);display:flex;flex-direction:column;gap:8px}.pg-preset-card h4,.pg-preset-card p{margin:0}.pg-preset-card p{font-size:.78rem;line-height:1.45}.pg-preset-card small{color:var(--ink-3)}.pg-preset-card button{margin-top:auto;align-self:start}.pg-preset-card[hidden]{display:none}
    .pg-channel-wrap{grid-column:1/-1;overflow:auto}.pg-channel-table{width:100%;border-collapse:collapse;font-size:.8rem}.pg-channel-table th,.pg-channel-table td{padding:8px;border-bottom:1px solid var(--rule);text-align:left}.pg-channel-table input{width:100%;min-width:75px}.pg-channel-table td:nth-child(2) input{min-width:160px}.pg-validation{margin:12px 0;font-size:.8rem;line-height:1.6}.pg-validation a{color:var(--crimson)}.pg-warning{color:var(--amber);padding:4px 0}.pg-field-error{display:block;color:var(--crimson);font-size:.7rem;grid-column:1/-1}[aria-invalid=true]{outline:2px solid var(--crimson)!important}.pg-help{display:block;font-size:.68rem;line-height:1.4;color:var(--ink-3);grid-column:1/-1}
    .pg-run-empty{padding:36px;border:1px dashed var(--rule-3);text-align:center;color:var(--ink-3)}.pg-config-preview{max-height:320px;overflow:auto;white-space:pre-wrap;font-size:.75rem}.pg-search{width:100%;max-width:460px;padding:10px;margin:10px 0}.pg-summary{padding:12px;border-left:3px solid var(--accent);background:var(--paper-2);line-height:1.6;font-size:.8rem}.pg-raw{margin:12px 0}.pg-raw>summary{cursor:pointer;padding:8px;font-size:.8rem}
    @media(max-width:850px){.pg-group-body{grid-template-columns:1fr}.pg-preset-grid{grid-template-columns:1fr}.pg-group>summary{font-size:.9rem}.pg-tools button{min-height:44px}.pg-live-monitor-body{overflow:auto;max-height:75vh}.pg-live-monitor-params{overflow:auto}.playground-session{flex-wrap:wrap}}
  `;
  document.head.append(style);
  const intro = (id, title, description) => {
    const node = document.createElement("header");
    node.className = "pg-page-intro";
    node.innerHTML = `<h2>${title}</h2><p>${description}</p>`;
    $(id).prepend(node);
    return node;
  };
  intro(
    "playground-builder",
    "Experiment aufbauen",
    "1 · Startpunkt wählen. 2 · Parameter prüfen. 3 · CPU, CUDA-Membran oder CUDA-PAN-Zustand wählen und den Lauf starten.",
  );
  intro(
    "playground-run",
    "Lauf & Auswertung",
    "Aktivität, Netzwerk und Lernmechanismen gemeinsam betrachten. Die Diagramme zeigen den zuletzt ausgeführten oder geladenen Playground-Lauf.",
  );
  intro(
    "playground-sessions",
    "Gespeicherte Sessions",
    "Persistierte Läufe vom lokalen Server öffnen und deren Ergebnisse vergleichen. Browser-Presets und Server-Sessions sind getrennte Speicher.",
  );
  intro(
    "playground-catalog",
    "Bausteine & Fähigkeiten",
    "Modelle, Topologien, Lernregeln und Schnittstellen erkunden. Ein Eintrag öffnet die Erklärung und den Implementierungsstatus.",
  );
  const cards = new Map();
  root.querySelectorAll("h3").forEach((h) => {
    const n = Number(h.textContent.match(/^(\d+) ·/)?.[1]);
    if (n) cards.set(n, h.parentElement);
  });
  const container = document.createElement("div");
  container.id = "pg-groups";
  root.querySelector(".playground-grid").before(container);
  root.querySelectorAll("input[type=number][step]").forEach((e) => {
    if (e.step.includes(".")) e.step = "any";
  });
  const defaults = new Map();
  const controls = () =>
    [...root.querySelectorAll("input[id],select[id],textarea[id]")].filter(
      (e) =>
        (e.id === "pg-user-preset-select" || !e.id.startsWith("pg-user-")) &&
        !e.id.startsWith("pg-workspace-"),
    );
  const snapshot = () =>
    Object.fromEntries(
      controls().map((e) => [
        e.id,
        e.type === "checkbox" ? e.checked : e.value,
      ]),
    );
  groups.forEach(([title, description, numbers], index) => {
    const group = document.createElement("details");
    group.className = "pg-group";
    group.id = `pg-group-${index}`;
    group.open = index === 0;
    group.innerHTML = `<summary>${String.fromCharCode(65 + index)} · ${title}<small>${description}</small></summary><div class="pg-group-body"></div>`;
    container.append(group);
    numbers.forEach((n, position) => {
      const card = cards.get(n);
      if (!card) return;
      const heading = card.querySelector("h3");
      heading.textContent = heading.textContent.replace(
        /^\d+ ·/,
        `${String.fromCharCode(65 + index)}${position + 1} ·`,
      );
      if (n >= 17) card.classList.add("pg-wide");
      const button = document.createElement("button");
      button.type = "button";
      button.className = "pg-section-reset";
      button.textContent = "Zurücksetzen";
      button.title = "Auf Werte des Startprofils zurücksetzen";
      button.onclick = () => {
        card
          .querySelectorAll("input[id],select[id],textarea[id]")
          .forEach((e) => {
            if (defaults.has(e.id)) {
              if (e.type === "checkbox") e.checked = defaults.get(e.id);
              else e.value = defaults.get(e.id);
            }
          });
        refresh();
        remember();
      };
      heading.append(button);
      group.lastElementChild.append(card);
    });
  });
  root.querySelectorAll(".playground-grid").forEach((e) => {
    if (!e.children.length) e.remove();
  });
  const tools = document.createElement("div");
  tools.className = "pg-tools";
  tools.innerHTML = `<button type="button" id="pg-workspace-expand">Alle öffnen</button><button type="button" id="pg-workspace-collapse">Alle schließen</button><button type="button" id="pg-workspace-undo" disabled>Änderung rückgängig</button><button type="button" id="pg-workspace-export">Konfiguration exportieren</button><button type="button" id="pg-workspace-import">JSON importieren</button><input type="file" id="pg-workspace-file" accept=".json,application/json" hidden>`;
  container.before(tools);
  const message = document.createElement("div");
  message.id = "pg-workspace-message";
  message.setAttribute("role", "status");
  tools.after(message);
  const validation = document.createElement("div");
  validation.id = "pg-validation";
  validation.className = "pg-validation";
  validation.setAttribute("aria-live", "polite");
  container.before(validation);
  const summary = document.createElement("div");
  summary.id = "pg-workspace-summary";
  summary.className = "pg-summary";
  container.before(summary);
  $("pg-workspace-expand").onclick = () =>
    container.querySelectorAll("details").forEach((e) => (e.open = true));
  $("pg-workspace-collapse").onclick = () =>
    container.querySelectorAll("details").forEach((e) => (e.open = false));
  const history = [];
  function remember() {
    const current = snapshot();
    if (JSON.stringify(current) !== JSON.stringify(history.at(-1))) {
      history.push(current);
      if (history.length > 30) history.shift();
    }
    $("pg-workspace-undo").disabled = history.length < 2;
  }
  $("pg-workspace-undo").onclick = () => {
    history.pop();
    Object.entries(history.at(-1) || {}).forEach(([id, v]) => {
      if ($(id).type === "checkbox") $(id).checked = v;
      else $(id).value = v;
    });
    refresh();
    $("pg-workspace-undo").disabled = history.length < 2;
  };
  const download = (data, name) => {
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  $("pg-workspace-export").onclick = () => {
    try {
      if (!validate())
        throw Error("Bitte zuerst die markierten Felder korrigieren.");
      download(
        {
          schema: "mhrn-playground-config-v1",
          settings: payload(),
          controls: snapshot(),
        },
        "playground-config.json",
      );
      message.textContent =
        "Konfiguration exportiert. Eigene Presets liegen nur im Browser-Speicher dieses Profils.";
    } catch (e) {
      message.textContent = e.message;
    }
  };
  $("pg-workspace-import").onclick = () => $("pg-workspace-file").click();
  $("pg-workspace-file").onchange = async (event) => {
    try {
      const file = event.target.files[0];
      if (!file) return;
      if (file.size > 1000000) throw Error("Datei ist größer als 1 MB.");
      const data = JSON.parse(await file.text());
      if (
        data.schema !== "mhrn-playground-config-v1" ||
        !data.settings ||
        typeof data.settings !== "object" ||
        Array.isArray(data.settings)
      )
        throw Error("Eine exportierte Playground-Konfiguration auswählen.");
      const allowed = new Set(Object.keys(payload()));
      const entries = Object.entries(data.settings);
      if (
        entries.some(
          ([k, v]) =>
            !allowed.has(k) ||
            v === null ||
            (!["number", "boolean", "string"].includes(typeof v) &&
              !Array.isArray(v)),
        )
      )
        throw Error(
          "Unbekannte Felder oder ungültige Werte in der Konfiguration.",
        );
      if (
        data.settings.closed_loop_preset &&
        [...$("pg-user-preset-select").options].some(
          (o) => o.value === data.settings.closed_loop_preset,
        )
      )
        $("pg-user-preset-select").value = data.settings.closed_loop_preset;
      if (data.controls) {
        const known = new Map(controls().map((e) => [e.id, e]));
        if (
          Object.entries(data.controls).some(
            ([id, v]) =>
              !known.has(id) ||
              typeof v !==
                (known.get(id).type === "checkbox" ? "boolean" : "string"),
          )
        )
          throw Error("Ungültige Formularfelder im Export.");
        Object.entries(data.controls).forEach(([id, v]) => {
          const e = known.get(id);
          if (e.type === "checkbox") e.checked = v;
          else e.value = v;
        });
      } else {
        entries.forEach(([k, v]) => setValue(k, v));
      }
      refresh();
      remember();
      message.textContent =
        "Konfiguration importiert. Hinweise und Validierung vor dem Start prüfen.";
    } catch (e) {
      message.textContent = `Import fehlgeschlagen: ${e.message}`;
    } finally {
      event.target.value = "";
    }
  };

  const presetBox = document.createElement("details");
  presetBox.open = true;
  presetBox.className = "pg-raw";
  presetBox.innerHTML =
    '<summary>Preset-Katalog erkunden & vergleichen</summary><input class="pg-search" id="pg-workspace-preset-search" aria-label="Presets durchsuchen" placeholder="Preset suchen …"><div class="pg-preset-grid" id="pg-preset-grid"></div><pre class="pg-config-preview" id="pg-workspace-comparison" aria-live="polite"></pre>';
  root.querySelector(".playground-preset-deck").after(presetBox);
  const storageNote = document.createElement("p");
  storageNote.className = "pg-help";
  storageNote.textContent =
    "Integrierte und Katalog-Presets kommen aus dieser Serverversion. Eigene Presets werden im localStorage dieses Browserprofils gespeichert. Exportierte JSON-Dateien können auf einem anderen Gerät importiert werden.";
  presetBox.before(storageNote);
  function renderPresets() {
    const all = presets();
    $("pg-preset-grid").innerHTML = Object.entries(all)
      .map(
        ([name, p]) =>
          `<article class="pg-preset-card" data-name="${escape(name)}"><h4>${escape(p.label || name)}</h4><small>${p.source === "catalog" ? "Server-Katalog" : p.saved_at ? "Browser · eigenes Preset" : "Integriert"}</small><p>${escape(p.description)}</p>${p.expected_success != null ? `<small>Hypothese: ${escape(p.expected_success)} Erfolgsanteil · kein Messergebnis</small>` : ""}<button type="button" data-apply="${escape(name)}">Anwenden</button><button type="button" data-compare="${escape(name)}">Mit aktueller Konfiguration vergleichen</button></article>`,
      )
      .join("");
    $("pg-preset-grid")
      .querySelectorAll("[data-apply]")
      .forEach(
        (b) =>
          (b.onclick = () => {
            $("pg-user-preset-select").value = b.dataset.apply;
            applyPreset();
            refresh();
            remember();
          }),
      );
    $("pg-preset-grid")
      .querySelectorAll("[data-compare]")
      .forEach(
        (b) =>
          (b.onclick = () => {
            try {
              const current = payload(),
                settings = all[b.dataset.compare].settings || {};
              $("pg-workspace-comparison").textContent =
                Object.entries(settings)
                  .filter(
                    ([k, v]) =>
                      JSON.stringify(v) !== JSON.stringify(current[k]),
                  )
                  .map(
                    ([k, v]) =>
                      `${k}\n  Aktuell: ${JSON.stringify(current[k])}\n  Preset:  ${JSON.stringify(v)}`,
                  )
                  .join("\n\n") || "Keine abweichenden Einstellungen.";
            } catch (e) {
              message.textContent = e.message;
            }
          }),
      );
  }
  $("pg-workspace-preset-search").oninput = (e) => {
    $("pg-preset-grid")
      .querySelectorAll("article")
      .forEach(
        (card) =>
          (card.hidden = !card.textContent
            .toLowerCase()
            .includes(e.target.value.toLowerCase())),
      );
  };
  const raw = document.createElement("details");
  raw.className = "pg-raw";
  raw.innerHTML = "<summary>Erweitert: Kanalwerte als JSON</summary>";
  const channelCard = $("pg-input-amplitudes").closest("article");
  channelCard.append(raw);
  ["pg-input-channel-map", ...channelFields].forEach((id) =>
    raw.append($(id).closest("label")),
  );
  const table = document.createElement("div");
  table.className = "pg-channel-wrap";
  table.innerHTML =
    '<p class="pg-help">Automatische Neuronenzuordnung bleibt im Backend. Eigene IDs kommagetrennt eingeben. Leere Werte verwenden die Runtime-Defaults: 0 / 20 Hz / 0 rad; kurze Listen werden zyklisch wiederholt.</p><table class="pg-channel-table"><thead><tr><th>Kanal</th><th>Neuronen</th><th>Amplitude</th><th>Hz</th><th>Phase (rad)</th></tr></thead><tbody id="pg-channel-rows"></tbody></table><div class="pg-tools"><button type="button" id="pg-channel-frequency-up">Alle Frequenzen +2 Hz</button><button type="button" id="pg-channel-auto">Neuronenzuordnung automatisch</button></div>';
  raw.before(table);
  const arrays = () =>
    ["pg-input-channel-map", ...channelFields].map((id) => {
      const v = JSON.parse($(id).value);
      if (!Array.isArray(v)) throw Error(`${id}: JSON-Liste erwartet.`);
      return v;
    });
  function renderChannels() {
    try {
      const [map, ...vectors] = arrays();
      const n = Number($("pg-input-channels").value);
      if (!Number.isInteger(n) || n < 1 || n > 64) return;
      $("pg-channel-rows").innerHTML = Array.from(
        { length: n },
        (_, i) =>
          `<tr><th scope="row">${i}</th><td><input id="pg-workspace-channel-map-${i}" aria-label="Kanal ${i} Neuronen" data-channel="${i}" data-column="map" value="${escape(map[i]?.join(", ") || "")}" placeholder="Automatisch · ${escape($("pg-input-topology").value)}"></td>${vectors.map((v, j) => `<td><input id="pg-workspace-channel-${i}-${j}" type="number" required step="any" min="${limits[j][0]}" max="${limits[j][1]}" aria-label="Kanal ${i} ${["Amplitude", "Frequenz", "Phase"][j]}" data-channel="${i}" data-column="${j}" value="${escape(v.length ? v[i % v.length] : limits[j][2])}"></td>`).join("")}</tr>`,
      ).join("");
    } catch {
      /* Raw JSON errors are displayed by validation. */
    }
  }
  table.addEventListener("input", (e) => {
    const input = e.target;
    if (!input.dataset.channel) return;
    const i = Number(input.dataset.channel),
      col = input.dataset.column,
      n = Number($("pg-input-channels").value);
    try {
      const [map, ...vectors] = arrays();
      if (col === "map") {
        if (
          input.value.trim() &&
          !/^\d+(\s*,\s*\d+)*$/.test(input.value.trim())
        ) {
          input.setCustomValidity(
            "IDs als kommagetrennte ganze Zahlen eingeben.",
          );
          return;
        }
        input.setCustomValidity("");
        while (map.length < n) map.push([]);
        map[i] = input.value.trim() ? input.value.split(",").map(Number) : [];
        $("pg-input-channel-map").value = JSON.stringify(map);
      } else {
        const j = Number(col),
          old = vectors[j];
        const values = Array.from({ length: n }, (_, k) =>
          old.length ? old[k % old.length] : limits[j][2],
        );
        if (input.value !== "" && Number.isFinite(input.valueAsNumber)) {
          values[i] = input.valueAsNumber;
          $(channelFields[j]).value = JSON.stringify(values);
        }
      }
    } catch (e) {
      message.textContent = e.message;
    }
  });
  $("pg-channel-frequency-up").onclick = () => {
    try {
      const v = arrays()[2],
        n = Number($("pg-input-channels").value);
      $("pg-input-frequencies").value = JSON.stringify(
        Array.from({ length: n }, (_, i) =>
          Math.min(200, (v.length ? v[i % v.length] : 20) + 2),
        ),
      );
      refresh();
      remember();
    } catch (e) {
      message.textContent = e.message;
    }
  };
  $("pg-channel-auto").onclick = () => {
    $("pg-input-channel-map").value = "[]";
    refresh();
    remember();
  };
  for (const [id, text] of Object.entries(help)) {
    const field = $(id);
    if (field) {
      const note = document.createElement("small");
      note.className = "pg-help";
      note.id = `${id}-help`;
      note.textContent = text;
      field.closest("label").append(note);
      field.setAttribute("aria-describedby", note.id);
    }
  }

  function validate() {
    const errors = [],
      warnings = [];
    root
      .querySelectorAll("[aria-invalid]")
      .forEach((e) => e.removeAttribute("aria-invalid"));
    root.querySelectorAll(".pg-field-error").forEach((e) => e.remove());
    root.querySelectorAll("input[type=number]").forEach((e) => {
      e.setAttribute(
        "aria-invalid",
        String(
          !e.validity.valid ||
            e.value === "" ||
            !Number.isFinite(e.valueAsNumber),
        ),
      );
      if (e.getAttribute("aria-invalid") === "true")
        errors.push([
          e.id,
          e.getAttribute("aria-label") ||
            e.closest("label")?.firstChild?.textContent ||
            "Kanalwert",
          e.validationMessage || "Eine endliche Zahl eingeben.",
        ]);
    });
    root.querySelectorAll("[data-column=map]").forEach((e) => {
      if (!e.validity.valid)
        errors.push([e.id, "Neuronenzuordnung", e.validationMessage]);
    });
    const value = (id) => Number($(id)?.value),
      enabled = (id) => $(id)?.checked;
    try {
      const [map, ...vectors] = arrays(),
        n = value("pg-input-channels");
      vectors.forEach((v, j) => {
        if (
          v.length > n ||
          v.some(
            (x) =>
              typeof x !== "number" ||
              !Number.isFinite(x) ||
              x < limits[j][0] ||
              x > limits[j][1],
          )
        )
          errors.push([
            channelFields[j],
            "Input-Kanäle",
            `Maximal ${n} Werte im Bereich ${limits[j][0]} bis ${limits[j][1]}.`,
          ]);
      });
      if (
        map.length > n ||
        map.some(
          (row) =>
            !Array.isArray(row) ||
            row.some(
              (x) => !Number.isInteger(x) || x < 0 || x >= value("pg-neurons"),
            ),
        )
      )
        errors.push([
          "pg-input-channel-map",
          "Neuronenzuordnung",
          "Nur gültige Neuronen-IDs und maximal eine Gruppe je Kanal verwenden.",
        ]);
      if (map.length)
        warnings.push(
          "Eigene Neuronenzuordnung aktiv: leere Zeilen enthalten keine Neuronen. Mit ‚automatisch‘ zur Topologie-Zuordnung zurückkehren.",
        );
    } catch (e) {
      errors.push(["pg-input-amplitudes", "Input-Kanäle", e.message]);
    }
    for (const id of [
      "pg-target-cue-channel",
      "pg-reward-cue-channel",
      "pg-reward-channel",
      "pg-action-feedback-channel",
      "pg-posture-score-channel",
      "pg-reward-event-channel",
    ]) {
      if (value(id) >= value("pg-input-channels"))
        errors.push([
          id,
          "Kanalzuordnung",
          `Kanal muss kleiner als ${value("pg-input-channels")} sein.`,
        ]);
    }
    if (enabled("pg-posture-reward-enabled") && !enabled("pg-sandbox-enabled"))
      warnings.push(
        "Posture Reward ist aktiv, aber die Stick-Figure Sandbox ist nicht gekoppelt.",
      );
    if (value("pg-inhibitory-fraction") > 0 && value("pg-gaba-strength") === 0)
      warnings.push(
        "Inhibitorischer Anteil ohne GABA-Stärke: die inhibitorische Kopplung bleibt wirkungslos.",
      );
    if (
      enabled("pg-action-loop-enabled") &&
      !$("pg-action-to-input-map").value.trim()
    )
      errors.push([
        "pg-action-to-input-map",
        "Aktions-Loop",
        "auto oder eine gültige Action → Input Map eingeben.",
      ]);
    if (
      enabled("pg-reward-enabled") &&
      $("pg-target-encoding").value !== "none" &&
      value("pg-target-cue-channel") === value("pg-reward-channel")
    )
      warnings.push(
        "Ziel und Reward verwenden denselben Kanal. Signale können sich überlagern.",
      );
    if (
      enabled("pg-action-loop-enabled") &&
      $("pg-target-encoding").value !== "none" &&
      value("pg-action-feedback-channel") === value("pg-target-cue-channel")
    )
      warnings.push("Action-Feedback und Ziel-Cue verwenden denselben Kanal.");
    if (value("pg-execution-low") >= value("pg-execution-high"))
      errors.push([
        "pg-execution-low",
        "PAN Runtime",
        "θ low muss kleiner als θ high sein.",
      ]);
    if (!errors.length) {
      try {
        payload();
      } catch (e) {
        errors.push(["pg-action-to-input-map", "Konfiguration", e.message]);
      }
    }
    errors.forEach(([id, , text]) => {
      const field = $(id);
      if (field) {
        field.setAttribute("aria-invalid", "true");
        const note = document.createElement("small");
        note.className = "pg-field-error";
        note.textContent = text;
        field.after(note);
      }
    });
    validation.innerHTML =
      errors
        .map(
          ([id, label, text]) =>
            `<div><a href="#${id}">${escape(label)}: ${escape(text)}</a></div>`,
        )
        .join("") +
      warnings
        .map((text) => `<div class="pg-warning">Hinweis: ${escape(text)}</div>`)
        .join("");
    for (const id of ["pg-run", "pg-robustness", "pg-user-preset-save"]) {
      if ($(id)) $(id).disabled = errors.length > 0;
    }
    summary.textContent = `${value("pg-neurons")} Neuronen · ${value("pg-edges")} Kanten · ${value("pg-ticks")} Ticks · Seed ${$("pg-seed").value} · ${$("pg-neuron-backend")?.value === "cuda_pan" ? "CUDA-Membran + PAN-Zustand" : $("pg-neuron-backend")?.value === "cuda_membrane" ? "CUDA-Membran / CPU-PAN" : "CPU-Referenz"}. ${errors.length ? `${errors.length} Eingabefehler.` : "Eingaben geprüft."} Laufzeit: noch keine belastbare Messung für diese Konfiguration. CUDA-PAN führt auch PAN-Zustand, Feedback und synaptische Regeln auf der GPU aus. Körper, Policy und Delay-Queue bleiben CPU; die Ergebnistabelle zeigt die tatsächlichen Komponenten.`;
    return errors.length === 0;
  }
  validation.onclick = (e) => {
    const a = e.target.closest("a");
    if (a) {
      e.preventDefault();
      const target = $(a.hash.slice(1));
      for (
        let parent = target?.parentElement;
        parent;
        parent = parent.parentElement
      )
        if (parent.tagName === "DETAILS") parent.open = true;
      target?.focus();
    }
  };
  function refresh() {
    renderChannels();
    validate();
  }
  root.addEventListener("input", validate);
  root.addEventListener(
    "click",
    (e) => {
      if (
        e.target.closest(
          "#pg-run,#pg-robustness,#pg-live-open,#pg-night-start,#pg-cpu-determinism,#pg-cuda-compile,#pg-cuda-preflight,#pg-cuda-smoke,#pg-cuda-rng",
        ) &&
        !validate()
      ) {
        e.preventDefault();
        e.stopImmediatePropagation();
        validation.scrollIntoView({ block: "center" });
      }
    },
    true,
  );
  root.addEventListener("change", (e) => {
    if (
      [
        "pg-input-channels",
        "pg-input-topology",
        "pg-neurons",
        ...channelFields,
        "pg-input-channel-map",
      ].includes(e.target.id)
    ) {
      if (e.target.id === "pg-input-channels") {
        const n = Number(e.target.value);
        if (Number.isInteger(n) && n >= 1 && n <= 64) {
          try {
            ["pg-input-channel-map", ...channelFields].forEach(
              (id) =>
                ($(id).value = JSON.stringify(
                  JSON.parse($(id).value).slice(0, n),
                )),
            );
          } catch {}
        }
      }
      refresh();
    }
    remember();
  });
  root.addEventListener("click", (e) => {
    if (
      e.target.closest(
        "#pg-user-preset-apply,#pg-reset,#pg-user-preset-save,#pg-user-preset-delete",
      )
    ) {
      refresh();
      renderPresets();
      remember();
    }
  });
  $("pg-user-preset-select").addEventListener("change", () => {
    refresh();
    remember();
  });
  controls().forEach((e) =>
    defaults.set(e.id, e.type === "checkbox" ? e.checked : e.value),
  );
  renderPresets();
  refresh();
  remember();

  for (const id of [
    "pg-run-json",
    "pg-cuda-stage-state",
    "pg-cuda-resource-state",
    "pg-cuda-parity-state",
    "pg-cuda-rng-state",
    "pg-cuda-compiler-state",
  ]) {
    const node = $(id);
    if (!node) continue;
    const detail = document.createElement("details");
    detail.className = "pg-raw";
    detail.innerHTML = "<summary>Technische Details / JSON</summary>";
    node.before(detail);
    detail.append(node);
    if (id.startsWith("pg-cuda-")) {
      const status = document.createElement("p");
      status.className = "pg-summary";
      status.setAttribute("role", "status");
      detail.before(status);
      const update = () => {
        try {
          const data = JSON.parse(node.textContent);
          if ("passed" in data)
            status.textContent = `${data.passed ? "Bestanden" : "Nicht bestanden"}${data.parity ? ` · D2-Abweichung ${data.parity.current_max_abs_error ?? "nicht bestimmbar"} · Wiederholung ${data.gpu_repeat_exact ? "identisch" : "abweichend"}` : ""}${data.samples ? ` · ${data.samples} RNG-Aktionen` : ""}`;
          else if ("ptxas_available" in data)
            status.textContent = `ptxas ${data.ptxas_available ? "verfügbar" : "fehlt"} · Treiber ${data.cuda_driver_available ? "verfügbar" : "fehlt"}. Hardware-Nachweis nur durch einen aktuellen Smoke-Test.`;
          else if (data.ptxas)
            status.textContent = `Register ${data.ptxas.registers ?? "—"} · Spill Store/Load ${data.ptxas.spill_store_bytes ?? "—"}/${data.ptxas.spill_load_bytes ?? "—"} Byte${"ready_for_cooperative_launch" in data ? ` · Preflight ${data.ready_for_cooperative_launch ? "bereit" : "nicht bereit"}` : ""}`;
          else if (data.manifest)
            status.textContent =
              "Gate-IR und PTX erzeugt. Nächster Schritt: ptxas + Occupancy.";
          else
            status.textContent =
              "Diagnose verfügbar – technische Details öffnen.";
        } catch {
          status.textContent = node.textContent;
        }
      };
      new MutationObserver(update).observe(node, { childList: true });
      update();
    }
  }
  const runSummary = document.createElement("div");
  runSummary.id = "pg-result-summary";
  runSummary.className = "pg-run-empty";
  runSummary.textContent =
    "Noch kein Lauf. Im Builder ein Preset wählen und starten oder eine gespeicherte Session öffnen.";
  $("pg-metrics").before(runSummary);
  const backendTable = document.createElement("table");
  backendTable.id = "pg-backend-components";
  backendTable.hidden = true;
  runSummary.after(backendTable);
  const resultPanels = [
    ...$("playground-run").querySelectorAll(
      ".playground-metrics,.playground-viz-grid,.playground-analysis-grid",
    ),
  ];
  resultPanels.forEach((panel) => (panel.hidden = true));
  new MutationObserver(() => {
    const r = lastResult();
    resultPanels.forEach((panel) => (panel.hidden = !r?.monitors));
    if (r) {
      backendTable.replaceChildren();
      backendTable.hidden = !r.execution?.components;
      if (r.execution?.components) {
        const caption = document.createElement("caption");
        caption.textContent =
          "Tatsächliche Ausführung dieses Laufs · hybrider Playground, kein vollständiges CUDA-MHRN";
        backendTable.append(caption);
        for (const [component, backend] of Object.entries(
          r.execution.components,
        )) {
          const row = document.createElement("tr"),
            label = document.createElement("th"),
            value = document.createElement("td");
          label.textContent = component.replaceAll("_", " ");
          value.textContent = backend === "cuda" ? "GPU (CUDA)" : "CPU";
          row.append(label, value);
          backendTable.append(row);
        }
      }
      runSummary.className = "pg-summary";
      runSummary.textContent = !r.session_id
        ? "Robustheitskontrollen abgeschlossen. Ergebnisse stehen in den technischen Details und im Export bereit."
        : `Session ${r.session_id || "—"} · Seed ${r.config?.seed ?? "—"} · ${r.execution?.neuron_backend === "cuda_pan" ? "CUDA-Membran + PAN-Zustand" : r.execution?.neuron_backend === "cuda_membrane" ? "CUDA-Membran / CPU-PAN" : "CPU-Referenz"} · ${r.metrics?.total_spikes ?? 0} Spikes · explorativer Lauf, keine wissenschaftliche Evidenz.`;
      if (r.cue_decoding?.status === "DESCRIPTIVE_ONLY") {
        runSummary.textContent += ` Aktivitaetsdecoder: ${(r.cue_decoding.accuracy * 100).toFixed(1)} % auf ${r.cue_decoding.test_episodes} Testepisoden; ${r.cue_decoding.input_cue_control || "aligned"}. Kein Nachweis eines neuronalen Lernvorteils.`;
      }
      if (r.behavioral_learning) {
        const learning = r.behavioral_learning;
        const contexts = Object.keys(learning.context_policies || {}).length;
        runSummary.textContent += ` Lernen: ${contexts} Reiz-Kontexte · ${learning.policy_updates || 0} Updates · ${((learning.success_fraction || 0) * 100).toFixed(1)} % Erfolg bei bewerteten Aktionen.`;
        if (r.closed_loop?.policy_context_source) {
          runSummary.textContent +=
            " Kontext aus ausgesendetem Zielreiz; kein Nachweis neuronaler Reizdekodierung.";
        }
      }
    }
  }).observe($("pg-run-json"), { childList: true });
  const runTools = document.createElement("div");
  runTools.className = "pg-tools";
  runTools.innerHTML =
    '<button type="button" id="pg-result-export">Letzten Lauf exportieren</button>';
  runSummary.after(runTools);
  $("pg-result-export").onclick = () => {
    const r = lastResult();
    if (r) download(r, "playground-result.json");
    else
      runSummary.textContent =
        "Zuerst einen Lauf ausführen oder eine Session laden.";
  };
  for (const [id, target, selector, placeholder] of [
    [
      "pg-workspace-session-search",
      "pg-session-list",
      "article",
      "Sessions durchsuchen …",
    ],
    [
      "pg-workspace-catalog-search",
      "pg-catalog-grid",
      "article",
      "Bausteine durchsuchen …",
    ],
  ]) {
    const search = document.createElement("input");
    search.id = id;
    search.className = "pg-search";
    search.placeholder = placeholder;
    search.setAttribute("aria-label", placeholder);
    $(target).before(search);
    const filter = () =>
      $(target)
        .querySelectorAll(selector)
        .forEach(
          (e) =>
            (e.hidden = !e.textContent
              .toLowerCase()
              .includes(search.value.toLowerCase())),
        );
    search.oninput = filter;
    new MutationObserver(filter).observe($(target), { childList: true });
  }
}
