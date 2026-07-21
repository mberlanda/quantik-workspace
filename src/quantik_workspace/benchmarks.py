"""Repository-owned benchmark invocation and report comparison."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import WorkspaceConfig
from .subprocesses import run


def benchmark_run(config: WorkspaceConfig, repository: str, *, execute: bool = False) -> dict[str, Any]:
    command = config.repositories[repository].get("commands", {}).get("benchmark", [])
    if not command:
        return {"status": "missing", "repository": repository, "diagnostics": "No benchmark command is declared."}
    if not execute:
        return {"status": "planned", "repository": repository, "command": command}
    result = run(command, config.repository_path(repository), timeout=3600)
    return {"status": "passed", "repository": repository, "command": command, "stdout": result.stdout, "stderr": result.stderr}


def benchmark_compare(left: Path, right: Path) -> dict[str, Any]:
    left_value = json.loads(left.read_text(encoding="utf-8"))
    right_value = json.loads(right.read_text(encoding="utf-8"))
    differences: list[dict[str, Any]] = []
    keys = sorted(set(left_value) | set(right_value)) if isinstance(left_value, dict) and isinstance(right_value, dict) else []
    for key in keys:
        if left_value.get(key) != right_value.get(key):
            differences.append({"field": key, "left": left_value.get(key), "right": right_value.get(key)})
    return {"status": "different" if differences else "equal", "left": str(left), "right": str(right), "differences": differences}

