#!/usr/bin/env python3
"""Create a non-identifying descriptive aggregate from a private review export.

The input export must remain outside the repository. The output contains only
summary statistics and instrument metadata; raw answers, notes, participant
codes, signatures and withdrawal secrets are never copied.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from review_portal.analysis import summarize

_FORBIDDEN_KEYS = {
    "answers",
    "notes",
    "participant_code",
    "withdrawal_token",
    "invitation_code",
    "signature",
    "email",
    "name",
}


def _load_records(path: Path) -> list[dict[str, Any]]:
    payload: object = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("records", [])
    if not isinstance(payload, list) or not all(isinstance(row, dict) for row in payload):
        raise ValueError("Input must be a JSON list or an admin export with records.")
    return [dict(row) for row in payload]


def _assert_safe(value: object) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in _FORBIDDEN_KEYS:
                raise ValueError(f"Unsafe field in aggregate: {key}")
            _assert_safe(child)
    elif isinstance(value, list):
        for child in value:
            _assert_safe(child)


def build_aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    aggregate = {
        "schema_version": 1,
        "classification": "PRIVATE_HUMAN_REVIEW_DESCRIPTIVES_NOT_EVIDENCE",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_record_count": len(records),
        "automatic_evidence_promotion": False,
        "raw_answers_included": False,
        "summary": summarize(records),
    }
    _assert_safe(aggregate)
    return aggregate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Private admin export JSON outside the repository")
    parser.add_argument("output", type=Path, help="Sanitized aggregate JSON")
    args = parser.parse_args()
    records = _load_records(args.input)
    aggregate = build_aggregate(records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(aggregate, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote sanitized aggregate for {len(records)} records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
