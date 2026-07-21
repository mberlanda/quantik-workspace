"""Central read-only validation entry points."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

from .config import WorkspaceConfig, load_data
from .contracts import contract_inventory, validate_fixtures
from .models import validate_instance
from .releases import validate_lock, validate_releases
from .reports import dependency_markdown, dependency_map
from .config import dump_data
from .tasks import validate_tasks


def validate_workspace(config: WorkspaceConfig) -> dict[str, Any]:
    errors: list[str] = []
    schema_path = config.root / "schemas" / "workspace.schema.json"
    if schema_path.is_file():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        errors.extend(validate_instance(config.data, schema))
    else:
        errors.append("schemas/workspace.schema.json is missing")
    if config.data.get("version") != 1:
        errors.append("workspace manifest version must be 1")
    repositories = config.repositories
    if not repositories:
        errors.append("workspace must define repositories")
    for name, definition in repositories.items():
        if not isinstance(definition, dict):
            errors.append(f"repositories.{name} must be an object")
            continue
        for field in ("url", "path", "role", "default_branch", "versions"):
            if field not in definition:
                errors.append(f"repositories.{name}.{field} is required")
        source = definition.get("versions", {}).get("repository_source")
        if source and "path" not in source:
            errors.append(f"repositories.{name}.versions.repository_source.path is required")
    names = set(repositories)
    allowed_types = {"build", "runtime", "contract", "fixture", "schema", "generated-data", "semantic-compatibility", "github-action", "release-order"}
    for index, edge in enumerate(config.data.get("dependencies", [])):
        if edge.get("from") not in names or edge.get("to") not in names:
            errors.append(f"dependencies[{index}] references an unknown repository")
        unknown = set(edge.get("types", [])) - allowed_types
        if unknown:
            errors.append(f"dependencies[{index}] has unknown types: {sorted(unknown)}")
    return {"status": "ok" if not errors else "failed", "errors": errors}


def validate_locks(config: WorkspaceConfig) -> dict[str, Any]:
    errors: list[str] = []
    checked = 0
    root = config.root / "releases" / "locks"
    if root.exists():
        for path in sorted(root.glob("*.yaml")):
            checked += 1
            errors.extend(f"{path}: {error}" for error in validate_lock(config, path))
    return {"status": "ok" if not errors else "failed", "checked": checked, "errors": errors}


def validate_generated(config: WorkspaceConfig) -> dict[str, Any]:
    expected = {
        config.root / "docs/generated/dependency-graph.md": dependency_markdown(config),
        config.root / "docs/generated/dependency-graph.json": dump_data(dependency_map(config)),
    }
    errors = [f"{path}: generated file is missing or stale" for path, content in expected.items() if not path.is_file() or path.read_text(encoding="utf-8") != content]
    summary = config.root / "docs/generated/repository-summary.md"
    if not summary.is_file():
        errors.append(f"{summary}: generated snapshot is missing")
    matrix = config.root / "docs/generated/compatibility-matrix.json"
    if not matrix.is_file():
        errors.append(f"{matrix}: generated compatibility matrix is missing")
    else:
        matrix_errors = validate_instance(json.loads(matrix.read_text(encoding="utf-8")), json.loads((config.root / "schemas/compatibility-matrix.schema.json").read_text(encoding="utf-8")))
        errors.extend(f"{matrix}: {error}" for error in matrix_errors)
    return {"status": "ok" if not errors else "failed", "checked": len(expected) + 2, "errors": errors}


def validate_document_links(config: WorkspaceConfig) -> dict[str, Any]:
    errors: list[str] = []
    checked = 0
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for document in config.root.rglob("*.md"):
        if any(part in {".git", ".venv", "build", "dist"} for part in document.parts):
            continue
        for number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
            for match in link_re.finditer(line):
                target = match.group(1).split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                checked += 1
                if not (document.parent / target).resolve().exists():
                    errors.append(f"{document.relative_to(config.root)}:{number}: broken link {target}")
    return {"status": "ok" if not errors else "failed", "checked": checked, "errors": errors}


def validate_all(config: WorkspaceConfig) -> dict[str, Any]:
    results = {
        "workspace": validate_workspace(config),
        "contracts": contract_inventory(config),
        "fixtures": validate_fixtures(config),
        "tasks": validate_tasks(config),
        "releases": validate_releases(config),
        "locks": validate_locks(config),
        "generated": validate_generated(config),
        "docs": validate_document_links(config),
    }
    failed = [name for name, result in results.items() if result.get("status") in {"failed", "missing"}]
    return {"status": "failed" if failed else "ok", "failed": failed, "results": results}
