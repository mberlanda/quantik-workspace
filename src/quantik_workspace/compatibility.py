"""Adapter orchestration and structured result collection."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .config import WorkspaceConfig
from .models import CompatibilityResult
from .subprocesses import CommandError, run


CATEGORIES = {
    "contract violation",
    "implementation bug",
    "serialization difference",
    "ordering difference",
    "numerical tolerance issue",
    "intentional implementation-specific behaviour",
    "missing coverage",
    "infrastructure failure",
}


def invoke_adapter(repository: str, operation: str, command: list[str], cwd: Path) -> CompatibilityResult:
    try:
        result = run(command, cwd)
    except (CommandError, OSError) as exc:
        return CompatibilityResult(repository, operation, "failed", "infrastructure failure", str(exc))
    output: dict[str, Any] | None = None
    if result.stdout.strip():
        try:
            parsed = json.loads(result.stdout)
            output = parsed if isinstance(parsed, dict) else {"value": parsed}
        except json.JSONDecodeError:
            output = {"stdout": result.stdout.strip()}
    return CompatibilityResult(repository, operation, "passed", "", result.stderr.strip(), output)


def run_compatibility(config: WorkspaceConfig, *, full: bool = False, execute: bool = False) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for name, definition in config.repositories.items():
        adapters = definition.get("compatibility_adapters", {})
        command = adapters.get("portability")
        if not command:
            results.append(CompatibilityResult(name, "portability", "missing", "missing coverage", "No repository-owned adapter is declared.").__dict__)
            continue
        if not execute:
            results.append(CompatibilityResult(name, "portability", "planned", "", "Dry run; pass --execute to invoke the repository-owned adapter.", {"command": command}).__dict__)
            continue
        results.append(invoke_adapter(name, "portability", list(command), config.repository_path(name)).__dict__)
    return {
        "schema": "quantik-compatibility-report.v1",
        "mode": "full" if full else "smoke",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "status": "failed" if any(row["status"] == "failed" for row in results) else "incomplete" if any(row["status"] in {"missing", "planned"} for row in results) else "passed",
    }


def validate_report(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if value.get("schema") != "quantik-compatibility-report.v1":
        errors.append("schema must be quantik-compatibility-report.v1")
    if not isinstance(value.get("results"), list):
        errors.append("results must be an array")
    else:
        for index, row in enumerate(value["results"]):
            if not isinstance(row, dict):
                errors.append(f"results[{index}] must be an object")
            elif row.get("category") and row["category"] not in CATEGORIES:
                errors.append(f"results[{index}].category is unknown")
    return errors
