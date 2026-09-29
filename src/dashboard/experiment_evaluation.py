"""Controlled post-hoc scientific interpretation artifacts for experiments."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ExperimentEvaluationError(ValueError):
    """Raised when a post-hoc evaluation cannot be safely recorded."""


_EXPERIMENT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_ANSWERS = frozenset({"supported", "refuted", "mixed", "inconclusive", "not_assessed"})
_TEXT_LIMITS = {
    "evaluator": 200,
    "evaluation": 30_000,
    "observations": 20_000,
    "limitations": 20_000,
    "follow_up": 20_000,
}


def _text(payload: dict[str, object], key: str, *, required: bool = False) -> str:
    value = payload.get(key, "")
    if not isinstance(value, str):
        raise ExperimentEvaluationError(f"{key} must be text")
    result = value.strip()
    if required and not result:
        raise ExperimentEvaluationError(f"{key} is required")
    limit = _TEXT_LIMITS.get(key)
    if limit is not None and len(result) > limit:
        raise ExperimentEvaluationError(f"{key} exceeds {limit} characters")
    return result


def _experiment_dir(research_root: Path, experiment_id: str) -> Path:
    if not _EXPERIMENT_ID.fullmatch(experiment_id):
        raise ExperimentEvaluationError("invalid experiment_id")
    directory = research_root / "experiments" / experiment_id
    manifest = directory / "manifest.json"
    if not manifest.is_file():
        raise ExperimentEvaluationError(f"experiment not found: {experiment_id}")
    return directory


def read_experiment_evaluation(
    research_root: Path, experiment_id: str
) -> dict[str, object]:
    """Return the saved evaluation without exposing arbitrary filesystem paths."""

    directory = _experiment_dir(research_root, experiment_id)
    path = directory / "posthoc" / "evaluation.json"
    if not path.is_file():
        return {"exists": False, "experiment_id": experiment_id}
    try:
        value: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ExperimentEvaluationError("saved evaluation is unreadable") from exc
    if not isinstance(value, dict):
        raise ExperimentEvaluationError("saved evaluation must be an object")
    return {"exists": True, **value}


def write_experiment_evaluation(
    research_root: Path, payload: dict[str, object]
) -> dict[str, object]:
    """Write a versioned interpretation artifact linked from the manifest."""

    experiment_id = _text(payload, "experiment_id", required=True)
    directory = _experiment_dir(research_root, experiment_id)
    answer = _text(payload, "hypothesis_answer", required=True)
    if answer not in _ANSWERS:
        raise ExperimentEvaluationError("invalid hypothesis_answer")

    evaluation = {
        "schema": "MHRN_POSTHOC_EVALUATION_V1",
        "experiment_id": experiment_id,
        "research_question": _text(payload, "research_question"),
        "hypothesis": _text(payload, "hypothesis"),
        "hypothesis_answer": answer,
        "evaluator": _text(payload, "evaluator", required=True),
        "evaluation": _text(payload, "evaluation", required=True),
        "observations": _text(payload, "observations"),
        "limitations": _text(payload, "limitations"),
        "follow_up": _text(payload, "follow_up"),
        "created_at": _text(payload, "created_at")
        or datetime.now(timezone.utc).isoformat(),
        "scientific_evidence": False,
        "epistemic_layer": "post_hoc_interpretation",
        "human_review_status": "not_reviewed",
        "automatic_evidence_promotion": False,
    }

    artifact_dir = directory / "posthoc"
    artifact_dir.mkdir(exist_ok=True)
    json_path = artifact_dir / "evaluation.json"
    markdown_path = artifact_dir / "evaluation.md"
    json_path.write_text(
        json.dumps(evaluation, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )
    markdown_path.write_text(_markdown(evaluation), encoding="utf-8")

    manifest_path = directory / "manifest.json"
    manifest_value: Any = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest_value, dict):
        raise ExperimentEvaluationError("experiment manifest must be an object")
    artifacts = manifest_value.get("artifacts")
    if not isinstance(artifacts, dict):
        artifacts = {}
    artifacts["posthoc_evaluation"] = "posthoc/evaluation.md"
    artifacts["posthoc_evaluation_data"] = "posthoc/evaluation.json"
    manifest_value["artifacts"] = artifacts
    manifest_value["posthoc_evaluation"] = {
        "status": "recorded_interpretation_not_evidence",
        "hypothesis_answer": answer,
        "updated_at": evaluation["created_at"],
    }
    manifest_path.write_text(
        json.dumps(manifest_value, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    return {
        "ok": True,
        "experiment_id": experiment_id,
        "markdown_path": f"experiments/{experiment_id}/posthoc/evaluation.md",
        "json_path": f"experiments/{experiment_id}/posthoc/evaluation.json",
        "scientific_evidence": False,
        "epistemic_layer": "post_hoc_interpretation",
    }


def _markdown(evaluation: dict[str, object]) -> str:
    def value(key: str, fallback: str = "Nicht angegeben") -> str:
        return str(evaluation.get(key) or fallback)

    return (
        "# Post-hoc wissenschaftliche Auswertung\n\n"
        f"- Experiment: `{value('experiment_id')}`\n"
        f"- Forschungsfrage: {value('research_question')}\n"
        f"- Hypothese: {value('hypothesis')}\n"
        f"- Hypothesenantwort: **{value('hypothesis_answer')}**\n"
        f"- Auswertende Person: {value('evaluator')}\n"
        f"- Zeitpunkt: {value('created_at')}\n\n"
        "## Wissenschaftliche Auswertung\n\n"
        f"{value('evaluation')}\n\n"
        "## Beobachtungen und Auswertungskriterien\n\n"
        f"{value('observations')}\n\n"
        "## Limitationen und Alternativerklärungen\n\n"
        f"{value('limitations')}\n\n"
        "## Nächste Schritte\n\n"
        f"{value('follow_up')}\n\n"
        "## Evidenzgrenze\n\n"
        "Dieses Dokument ist eine nachgelagerte Interpretation. Es ist keine "
        "automatische EVID-Einstufung, verändert keine Hypothesenregistrierung "
        "und benötigt einen separaten Human-Review-/EVID-Workflow, bevor es als "
        "wissenschaftlich geprüfte Aussage in die Arbeit eingehen kann.\n"
    )