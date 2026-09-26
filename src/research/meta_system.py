"""Deterministic crosswalks for MHRN research taxonomies."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, cast

import yaml

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "research" / "registry"
GEN = ROOT / "research" / "generated"
RQ_RE = re.compile(r"\bRQ-[A-Z0-9]+-[0-9]+\b")


def _yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _family(stem: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    candidates = {REG / f"{stem}.yaml", *REG.glob(f"{stem}.*.yaml")}
    for path in sorted(candidates):
        if path.is_file():
            raw: Any = _yaml(path)
            if raw is None:
                raw = []
            if not isinstance(raw, list):
                raise ValueError(f"{path} must contain a list")
            rows.extend(cast(list[dict[str, Any]], raw))
    return rows


def _index(rows: list[dict[str, Any]], key: str = "id") -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        ident = str(row[key])
        if ident in out:
            raise ValueError(f"duplicate registry id: {ident}")
        out[ident] = row
    return out


def load_directions() -> list[dict[str, Any]]:
    data = _yaml(REG / "directions.yaml")
    if not isinstance(data, dict):
        raise ValueError("directions.yaml must contain an object")
    rows = cast(list[dict[str, Any]], data["directions"])
    expected = [f"DIR-{i:02d}" for i in range(1, 12)]
    if len(rows) != 11 or [str(r["id"]) for r in rows] != expected:
        raise ValueError(
            "research direction registry must preserve exactly DIR-01..DIR-11"
        )
    if len({str(r["title"]) for r in rows}) != 11:
        raise ValueError("research direction titles must be unique")
    return rows


def assign_direction(domain: str, directions: list[dict[str, Any]]) -> str:
    for row in directions:
        if domain in row.get("domains", []):
            return str(row["id"])
    return "UNMAPPED"


def manuscript_parts(question_ids: set[str]) -> dict[str, list[str]]:
    edition_root = ROOT / "research/publications/2026-09-17_recursive-epistemics_v1.8"
    edition = json.loads((edition_root / "edition.json").read_text(encoding="utf-8"))
    result: dict[str, list[str]] = {qid: [] for qid in question_ids}
    for part in edition["parts"]:
        text = (edition_root / part["file"]).read_text(encoding="utf-8")
        for qid in set(RQ_RE.findall(text)) & question_ids:
            result[qid].append(str(part["id"]))
    return result


def stage_links(question_ids: set[str]) -> dict[str, list[int]]:
    progress_path = ROOT / "src/dashboard/static/scientific-progress.json"
    data = json.loads(progress_path.read_text(encoding="utf-8"))
    result: dict[str, list[int]] = {qid: [] for qid in question_ids}
    for stage in data["stages"]:
        blob = json.dumps(stage, ensure_ascii=False)
        for qid in set(RQ_RE.findall(blob)) & question_ids:
            result[qid].append(int(stage["stage"]))
    return result


def build_crosswalk() -> dict[str, Any]:
    questions = _index(_family("questions"))
    hypotheses = _index(_family("hypotheses"))
    sources = _index(_family("sources"), "source_id")
    directions = load_directions()
    parts = manuscript_parts(set(questions))
    stages = stage_links(set(questions))
    rows: list[dict[str, Any]] = []

    for qid, question in sorted(questions.items()):
        hypotheses_for_question = sorted(
            hid
            for hid, hypothesis in hypotheses.items()
            if hypothesis["research_question"] == qid
        )
        literature = cast(list[str], question.get("literature", []))
        rows.append(
            {
                "research_question": qid,
                "domain": question["domain"],
                "direction": assign_direction(str(question["domain"]), directions),
                "stages": sorted(set(stages[qid])),
                "manuscript_parts": parts[qid],
                "hypotheses": hypotheses_for_question,
                "rq_status": question.get("status", "open"),
                "literature": literature,
                "missing_literature_refs": sorted(
                    source_id for source_id in literature if source_id not in sources
                ),
            }
        )

    return {
        "schema_version": 1,
        "authority": "descriptive_crosswalk_not_evidence",
        "directions": directions,
        "questions": rows,
        "invariants": [
            "direction != stage",
            "direction != manuscript_part",
            "implementation != DATA",
            "DATA != EVID",
            "human_review != independent_replication",
            "doi != peer_review",
            "ai_analysis != scientific_evidence",
        ],
    }


def _table(headers: list[str], rows: list[list[Any]]) -> str:
    def cell(value: Any) -> str:
        if isinstance(value, list):
            value = ", ".join(map(str, cast(list[object], value)))
        return str(value if value not in (None, "") else "-").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines += ["| " + " | ".join(cell(value) for value in row) + " |" for row in rows]
    return "\n".join(lines)


def render() -> dict[str, str]:
    cross = build_crosswalk()
    directions = cast(list[dict[str, Any]], cross["directions"])
    questions = cast(list[dict[str, Any]], cross["questions"])
    notice = (
        "\n\n> Implementation != DATA != EVID; Human Review != independent "
        "replication; this projection performs no evidence promotion.\n"
    )

    direction = (
        "# MHRN Direction Matrix\n\n"
        "Exactly eleven content directions. They are independent of Stage "
        "0-10 and Edition I-XI.\n\n"
        + _table(
            ["ID", "Direction", "Legacy label"],
            [[row["id"], row["title"], row["legacy_label"]] for row in directions],
        )
        + notice
    )

    progress_path = ROOT / "src/dashboard/static/scientific-progress.json"
    stage_data = json.loads(progress_path.read_text(encoding="utf-8"))
    stage = (
        "# MHRN Stage Matrix\n\n"
        "Development/scientific maturity only; not a research-direction "
        "taxonomy.\n\n"
        + _table(
            ["Stage", "Name", "Score", "Linked RQs"],
            [
                [
                    row["stage"],
                    row["name"],
                    row.get("score"),
                    [
                        question["research_question"]
                        for question in questions
                        if row["stage"] in question["stages"]
                    ],
                ]
                for row in stage_data["stages"]
            ],
        )
        + notice
    )

    cross_md = (
        "# MHRN Research Crosswalk\n\n"
        "Unmapped domains remain visible and do not generate a new "
        "direction.\n\n"
        + _table(
            [
                "RQ",
                "Domain",
                "Direction",
                "Stage(s)",
                "Manuscript part(s)",
                "Hypotheses",
            ],
            [
                [
                    row["research_question"],
                    row["domain"],
                    row["direction"],
                    row["stages"],
                    row["manuscript_parts"],
                    row["hypotheses"],
                ]
                for row in questions
            ],
        )
        + notice
    )

    edition_root = ROOT / "research/publications/2026-09-17_recursive-epistemics_v1.8"
    edition = json.loads((edition_root / "edition.json").read_text(encoding="utf-8"))
    dissertation = [
        "# MHRN Dissertation / Manuscript Map",
        "",
        "Current Edition 1.8 argument structure; not the 11-direction taxonomy.",
    ]
    for part in edition["parts"]:
        linked = [
            question["research_question"]
            for question in questions
            if part["id"] in question["manuscript_parts"]
        ]
        dissertation += [
            "",
            f"## Teil {part['id']} - {part['title']}",
            "",
            f"Source: `{part['file']}`",
            "",
            "Linked RQs: " + (", ".join(linked) if linked else "-"),
        ]

    return {
        "DIRECTION_MATRIX.md": direction,
        "STAGE_MATRIX.md": stage,
        "CROSSWALK.md": cross_md,
        "DISSERTATION_MAP.md": "\n".join(dissertation) + notice,
        "META_RESEARCH_CROSSWALK.json": json.dumps(
            cross, ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n",
    }


def write_all() -> dict[str, Path]:
    GEN.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}
    for name, content in render().items():
        path = GEN / name
        path.write_text(content, encoding="utf-8")
        out[name] = path
    return out
