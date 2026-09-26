"""Deterministic projections for the MHRN research-system taxonomy.

This module is descriptive only. It never executes studies, changes DATA/EVID status,
or infers the names of the human-defined eleven research directions.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
RQ_RE = re.compile(r"\bRQ-[A-Z0-9]+-[0-9]+\b")
H_RE = re.compile(r"\bH-[A-Z0-9]+-[0-9]+-[A-Z0-9]+\b")
AXES = {
    "empirical_technical",
    "epistemological_methodological",
    "philosophical_ethical",
    "unclassified",
}


def _json_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _read(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return json.loads(text)


def _registry_family(root: Path, stem: str, key: str = "id") -> dict[str, dict[str, Any]]:
    registry = root / "research" / "registry"
    paths = sorted(set(registry.glob(f"{stem}.yaml")) | set(registry.glob(f"{stem}.*.yaml")))
    merged: dict[str, dict[str, Any]] = {}
    for path in paths:
        data = _read(path) or []
        if not isinstance(data, list):
            raise ValueError(f"Registry family must contain lists: {path}")
        for item in data:
            ident = item[key]
            if ident in merged:
                raise ValueError(f"Duplicate registry identifier {ident}: {path}")
            merged[ident] = dict(item, source_path=path.relative_to(root).as_posix())
    return merged


def validate_direction_registry(data: dict[str, Any], lock: dict[str, Any]) -> None:
    if data.get("expected_count") != 11 or lock.get("expected_count") != 11:
        raise ValueError("The canonical research map must preserve exactly eleven directions.")
    entries = data.get("directions") or []
    assignments = data.get("assignments") or {}
    if data.get("status") == "awaiting_canonical_source":
        if entries or assignments or lock.get("identity_digest") is not None:
            raise ValueError("Unresolved direction names/order cannot carry invented identities.")
        return
    if data.get("status") != "source_bound" or len(entries) != 11:
        raise ValueError("Activated direction registry requires exactly 11 source-bound entries.")
    identities = []
    ids: set[str] = set()
    for item in entries:
        for field in ("id", "title", "source_ref"):
            if not item.get(field):
                raise ValueError(f"Direction entry lacks {field}")
        if item["id"] in ids:
            raise ValueError(f"Duplicate direction ID: {item['id']}")
        ids.add(item["id"])
        identities.append({k: item[k] for k in ("id", "title", "source_ref")})
    if _json_digest(identities) != lock.get("identity_digest"):
        raise ValueError("Direction identities/order differ from the human-bound lock.")
    if not lock.get("human_decision_ref"):
        raise ValueError("Activated direction registry requires a human governance reference.")
    unknown = set(assignments.values()) - ids
    if unknown:
        raise ValueError(f"Unknown direction assignments: {sorted(unknown)}")


class MetaSystem:
    """Build read-only crosswalk and taxonomy projections."""

    def __init__(self, root: Path = ROOT) -> None:
        self.root = root
        self.system = _read(root / "research/meta/system.json")
        self.directions = _read(root / "research/registry/directions.yaml")
        self.direction_lock = _read(root / "research/registry/directions.lock.json")
        validate_direction_registry(self.directions, self.direction_lock)
        self.coordinates = _read(root / "research/meta/question_coordinates.json")
        self.questions = _registry_family(root, "questions")
        self.hypotheses = _registry_family(root, "hypotheses")
        self.sources = _registry_family(root, "sources", "source_id")
        self.claims = _registry_family(root, "claims")
        self.edition_root = root / self.system["edition_path"]
        self.edition = _read(self.edition_root / "edition.json")
        self.parts = list(self.edition["parts"])
        self.progress = _read(root / "src/dashboard/static/scientific-progress.json")
        self.stages = list(self.progress["stages"])
        self.studies = [
            _read(path)
            for path in sorted((root / "research/meta/studies").glob("*.json"))
        ]
        self.part_questions = self._part_question_index()
        self.experiments = self._experiment_index()
        self.evidence = self._evidence_index()
        self.papers = self._paper_index()
        self.review_queue = self._review_queue()
        self.rows = self._crosswalk()
        self._validate()

    def _part_question_index(self) -> dict[str, set[str]]:
        result: dict[str, set[str]] = {}
        known = set(self.questions)
        for part in self.parts:
            text = (self.edition_root / part["file"]).read_text(encoding="utf-8")
            result[part["id"]] = set(RQ_RE.findall(text)) & known
        return result

    def _experiment_index(self) -> dict[str, set[str]]:
        result: dict[str, set[str]] = {qid: set() for qid in self.questions}
        exp_root = self.root / "research" / "experiments"
        for manifest in sorted(exp_root.glob("*/manifest.json")):
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            text = json.dumps(
                {
                    "research_question": data.get("research_question"),
                    "research_questions": data.get("research_questions"),
                    "hypothesis": data.get("hypothesis"),
                    "hypotheses": data.get("hypotheses"),
                }
            )
            qids = set(RQ_RE.findall(text))
            for hid in H_RE.findall(text):
                hypothesis = self.hypotheses.get(hid)
                if hypothesis:
                    qids.add(hypothesis["research_question"])
            exp_id = data.get("experiment_id") or manifest.parent.name
            for qid in qids & set(self.questions):
                result[qid].add(exp_id)
        for claim in self.claims.values():
            qid = claim.get("research_question")
            if qid in result:
                result[qid].update(claim.get("experiments") or [])
        return result

    def _evidence_index(self) -> dict[str, dict[str, Any]]:
        out: dict[str, dict[str, Any]] = {}
        for path in sorted((self.root / "research/registry/evidence").glob("EVID-*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            out[path.stem] = data
        return out

    def _paper_index(self) -> list[dict[str, Any]]:
        out = []
        for path in sorted((self.root / "research/publications/papers").glob("*/PAPER.md")):
            text = path.read_text(encoding="utf-8")
            status = re.search(r"\*\*Status:\*\*\s*([^\n]+)", text)
            out.append(
                {
                    "path": path.relative_to(self.root).as_posix(),
                    "title": text.splitlines()[0].lstrip("# "),
                    "questions": sorted(set(RQ_RE.findall(text))),
                    "declared_status": status.group(1).strip() if status else "not_declared",
                    "peer_review": "not_verified_by_projection",
                    "doi": "not_inferred",
                    "independent_replication": "not_inferred",
                }
            )
        return out

    def _review_queue(self) -> list[dict[str, Any]]:
        """Project review state from manifests and append-only review artefacts.

        Presence of a review file is not EVID and is not interpreted as independent
        replication. Historical status disagreements remain visible.
        """
        rows: list[dict[str, Any]] = []
        exp_root = self.root / "research" / "experiments"
        for manifest in sorted(exp_root.glob("*/manifest.json")):
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            exp_id = data.get("experiment_id") or manifest.parent.name
            manifest_state = data.get("human_review_status", "unknown")
            review_paths = sorted(
                path.relative_to(self.root).as_posix()
                for path in manifest.parent.glob("*review*.json")
                if path.is_file()
            )
            rows.append(
                {
                    "experiment_id": exp_id,
                    "manifest_review_status": manifest_state,
                    "review_artifacts": review_paths,
                    "reconciliation_state": (
                        "recorded_review_present_check_status_binding"
                        if review_paths
                        else "review_not_found_in_experiment_root"
                    ),
                    "authority": "review_record_only_not_EVID_or_replication",
                }
            )
        return rows

    def _crosswalk(self) -> list[dict[str, Any]]:
        assignments = self.directions.get("assignments") or {}
        known_parts = [part["id"] for part in self.parts]
        rows = []
        for qid, question in sorted(self.questions.items()):
            coordinate = self.coordinates.get(qid, {})
            parts = {
                part_id for part_id, qids in self.part_questions.items() if qid in qids
            }
            parts.update(coordinate.get("manuscript_parts") or [])
            hypotheses = sorted(
                hid
                for hid, item in self.hypotheses.items()
                if item.get("research_question") == qid
            )
            claims = sorted(
                cid
                for cid, item in self.claims.items()
                if item.get("research_question") == qid
            )
            evidence = sorted(
                eid
                for eid, item in self.evidence.items()
                if item.get("hypothesis_id") in hypotheses or item.get("claim_id") in claims
            )
            explicit_stages = list(coordinate.get("stages") or [])
            stages = [] if coordinate.get("stage_applicability") == "not_applicable" else explicit_stages
            rows.append(
                {
                    "research_question": qid,
                    "source_path": question["source_path"],
                    "domain": question.get("domain"),
                    "direction": assignments.get(qid),
                    "direction_status": (
                        "source_bound" if qid in assignments else "unresolved_no_inference"
                    ),
                    "research_axis": coordinate.get("research_axis", "unclassified"),
                    "stages": sorted(set(stages)),
                    "manuscript_parts": [p for p in known_parts if p in parts],
                    "hypotheses": hypotheses,
                    "hypothesis_statuses": {
                        hid: self.hypotheses[hid].get("status", "untested")
                        for hid in hypotheses
                    },
                    "experiments": sorted(self.experiments.get(qid, set())),
                    "claims": claims,
                    "claim_statuses": {
                        cid: self.claims[cid].get("status", "untested") for cid in claims
                    },
                    "evidence_records": evidence,
                    "literature": list(question.get("literature") or []),
                    "papers": [
                        paper["path"] for paper in self.papers if qid in paper["questions"]
                    ],
                    "rq_status": question.get("status", "open"),
                    "cross_cuts": list(coordinate.get("cross_cuts") or []),
                }
            )
        return rows

    def _validate(self) -> None:
        known_parts = {part["id"] for part in self.parts}
        for qid, coordinate in self.coordinates.items():
            if qid not in self.questions:
                raise ValueError(f"Coordinates reference unknown question: {qid}")
            if coordinate.get("research_axis", "unclassified") not in AXES:
                raise ValueError(f"Unknown research axis: {qid}")
            if set(coordinate.get("manuscript_parts") or []) - known_parts:
                raise ValueError(f"Unknown manuscript part: {qid}")
            for stage in coordinate.get("stages") or []:
                if type(stage) is not int or not 0 <= stage <= 10:
                    raise ValueError(f"Invalid developmental stage: {qid}")
        for row in self.rows:
            missing = set(row["literature"]) - set(self.sources)
            if missing:
                raise ValueError(
                    f"{row['research_question']} references unknown sources: {sorted(missing)}"
                )
        for study in self.studies:
            if study.get("research_question") not in self.questions:
                raise ValueError(f"Study references unknown RQ: {study}")
            if study.get("execution_authorized") is not False:
                raise ValueError("Design registry must not authorize execution.")
            if study.get("scientific_evidence") is not False:
                raise ValueError("Design registry must not manufacture EVID.")

    @staticmethod
    def _table(headers: list[str], body: list[list[Any]]) -> str:
        def cell(value: Any) -> str:
            if isinstance(value, list):
                value = ", ".join(str(x) for x in value)
            if value is None or value == "":
                value = "unresolved"
            return str(value).replace("|", "\\|").replace("\n", " ")
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        lines.extend("| " + " | ".join(cell(v) for v in row) + " |" for row in body)
        return "\n".join(lines)

    def render(self) -> dict[str, str]:
        suffix = (
            "\n\n> Authority boundary: implementation != DATA != reviewed EVID != "
            "independent replication; Human Review != independent replication; DOI != "
            "peer review. This projection executes and promotes nothing.\n"
        )
        directions = self.directions.get("directions") or []
        direction_body = [
            [item["id"], item["title"], item["source_ref"]] for item in directions
        ]
        if direction_body:
            direction_note = (
                "The eleven identities and their order are source-bound and lock protected."
            )
        else:
            direction_note = (
                "The existence/count of eleven directions is locked, but their exact "
                "canonical names/order are not source-bound in the available repository or "
                "retrieved project history. No replacement names are inferred from stages, "
                "manuscript parts, domains or assistant summaries."
            )
        direction_matrix = (
            "# MHRN Research Direction Matrix\n\n"
            f"Registry status: **{self.directions['status']}**. Expected immutable count: **11**.\n\n"
            + direction_note
            + "\n\n"
            + self._table(["ID", "Canonical title", "Source"], direction_body)
        )
        stage_matrix = (
            "# MHRN Developmental Stage Matrix\n\n"
            "Stage 0-10 is a maturity/development axis, not the research-direction taxonomy.\n\n"
            + self._table(
                ["Stage", "Name", "Recorded score", "Claim boundary"],
                [
                    [s["stage"], s["name"], s.get("score"), s.get("claim_boundary", "")]
                    for s in self.stages
                ],
            )
        )
        crosswalk = (
            "# MHRN Research-System Crosswalk\n\n"
            "All registered RQs are projected. Empty direction coordinates remain explicit "
            "until the canonical 11-name source is supplied; this is preferable to taxonomy drift.\n\n"
            + self._table(
                [
                    "RQ",
                    "Direction",
                    "Axis",
                    "Stages",
                    "Manuscript",
                    "Hypotheses",
                    "Experiments",
                    "EVID records",
                    "Papers",
                ],
                [
                    [
                        row["research_question"],
                        row["direction"],
                        row["research_axis"],
                        row["stages"],
                        row["manuscript_parts"],
                        row["hypotheses"],
                        row["experiments"],
                        row["evidence_records"],
                        row["papers"],
                    ]
                    for row in self.rows
                ],
            )
        )
        dissertation = [
            "# MHRN Dissertation / Manuscript Routing Map",
            "",
            "This file follows current Recursive Epistemics Edition 1.8 Parts I-XI. "
            "It is an editorial/argument map, not a research-direction taxonomy and not a degree claim.",
            "",
        ]
        for part in self.parts:
            linked = [r for r in self.rows if part["id"] in r["manuscript_parts"]]
            dissertation += [
                f"## Teil {part['id']} - {part['title']}",
                "",
                f"Source: `{self.system['edition_path']}/{part['file']}`",
                "",
                self._table(
                    ["RQ", "RQ status", "Direction", "Axis", "Experiments", "EVID records"],
                    [
                        [
                            r["research_question"],
                            r["rq_status"],
                            r["direction"],
                            r["research_axis"],
                            r["experiments"],
                            r["evidence_records"],
                        ]
                        for r in linked
                    ],
                ),
                "",
            ]
        unmapped = [r["research_question"] for r in self.rows if not r["manuscript_parts"]]
        dissertation += ["## Unmapped registered RQs", "", ", ".join(unmapped) or "None."]
        review_queue = (
            "# MHRN Review Queue / Reconciliation Matrix\n\n"
            "This projection reconciles manifest review flags with append-only review artefact "
            "presence. A review artefact is not EVID and never counts as independent replication.\n\n"
            + self._table(
                ["Experiment", "Manifest review status", "Review artefacts", "Reconciliation"],
                [
                    [
                        item["experiment_id"],
                        item["manifest_review_status"],
                        item["review_artifacts"],
                        item["reconciliation_state"],
                    ]
                    for item in self.review_queue
                ],
            )
        )
        publication = (
            "# MHRN Publication State Matrix\n\n"
            "Working paper/preprint, DOI, peer review and independent replication are independent states.\n\n"
            + self._table(
                ["Paper", "Declared status", "Peer review", "DOI", "Independent replication"],
                [
                    [
                        p["path"],
                        p["declared_status"],
                        p["peer_review"],
                        p["doi"],
                        p["independent_replication"],
                    ]
                    for p in self.papers
                ],
            )
        )
        meta_readiness = (
            "# MHRN Meta-Research Readiness\n\n"
            "Registered designs are implementation/preparation artefacts only.\n\n"
            + self._table(
                ["Study", "RQ", "Status", "Execution authorized", "Scientific EVID"],
                [
                    [
                        s["study_id"],
                        s["research_question"],
                        s["status"],
                        s["execution_authorized"],
                        s["scientific_evidence"],
                    ]
                    for s in self.studies
                ],
            )
        )
        snapshot = {
            "schema_version": 1,
            "authority": "read_only_projection",
            "direction_status": self.directions["status"],
            "direction_expected_count": 11,
            "direction_bound_count": len(directions),
            "question_count": len(self.questions),
            "questions": self.rows,
            "studies": self.studies,
            "papers": self.papers,
            "review_queue": self.review_queue,
            "scientific_evidence": False,
            "automatic_evidence_promotion": False,
        }
        return {
            "DIRECTION_MATRIX.md": direction_matrix.rstrip() + suffix,
            "STAGE_MATRIX.md": stage_matrix.rstrip() + suffix,
            "CROSSWALK.md": crosswalk.rstrip() + suffix,
            "DISSERTATION_MAP.md": "\n".join(dissertation).rstrip() + suffix,
            "REVIEW_QUEUE.md": review_queue.rstrip() + suffix,
            "PUBLICATION_STATE_MATRIX.md": publication.rstrip() + suffix,
            "META_RESEARCH_READINESS.md": meta_readiness.rstrip() + suffix,
            "META_RESEARCH_CROSSWALK.json": json.dumps(
                snapshot, ensure_ascii=False, indent=2, sort_keys=True
            )
            + "\n",
        }

    def write(self, output_dir: Path | None = None, check: bool = False) -> list[str]:
        output_dir = output_dir or self.root / "research/generated"
        drift: list[str] = []
        for name, content in self.render().items():
            path = output_dir / name
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drift.append(name)
                if not check:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")
        return drift
