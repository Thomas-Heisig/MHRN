"use strict";

const GITHUB = "https://github.com/Thomas-Heisig/MHRN";

function card(title, body) {
  return `<article><h2>${title}</h2>${body}</article>`;
}

export function initPublicationExplainer() {
  const panel = document.getElementById("publication-simple-panel");
  if (!panel || panel.dataset.explainerInitialised === "true") return;
  panel.dataset.explainerInitialised = "true";
  panel.innerHTML = `
    <section class="pub-simple-page" aria-labelledby="pub-simple-title">
      <header class="pub-simple-hero">
        <span class="workspace-kicker">MHRN · EINFACH ERKLÄRT</span>
        <h1 id="pub-simple-title">Was wird hier eigentlich erforscht?</h1>
        <p><strong>Die Oma-Version:</strong> MHRN ist ein Forschungsbaukasten für ein künstliches Nervensystem. Statt nur Antworten eines großen Sprachmodells zu sammeln, wird untersucht, wie ein eigenes spikendes Netzwerk Signale verarbeitet, lernt, erinnert und mit einer Umwelt gekoppelt werden kann.</p>
      </header>
      <div class="pub-simple-grid">
        ${card("1. Was ist MHRN?", "<p>Im Kern besteht MHRN aus künstlichen Neuronen und Synapsen. Viele technische Teile funktionieren bereits; daraus folgt aber nicht automatisch, dass alle wissenschaftlichen Hypothesen bestätigt sind.</p>")}
        ${card("2. Was bedeutet 5D?", "<p>„5D“ bezeichnet zunächst eine Adress- und Geometriestruktur des Netzes. Das Projekt untersucht, ob und wann solche Topologien einen messbaren Unterschied machen. Es wird <strong>keine allgemeine Überlegenheit von 5D</strong> behauptet.</p>")}
        ${card("3. Was bedeuten DATA und EVID?", "<p><strong>DATA</strong> bedeutet: Ein Experiment wurde nachvollziehbar ausgeführt. <strong>EVID</strong> ist eine strengere, geprüfte Evidenzstufe. Tests, Grafiken, ein DOI oder eine Veröffentlichung machen DATA nicht automatisch zu EVID.</p>")}
        ${card("4. Welche Rolle spielt KI?", "<p>KI-Assistenten helfen bei Recherchehinweisen, Gegenargumenten, Textstruktur, Code, Tests und Reviews. Das wird nicht versteckt: <strong>die Zusammenarbeit Mensch–KI ist selbst Teil des methodischen Forschungsgegenstands.</strong> Die KI ist weder Autor noch Beweisinstanz; die menschliche Verantwortung bleibt bei Thomas Heisig.</p>")}
        ${card("5. Was ist noch offen?", "<p>Wichtige Aussagen brauchen weitere Human Reviews, bessere Kontrollen, Prior-Art-Prüfung und vor allem <strong>unabhängige externe Replikation</strong>. Ein eigenes positives Ergebnis entscheidet nicht allein über wissenschaftlichen Wert oder Neuheit.</p>")}
        ${card("6. Warum veröffentlichen?", `<p>Die Veröffentlichung soll die Arbeit prüfbar machen: Quellcode, negative Ergebnisse, Grenzen und Replikationsaufruf werden sichtbar. Externe Forscher dürfen bestätigen, widersprechen oder bessere Erklärungen liefern.</p><p class="pub-simple-links"><a href="${GITHUB}/blob/main/INDEPENDENT_REPLICATION.md" target="_blank" rel="noopener">Aufruf zur unabhängigen Replikation</a> · <a href="${GITHUB}/blob/main/research/CURRENT_SCIENTIFIC_STATE.md" target="_blank" rel="noopener">Aktueller wissenschaftlicher Stand</a></p>`)}
      </div>
      <aside class="pub-simple-boundary"><strong>Kurz gesagt:</strong> MHRN ist gleichzeitig ein technisches Forschungsobjekt und ein Experiment darüber, wie ein einzelner Mensch mit KI-Unterstützung transparent, prüfbar und fehlertolerant forschen kann. Ob daraus ein wissenschaftlich relevanter Beitrag entsteht, entscheiden nicht Projektmarketing oder Autor allein, sondern belastbare Befunde, Kritik und Replikation.</aside>
    </section>
  `;
}
