"""Small, explicit subprocess boundary used by all orchestration commands."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Iterable


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    cwd: Path
    returncode: int
    stdout: str
    stderr: str


class CommandError(RuntimeError):
    def __init__(self, result: CommandResult):
        rendered = " ".join(result.command)
        detail = result.stderr.strip() or result.stdout.strip()
        super().__init__(f"command failed ({result.returncode}): {rendered}\n{detail}")
        self.result = result


def run(
    command: Iterable[str],
    cwd: Path,
    *,
    check: bool = True,
    timeout: int = 120,
) -> CommandResult:
    argv = tuple(str(part) for part in command)
    completed = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    result = CommandResult(argv, cwd, completed.returncode, completed.stdout, completed.stderr)
    if check and result.returncode:
        raise CommandError(result)
    return result

