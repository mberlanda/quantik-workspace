"""Read-only Git inspection and tightly guarded mutation primitives."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .subprocesses import CommandError, run


@dataclass(frozen=True)
class GitStatus:
    path: str
    exists: bool
    is_git: bool
    branch: str | None = None
    commit: str | None = None
    upstream: str | None = None
    dirty: bool = False
    untracked: int = 0
    ahead: int | None = None
    behind: int | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def inspect(path: Path) -> GitStatus:
    if not path.exists():
        return GitStatus(str(path), False, False)
    probe = run(["git", "rev-parse", "--is-inside-work-tree"], path, check=False)
    if probe.returncode or probe.stdout.strip() != "true":
        return GitStatus(str(path), True, False)
    result = run(["git", "status", "--porcelain=v2", "--branch"], path)
    branch: str | None = None
    commit: str | None = None
    upstream: str | None = None
    ahead: int | None = None
    behind: int | None = None
    dirty = False
    untracked = 0
    for line in result.stdout.splitlines():
        if line.startswith("# branch.head "):
            branch = line.removeprefix("# branch.head ")
            if branch == "(detached)":
                branch = None
        elif line.startswith("# branch.oid "):
            commit = line.removeprefix("# branch.oid ")
        elif line.startswith("# branch.upstream "):
            upstream = line.removeprefix("# branch.upstream ")
        elif line.startswith("# branch.ab "):
            fields = line.split()
            ahead = int(fields[2].removeprefix("+"))
            behind = int(fields[3].removeprefix("-"))
        elif line.startswith("?"):
            dirty = True
            untracked += 1
        elif not line.startswith("#"):
            dirty = True
    return GitStatus(str(path), True, True, branch, commit, upstream, dirty, untracked, ahead, behind)


def tags(path: Path) -> list[str]:
    result = run(["git", "tag", "--list", "--sort=-v:refname"], path)
    return [line for line in result.stdout.splitlines() if line]


def tag_commit(path: Path, tag: str) -> str | None:
    result = run(["git", "rev-list", "-n", "1", tag], path, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def create_annotated_tag(path: Path, tag: str, message: str, commit: str) -> None:
    if tag_commit(path, tag):
        raise CommandError(run(["git", "show", "--no-patch", tag], path, check=False))
    run(["git", "tag", "-a", tag, "-m", message, commit], path)

