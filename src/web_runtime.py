#!/usr/bin/env python3
"""Shared runtime helpers for the local web manager."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Sequence
from urllib.parse import urlparse

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = Path(
    os.getenv("OPENFANG_OUTPUT_DIR", str(Path.home() / ".openfang"))
).expanduser()
TASKS_FILE = DEFAULT_OUTPUT_DIR / "web_tasks.json"
MAX_LOG_CHARS = 20_000


def now_iso() -> str:
    """Return the current timestamp in ISO 8601 format."""
    return datetime.now().isoformat(timespec="seconds")


def resolve_project_dir() -> Path:
    """Return the repository root used by the web manager."""
    return Path(
        os.getenv("OPENFANG_AUTO_CLIP_PROJECT_DIR", str(PROJECT_DIR))
    ).expanduser().resolve()


def resolve_output_dir() -> Path:
    """Return the output root for generated assets and task metadata."""
    return DEFAULT_OUTPUT_DIR.resolve()


def resolve_ip_characters_dir() -> Path:
    """Return the directory that stores generated IP character projects."""
    return resolve_output_dir() / "ip_characters"


def resolve_tasks_file() -> Path:
    """Return the persisted task status file."""
    return TASKS_FILE.resolve()


def validate_video_url(url: str) -> bool:
    """Basic validation for externally supplied video URLs."""
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return False

    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def parse_transform_level(raw_value: Any, default: int = 1) -> int:
    """Normalize transform level input to a safe integer."""
    if raw_value in (None, ""):
        return default

    try:
        level = int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError("transform_level must be an integer") from exc

    if level not in {0, 1, 2, 3}:
        raise ValueError("transform_level must be one of 0, 1, 2, 3")

    return level


def is_allowed_path(raw_path: str | Path) -> bool:
    """Allow opening only paths inside the repo or output directory."""
    candidate = Path(raw_path).expanduser().resolve()
    allowed_roots = (resolve_project_dir(), resolve_output_dir())
    return any(root == candidate or root in candidate.parents for root in allowed_roots)


def build_python_command(script_name: str, *args: Any) -> list[str]:
    """Build a Python command that executes one of the repository scripts."""
    script_path = resolve_project_dir() / script_name
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    return [sys.executable, str(script_path), *[str(arg) for arg in args]]


def truncate_output(text: str) -> str:
    """Keep persisted task logs bounded."""
    if len(text) <= MAX_LOG_CHARS:
        return text
    return text[-MAX_LOG_CHARS:]


class TaskStore:
    """Thread-safe task persistence for the local web manager."""

    def __init__(self, tasks_file: Optional[Path] = None):
        self.tasks_file = (tasks_file or resolve_tasks_file()).expanduser().resolve()
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._tasks = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        if not self.tasks_file.exists():
            return {}

        try:
            with self.tasks_file.open() as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            return {}

        if isinstance(data, dict):
            return data

        return {}

    def _save(self) -> None:
        with self.tasks_file.open("w") as handle:
            json.dump(self._tasks, handle, indent=2, ensure_ascii=False)

    def create(
        self,
        task_id: str,
        command: Sequence[str],
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        task = {
            "status": "running",
            "output": "",
            "error": "",
            "command": list(command),
            "start_time": now_iso(),
        }
        if metadata:
            task.update(metadata)

        with self._lock:
            self._tasks[task_id] = task
            self._save()

        return task

    def update(self, task_id: str, **fields: Any) -> dict[str, Any]:
        with self._lock:
            task = self._tasks.setdefault(task_id, {})
            task.update(fields)
            self._save()
            return dict(task)

    def get(self, task_id: str) -> Optional[dict[str, Any]]:
        with self._lock:
            task = self._tasks.get(task_id)
            return dict(task) if task else None

    def all(self) -> dict[str, dict[str, Any]]:
        with self._lock:
            return {task_id: dict(task) for task_id, task in self._tasks.items()}


def run_command_async(
    command: Sequence[str],
    task_id: str,
    store: TaskStore,
    metadata: Optional[dict[str, Any]] = None,
    cwd: Optional[Path] = None,
) -> None:
    """Run a subprocess and persist its result."""
    store.create(task_id, command, metadata=metadata)

    try:
        process = subprocess.Popen(
            [str(part) for part in command],
            cwd=str((cwd or resolve_project_dir()).resolve()),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()

        store.update(
            task_id,
            status="completed" if process.returncode == 0 else "error",
            output=truncate_output(stdout),
            error=truncate_output(stderr),
            end_time=now_iso(),
            return_code=process.returncode,
        )
    except Exception as exc:
        store.update(
            task_id,
            status="error",
            error=str(exc),
            end_time=now_iso(),
            return_code=-1,
        )


def start_background_task(
    prefix: str,
    command: Sequence[str],
    store: TaskStore,
    metadata: Optional[dict[str, Any]] = None,
    cwd: Optional[Path] = None,
) -> str:
    """Create a task id and dispatch the command in a background thread."""
    task_id = f"{prefix}_{int(time.time() * 1000)}"
    thread = threading.Thread(
        target=run_command_async,
        args=(command, task_id, store),
        kwargs={"metadata": metadata, "cwd": cwd},
        daemon=True,
    )
    thread.start()
    return task_id
