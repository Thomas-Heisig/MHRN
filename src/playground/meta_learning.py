"""Meta-learning tasks, local knowledge index and strategy rewards.

Everything in this module is Playground-only. Stored knowledge is external to
PAN; PAN learns routing/organization strategies rather than factual payloads.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ0-9_\-]+", re.UNICODE)


def text_vector(text: str, dimensions: int = 64) -> list[float]:
    """Return a deterministic dependency-free hashing embedding."""

    if dimensions < 8:
        raise ValueError("dimensions must be at least 8")
    vector = [0.0 for _ in range(dimensions)]
    tokens = _TOKEN_RE.findall(text.lower())
    for token in tokens:
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=16).digest()
        index = int.from_bytes(digest[:4], "little") % dimensions
        sign = 1.0 if digest[4] & 1 else -1.0
        weight = 1.0 + (digest[5] / 255.0)
        vector[index] += sign * weight
    norm = math.sqrt(sum(value * value for value in vector))
    if norm > 0:
        vector = [value / norm for value in vector]
    return vector


def cosine(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vector size mismatch")
    return sum(a * b for a, b in zip(left, right))


@dataclass(slots=True)
class KnowledgeRecord:
    record_id: str
    text: str
    category: str
    source: str
    vector: list[float]
    location: str | None = None

    def public(self) -> dict[str, object]:
        return {
            "record_id": self.record_id,
            "text": self.text,
            "category": self.category,
            "source": self.source,
            "location": self.location,
        }


class KnowledgeBase:
    """Small local vector store plus bounded read-only file index."""

    def __init__(self, *, dimensions: int = 64) -> None:
        self.dimensions = dimensions
        self.records: dict[str, KnowledgeRecord] = {}
        self.relations: list[dict[str, str]] = []

    def _id(self, source: str, text: str, location: str | None = None) -> str:
        raw = f"{source}\0{location or ''}\0{text}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:20]

    def store_info(
        self,
        text: str,
        category: str,
        *,
        source: str = "vector_db",
        location: str | None = None,
    ) -> dict[str, object]:
        clean = " ".join(text.split()).strip()
        if not clean:
            raise ValueError("text must not be empty")
        record_id = self._id(source, clean, location)
        duplicate = record_id in self.records
        if not duplicate:
            self.records[record_id] = KnowledgeRecord(
                record_id=record_id,
                text=clean,
                category=category,
                source=source,
                vector=text_vector(clean, self.dimensions),
                location=location,
            )
        return {
            "stored": not duplicate,
            "duplicate": duplicate,
            "record_id": record_id,
        }

    def index_files(
        self,
        roots: Iterable[Path],
        *,
        category: str = "Konzepte",
        max_files: int = 200,
        max_chars_per_file: int = 16_000,
    ) -> dict[str, int]:
        allowed = {".md", ".txt", ".rst", ".py", ".json", ".yaml", ".yml"}
        indexed = 0
        skipped = 0
        for root in roots:
            root = root.resolve()
            if not root.exists():
                continue
            candidates = [root] if root.is_file() else sorted(root.rglob("*"))
            for path in candidates:
                if indexed >= max_files:
                    break
                if not path.is_file() or path.suffix.lower() not in allowed:
                    continue
                try:
                    content = path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    skipped += 1
                    continue
                content = content[:max_chars_per_file]
                if not content.strip():
                    skipped += 1
                    continue
                # Index bounded paragraph chunks, not the whole repository file.
                paragraphs = [
                    " ".join(item.split())
                    for item in re.split(r"\n\s*\n", content)
                    if item.strip()
                ][:8]
                for index, paragraph in enumerate(paragraphs):
                    self.store_info(
                        paragraph[:2000],
                        category,
                        source="file_index",
                        location=f"{path.as_posix()}#chunk-{index}",
                    )
                indexed += 1
            if indexed >= max_files:
                break
        return {"indexed_files": indexed, "skipped_files": skipped}

    def find(
        self,
        query: str,
        *,
        source: str,
        category: str | None = None,
        limit: int = 5,
    ) -> dict[str, object]:
        query_vector = text_vector(query, self.dimensions)
        candidates = [
            record
            for record in self.records.values()
            if record.source == source
            and (category is None or record.category == category)
        ]
        ranked = sorted(
            (
                (cosine(query_vector, record.vector), record)
                for record in candidates
            ),
            key=lambda item: item[0],
            reverse=True,
        )[: max(1, limit)]
        matches = [
            {"score": score, **record.public()} for score, record in ranked
        ]
        return {
            "found": bool(matches),
            "source": source,
            "category": category,
            "matches": matches,
        }

    def link(self, left_id: str, right_id: str, relation: str) -> dict[str, object]:
        both_exist = left_id in self.records and right_id in self.records
        linked = False
        if both_exist:
            item = {"left": left_id, "right": right_id, "relation": relation}
            if item not in self.relations:
                self.relations.append(item)
            linked = True
        return {"linked": linked, "both_exist": both_exist}

    def records_for_source(self, source: str) -> list[KnowledgeRecord]:
        return [record for record in self.records.values() if record.source == source]

    def snapshot(self) -> dict[str, object]:
        return {
            "classification": "PLAYGROUND_KNOWLEDGE_BASE",
            "scientific_evidence": False,
            "dimensions": self.dimensions,
            "records": [record.public() for record in self.records.values()],
            "relations": list(self.relations),
        }

    @classmethod
    def from_snapshot(cls, payload: dict[str, object]) -> "KnowledgeBase":
        dimensions = int(payload.get("dimensions", 64))
        kb = cls(dimensions=dimensions)
        raw_records = payload.get("records", [])
        if isinstance(raw_records, list):
            for item in raw_records:
                if not isinstance(item, dict):
                    continue
                text = item.get("text")
                category = item.get("category")
                source = item.get("source")
                if not isinstance(text, str) or not isinstance(category, str) or not isinstance(source, str):
                    continue
                location = item.get("location")
                kb.store_info(
                    text,
                    category,
                    source=source,
                    location=location if isinstance(location, str) else None,
                )
        raw_relations = payload.get("relations", [])
        if isinstance(raw_relations, list):
            kb.relations = [
                {
                    "left": str(item["left"]),
                    "right": str(item["right"]),
                    "relation": str(item["relation"]),
                }
                for item in raw_relations
                if isinstance(item, dict)
                and {"left", "right", "relation"} <= set(item)
            ]
        return kb

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.snapshot(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


class MetaTaskGenerator:
    """Generate find/store/link strategy tasks with known supervision."""

    categories = ("Personen", "Orte", "Ereignisse", "Konzepte")
    relations = ("ist_verwandt_mit", "arbeitet_mit", "lebte_in", "gehört_zu")
    category_cues = {
        "Personen": ("profile", "contact", "biography", "name"),
        "Orte": ("address", "location", "city", "map"),
        "Ereignisse": ("date", "meeting", "launch", "incident"),
        "Konzepte": ("definition", "principle", "method", "model"),
    }

    def __init__(self, seed: int = 0) -> None:
        self.rng = random.Random(seed ^ 0x4D455441)
        self.counter = 0

    def _semantic_category(self, text: str, fallback: str) -> str:
        lowered = text.lower()
        for category, cues in self.category_cues.items():
            if any(cue in lowered for cue in cues):
                return category
        return fallback

    def _relation_for(self, left: KnowledgeRecord, right: KnowledgeRecord) -> str:
        left_category = self._semantic_category(left.text, left.category)
        right_category = self._semantic_category(right.text, right.category)
        if left_category == right_category:
            return "ist_verwandt_mit"
        if "Personen" in {left_category, right_category} and "Orte" in {
            left_category,
            right_category,
        }:
            return "lebte_in"
        if "Personen" in {left_category, right_category} and "Konzepte" in {
            left_category,
            right_category,
        }:
            return "arbeitet_mit"
        return "gehört_zu"

    def generate(
        self,
        kb: KnowledgeBase,
        *,
        gateway_available: bool = False,
    ) -> dict[str, object]:
        self.counter += 1
        task_type = ("find_source", "store_info", "link_info")[
            self.counter % 3
        ]
        if task_type == "find_source":
            sources = ["vector_db", "file_index"]
            available = [
                source for source in sources if kb.records_for_source(source)
            ]
            if gateway_available:
                sources.append("gateway")
                available.append("gateway")
            if not available:
                task_type = "store_info"
            else:
                true_source = self.rng.choice(available)
                if true_source == "gateway":
                    query = f"fresh-external-query-{self.counter}"
                    category = self.rng.choice(self.categories)
                    target_id = None
                else:
                    record = self.rng.choice(kb.records_for_source(true_source))
                    query = record.text[:240]
                    category = self._semantic_category(record.text, record.category)
                    target_id = record.record_id
                return {
                    "type": "find_source",
                    "question": query,
                    "true_source": true_source,
                    "true_category": category,
                    "target_record_id": target_id,
                    "possible_sources": sources,
                    "possible_categories": list(self.categories),
                }

        if task_type == "store_info":
            category = self.rng.choice(self.categories)
            cue = self.rng.choice(self.category_cues[category])
            token = hashlib.sha256(
                f"{self.counter}:{self.rng.random()}".encode("utf-8")
            ).hexdigest()[:10]
            return {
                "type": "store_info",
                "info": f"{cue} night-note-{token}",
                "true_category": category,
                "possible_categories": list(self.categories),
            }

        records = list(kb.records.values())
        if len(records) < 2:
            return self.generate(kb, gateway_available=gateway_available)
        left, right = self.rng.sample(records, 2)
        relation = self._relation_for(left, right)
        return {
            "type": "link_info",
            "left_id": left.record_id,
            "right_id": right.record_id,
            "left_hint": left.text[:160],
            "right_hint": right.text[:160],
            "true_relation": relation,
            "possible_relations": list(self.relations),
        }


class MetaReward:
    """Reward routing/organization strategy rather than factual content."""

    def compute(
        self,
        task: dict[str, object],
        action: dict[str, object],
        result: dict[str, object],
    ) -> dict[str, float]:
        task_type = str(task["type"])
        components: dict[str, float] = {}
        if task_type == "find_source":
            components["source"] = (
                1.0 if action.get("source") == task.get("true_source") else -0.5
            )
            components["category"] = (
                1.0 if action.get("category") == task.get("true_category") else -0.5
            )
            components["retrieval"] = 0.25 if result.get("found") else -0.1
        elif task_type == "store_info":
            components["category"] = (
                1.0 if action.get("category") == task.get("true_category") else -0.5
            )
            components["storage"] = 0.2 if result.get("stored") else 0.0
        elif task_type == "link_info":
            components["relation"] = (
                1.0 if action.get("relation") == task.get("true_relation") else -0.5
            )
            components["link"] = 0.3 if result.get("linked") else -0.1
        else:
            raise ValueError(f"unknown meta task type: {task_type}")
        components["total"] = sum(components.values())
        return components
