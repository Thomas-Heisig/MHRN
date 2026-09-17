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

Stage 1 benötigt vor allem eine stärkere Forschungsbasis jenseits technischer Signalweitergabe:

- eigene präregistrierte Small-Network-RQ/Hypothesen;
- task-basierte Kontrollen statt nur Funktionsverifikation;
- Störungs- und Topologievariationen;
- unabhängige Replikation.

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

Die EXP-GEN-0045/0046-DATA schließen die Frage nicht vollständig. Als nächste Schritte sind erforderlich:

- semantische Zuordnungsregel für `RQ-DET-001` registrieren und EXP-GEN-0046 human reviewen;
- Same-Seed-Reproduzierbarkeit von echter unabhängiger Replikation getrennt halten;
- zusätzliche Seeds, Eingangsregime, Netzwerkgrößen und Restart/Restore-Bedingungen prüfen;
- deterministische Identität, numerische Toleranz und statistische Reproduzierbarkeit als getrennte Klassen auswerten;
- AIRR-Interpretation nicht als EVID verwenden, solange Human Review und semantisches Gate offen sind.

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

Diese Stufe bleibt Forschungs- und Governance-Frontier. Vor jedem stärkeren Experiment sind kontrastierende, operationalisierte Vorhersagen, externe Ethik-/Stop-Governance und unabhängige adversariale Replikationsanforderungen nötig. Kein Stage-Score darf als Bewusstseins-, Sentienz- oder Moralstatusindikator verwendet werden.

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
- Corrigibility und Safe Interruptibility;
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
