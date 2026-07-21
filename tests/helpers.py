from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import Any


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def init_git(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=path, check=True)
    (path / "README.md").write_text("fixture\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Tests", "-c", "user.email=tests@example.invalid", "commit", "-q", "-m", "initial"],
        cwd=path,
        check=True,
    )
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, text=True, capture_output=True, check=True).stdout.strip()


def minimal_manifest(repository_path: str = "repo") -> dict[str, Any]:
    return {
        "version": 1,
        "workspace": {"name": "test", "repository_layout": "siblings", "context_budget_tokens": 1000},
        "repositories": {
            "repo": {
                "url": "https://example.invalid/repo",
                "path": repository_path,
                "role": "test",
                "default_branch": "main",
                "versions": {"repository_source": {"path": "VERSION", "kind": "text"}, "release_mirrors": [], "supported_contracts_source": None},
                "commands": {},
            }
        },
        "dependencies": [],
    }
