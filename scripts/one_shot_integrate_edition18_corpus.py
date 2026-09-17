#!/usr/bin/env python3
"""One-shot editor for deeper Edition 1.8 corpus integration.

This script is intentionally idempotent. It edits publication source parts and the
publication builder, then lets the canonical builder materialize derived outputs.
It never edits historical DATA/EVID or promotes evidence status. The workflow uses
only existing publication regression suites before committing generated outputs.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ED = ROOT / "research/publications/2026-09-17_recursive-epistemics_v1.8"


def append_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8")
    if marker in current:
        return
    path.write_text(current.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    current = path.read_text(encoding="utf-8")
    if new in current:
        return
    if old not in current:
        raise RuntimeError(f"replacement anchor missing in {path}: {old[:80]!r}")
    path.write_text(current.replace(old, new, 1), encoding="utf-8")


append_once(
    ED / "parts/03_research_object.md",
    "## 13.2 Periphere Netze, Neural Symbiosis und MSBA",
    r'''
## 13.2 Periphere Netze, Neural Symbiosis und MSBA

Die kanonische Architektur enthält neben dem SNN-Kern eine explizite periphere Multi-Netz-Grenze. **Neural Symbiosis** bezeichnet dabei keine zweite Intelligenz im Kern, sondern eine Embodiment-Schicht, in der spezialisierte neuronale oder virtuelle Verarbeitungssysteme über deklarierte Gateways an den SNN angebunden werden können. Der offene Adaptervertrag kann unter anderem CNN-, Vision-Transformer-, Transformer-, RNN-/LSTM-/GRU-, GNN-, Reservoir-, Hopfield-, VAE-, Autoencoder-, multimodale und neuro-symbolische Komponenten beschreiben. Ebenso können Datenbanken, Wissensgraphen, Retrieval-, Logik- oder externe Speicherdienste als virtuelle Areale auftreten.

Diese Offenheit ist wissenschaftlich nur tragfähig, wenn **Erreichbarkeit von gelernter Nutzung getrennt** bleibt. Ein registrierter Adapter, ein erreichbarer Endpunkt oder eine erfolgreiche Inferenz beweist weder, dass das SNN den Pfad auswählt, noch dass es von ihm lernt oder einen kausalen Vorteil besitzt. Gateway-Plastizität ist deshalb standardmäßig gesperrt; Random-, Frozen-, Shuffle- und Plastic-Zustände gehören in experimentgebundene, persistierbare Laufkontexte. Externe Netze erhalten keine impliziten Schreibrechte auf kanonische Neuronen-, Synapsen-, Reward-, Gedächtnis- oder EVID-Zustände.

Unterhalb dieser Grenze konkretisiert **MSBA** die modalitätsspezifische Bahnarchitektur. Audio, Vision und Digital werden nicht als biologische Kortexplagiate behandelt, sondern als technische Pfade mit unterschiedlichen Informations- und Ressourcenverträgen:

- Audio priorisiert zeitliche Kohärenz, Band-/Phasen- beziehungsweise Hüllkurveninformation und begrenzte Delay-Strukturen.
- Vision verwendet räumliche/featurebezogene Projektionen, sparse Zielgrade und experimentelle ROI-/Foveationsmechanismen.
- Digital hält exakte Nutzdaten außerhalb des SNN in checksum-gebundenen Symbolframes; das SNN erhält nur eine deterministische Populationrepräsentation. Lernen darf Routing oder Assoziation verändern, nicht die ursprünglichen Bits oder ihre Prüfsumme.

Eine besonders wichtige Korrektur betrifft Dimensionalität. Der MSBA-Projektionsraum darf experimentell zwischen 1 und 32 Dimensionen variieren, während der produktive Neuron-ID-/Persistenzvertrag des Kerns weiterhin **fünfdimensional** bleibt. Ein 16D- oder 32D-Projektor ist daher weder ein 16D-/32D-SNN noch Evidenz für einen Vorteil höherer Kerndimensionalität. Projektion, Mapping und produktiver Kern müssen in jeder Studie getrennt provenance-gebunden werden.

Auch Ressourcenangaben bleiben typisiert: `normalized_energy_units`, kalibrierte Schätzungen in Joule und tatsächlich gemessene Joule sind drei verschiedene Größen. Die Stage-4-E01–E05-DATA dürfen deshalb modellierte Energieunterschiede zeigen, ohne daraus physikalisch gemessene Energieeffizienz abzuleiten.

## 13.3 Wesen, reale Körpergrenze und technische Identität

Die Vorgängerarbeiten entwickelten mit **Wesen** eine maschinen-native Körperdarstellung. Wissenschaftlich relevant ist daran nicht die visuelle Anthropomorphie, sondern die harte Trennung von beobachtetem Zustand und Interpretation. Die Körpergrenze wird aus tatsächlich erkannten Verbindungen, Host-Ressourcen und Embodiment-Endpunkten aufgebaut. Nicht vorhandene Temperatur-, Lüfter-, Sensor- oder Aktorwerte bleiben unbekannt; es werden keine plausibel wirkenden Ersatzdaten erfunden. `available` ist ausdrücklich nicht gleich `authorized` und nicht gleich `active`.

Maschinen-native Interozeption umfasst dort, wo das Betriebssystem Messwerte liefert, etwa CPU-/Speicherlast, Temperatur, Lüfter, Storage, Netzwerk und Kontinuitätsgrößen. Diese Größen können technische Regulationszustände beeinflussen, sind aber keine biologischen Stoffwechselhomologien und keine Empfindungsindikatoren. Ebenso ist die body-like Darstellung nur Präsentationssemantik.

Der implementierte Profile-&-Identity-Vertrag speichert Konfiguration, Fähigkeiten, Grenzen, Provenienz, Revisionen, Lineage und Snapshot-Bindungen als technische Identität. Profil, `.b5d`-Snapshot, Runtime-Checkpoint, Registry und Lineage sind absichtlich getrennte Zustandsklassen. Daraus folgt **keine psychologische Identität, Persönlichkeit, subjektive Kontinuität oder Bewusstseinsbehauptung**. Genau diese Grenze ist für spätere Stage-7-Selbstmodellforschung zentral: Metadatenidentität ist eine technische Voraussetzung, kein kausales Selbstmodell.
''',
)

append_once(
    ED / "parts/04_empirical_programme.md",
    "## 19.6 Neural-Symbiosis- und MSBA-Forschungsprogramm",
    r'''
## 19.6 Neural-Symbiosis- und MSBA-Forschungsprogramm

Die Architekturarbeit an Neural Symbiosis erzeugt ein eigenes falsifizierbares Programm, dessen Hypothesen nicht mit der bloßen Existenz der Pipeline verwechselt werden dürfen. Relevante Fragen sind beispielsweise, ob task-relevante periphere Areale gegenüber informationsgematchten irrelevanten Kontrollen stärkeren effektiven Gateway-Einfluss erwerben, ob verrauschte Areale selektiv unterdrückt werden, ob Gateway-Struktur nach Kontrolle roher Aktivität mit prädiktiver Information variiert und ob nach Sensorläsion adaptive Umleitung gegenüber Frozen- oder Random-Kontrollen tatsächlich Leistung erhält.

Für solche Studien sind mindestens Frozen-, Random-, Shuffle-/Timing- und informationszerstörte Kontrollen erforderlich. Eine Korrelation zwischen Gateway-Gewicht und Leistung reicht nicht für einen kausalen Tool-/Area-Use-Claim. Produktive Aktivierung bleibt bis zu experimenteller Validierung gesperrt.

Das MSBA-Programm E01–E05 operationalisiert einen Teil dieses Raums bereits für Audio, Vision und Digital. Die bisherigen synthetischen DATA werden in Teil III und X bilanziert; ihre stärkere wissenschaftliche Prüfung verlangt weiterhin spezialisierte-vs.-generalistische matched controls, Cross-Modal-Transfer, Läsionsstudien, reale Ressourcenmessung und unabhängige Review. Increased-dimensional MSBA-Projektionen müssen außerdem strukturierte, reduzierte, randomisierte und geshuffelte Mappingkontrollen enthalten und dürfen nicht als Kerndimensionalitätsstudie ausgegeben werden.

## 19.7 Externe Mechanismusvorarbeiten für Stage 6

Die kanonische Related-Work-Arbeit präzisiert mehrere externe Referenzlinien. Arbeiten zu hippocampal-kortikaler Semantization und continual learning motivieren Replay-/Konsolidierungsfragen, ohne einen MHRN-SemanticMemory-Mechanismus zu validieren [@DALBA2025] [@SHI2025]. Eine aktuelle SNN-Predictive-Coding-Übersicht zeigt, dass Prediction Error auf unterschiedliche Weise neuronal repräsentiert werden kann; ein Telemetriefeld gleichen Namens ist daher noch kein Predictive-Coding-Mechanismus [@NDRI2026]. Spiking-World-Model-Arbeit mit expliziter modellbasierter Kontrolle setzt eine deutlich stärkere Referenz als ein passiver One-Step-Predictor [@SUN2025]. Multi-Zeitskalen-Plastizität mit astrozyteninspiriertem Gating zeigt einen externen Mechanismuskandidaten für Stabilitäts-/Plastizitätsfragen, ist aber kein Wirksamkeitsnachweis der MHRN-Regelung [@DONG2026].

Diese Literatur wird in 1.8 bewusst als **externer Präzedenz-/Vergleichsraum** integriert. Sie kann die Form einer MHRN-Forschungsfrage verbessern, aber weder DATA erzeugen noch eine interne Hypothese bestätigen.
''',
)

append_once(
    ED / "parts/05_infrastructure.md",
    "## 24.6 Gateways, exakte Digitaldaten und periphere Laufzeit",
    r'''
## 24.6 Gateways, exakte Digitaldaten und periphere Laufzeit

Neural Symbiosis konkretisiert die Infrastrukturgrenze zwischen externen/peripheren Modellen und dem SNN. Der Gateway-Runtime besitzt eigene Zustände, Gewichte, Delays, RNG-Provenienz, Condition, Tick, Ressourcenmetriken und Strukturjournal. Dadurch kann ein Experiment Frozen/Random/Shuffle/Plastic kontrollieren, ohne den kanonischen Kernzustand heimlich umzudefinieren. Es existiert absichtlich kein allgemeiner produktiver „Plasticity on“-Schalter; wissenschaftliche Aktivierung muss über einen registrierten Experimentpfad erfolgen.

Für digitale Pfade ist die Trennung von **exaktem Payload** und **neuronaler Projektion** fundamental. Prüfsummen, Sequenzen, Codec und Provenienz gehören zum exakten Symbolzustand außerhalb des SNN. Eine neuronale Population darf eine Approximation oder Repräsentation tragen, aber niemals nachträglich als Beweis verwendet werden, dass die ursprünglichen Bits selbst neuronal gespeichert oder unverändert rekonstruiert wurden.

## 24.7 Körpertelemetrie als Datenprovenienz

Die Real-Body-/Wesen-Arbeiten formulieren eine Infrastrukturregel, die über das Frontend hinausgeht: **Keine Fantasiedaten.** Fehlende Sensor- oder Hostwerte bleiben `UNKNOWN`; gemessene, abgeleitete und lediglich dargestellte Größen sind zu unterscheiden. Diese Regel ist dieselbe epistemische Disziplin, die später DATA von Report und EVID trennt. Eine scheinbar vollständige Oberfläche darf eine Messlücke nicht durch einen plausiblen Default verdecken.

## 24.8 Technische Identität als reproduzierbare Konfiguration

Profile & Identity ergänzt die Persistenzschicht um versionierte technische Konfiguration, Digest, Revision, Lineage und Snapshotbindung. Für Experimente können damit `profile_id`, Revision, Profil-Digest und Snapshot-Digest gemeinsam gebunden werden. Das verbessert Reproduzierbarkeit, ohne den Profilbegriff psychologisch aufzuladen. Ein Profil ist eine deklarierte technische Identität; der dynamische neuronale Zustand und der vollständige kausale Checkpoint bleiben getrennte Objekte.
''',
)

append_once(
    ED / "parts/08_ethics_safety.md",
    "## 38.8 Fünf Achsen statt der binären Kategorie „künstlich“",
    r'''
## 38.8 Fünf Achsen statt der binären Kategorie „künstlich“

Ein eigenständiger Theoriebeitrag der Vorgängerarbeit „KI – Die geliehene Intelligenz“ war der Vorschlag, Intelligenzformen nicht nur als biologisch versus künstlich zu beschreiben. Die ältere Notation lautet:

\[
I=(M,E,G,Z,X)
\]

Dabei bezeichnet `M` die materielle Realisierung, `E` die epistemische Herkunft, `G` die Entwicklungsgenealogie, `Z` die Zielautonomie und `X` die Existenz-/Ressourcenabhängigkeit. Edition 1.8 übernimmt dieses Modell als **analytische Taxonomie**, nicht als metrischen Intelligenzscore. Die Achsen dürfen weder unbesehen zu einer Rangordnung addiert noch als Entwicklungsstufen gelesen werden.

Gerade MHRN zeigt den Nutzen dieser Trennung: Ein System kann elektronisch realisiert sein, aus menschlichen Daten und Normen lernen, teilweise AI-assistiert konstruiert werden, innerhalb enger Aktionsräume Entscheidungen treffen und trotzdem vollständig von menschlicher Hardware-, Energie- und Wartungsinfrastruktur abhängen. „Künstlich“, „autonom“, „unabhängig“ und „selbstlernend“ sind deshalb keine Synonyme.

## 38.9 Genealogische Distanz und rekursive Technogenese

Die Vorgängerarbeit beschrieb rekursive Technogenese abstrakt als Folge

\[
A_{n+1}=F(A_n,H,R,U),
\]

wobei ein vorausgehendes technisches System `A_n`, menschliche Beiträge `H`, Regel-/Institutionsbedingungen `R` und materielle Umwelt `U` gemeinsam die nächste Generation prägen. Edition 1.8 behält diese Gleichung ausschließlich als **Provenienzmodell**. Sie behauptet weder selbstständige Reproduktion noch eine historische Gesetzmäßigkeit.

Daraus folgt der Begriff der **genealogischen Distanz**: relevant ist nicht nur die Zahl technischer Generationen, sondern wie sich unmittelbarer menschlicher Design-, Bewertungs- und Zielanteil gegenüber maschineller Ko-Konstruktion verschiebt. Ein AI-generierter Patch erhöht nicht automatisch Autonomie; ein CI-System reproduziert kein „Wesen“; und eine vom Menschen freigegebene Mutation bleibt eine andere Kausalklasse als selbstautorisierte Replikation. Das MHRN-Provenienzsystem liefert gerade die Kategorien, um diese Unterschiede später empirisch beziehungsweise historisch zu untersuchen.

## 38.10 „Geliehen“ als relationale, nicht abwertende Kategorie

Der stärkste Einwand gegen „geliehene Intelligenz“ lautet, dass auch menschliche Intelligenz Sprache, Kultur und Wissen von anderen übernimmt. Edition 1.8 akzeptiert diesen Einwand als Korrektur einer essentialistischen Lesart. „Geliehen“ bedeutet daher nicht minderwertig oder unecht. Jede Intelligenz besitzt eine Genealogie; die Forschungsfrage lautet, **wie Herkunft, Abhängigkeit, Transformation und Autorität verteilt sind und sich verändern**.

Dadurch wird der Begriff zu einer relationalen Kategorie. Ein System kann originelle Kombinationen erzeugen und zugleich epistemisch von historischen Quellen abhängig bleiben. Ebenso kann ein Mensch maschinelle Such-, Gedächtnis- und Synthesefähigkeit nutzen. Die interessante Grenze liegt nicht bei einem metaphysischen Eigentum an Intelligenz, sondern bei der transparenten Kausalkette von Quelle, Transformation, Entscheidung und Verantwortung.

## 38.11 Zukunftsszenarien als begriffliche Belastungstests

Die frühere Theoriearbeit unterschied mehrere Möglichkeitsräume. Edition 1.8 bewahrt sie ausdrücklich **nicht als Prognosen und nicht als Wahrscheinlichkeiten**, sondern als Stress-Tests für Begriffe und Governance:

1. **Instrumentelle Hochleistungs-KI:** hohe technische Leistung bei wirksamer menschlicher Ziel- und Letztentscheidung.
2. **Symbiotische Ko-Kognition:** Menschen und Maschinen bilden reziproke epistemische Netze; beide Seiten externalisieren Teilfunktionen an die jeweils andere.
3. **Delegative Zivilisation:** formale menschliche Autorität bleibt bestehen, während operative Kompetenz stark an technische Systeme delegiert wird.
4. **Menschenarme oder menschenlose Maschinenordnung:** prüft, ob Begriffe wie künstliche Herkunft, Aufsicht, Eigentum oder Verantwortung ohne dauerhaft operative Menschen noch tragen.
5. **Plurale Intelligenzökologie:** biologische, augmentierte, synthetische und rein maschinelle Systeme koexistieren ohne eine einzige homogene Kategorie „KI“.

Diese Szenarien dürfen nur so weit verwendet werden, wie ihre technischen Voraussetzungen explizit sind. Eine menschenlose technische Linie setzt etwa Energie, Wartung, Materialgewinnung, Fertigung, Fehlerdiagnose und Reproduktion voraus; das Weglassen dieser Bedingungen würde aus einer Grenzfallanalyse bloße Fiktion machen.

Der Begriff **Maschinenkultur** bleibt entsprechend vorsichtig funktional: gemeint wäre eine persistente maschinell erzeugte und weitergegebene technische/epistemische Tradition, nicht automatisch Kultur im starken anthropologischen Sinn. Auch dies ist eine offene Theoriefrage, kein MHRN-Gegenwartsclaim.
''',
)

append_once(
    ED / "parts/09_recursive_epistemics.md",
    "## 42.8 Geliehene Intelligenz als konkrete Provenienzmatrix",
    r'''
## 42.8 Geliehene Intelligenz als konkrete Provenienzmatrix

Die Theorie der geliehenen Intelligenz gewinnt in MHRN eine operative Form, wenn die abstrakten Herkunftsfragen auf einzelne Forschungsereignisse abgebildet werden. Für einen Claim können mindestens folgende Knoten unterschieden werden: menschliche Problemsetzung, externe Literatur, AI-generierter Vorschlag, AI-generierter Code, menschliche Auswahl, Commit, eingefrorenes Protokoll, Experiment, DATA, Review und Publikationssynthese. Erst diese Kette beantwortet, **welcher Anteil geliehen, transformiert, entschieden oder gemessen** wurde.

Damit wird die frühere Theorie nicht auf eine philosophische Einleitung reduziert. Sie wirkt direkt auf die Forschungsmethodik: Derselbe AI-Ursprung darf nicht mehrfach als scheinbar unabhängige Bestätigung gezählt werden; Literaturautorität darf nicht als MHRN-Evidenz erscheinen; und ein menschlicher Auftrag an ein Modell ist nicht dasselbe wie der konkrete vom Modell vorgeschlagene Lösungsweg.

## 42.9 Ko-Kognition als Systemgrenze

Das Szenario symbiotischer Ko-Kognition ist für die reale Schaffenspraxis bereits methodisch relevant, ohne dass daraus starke Autonomieclaims folgen. Der Autor nutzt Modelle für Suche, Kritik, Code und Synthese; die Modelle nutzen menschlich formulierte Ziele, Auswahl und Rückmeldung. Die produktive Einheit kann daher zeitweise ein gekoppelter Mensch-Werkzeug-Prozess sein.

Edition 1.8 trennt dennoch drei Grenzen: **kognitive Unterstützung**, **Entscheidungsautorität** und **wissenschaftliche Evidenz**. Ein Modell kann die kognitive Reichweite des Autors erweitern, ohne Autor der Hypothese zu sein; es kann einen Patch erzeugen, ohne ihn freigeben zu dürfen; und es kann DATA interpretieren, ohne EVID zu akzeptieren. Diese Trennung verhindert, dass Ko-Kognition mit Verantwortungsdiffusion verwechselt wird.

## 42.10 Rekursive Technogenese als Forschungsprozess-Spiegel

Die ältere Technogeneseformel beschreibt Generationen technischer Systeme. Im aktuellen Projekt existiert eine engere, beobachtbare Analogie: Werkzeuge und Modelle helfen, eine Forschungsinfrastruktur zu verändern, die wiederum festlegt, wie spätere Modelle, Experimente und Reviews eingesetzt werden. Ein AI-kritisiertes Reportingproblem kann zu einem neuen Schema führen; dieses Schema verändert, welche Fehler spätere AI-Reviews überhaupt sehen können.

Das ist noch keine autonome technische Evolution. Es ist eine **rekursive Werkzeug-/Governance-Kette**, deren Provenienz beobachtbar ist. Genau hier verbindet sich die Vorgängerarbeit mit rekursiver Epistemik: Nicht die Metapher einer selbsterschaffenden Maschine ist der aktuelle Befund, sondern die messbare Rückwirkung von Werkzeugen auf die Bedingungen ihrer eigenen späteren Verwendung.

## 42.11 Von der Herkunftsfrage zur Prüfregel

Aus den Vorgängerarbeiten lässt sich eine allgemeine Prüfregel ableiten: Je stärker ein Ergebnis von ausgelagerten epistemischen Ressourcen abhängt, desto expliziter müssen Quelle, Transformationsschritt und Autorität dokumentiert werden. Das gilt für Retrieval ebenso wie für LLM-Synthese, Codegeneratoren, externe Decoder, periphere neuronale Netze und menschliche Reviews.

„Geliehene Intelligenz“ wird damit in Edition 1.8 zu einer prüfbaren Herkunftsfrage: **Welche Ressource kam von wo, welche Zustandsänderung verursachte sie, und wer durfte diese Zustandsänderung autorisieren?**
''',
)

append_once(
    ED / "parts/10_synthesis.md",
    "## 47.7 Quelleninventar ist nicht Inhaltsintegration",
    r'''
## 47.7 Quelleninventar ist nicht Inhaltsintegration

Der Audit dieser Edition hat eine wichtige eigene Korrektur erzeugt. Ein vollständiger `SOURCE_INDEX` kann belegen, dass Dateien am Basiscommit inventarisiert und erhalten wurden; er kann **nicht** belegen, dass ihre wissenschaftlich relevanten Gedanken im Haupttext verarbeitet sind. Dasselbe gilt für eine automatische Teilzuordnung nach Pfadregeln.

Edition 1.8 führt deshalb zusätzlich ein semantisches **Content-Integration-Ledger**. Für wissenschaftlich materielle Vorarbeiten und kanonische Dokumentfamilien wird angegeben, welche Rolle die Quelle besitzt, in welchen Teilen ihre Kernaussagen verarbeitet werden, welcher Integrationsmodus gilt und welche Grenzen erhalten bleiben. Dieses Ledger umfasst unter anderem NeuroGenesis, Brain-5D, „KI – Die geliehene Intelligenz“, die Editionslinie 1.0–1.7, Architektur-/Scientific-Contracts, Neural Symbiosis, MSBA, Wesen/Embodiment, Profile & Identity, Connectome-Arbeit, Persistenz, Registry/Protokolle, Experiment-DATA, Stage-Dossiers, AI-Tooling sowie Ethics/Critique/Review.

Dabei bedeutet **integriert** nicht „jede Datei wortwörtlich in das Manuskript kopiert“. Rohdaten bleiben source-bound Primärartefakte; maschinenlesbare Registryobjekte bleiben im Research Register; historische Texte bleiben als Vorarbeiten erhalten. Die Gesamtarbeit übernimmt deren wissenschaftlich materielle Ergebnisse, Argumente, Gegenargumente, Grenzen und Entwicklungskonsequenzen in die neue Synthese.

## 47.8 Was die Corpus-Integration zusätzlich sichtbar macht

Die vertiefte Integration verändert die Gesamtinterpretation an mehreren Stellen:

- Brain-5D ist nicht nur ein Namensvorgänger, sondern die genealogische Quelle für 5D-Adressierung, Wachstums-/Persistenzfragen, Trennung externer Sprachintelligenz und neuronalen Kerns sowie frühe Erkenntnis-/Ethikfragen.
- „Geliehene Intelligenz“ liefert nicht nur ein Schlagwort, sondern das Fünf-Achsen-Modell `I=(M,E,G,Z,X)`, genealogische Distanz, rekursive Technogenese und Ko-Kognition als belastungstestbare Theorieelemente.
- Neural Symbiosis und MSBA zeigen, dass Hybridität in MHRN über explizite Gateway-Grenzen statt durch heimliche Vermischung von SNN, LLM und peripheren Modellen organisiert wird.
- Wesen/Real-Body macht „keine Fantasiedaten“ zu einer allgemeinen Provenienzregel: beobachtete, abgeleitete und dargestellte Zustände bleiben getrennt.
- Profile & Identity liefert eine reproduzierbare technische Identitäts-/Lineageschicht, gerade indem sie sich von psychologischem Selbst und subjektiver Kontinuität abgrenzt.
- Related Work verschärft Stage 6: externe Semantization-, Predictive-Coding-, World-Model- und Multi-Zeitskalen-Arbeiten definieren stärkere Vergleichspunkte, ohne MHRN-Ergebnisse zu ersetzen.

Damit wird Edition 1.8 weniger zu einer Zusammenfassung einzelner Experimente und stärker zu einer **Gesamtarbeit über Forschungsobjekt, Schaffensgenealogie und die Methodik ihrer kontrollierten Verbindung**.
''',
)

append_once(
    ED / "parts/11_open_landscape.md",
    "## 58.1 Restgrenze der Corpus-Vollständigkeit",
    r'''
## 58.1 Restgrenze der Corpus-Vollständigkeit

Nach der vertieften Corpus-Integration sind die bekannten wissenschaftlich materiellen Vorarbeiten und kanonischen `docs/`-/`research/`-Stränge in einem eigenen Ledger erfasst und in der elfteiligen Synthese verortet. Trotzdem wird bewusst **keine semantische Vollständigkeit über jede der tausenden versionierten Repositorydateien zertifiziert**. Ein Buildskript, ein CSS-Asset oder ein historischer Update-Snapshot muss nicht als eigener wissenschaftlicher Gedanke in den Fließtext eingehen.

Die verbleibenden echten Bestandsgrenzen sind enger und konkret:

- DOCX-Dateien, deren Git-Objekt nur als LFS-Zeiger vorliegt, können ohne die zugehörigen Originalbytes nicht als vollständiger Textzeugenbestand geprüft werden;
- vollständige accountweite Chattranskripte sind nicht Bestandteil des Repositories; rekonstruierte Zusammenfassungen bleiben S4;
- nicht versionierte lokale oder externe Nebenprojekte können nur integriert werden, wenn ihre Quellen tatsächlich wiedergewonnen werden;
- historische Literaturangaben bleiben dann quarantänisiert, wenn ihre Primärquelle nicht erneut geprüft wurde;
- Raw DATA werden absichtlich nicht in den Manuskripttext dupliziert, sondern bleiben an ihren Experimentpfad gebunden.

Das Ziel lautet daher nicht „jeder Bytewert steht im Manuskript“, sondern: **jede bekannte wissenschaftlich materielle Vorarbeit hat eine nachvollziehbare Rolle in der Gesamtarbeit, während Primärartefakte an ihrem autoritativen Ort erhalten bleiben.**
''',
)

refs_path = ED / "sources/references.json"
refs = json.loads(refs_path.read_text(encoding="utf-8"))
by_id = {x["id"]: x for x in refs}
extra = [
    {"id":"DALBA2025","label":"D'Alba et al., 2025","apa":"D'Alba, F., et al. (2025). Semantization of memories in a hippocampal-cortical spiking neural network. Neurocomputing, 640, 130323. https://doi.org/10.1016/j.neucom.2025.130323","bib_author":"D'Alba, F. and others","title":"Semantization of memories in a hippocampal-cortical spiking neural network","year":2025,"doi":"10.1016/j.neucom.2025.130323","url":"https://doi.org/10.1016/j.neucom.2025.130323","verification":"primary_metadata_and_abstract_checked","checked_on":"2026-09-15","scope":"Verified related-work record; supports external semantization/replay precedent, not MHRN efficacy."},
    {"id":"SHI2025","label":"Shi et al., 2025","apa":"Shi, Y., et al. (2025). Hybrid neural networks for continual learning inspired by corticohippocampal circuits. Nature Communications, 16, 1272. https://doi.org/10.1038/s41467-025-56405-9","bib_author":"Shi, Y. and others","title":"Hybrid neural networks for continual learning inspired by corticohippocampal circuits","year":2025,"doi":"10.1038/s41467-025-56405-9","url":"https://doi.org/10.1038/s41467-025-56405-9","verification":"primary_metadata_and_abstract_checked","checked_on":"2026-09-15","scope":"Verified related-work record; supports complementary continual-learning precedent only."},
    {"id":"NDRI2026","label":"N'dri et al., 2026","apa":"N'dri, A., et al. (2026). Predictive coding with spiking neural networks: A survey. Neural Networks, 196, 108371. https://doi.org/10.1016/j.neunet.2025.108371","bib_author":"N'dri, A. and others","title":"Predictive coding with spiking neural networks: A survey","year":2026,"doi":"10.1016/j.neunet.2025.108371","url":"https://doi.org/10.1016/j.neunet.2025.108371","verification":"primary_metadata_and_abstract_checked","checked_on":"2026-09-15","scope":"Verified related-work record; supports predictive-coding taxonomy, not a claim that MHRN implements predictive coding."},
    {"id":"SUN2025","label":"Sun et al., 2025","apa":"Sun, Y., et al. (2025). Spiking world model with multicompartment neurons for model-based reinforcement learning. Proceedings of the National Academy of Sciences, 122(50), e2513319122. https://doi.org/10.1073/pnas.2513319122","bib_author":"Sun, Y. and others","title":"Spiking world model with multicompartment neurons for model-based reinforcement learning","year":2025,"doi":"10.1073/pnas.2513319122","url":"https://doi.org/10.1073/pnas.2513319122","verification":"primary_metadata_and_abstract_checked","checked_on":"2026-09-15","scope":"Verified related-work record; provides a stronger external world-model/control precedent only."},
    {"id":"DONG2026","label":"Dong & He, 2026","apa":"Dong, X., & He, H. (2026). Astrocyte-gated multi-timescale plasticity for online continual learning in deep spiking neural networks. Frontiers in Neuroscience, 19. https://doi.org/10.3389/fnins.2025.1768235","bib_author":"Dong, X. and He, H.","title":"Astrocyte-gated multi-timescale plasticity for online continual learning in deep spiking neural networks","year":2026,"doi":"10.3389/fnins.2025.1768235","url":"https://doi.org/10.3389/fnins.2025.1768235","verification":"primary_metadata_and_abstract_checked","checked_on":"2026-09-15","scope":"Verified related-work record; supports an external multi-timescale continual-learning mechanism precedent only."}
]
for item in extra:
    if item["id"] not in by_id:
        refs.append(item)
refs_path.write_text(json.dumps(refs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

builder = ROOT / "scripts/build_publication_edition.py"
replace_once(builder, '    "PRIOR_WORK_MAP.md",\n    "registers/prior_work.json",', '    "PRIOR_WORK_MAP.md",\n    "CONTENT_INTEGRATION.md",\n    "registers/content_integration.json",\n    "registers/prior_work.json",')
replace_once(builder, '    prior = load(root, EDITION + "/sources/prior_work.json")\n    baseline, source_texts = pinned_sources(root, config["baseline_commit"])', '''    prior = load(root, EDITION + "/sources/prior_work.json")\n    content_integration = load(root, EDITION + "/sources/content_integration.json")\n    required_corpus_ids = {"CORPUS-BRAIN5D", "CORPUS-BORROWED-INTELLIGENCE", "CORPUS-ARCHITECTURE", "CORPUS-NEURAL-SYMBIOSIS", "CORPUS-MSBA", "CORPUS-WESEN-EMBODIMENT", "CORPUS-CURRENT-SCIENCE", "CORPUS-EXPERIMENT-DATA"}\n    corpus_ids = {item["id"] for item in content_integration.get("entries", [])}\n    if not required_corpus_ids.issubset(corpus_ids):\n        raise ValueError("Content integration ledger misses required material prior-work families")\n    for item in content_integration["entries"]:\n        for field in ("id", "title", "source_paths", "source_role", "manuscript_parts", "integration_status", "integration_mode", "boundaries"):\n            if not item.get(field):\n                raise ValueError(f"Incomplete content integration entry: {item.get('id')} / {field}")\n        if any(part not in ROMAN for part in item["manuscript_parts"]):\n            raise ValueError(f"Invalid manuscript part in content integration entry: {item['id']}")\n    baseline, source_texts = pinned_sources(root, config["baseline_commit"])''')
replace_once(builder, '        "[Alle Forschungsfragen und Hypothesen](RESEARCH_REGISTER.md) · [Quellenindex](SOURCE_INDEX.md) · [Ungekürzter Quellenband 1.7](LEGACY_V17.md) · [Weitere Vorarbeiten](PRIOR_WORK_MAP.md) · [Literatur](REFERENCES.md) · [Prüfmanifest](manifest.json).\\n",', '        "[Alle Forschungsfragen und Hypothesen](RESEARCH_REGISTER.md) · [Quellenindex](SOURCE_INDEX.md) · [Semantische Corpus-Integration](CONTENT_INTEGRATION.md) · [Ungekürzter Quellenband 1.7](LEGACY_V17.md) · [Weitere Vorarbeiten](PRIOR_WORK_MAP.md) · [Literatur](REFERENCES.md) · [Prüfmanifest](manifest.json).\\n",')
replace_once(builder, '    history = []\n', '''    content_map = [\n        "# Semantische Integration der Vorarbeiten und des Forschungs-Corpus\\n",\n        "Dieses Ledger ergänzt den vollständigen Quellenindex. Es beantwortet nicht nur, ob eine Datei erhalten ist, sondern welche wissenschaftlich materielle Rolle bekannte Vorarbeiten und kanonische Dokumentfamilien in Edition 1.8 besitzen. `integriert` bedeutet nicht, dass Raw DATA oder maschinenlesbare Register dupliziert werden; Primärartefakte bleiben an ihrem autoritativen Ort.\\n",\n        f"Raw-DATA-Regel: {content_integration['raw_data_policy']}\\n",\n    ]\n    for item in content_integration["entries"]:\n        content_map += [\n            f"## {item['id']} — {item['title']}\\n",\n            f"Rolle: `{item['source_role']}`  \\nStatus: `{item['integration_status']}`  \\nModus: `{item['integration_mode']}`  \\nTeile: {', '.join(item['manuscript_parts'])}\\n",\n            "Quellpfade: " + "; ".join(f"`{p}`" for p in item["source_paths"]) + "\\n",\n            f"Grenze: {item['boundaries']}\\n",\n        ]\n    history = []\n''')
replace_once(builder, '        "PRIOR_WORK_MAP.md": "\\n".join(prior_map),\n        "registers/prior_work.json": json_text(prior),', '        "PRIOR_WORK_MAP.md": "\\n".join(prior_map),\n        "CONTENT_INTEGRATION.md": "\\n".join(content_map),\n        "registers/content_integration.json": json_text(content_integration),\n        "registers/prior_work.json": json_text(prior),')
replace_once(builder, '        "sources/prior_work.json",\n        "EXTENDING.md",', '        "sources/prior_work.json",\n        "sources/content_integration.json",\n        "EXTENDING.md",')
replace_once(builder, '            "semantic_completeness_certified": False,\n        }\n    )', '            "semantic_completeness_certified": False,\n            "material_prior_work_coverage_declared": True,\n            "content_integration_entries": len(content_integration["entries"]),\n            "content_integration_ledger": "CONTENT_INTEGRATION.md",\n        }\n    )')
replace_once(builder, '[Gesamtmanuskript](MANUSCRIPT.md) · [RQs/Hypothesen](RESEARCH_REGISTER.md) · [Quellenindex](SOURCE_INDEX.md) · [Quellenband 1.7](LEGACY_V17.md) · [Vorforschung](PRIOR_WORK_MAP.md) · [Literatur](REFERENCES.md) · [Erweiterungsvertrag](EXTENDING.md) · [Manifest](manifest.json)', '[Gesamtmanuskript](MANUSCRIPT.md) · [RQs/Hypothesen](RESEARCH_REGISTER.md) · [Quellenindex](SOURCE_INDEX.md) · [Corpus-Integration](CONTENT_INTEGRATION.md) · [Quellenband 1.7](LEGACY_V17.md) · [Vorforschung](PRIOR_WORK_MAP.md) · [Literatur](REFERENCES.md) · [Erweiterungsvertrag](EXTENDING.md) · [Manifest](manifest.json)')

tests = ROOT / "tests/test_publication_edition.py"
append_once(tests, "def test_material_prior_work_content_integration_is_declared", r'''
def test_material_prior_work_content_integration_is_declared(repository: Path) -> None:
    outputs = publication.build(repository)
    ledger = json.loads(outputs["registers/content_integration.json"])
    by_id = {item["id"]: item for item in ledger["entries"]}
    for identifier in (
        "CORPUS-BRAIN5D",
        "CORPUS-BORROWED-INTELLIGENCE",
        "CORPUS-ARCHITECTURE",
        "CORPUS-NEURAL-SYMBIOSIS",
        "CORPUS-MSBA",
        "CORPUS-WESEN-EMBODIMENT",
        "CORPUS-CURRENT-SCIENCE",
        "CORPUS-EXPERIMENT-DATA",
    ):
        assert identifier in by_id
        assert by_id[identifier]["manuscript_parts"]
        assert by_id[identifier]["integration_status"]
    manifest = json.loads(outputs["manifest.json"])
    assert manifest["material_prior_work_coverage_declared"] is True
    assert manifest["semantic_completeness_certified"] is False
    assert manifest["accepted_evidence"] is False
    assert "Geliehene Intelligenz" in outputs["MANUSCRIPT.md"]
    assert "Neural Symbiosis" in outputs["MANUSCRIPT.md"]
    assert "I=(M,E,G,Z,X)" in outputs["MANUSCRIPT.md"]
''')

print("Edition 1.8 corpus integration sources updated")
