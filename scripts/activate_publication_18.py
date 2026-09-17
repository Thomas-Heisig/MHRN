#!/usr/bin/env python3
"""Activate publication edition 1.8 without changing software or evidence state."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NEW = "research/publications/2026-09-17_recursive-epistemics_v1.8"
OLD = "research/publications/2026-09-15_recursive-epistemics_v1.7"
NEW_ID = "PUB-RECURSIVE-EPISTEMICS-20260917-V1.8"
OLD_ID = "PUB-RECURSIVE-EPISTEMICS-20260915-V1.7"


def load(path: str) -> dict[str, Any]:
    value = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(path)
    return value


def save(path: str, value: Any) -> None:
    (ROOT / path).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def prepend_once(path: str, marker: str, block: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if marker not in text:
        target.write_text(block + "\n\n" + text, encoding="utf-8")


def main() -> None:
    catalog = load("research/publications/catalog.json")
    publications = catalog.get("publications", [])
    if not isinstance(publications, list):
        raise TypeError("catalog publications")
    by_id = {item.get("id"): item for item in publications if isinstance(item, dict)}
    if OLD_ID not in by_id:
        raise ValueError("Expected edition 1.7 predecessor is missing")
    current = [
        item.get("id")
        for item in publications
        if isinstance(item, dict) and item.get("current")
    ]
    if current not in ([OLD_ID], [NEW_ID]):
        raise ValueError(f"Unexpected current publication: {current}")

    predecessor = dict(by_id[OLD_ID])
    new_entry = dict(predecessor)
    new_entry.update(
        id=NEW_ID,
        version="1.8",
        date="2026-09-17",
        current=True,
        edition_status="current_wip",
        predecessor=OLD_ID,
        entrypoint=NEW.removeprefix("research/") + "/MANUSCRIPT.md",
        reader=NEW.removeprefix("research/") + "/MANUSCRIPT.md",
        snapshot=NEW.removeprefix("research/"),
        manifest=NEW.removeprefix("research/") + "/manifest.json",
    )
    updated = []
    for item in publications:
        if not isinstance(item, dict) or item.get("id") == NEW_ID:
            continue
        item = dict(item)
        item["current"] = False
        if item.get("id") == OLD_ID:
            item["edition_status"] = "historical_integrative_predecessor"
        updated.append(item)
    catalog["publications"] = [new_entry] + updated
    catalog["current_publication_id"] = NEW_ID
    catalog["current_publication"] = NEW_ID
    catalog["current_entrypoint"] = new_entry["entrypoint"]
    save("research/publications/catalog.json", catalog)

    identity = load("project_identity.json")
    publication = identity.get("publication")
    if not isinstance(publication, dict):
        raise TypeError("project_identity publication")
    publication.update(
        edition="1.8",
        edition_status="current_wip",
        path=NEW,
        viewer_entrypoint=NEW + "/MANUSCRIPT.md",
        predecessor=OLD,
    )
    save("project_identity.json", identity)

    (ROOT / "research/publications/CURRENT.md").write_text(
        "# Aktuelle wissenschaftliche Arbeitsfassung\n\n"
        "**Recursive Epistemics / Rekursive Epistemik 1.8 - current_wip**\n\n"
        "[Gesamtmanuskript](2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md) | "
        "[Kapitel und Register](2026-09-17_recursive-epistemics_v1.8/README.md)\n\n"
        "Edition 1.8 setzt die fuer 2.0 geplante elfteilige Struktur bereits als "
        "Arbeitsfassung um. Das ist weder ein Software-Release 2.0 noch eine neue "
        "Evidenzentscheidung.\n\n"
        "[Vorgaenger 1.7](2026-09-15_recursive-epistemics_v1.7/README.md) | "
        "[Frozen empirical baseline 1.5](FROZEN_V1.5.md)\n",
        encoding="utf-8",
    )

    prepend_once(
        "README.md",
        "<!-- publication-current-1.8 -->",
        "<!-- publication-current-1.8 -->\n"
        "## Scientific publication: edition 1.8 WIP\n\n"
        "The eleven-part structure planned for publication 2.0 is implemented now as "
        "**edition 1.8 WIP**, independently of the MHRN software version. It integrates "
        "the reconstructed prehistory, architecture, empirical programme, engineering, "
        "epistemology, attribution, ethics, recursive epistemics and open research.\n\n"
        "- [Current manuscript](research/publications/2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md)\n"
        "- [Research questions and hypotheses](research/publications/2026-09-17_recursive-epistemics_v1.8/RESEARCH_REGISTER.md)\n"
        "- [Complete baseline source inventory](research/publications/2026-09-17_recursive-epistemics_v1.8/SOURCE_INDEX.md)\n"
        "- [Unabridged 1.7 source volume](research/publications/2026-09-17_recursive-epistemics_v1.8/LEGACY_V17.md)\n"
        "- [Prior research map](research/publications/2026-09-17_recursive-epistemics_v1.8/PRIOR_WORK_MAP.md)\n"
        "- [Extension and citation contract](research/publications/2026-09-17_recursive-epistemics_v1.8/EXTENDING.md)\n\n"
        "Historical publication bytes and empirical artifacts are preserved. Reconstructed "
        "chat history remains S4 until original messages are source-bound.",
    )
    prepend_once(
        "docs/README.md",
        "<!-- publication-current-1.8 -->",
        "<!-- publication-current-1.8 -->\n> Aktuelle wissenschaftliche Arbeitsfassung: "
        "[Edition 1.8](../research/publications/2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md). "
        "Aeltere Editionsangaben dokumentieren ihren damaligen Stand.",
    )
    prepend_once(
        "research/README.md",
        "<!-- publication-current-1.8 -->",
        "<!-- publication-current-1.8 -->\n> Aktuelle wissenschaftliche Arbeitsfassung: "
        "[Edition 1.8](publications/2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md). "
        "Registry, DATA und EVID behalten ihre getrennten Autoritaeten.",
    )
    prepend_once(
        "research/publications/README.md",
        "<!-- publication-current-1.8 -->",
        "<!-- publication-current-1.8 -->\n> Current WIP: "
        "[Edition 1.8](2026-09-17_recursive-epistemics_v1.8/MANUSCRIPT.md). "
        "Frozen 1.5 und alle Vorgaenger bleiben erreichbar.",
    )
    prepend_once(
        "docs/08-roadmap/V2_PUBLICATION_STRUCTURE_MIGRATION.md",
        "<!-- edition-1.8-implementation -->",
        "<!-- edition-1.8-implementation -->\n> **Fortschreibung 17.09.2026:** Auf ausdruecklichen Autorenauftrag wird die "
        "elfteilige Zielstruktur bereits als **1.8 WIP** implementiert. Diese Entscheidung "
        "ersetzt die fruehere zeitliche Bedingung 'erst ab 2.0', nicht die Erhaltungs-, "
        "Provenienz- und Evidenzregeln. Die urspruengliche Planung bleibt nachfolgend erhalten.",
    )

    governance = load("research/document_governance_overrides.json")
    overrides = governance.get("overrides")
    if not isinstance(overrides, dict):
        raise TypeError("document governance overrides")
    overrides[NEW] = {
        "kind": "publication",
        "status": "current_wip",
        "authority": "publication_interpretation",
        "mutability": "editable",
        "citation": "cite_edition_path_and_git_revision",
        "evidence_role": "interpretation_not_automatic_evidence",
        "rationale": "Current edition 1.8; structure change does not promote evidence.",
    }
    overrides[OLD] = {
        "kind": "publication",
        "status": "historical",
        "authority": "publication_interpretation",
        "mutability": "immutable_historical_snapshot",
        "citation": "cite_edition_path_and_git_revision",
        "evidence_role": "interpretation_not_automatic_evidence",
        "rationale": "Edition 1.7 predecessor retained unchanged.",
    }
    overrides[NEW + "/registers"] = {
        "kind": "generated",
        "status": "generated",
        "authority": "generated_projection",
        "mutability": "regenerable",
        "citation": "cite_underlying_source_and_revision",
        "evidence_role": "projection_not_evidence_by_itself",
        "rationale": "Deterministic publication projections, not canonical EVID.",
    }
    save("research/document_governance_overrides.json", governance)

    checker = ROOT / "scripts/check_scientific_maturity_integrity.py"
    text = checker.read_text(encoding="utf-8")
    text = text.replace(
        'V17 = "research/publications/2026-09-15_recursive-epistemics_v1.7"',
        'V18 = "research/publications/2026-09-17_recursive-epistemics_v1.8"\nV17 = "research/publications/2026-09-15_recursive-epistemics_v1.7"',
    )
    text = text.replace(
        'item.get("version") == "1.7",\n            "current publication must be edition 1.7",',
        'item.get("version") == "1.8",\n            "current publication must be edition 1.8",',
    )
    text = text.replace(
        'item.get("entrypoint", "").endswith("v1.7/MANUSCRIPT.md"),\n            "Publication Viewer must open the current v1.7 manuscript",',
        'item.get("entrypoint", "").endswith("v1.8/MANUSCRIPT.md"),\n            "Publication Viewer must open the current v1.8 manuscript",',
    )
    text = text.replace(
        'item.get("predecessor") == "PUB-RECURSIVE-EPISTEMICS-20260915-V1.6",\n            "edition 1.7 predecessor mismatch",',
        'item.get("predecessor") == "PUB-RECURSIVE-EPISTEMICS-20260915-V1.7",\n            "edition 1.8 predecessor mismatch",',
    )
    text = text.replace(
        'isinstance(publication, dict) and publication.get("edition") == "1.7",',
        'isinstance(publication, dict) and publication.get("edition") == "1.8",',
    )
    text = text.replace(
        '"project identity publication edition mismatch",',
        '"project identity publication edition mismatch",',
    )
    required_marker = '        f"{V17}/MANUSCRIPT.md",'
    if required_marker in text and 'f"{V18}/MANUSCRIPT.md"' not in text:
        text = text.replace(
            required_marker, '        f"{V18}/MANUSCRIPT.md",\n' + required_marker
        )
    manuscript_marker = '    manuscript = (ROOT / V17 / "MANUSCRIPT.md").read_text(encoding="utf-8").lower()'
    if manuscript_marker in text:
        text = text.replace(
            manuscript_marker,
            '    manuscript = (ROOT / V18 / "MANUSCRIPT.md").read_text(encoding="utf-8").lower()',
        )
    checker.write_text(text, encoding="utf-8")

    (ROOT / NEW / "CITATION.md").write_text(
        "# Diese Arbeitsfassung zitieren\n\n"
        "Heisig, T. (2026). *Rekursive Epistemik in verkoerperten spikenden neuronalen "
        "Architekturen* (Edition 1.8, Arbeitsmanuskript). MHRN.\n\n"
        "Ergaenzen: exakter Git-Commit, Kapitel/Abschnitt und Abrufdatum. Fuer Vorfassungen "
        "deren Edition und Ursprungspfad nennen. Kein behaupteter DOI und kein behauptetes "
        "Peer Review. Die Software wird unabhaengig ueber CITATION.cff im Repository-Root zitiert.\n",
        encoding="utf-8",
    )
    print(
        "Publication 1.8 activated; software version and evidence registries unchanged."
    )


if __name__ == "__main__":
    main()
