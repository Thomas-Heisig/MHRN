#!/usr/bin/env python3
"""Deterministically assemble edition 1.8; never execute experiments or accept EVID."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import quote, unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
EDITION = "research/publications/2026-09-17_recursive-epistemics_v1.8"
PREVIOUS = "research/publications/2026-09-15_recursive-epistemics_v1.7"
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI")
OUTPUTS = (
    "MANUSCRIPT.md",
    "README.md",
    "REFERENCES.md",
    "references.bib",
    "SOURCE_INDEX.md",
    "RESEARCH_REGISTER.md",
    "LEGACY_V17.md",
    "manifest.json",
    "PRIOR_WORK_MAP.md",
    "registers/prior_work.json",
    "registers/section_inventory.json",
    "registers/source_inventory.json",
    "registers/creation_events.json",
    "registers/edition_genealogy.json",
    "registers/experiment_genealogy.json",
    "registers/research_objects.json",
    "registers/provenance.json",
    "registers/claim_ledger.json",
    "registers/preservation.json",
)
CITATION = re.compile(r"\[@([A-Za-z0-9_-]+)\]")
LINK = re.compile(r"(!?\[[^\]\n]*\]\()([^\s)]+)(\))")


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inside(root: Path, relative: str) -> Path:
    p = PurePosixPath(relative)
    if p.is_absolute() or ".." in p.parts or "\\" in relative:
        raise ValueError(f"Unsafe repository path: {relative}")
    t = root.joinpath(*p.parts).resolve()
    if not t.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes repository: {relative}")
    return t


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def load(root: Path, path: str) -> Any:
    return json.loads(inside(root, path).read_text(encoding="utf-8"))


def pinned_sources(root: Path, revision: str):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("baseline_commit must be a full Git commit")
    entries = []
    for line in git(root, "ls-tree", "-rz", "-r", revision).split(b"\0"):
        if not line:
            continue
        header, raw_path = line.split(b"\t", 1)
        mode, kind, sha = header.decode().split()
        if kind != "blob":
            raise ValueError("Submodules require a separate provenance contract")
        entries.append((raw_path.decode("utf-8"), mode, sha))
    shas = sorted({x[2] for x in entries})
    result = subprocess.run(
        ["git", "-C", str(root), "cat-file", "--batch"],
        input=("\n".join(shas) + "\n").encode(),
        capture_output=True,
        check=True,
    ).stdout
    blobs = {}
    offset = 0
    for expected in shas:
        end = result.index(b"\n", offset)
        sha, kind, size = result[offset:end].decode().split()
        offset = end + 1
        if sha != expected or kind != "blob":
            raise ValueError("Git batch response mismatch")
        blobs[sha] = result[offset : offset + int(size)]
        offset += int(size) + 1
    rows = []
    texts = {}
    for path, mode, sha in entries:
        content = blobs[sha]
        rows.append(
            {
                "path": path,
                "mode": mode,
                "git_blob": sha,
                "sha256": digest(content),
                "bytes": len(content),
            }
        )
        if path.startswith(("docs/", "research/")) and path.endswith(".md"):
            texts[path] = content
    return rows, texts


def route(path: str, config: dict[str, Any]):
    parts = []
    for rule in config["routing_rules"]:
        if re.search(rule["pattern"], path, re.IGNORECASE):
            parts.extend(rule["parts"])
    ordered = [p for p in ROMAN if p in parts]
    return (
        (ordered, "path_rule_requires_semantic_review")
        if ordered
        else (["XI"], "unclassified_source_retained_for_review")
    )


def relative_link(source: str, target: str) -> str:
    return quote(
        os.path.relpath(target, str(PurePosixPath(source).parent)).replace("\\", "/"),
        safe="/#._-",
    )


def rebase_links(
    text: str, source: str, destination: str, pinned: str | None = None
) -> str:
    def rewrite(m):
        url = m[2]
        parsed = urlsplit(url)
        if parsed.scheme or url.startswith("//"):
            return m[0]
        path, sep, fragment = url.partition("#")
        resolved = (
            os.path.normpath(str(PurePosixPath(source).parent / unquote(path))).replace(
                "\\", "/"
            )
            if path
            else source
        )
        if resolved.startswith(("../", "/")):
            raise ValueError(f"Link escapes repository in {source}: {url}")
        if pinned:
            target = f"https://github.com/Thomas-Heisig/MHRN/blob/{pinned}/" + quote(
                resolved, safe="/"
            )
        elif not path:
            return m[0]
        else:
            target = relative_link(destination, resolved)
        if sep:
            target += "#" + fragment
        return m[1] + target + m[3]

    return LINK.sub(rewrite, text)


def bibliography(refs):
    lookup = {}
    lines = [
        "# Literaturverzeichnis und Quellenstatus\n",
        "Autor-Jahr-Zitation nach APA 7; Identifikations- und Leseumfang werden getrennt ausgewiesen. Keine Volltext-, Prioritäts- oder Plagiatszertifizierung.\n",
    ]
    bib = []
    allowed = {
        "primary_metadata_checked",
        "primary_metadata_and_abstract_checked",
        "primary_text_checked",
        "official_guidance_checked",
    }
    for ref in refs:
        key = ref["id"]
        if (
            key in lookup
            or ref["verification"] not in allowed
            or not ref["url"].startswith("https://")
        ):
            raise ValueError(f"Invalid reference: {key}")
        lookup[key] = ref
        lines += [
            f'<a id="ref-{key}"></a>\n',
            ref["apa"] + "\n",
            f"Originalquelle: {ref['url']}  \nPrüfumfang: {ref['verification']}; geprüft am {ref['checked_on']}. {ref['scope']}\n",
        ]
        fields = {
            "author": ref["bib_author"],
            "title": ref["title"],
            "year": str(ref["year"]),
            "url": ref["url"],
            "note": ref["verification"],
        }
        if ref.get("doi"):
            fields["doi"] = ref["doi"]
        bib.append(
            "@misc{"
            + key
            + ",\n"
            + ",\n".join("  " + k + " = {" + v + "}" for k, v in fields.items())
            + "\n}\n"
        )
    return lookup, "\n".join(lines), "\n".join(bib)


def cite(text, refs):
    def repl(m):
        key = m[1]
        if key not in refs:
            raise ValueError(f"Unknown or quarantined citation: {key}")
        return f"[{refs[key]['label']}](REFERENCES.md#ref-{key})"

    return CITATION.sub(repl, text)


def registry_objects(root: Path):
    objects = []
    for filename in ("questions.yaml", "hypotheses.yaml", "claims.yaml"):
        path = "research/registry/" + filename
        if not (root / path).is_file():
            continue
        raw = (root / path).read_bytes()
        payload = yaml.safe_load(raw)

        def walk(value, pointer):
            if isinstance(value, dict):
                identifier = value.get("id")
                if isinstance(identifier, str) and re.match(
                    r"^(RQ|H|CL|CLAIM)-", identifier
                ):
                    prefix = identifier.split("-")[0]
                    kind = {"RQ": "research_question", "H": "hypothesis"}.get(
                        prefix, "claim"
                    )
                    parents = value.get("parent_ids", [])
                    if not parents:
                        parents = [
                            value[k]
                            for k in (
                                "question_id",
                                "research_question_id",
                                "rq_id",
                                "question",
                            )
                            if isinstance(value.get(k), str)
                            and value[k].startswith("RQ-")
                        ]
                    objects.append(
                        {
                            "id": identifier,
                            "axis": value.get("axis", "not_declared_in_source"),
                            "stage": value.get("stage"),
                            "object_type": kind,
                            "evidence_mode": "source_registry_projection_not_evidence",
                            "parent_ids": parents,
                            "publication_refs": ["IV", "XI"],
                            "status": value.get("status", "not_declared_in_source"),
                            "source_path": path,
                            "source_pointer": pointer,
                            "source_sha256": digest(raw),
                            "source_object": value,
                        }
                    )
                for k, item in value.items():
                    walk(
                        item,
                        pointer + "/" + str(k).replace("~", "~0").replace("/", "~1"),
                    )
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    walk(item, pointer + "/" + str(i))

        walk(payload, "")
    ids = [x["id"] for x in objects]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate canonical RQ/H/Claim identifiers")
    if not any(x["object_type"] == "research_question" for x in objects):
        raise ValueError("No research questions extracted")
    return sorted(objects, key=lambda x: x["id"])


def build(root: Path = ROOT):
    config = load(root, EDITION + "/edition.json")
    if config["version"] != "1.8" or [p["id"] for p in config["parts"]] != list(ROMAN):
        raise ValueError("Edition 1.8 requires all eleven ordered parts")
    refs, reference_md, bib = bibliography(
        load(root, EDITION + "/sources/references.json")
    )
    reconstruction = load(root, EDITION + "/sources/chat_reconstruction.json")
    for event in reconstruction["events"]:
        if (
            event["provenance_class"] != "S4"
            or event["raw_transcript_available"] is not False
        ):
            raise ValueError("Chat summaries cannot be promoted to primary transcripts")
    claims = load(root, EDITION + "/sources/synthesis_claims.json")
    for claim in claims:
        for field in (
            "id",
            "axis",
            "topic",
            "phase",
            "provenance_class",
            "status",
            "interpretation",
            "revision_criterion",
            "source_refs",
        ):
            if field not in claim:
                raise ValueError(
                    f"Incomplete synthesis claim: {claim.get('id')} / {field}"
                )
        if claim["status"] == "accepted_EVID":
            raise ValueError("The publication builder cannot accept evidence")
    prior = load(root, EDITION + "/sources/prior_work.json")
    baseline, source_texts = pinned_sources(root, config["baseline_commit"])
    legacy = {p: b for p, b in source_texts.items() if p.startswith(PREVIOUS + "/")}
    inventory = []
    protected = []
    changes = []
    sections = []
    for row in baseline:
        parts, method = route(row["path"], config)
        row = dict(
            row,
            publication_parts=parts,
            mapping_status=method,
            source_commit=config["baseline_commit"],
            evidence_role="source_artifact_not_automatically_evidence",
        )
        inventory.append(row)
        if row["path"].startswith("research/publications/20"):
            target = root / row["path"]
            if not target.is_file() or digest(target.read_bytes()) != row["sha256"]:
                changes.append(row["path"])
            protected.append({"path": row["path"], "sha256": row["sha256"]})
    if changes:
        raise ValueError("Historical publication changed: " + ", ".join(changes[:10]))
    for path, content in sorted(source_texts.items()):
        for number, line in enumerate(
            content.decode("utf-8", errors="replace").splitlines(), 1
        ):
            if re.match(r"^#{1,6}\s+", line):
                parts, method = route(path, config)
                sections.append(
                    {
                        "path": path,
                        "line": number,
                        "heading": line,
                        "publication_parts": parts,
                        "mapping_status": method,
                    }
                )
    objects = registry_objects(root)
    manuscript_path = EDITION + "/MANUSCRIPT.md"
    toc = [
        f"- [Teil {p['id']} — {p['title']}](#part-{p['id'].lower()})"
        for p in config["parts"]
    ]
    manuscript = [
        "# Rekursive Epistemik in verkörperten spikenden neuronalen Architekturen\n",
        "**Thomas Heisig · Edition 1.8 · current_wip · 17. September 2026**\n",
        "> Die elfteilige Zielstruktur 2.0 wird hier als Edition 1.8 umgesetzt. Kein Software-Release 2.0, kein Peer-Review-Siegel und keine neue Evidenzentscheidung.\n",
        "Vorgänger: [1.7](../2026-09-15_recursive-epistemics_v1.7/README.md). Unveränderte empirische Basis: [Frozen 1.5](../FROZEN_V1.5.md). [Erweiterungsvertrag](EXTENDING.md).\n",
        "## Inhaltsverzeichnis\n",
        "\n".join(toc) + "\n",
    ]
    inputs = {}
    for part in config["parts"]:
        path = EDITION + "/" + part["file"]
        raw = inside(root, path).read_bytes()
        if len(raw) < 1000:
            raise ValueError(f"Part {part['id']} is only a placeholder")
        inputs[path] = digest(raw)
        manuscript += [
            f'<a id="part-{part["id"].lower()}"></a>\n',
            cite(rebase_links(raw.decode("utf-8"), path, manuscript_path), refs),
            "\n---\n",
        ]
    manuscript += [
        "# Anhang — Quellen und Vorarbeiten\n",
        "[Alle Forschungsfragen und Hypothesen](RESEARCH_REGISTER.md) · [Quellenindex](SOURCE_INDEX.md) · [Ungekürzter Quellenband 1.7](LEGACY_V17.md) · [Weitere Vorarbeiten](PRIOR_WORK_MAP.md) · [Literatur](REFERENCES.md) · [Prüfmanifest](manifest.json).\n",
        "Die Quellenbestandsaufnahme belegt referenzierte Datei-Erhaltung am angegebenen Commit, nicht die vollständige semantische Erfassung jeder Idee. Die außerhalb des Repositories rekonstruierte Vorgeschichte ist ausdrücklich unvollständig.\n",
    ]
    index = [
        "# Quellenindex und 2.0-Zuordnung\n",
        f"Basis: `{config['baseline_commit']}`. {len(inventory)} versionierte Quelldateien. Pfadregeln sind Zuordnungsvorschläge, keine wissenschaftliche Anerkennung. Nicht klassifizierte Quellen bleiben in Teil XI sichtbar.\n",
        "| Quelle am Basiscommit | Teile | SHA-256 |\n|---|---|---|\n",
    ]
    for row in inventory:
        url = (
            "https://github.com/Thomas-Heisig/MHRN/blob/"
            + config["baseline_commit"]
            + "/"
            + quote(row["path"], safe="/")
        )
        index.append(
            f"| [{row['path'].replace('|','&#124;')}]({url}) | {', '.join(row['publication_parts'])} | `{row['sha256']}` |\n"
        )
    register = [
        "# Forschungsfragen, Hypothesen und Claims — Registry-Projektion\n",
        "Die Originalobjekte werden vollständig und ohne Statusänderung wiedergegeben. RQ-, Hypothesen- und Claim-Status bleiben getrennt. Fehlende Zuordnungen werden nicht erfunden.\n",
    ]
    for obj in objects:
        register += [
            f"## {obj['id']}\n",
            f"Typ: `{obj['object_type']}`; Quellstatus: `{obj['status']}`; Quelle: [{obj['source_path']}]({relative_link(EDITION+'/RESEARCH_REGISTER.md',obj['source_path'])}), JSON-Pointer `{obj['source_pointer']}`.\n",
            "```json\n" + json_text(obj["source_object"]) + "```\n",
        ]
    legacy_text = [
        "# Quellenband 1.7 — ungekürzte historische Vorfassung\n",
        "> Eigene Vorarbeiten von Thomas Heisig, keine neu erhobenen Ergebnisse. Historische Current-Vermerke und Prozentwerte beschreiben den damaligen Quellstand. Inline-Links sind an den Basiscommit gebunden; Originalbytes bleiben unverändert. Literatur der Vorfassung ist nicht automatisch neu verifiziert.\n",
    ]
    for path, content in sorted(legacy.items()):
        legacy_text += [
            f"## Historische Quelle: {PurePosixPath(path).name}\n",
            f"Quelle: `{path}`; SHA-256: `{digest(content)}`.\n",
            rebase_links(
                content.decode("utf-8"),
                path,
                EDITION + "/LEGACY_V17.md",
                config["baseline_commit"],
            ),
            "\n---\n",
        ]
    prior_map = [
        "# Vorarbeiten und wissenschaftliche Anschlussstellen\n",
        "Die Zuordnung erhält Themen; sie bestätigt weder alte Befunde noch externe Quellen. Nicht verfügbare Originalbytes/Formeln bleiben als Importlücke sichtbar.\n",
    ]
    for item in prior["works"]:
        prior_map += [
            f"## {item['id']} — {item['title']}\n",
            f"Autor: {item['author']}; Datierung: {item['date']}; Zugang: {item['access']}; Originalbytes verfügbar: {item['original_bytes_available']}.\n",
            item["boundary"] + "\n",
        ]
        for mapping in item["topic_map"]:
            prior_map.append(
                f"- {mapping['topic']} → Teile {', '.join(mapping['parts'])}. Weiterführung: {mapping['continuation']}\n"
            )
    history = []
    for record in (
        git(
            root,
            "log",
            "--reverse",
            "--format=%H%x1f%aI%x1f%cI%x1f%s",
            config["baseline_commit"],
        )
        .decode()
        .splitlines()
    ):
        sha, authored, committed, subject = record.split("\x1f", 3)
        history.append(
            {
                "id": "GIT-" + sha,
                "commit": sha,
                "author_date": authored,
                "committer_date": committed,
                "subject": subject,
                "provenance_class": "S1",
                "supports": "repository_event_not_date_of_idea_inception",
            }
        )
    exp = {}
    for row in inventory:
        m = re.match(r"research/experiments/([^/]+)/", row["path"])
        if m:
            exp.setdefault(m[1], []).append(row["path"])
    old_catalog = json.loads(
        git(
            root,
            "show",
            config["baseline_commit"] + ":research/publications/catalog.json",
        )
    )
    current_id = "PUB-RECURSIVE-EPISTEMICS-20260917-V1.8"
    outputs = {
        "MANUSCRIPT.md": "\n".join(manuscript),
        "README.md": "# Recursive Epistemics / Rekursive Epistemik — Edition 1.8\n\n**current_wip; Interpretation und Forschungsprogramm; keine automatische EVID.**\n\n[Gesamtmanuskript](MANUSCRIPT.md) · [RQs/Hypothesen](RESEARCH_REGISTER.md) · [Quellenindex](SOURCE_INDEX.md) · [Quellenband 1.7](LEGACY_V17.md) · [Vorforschung](PRIOR_WORK_MAP.md) · [Literatur](REFERENCES.md) · [Erweiterungsvertrag](EXTENDING.md) · [Manifest](manifest.json)\n\n"
        + "\n".join(
            f"- [Teil {p['id']} — {p['title']}]({p['file']})" for p in config["parts"]
        )
        + "\n\n[Vorgänger 1.7](../2026-09-15_recursive-epistemics_v1.7/README.md); [Frozen 1.5](../FROZEN_V1.5.md). Strukturmigration ist kein empirisches Ergebnis.\n",
        "REFERENCES.md": reference_md,
        "references.bib": bib,
        "SOURCE_INDEX.md": "".join(index),
        "RESEARCH_REGISTER.md": "\n".join(register),
        "LEGACY_V17.md": "\n".join(legacy_text),
        "PRIOR_WORK_MAP.md": "\n".join(prior_map),
        "registers/prior_work.json": json_text(prior),
        "registers/section_inventory.json": json_text(
            {
                "baseline_commit": config["baseline_commit"],
                "scope": "all_markdown_headings_in_docs_and_research_at_baseline",
                "sections": sections,
            }
        ),
        "registers/source_inventory.json": json_text(
            {
                "baseline_commit": config["baseline_commit"],
                "scope": "all_tracked_repository_files_at_baseline",
                "semantic_completeness_certified": False,
                "files": inventory,
            }
        ),
        "registers/creation_events.json": json_text(
            {
                "scope": "all_commits_reachable_from_baseline",
                "events": history,
                "chat_reconstruction": reconstruction["events"],
            }
        ),
        "registers/edition_genealogy.json": json_text(
            {
                "source_commit": config["baseline_commit"],
                "historical_catalog": old_catalog,
                "current_edition": {
                    "id": current_id,
                    "version": "1.8",
                    "predecessor": "PUB-RECURSIVE-EPISTEMICS-20260915-V1.7",
                },
            }
        ),
        "registers/experiment_genealogy.json": json_text(
            {
                "relation_policy": "explicit_editorial_links_only_no_inferred_run_parentage",
                "experiments": exp,
                "editorial_question_refinement": config["experiment_relations"],
            }
        ),
        "registers/research_objects.json": json_text(
            {"schema_version": "1.0", "objects": objects}
        ),
        "registers/provenance.json": json_text(reconstruction),
        "registers/claim_ledger.json": json_text(
            {
                "authority": "publication_synthesis_not_canonical_evidence_registry",
                "claims": claims,
            }
        ),
        "registers/preservation.json": json_text(
            {
                "baseline_commit": config["baseline_commit"],
                "historical_publications_byte_identical": True,
                "protected_files": protected,
                "historical_data_reinterpreted": False,
                "limitation": "Byte preservation does not certify completeness of interpretation.",
            }
        ),
    }
    for filename in (
        "edition.json",
        "sources/references.json",
        "sources/chat_reconstruction.json",
        "sources/synthesis_claims.json",
        "sources/prior_work.json",
        "EXTENDING.md",
    ):
        inputs[EDITION + "/" + filename] = digest(
            inside(root, EDITION + "/" + filename).read_bytes()
        )
    inputs["scripts/build_publication_edition.py"] = digest(
        (root / "scripts/build_publication_edition.py").read_bytes()
    )
    outputs["manifest.json"] = json_text(
        {
            "schema_version": "1.0",
            "id": current_id,
            "version": "1.8",
            "date": config["date"],
            "edition_status": "current_wip",
            "structure": "eleven_part_2.0_structure_in_1.8",
            "baseline_commit": config["baseline_commit"],
            "predecessor_edition": PREVIOUS,
            "viewer_entrypoint": "MANUSCRIPT.md",
            "historical_data_modified": False,
            "accepted_evidence": False,
            "automatic_evidence_promotion": False,
            "inherited_campaign": "EXP-EMP-20260913-A3",
            "input_sha256": inputs,
            "output_sha256": {n: digest(t.encode()) for n, t in outputs.items()},
            "source_files": len(inventory),
            "historical_publications_preserved": len(protected),
            "creation_events": len(history),
            "research_objects": len(objects),
            "prior_works": len(prior["works"]),
            "indexed_sections": len(sections),
            "complete_chat_archive_available": False,
            "semantic_completeness_certified": False,
        }
    )
    if set(outputs) != set(OUTPUTS):
        raise ValueError("Generated output contract mismatch")
    return outputs


def materialize(root: Path = ROOT, check: bool = False):
    outputs = build(root)
    mismatches = []
    for relative, text in outputs.items():
        path = root / EDITION / relative
        data = text.encode()
        if check:
            if not path.is_file() or path.read_bytes() != data:
                mismatches.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if mismatches:
        raise ValueError("Stale/missing publication outputs: " + ", ".join(mismatches))
    m = json.loads(outputs["manifest.json"])
    return {
        "result": "PASS",
        "mode": "check" if check else "write",
        "generated_files": len(outputs),
        "source_files": m["source_files"],
        "preserved_publication_files": m["historical_publications_preserved"],
        "research_objects": m["research_objects"],
        "creation_events": m["creation_events"],
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    p.add_argument("--write", action="store_true")
    a = p.parse_args()
    if a.check == a.write:
        p.error("Choose exactly one of --check or --write")
    try:
        print(json_text(materialize(check=a.check)))
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        p.exit(1, f"Publication integrity failure: {e}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
