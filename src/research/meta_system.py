"""Deterministic crosswalks for MHRN research taxonomies."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
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
            data = _yaml(path) or []
            if not isinstance(data, list):
                raise ValueError(f"{path} must contain a list")
            rows.extend(data)
    return rows

def _index(rows: list[dict[str, Any]], key: str = "id") -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        ident = row[key]
        if ident in out:
            raise ValueError(f"duplicate registry id: {ident}")
        out[ident] = row
    return out

def load_directions() -> list[dict[str, Any]]:
    data = _yaml(REG / "directions.yaml")
    rows = data["directions"]
    expected = [f"DIR-{i:02d}" for i in range(1, 12)]
    if len(rows) != 11 or [r["id"] for r in rows] != expected:
        raise ValueError("research direction registry must preserve exactly DIR-01..DIR-11")
    if len({r["title"] for r in rows}) != 11:
        raise ValueError("research direction titles must be unique")
    return rows

def assign_direction(domain: str, directions: list[dict[str, Any]]) -> str:
    for row in directions:
        if domain in row.get("domains", []):
            return row["id"]
    return "UNMAPPED"

def manuscript_parts(question_ids: set[str]) -> dict[str, list[str]]:
    edition_root = ROOT / "research/publications/2026-09-17_recursive-epistemics_v1.8"
    edition = json.loads((edition_root / "edition.json").read_text(encoding="utf-8"))
    result = {qid: [] for qid in question_ids}
    for part in edition["parts"]:
        text = (edition_root / part["file"]).read_text(encoding="utf-8")
        for qid in set(RQ_RE.findall(text)) & question_ids:
            result[qid].append(part["id"])
    return result

def stage_links(question_ids: set[str]) -> dict[str, list[int]]:
    data = json.loads((ROOT / "src/dashboard/static/scientific-progress.json").read_text(encoding="utf-8"))
    result = {qid: [] for qid in question_ids}
    for stage in data["stages"]:
        blob = json.dumps(stage, ensure_ascii=False)
        for qid in set(RQ_RE.findall(blob)) & question_ids:
            result[qid].append(stage["stage"])
    return result

def build_crosswalk() -> dict[str, Any]:
    questions = _index(_family("questions"))
    hypotheses = _index(_family("hypotheses"))
    sources = _index(_family("sources"), "source_id")
    directions = load_directions()
    parts = manuscript_parts(set(questions))
    stages = stage_links(set(questions))
    rows = []
    for qid, q in sorted(questions.items()):
        hs = sorted(hid for hid, h in hypotheses.items() if h["research_question"] == qid)
        rows.append({
            "research_question": qid,
            "domain": q["domain"],
            "direction": assign_direction(q["domain"], directions),
            "stages": sorted(set(stages[qid])),
            "manuscript_parts": parts[qid],
            "hypotheses": hs,
            "rq_status": q.get("status", "open"),
            "literature": q.get("literature", []),
            "missing_literature_refs": sorted(s for s in q.get("literature", []) if s not in sources),
        })
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
    def cell(v: Any) -> str:
        if isinstance(v, list):
            v = ", ".join(map(str, v))
        return str(v if v not in (None, "") else "-").replace("|", "\\|")
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)

def render() -> dict[str, str]:
    cross = build_crosswalk()
    dirs = cross["directions"]
    qs = cross["questions"]
    notice = "\n\n> Implementation != DATA != EVID; Human Review != independent replication; this projection performs no evidence promotion.\n"
    direction = "# MHRN Direction Matrix\n\nExactly eleven content directions. They are independent of Stage 0-10 and Edition I-XI.\n\n" + _table(["ID", "Direction", "Legacy label"], [[d["id"], d["title"], d["legacy_label"]] for d in dirs]) + notice
    stage_data = json.loads((ROOT / "src/dashboard/static/scientific-progress.json").read_text(encoding="utf-8"))
    stage = "# MHRN Stage Matrix\n\nDevelopment/scientific maturity only; not a research-direction taxonomy.\n\n" + _table(["Stage", "Name", "Score", "Linked RQs"], [[s["stage"], s["name"], s.get("score"), [q["research_question"] for q in qs if s["stage"] in q["stages"]]] for s in stage_data["stages"]]) + notice
    cross_md = "# MHRN Research Crosswalk\n\nUnmapped domains remain visible and do not generate a new direction.\n\n" + _table(["RQ", "Domain", "Direction", "Stage(s)", "Manuscript part(s)", "Hypotheses"], [[q["research_question"], q["domain"], q["direction"], q["stages"], q["manuscript_parts"], q["hypotheses"]] for q in qs]) + notice
    edition_root = ROOT / "research/publications/2026-09-17_recursive-epistemics_v1.8"
    edition = json.loads((edition_root / "edition.json").read_text(encoding="utf-8"))
    diss = ["# MHRN Dissertation / Manuscript Map", "", "Current Edition 1.8 argument structure; not the 11-direction taxonomy."]
    for p in edition["parts"]:
        linked = [q["research_question"] for q in qs if p["id"] in q["manuscript_parts"]]
        diss += ["", f"## Teil {p['id']} - {p['title']}", "", f"Source: `{p['file']}`", "", "Linked RQs: " + (", ".join(linked) if linked else "-")]
    return {
        "DIRECTION_MATRIX.md": direction,
        "STAGE_MATRIX.md": stage,
        "CROSSWALK.md": cross_md,
        "DISSERTATION_MAP.md": "\n".join(diss) + notice,
        "META_RESEARCH_CROSSWALK.json": json.dumps(cross, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    }

def write_all() -> dict[str, Path]:
    GEN.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}
    for name, content in render().items():
        path = GEN / name
        path.write_text(content, encoding="utf-8")
        out[name] = path
    return out
