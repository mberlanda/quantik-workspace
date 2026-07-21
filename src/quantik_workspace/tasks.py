"""Repository-scoped initiative task packets."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import shutil
from typing import Any

from .config import WorkspaceConfig, dump_data, load_data


TASK_ID_RE = re.compile(r"^QW-\d{3}(?:-[a-z0-9-]+)?$")


def validate_initiative(path: Path, repositories: set[str]) -> list[str]:
    errors: list[str] = []
    manifest = path / "manifest.yaml"
    if not manifest.is_file():
        return [f"{path}: missing manifest.yaml"]
    try:
        value = load_data(manifest)
    except ValueError as exc:
        return [str(exc)]
    identifier = value.get("id")
    if not isinstance(identifier, str) or not TASK_ID_RE.fullmatch(identifier):
        errors.append(f"{manifest}: invalid id")
    required = ["title", "status", "problem", "affected_repositories", "acceptance_criteria"]
    for field in required:
        if not value.get(field):
            errors.append(f"{manifest}: missing {field}")
    affected = value.get("affected_repositories", [])
    if not isinstance(affected, list):
        errors.append(f"{manifest}: affected_repositories must be a list")
    else:
        unknown = sorted(set(affected) - repositories)
        if unknown:
            errors.append(f"{manifest}: unknown repositories: {', '.join(unknown)}")
        for repository in affected:
            if not (path / "repos" / f"{repository}.md").is_file():
                errors.append(f"{path}: missing repos/{repository}.md")
    for document in ("initiative.md", "decisions.md", "status.md"):
        if not (path / document).is_file():
            errors.append(f"{path}: missing {document}")
    return errors


def validate_tasks(config: WorkspaceConfig) -> dict[str, Any]:
    errors: list[str] = []
    checked = 0
    for state in ("active", "completed", "archived"):
        root = config.root / "tasks" / state
        if not root.exists():
            continue
        for path in sorted(item for item in root.iterdir() if item.is_dir()):
            checked += 1
            errors.extend(validate_initiative(path, set(config.repositories)))
    return {"status": "ok" if not errors else "failed", "checked": checked, "errors": errors}


def create_task(config: WorkspaceConfig, identifier: str, title: str, repositories: list[str]) -> Path:
    if not TASK_ID_RE.fullmatch(identifier):
        raise ValueError("task id must match QW-NNN with an optional slug")
    unknown = sorted(set(repositories) - set(config.repositories))
    if unknown:
        raise ValueError(f"unknown repositories: {', '.join(unknown)}")
    path = config.root / "tasks" / "active" / identifier
    if path.exists():
        raise FileExistsError(path)
    (path / "repos").mkdir(parents=True)
    (path / "handoffs").mkdir()
    (path / "reports").mkdir()
    manifest = {
        "id": identifier.split("-", 2)[0] + "-" + identifier.split("-", 2)[1],
        "title": title,
        "status": "planned",
        "created": date.today().isoformat(),
        "problem": "To be refined.",
        "affected_repositories": repositories,
        "affected_contracts": [],
        "acceptance_criteria": ["Repository-scoped completion evidence is recorded."],
    }
    (path / "manifest.yaml").write_text(dump_data(manifest), encoding="utf-8")
    (path / "initiative.md").write_text(f"# {identifier}: {title}\n\nSee `manifest.yaml`.\n", encoding="utf-8")
    (path / "decisions.md").write_text("# Decisions\n\nNo decisions recorded.\n", encoding="utf-8")
    (path / "status.md").write_text("# Status\n\nPlanned.\n", encoding="utf-8")
    for repository in repositories:
        (path / "repos" / f"{repository}.md").write_text(
            f"# {repository}\n\n## Objective\n\nTo be refined.\n\n## Completion criteria\n\n- Focused tests pass.\n- Handoff records exact commit and evidence.\n",
            encoding="utf-8",
        )
    return path


def complete_task(config: WorkspaceConfig, identifier: str) -> Path:
    matches = list((config.root / "tasks" / "active").glob(f"{identifier}*"))
    if len(matches) != 1:
        raise ValueError(f"expected one active initiative for {identifier}, found {len(matches)}")
    errors = validate_initiative(matches[0], set(config.repositories))
    if errors:
        raise ValueError("cannot complete invalid task: " + "; ".join(errors))
    target = config.root / "tasks" / "completed" / matches[0].name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(matches[0]), target)
    return target

