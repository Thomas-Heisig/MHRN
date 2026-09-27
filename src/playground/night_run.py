"""Bounded overnight meta-learning runner for the PAN Playground."""

from __future__ import annotations

import argparse
import json
import signal
import threading
import time
import uuid
from pathlib import Path
from typing import Callable

from .meta_learning import KnowledgeBase, MetaReward, MetaTaskGenerator, text_vector
from .models import PlaygroundConfig
from .pan.live_session import PANLiveSession

GatewayQuery = Callable[[str], str | None]


class NightRunDaemon:
    """Run bounded strategy-learning episodes with checkpoints and summaries."""

    def __init__(
        self,
        *,
        hours: float = 8.0,
        max_episodes: int = 10_000,
        checkpoint_seconds: float = 600.0,
        output_root: Path = Path("playground_sessions/night_runs"),
        seed: int = 12345,
        gateway_query: GatewayQuery | None = None,
        file_roots: list[Path] | None = None,
        config: PlaygroundConfig | None = None,
        resume_dir: Path | None = None,
    ) -> None:
        if not 0.01 <= hours <= 24.0:
            raise ValueError("hours must be between 0.01 and 24")
        if not 1 <= max_episodes <= 1_000_000:
            raise ValueError("max_episodes outside allowed range")
        if not 10.0 <= checkpoint_seconds <= 3600.0:
            raise ValueError("checkpoint_seconds must be between 10 and 3600")
        self.hours = hours
        self.max_episodes = max_episodes
        self.checkpoint_seconds = checkpoint_seconds
        self.gateway_query = gateway_query
        self.run_id = resume_dir.name if resume_dir is not None else "PGNIGHT-" + uuid.uuid4().hex[:12]
        self.run_dir = resume_dir if resume_dir is not None else output_root / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_path = self.run_dir / "episodes.jsonl"
        self.status_path = self.run_dir / "status.json"
        self.summary_path = self.run_dir / "summary.json"
        self.analysis_path = self.run_dir / "analysis.json"
        self.kb_path = self.run_dir / "knowledge_base.json"
        self.checkpoint_path = self.run_dir / "checkpoint.json"
        self.task_gen = MetaTaskGenerator(seed=seed)
        self.reward_fn = MetaReward()
        self.kb = KnowledgeBase()
        self.config = config or PlaygroundConfig.from_mapping(
            {
                "name": self.run_id,
                "neuron_model": "pan_adex_5d",
                "pan_enabled": True,
                "pan_bias_current": 15.0,
                "thalamic_gating_enabled": True,
                "thalamic_relay_threshold": 0.0,
                "behavior_learning_enabled": True,
                "behavior_action_count": 4,
                "behavior_target_mode": "cycle",
                "execution_mode": "HYBRID_AUTO",
                "execution_initial_mode": "EVENT_ONLY",
                "n_neurons": 128,
                "edge_budget": 512,
                "seed": seed,
                "ticks": 256,
            }
        )
        self.pan = PANLiveSession(self.config)
        self.pan.auto_reward_enabled = False
        self.running = True
        self.started_at = time.time()
        self.last_checkpoint_at = self.started_at
        self.episode = 0
        self.total_reward = 0.0
        self.task_counts = {"find_source": 0, "store_info": 0, "link_info": 0}
        self.reward_by_task = {key: 0.0 for key in self.task_counts}
        self.errors: list[str] = []
        self._install_signals()

        roots = [Path("docs/playground"), Path("src/playground")] if file_roots is None else file_roots
        self.kb.index_files(roots, category="Konzepte", max_files=120)
        # Seed vector memory so find/link are available from the first episodes.
        bootstrap = {
            "Personen": "profile contact biography bootstrap-alpha",
            "Orte": "address location city bootstrap-beta",
            "Ereignisse": "date meeting launch bootstrap-gamma",
            "Konzepte": "definition principle method bootstrap-delta",
        }
        for category, text in bootstrap.items():
            self.kb.store_info(text, category)
        if resume_dir is not None:
            self._restore_checkpoint()

    def _restore_checkpoint(self) -> None:
        if not self.checkpoint_path.exists():
            raise FileNotFoundError(f"night-run checkpoint not found: {self.checkpoint_path}")
        payload = json.loads(self.checkpoint_path.read_text(encoding="utf-8"))
        raw_status = payload.get("status", {})
        if isinstance(raw_status, dict):
            self.episode = int(raw_status.get("episode", 0))
            self.total_reward = float(raw_status.get("total_reward", 0.0))
            elapsed = float(raw_status.get("elapsed_seconds", 0.0))
            self.started_at = time.time() - max(0.0, elapsed)
            raw_counts = raw_status.get("task_counts")
            if isinstance(raw_counts, dict):
                self.task_counts = {key: int(raw_counts.get(key, 0)) for key in self.task_counts}
            raw_rewards = raw_status.get("reward_by_task")
            if isinstance(raw_rewards, dict):
                self.reward_by_task = {key: float(raw_rewards.get(key, 0.0)) for key in self.reward_by_task}
        raw_pan = payload.get("pan_checkpoint")
        if isinstance(raw_pan, dict):
            self.pan.import_checkpoint(raw_pan)
        raw_kb = payload.get("knowledge_base")
        if isinstance(raw_kb, dict):
            self.kb = KnowledgeBase.from_snapshot(raw_kb)
        self.task_gen.counter = int(payload.get("task_counter", self.episode))
        self.last_checkpoint_at = time.time()

    def _install_signals(self) -> None:
        try:
            signal.signal(signal.SIGINT, self.shutdown)
            signal.signal(signal.SIGTERM, self.shutdown)
        except ValueError:
            # Signal registration is only legal from the main thread.
            pass

    def shutdown(self, *_: object) -> None:
        self.running = False

    def should_continue(self) -> bool:
        elapsed_hours = (time.time() - self.started_at) / 3600.0
        return (
            self.running
            and elapsed_hours < self.hours
            and self.episode < self.max_episodes
        )

    def _encode_task(self, task: dict[str, object]) -> list[float]:
        safe = {
            key: value
            for key, value in task.items()
            if key not in {"true_source", "true_category", "true_relation"}
        }
        return text_vector(
            json.dumps(safe, sort_keys=True, ensure_ascii=False),
            self.config.n_neurons,
        )

    def _choice(self, context: str, options: list[str]) -> tuple[int, str]:
        index = self.pan.learning.choose_context_action(context, len(options))
        return index, options[index]

    def _find(self, task: dict[str, object]) -> tuple[dict[str, object], dict[str, object], list[tuple[str, int, int, float]]]:
        sources = [str(item) for item in task["possible_sources"]]
        categories = [str(item) for item in task["possible_categories"]]
        source_index, source = self._choice("find:source", sources)
        category_index, category = self._choice("find:category", categories)
        action = {"source": source, "category": category}
        if source == "gateway":
            answer = self.gateway_query(str(task["question"])) if self.gateway_query else None
            result = {
                "found": answer is not None,
                "source": "gateway",
                "answer_available": answer is not None,
            }
        else:
            result = self.kb.find(
                str(task["question"]), source=source, category=category, limit=3
            )
        reward = self.reward_fn.compute(task, action, result)
        updates = [
            ("find:source", source_index, len(sources), reward["source"]),
            ("find:category", category_index, len(categories), reward["category"]),
        ]
        return action, result, updates

    def _store(self, task: dict[str, object]) -> tuple[dict[str, object], dict[str, object], list[tuple[str, int, int, float]]]:
        categories = [str(item) for item in task["possible_categories"]]
        index, category = self._choice("store:category", categories)
        action = {"category": category}
        result = self.kb.store_info(str(task["info"]), category)
        reward = self.reward_fn.compute(task, action, result)
        return action, result, [("store:category", index, len(categories), reward["category"])]

    def _link(self, task: dict[str, object]) -> tuple[dict[str, object], dict[str, object], list[tuple[str, int, int, float]]]:
        relations = [str(item) for item in task["possible_relations"]]
        index, relation = self._choice("link:relation", relations)
        action = {"relation": relation}
        result = self.kb.link(
            str(task["left_id"]), str(task["right_id"]), relation
        )
        reward = self.reward_fn.compute(task, action, result)
        return action, result, [("link:relation", index, len(relations), reward["relation"])]

    def run_episode(self) -> dict[str, object]:
        task = self.task_gen.generate(
            self.kb, gateway_available=self.gateway_query is not None
        )
        vector = self._encode_task(task)
        if task["type"] == "find_source":
            self.pan.learning.activate_context(
                "find:source", len(task["possible_sources"])
            )
        elif task["type"] == "store_info":
            self.pan.learning.activate_context(
                "store:category", len(task["possible_categories"])
            )
        else:
            self.pan.learning.activate_context(
                "link:relation", len(task["possible_relations"])
            )
        self.pan.inject_vector(vector, duration_ticks=8, gain=25.0)
        pan_result = self.pan.step(16)

        if task["type"] == "find_source":
            action, result, updates = self._find(task)
        elif task["type"] == "store_info":
            action, result, updates = self._store(task)
        else:
            action, result, updates = self._link(task)

        reward_components = self.reward_fn.compute(task, action, result)
        for context, action_index, action_count, reward in updates:
            self.pan.learning.apply_external_reward(
                context=context,
                action=action_index,
                reward=reward,
                action_count=action_count,
            )

        reward = float(reward_components["total"])
        self.episode += 1
        self.total_reward += reward
        task_type = str(task["type"])
        self.task_counts[task_type] += 1
        self.reward_by_task[task_type] += reward
        event = {
            "episode": self.episode,
            "time": time.time(),
            "task_type": task_type,
            "action": action,
            "reward": reward,
            "reward_components": reward_components,
            "result_summary": {
                "found": result.get("found"),
                "stored": result.get("stored"),
                "linked": result.get("linked"),
            },
            "pan": {
                "tick": pan_result["tick"],
                "total_spikes": pan_result["total_spikes"],
                "current_engine": pan_result["execution"]["current_engine"],
            },
        }
        with self.metrics_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
        return event

    def status_snapshot(self, *, final: bool = False) -> dict[str, object]:
        now = time.time()
        elapsed = now - self.started_at
        return {
            "classification": "PLAYGROUND_NIGHT_RUN",
            "scientific_evidence": False,
            "run_id": self.run_id,
            "running": self.running and not final,
            "episode": self.episode,
            "max_episodes": self.max_episodes,
            "elapsed_seconds": elapsed,
            "configured_hours": self.hours,
            "total_reward": self.total_reward,
            "mean_reward": self.total_reward / self.episode if self.episode else 0.0,
            "task_counts": dict(self.task_counts),
            "reward_by_task": dict(self.reward_by_task),
            "pan": self.pan.snapshot(),
            "knowledge_records": len(self.kb.records),
            "relations": len(self.kb.relations),
            "errors": list(self.errors[-20:]),
            "updated_at": now,
        }

    def checkpoint(self, *, final: bool = False) -> dict[str, object]:
        status = self.status_snapshot(final=final)
        self.status_path.write_text(
            json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self.kb.save(self.kb_path)
        self.checkpoint_path.write_text(
            json.dumps(
                {
                    "classification": "PLAYGROUND_NIGHT_CHECKPOINT",
                    "scientific_evidence": False,
                    "status": status,
                    "task_counter": self.task_gen.counter,
                    "pan_checkpoint": self.pan.export_checkpoint(),
                    "knowledge_base": self.kb.snapshot(),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        if final:
            self.summary_path.write_text(
                json.dumps(status, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        self.last_checkpoint_at = time.time()
        return status

    def run(self) -> dict[str, object]:
        self.checkpoint()
        try:
            while self.should_continue():
                self.run_episode()
                if time.time() - self.last_checkpoint_at >= self.checkpoint_seconds:
                    self.checkpoint()
        except Exception as exc:
            self.errors.append(f"{type(exc).__name__}: {exc}")
            self.running = False
            self.checkpoint(final=True)
            raise
        self.running = False
        status = self.checkpoint(final=True)
        analysis = analyze_run(self.run_dir)
        self.analysis_path.write_text(
            json.dumps(analysis, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        status["analysis"] = analysis
        self.summary_path.write_text(
            json.dumps(status, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return status


def analyze_run(run_dir: Path) -> dict[str, object]:
    events: list[dict[str, object]] = []
    metrics_path = run_dir / "episodes.jsonl"
    if metrics_path.exists():
        for line in metrics_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
    rewards = [float(item.get("reward", 0.0)) for item in events]
    half = max(1, len(rewards) // 2)
    first = rewards[:half]
    second = rewards[-half:]
    return {
        "classification": "PLAYGROUND_NIGHT_ANALYSIS",
        "scientific_evidence": False,
        "run_id": run_dir.name,
        "episodes": len(events),
        "mean_reward": sum(rewards) / len(rewards) if rewards else 0.0,
        "first_half_mean": sum(first) / len(first) if first else 0.0,
        "second_half_mean": sum(second) / len(second) if second else 0.0,
        "reward_delta": (
            (sum(second) / len(second) if second else 0.0)
            - (sum(first) / len(first) if first else 0.0)
        ),
        "positive_fraction": (
            sum(1 for value in rewards if value > 0.0) / len(rewards)
            if rewards
            else 0.0
        ),
        "interpretation": (
            "Descriptive Playground metric only; reward increase is not scientific evidence."
        ),
    }


def _main() -> None:
    parser = argparse.ArgumentParser(description="Run PAN Playground overnight meta-learning.")
    parser.add_argument("--hours", type=float, default=8.0)
    parser.add_argument("--max-episodes", type=int, default=10_000)
    parser.add_argument("--checkpoint-seconds", type=float, default=600.0)
    parser.add_argument("--seed", type=int, default=12345)
    parser.add_argument("--output-root", type=Path, default=Path("playground_sessions/night_runs"))
    parser.add_argument("--resume", type=Path, default=None)
    args = parser.parse_args()
    daemon = NightRunDaemon(
        hours=args.hours,
        max_episodes=args.max_episodes,
        checkpoint_seconds=args.checkpoint_seconds,
        seed=args.seed,
        output_root=args.output_root,
        resume_dir=args.resume,
    )
    summary = daemon.run()
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _main()



class NightRunManager:
    """Bounded in-process manager for one active Playground night run."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._daemon: NightRunDaemon | None = None
        self._thread: threading.Thread | None = None
        self._last_summary: dict[str, object] | None = None
        self._last_error: str | None = None

    def start(
        self,
        *,
        hours: float = 8.0,
        max_episodes: int = 10_000,
        checkpoint_seconds: float = 600.0,
        seed: int = 12345,
    ) -> dict[str, object]:
        with self._lock:
            if self._thread is not None and self._thread.is_alive():
                raise RuntimeError("a Playground night run is already active")
            daemon = NightRunDaemon(
                hours=hours,
                max_episodes=max_episodes,
                checkpoint_seconds=checkpoint_seconds,
                seed=seed,
            )
            self._daemon = daemon
            self._last_summary = None
            self._last_error = None
            thread = threading.Thread(
                target=self._worker,
                name=f"pan-night-{daemon.run_id}",
                daemon=True,
            )
            self._thread = thread
            thread.start()
            return self.status()

    def _worker(self) -> None:
        daemon = self._daemon
        if daemon is None:
            return
        try:
            summary = daemon.run()
            with self._lock:
                self._last_summary = summary
        except Exception as exc:
            with self._lock:
                self._last_error = f"{type(exc).__name__}: {exc}"

    def stop(self) -> dict[str, object]:
        with self._lock:
            daemon = self._daemon
            if daemon is None:
                raise RuntimeError("no Playground night run exists")
            daemon.shutdown()
        return self.status()

    def status(self) -> dict[str, object]:
        with self._lock:
            daemon = self._daemon
            thread = self._thread
            if daemon is None:
                return {
                    "classification": "PLAYGROUND_NIGHT_RUN_MANAGER",
                    "scientific_evidence": False,
                    "active": False,
                    "last_summary": self._last_summary,
                    "last_error": self._last_error,
                }
            active = bool(thread and thread.is_alive())
            current = daemon.status_snapshot() if active else (
                self._last_summary or daemon.status_snapshot(final=True)
            )
            return {
                "classification": "PLAYGROUND_NIGHT_RUN_MANAGER",
                "scientific_evidence": False,
                "active": active,
                "run_id": daemon.run_id,
                "status": current,
                "last_error": self._last_error,
            }
