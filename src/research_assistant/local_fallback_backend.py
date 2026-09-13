"""Deterministic zero-network fallback backend for MHRN research chat.

The fallback is deliberately small and read-only. It does not execute tools,
access the network, mutate the SNN, or create scientific evidence. Its purpose
is to keep basic operator/help chat available when a configured model provider
is unavailable.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import time
from typing import Any, cast

from src.language_organ.protocols import LanguageRequest, LanguageResponse

from .contracts import AIInferenceFailureEvent

_EMBEDDED_KNOWLEDGE: dict[str, str] = {
    "what is mhrn": (
        "MHRN is the project runtime for experiments with recurrent spiking "
        "neural networks, explicit plasticity, homeostasis and reproducible "
        "research workflows."
    ),
    "what is brain-5d": (
        "Brain-5D is the former project name. The current project name is MHRN. "
        "Dimensionality is an experimental treatment, not a biological claim."
    ),
    "firing rate": (
        "Firing-rate telemetry is available from the live runtime and dashboard. "
        "Use the current run data rather than a historical experiment when asking "
        "about the network that is running now."
    ),
    "homeostasis": (
        "Homeostasis is a configurable regulation mechanism that can adjust "
        "neural state toward declared targets. Its effect must be evaluated by "
        "matched experiments and must not be inferred from configuration alone."
    ),
    "stdp": (
        "STDP changes eligible synaptic weights as a function of relative spike "
        "timing. The configured rule and parameters belong to the run provenance."
    ),
    "synapse": (
        "Synapses are explicit directed network connections with runtime state "
        "such as weight and delay. The live dashboard reads the canonical network."
    ),
    "neuron": (
        "MHRN neurons expose model identity and live state such as membrane "
        "potential, recovery state, energy, spike count, traces and regulation."
    ),
    "experiment": (
        "Experiments are governed through the research registry and evidence "
        "workflow. Engineering success does not automatically promote a result "
        "to scientific evidence."
    ),
    "self-organization": (
        "Self-organization covers declared structural mechanisms such as pruning "
        "and sprouting. Their effects require controlled experiments."
    ),
    "dashboard": (
        "The MHRN dashboard provides read-only observability and explicit operator "
        "controls for runtime, science, files, review, release and settings."
    ),
    "energy": (
        "Energy is an explicit simulation state variable. Its semantics and causal "
        "effect depend on the active model/configuration and must be read from run "
        "provenance."
    ),
    "reward": (
        "Reward/modulatory signals are experimental inputs. They do not grant an "
        "AI assistant authority to change the canonical SNN outside declared APIs."
    ),
    "structural plasticity": (
        "Structural plasticity changes network topology under declared rules. "
        "Topology changes must remain observable, reproducible and attributable."
    ),
    "storage": (
        "Runtime persistence uses project storage/checkpoint mechanisms. The "
        "dashboard reports storage state but does not turn persisted data into "
        "accepted evidence automatically."
    ),
    "tick": (
        "A tick is the canonical discrete simulation step. A changing live tick "
        "is the clearest basic indicator that the runtime is advancing even when "
        "the current spike count is zero."
    ),
    "help": (
        "I am the deterministic MHRN local fallback assistant. I can provide basic "
        "project help when the configured model provider is unavailable."
    ),
}

_STOP_WORDS: set[str] = {
    "der",
    "die",
    "das",
    "den",
    "dem",
    "des",
    "ein",
    "eine",
    "einen",
    "einem",
    "eines",
    "und",
    "oder",
    "aber",
    "mit",
    "von",
    "für",
    "auf",
    "an",
    "in",
    "zu",
    "aus",
    "bei",
    "nach",
    "um",
    "vor",
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "shall",
    "can",
    "not",
    "no",
    "nor",
    "but",
    "or",
    "if",
    "so",
    "as",
    "at",
    "by",
    "for",
    "from",
    "into",
    "of",
    "on",
    "to",
    "with",
    "it",
    "its",
    "this",
    "that",
    "these",
    "those",
    "we",
    "you",
    "they",
    "he",
    "she",
    "them",
    "their",
    "your",
    "our",
    "my",
    "bitte",
    "danke",
    "gern",
    "gerne",
    "hallo",
    "hi",
    "hey",
}


class LocalFallbackBackend:
    """Small deterministic assistant compatible with the language/chat protocols."""

    def __init__(
        self,
        model: str = "local-fallback",
        temperature: float = 0.0,
        max_tokens: int = 1024,
        seed: int | None = None,
        knowledge_base: dict[str, str] | None = None,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._rng = random.Random(seed) if seed is not None else random.Random()
        self._knowledge = dict(_EMBEDDED_KNOWLEDGE)
        if knowledge_base:
            self._knowledge.update(knowledge_base)
        self._last_failure_event: AIInferenceFailureEvent | None = None

    @property
    def name(self) -> str:
        return "local-fallback"

    @property
    def last_failure_event(self) -> AIInferenceFailureEvent | None:
        return self._last_failure_event

    def infer(self, request: LanguageRequest) -> LanguageResponse:
        """Implement the canonical language-model backend contract."""
        started = time.time()
        try:
            text, _metadata = self.generate_text(request.text)
            return LanguageResponse(
                request_id=request.request_id,
                text=text,
                backend_name=self.name,
                success=True,
            )
        except (OSError, ValueError) as exc:
            latency_ms = (time.time() - started) * 1000
            self._last_failure_event = AIInferenceFailureEvent.create(
                request_id=request.request_id,
                backend=self.name,
                request_digest=hashlib.sha256(request.text.encode("utf-8")).hexdigest(),
                latency_ms=latency_ms,
                retry_status="not_retried",
                error=str(exc),
            )
            return LanguageResponse(
                request_id=request.request_id,
                text="",
                backend_name=self.name,
                success=False,
                error=str(exc),
            )

    def generate_text(
        self,
        prompt: str,
        images: list[str] | None = None,
        tools: list[dict[str, object]] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Generate a deterministic local response and provider-style metadata."""
        del images, tools
        started_ns = time.perf_counter_ns()
        response, match_info = self._match_response(prompt)
        elapsed_ns = time.perf_counter_ns() - started_ns
        metadata: dict[str, Any] = {
            "model": self.model,
            "provider": self.name,
            "response_digest": hashlib.sha256(response.encode("utf-8")).hexdigest(),
            "total_duration_ns": elapsed_ns,
            "eval_duration_ms": elapsed_ns / 1_000_000,
            "match_method": match_info.get("method", "template"),
            "match_confidence": match_info.get("confidence", 0.0),
            "match_keywords": match_info.get("keywords", []),
            "structured_output_valid": True,
            "vision_enabled": False,
            "tools_enabled": False,
            "network_access": False,
            "authority": "read_only_non_evidentiary",
        }
        return response, metadata

    def __call__(self, prompt: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """Return an AIRR-compatible schema-shaped analysis result."""
        text, metadata = self.generate_text(prompt)
        return {"response": text, "assessment": text}, metadata

    def _match_response(self, prompt: str) -> tuple[str, dict[str, Any]]:
        clean = re.sub(r"[^\w\s]", " ", prompt.lower())
        words = [word for word in clean.split() if len(word) > 2]
        keywords = list(
            dict.fromkeys(word for word in words if word not in _STOP_WORDS)
        )
        if not keywords:
            return self._greeting_response(), {
                "method": "greeting",
                "confidence": 1.0,
                "keywords": [],
            }

        normalized_prompt = " ".join(words)
        direct_matches = [key for key in self._knowledge if key in normalized_prompt]
        if direct_matches:
            direct_best_key = max(direct_matches, key=len)
            return self._knowledge[direct_best_key], {
                "method": "knowledge_match",
                "confidence": 1.0,
                "keywords": keywords[:8],
                "matched_key": direct_best_key,
            }

        fuzzy_best_key: str | None = None
        best_score = 0.0
        for key in self._knowledge:
            key_words = set(key.split())
            overlap = sum(1 for word in keywords if word in key_words)
            denominator = len(key_words) + len(keywords) - overlap
            score = overlap / denominator if denominator else 0.0
            if score > best_score:
                fuzzy_best_key = key
                best_score = score

        if fuzzy_best_key is not None and best_score >= 0.25:
            return self._knowledge[fuzzy_best_key], {
                "method": "knowledge_match",
                "confidence": round(best_score, 3),
                "keywords": keywords[:8],
                "matched_key": fuzzy_best_key,
            }

        return self._template_response(keywords), {
            "method": "template",
            "confidence": round(best_score, 3),
            "keywords": keywords[:8],
        }

    def _greeting_response(self) -> str:
        greetings = (
            "Hallo! Ich bin der lokale MHRN-Fallback. Fragen Sie mich z. B. "
            "nach Neuronen, Synapsen, STDP, Homöostase oder Experimenten.",
            "MHRN Local Fallback ist aktiv. Für Live-Zustände verwenden Sie die "
            "Runtime-Ansichten; für tiefe Analysen den konfigurierten Modellanbieter.",
        )
        return self._rng.choice(greetings)

    def _template_response(self, keywords: list[str]) -> str:
        visible = ", ".join(keywords[:6]) if keywords else "keine"
        return (
            "Der lokale Fallback hat dafür keine ausreichend spezifische, "
            "repository-gestützte Antwort. Erkannte Begriffe: "
            f"{visible}. Nutzen Sie für detaillierte Analyse den konfigurierten "
            "Research-Chat. Der Fallback erfindet keine Laufzeit- oder "
            "Experimentergebnisse."
        )

    def _repair_json(self, text: str) -> dict[str, Any]:
        """Return a dictionary for valid JSON objects, otherwise a safe fallback."""
        try:
            parsed: object = json.loads(text)
        except json.JSONDecodeError:
            return {"response": text, "assessment": text}
        if isinstance(parsed, dict):
            mapping = cast(dict[object, Any], parsed)
            return {str(key): value for key, value in mapping.items()}
        return {"response": text, "assessment": text}


def create_local_fallback_backend(
    model: str = "local-fallback",
    **kwargs: Any,
) -> LocalFallbackBackend:
    """Create the always-available deterministic fallback backend."""
    return LocalFallbackBackend(model=model, **kwargs)
