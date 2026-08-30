"""Bounded, layered context assembly."""

from __future__ import annotations

from dataclasses import dataclass
import math
import os
from pathlib import Path
from typing import Iterable

from .config import WorkspaceConfig
from .repositories import repository_status
from .versions import read_version_source


class ContextBudgetExceeded(ValueError):
    pass


@dataclass(frozen=True)
class ContextBundle:
    text: str
    sources: tuple[str, ...]
    excluded: tuple[str, ...]
    approximate_tokens: int


def _read_sources(root: Path, paths: Iterable[Path]) -> tuple[list[str], list[str]]:
    sections: list[str] = []
    included: list[str] = []
    for path in paths:
        if not path.is_file():
            continue
        included.append(str(path.relative_to(root)))
        sections.append(f"\n---\n\nSource: `{path.relative_to(root)}`\n\n{path.read_text(encoding='utf-8').strip()}\n")
    return sections, included


def _finish(header: str, sections: list[str], sources: list[str], excluded: list[str], budget: int) -> ContextBundle:
    preamble = (
        f"# Quantik Workspace Context\n\n{header}\n\n"
        f"Included sources: {', '.join(sources) if sources else 'none'}\n\n"
        f"Excluded by design: {', '.join(excluded)}\n"
    )
    text = preamble + "".join(sections)
    estimate = math.ceil(len(text) / 4)
    if estimate > budget:
        raise ContextBudgetExceeded(f"context estimate {estimate} tokens exceeds budget {budget}; increase --budget or narrow the request")
    return ContextBundle(text, tuple(sources), tuple(excluded), estimate)


def budget_for(config: WorkspaceConfig, override: int | None = None) -> int:
    if override is not None:
        return override
    environment = os.environ.get("QUANTIK_CONTEXT_BUDGET_TOKENS")
    return int(environment or config.data.get("workspace", {}).get("context_budget_tokens", 12000))


def repository_context(config: WorkspaceConfig, name: str, budget: int | None = None) -> ContextBundle:
    if name not in config.repositories:
        raise ValueError(f"unknown repository: {name}")
    status = repository_status(config, name)
    definition = config.repositories[name]
    dynamic = (
        f"Purpose: repository packet for `{name}`.\n\nRevision: `{status.get('commit')}` on `{status.get('branch')}`; "
        f"dirty={status.get('dirty')}. Repository version: `{status.get('repository_version')}`. "
        f"Supported contracts release: `{status.get('supported_contracts_release')}`.\n\n"
        f"Commands: `{definition.get('commands', {})}`\n"
    )
    paths = [
        config.root / "context/system/repository-map.md",
        config.root / "context/system/canonical-invariants.md",
        config.root / f"context/repositories/{name}.md",
    ]
    sections, sources = _read_sources(config.root, paths)
    return _finish(dynamic, sections, sources, ["implementation source trees", "unrelated repository packets", "historical task archives"], budget_for(config, budget))


def initiative_context(config: WorkspaceConfig, identifier: str, repository: str | None = None, budget: int | None = None) -> ContextBundle:
    matches = list((config.root / "tasks" / "active").glob(f"{identifier}*"))
    if len(matches) != 1:
        raise ValueError(f"expected one active initiative for {identifier}, found {len(matches)}")
    initiative = matches[0]
    paths = [config.root / "context/system/canonical-invariants.md", initiative / "initiative.md", initiative / "plan.md", initiative / "manifest.yaml", initiative / "decisions.md", initiative / "status.md"]
    if repository:
        paths.extend([config.root / f"context/repositories/{repository}.md", initiative / "repos" / f"{repository}.md"])
    sections, sources = _read_sources(config.root, paths)
    revisions = []
    for name in ([repository] if repository else []):
        status = repository_status(config, name)
        revisions.append(f"{name}={status.get('commit')} dirty={status.get('dirty')}")
    header = f"Purpose: {'repository task' if repository else 'initiative'} context for `{identifier}`. Revisions: {', '.join(revisions) or 'recorded in repository packets'}."
    return _finish(header, sections, sources, ["unaffected repositories", "completed/archived initiatives", "full source trees"], budget_for(config, budget))


def release_context(config: WorkspaceConfig, identifier: str, budget: int | None = None) -> ContextBundle:
    matches = list((config.root / "releases" / "active").glob(f"{identifier}*"))
    if len(matches) != 1:
        raise ValueError(f"expected one active release for {identifier}, found {len(matches)}")
    release = matches[0]
    paths = [config.root / "context/system/release-model.md", release / "release.yaml", release / "checklist.md", release / "status.md"]
    paths.extend(sorted((release / "consumers").glob("*.md")) if (release / "consumers").exists() else [])
    sections, sources = _read_sources(config.root, paths)
    return _finish(f"Purpose: release context for `{identifier}`.", sections, sources, ["implementation source trees", "unrelated initiatives", "other release trains"], budget_for(config, budget))

