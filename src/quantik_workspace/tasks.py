"""Initiatives and atomic, repository-owned work packets."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re
import shutil
from typing import Any

from .config import WorkspaceConfig, dump_data, load_data


TASK_ID_RE = re.compile(r"^QW-\d{3}(?:-[a-z0-9-]+)?$")


def scoped_file(root: Path, relative: str) -> Path:
    """Resolve a required input without allowing traversal or symlink escape."""
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError(f"invalid relative path: {relative!r}")
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"missing or out-of-scope input: {relative}")
    return path


def read_reference(root: Path, reference: str) -> str:
    """Read an explicit Markdown heading, never the surrounding document."""
    if not isinstance(reference, str) or "#" not in reference:
        raise ValueError(f"reference must be file#heading: {reference!r}")
    filename, heading = reference.split("#", 1)
    lines = scoped_file(root, filename).read_text(encoding="utf-8").splitlines()
    matches = [i for i, line in enumerate(lines) if re.fullmatch(r"#{1,6} " + re.escape(heading), line)]
    if len(matches) != 1:
        raise ValueError(f"expected one heading for {reference}")
    start = matches[0]
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"#{1," + str(level) + r"} ", lines[i])), len(lines))
    return "\n".join(lines[start:end]).strip()


def validate_work_items(path: Path, value: dict, repositories: set[str]) -> list[str]:
    errors: list[str] = []
    items = value.get("work_items", [])
    if not isinstance(items, list) or not items:
        return [f"{path}: work_items must be a non-empty list"]
    ids, packets, branches = set(), set(), set()
    for item in items:
        try:
            if not isinstance(item, dict):
                raise ValueError("work item must be an object")
            identifier, repo = item.get("id"), item.get("repository")
            if not isinstance(identifier, str) or not re.fullmatch(r"[A-Z][A-Z0-9_-]*", identifier) or identifier in ids:
                raise ValueError(f"invalid or duplicate work item id: {identifier}")
            ids.add(identifier)
            if repo not in repositories or repo not in value.get("affected_repositories", []):
                raise ValueError(f"unknown or unaffected repository: {repo}")
            packet = item.get("packet", "")
            scoped_file(path, packet)
            if not packet.startswith(f"repos/{repo}/") or not packet.endswith(".md") or packet in packets:
                raise ValueError(f"invalid or duplicate packet: {packet}")
            packets.add(packet)
            branch = item.get("branch")
            if not isinstance(branch, str) or not branch.strip() or (repo, branch) in branches:
                raise ValueError(f"missing or duplicate branch for {identifier}")
            branches.add((repo, branch))
            allowed = item.get("allowed_paths")
            if not isinstance(allowed, list) or not allowed or any(not isinstance(x, str) or not x or Path(x).is_absolute() or ".." in Path(x).parts for x in allowed):
                raise ValueError(f"invalid allowed_paths for {identifier}")
            for field in ("decisions", "invariants", "depends_on"):
                refs = item.get(field, [])
                if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
                    raise ValueError(f"{field} must be a list of strings")
            for ref in item.get("decisions", []):
                if ref.split("#", 1)[0] != "decisions.md":
                    raise ValueError("decisions must reference decisions.md headings")
                read_reference(path, ref)
        except (ValueError, TypeError) as exc:
            errors.append(f"{path}: {exc}")
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("depends_on", []), list):
            for dependency in item.get("depends_on", []):
                if not isinstance(dependency, str) or dependency not in ids or dependency == item.get("id"):
                    errors.append(f"{path}: invalid dependency: {dependency}")
    if not errors:
        pending = {item["id"]: set(item.get("depends_on", [])) for item in items}
        while pending:
            ready = {identifier for identifier, dependencies in pending.items() if not dependencies}
            if not ready:
                errors.append(f"{path}: cyclic work-item dependencies")
                break
            pending = {identifier: dependencies - ready for identifier, dependencies in pending.items() if identifier not in ready}
    return errors


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
    if not isinstance(affected, list) or any(not isinstance(repo, str) for repo in affected):
        errors.append(f"{manifest}: affected_repositories must be a list of strings")
    else:
        unknown = sorted(set(affected) - repositories)
        if unknown:
            errors.append(f"{manifest}: unknown repositories: {', '.join(unknown)}")
        for repository in affected:
            if "work_items" not in value and not (path / "repos" / f"{repository}.md").is_file():
                errors.append(f"{path}: missing repos/{repository}.md")
    if "work_items" in value:
        errors.extend(validate_work_items(path, value, repositories))
        items = value.get("work_items")
        assigned = {item.get("repository") for item in items if isinstance(item, dict) and isinstance(item.get("repository"), str)} if isinstance(items, list) else set()
        for repository in affected if isinstance(affected, list) else []:
            if isinstance(repository, str) and repository not in assigned:
                errors.append(f"{path}: missing work item for {repository}")
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
            initiative_errors = validate_initiative(path, set(config.repositories))
            errors.extend(initiative_errors)
            if initiative_errors:
                continue
            try:
                manifest = load_data(path / "manifest.yaml")
                for item in manifest.get("work_items", []):
                    for ref in item.get("invariants", []):
                        if ref.split("#", 1)[0] != "context/system/canonical-invariants.md":
                            raise ValueError("invariants must reference canonical-invariants.md headings")
                        read_reference(config.root, ref)
            except (ValueError, TypeError, AttributeError) as exc:
                errors.append(f"{path}: {exc}")
    return {"status": "ok" if not errors else "failed", "checked": checked, "errors": errors}


def task_status(config: WorkspaceConfig) -> dict[str, Any]:
    """Expose tracked work-item state without inferring completion from Git."""
    result = validate_tasks(config)
    initiatives = []
    if result["errors"]:
        return result
    for path in sorted((config.root / "tasks" / "active").glob("*/manifest.yaml")):
        manifest = load_data(path)
        initiatives.append({
            "id": manifest["id"], "title": manifest["title"], "status": manifest["status"],
            "work_items": [{key: item.get(key, [] if key == "depends_on" else None)
                            for key in ("id", "repository", "status", "branch", "packet", "depends_on")}
                           for item in manifest.get("work_items", [])],
        })
    result["initiatives"] = initiatives
    return result


def create_task(config: WorkspaceConfig, identifier: str, title: str, repositories: list[str]) -> Path:
    if not TASK_ID_RE.fullmatch(identifier):
        raise ValueError("task id must match QW-NNN with an optional slug")
    if not repositories or len(repositories) != len(set(repositories)):
        raise ValueError("repositories must be non-empty and unique")
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
    manifest["work_items"] = [
        {"id": f"W{index}", "repository": repository,
         "packet": f"repos/{repository}/W{index}-implementation.md",
         "branch": f"feat/{manifest['id'].lower()}-w{index}", "status": "plan-required",
         "allowed_paths": ["REPLACE_WITH_EXPLICIT_PATHS"], "decisions": [], "invariants": [], "depends_on": []}
        for index, repository in enumerate(repositories, 1)
    ]
    manifest["status"] = "plan-required"
    (path / "manifest.yaml").write_text(dump_data(manifest), encoding="utf-8")
    (path / "initiative.md").write_text(f"# {identifier}: {title}\n\nSee `manifest.yaml`.\n", encoding="utf-8")
    (path / "decisions.md").write_text("# Decisions\n\nNo decisions recorded.\n", encoding="utf-8")
    (path / "status.md").write_text("# Status\n\nPlan required: refine work-item paths, references, and completion criteria before dispatch.\n", encoding="utf-8")
    for item in manifest["work_items"]:
        repository = item["repository"]
        (path / "repos" / repository).mkdir()
        (path / item["packet"]).write_text(
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

