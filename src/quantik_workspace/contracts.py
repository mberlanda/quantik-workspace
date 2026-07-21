"""Contract and fixture validation without reimplementing Quantik behavior."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import WorkspaceConfig
from .versions import read_version_source


def validate_jsonl(path: Path, *, expected_release: str | None = None) -> list[str]:
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [f"{path}: {exc}"]
    if not lines:
        return [f"{path}: empty fixture"]
    for number, line in enumerate(lines, 1):
        if not line.strip():
            errors.append(f"{path}:{number}: blank JSONL row")
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{number}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(row, dict):
            errors.append(f"{path}:{number}: row must be an object")
            continue
        if not isinstance(row.get("schema"), str):
            errors.append(f"{path}:{number}: missing string schema")
        release = row.get("contract_version")
        if expected_release and release is not None and release != expected_release:
            errors.append(f"{path}:{number}: contract_version {release!r} != {expected_release!r}")
    return errors


def validate_fixtures(config: WorkspaceConfig) -> dict[str, Any]:
    definition = config.repositories["quantik-core-contracts"]
    root = config.repository_path("quantik-core-contracts")
    expected = read_version_source(root, definition["versions"]["repository_source"])
    files = sorted((root / "fixtures").rglob("*.jsonl")) if (root / "fixtures").exists() else []
    errors: list[str] = []
    for path in files:
        errors.extend(validate_jsonl(path, expected_release=expected))
    return {"status": "ok" if not errors else "failed", "expected_release": expected, "files": len(files), "errors": errors}


def contract_inventory(config: WorkspaceConfig) -> dict[str, Any]:
    root = config.repository_path("quantik-core-contracts")
    manifest = root / "contracts.json"
    if not manifest.is_file():
        return {"status": "missing", "path": str(manifest), "contracts": {}}
    value = json.loads(manifest.read_text(encoding="utf-8"))
    return {"status": "ok", "path": str(manifest), "release": value.get("release_version"), "contracts": value.get("contracts", {})}

