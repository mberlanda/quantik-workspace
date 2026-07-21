"""Manifest loading with deterministic JSON/YAML handling and local overrides."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
from typing import Any


class ConfigurationError(ValueError):
    pass


def _scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith(("[", "{")):
        return json.loads(value)
    if value.startswith(("\"", "'")):
        if value[0] == "\"":
            return json.loads(value)
        return value[1:-1].replace("''", "'")
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def _yaml_lines(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise ConfigurationError(f"tabs are not allowed in YAML indentation (line {number})")
        content = raw.strip()
        result.append((len(raw) - len(raw.lstrip()), content))
    return result


def _parse_yaml_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    is_list = lines[index][1].startswith("- ") or lines[index][1] == "-"
    container: Any = [] if is_list else {}
    while index < len(lines):
        current_indent, content = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ConfigurationError(f"unexpected indentation near: {content}")
        if is_list:
            if not content.startswith("-"):
                break
            rest = content[1:].strip()
            if not rest:
                value, index = _parse_yaml_block(lines, index + 1, lines[index + 1][0])
                container.append(value)
                continue
            if ":" in rest and not rest.startswith(("\"", "'")):
                key, raw_value = rest.split(":", 1)
                item: dict[str, Any] = {key.strip(): _scalar(raw_value)}
                index += 1
                if index < len(lines) and lines[index][0] > indent:
                    extra, index = _parse_yaml_block(lines, index, lines[index][0])
                    if isinstance(extra, dict):
                        item.update(extra)
                    else:
                        raise ConfigurationError("list mapping continuation must be a mapping")
                container.append(item)
                continue
            container.append(_scalar(rest))
            index += 1
            continue
        if ":" not in content:
            raise ConfigurationError(f"expected key: value, got: {content}")
        key, raw_value = content.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        index += 1
        if raw_value:
            container[key] = _scalar(raw_value)
        elif index < len(lines) and lines[index][0] > indent:
            container[key], index = _parse_yaml_block(lines, index, lines[index][0])
        else:
            container[key] = {}
    return container, index


def load_data(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigurationError(f"cannot read {path}: {exc}") from exc
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        lines = _yaml_lines(text)
        value, consumed = _parse_yaml_block(lines, 0, lines[0][0] if lines else 0)
        if consumed != len(lines):
            raise ConfigurationError(f"could not parse all of {path}")
    if not isinstance(value, dict):
        raise ConfigurationError(f"{path} must contain a mapping")
    return value


def dump_data(value: Any) -> str:
    """Return deterministic JSON, which is also valid YAML 1.2."""
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def find_manifest(start: Path | None = None) -> Path:
    explicit = os.environ.get("QUANTIK_WORKSPACE_FILE")
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.is_file():
            raise ConfigurationError(f"QUANTIK_WORKSPACE_FILE does not exist: {path}")
        return path
    current = (start or Path.cwd()).resolve()
    for candidate_root in (current, *current.parents):
        candidate = candidate_root / "workspace.yaml"
        if candidate.is_file():
            return candidate
    raise ConfigurationError("workspace.yaml not found in this directory or its parents")


@dataclass(frozen=True)
class WorkspaceConfig:
    manifest_path: Path
    data: dict[str, Any]

    @property
    def root(self) -> Path:
        return self.manifest_path.parent

    @property
    def repositories(self) -> dict[str, dict[str, Any]]:
        value = self.data.get("repositories", {})
        return value if isinstance(value, dict) else {}

    def repository_path(self, name: str) -> Path:
        try:
            raw = self.repositories[name]["path"]
        except KeyError as exc:
            raise ConfigurationError(f"unknown or pathless repository: {name}") from exc
        path = Path(str(raw)).expanduser()
        return path.resolve() if path.is_absolute() else (self.root / path).resolve()


def load_workspace(path: Path | None = None) -> WorkspaceConfig:
    manifest = (path or find_manifest()).resolve()
    data = load_data(manifest)
    local = manifest.with_name("workspace.local.yaml")
    if local.is_file():
        data = _merge(data, load_data(local))
    return WorkspaceConfig(manifest, data)

