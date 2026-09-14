# Stage 6: expliziter Referenz-Wiederaufbau

Status: implementierter Referenzpfad, keine kanonische Runtime-Migration und kein neuronaler Replay-/Konsolidierungsmechanismus. Implementierung: `src/memory/replay.py`; Tests: `tests/test_stage6_replay.py`.

## Warum kein automatisches Upgrade?

Das v1-Aggregat verlor Kategorie-Typen und Einfuegereihenfolge. Diese Information kann nicht verlaesslich aus Zaehlern rekonstruiert werden. v2-Praediktor und gekoppelter Speicher lehnen v1 deshalb weiterhin ab. Bestehende Dateien bleiben erhalten. Ein neuer Lauf oder der hier beschriebene Wiederaufbau ist eine neue, explizit dokumentierte Ableitung.

Der Wiederaufbau verlangt die gesamte Folge von Sensor-, Aktions-, Beobachtungs- und Steuersignalen ab Reset. Das ist besonders bei deaktiviertem Episodenschreiben wichtig: Der Praediktor kann weiterlernen, obwohl keine Episode gespeichert wird. Die begrenzte Dashboard-Exportdatei enthaelt diese Historie nicht und wird als Eingabe abgelehnt.

## Ausfuehrung

```bash
python -m src.memory.replay input-events.json NEW_OUTPUT_DIRECTORY --sha256 EXPECTED_SOURCE_SHA256
```

Der Elternordner muss existieren; das Zielverzeichnis darf noch nicht existieren. Den erwarteten Hash aus dem unabhaengig aufbewahrten Manifest uebernehmen. Ein unmittelbar aus derselben ungeprueften Datei berechneter Hash bestaetigt lediglich die Transportkonsistenz, nicht deren Herkunft. Der Aufruf schreibt weder die Quelle noch alte Snapshots um und aktiviert keine Geraete.

Die beiden Ergebnisdateien sind `state.json` (gekoppelter v2-Referenzzustand) und `provenance.json` (Quell-/Zustandshash, Hashes der Implementierungsdateien, Ereignis-/Episodenzahl und Grenzen). Nur ein Ergebnis mit vollstaendiger Provenienzdatei als abgeschlossen betrachten. Bei einem Schreibfehler kann ein unvollstaendiges NEUES Zielverzeichnis zurueckbleiben; fuer den naechsten Versuch ein anderes Ziel verwenden. Es gibt keinen atomaren Austausch einer Gruppe alter Dateien.

## Minimalbeispiel

```json
{
  "kind": "mhrn.cognition.replay",
  "schema_version": 1,
  "run_id": "reference-example",
  "complete_from_reset": true,
  "configuration": {
    "episode_capacity": 128,
    "working_capacity": 16,
    "prediction_capacity": 128,
    "retention_ticks": 1024,
    "max_contexts": 128
  },
  "events": [{
    "episode_id": "episode-0",
    "tick": 0,
    "frame": {"sensor_id": "digital-0", "tick": 0, "modality": "digital", "payload": {"cue": 1}},
    "action": null,
    "observation": {"tick": 1, "state": {"matched": false, "position": 0}, "reward": 0, "terminated": false, "truncated": false},
    "controls": {"read_enabled": true, "write_enabled": true, "prediction_enabled": true, "learning_enabled": true}
  }]
}
```

Jedes Objekt hat genau die gezeigten Felder. Eine Aktion ist `null` oder ein Objekt mit `actuator_id`, `tick`, `action`, `payload`. Beobachtungen duerfen `null` sein. Die vier Schalter werden vor jedem Ereignis angewendet. In jedem neu benannten Abschnitt beginnen Ticks bei null und steigen lueckenlos; Sensor-/Aktionstick stimmen mit dem Ereignis ueberein, Rueckmeldungen liegen bei Tick + 1. Nach `terminated` oder `truncated` ist eine neue Episoden-ID erforderlich. Eine bereits abgeschlossene Episoden-ID darf nicht wieder auftreten. Kein Ereignis wird sortiert, ergaenzt oder stillschweigend uebersprungen.

Grenzen: maximal 8 MiB Eingabe, 100000 Ereignisse; Kapazitaeten und Aufbewahrung zwischen 1 und 100000. Doppelte JSON-Schluessel, nicht-endliche Zahlen, als Zahlen uebergebene Booleans, unbekannte Protokollversionen und falsche Hashes werden zurueckgewiesen, bevor ein Zielverzeichnis entsteht. `complete_from_reset` ist **eine Deklaration der Quelle**, kein Beweis ihrer Vollstaendigkeit.

## Aussage und Grenzen

Vorhersage erfolgt vor Modellupdate. Nach jedem Ereignis kann der Zustand der direkten Referenzausfuehrung mit dem wiederaufgebauten Zustand verglichen werden; die Tests pruefen alle 16 Schalterkombinationen, Kapazitaetsverdraengung und anschliessende Fortsetzung. Dies zeigt keine SNN-interne Erinnerung, keine kanonische Checkpoint-Identitaet und keinen wissenschaftlichen Transfererfolg. Ein produktiver Logger, der diesen vollstaendigen Verlauf automatisch erzeugt, ist in diesem Schritt nicht enthalten. Ohne geeignete Historie bleibt nur ein ausdruecklich neuer Referenzlauf.
