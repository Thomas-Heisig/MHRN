"""Bounded research chat with repository-wide read-only retrieval."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol, cast

from .contracts import AIExposure, AIInteractionRecord, CausalTaint
from .firewall import ScientificAIFirewall
from .governance import KnowledgeOrigin, NetworkMode, RetrievalRecord
from .repository_context import RepositoryContext


class _ResearchDocument(Protocol):
    path: str
    kind: str


class _ResearchSource(Protocol):
    def list_documents(self) -> Sequence[_ResearchDocument]: ...
    def read_content(self, path: str) -> str: ...


class _DocDocument(Protocol):
    path: str
    file_type: Any


class _DocsSource(Protocol):
    def list_documents(
        self, recursive: bool = False, max_count: int = 0
    ) -> Sequence[_DocDocument]: ...
    def read_content(self, path: str) -> str: ...


class ChatBackend(Protocol):
    """Callable read-only research-chat backend contract."""

    def __call__(self, prompt: str) -> tuple[str, dict[str, Any]]: ...


@dataclass(frozen=True, slots=True)
class ResearchChat:
    """Construct grounded repository prompts; responses have no mutation authority."""

    research: _ResearchSource
    docs: _DocsSource
    backend: ChatBackend
    max_context_chars: int = 80_000
    system_context: str = ""
    web_context: str = ""
    system_prompt: str = ""
    conversation_context: str = ""
    handoff_prompt: str = ""
    response_mode: str = "detailed"
    firewall: ScientificAIFirewall = ScientificAIFirewall()
    config_tool_enabled: bool = False

    def answer(self, message: str) -> tuple[str, dict[str, Any]]:
        question = message.strip()
        if not question:
            raise ValueError("Chat message must not be empty.")
        if self.response_mode not in {"short", "detailed", "scientific"}:
            raise ValueError("Unsupported response mode.")
        self.firewall.assert_read_only()
        self.firewall.authorize("interpret")
        repository = self._repository_context(question)
        prompt = self._prompt(question, repository)
        answer, metadata = self.backend(prompt)
        retrieval = self._retrieval_record(repository)
        metadata = {
            **metadata,
            "retrieval": retrieval.to_dict(),
            "repository_retrieval": {
                "digest": repository.digest,
                "indexed_files": repository.indexed_files,
                "selected_files": list(repository.selected_files),
                "omitted_large_files": repository.omitted_large_files,
                "authority": "read_only_non_evidentiary",
            },
        }
        interaction = AIInteractionRecord.create(
            role="research_ai",
            experiment_id=None,
            tick=None,
            input_value=question,
            prompt=prompt,
            output_value=answer,
            model_provenance=metadata,
            authority="read_only",
            exposure=AIExposure.OBSERVER_ONLY,
            causal_effect=CausalTaint.OBSERVED,
        )
        return answer, {**metadata, "ai_interaction": interaction.to_dict()}

    def _repository_context(self, question: str) -> RepositoryContext:
        del question  # Retrieval is bounded by source inventories, not free-text execution.
        chunks: list[str] = []
        paths: list[str] = []
        max_docs = min(16, max(4, self.max_context_chars // 4000))

        def _try_read(source: _ResearchSource | _DocsSource, path: str) -> str | None:
            try:
                content = source.read_content(path)
                return content[:6000]
            except (OSError, ValueError, FileNotFoundError, UnicodeError):
                return None

        def _append_documents(
            label: str,
            source: _ResearchSource | _DocsSource,
            documents: Sequence[_ResearchDocument | _DocDocument],
        ) -> None:
            chunks.append(label)
            for document in documents:
                if len(paths) >= max_docs:
                    break
                doc_path = document.path
                paths.append(doc_path)
                content = _try_read(source, doc_path)
                if content:
                    chunks.append(f"[{doc_path}]\n{content}")

        research_documents = list(self.research.list_documents())[:max_docs]
        _append_documents(
            "SCIENTIFIC RESEARCH SOURCES",
            self.research,
            research_documents,
        )

        remaining = max(0, max_docs - len(paths))
        if remaining:
            documentation_documents = self.docs.list_documents(max_count=remaining)
            _append_documents(
                "DOCUMENTATION SOURCES",
                self.docs,
                documentation_documents,
            )

        text = "\n\n".join(chunks)[: self.max_context_chars]
        return RepositoryContext(
            text,
            hashlib.sha256(text.encode("utf-8")).hexdigest(),
            len(paths),
            tuple(paths),
            0,
        )

    def _retrieval_record(self, repository: RepositoryContext) -> RetrievalRecord:
        web_enabled = bool(self.web_context.strip())
        mode = NetworkMode.LIVE_NETWORK if web_enabled else NetworkMode.FROZEN_CORPUS
        snapshot_digest = hashlib.sha256(
            json.dumps(
                {
                    "repository_digest": repository.digest,
                    "system_context": self.system_context,
                    "web_context": self.web_context,
                    "conversation_context": self.conversation_context,
                },
                sort_keys=True,
                ensure_ascii=True,
            ).encode("utf-8")
        ).hexdigest()
        source_count = len(repository.selected_files) + (1 if web_enabled else 0)
        return RetrievalRecord(
            enabled=True,
            mode=mode,
            snapshot_digest=snapshot_digest,
            source_count=source_count,
            knowledge_origin=(
                KnowledgeOrigin.EXTERNAL_RETRIEVAL
                if web_enabled
                else KnowledgeOrigin.SYSTEM_STATE
            ),
        )

    def _prompt(self, message: str, repository: RepositoryContext | None = None) -> str:
        if repository is None:
            repository = self._repository_context(message)
        context = repository.text
        if self.system_context:
            context = f"SYSTEM READ-ONLY CONTEXT:\n{self.system_context}\n\n{context}"
        if self.web_context:
            context = f"WEB SOURCES (external and unverified):\n{self.web_context}\n\n{context}"
        if self.conversation_context:
            context = (
                "CHAT HIERARCHY (conversation context, not evidence):\n"
                f"{self.conversation_context}\n\n{context}"
            )
        if self.handoff_prompt.strip():
            context = (
                "HANDOFF INSTRUCTIONS (editable operator context, not evidence):\n"
                f"{self.handoff_prompt.strip()}\n\n{context}"
            )
        mode_instructions = {
            "short": "Response mode: SHORT. Answer in at most 5 concise bullet points. Lead with the direct answer and omit background.",
            "detailed": "Response mode: DETAILED. Explain the answer with relevant context, status, exact repository paths, uncertainty, and a concise conclusion.",
            "scientific": "Response mode: SCIENTIFIC. Separate research question, method/protocol, DATA, EVIDENCE, limitations, AI interpretation, and human conclusion. Never upgrade inconclusive or untested status.",
        }[self.response_mode]
        return (
            (f"{self.system_prompt.strip()}\n" if self.system_prompt.strip() else "")
            + "You are the MHRN Research Self-Knowledge Assistant.\n"
            "You are an AI assistant, not a person and not a scientific authority.\n"
            "The repository retrieval layer can inspect the whole eligible repository tree, but only selected bounded snippets are supplied per question.\n"
            "Answer only from supplied read-only context and cite exact repository paths.\n"
            "Large/binary files may be represented by index metadata/digests; never pretend their omitted bytes were read.\n"
            "If WEB SOURCES are supplied, cite their URLs and label them external/unverified.\n"
            "Clearly distinguish internal DATA, accepted EVIDENCE, source code/docs, WEB SOURCES, AI interpretation, and human conclusion.\n"
            "Source code, docs, AI output and web content are never automatically scientific EVID.\n"
            "Never invent values or experiment results; never execute an experiment from free text.\n"
            "WEB SOURCES must never appear under EVIDENCE.\n"
            + (
                "CONFIG TOOL: You can read and update the active YAML configuration file.\n"
                "  To READ a config value, respond with exactly:\n"
                "    [CONFIG_READ] key.name\n"
                "  To WRITE a config value, respond with exactly:\n"
                "    [CONFIG_WRITE] key.name = value\n"
                "  Supported keys include: initial_neurons, max_neurons, dimensions, seed,\n"
                "  simulation.ticks, simulation.dt_ms, neuron.a-d, network.*, homeostasis.*,\n"
                "  stdp.*, eligibility.*, reward.*, self_organization.*, and more.\n"
                "  The change takes effect after a restart.\n"
                if self.config_tool_enabled
                else ""
            )
            + f"{mode_instructions}\n"
            "For current-running questions use only explicit SYSTEM READ-ONLY CONTEXT runtime/session fields. Completed experiments do not prove a live run.\n"
            f"User question: {message}\n\nRepository context:\n{context[: self.max_context_chars]}"
        )


def chat_backend_from_text_backend(backend: Any) -> ChatBackend:
    """Adapt a shared provider backend returning text or ``(text, metadata)``."""

    def call(prompt: str) -> tuple[str, dict[str, Any]]:
        result = backend(prompt)
        if isinstance(result, tuple):
            tuple_result = cast(tuple[object, ...], result)
            if len(tuple_result) != 2:
                raise ValueError("Chat backend must return text or (text, metadata).")
            text, metadata = tuple_result
            if isinstance(text, str) and isinstance(metadata, dict):
                typed_metadata = cast(dict[object, Any], metadata)
                return text, {str(key): value for key, value in typed_metadata.items()}
        if isinstance(result, str):
            return result, {}
        raise ValueError("Chat backend must return text or (text, metadata).")

    return call
