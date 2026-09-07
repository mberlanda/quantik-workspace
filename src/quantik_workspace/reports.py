"""Deterministic generated reports derived from the manifest and local checkouts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import WorkspaceConfig, dump_data, load_data
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


def task_initiatives(config: WorkspaceConfig) -> list[dict[str, Any]]:
    """Load every tracked initiative across active/completed/archived, newest facts only.

    `done` is true for anything already filed under `completed/`, or an active
    initiative whose atomic work items are all `status: completed` (a manifest
    that has not yet been moved by `task complete`).
    """
    initiatives = []
    for state in ("active", "completed", "archived"):
        root = config.root / "tasks" / state
        if not root.exists():
            continue
        for path in sorted(root.glob("*/manifest.yaml")):
            manifest = load_data(path)
            items = manifest.get("work_items", [])
            all_items_done = bool(items) and all(item.get("status") == "completed" for item in items)
            initiatives.append({
                "id": manifest["id"],
                "title": manifest.get("title", ""),
                "state": state,
                "status": manifest.get("status"),
                "complexity": manifest.get("complexity"),
                "affected_repositories": manifest.get("affected_repositories", []),
                "dependencies": manifest.get("dependencies", []),
                "done": state == "completed" or all_items_done,
            })
    return initiatives


def task_dependency_map(config: WorkspaceConfig) -> dict[str, Any]:
    """Machine-readable initiative graph: nodes carry state/complexity, edges carry gaps.

    `blocked_by` lists only dependencies that are not yet `done` — an agent can
    filter on it directly instead of re-deriving completion from `dependencies`.
    """
    initiatives = task_initiatives(config)
    done_ids = {item["id"] for item in initiatives if item["done"]}
    return {
        "schema": "quantik-task-dependency-map.v1",
        "initiatives": [
            {**item, "blocked_by": [dep for dep in item["dependencies"] if dep not in done_ids]}
            for item in initiatives
        ],
    }


def task_dependency_markdown(config: WorkspaceConfig) -> str:
    """A Mermaid flowchart plus a plain adjacency table, generated from `tasks/*/manifest.yaml`.

    The diagram is for a human glancing at rendered Markdown; the table below it
    is the same facts in a form an agent can grep without a Mermaid renderer.
    """
    graph = task_dependency_map(config)
    nodes = [item for item in graph["initiatives"] if item["state"] != "archived"]
    lines = [
        "# Task Dependency Graph", "",
        "Generated from `tasks/{active,completed,archived}/*/manifest.yaml`. Archived initiatives are omitted.",
        "", "```mermaid", "flowchart TD",
    ]
    for item in nodes:
        title = item["title"].replace('"', "'")
        lines.append(f'  {item["id"]}["{item["id"]}: {title}"]')
    for item in nodes:
        for dependency in item["dependencies"]:
            lines.append(f"  {dependency} --> {item['id']}")
    for item in nodes:
        style = "done" if item["done"] else ("blocked" if item["blocked_by"] else "ready")
        lines.append(f"  class {item['id']} {style}")
    lines.extend([
        "  classDef done fill:#d3f9d8,stroke:#2b8a3e,color:#1b1b1b",
        "  classDef blocked fill:#ffe3e3,stroke:#c92a2a,color:#1b1b1b",
        "  classDef ready fill:#e7f5ff,stroke:#1971c2,color:#1b1b1b",
        "```", "",
        "`done`: filed under `completed/`, or every active work item is `status: completed`. "
        "`blocked`: at least one `dependencies` entry is not yet done. `ready`: unblocked, dispatchable now.",
        "",
        "| ID | State | Complexity | Repos | Depends on | Blocked by | Title |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for item in nodes:
        state = "done" if item["done"] else ("blocked" if item["blocked_by"] else "ready")
        lines.append(
            f"| `{item['id']}` | {state} | {item['complexity'] or '-'} | "
            f"{', '.join(f'`{r}`' for r in item['affected_repositories']) or '-'} | "
            f"{', '.join(item['dependencies']) or '-'} | {', '.join(item['blocked_by']) or '-'} | {item['title']} |"
        )
    return "\n".join(lines) + "\n"


def dispatch_board(config: WorkspaceConfig) -> list[dict[str, Any]]:
    """Every work item in an active initiative, with whether it can be picked up right now.

    `ready` means the initiative has no unmet dependency and every work item this one
    declares in `depends_on` is `completed` — i.e. an agent can take it today.
    """
    graph = {item["id"]: item for item in task_dependency_map(config)["initiatives"]}
    rows: list[dict[str, Any]] = []
    for path in sorted((config.root / "tasks" / "active").glob("*/manifest.yaml")):
        manifest = load_data(path)
        initiative = graph.get(manifest["id"], {})
        if initiative.get("done"):
            continue
        items = {item["id"]: item for item in manifest.get("work_items", [])}
        for item in manifest.get("work_items", []):
            unmet = [dep for dep in item.get("depends_on", []) if items.get(dep, {}).get("status") != "completed"]
            rows.append({
                "initiative": manifest["id"],
                "work_item": item["id"],
                "repository": item.get("repository"),
                "branch": item.get("branch"),
                "status": item.get("status"),
                "complexity": item.get("complexity"),
                "dispatch": item.get("dispatch"),
                "depends_on": item.get("depends_on", []),
                "unmet_dependencies": unmet,
                "initiative_blocked_by": initiative.get("blocked_by", []),
                "ready": not unmet
                and not initiative.get("blocked_by")
                and item.get("status") not in {"completed", "plan-required"},
            })
    return rows


def dispatch_board_markdown(config: WorkspaceConfig) -> str:
    """The pick-up-and-go menu: one row per work item, ready ones first."""
    rows = dispatch_board(config)
    ready = [row for row in rows if row["ready"]]
    waiting = [row for row in rows if not row["ready"]]
    lines = [
        "# Dispatch Board", "",
        "Generated from `tasks/active/*/manifest.yaml`. One row per work item — the unit an agent "
        "is actually assigned. `ready` means nothing blocks it today.", "",
        "Generate a work item's execution bundle with:", "",
        "```sh",
        "quantik-workspace context task <INITIATIVE> <REPOSITORY> --work-item <ID> \\",
        "  --budget 64000 --output /tmp/<ID>.md",
        "```", "",
        f"**{len(ready)} ready now · {len(waiting)} waiting.** "
        "`dispatch` says what kind of agent an item wants: `mechanical` (every decision already "
        "made — a small model is enough), `execute-and-record` (run the specified thing, report "
        "real output), `judgment` (a real call to make — capable model, human review).", "",
        "## Ready now", "",
        "| Initiative | Item | Repository | Complexity | Dispatch | Branch |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in ready:
        lines.append(
            f"| `{row['initiative']}` | `{row['work_item']}` | `{row['repository']}` | "
            f"{row['complexity'] or '-'} | {row['dispatch'] or '-'} | `{row['branch']}` |"
        )
    lines.extend([
        "", "## Waiting", "",
        "| Initiative | Item | Repository | Complexity | Dispatch | Waiting on |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in waiting:
        blockers = ", ".join(
            [f"{row['initiative']}.{dep}" for dep in row["unmet_dependencies"]]
            + list(row["initiative_blocked_by"])
        ) or (row["status"] or "-")
        lines.append(
            f"| `{row['initiative']}` | `{row['work_item']}` | `{row['repository']}` | "
            f"{row['complexity'] or '-'} | {row['dispatch'] or '-'} | {blockers} |"
        )
    return "\n".join(lines) + "\n"


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
        generated / "task-dependency-graph.md": task_dependency_markdown(config),
        generated / "task-dependency-graph.json": dump_data(task_dependency_map(config)),
        generated / "dispatch-board.md": dispatch_board_markdown(config),
        generated / "dispatch-board.json": dump_data({"schema": "quantik-dispatch-board.v1",
                                                      "work_items": dispatch_board(config)}),
    }
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    return list(outputs)
