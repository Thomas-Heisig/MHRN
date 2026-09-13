"""Local fallback AI backend — embedded, zero-dependency, no network required.

Provides a lightweight rule-based response engine for basic chat tasks when
Ollama or other external providers are unavailable. Uses keyword matching,
pattern templates, and a small embedded knowledge base.

This module is self-contained and intentionally does NOT import any external
AI/ML libraries. All responses are generated locally via deterministic rules.

Usage:
    backend = LocalFallbackBackend()
    text, metadata = backend.generate_text("What is the firing rate?")
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import re
import time
from datetime import datetime, timezone
from typing import Any

from src.language_organ.protocols import LanguageRequest, LanguageResponse

from .contracts import AIInferenceFailureEvent


# ── Embedded knowledge base ────────────────────────────────────────────────
# These are simple Q/A pairs for common MHRN/Brain-5D questions.
# Extended dynamically by the response engine.

_EMBEDDED_KNOWLEDGE: dict[str, str] = {
    "what is mhrn": (
        "MHRN (Multi-Scale Homeostatic Recurrence Network) is a "
        "biologically-inspired spiking neural network simulation. It models "
        "neurons with Izhikevich dynamics, STDP-based plasticity, "
        "homeostatic regulation, and structural self-organization."
    ),
    "what is brain-5d": (
        "Brain-5D is the codename for the MHRN project — a 5-dimensional "
        "spiking neural network simulation platform for cognitive architecture research."
    ),
    "firing rate": (
        "The mean firing rate is reported in the dashboard Vitals panel. "
        "Homeostasis targets a rate of 5.0 Hz by default. Current rate "
        "depends on network activity and input stimulation."
    ),
    "homeostasis": (
        "Homeostasis regulates neuron firing rates toward a target (default 5.0 Hz) "
        "by adjusting thresholds. It also manages energy levels. "
        "Configuration is in the `homeostasis` section of the YAML config."
    ),
    "stdp": (
        "STDP (Spike-Timing-Dependent Plasticity) strengthens or weakens "
        "synapses based on the relative timing of pre- and post-synaptic spikes. "
        "Parameters: A_plus=0.1, A_minus=0.12, tau_plus=20.0, tau_minus=20.0."
    ),
    "synapse": (
        "Synapses connect neurons and transmit spikes. The network starts "
        "with ~10 connections per neuron. Synapses have weights (0.0-0.5), "
        "delays (1-20ms), and can be pruned or sprouted during self-organization."
    ),
    "neuron": (
        "Neurons use Izhikevich dynamics with parameters a=0.02, b=0.2, "
        "c=-65.0, d=8.0 (regular spiking). The network starts with 5000 "
        "neurons in a 5D grid of dimensions [10, 10, 10, 10, 10]."
    ),
    "experiment": (
        "Experiments are registered in the research registry. Use the "
        "Research tab to view registered experiments, their status, "
        "and evidence records. Experiments follow a structured workflow "
        "with pre-registration, execution, and analysis phases."
    ),
    "self-organization": (
        "Self-organization manages structural plasticity: pruning weak "
        "synapses (weight < 0.005, age > 1000 ticks), sprouting new "
        "connections (max 12 per neuron, radius 2.0), and neurogenesis "
        "(when spike rate delta exceeds 50 Hz)."
    ),
    "dashboard": (
        "The MHRN Operator Dashboard provides real-time telemetry: "
        "neural activity, learning metrics, structural changes, storage "
        "status, and experiment management. Tabs: Overview, Network, "
        "Control, Research, Release, Settings, Embodiment."
    ),
    "energy": (
        "Each neuron has an energy level (initial 1.0). Spikes cost "
        "0.001 energy. Homeostasis can manage energy with target=1.0, "
        "recovery_rate=0.001. Energy-affects-firing is disabled by default."
    ),
    "reward": (
        "The reward system modulates STDP based on external reward "
        "signals. Learning_rate=0.01, delay=5 ticks. Rewards can be "
        "used for reinforcement learning experiments."
    ),
    "structural plasticity": (
        "Structural plasticity encompasses pruning (removing weak synapses), "
        "sprouting (creating new connections), and neurogenesis (adding "
        "new neurons). All are configured in the `self_organization` section."
    ),
    "storage": (
        "Storage uses the .b5d binary format with journaling for crash "
        "recovery. Runtime deltas are captured for telemetry. Checkpoints "
        "can be written on demand via the dashboard Control tab."
    ),
    "tik tok": (
        "A tick is the basic simulation time step (dt=1.0ms). Each tick "
        "updates all neuron potentials, processes spikes, applies STDP, "
        "and runs self-organization at configured intervals."
    ),
    "help": (
        "I am the MHRN Local Fallback Assistant. I can answer basic "
        "questions about the system architecture, components, and "
        "configuration. For detailed analysis, please use Ollama. "
        "Try asking about: neurons, synapses, STDP, homeostasis, "
        "experiments, dashboard, energy, or self-organization."
    ),
}


class LocalFallbackBackend:
    """Zero-dependency local fallback AI backend.

    Generates responses using pattern matching against an embedded
    knowledge base and simple template expansion. No network calls,
    no model files, no external dependencies.

    The backend provides:
    - Keyword-based Q/A from embedded knowledge
    - Template-based responses for unknown queries
    - Metadata tracking (response time, match method, digest)
    - Full compatibility with the ChatBackend protocol
    """

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
        self._knowledge = {**knowledge_base} if knowledge_base else {}
        self._knowledge.update(_EMBEDDED_KNOWLEDGE)
        self._last_failure_event: AIInferenceFailureEvent | None = None

    @property
    def name(self) -> str:
        return "local-fallback"

    @property
    def last_failure_event(self) -> AIInferenceFailureEvent | None:
        return self._last_failure_event

    # ── LanguageModelBackend protocol ──

    def infer(self, request: LanguageRequest) -> LanguageResponse:
        """Implement the LanguageModelBackend protocol."""
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
                request_digest=hashlib.sha256(
                    request.text.encode("utf-8")
                ).hexdigest(),
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

    # ── Chat interface ──

    def generate_text(
        self,
        prompt: str,
        images: list[str] | None = None,
        tools: list[dict[str, object]] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Generate a response from the embedded knowledge base.

        Args:
            prompt: The input text prompt.
            images: Ignored (fallback has no vision capability).
            tools: Ignored (fallback has no tool-use capability).

        Returns:
            Tuple of (response_text, metadata_dict).
        """
        del images  # not supported
        del tools  # not supported

        started_ns = time.perf_counter_ns()
        response, match_info = self._match_response(prompt)
        elapsed_ms = (time.perf_counter_ns() - started_ns) / 1_000_000

        metadata: dict[str, Any] = {
            "model": self.model,
            "provider": self.name,
            "response_digest": hashlib.sha256(
                response.encode("utf-8")
            ).hexdigest(),
            "total_duration_ns": (time.perf_counter_ns() - started_ns),
            "eval_duration_ms": elapsed_ms,
            "match_method": match_info.get("method", "template"),
            "match_confidence": match_info.get("confidence", 0.5),
            "match_keywords": match_info.get("keywords", []),
            "structured_output_valid": True,
            "vision_enabled": False,
            "tools_enabled": False,
        }
        return response, metadata

    def __call__(self, prompt: str) -> tuple[dict[str, Any], dict[str, Any]]:
        """Return schema-shaped analysis (for AIRR compatibility)."""
        text, metadata = self.generate_text(prompt)
        return {"response": text, "assessment": text}, metadata

    # ── Response engine ──

    def _match_response(self, prompt: str) -> tuple[str, dict[str, Any]]:
        """Match a prompt against the knowledge base and return a response.

        Strategy:
        1. Extract keywords from the prompt
        2. Score each knowledge entry by keyword overlap
        3. If best score > threshold, return the matched answer
        4. Otherwise, generate a template-based response
        """
        # Normalize and extract significant words
        clean = re.sub(r"[^\w\s]", " ", prompt.lower())
        words = [w for w in clean.split() if len(w) > 2 and w not in _STOP_WORDS]
        keywords = list(dict.fromkeys(words))  # deduplicate, preserve order

        if not keywords:
            return self._greeting_response(), {
                "method": "greeting",
                "confidence": 1.0,
                "keywords": [],
            }

        # Score each knowledge entry
        best_key: str | None = None
        best_score = 0.0
        for key, _value in self._knowledge.items():
            key_words = set(key.split())
            if not key_words:
                continue
            # Jaccard-like similarity
            overlap = sum(1 for w in keywords if w in key_words)
            score = overlap / (len(key_words) + len(keywords) - overlap + 0.001)
            if score > best_score:
                best_score = score
                best_key = key

        # Threshold for direct match
        if best_key is not None and best_score >= 0.25:
            return self._knowledge[best_key], {
                "method": "knowledge_match",
                "confidence": round(best_score, 3),
                "keywords": keywords[:8],
                "matched_key": best_key,
            }

        # Check for question patterns
        return self._template_response(keywords, prompt), {
            "method": "template",
            "confidence": round(best_score, 3),
            "keywords": keywords[:8],
        }

    def _greeting_response(self) -> str:
        """Return a greeting when no specific question is detected."""
        greetings = [
            "Hallo! Ich bin der MHRN Local Fallback Assistant. "
            "Wie kann ich Ihnen helfen? Fragen Sie z. B. nach "
            "Neuronen, Synapsen, STDP oder Homöostase.",
            "Willkommen beim MHRN Research Assistant (Fallback-Modus). "
            "Ich beantworte Fragen zur Systemarchitektur. "
            "Tipp: Fragen Sie nach 'Neuronen', 'Synapsen' oder 'Experimenten'.",
        ]
        return self._rng.choice(greetings)

    def _template_response(
        self, keywords: list[str], original: str
    ) -> str:
        """Generate a template-based response for unrecognized queries."""
        # Categorize keywords
        question_words = {"was", "wie", "warum", "wann", "wo", "wer", "welche",
                          "what", "how", "why", "when", "where", "who", "which",
                          "is", "are", "does", "can", "do", "define", "explain",
                          "describe", "tell", "meaning", "purpose", "function"}
        is_question = any(w in question_words for w in keywords[:5])

        # Build context-aware response
        if is_question:
            response = (
                "Ihre Frage enthält Begriffe, zu denen ich keine "
                "spezifischen Informationen in meiner Wissensdatenbank habe. "
            )
        else:
            response = (
                "Ich habe Ihre Eingabe erhalten, kann aber keine "
                "direkte Übereinstimmung in meiner Wissensdatenbank finden. "
            )

        # Add keyword context if available
        if keywords:
            known = [k for k in keywords if k in self._knowledge]
            if known:
                response += (
                    f" Ich habe Informationen zu: {', '.join(known[:5])}. "
                    f"Stellen Sie eine gezielte Frage dazu."
                )
            else:
                response += (
                    "Die genannten Begriffe sind mir nicht bekannt. "
                    "Versuchen Sie es mit: Neuronen, Synapsen, STDP, "
                    "Homöostase, Experimente, Energie oder Dashboard."
                )

        response += (
            "\n\nHinweis: Für detaillierte Analysen aktivieren Sie bitte "
            "Ollama in den Chat-Einstellungen."
        )
        return response

    def _repair_json(self, text: str) -> dict[str, Any]:
        """Attempt to repair malformed JSON (for AIRR compatibility)."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"response": text, "assessment": text}


# ── Stop words ─────────────────────────────────────────────────────────────

_STOP_WORDS: set[str] = {
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen",
    "einem", "eines", "und", "oder", "aber", "mit", "von", "für",
    "auf", "an", "in", "zu", "aus", "bei", "nach", "um", "vor",
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can",
    "not", "no", "nor", "but", "or", "if", "so", "as", "at",
    "by", "for", "from", "in", "into", "of", "on", "to", "with",
    "it", "its", "this", "that", "these", "those", "we", "you",
    "they", "he", "she", "them", "their", "your", "our", "my",
    "bitte", "danke", "gern", "gerne", "hallo", "hi", "hey",
}


# ── Module-level factory ───────────────────────────────────────────────────

def create_local_fallback_backend(
    model: str = "local-fallback",
    **kwargs: Any,
) -> LocalFallbackBackend:
    """Create a configured LocalFallbackBackend instance.

    Args:
        model: Model identifier string.
        **kwargs: Additional arguments passed to LocalFallbackBackend.__init__.

    Returns:
        A configured LocalFallbackBackend instance.
    """
    return LocalFallbackBackend(model=model, **kwargs)
