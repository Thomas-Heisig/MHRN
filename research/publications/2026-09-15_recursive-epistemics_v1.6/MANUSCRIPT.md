# Rekursive Epistemik in verkörperten spikenden neuronalen Architekturen

## Integriertes Dissertationsmanuskript, Fassung 1.6

**Thomas Heisig | 15. September 2026**

Diese Fassung bewahrt die vollständige Fassung 1.5 als eingefrorene empirische und theoretische Basis und ergänzt sie um einen aktuellen autoritativen Revisionsblock. Dadurch bleiben historische Aussagen, Daten und Provenienz erhalten, während der aktuelle Stand des Repositories wissenschaftlich neu eingeordnet wird.

# Teil I – Revision 1.6: wissenschaftliche Reife, Mechanismen und Forschungsintegrität

## 1. Warum technische und wissenschaftliche Entwicklung getrennt werden

MHRN hat sich technisch schneller entwickelt als seine wissenschaftliche Absicherung. Das ist in einem Forschungsframework nicht ungewöhnlich, muss aber sichtbar bleiben. Ein implementierter Mechanismus beantwortet die Frage, ob ein bestimmter Prozess im System ausführbar ist. Ein technisch verifizierter Mechanismus beantwortet zusätzlich, ob dieser Prozess unter definierten Bedingungen reproduzierbar funktioniert. Erst eine wissenschaftliche Untersuchung fragt, ob der Mechanismus eine behauptete Funktion kausal erklärt, gegen Alternativerklärungen besteht und unabhängig bestätigt wurde.

Deshalb führt Fassung 1.6 zwei getrennte Entwicklungsachsen. Die technische Timeline umfasst Implementierung, Integration, Verifikation und Runtime-/Persistenzstatus. Die wissenschaftliche Timeline umfasst Forschungsfrage, Protokoll, DATA, reviewte EVID, unabhängige Replikation und Attribution. Beide Achsen folgen denselben Stufen 0–10, dürfen aber unterschiedliche Werte besitzen.

Die Trennung löst einen zentralen Kritikpunkt früherer Darstellungen: Fortschrittsprozente dürfen nicht vorgeben, dass Infrastruktur und Kognition dasselbe sind. Ein API-Endpunkt ist keine kognitive Fähigkeit. Ein Datenmodell ist kein Mechanismus. Ein technisch erfolgreiches Experiment ist keine automatisch akzeptierte wissenschaftliche Evidenz.

## 2. Der Mechanismus als Gegenstand wissenschaftlicher Prüfung

Die wissenschaftliche Substanz eines Modells liegt in den kausal prüfbaren Beziehungen zwischen Zustand, Intervention und Ergebnis. Für MHRN gilt daher:

- Datenstrukturen beschreiben gespeicherte Zustände;
- Algorithmen beschreiben Transformationen;
- Mechanismen müssen durch Interventionen von Alternativerklärungen getrennt werden;
- wissenschaftliche Claims müssen enger sein als die beobachtete Datenoberfläche, nicht weiter.

Diese Regel ist besonders für Gedächtnis, Vorhersage, Selbstmodell und Weltmodell relevant. Ein Speicher mit Episoden kann technisch nützlich sein, ohne die neurokognitive Funktion episodischen Gedächtnisses zu erfüllen. Eine Fehlerzahl kann eine Metrik sein, ohne Predictive Coding zu bilden. Ein Systemzustand kann Identität persistieren, ohne ein kausales Selbstmodell zu besitzen.

## 3. Die wissenschaftliche Reifematrix 0–10

Die vollständige Stage-by-Stage-Matrix ist in [SCIENTIFIC_STAGE_MATRIX.md](SCIENTIFIC_STAGE_MATRIX.md) dokumentiert. Sie ist Teil dieser Abhandlung. Die Scores sind transparente Projektsteuerungsheuristiken und keine naturwissenschaftlich validierte Skala.

Der aktuelle wissenschaftliche Schwerpunkt liegt auf den Stufen 2–6. Stufen 0–1 besitzen eine solide technische Basis, aber nur begrenzte eigenständige Forschungsfragen. Stufen 2–5 besitzen reale Protokolle und DATA, jedoch noch Lücken bei EVID-Promotion und unabhängiger Replikation. Stage 6 besitzt eine breite Infrastruktur und erste Mechanismen, bleibt aber wissenschaftlich niedriger bewertet, weil die entscheidenden kognitiven Mechanismen noch nicht vollständig implementiert und bestätigt sind.

## 4. Stage 6 als Übergang von Infrastruktur zu Kognition

### 4.1 Episodisches und semantisches Gedächtnis

Die Complementary Learning Systems (CLS) Theorie unterscheidet schnelle episodische Speicherung und langsame neokortikale Integration. Für MHRN ist diese Theorie kein Bauplan, sondern ein Prüfrahmen. Sie legt nahe, episodische Akquisition, Reaktivierung und Konsolidierung getrennt zu operationalisieren.

Die aktuelle Stage-6-Arbeit enthält Speicherpfade und semantische Prototyp-/Registry-Strukturen. Damit ist eine Grundlage vorhanden, aber der entscheidende Mechanismus bleibt offen: die kontrollierte Umwandlung episodischer Erfahrung in eine stabilere semantische Repräsentation. Eine solche Semantization muss Veränderungen über Replay/Konsolidierung zeigen und gegen shuffled replay, no replay und matched-compute Kontrollen bestehen.

### 4.2 Predictive Coding und Prediction Error

Predictive Coding bezeichnet nicht bloß die Berechnung einer Differenz zwischen Vorhersage und Beobachtung. Theorien und Modelle unterscheiden top-down Vorhersagen und bottom-up Fehlerdynamik, teilweise in getrennten Populationen oder dendritischen Kompartimenten. Für MHRN ergibt sich daraus kein Zwang zu einer bestimmten biologischen Architektur. Erforderlich ist aber eine kausal prüfbare Trennung der Pfade.

Ein zukünftiger MHRN-Predictive-Coding-Vertrag muss festlegen, welche neuronalen Zustände Vorhersagen tragen, welche Zustände Fehler tragen, wie beide zeitlich interagieren und wie die Mechanik durch Ablationen zerstört werden kann. Nur dann kann gezeigt werden, dass ein beobachteter Vorteil auf Prediction-Error-Verarbeitung und nicht auf einen externen Prädiktor oder zusätzliche Parameter zurückgeht.

### 4.3 Weltmodelle

Ein Weltmodell wird hier minimal als ein internes Modell der zustands- und aktionsabhängigen Dynamik definiert, das über unmittelbare Beobachtungswiedergabe hinausgeht. Die aktuelle Ein-Schritt-Vorhersage erfüllt diese stärkere Definition noch nicht. Die nächste Stufe verlangt mehrschrittige Rollouts, aktionskonditionierte Übergänge, held-out Sequenzen und einen messbaren Nutzen gegenüber reaktiven Baselines.

Planung oder „Imagination“ ist eine zusätzliche Funktion. Sie sollte nur dann behauptet werden, wenn intern simulierte zukünftige Zustände Entscheidungen verbessern und dieser Vorteil durch Abschalten oder Perturbieren des Weltmodells verschwindet.

### 4.4 Replay, Konsolidierung und Continual Learning

Replay ist eine mechanistische Brücke zwischen Stage 6 und Stage 8. Die Literatur zeigt verschiedene Formen von Offline-Reaktivierung und schlafähnlicher Konsolidierung. Für MHRN muss der Begriff funktional bleiben: Eine Replay-Phase ist eine kontrollierte Wiederaktivierung gespeicherter Information außerhalb der ursprünglichen Erfahrung. Ob sie „Schlaf“ genannt werden darf, ist eine separate biologische Interpretationsfrage.

Prüfbar sind Retention, Interferenz, Transfer, Repräsentationsänderung und Ressourcenverbrauch. Matched-compute Kontrollen sind unverzichtbar, damit ein Vorteil nicht allein aus zusätzlicher Rechenzeit entsteht.

## 5. Multi-Timescale-Architektur: Stärke und Grenze

Die explizite Trennung von Tick-, Plastizitäts-, Konsolidierungs- und Entwicklungszeitskalen ist eine konzeptionelle Stärke von MHRN. Sie schafft eine geeignete Infrastruktur für Stabilitäts-/Plastizitätsforschung. Sie ist aber noch kein Beweis, dass die Zeitskalen funktional richtig gekoppelt sind.

Astrozyteninspirierte oder andere langsame Modulationsmechanismen können als experimentelle Kandidaten aufgenommen werden. Sie dürfen nicht als notwendige biologische Wahrheit oder als automatisch überlegene Lösung dargestellt werden. Jede Modulation muss gegen einfachere Baselines geprüft werden: fester Lernratenplan, Schwellenregelung, Ressourcenbudget und randomisierte Gates.

## 6. Reproduzierbarkeit jenseits von Seeds

Reproduzierbarkeit umfasst Quellcommit, Konfiguration, Umgebung, numerischen Vertrag, Datensatz/Stimulus, Kontrollarme, Rohdaten, Digests und Auswertungsvertrag. Bit-exakte Gleichheit ist eine starke Eigenschaft und wird nur dort verlangt oder behauptet, wo sie für den jeweiligen Mechanismus sinnvoll spezifiziert und getestet wurde.

Fassung 1.6 übernimmt keine unbestätigte externe Spezifikation als Standard. Externe Frameworks oder Bewertungsrubriken können als zusätzliche Orientierung dienen, werden aber nicht als verpflichtender Community-Standard ausgegeben, solange diese Einordnung nicht belastbar belegt ist.

## 7. Forschungsintegrität und Attribution

Wissenschaftliche Eigenständigkeit bedeutet nicht, dass jede Idee ohne Vorläufer entstanden sein muss. Entscheidend ist, dass Herkunft und eigener Beitrag transparent getrennt werden.

MHRN führt deshalb folgende Regeln:

1. Fremde theoretische Konzepte werden an der Stelle zitiert, an der sie die eigene Hypothese oder Architektur motivieren.
2. Übernommener oder adaptierter Code wird mit Quelle und Lizenz dokumentiert.
3. Eigene ältere Editionen werden als Vorarbeiten behandelt. Wiederverwendete Ergebnisse werden auf die ursprüngliche Kampagne zurückgeführt.
4. Große Textübernahmen aus eigenen Vorfassungen werden nicht als neue Originalleistung ausgegeben; die Editionsbeziehung wird offengelegt.
5. KI-generierte oder KI-vorgeschlagene Literaturangaben gelten bis zur manuellen Prüfung als unbestätigt.
6. Eine Similarity-Prüfung kann Risikostellen anzeigen, ersetzt aber nicht die inhaltliche Quellenprüfung.

Der verbindliche Prozess steht in [INTEGRITY_AND_ATTRIBUTION.md](INTEGRITY_AND_ATTRIBUTION.md).

## 8. Kritikfähigkeit statt Kritikfreiheit

„Kritikfreiheit“ ist kein realistisches wissenschaftliches Ziel. Ein starkes Forschungsprogramm zeichnet sich dadurch aus, dass Kritikpunkte prüfbar gemacht und nicht sprachlich beseitigt werden. Fassung 1.6 behandelt deshalb negative Befunde, offene Mechanismen und fehlende Replikation als wissenschaftlichen Fortschritt, wenn sie den Raum zulässiger Behauptungen präzisieren.

Die neue wissenschaftliche Timeline kann daher auch steigen, wenn eine überzogene Behauptung verworfen, eine Alternativerklärung identifiziert oder ein Negativbefund sauber repliziert wird. Sie misst Forschungsreife, nicht Erfolg im Sinne positiver Ergebnisse.

## 9. Systemweite Konsequenzen

Die Trennung wird im gesamten Projekt verankert:

- Release-Frontend: technische und wissenschaftliche Timeline getrennt;
- Publikationssystem: aktuelle Edition 1.6 und eingefrorene historische 1.5;
- Roadmap/TODO: technische und wissenschaftliche Akzeptanzkriterien getrennt;
- Research Workspace: DATA, EVID und Interpretation bleiben getrennte Zustände;
- Review: menschliche Freigabe bleibt Voraussetzung für EVID-Promotion;
- Stage-6-Planung: Semantization, Predictive Coding, Replay und World Model erhalten jeweils eigene Forschungsfragen und Ablationen;
- Integrität: Related Work und Attribution werden als Teil der Forschung, nicht als nachträgliche Formalie behandelt.

## 10. Schlussposition

MHRN ist weder nur Infrastruktur noch bereits eine vollständige kognitive Architektur. Es ist ein wachsendes experimentelles System, dessen technische Mechanismen zunehmend prüfbar werden. Der nächste wissenschaftliche Fortschritt hängt weniger von zusätzlichen Namen oder UI-Feldern ab als von kausalen Mechanismen, starken Kontrollen, Replikation und enger Claim-Disziplin.

Die wichtigste Konsequenz dieser Revision lautet daher: **Technischer Fortschritt darf wissenschaftlichen Fortschritt ermöglichen, aber niemals ersetzen.**

# Teil II – Eingefrorene vollständige Basisfassung 1.5

Die vollständige Fassung 1.5 bleibt unverändert und ist Bestandteil der Provenienz dieser Edition:

- [Dissertationsmanuskript 1.5](../2026-09-13_recursive-epistemics_v1.5/MANUSCRIPT.md)
- [Forschungsarbeit 1.5](../2026-09-13_recursive-epistemics_v1.5/FORSCHUNGSBERICHT.md)
- [Manifest 1.5](../2026-09-13_recursive-epistemics_v1.5/manifest.json)

Die historischen Inhalte werden bewusst nicht kopiert und als neue Texte ausgegeben. Diese Referenzierung macht Eigenwiederverwendung und Editionsabstammung sichtbar.
