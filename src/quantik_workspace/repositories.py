"""Repository inventory, status, and explicitly authorized local setup operations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import WorkspaceConfig
from .git import inspect
from .subprocesses import run
from .versions import read_version_source, scan_action_references


def list_repositories(config: WorkspaceConfig) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, definition in config.repositories.items():
        rows.append(
            {
                "name": name,
                "path": str(config.repository_path(name)),
                "url": definition.get("url"),
                "language": definition.get("language"),
                "role": definition.get("role"),
            }
        )
    return rows


def _active_for(config: WorkspaceConfig, name: str, directory: str) -> list[str]:
    result: list[str] = []
    root = config.root / directory / "active"
    if not root.exists():
        return result
    for path in root.iterdir():
        if not path.is_dir():
            continue
        text = "\n".join(
            file.read_text(encoding="utf-8", errors="ignore")
            for pattern in ("*.md", "*.yaml")
            for file in path.rglob(pattern)
        )
        if name in text:
            result.append(path.name)
    return sorted(result)


def repository_status(config: WorkspaceConfig, name: str) -> dict[str, Any]:
    definition = config.repositories[name]
    path = config.repository_path(name)
    status = inspect(path).to_dict()
    versions = definition.get("versions", {})
    status.update(
        {
            "name": name,
            "repository_version": read_version_source(path, versions.get("repository_source")),
            "supported_contracts_release": read_version_source(path, versions.get("supported_contracts_source")),
            "action_references": scan_action_references(path) if path.exists() else [],
            "active_initiatives": _active_for(config, name, "tasks"),
            "active_releases": _active_for(config, name, "releases"),
        }
    )
    return status


def all_status(config: WorkspaceConfig) -> list[dict[str, Any]]:
    return [repository_status(config, name) for name in config.repositories]


def clone_missing(config: WorkspaceConfig, *, execute: bool = False) -> list[str]:
    actions: list[str] = []
    for name, definition in config.repositories.items():
        path = config.repository_path(name)
        if path.exists():
            continue
        command = ["git", "clone", str(definition["url"]), str(path)]
        actions.append(" ".join(command))
        if execute:
            path.parent.mkdir(parents=True, exist_ok=True)
            run(command, path.parent)
    return actions


def update_repositories(config: WorkspaceConfig, *, execute: bool = False) -> list[str]:
    actions: list[str] = []
    for name in config.repositories:
        path = config.repository_path(name)
        status = inspect(path)
        if not status.is_git:
            continue
        command = ["git", "fetch", "--prune", "--tags"]
        actions.append(f"{name}: {' '.join(command)}")
        if execute:
            run(command, path)
    return actions
