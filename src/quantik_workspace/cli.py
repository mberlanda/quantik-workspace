"""`quantik-workspace` command-line interface."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import sys
from typing import Any, Callable

from .benchmarks import benchmark_compare, benchmark_run
from .compatibility import run_compatibility, validate_report
from .config import ConfigurationError, dump_data, load_workspace
from .context import initiative_context, release_context, repository_context
from .contracts import contract_inventory, validate_fixtures
from .releases import (
    complete_release,
    create_consumer_tasks,
    drift,
    plan_release,
    prepare_release,
    publish_release,
    release_status,
    tag_release,
    validate_candidate,
    validate_releases,
    verify_published,
)
from .repositories import all_status, clone_missing, list_repositories, update_repositories
from .reports import write_generated
from .tasks import complete_task, create_task, validate_tasks
from .validation import validate_all, validate_document_links, validate_generated, validate_locks, validate_workspace


LOG = logging.getLogger("quantik_workspace")


def _json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def _human_status(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        print(row["name"])
        print(f"  path: {row['path']}")
        print(f"  branch/commit: {row.get('branch') or '-'} / {row.get('commit') or '-'}")
        print(f"  upstream: {row.get('upstream') or '-'}; ahead={row.get('ahead')}; behind={row.get('behind')}")
        print(f"  dirty: {row.get('dirty')} (untracked: {row.get('untracked')})")
        print(f"  repository version: {row.get('repository_version') or '-'}")
        print(f"  supported contracts: {row.get('supported_contracts_release') or '-'}")
        action_refs = [item for item in row.get("action_references", []) if "action" in item]
        for item in action_refs:
            print(f"  action: {item['action']}@{item['ref']} ({item['path']}:{item['line']})")
        print(f"  initiatives: {', '.join(row.get('active_initiatives', [])) or '-'}")
        print(f"  releases: {', '.join(row.get('active_releases', [])) or '-'}")


def _validation(value: dict[str, Any]) -> int:
    _json(value)
    return 0 if value.get("status") not in {"failed", "missing"} else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="quantik-workspace", description="Quantik multi-repository control plane")
    parser.add_argument("--workspace", type=Path, help="Path to workspace.yaml")
    parser.add_argument("--verbose", action="store_true")
    commands = parser.add_subparsers(dest="command", required=True)

    repos = commands.add_parser("repos", help="Inspect or explicitly set up repositories").add_subparsers(dest="repos_command", required=True)
    repos.add_parser("list")
    repos_status = repos.add_parser("status")
    repos_status.add_argument("--json", action="store_true")
    for name in ("clone", "update"):
        item = repos.add_parser(name)
        item.add_argument("--execute", action="store_true", help="Perform the mutation; otherwise print a dry run")

    tasks = commands.add_parser("task", help="Manage initiative task packets").add_subparsers(dest="task_command", required=True)
    create = tasks.add_parser("create")
    create.add_argument("id")
    create.add_argument("--title", required=True)
    create.add_argument("--repository", action="append", required=True)
    tasks.add_parser("validate")
    tasks.add_parser("status")
    complete = tasks.add_parser("complete")
    complete.add_argument("id")

    context = commands.add_parser("context", help="Generate bounded agent context").add_subparsers(dest="context_command", required=True)
    for name in ("repo", "initiative", "release"):
        item = context.add_parser(name)
        item.add_argument("identifier")
        item.add_argument("--budget", type=int)
        item.add_argument("--output", type=Path)
    task_context = context.add_parser("task")
    task_context.add_argument("initiative")
    task_context.add_argument("repository")
    task_context.add_argument("--budget", type=int)
    task_context.add_argument("--output", type=Path)

    validate = commands.add_parser("validate", help="Read-only validation").add_subparsers(dest="validate_command", required=True)
    for name in ("workspace", "contracts", "fixtures", "tasks", "releases", "locks", "generated", "docs", "all"):
        validate.add_parser(name)

    compatibility = commands.add_parser("compatibility", help="Coordinate repository-owned adapters").add_subparsers(dest="compatibility_command", required=True)
    for name in ("smoke", "full"):
        item = compatibility.add_parser(name)
        item.add_argument("--execute", action="store_true")
        item.add_argument("--output", type=Path)
    report = compatibility.add_parser("report")
    report.add_argument("path", type=Path)

    benchmark = commands.add_parser("benchmark", help="Coordinate repository-owned benchmarks").add_subparsers(dest="benchmark_command", required=True)
    run_bench = benchmark.add_parser("run")
    run_bench.add_argument("repository")
    run_bench.add_argument("--execute", action="store_true")
    compare = benchmark.add_parser("compare")
    compare.add_argument("left", type=Path)
    compare.add_argument("right", type=Path)

    releases = commands.add_parser("release", help="Plan and guard releases").add_subparsers(dest="release_command", required=True)
    for name in ("plan", "prepare"):
        item = releases.add_parser(name)
        item.add_argument("--repository", required=True)
        item.add_argument("--version", required=True)
        item.add_argument("--id", required=True)
        if name == "prepare":
            group = item.add_mutually_exclusive_group()
            group.add_argument("--dry-run", action="store_true", default=True)
            group.add_argument("--write-plan", action="store_true", help="Write only workspace release metadata; never edit siblings")
    for name in ("validate-candidate", "verify-published", "create-consumer-tasks", "complete"):
        item = releases.add_parser(name)
        item.add_argument("id")
        if name == "verify-published":
            item.add_argument("--network", action="store_true")
            item.add_argument("--write-lock", action="store_true")
    for name in ("tag", "publish"):
        item = releases.add_parser(name)
        item.add_argument("id")
        item.add_argument("--execute", action="store_true")
    release_status_parser = releases.add_parser("status")
    release_status_parser.add_argument("id", nargs="?")
    drift_parser = releases.add_parser("drift")
    drift_parser.add_argument("--json", action="store_true")

    reports = commands.add_parser("reports", help="Generate deterministic derived reports").add_subparsers(dest="reports_command", required=True)
    reports.add_parser("generate")
    return parser


def _write_or_print(text: str, output: Path | None) -> None:
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        print(output)
    else:
        print(text, end="" if text.endswith("\n") else "\n")


def dispatch(args: argparse.Namespace) -> int:
    config = load_workspace(args.workspace)
    if args.command == "repos":
        if args.repos_command == "list":
            _json(list_repositories(config)); return 0
        if args.repos_command == "status":
            rows = all_status(config)
            _json(rows) if args.json else _human_status(rows)
            return 0
        actions = clone_missing(config, execute=args.execute) if args.repos_command == "clone" else update_repositories(config, execute=args.execute)
        _json({"execute": args.execute, "actions": actions}); return 0
    if args.command == "task":
        if args.task_command == "create":
            print(create_task(config, args.id, args.title, args.repository)); return 0
        if args.task_command == "validate":
            return _validation(validate_tasks(config))
        if args.task_command == "status":
            return _validation(validate_tasks(config))
        print(complete_task(config, args.id)); return 0
    if args.command == "context":
        if args.context_command == "repo":
            bundle = repository_context(config, args.identifier, args.budget)
        elif args.context_command == "initiative":
            bundle = initiative_context(config, args.identifier, budget=args.budget)
        elif args.context_command == "task":
            bundle = initiative_context(config, args.initiative, args.repository, args.budget)
        else:
            bundle = release_context(config, args.identifier, args.budget)
        _write_or_print(bundle.text, args.output)
        return 0
    if args.command == "validate":
        functions: dict[str, Callable[[], dict[str, Any]]] = {
            "workspace": lambda: validate_workspace(config), "contracts": lambda: contract_inventory(config),
            "fixtures": lambda: validate_fixtures(config), "tasks": lambda: validate_tasks(config),
            "releases": lambda: validate_releases(config), "locks": lambda: validate_locks(config),
            "generated": lambda: validate_generated(config), "docs": lambda: validate_document_links(config),
            "all": lambda: validate_all(config),
        }
        return _validation(functions[args.validate_command]())
    if args.command == "compatibility":
        if args.compatibility_command == "report":
            value = json.loads(args.path.read_text(encoding="utf-8")); errors = validate_report(value)
            return _validation({"status": "ok" if not errors else "failed", "errors": errors})
        value = run_compatibility(config, full=args.compatibility_command == "full", execute=args.execute)
        if args.output:
            args.output.write_text(dump_data(value), encoding="utf-8")
        _json(value); return 1 if value["status"] == "failed" else 0
    if args.command == "benchmark":
        value = benchmark_run(config, args.repository, execute=args.execute) if args.benchmark_command == "run" else benchmark_compare(args.left, args.right)
        _json(value); return 1 if value["status"] == "failed" else 0
    if args.command == "release":
        command = args.release_command
        if command == "plan": value = plan_release(config, args.repository, args.version, args.id)
        elif command == "prepare": value = prepare_release(config, args.repository, args.version, args.id, dry_run=not args.write_plan)
        elif command == "validate-candidate": value = validate_candidate(config, args.id)
        elif command == "tag": value = tag_release(config, args.id, execute=args.execute)
        elif command == "publish": value = publish_release(config, args.id, execute=args.execute)
        elif command == "verify-published": value = verify_published(config, args.id, network=args.network, write_lock=args.write_lock)
        elif command == "create-consumer-tasks": value = {"created": create_consumer_tasks(config, args.id)}
        elif command == "status": value = release_status(config, args.id)
        elif command == "drift": value = drift(config)
        elif command == "complete": value = {"path": str(complete_release(config, args.id))}
        else: raise ValueError(command)
        _json(value)
        return 1 if isinstance(value, dict) and value.get("status") == "failed" else 0
    if args.command == "reports":
        _json({"generated": [str(path) for path in write_generated(config)]}); return 0
    raise ValueError(args.command)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(message)s")
    try:
        return dispatch(args)
    except (ConfigurationError, ValueError, FileNotFoundError, FileExistsError) as exc:
        LOG.error("%s", exc)
        return 2
    except KeyboardInterrupt:
        LOG.error("interrupted")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
