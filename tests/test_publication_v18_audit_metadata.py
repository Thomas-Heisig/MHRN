"""Regression checks for the Edition 1.8 publication audit metadata."""

# fmt: off

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PUBLICATIONS = ROOT / "research" / "publications"
EDITION = PUBLICATIONS / "2026-09-17_recursive-epistemics_v1.8"
EXPECTED_LINEAGE = (
    "1.8 current WIP → 1.7 predecessor → "
    "1.5 frozen empirical baseline"
)


def test_visible_publication_pointers_are_edition_18() -> None:
    root = (ROOT / "README.md").read_text(encoding="utf-8")
    frozen = (PUBLICATIONS / "FROZEN_V1.5.md").read_text(
        encoding="utf-8"
    )
    assert "publication-1.8_WIP" in root
    assert EXPECTED_LINEAGE in root
    assert "1.8 (aktuelle WIP-Fortschreibung)" in frozen


def test_corrected_section_numbers_remain_unambiguous() -> None:
    part3 = (EDITION / "parts/03_research_object.md").read_text(
        encoding="utf-8"
    )
    assert "## 13.2 Eine zentrale Revision" in part3
    assert "## 13.3 Periphere Netze" in part3
    assert "## 13.4 Wesen" in part3
    headings = re.findall(r"^## (13\.\d+) ", part3, flags=re.MULTILINE)
    assert len(headings) == len(set(headings))

    part4 = (EDITION / "parts/04_empirical_programme.md").read_text(
        encoding="utf-8"
    )
    headings4 = re.findall(r"^## (19\.\d+) ", part4, flags=re.MULTILINE)
    assert len(headings4) == len(set(headings4))
    for expected in ("19.4", "19.5", "19.6", "19.7", "19.8"):
        assert expected in headings4


def test_claim_ledger_is_exposed_as_scientific_balance() -> None:
    ledger_path = EDITION / "registers/claim_ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in ledger["claims"]}
    assert len(by_id) == 7
    assert by_id["SYN-18-007"]["status"] == "open"
    assert by_id["SYN-18-002"]["status"] == (
        "DATA_interpretation_pending_review"
    )

    balance = (EDITION / "SCIENTIFIC_BALANCE.md").read_text(
        encoding="utf-8"
    )
    for claim_id in by_id:
        assert claim_id in balance
    assert "semantic_completeness_certified = false" in balance
    assert "complete_chat_archive_available = false" in balance
    assert "Nach dem **aktuellen Manifest der Edition 1.8**" in balance


def test_all_six_paper_offshoots_are_present_and_bounded() -> None:
    offshoot_path = ROOT / "research" / "paper_offshoots" / "README.md"
    offshoots = offshoot_path.read_text(encoding="utf-8")
    balance = (EDITION / "SCIENTIFIC_BALANCE.md").read_text(
        encoding="utf-8"
    )
    for number in range(1, 7):
        identifier = f"PO-{number:03d}"
        assert identifier in offshoots
        assert identifier in balance
    assert "keine DATA, keine EVID" in offshoots


def test_publication_and_software_cff_share_identity_and_license() -> None:
    software_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    publication_text = (EDITION / "CITATION.cff").read_text(
        encoding="utf-8"
    )
    software = yaml.safe_load(software_text)
    publication = yaml.safe_load(publication_text)

    assert publication["authors"] == software["authors"]
    assert publication["license"] == software["license"] == "MIT"
    assert publication["version"] == "1.8"
    assert publication["type"] == "dataset"
    assert publication["preferred-citation"]["type"] == "unpublished"
    assert publication["preferred-citation"]["authors"] == software["authors"]
    assert publication["preferred-citation"]["license"] == software["license"]


def test_manifest_completeness_boundary_is_not_overstated() -> None:
    manifest_text = (EDITION / "manifest.json").read_text(encoding="utf-8")
    manifest = json.loads(manifest_text)
    assert manifest["source_files"] == 9412
    assert manifest["indexed_sections"] == 18022
    assert manifest["complete_chat_archive_available"] is False
    assert manifest["semantic_completeness_certified"] is False
    assert manifest["material_prior_work_coverage_declared"] is True


def test_branch_context_is_preserved_before_cleanup() -> None:
    genealogy = (EDITION / "EDITION_GENEALOGY.md").read_text(
        encoding="utf-8"
    )
    expected = [
        (
            "docs/edition-1-8-corpus-integration",
            "633a16e15db9c2a4f4754a440a947bad8f1ebee8",
        ),
        (
            "docs/edition-1-8-current-reviews-20260918",
            "7d5ca56a5deb19b16e1eccc91f0746b783160750",
        ),
        (
            "docs/edition-1-8-current-state-20260918",
            "9f167c5b301191209228f18484a4ad7630b3e2a5",
        ),
        (
            "feat/publication-reader-complete-v18-20260918",
            "87f1364c558bdf8eb7824a319c22ed53a103479d",
        ),
        (
            "fix/learning-prep-provenance-ui-20260917",
            "426cc5a6642281d6221d70555d4043c9701735b5",
        ),
        (
            "research/edition18-reader-paths-offshoots-20260918",
            "29aadee2b796117a88ee8cfaf7d9ee2b509fe7f7",
        ),
        (
            "fix/publication-18-consistency-20260918",
            "87d0260e56dd9306590a4b8d929b881f8dd6f0c8",
        ),
    ]
    for name, sha in expected:
        assert name in genealogy
        assert sha in genealogy
    assert "PR #136" in genealogy
    assert "774671bcff753489f833b50bbdd3bea7ab3e3169" in genealogy


def test_historical_reader_is_explicitly_separated_from_current_viewer() -> None:
    notice = (PUBLICATIONS / "HISTORICAL_READER.md").read_text(
        encoding="utf-8"
    )
    legacy = (PUBLICATIONS / "reader" / "README.md").read_text(
        encoding="utf-8"
    )
    assert "7. September 2026" in notice
    assert "catalog.json" in notice
    assert "Edition 1.8" in notice
    assert "KI - Die geliehene Intelligenz" in legacy


def test_publication_citations_are_claim_near_and_source_typed() -> None:
    refs = json.loads((EDITION / "sources/references.json").read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in refs}
    required = {
        "APA2020", "ICMJE2026", "CREDIT2022", "BI_POO1998",
        "TURRIGIANO1998", "TURRIGIANO2008", "DIPELLEGRINO1992",
        "RIZZOLATTI2004", "KILNER2007", "NOSEK2018",
    }
    assert required.issubset(by_id)
    assert {row["source_class"] for row in refs} <= {
        "primary", "secondary", "guideline", "standard",
    }
    assert all(row.get("source_type") for row in refs)
    assert "et al." not in by_id["DALBA2025"]["apa"]
    assert "et al." not in by_id["SHI2025"]["apa"]
    assert "et al." not in by_id["NDRI2026"]["apa"]
    assert "et al." not in by_id["SUN2025"]["apa"]

    manuscript = (EDITION / "MANUSCRIPT.md").read_text(encoding="utf-8")
    for label in (
        "Bi & Poo, 1998", "Turrigiano et al., 1998",
        "di Pellegrino et al., 1992", "Nosek et al., 2018",
        "ICMJE, 2026", "NISO, 2022",
    ):
        assert label in manuscript
    assert "Autor und wissenschaftlich verantwortliche Person" in manuscript
    assert "Thomas Heisig" in manuscript


def test_scientific_balance_has_explicit_5d_and_compression_roadmaps() -> None:
    balance = (EDITION / "SCIENTIFIC_BALANCE.md").read_text(encoding="utf-8")
    assert "H-5D-005-A" in balance
    assert "Kanonisch bleibt `RQ-5D-005` **open** und `H-5D-005-A` **untested**." in balance
    assert "≥ 1.000 Neuronen pro Bedingung" in balance
    assert "≥ 10 eingehende Synapsen pro Neuron" in balance
    assert "distanzabhängige Konnektivitätswahrscheinlichkeit" in balance
    assert "OBJ-MEM-COMPRESSION-001" in balance
    assert "10 % des Raw-Replay-Speicherbudgets" in balance
    assert "mindestens 95 % der Retention" in balance
    assert "Präregistrierungsvorbereitung" in balance

# fmt: on


def test_publication_keeps_dissertation_research_architecture() -> None:
    manuscript = (EDITION / "MANUSCRIPT.md").read_text(encoding="utf-8")
    required = (
        "Forschungsproblem und monographische Gesamtarchitektur",
        "Übergeordnetes Forschungsproblem",
        "Zentrale Leitfrage",
        "Publikationsweite Syntheseproposition",
        "Teilstudie A — Basale Dynamik, Referenzkonformität und Determinismus",
        "Teilstudie B — Rekurrenz, Topologie und 5D-Geometrie",
        "Teilstudie C — Plastizität, Lernen und adaptive Stabilität",
        "Teilstudie D — Spezialisierte Pfade, Neural Symbiosis und MSBA",
        "Teilstudie E — Kontrolliertes synthetisches Embodiment",
        "Teilstudie F — Gedächtnis, Replay, semantische Verdichtung und Weltmodell",
        "RQ-EPIST-002 — Prozessgovernance als prüfbarer Forschungsgegenstand",
        "Normative Teilstudie — Forschungsfrage, Verfahren und Geltungsgrenzen",
        "Theorieentwicklungsstudie — Rekursive Epistemik als prüfbare Arbeitshypothese",
        "General Discussion",
        "Limitationen und interne Validität",
        "Externe Validität und Generalisierbarkeit",
        "Forschungsagenda und Abschlusskriterien der Teilstudien",
    )
    for item in required:
        assert item in manuscript
