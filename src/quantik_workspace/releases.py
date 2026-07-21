"""Two-phase release orchestration, drift detection, and guarded publication."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
import shutil
from typing import Any

from . import git
from .config import WorkspaceConfig, dump_data, load_data
from .models import ReleaseTrain, ValidationError
from .subprocesses import run
from .versions import SemVer, read_version_source, scan_action_references, scan_occurrences


STATES = [
    "planned",
    "prepared",
    "candidate-green",
    "tagged",
    "published",
    "producer-verified",
    "consumer-updates-open",
    "consumer-compatible",
    "completed",
]
TERMINAL_STATES = {"failed", "rolled-back"}


def can_transition(current: str, target: str) -> bool:
    if target in TERMINAL_STATES:
        return current != "completed"
    if current in TERMINAL_STATES or current not in STATES or target not in STATES:
        return False
    return STATES.index(target) == STATES.index(current) + 1


def _release_dirs(config: WorkspaceConfig) -> list[Path]:
    result: list[Path] = []
    for state in ("active", "completed"):
        root = config.root / "releases" / state
        if root.exists():
            result.extend(path for path in root.iterdir() if path.is_dir())
    return result


def find_release(config: WorkspaceConfig, identifier: str) -> Path:
    matches = [path for path in _release_dirs(config) if path.name == identifier]
    if len(matches) != 1:
        raise ValueError(f"expected one release {identifier}, found {len(matches)}")
    return matches[0]


def load_release(config: WorkspaceConfig, identifier: str) -> tuple[Path, dict[str, Any]]:
    path = find_release(config, identifier)
    return path, load_data(path / "release.yaml")


def validate_release_mapping(value: dict[str, Any], config: WorkspaceConfig | None = None) -> list[str]:
    errors: list[str] = []
    try:
        train = ReleaseTrain.from_mapping(value)
    except ValidationError as exc:
        return [str(exc)]
    if not re.fullmatch(r"QREL-\d{4}-\d{3}", train.id):
        errors.append("id must match QREL-YYYY-NNN")
    if train.status not in STATES and train.status not in TERMINAL_STATES:
        errors.append(f"unknown release status: {train.status}")
    producer = train.producer
    for field in ("repository", "version", "tag", "branch"):
        if not producer.get(field):
            errors.append(f"producer.{field} is required")
    version = producer.get("version")
    if version:
        try:
            SemVer.parse(str(version))
        except ValueError as exc:
            errors.append(str(exc))
        if producer.get("tag") != f"v{version}":
            errors.append("producer.tag must equal v${producer.version}")
    if config:
        known = set(config.repositories)
        if producer.get("repository") not in known:
            errors.append("producer.repository is unknown")
        unknown = sorted(set(train.consumers) - known)
        if unknown:
            errors.append(f"unknown consumers: {', '.join(unknown)}")
        if train.release_order and train.release_order[0] != producer.get("repository"):
            errors.append("release_order must begin with the producer")
    return errors


def validate_releases(config: WorkspaceConfig) -> dict[str, Any]:
    errors: list[str] = []
    checked = 0
    for path in _release_dirs(config):
        checked += 1
        release_file = path / "release.yaml"
        if not release_file.is_file():
            errors.append(f"{path}: missing release.yaml")
            continue
        try:
            value = load_data(release_file)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        errors.extend(f"{release_file}: {error}" for error in validate_release_mapping(value, config))
        for consumer in value.get("consumers", {}):
            if not (path / "consumers" / f"{consumer}.md").is_file():
                errors.append(f"{path}: missing consumers/{consumer}.md")
    return {"status": "ok" if not errors else "failed", "checked": checked, "errors": errors}


def plan_release(
    config: WorkspaceConfig,
    repository: str,
    version: str,
    identifier: str,
) -> dict[str, Any]:
    target = SemVer.parse(version)
    definition = config.repositories[repository]
    root = config.repository_path(repository)
    current = read_version_source(root, definition["versions"]["repository_source"])
    if current and target <= SemVer.parse(current):
        raise ValueError(f"target {target} must be greater than current {current}")
    consumers: dict[str, Any] = {}
    for name, candidate in config.repositories.items():
        if name == repository:
            continue
        if candidate.get("contracts", {}).get("owner") != repository:
            continue
        supported = read_version_source(config.repository_path(name), candidate.get("versions", {}).get("supported_contracts_source"))
        refs = scan_action_references(config.repository_path(name))
        current_ref = next((item["ref"] for item in refs if "ref" in item and "quantik-core-contracts" in item.get("action", "")), None)
        consumers[name] = {
            "required": True,
            "current_contracts_release": supported,
            "target_contracts_release": str(target),
            "current_action_ref": current_ref,
            "target_action_ref": f"v{target}",
            "adoption_status": "pending",
        }
    return {
        "id": identifier,
        "status": "planned",
        "producer": {
            "repository": repository,
            "previous_version": current,
            "version": str(target),
            "tag": f"v{target}",
            "branch": f"release/v{target}",
            "commit": None,
        },
        "version_sources": {
            "primary": definition["versions"]["repository_source"],
            "mirrors": definition["versions"].get("release_mirrors", []),
        },
        "published_interfaces": definition.get("published_interfaces", {}),
        "consumers": consumers,
        "compatibility": {
            "breaking_changes": [],
            "additive_changes": [],
            "required_checks": [
                "contracts-source-validation",
                "action-source-smoke",
                "release-tag-validation",
                "published-action-smoke",
                *[f"{name}-consumer-smoke" for name in consumers],
            ],
            "evidence": [],
        },
        "release_order": [repository, *consumers],
    }


def prepare_release(
    config: WorkspaceConfig,
    repository: str,
    version: str,
    identifier: str,
    *,
    dry_run: bool = True,
) -> dict[str, Any]:
    definition = config.repositories[repository]
    root = config.repository_path(repository)
    current = read_version_source(root, definition["versions"]["repository_source"])
    target = SemVer.parse(version)
    if current and target <= SemVer.parse(current):
        if str(target) != current:
            raise ValueError(f"target {target} must be greater than current {current}")
    occurrences = scan_occurrences(root)
    classified = [item for item in occurrences if item["value"].removeprefix("v") in {current, str(target)}]
    for item in classified:
        category = item["classification"]
        value = item["value"].removeprefix("v")
        if category in {"historical compatibility test", "release record"}:
            item["proposed_action"] = "retain"
        elif category == "published action reference":
            item["proposed_action"] = "defer until publication"
        elif category == "consumer action reference":
            item["proposed_action"] = "consumer adoption task"
        elif category == "unclassified version occurrence":
            item["proposed_action"] = "manual review"
        else:
            item["proposed_action"] = "retain" if value == str(target) else "update"
    release = plan_release(config, repository, version, identifier) if not current or str(target) != current else {
        **plan_existing_release(config, repository, version, identifier),
    }
    report = {
        "dry_run": dry_run,
        "current_version": current,
        "target_version": str(target),
        "occurrences": classified,
        "unresolved_ambiguities": [item for item in classified if item["proposed_action"] == "manual review"],
        "release": release,
    }
    if dry_run:
        return report
    path = config.root / "releases" / "active" / identifier
    if path.exists():
        raise FileExistsError(path)
    (path / "consumers").mkdir(parents=True)
    release["status"] = "prepared"
    (path / "release.yaml").write_text(dump_data(release), encoding="utf-8")
    (path / "status.md").write_text("# Status\n\nPrepared workspace plan; producer candidate validation is pending.\n", encoding="utf-8")
    (path / "checklist.md").write_text(_checklist(release), encoding="utf-8")
    for name, consumer in release["consumers"].items():
        (path / "consumers" / f"{name}.md").write_text(_consumer_task(name, consumer), encoding="utf-8")
    return report | {"path": str(path)}


def plan_existing_release(config: WorkspaceConfig, repository: str, version: str, identifier: str) -> dict[str, Any]:
    definition = config.repositories[repository]
    root = config.repository_path(repository)
    status = git.inspect(root)
    consumers: dict[str, Any] = {}
    for name, candidate in config.repositories.items():
        if candidate.get("contracts", {}).get("owner") != repository:
            continue
        supported = read_version_source(config.repository_path(name), candidate.get("versions", {}).get("supported_contracts_source"))
        refs = scan_action_references(config.repository_path(name))
        current_ref = next((item["ref"] for item in refs if "ref" in item and "quantik-core-contracts" in item.get("action", "")), None)
        consumers[name] = {"required": True, "current_contracts_release": supported, "target_contracts_release": version, "current_action_ref": current_ref, "target_action_ref": f"v{version}", "adoption_status": "pending"}
    return {
        "id": identifier,
        "status": "planned",
        "producer": {"repository": repository, "previous_version": None, "version": version, "tag": f"v{version}", "branch": status.branch or f"release/v{version}", "commit": status.commit},
        "version_sources": {"primary": definition["versions"]["repository_source"], "mirrors": definition["versions"].get("release_mirrors", [])},
        "published_interfaces": definition.get("published_interfaces", {}),
        "consumers": consumers,
        "compatibility": {"breaking_changes": [], "additive_changes": [], "required_checks": ["contracts-source-validation", "action-source-smoke", "release-tag-validation", "published-action-smoke", *[f"{name}-consumer-smoke" for name in consumers]], "evidence": []},
        "release_order": [repository, *consumers],
    }


def _checklist(release: dict[str, Any]) -> str:
    return "\n".join([
        f"# {release['id']} Checklist", "", "## Candidate", "", "- [ ] Primary and mirrored versions agree.", "- [ ] Source schemas and fixtures pass.", "- [ ] Candidate actions are invoked through relative paths.", "- [ ] Required candidate jobs do not reference the future exact tag.", "- [ ] Release notes and breaking-change declaration exist.", "", "## Published producer", "", "- [ ] Exact annotated tag resolves to the approved commit.", "- [ ] GitHub Release, archive, and checksum exist.", "- [ ] Externally invoked tagged actions pass.", "- [ ] Release lock records tag and full SHA.", "", "## Consumers", "", *[f"- [ ] `{name}` adoption complete." for name in release.get('consumers', {})], "- [ ] Compatibility matrix contains evidence.", "- [ ] Stable documentation points to the published release.", ""
    ])


def _consumer_task(name: str, value: dict[str, Any]) -> str:
    return f"""# {name} adoption

- Previous contracts release: `{value.get('current_contracts_release')}`
- Target contracts release: `{value.get('target_contracts_release')}`
- Previous action ref: `{value.get('current_action_ref')}`
- Target action ref: `{value.get('target_action_ref')}`

## Required work

1. Update the exact action ref and its expected-release input after producer verification.
2. Update the implementation-supported release and live fixtures, retaining historical evidence.
3. Run repository tests and compatibility smoke.
4. Record exact commit, commands, results, PR/merge state, and package release impact.
5. Update the compatibility matrix only from passing evidence.
"""


def validate_candidate(config: WorkspaceConfig, identifier: str) -> dict[str, Any]:
    path, release = load_release(config, identifier)
    errors = validate_release_mapping(release, config)
    producer_name = release.get("producer", {}).get("repository")
    if producer_name not in config.repositories:
        return {"status": "failed", "errors": errors, "warnings": []}
    definition = config.repositories[producer_name]
    root = config.repository_path(producer_name)
    versions = definition.get("versions", {})
    expected = str(release["producer"]["version"])
    primary = read_version_source(root, versions.get("repository_source"))
    if primary != expected:
        errors.append(f"primary version {primary!r} does not match candidate {expected!r}")
    for mirror in versions.get("release_mirrors", []):
        value = read_version_source(root, mirror)
        if value != expected:
            errors.append(f"version mirror {mirror.get('path')} is {value!r}, expected {expected!r}")
    candidate_tag = f"v{expected}"
    if release["producer"].get("tag") != candidate_tag:
        errors.append(f"proposed tag must be {candidate_tag}")
    future_refs: list[str] = []
    local_action_refs: list[str] = []
    workflows = root / ".github" / "workflows"
    if workflows.exists():
        for workflow in workflows.glob("*.y*ml"):
            for number, line in enumerate(workflow.read_text(encoding="utf-8").splitlines(), 1):
                if "uses:" in line and f"@{candidate_tag}" in line:
                    future_refs.append(f"{workflow.relative_to(root)}:{number}")
                if re.search(r"uses:\s*\./actions/", line):
                    local_action_refs.append(f"{workflow.relative_to(root)}:{number}")
    if not git.tag_commit(root, candidate_tag) and future_refs:
        errors.append(f"candidate CI references unpublished tag {candidate_tag}: {', '.join(future_refs)}; use checked-out ./actions paths")
    action_paths = definition.get("published_interfaces", {}).get("github_actions", {})
    if action_paths and not local_action_refs:
        errors.append("candidate workflows do not exercise checked-out composite actions through relative ./actions paths")
    release_notes = release.get("producer", {}).get("release_notes")
    if not release_notes or not (root / str(release_notes)).is_file():
        errors.append("producer release notes are not recorded or do not exist in the candidate tree")
    compatibility = release.get("compatibility", {})
    if "breaking_changes" not in compatibility or "additive_changes" not in compatibility:
        errors.append("breaking_changes and additive_changes must both be declared")
    for name in release.get("consumers", {}):
        if not (path / "consumers" / f"{name}.md").is_file():
            errors.append(f"missing consumer adoption task for {name}")
    status = git.inspect(root)
    warnings = []
    if status.dirty:
        warnings.append(f"producer working tree is dirty at {status.commit}")
    if release["producer"].get("commit") and release["producer"]["commit"] != status.commit:
        errors.append("producer checkout commit differs from the recorded candidate commit")
    return {"status": "passed" if not errors else "failed", "errors": errors, "warnings": warnings, "source_action_references": local_action_refs}


def drift(config: WorkspaceConfig) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    contracts_root = config.repository_path("quantik-core-contracts")
    published_tags = set(git.tags(contracts_root)) if contracts_root.exists() else set()
    active_targets: dict[str, str] = {}
    for release_path in _release_dirs(config):
        release_value = load_data(release_path / "release.yaml")
        if release_value.get("status") == "completed":
            continue
        target = release_value.get("producer", {}).get("version")
        for consumer, consumer_value in release_value.get("consumers", {}).items():
            if consumer_value.get("required") and target:
                active_targets[consumer] = str(target)
    for name, definition in config.repositories.items():
        root = config.repository_path(name)
        versions = definition.get("versions", {})
        repository_version = read_version_source(root, versions.get("repository_source"))
        for mirror in versions.get("release_mirrors", []):
            mirror_value = read_version_source(root, mirror)
            if mirror_value != repository_version:
                issues.append({"repository": name, "kind": "version-mirror", "path": mirror.get("path"), "actual": mirror_value, "expected": repository_version})
        supported = read_version_source(root, versions.get("supported_contracts_source"))
        target_release = active_targets.get(name)
        if target_release and supported != target_release:
            issues.append({"repository": name, "kind": "release-train-supported-contract", "actual": supported, "expected": target_release})
        if repository_version and name != "quantik-models-py" and f"v{repository_version}" not in set(git.tags(root)):
            issues.append({"repository": name, "kind": "repository-version-unpublished", "actual": repository_version, "expected_tag": f"v{repository_version}"})
        refs = scan_action_references(root)
        action_refs = [item for item in refs if item.get("action", "").startswith("mberlanda/quantik-core-contracts")]
        expectations = [item for item in refs if "expected_release" in item]
        for ref in action_refs:
            value = ref["ref"]
            if re.fullmatch(r"v\d+\.\d+\.\d+", value) and value not in published_tags:
                issues.append({"repository": name, "kind": "unpublished-action-ref", "path": ref["path"], "line": ref["line"], "actual": value})
            if not re.fullmatch(r"v\d+\.\d+\.\d+", value):
                issues.append({"repository": name, "kind": "mutable-action-ref", "path": ref["path"], "line": ref["line"], "actual": value})
            action_path = ref.get("action", "").split("quantik-core-contracts/", 1)
            if len(action_path) == 2 and not (contracts_root / action_path[1]).exists():
                issues.append({"repository": name, "kind": "missing-action-path", "path": ref["path"], "line": ref["line"], "actual": action_path[1]})
            if target_release and value != f"v{target_release}":
                issues.append({"repository": name, "kind": "release-train-action-ref", "path": ref["path"], "line": ref["line"], "actual": value, "expected": f"v{target_release}", "defer_until_published": f"v{target_release}" not in published_tags})
        for expected in expectations:
            expected_value = expected["expected_release"].strip("\"'")
            if supported and re.fullmatch(r"\d+\.\d+\.\d+", expected_value) and expected_value != supported:
                issues.append({"repository": name, "kind": "implementation-ci-expectation", "path": expected["path"], "line": expected["line"], "actual": expected_value, "expected": supported})
        for ref in action_refs:
            exact = ref["ref"].removeprefix("v")
            nearby = [item["expected_release"].strip("\"'") for item in expectations if item["path"] == ref["path"]]
            if nearby and re.fullmatch(r"\d+\.\d+\.\d+", exact) and exact not in nearby:
                issues.append({"repository": name, "kind": "action-expectation", "path": ref["path"], "line": ref["line"], "actual": ref["ref"], "expected_release_values": nearby})
    docs = [contracts_root / "README.md", contracts_root / "docs" / "consistency-checks.md"]
    external_ref = re.compile(r"mberlanda/quantik-core-contracts/[^\s`]+@(v\d+\.\d+\.\d+)")
    for document in docs:
        if not document.is_file():
            continue
        for number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), 1):
            match = external_ref.search(line)
            if match and match.group(1) not in published_tags:
                issues.append({"repository": "quantik-core-contracts", "kind": "documentation-unpublished-action-ref", "path": str(document.relative_to(contracts_root)), "line": number, "actual": match.group(1)})
    return {"schema": "quantik-release-drift.v1", "status": "drift" if issues else "consistent", "published_contract_tags": sorted(published_tags), "issues": issues}


def release_status(config: WorkspaceConfig, identifier: str | None = None) -> dict[str, Any]:
    releases = []
    paths = [find_release(config, identifier)] if identifier else _release_dirs(config)
    for path in paths:
        value = load_data(path / "release.yaml")
        producer = value.get("producer", {})
        root = config.repository_path(producer.get("repository")) if producer.get("repository") in config.repositories else None
        releases.append({
            "id": value.get("id"), "status": value.get("status"), "producer": producer,
            "tag_commit": git.tag_commit(root, producer.get("tag")) if root and producer.get("tag") else None,
            "consumers": {name: item.get("adoption_status") for name, item in value.get("consumers", {}).items()},
            "lock_exists": (config.root / "releases" / "locks" / f"{value.get('id')}.yaml").is_file(),
        })
    return {"releases": releases}


def _write_release(path: Path, value: dict[str, Any]) -> None:
    (path / "release.yaml").write_text(dump_data(value), encoding="utf-8")


def transition(config: WorkspaceConfig, identifier: str, target: str) -> dict[str, Any]:
    path, release = load_release(config, identifier)
    current = str(release["status"])
    if not can_transition(current, target):
        raise ValueError(f"invalid release transition: {current} -> {target}")
    release["status"] = target
    _write_release(path, release)
    return release


def tag_release(config: WorkspaceConfig, identifier: str, *, execute: bool = False) -> dict[str, Any]:
    path, release = load_release(config, identifier)
    if release.get("status") != "candidate-green":
        raise ValueError("tagging requires candidate-green state")
    candidate = validate_candidate(config, identifier)
    if candidate["errors"]:
        raise ValueError("candidate validation failed: " + "; ".join(candidate["errors"]))
    producer = release["producer"]
    if not producer.get("commit"):
        raise ValueError("target producer commit is not recorded")
    root = config.repository_path(producer["repository"])
    if git.tag_commit(root, producer["tag"]):
        raise ValueError(f"exact tag already exists and will not be moved: {producer['tag']}")
    action = {"command": ["git", "tag", "-a", producer["tag"], "-m", f"{producer['repository']} {producer['version']}", producer["commit"]], "execute": execute}
    if execute:
        git.create_annotated_tag(root, producer["tag"], f"{producer['repository']} {producer['version']}", producer["commit"])
        release["status"] = "tagged"
        _write_release(path, release)
    return action


def publish_release(config: WorkspaceConfig, identifier: str, *, execute: bool = False) -> dict[str, Any]:
    path, release = load_release(config, identifier)
    if release.get("status") != "tagged":
        raise ValueError("publication requires tagged state")
    producer = release["producer"]
    root = config.repository_path(producer["repository"])
    command = ["gh", "release", "create", producer["tag"], "--verify-tag", "--title", f"{producer['repository']} {producer['version']}", "--generate-notes"]
    if execute:
        run(command, root)
        release["status"] = "published"
        _write_release(path, release)
    return {"command": command, "execute": execute}


def verify_published(config: WorkspaceConfig, identifier: str, *, network: bool = False, write_lock: bool = False) -> dict[str, Any]:
    _, release = load_release(config, identifier)
    producer = release["producer"]
    root = config.repository_path(producer["repository"])
    actual = git.tag_commit(root, producer["tag"])
    errors: list[str] = []
    if actual != producer.get("commit"):
        errors.append(f"tag resolves to {actual}, recorded commit is {producer.get('commit')}")
    for path_value in release.get("published_interfaces", {}).get("github_actions", {}).values():
        result = run(["git", "cat-file", "-e", f"{producer['tag']}:{path_value}/action.yml"], root, check=False)
        if result.returncode:
            errors.append(f"tagged action path is absent: {path_value}/action.yml")
    if network:
        result = run(["gh", "release", "view", producer["tag"], "--json", "tagName,assets"], root, check=False)
        if result.returncode:
            errors.append("GitHub Release is absent or inaccessible")
    lock = {
        "producer": {"repository": f"mberlanda/{producer['repository']}", "version": producer["version"], "tag": producer["tag"], "commit": producer.get("commit")},
        "interfaces": {name: {"path": action_path, "ref": producer["tag"], "commit": producer.get("commit")} for name, action_path in release.get("published_interfaces", {}).get("github_actions", {}).items()},
    }
    if write_lock:
        if not network:
            errors.append("--write-lock requires --network published-release verification")
        elif not errors:
            lock_path = config.root / "releases" / "locks" / f"{identifier}.yaml"
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            lock_path.write_text(dump_data(lock), encoding="utf-8")
    return {"status": "passed" if not errors else "failed", "errors": errors, "lock": lock}


def validate_lock(config: WorkspaceConfig, path: Path) -> list[str]:
    value = load_data(path)
    errors: list[str] = []
    producer = value.get("producer", {})
    for field in ("repository", "version", "tag", "commit"):
        if not producer.get(field):
            errors.append(f"producer.{field} is required")
    if producer.get("version") and producer.get("tag") != f"v{producer['version']}":
        errors.append("producer tag/version mismatch")
    if producer.get("commit") and not re.fullmatch(r"[0-9a-f]{40}", str(producer["commit"])):
        errors.append("producer.commit must be a full SHA")
    for name, interface in value.get("interfaces", {}).items():
        if interface.get("commit") != producer.get("commit"):
            errors.append(f"interfaces.{name}.commit differs from producer")
        if interface.get("ref") != producer.get("tag"):
            errors.append(f"interfaces.{name}.ref differs from producer tag")
    return errors


def create_consumer_tasks(config: WorkspaceConfig, identifier: str) -> list[str]:
    path, release = load_release(config, identifier)
    created: list[str] = []
    directory = path / "consumers"
    directory.mkdir(exist_ok=True)
    for name, value in release.get("consumers", {}).items():
        target = directory / f"{name}.md"
        if not target.exists():
            target.write_text(_consumer_task(name, value), encoding="utf-8")
            created.append(str(target))
    return created


def complete_release(config: WorkspaceConfig, identifier: str) -> Path:
    path, release = load_release(config, identifier)
    if release.get("status") != "consumer-compatible":
        raise ValueError("completion requires consumer-compatible state")
    lock_path = config.root / "releases" / "locks" / f"{identifier}.yaml"
    if not lock_path.is_file() or validate_lock(config, lock_path):
        raise ValueError("a valid release lock is required")
    incomplete = [name for name, item in release.get("consumers", {}).items() if item.get("required") and item.get("adoption_status") != "complete"]
    if incomplete:
        raise ValueError("required consumers are incomplete: " + ", ".join(incomplete))
    matrix = config.root / "docs" / "generated" / "compatibility-matrix.md"
    matrix_text = matrix.read_text(encoding="utf-8") if matrix.is_file() else ""
    if str(release["producer"]["version"]) not in matrix_text or "| supported |" not in matrix_text:
        raise ValueError("compatibility matrix does not record an evidence-backed supported release")
    release["status"] = "completed"
    _write_release(path, release)
    target = config.root / "releases" / "completed" / identifier
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), target)
    return target
