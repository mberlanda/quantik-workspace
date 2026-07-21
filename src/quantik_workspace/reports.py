"""Deterministic generated reports derived from the manifest and local checkouts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import WorkspaceConfig, dump_data
from .repositories import all_status


def dependency_map(config: WorkspaceConfig) -> dict[str, Any]:
    return {"schema": "quantik-dependency-map.v1", "repositories": list(config.repositories), "dependencies": config.data.get("dependencies", [])}


def dependency_order(config: WorkspaceConfig, repositories: set[str] | None = None) -> list[str]:
    """Topologically order providers before consumers for release-order edges."""
    nodes = set(repositories or config.repositories)
    incoming = {node: 0 for node in nodes}
    outgoing = {node: set() for node in nodes}
    for edge in config.data.get("dependencies", []):
        consumer, provider = edge.get("from"), edge.get("to")
        if "release-order" not in edge.get("types", []) or consumer not in nodes or provider not in nodes:
            continue
        if consumer not in outgoing[provider]:
            outgoing[provider].add(consumer)
            incoming[consumer] += 1
    ready = sorted(node for node, count in incoming.items() if count == 0)
    ordered: list[str] = []
    while ready:
        node = ready.pop(0)
        ordered.append(node)
        for consumer in sorted(outgoing[node]):
            incoming[consumer] -= 1
            if incoming[consumer] == 0:
                ready.append(consumer)
                ready.sort()
    if len(ordered) != len(nodes):
        cycle = sorted(node for node, count in incoming.items() if count)
        raise ValueError(f"release-order dependency cycle: {', '.join(cycle)}")
    return ordered


def dependency_markdown(config: WorkspaceConfig) -> str:
    lines = ["# Dependency Graph", "", "Generated from `workspace.yaml`.", "", "| Consumer | Provider | Dependency types |", "| --- | --- | --- |"]
    for item in config.data.get("dependencies", []):
        lines.append(f"| `{item['from']}` | `{item['to']}` | {', '.join(item['types'])} |")
    lines.extend(["", "Release-order edges point from consumer to the provider that must be available first.", ""])
    return "\n".join(lines)


def repository_summary_markdown(config: WorkspaceConfig) -> str:
    lines = ["# Repository Summary", "", "| Repository | Branch | Commit | Dirty | Version | Contracts |", "| --- | --- | --- | --- | --- | --- |"]
    for row in all_status(config):
        lines.append(f"| `{row['name']}` | `{row.get('branch')}` | `{str(row.get('commit') or '')[:12]}` | {row.get('dirty')} | `{row.get('repository_version')}` | `{row.get('supported_contracts_release')}` |")
    return "\n".join(lines) + "\n"


def write_generated(config: WorkspaceConfig) -> list[Path]:
    generated = config.root / "docs" / "generated"
    generated.mkdir(parents=True, exist_ok=True)
    outputs = {
        generated / "repository-summary.md": repository_summary_markdown(config),
        generated / "dependency-graph.md": dependency_markdown(config),
        generated / "dependency-graph.json": dump_data(dependency_map(config)),
    }
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    return list(outputs)
