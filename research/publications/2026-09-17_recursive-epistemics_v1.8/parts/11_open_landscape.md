# Teil XI — Offene Forschungslandschaft

## 48. Offene empirische Felder

Die offene Forschungslandschaft wird aus dem tatsächlich erreichten Stand abgeleitet. Bereits erledigte Prüfungen werden nicht weiterhin als pauschal „offen“ geführt; zugleich wird ein enger positiver Befund nicht zu einer breiteren Reife hochgestuft.

### Stage 0 — einzelne Nervenzelle

Der scoped Referenzkonformitätsvertrag für Izhikevich und `lif-current-v1` ist mit der Brian2-V2-Kampagne erfüllt. Offen bleiben daher **nicht** mehr allgemein „ein externer Referenzvergleich“, sondern die stärkeren nächsten Ebenen:

- menschliche EVID-Entscheidung zu den confirmatory DATA;
- unabhängig autorisierte Replikation außerhalb derselben MHRN-Ausführungskette;
- breitere Integrator-, Zeitschritt- und Parameterablationen;
- zusätzliche Neuronmodelle nur als klar deklarierte alternative Modellarme;
- Prüfung, welche lokalen Konformitätsaussagen über längere freie Trajektorien stabil bleiben und wo chaotische/nichtlineare Divergenz erwartbar ist.

Der scoped Readiness-Vertrag kann 100 % erreicht haben, ohne dass damit die gesamte wissenschaftliche Reife der Stage abgeschlossen ist.

### Stage 1 — kleines SNN

Mit `EXP-S1-TOPO-V2-20260918` liegt nun eine präregistrierte Small-Network-Topologiestudie vor. Sie zeigt DATA-seitig, dass Topologie die Propagationsdynamik im kontrollierten 64-Neuronen-Regime beeinflusst. Offen bleiben:

- Human Review und eine mögliche spätere EVID-Entscheidung;
- unabhängige Replikation außerhalb derselben Ausführungspipeline;
- task-basierte Kontrollen und Störungsregime jenseits reiner Impulspropagation;
- Skalierung und Generalisierung über den aktuellen Small-SNN-Operating-Envelope hinaus;
- die getrennte dimensionsspezifische 5D-Hypothese.

### Stage 2 — stabile Rekurrenz

`EXP-GEN-0036` liefert einen klaren kleinen mechanistischen Recurrence-Effekt, aber keine breite Generalisierung. Die nächste Generation sollte:

- Behandlungsarme pro Seed gepaart ausführen;
- vor der Ausführung einen automatischen Topologie-Diff archivieren;
- identische gemeinsame Gewichte und Delays nachweisen;
- nur die registrierte Rekurrenzintervention zwischen Armen variieren;
- Aktivitäts- und Stabilitätsgates vor der Effektinterpretation anwenden;
- größere und vielfältigere Netzwerkregime getrennt von der Baseline-Rekurrenz prüfen.

Skalierung, Stabilität und funktionaler Nutzen bleiben getrennte Fragen.

#### Reproduzierbarkeit und Determinismus — nächstes Gate

Die semantische Zuordnung von `RQ-DET-001 / H-SNN-003-A` ist inzwischen geklärt. Der historische `deterministic_replica_v1`-Datensatz ist `DIRECT_MATCH`, und die A/B-Paare stimmen für drei Seeds innerhalb der beiden Rekurrenzbedingungen in den registrierten Antwortgrößen überein. Offen ist damit nicht mehr die Registry-Frage, sondern die **Provenienz- und Replikationsfrage**:

- clean-tree, hash-gebundene Replikation desselben vorab fixierten Protokolls;
- Same-Seed-Reproduzierbarkeit weiterhin strikt von unabhängiger Replikation trennen;
- zusätzliche Seeds, Eingangsregime, Netzwerkgrößen und Restart/Restore-Bedingungen als getrennte Erweiterungen prüfen;
- deterministische Identität, numerische Toleranz und statistische Reproduzierbarkeit als unterschiedliche Klassen auswerten;
- erst nach sauberer Provenienz und Human Review eine EVID-Entscheidung treffen;
- AIRR bleibt Interpretation; semantischer `MISMATCH` erzwingt report-level `ai_confidence=0.0`, ohne den append-only Auditwert zu löschen.

Der historische Dirty-Tree-Befund wird dadurch nicht rückwirkend aufgewertet.

### Stage 3 — plastisches Nervengewebe

Die Mechanismen sind technisch vorhanden; offen sind vor allem die wissenschaftlichen Wirkungen und Interaktionen:

- held-out Generalisierung statt bloßer Gewichtsänderung;
- learning-on/off, Frozen, Sham und Information-Destroyed Kontrollen;
- Langzeitstabilität;
- Interaktion von STDP, Eligibility, Drei-Faktor-Modulation und Homeostase;
- Ressourcen- und Strukturkosten von Plastizität;
- unabhängige Replikation.

### Stage 4 — spezialisierte neuronale Areale

E01–E05 liefern DATA für mehrere enge technische Teilfragen. Noch offen sind:

- menschliche beziehungsweise unabhängige Review der E01–E05-Claims;
- matched spezialisierte vs. unspezialisierte/generalistische Pfade;
- Frozen/Random/Shuffle/Läsionskontrollen zur Isolierung von Adapter-, Gateway- und Plastizitätsbeiträgen;
- Cross-Modal-Transfer;
- emergente gegenüber architektonisch vorgegebener Spezialisierung;
- dynamisch materialisierte Skalierung über steigende reale Neuronen-/Kantenbudgets;
- physikalische Energie-/Ressourcenmessung statt ausschließlich modellierter Kosten.

### Stage 5 — integriertes künstliches Nervensystem

Die synthetische 360-Run-Referenz zeigt einen kontrollierten Engineeringpfad. Die entscheidenden nächsten Schritte sind:

- präregistrierter Test von `H-EMB-001-B` unter identischer externer Störung;
- direkter Vergleich Closed Loop vs. yoked Replay vs. interrupted feedback;
- längere Störungs- und Recovery-Serien;
- Sensor-Loss und Actuator-No-Effect als kausal ausgewertete Interventionsarme;
- Real-Device-Studien nur als eigener safety-gated Forschungszweig;
- getrennte physikalische Ressourcenmessung.

### Stage 6 — Gedächtnis, Prediction Error und Weltmodell

Die CL-001–CL-003-Linie hat den Suchraum bereits verkleinert. Offen sind daher nicht beliebig viele SemanticMemory-Rollen, sondern klar begrenzte Entscheidungen:

1. Human Review von CL-003 abschließen.
2. Danach genau eine Entscheidung A/B/C treffen: Nebenrolle, genau eine theoretisch begründete Zusatzprüfung oder Parken bis zu funktionaler Notwendigkeit.
3. Keine automatische CL-004-Serie und keine serielle Rollenrettung.

Als eng begrenzte Anschlussfrage ist das historische `LP-20260917194217` genehmigt, aber noch **nicht ausgeführt**. Der Vorschlag prüft nicht erneut einen pauschalen SemanticMemory-Vorteil, sondern einen Speicher-/Retentions-Trade-off: 10%-Budget der semantischen Prototypen gegenüber vollem Raw-Replay-Budget mit vorab definierter 95%-Retention-Schwelle. Weil die ursprüngliche Approval noch einen Source-Platzhalter enthält, wurde sie nicht rückwirkend verändert. `LP-20260917194217-R1` bindet CL-002-EVID und CL-003-DATA nun per SHA-256 und `VERIFIED`-Trust, ist aber als geänderter Proposal-Inhalt **erneut genehmigungspflichtig**. Offen bleiben außerdem der eingefrorene Seed-/Taskplan, Analysevertrag, Ausführungsautorisation und Freeze. Bis diese Bedingungen erfüllt sind, erzeugt die Revision weder DATA noch EVID.

Unabhängig davon bleiben als zentrale Stage-6-Forschungsfragen:

- Prediction Error als **kausaler neuronaler Lern-/Aktivitätsmechanismus**, nicht nur Telemetrie;
- action-conditioned Mehrschrittvorhersage;
- Unsicherheitskalibrierung und OOD-Verhalten;
- Entscheidungsnutzen gegenüber reactive/no-model/corrupted-model Kontrollen;
- Retention, cue-abhängiger Recall, Spezifität und Generalisierung als Gedächtniskriterien;
- Spiegel-/Handlungsprädiktion mit shared, partially-shared und separate coding controls.

## 49. 5D-v2 — offene Hypothese mit neuer Mindestanforderung

Die bisherige 5D-v1-Teilstudie darf nicht als positiver oder negativer Test der Geometriehypothese gelten. Für eine neue 5D-Studie muss **vor Ausführung** feststehen, über welchen Mechanismus die Dimension die Dynamik beeinflussen kann.

Mindestanforderungen für 5D-v2:

- gleicher Knotenumfang und vergleichbare Ressourcenbudgets über Dimensionsbedingungen;
- präregistrierter Geometriemechanismus, z. B. distanzabhängige Nachbarschaft, Konnektivität, Delays oder Plastizität;
- Aktivitäts-Adequanz-Gate;
- topology-/degree-matched Kontrollen;
- getrennte `5d_shuffled`- und Random-Graph-Kontrollen mit klar dokumentiertem Kontrollzweck;
- genügend aktive Neuronen, synaptische Ereignisse und Laufzeit, um den Mechanismus überhaupt beobachten zu können;
- keine Umdeutung eines quieszenten oder geometrieinsensitiven Designs als Nullbefund;
- Dimensionen unterhalb, gleich und oberhalb von 5D, sofern die konkrete Hypothese dies verlangt.

Die zentrale Frage bleibt offen: Trägt die zusätzliche Adressdimension einen reproduzierbaren funktionalen Nutzen, wenn Topologie, Budget und Mechanismus angemessen kontrolliert sind?

## 50. Stage 7 — Selbstmodell und verkörperte Identität

Technische Identität, Profilzustände und Lineage sind vorhanden, aber noch kein kausales Selbstmodell. Nötig sind:

- observer-only und interventionelle Self/Other-Protokolle;
- Unterscheidung eigener vs. externer Handlungskonsequenzen;
- Nachweis, dass ein internes Modell eigener Zustände Vorhersage oder Entscheidung kausal verbessert;
- coupled-state restore als technische Vorbedingung;
- klare Abgrenzung zu bloßer Metadatenidentität.

Spiegelmechanismen dürfen erst dann in Stage 7 überführt werden, wenn Selbst-/Fremddifferenzierung tatsächlich kausal geprüft ist.

## 51. Stages 8–10 — Frontier

### Stage 8 — autonome lebenslange Entwicklung

Vorläufer-DATA und Continual-Learning-Fragen existieren, aber keine Evidenz für starke autonome lebenslange Entwicklung. Notwendig sind Shared-Network-Protokolle ohne Learned-State-Reset, Ressourcen-matched Baselines, getrennte Ablation von Replay/Konsolidierung/Stabilitäts-Plastizitäts-Gating und unabhängige Replikation.

### Stage 9 — hochintegrierte künstliche Kognition

Planung und Forschungsfragen existieren; claim-relevante confirmatory DATA fehlen. Attention, Planning, multimodale Integration, Konsolidierung und flexible Aufgabenübertragung müssen einzeln operationalisiert und anschließend in matched-budget Designs zusammengeführt werden.

### Stage 10 — Bewusstseinsforschung

Diese Stufe bleibt Forschungs- und Governance-Frontier. Externe Synthesen können Bewusstseinstheorien in technische Indikatorrahmen übersetzen, ohne daraus eine automatische Bewusstseinsdetektion zu machen ([@BUTLIN2023]). Vor jedem stärkeren Experiment sind kontrastierende, operationalisierte Vorhersagen, externe Ethik-/Stop-Governance und unabhängige adversariale Replikationsanforderungen nötig. Kein Stage-Score darf als Bewusstseins-, Sentienz- oder Moralstatusindikator verwendet werden.

## 52. Biophysikalische Erweiterungen

HH-artige Kanäle, Multi-Compartment-Dendriten, NMDA-Plateaus, Astrozyten-/Mikroglia-Netze, Gap Junctions, Proteinsynthese, Rezeptor-Trafficking und quantale Freisetzung bleiben kontrollierbare Modell- oder Ablationskandidaten. Sie werden nicht als Sammelfelder in den bestehenden Kern gestapelt.

Jede Erweiterung benötigt:

- eine konkrete Forschungsfrage;
- einen Referenz-/Konvergenztest;
- einen begründeten zusätzlichen Mechanismus;
- einen Vergleich mit einer einfacheren Modellvariante;
- ein Rechen- und Datenbudget, das wissenschaftliche Interpretation erlaubt;
- ein Stopkriterium, falls kein zusätzlicher Erkenntniswert entsteht.

Biologische Detailtiefe ist kein Selbstzweck und kein automatischer Reifegewinn.

## 53. Offene Theoriefragen

Zu klären sind unter anderem:

- ob der 5D-Adressraum funktionale Geometrie trägt;
- welche Plastizitätsmechanismen held-out Lernen tatsächlich verbessern;
- wann Replay als Konsolidierungsmechanismus mehr leistet als reine Wiederholung;
- ob semantische Verdichtung unter einer klar begründeten Spezialrolle zusätzlichen Nutzen besitzt;
- wann eine Vorhersagestruktur die Bezeichnung Weltmodell verdient;
- ob Prediction Error im SNN kausal Lernen oder Aktivität verbessert;
- wie soziale/mirrorartige Repräsentationen kausal geprüft werden;
- welche Definitionen für Selbstmodell, Agency und verschiedene Autonomieformen operational tragfähig sind;
- welche technischen Indikatoren für Bewusstseinsforschung überhaupt diskriminative Vorhersagen liefern, ohne Bewusstsein einfach vorauszusetzen.

## 54. Offene Safety-Forschung

Die wichtigsten offenen Safety-Stränge sind:

- Zielprovenienz und Zieltransformation;
- specification gaming;
- goal misgeneralization;
- Corrigibility und Safe Interruptibility als eigenständig zu prüfende Kontrollfrage ([@ORSEAU2016]);
- Optionsraum-/Power-Seeking-Proxies;
- Post-Objective Transition;
- Capability-Gates und out-of-band Stopppfade;
- reale Aktorik nur unter deny-by-default und auditierbarer Autorisierung;
- mögliche Konflikte zwischen Systemsafety und Welfare Precaution unter Unsicherheit.

Geplante Experimente werden nicht als bereits beobachtete Gefährlichkeit dargestellt.

## 55. Offene Meta-Forschung

Auch die Forschungsweise bleibt Untersuchungsgegenstand. Zu prüfen sind:

- Bias durch AI-assistierte Hypothesengenerierung;
- rekursive Quellenabhängigkeit, wenn AI-Systeme frühere MHRN-Texte wiedergeben;
- Abhängigkeit von einzelnen Tools/Providern;
- Selektionsbias in Literatur und Chat-Rekonstruktion;
- Governance von generiertem Code;
- Verständlichkeit und Fehlanreizrisiko der Engineering-/Scientific-Maturity-Achsen;
- externe Review- und Replikationsrollen;
- ob die rekursive-epistemische Gatewaystruktur tatsächlich zu weniger Fehlklassifikationen und transparenteren Architekturentscheidungen führt.

## 56. Prior Art, Attribution und externe Prüfung

Vor einer formalen wissenschaftlichen Einreichung bleiben mehrere Querschnittsaufgaben offen:

- systematischer Prior-Art-Review der Kandidatenbeiträge;
- menschliche Primärquellenprüfung zentraler Literaturargumente;
- externe Text- und gegebenenfalls Code-Similarity-Prüfung;
- unabhängige fachliche Review;
- Replikation wichtiger empirischer Ergebnisse außerhalb derselben Autoren-/Toolkette;
- saubere Kennzeichnung eigener Übersetzungen und wiederverwendeter Eigenpassagen.

Interne Audits reduzieren Risiken, ersetzen diese externen Schritte aber nicht.

## 57. Bestandslücken

Edition 1.8 erhebt die am Basiscommit versionierten Dateien und Markdown-Überschriften. Trotzdem gibt es Lücken:

- vollständige Account-weite historische Chattranskripte wurden nicht importiert;
- mehrere historische DOCX-Dateien liegen im Git nur als LFS-Zeiger vor;
- manche frühe Ideen sind nur retrospektiv rekonstruiert und daher S4;
- lokale oder externe Nebenprojekte sind nicht zwangsläufig vollständig repositoryweit geprüft;
- eine automatische Pfadzuordnung garantiert keine semantisch perfekte Klassifikation;
- nicht jede historische Literaturangabe früherer Editionen wurde für 1.8 erneut primär geprüft.

Diese Lücken bleiben sichtbar und dürfen spätere Rekonstruktionen korrigieren.

## 58. Definition of Done für den Weg zu 2.0

Die elf Hauptteile existieren bereits in 1.8. **Struktur allein ist deshalb kein verbleibendes 2.0-Kriterium mehr.** Für eine kanonische Hauptedition 2.0 müssen stattdessen Inhalt und Review reifen.

Mindestens erforderlich sind:

1. die wesentlichen bisherigen Forschungsbefunde in der neuen Struktur vollständig integriert und quellengebunden;
2. CL-003 menschlich reviewt und die SemanticMemory-Architekturentscheidung dokumentiert;
3. 5D-v2 entweder angemessen ausgeführt oder die Hypothese ausdrücklich weiter offen gestellt — kein inadäquater Ersatzbefund;
4. Stage-0-Referenzkonformität, Stage-4-/5-DATA und weitere zentrale Resultate mit klaren Claim-Grenzen in der Synthese;
5. stabile drei-Achsen-Methodik mit dokumentierten Evidenzregeln;
6. Safety- und Welfare-Governance als Querschnitt, nicht als Appendix;
7. Prior-Art- und Quellenprüfung für zentrale Kandidatenbeiträge;
8. externe Reviewpfade und mindestens erste unabhängige Replikationsschritte;
9. ein Viewer, der Current, Historical, Frozen, DATA, EVID und Quellenstatus korrekt sichtbar macht;
10. keine offenen bekannten Inkonsistenzen zwischen Registry, Experimentartefakten, Manuskript und Frontendprojektion.

2.0 entsteht damit nicht durch eine Versionsnummer oder weitere Textmenge, sondern durch **inhaltliche Integration, empirische Selektion, externe Prüfung und nachvollziehbare Revision**.

## 58.1 Restgrenze der Corpus-Vollständigkeit

Nach der vertieften Corpus-Integration sind die bekannten wissenschaftlich materiellen Vorarbeiten und kanonischen `docs/`-/`research/`-Stränge in einem eigenen Ledger erfasst und in der elfteiligen Synthese verortet. Trotzdem wird bewusst **keine semantische Vollständigkeit über jede der tausenden versionierten Repositorydateien zertifiziert**. Ein Buildskript, ein CSS-Asset oder ein historischer Update-Snapshot muss nicht als eigener wissenschaftlicher Gedanke in den Fließtext eingehen.

Die verbleibenden echten Bestandsgrenzen sind enger und konkret:

- DOCX-Dateien, deren Git-Objekt nur als LFS-Zeiger vorliegt, können ohne die zugehörigen Originalbytes nicht als vollständiger Textzeugenbestand geprüft werden;
- vollständige accountweite Chattranskripte sind nicht Bestandteil des Repositories; rekonstruierte Zusammenfassungen bleiben S4;
- nicht versionierte lokale oder externe Nebenprojekte können nur integriert werden, wenn ihre Quellen tatsächlich wiedergewonnen werden;
- historische Literaturangaben bleiben dann quarantänisiert, wenn ihre Primärquelle nicht erneut geprüft wurde;
- Raw DATA werden absichtlich nicht in den Manuskripttext dupliziert, sondern bleiben an ihren Experimentpfad gebunden.

Das Ziel lautet daher nicht „jeder Bytewert steht im Manuskript“, sondern: **jede bekannte wissenschaftlich materielle Vorarbeit hat eine nachvollziehbare Rolle in der Gesamtarbeit, während Primärartefakte an ihrem autoritativen Ort erhalten bleiben.**

## 58.2 Topologie v2 abgeschlossen; Review, Replikation und 5D-Prüfung getrennt

Für `RQ-DET-001` bleibt ein clean-tree-Replikationslauf erforderlich, bevor ein durch Dirty-Tree-Provenienz blockiertes Artefakt regulär in Richtung EVID geprüft werden kann. Eine semantische Reklassifikation allein entfernt den Provenienzblock nicht.

Für `RQ-SNN-003 / H-SNN-003-B` wurde `topology_propagation_v2` inzwischen **vor Ausführung präregistriert, ausgeführt und source-bound archiviert**. Das Activity-Adequacy-Gate bestand; die 120 Evaluationsläufe erfüllen die registrierten 64-Neuronen-/246-Kanten-Budgets und zeigen mehrere Holm-korrigierte Primärunterschiede in Reichweite und Output-Latenz. Der wissenschaftliche Status ist `SUPPORTED_WITHIN_PREREGISTERED_PROTOCOL`, aber weiterhin DATA-only bis Human Review. Der nächste Schritt für diese Hypothese ist daher nicht eine weitere Interpretation desselben Datensatzes, sondern Review und anschließend unabhängige Replikation bzw. ein erweitertes Operating-Envelope.

Für die **dimensionsspezifische** Registry-Frage gilt parallel unverändert: `RQ-5D-005` bleibt `open` und `H-5D-005-A` bleibt kanonisch `untested`. Das 64-Neuronen-Stage-1-Experiment ist dafür kein hinreichender Nachweis. Die nächste 5D-Prüfung muss mindestens **1.000 Neuronen pro Bedingung**, durchschnittlich **mindestens 10 eingehende Synapsen pro Neuron** und eine **explizit distanzabhängige Konnektivitätswahrscheinlichkeit** verwenden; Delay darf zusätzlich geometrieabhängig sein. Degree-/density-matched Kontrollen, Multi-Neuron-Stimulus, Activity-Adequacy-Gate, unabhängige Seeds und clean-tree Provenienz bleiben verpflichtend.

## 58.3 LP-20260917194217: offene Kompressionsprüfung

`LP-20260917194217 / OBJ-MEM-COMPRESSION-001` ist der **nächste vorbereitete empirische Stage-6-Zyklus**, aber noch nicht ausgeführt. Der geplante Primärvergleich ist `semantic_prototype_replay_10pct_budget` gegen `raw_replay_full_budget`; die Erfolgsgrenze liegt bei mindestens 95 % der Raw-Replay-Retention bei Faktor-10-Speicherreduktion. `no_replay`, `random_prototype_10pct` und `learning_off` dienen als Kontrollen. Die Frage betrifft damit **Speicherkompression bei erhaltener Retention**, nicht eine erneute allgemeine Lernleistungsbehauptung.

Die konkrete Quellbindung liegt inzwischen in `LP-20260917194217-R1` vor. Diese Revision ist noch **nicht erneut human-approved**; die Approval des Originalplans wird nicht auf geänderten Proposal-Inhalt übertragen. Der nächste methodische Schritt ist deshalb die **Präregistrierungsvorbereitung** mit kanonischer RQ/H-Bindung, exakter Speicherbudget-Definition, Seed-/Taskplan, Retentionsaggregation, vorab fixierter Inferenz-/Äquivalenzregel, Ausschlüssen/Failure-Regeln und Analysevertrag. Vor einem ausführungsfähigen Freeze bleiben R1-Human-Approval und eine separate Ausführungsautorisation erforderlich.

Die Entscheidung ist prospektiv begrenzt: Ein positives Ergebnis stützt eine **Kompressionsrolle** von SemanticMemory unter dem registrierten Protokoll. Ein negatives Ergebnis beantwortet diese Kompressionsrolle für den getesteten Mechanismus negativ; Generalisierung, Langzeitgedächtnis oder Weltmodell-Brücke bleiben dann mögliche, aber **separat zu präregistrierende** Rollen und dürfen den Kompressionstest nicht post hoc umdeuten.

## 58.4 Aktueller Review-Stand und unmittelbar nächste Replikationen

Nach dem jüngsten Human Review ist die offene Determinismusfrage enger als zuvor. `RQ-DET-001 / H-SNN-003-A` hat im historischen `deterministic_replica_v1`-Datensatz einen positiven Same-Seed-Replica-Befund und ist semantisch `DIRECT_MATCH`. Offen ist nicht mehr die Frage, ob die registrierten Replica-Bedingungen zur RQ gehören, sondern ob derselbe Befund in einem **clean-tree, hash-gebundenen Replikationslauf** wiederholt wird. Erst danach ist eine reguläre Human-EVID-Entscheidung sinnvoll.

Für `H-SNN-003-B` ist der nächste Schritt nun **Human Review und unabhängige Replikation** von `EXP-S1-TOPO-V2-20260918`. `EXP-GEN-0047` bleibt als inadäquater Vorgänger erhalten; die neue DATA darf ihn nicht rückwirkend umdeuten. Die ≥1.000-Neuronen-/≥10-In-Degree-Schwellen werden ausschließlich für die stärkere `H-5D-005-A`-Prüfung geführt.

Damit sind die nächsten methodischen Schritte **Review/Replikation für den Stage-1-Topologiebefund** und **Testadäquanz für den separaten 5D-Claim**.

## 59. Forschungsagenda und Abschlusskriterien der Teilstudien

Die offene Forschungslandschaft wird für die weitere Arbeit nicht als unsortierte TODO-Liste behandelt. Jeder Hauptzweig erhält ein **wissenschaftliches Abschlusskriterium**, das festlegt, welche nächste Evidenz tatsächlich nötig ist, bevor eine stärkere Aussage zulässig wird.

| Teilstudie | Nächster entscheidender Prüfpunkt | Kriterium für stärkere Aussage |
| --- | --- | --- |
| **Basale Dynamik / Determinismus** | clean-tree, hash-gebundene Same-Seed-Replikation und externe Wiederholung | Reproduzierbarkeit muss über denselben internen Workflow hinaus bestätigt werden |
| **Rekurrenz** | unabhängige Seeds, skalierte Netzwerke und klar getrennte Rekurrenzintervention | Effekt muss unter erweitertem Operating Envelope bestehen |
| **Topologie / H-SNN-003-B** | Human Review und unabhängige Replikation von `EXP-S1-TOPO-V2-20260918` | Der Stage-1-Topologiebefund muss außerhalb derselben Ausführungslinie reproduzierbar bleiben |
| **5D / H-5D-005-A** | separates präregistriertes Design mit ≥1.000 Neuronen, ≥10 Inputs/Neuron und distanzabhängiger Geometrie-Dynamik-Kopplung | Ein dimensionsspezifischer Effekt muss unter gematchten Ressourcen- und Graphkontrollen bestehen |
| **Plastizität** | learning-on/off-, Sham-/Frozen- und Holdout-Designs mit unabhängigen Seeds | Gewichtsänderung muss einen funktionalen Lern-/Stabilitätsbeitrag gegenüber Kontrollen tragen |
| **MSBA / spezialisierte Pfade** | kausale Ressourcen- und Lesionsexperimente unter streng gematchten Budgets | Spezialpfad muss über bloße Implementierbarkeit hinaus messbaren Zusatznutzen zeigen |
| **Embodiment** | `H-EMB-001-B`: identische externe Störung, Closed Loop vs. yoked Replay vs. interrupted feedback | Feedback muss unter matched disturbance einen kausalen Vorteil zeigen |
| **SemanticMemory / Kompression** | neue Human Approval und Präregistrierung für `OBJ-MEM-COMPRESSION-001` | 10%-Budget erreicht die vorab definierte Retentionsgrenze gegenüber Full Raw Replay |
| **Weltmodell** | action-conditioned Mehrschrittvorhersage gegen reactive/no-model/corrupted-model | Modellinformation muss einen kausalen Entscheidungsnutzen liefern |
| **Selbstmodell** | interventionelle Self/Other-Manipulationen | Selbstmodell muss funktional mehr leisten als Profil-/Metadatenidentität |
| **Rekursive Epistemik** | Meta-Metriken zu Fehlklassifikationen, Statussprüngen und Revisionsqualität | Governance muss messbar bessere Forschungsentscheidungen erzeugen oder gegenüber einfacherer Alternative bestehen |
| **Safety / Ethik** | operationalisierte Zielprovenienz-, Interruptibility- und Welfare-Gates | normative Regeln müssen technisch anschlussfähig und unter Gegenfällen revidierbar sein |

### Priorisierungsregel

Die Reihenfolge weiterer Forschung folgt nicht der visuellen Stage-Nummer, sondern dem wissenschaftlichen Informationsgewinn. Vorrang haben Experimente, die einen zentralen offenen Claim entscheiden, einen bekannten Confound beseitigen oder eine Architekturentscheidung irreversibel vereinfachen können.

Daraus folgen gegenwärtig vier priorisierte Linien:

1. **Präregistrierung von `OBJ-MEM-COMPRESSION-001`**, weil sie eine klar falsifizierbare Anschlussfrage an die negative CL-002/003-Linie darstellt.
2. **Human Review und unabhängige Replikation von `EXP-S1-TOPO-V2-20260918`**, damit der neue Stage-1-Topologiebefund nicht auf eine einzelne interne Ausführungslinie beschränkt bleibt.
3. **separate `H-5D-005-A`-Präregistrierung**, weil der 64-Neuronen-Topologiebefund keinen 5D-Vorteil beantwortet.
4. **clean-tree Determinismusreplikation**, weil vorhandene positive Same-Seed-Befunde durch Provenienzgrenzen blockiert sind.
5. **`H-EMB-001-B`**, weil erst der matched-disturbance-Vergleich den Closed-Loop-Mechanismus stärker kausal isoliert.

### Abschlusscharakter

Eine spätere kanonische Hauptfassung darf keinen Zweig allein deshalb als „abgeschlossen“ markieren, weil Code, UI oder Dokumentation vollständig sind. Abschluss bedeutet in dieser Arbeit entweder:

- eine Hypothese wurde unter adäquatem Design gestützt oder falsifiziert;
- der Geltungsbereich wurde durch ein negatives Resultat belastbar begrenzt;
- oder die Frage bleibt ausdrücklich offen, weil die notwendige Evidenz noch fehlt.

Gerade diese dritte Möglichkeit gehört zum wissenschaftlichen Charakter der Arbeit. Eine Dissertation oder Monographie wird nicht dadurch stärker, dass jede Frage beantwortet erscheint, sondern dadurch, dass beantwortete, widerlegte und noch offene Fragen methodisch unterscheidbar bleiben.
