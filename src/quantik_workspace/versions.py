"""Independent version axes, SemVer handling, and occurrence classification."""

from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
import json
from pathlib import Path
import re
import tomllib
from typing import Any, Iterable


SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<pre>[0-9A-Za-z.-]+))?(?:\+(?P<build>[0-9A-Za-z.-]+))?$"
)
VERSION_RE = re.compile(r"(?<![\w.])v?\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?![\w.])")
ACTION_RE = re.compile(r"uses:\s*([^\s@]+)@([^\s#]+)")
EXPECTED_RE = re.compile(r"expected[-_]release\s*:\s*[\"']?([^\s\"']+)")


@total_ordering
@dataclass(frozen=True)
class SemVer:
    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...] = ()

    @classmethod
    def parse(cls, value: str) -> "SemVer":
        match = SEMVER_RE.fullmatch(value.strip().removeprefix("v"))
        if not match:
            raise ValueError(f"not valid SemVer: {value!r}")
        pre = tuple((match.group("pre") or "").split(".")) if match.group("pre") else ()
        return cls(int(match.group("major")), int(match.group("minor")), int(match.group("patch")), pre)

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return base + ("-" + ".".join(self.prerelease) if self.prerelease else "")

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        left = (self.major, self.minor, self.patch)
        right = (other.major, other.minor, other.patch)
        if left != right:
            return left < right
        if not self.prerelease:
            return False if not other.prerelease else False
        if not other.prerelease:
            return True
        for left_part, right_part in zip(self.prerelease, other.prerelease):
            if left_part == right_part:
                continue
            left_numeric = left_part.isdigit()
            right_numeric = right_part.isdigit()
            if left_numeric and right_numeric:
                return int(left_part) < int(right_part)
            if left_numeric != right_numeric:
                return left_numeric
            return left_part < right_part
        return len(self.prerelease) < len(other.prerelease)


def _pointer(value: Any, pointer: str) -> Any:
    if pointer.startswith("/"):
        parts = pointer.split("/")[1:]
    else:
        parts = pointer.split(".")
    current = value
    for part in parts:
        current = current[part.replace("~1", "/").replace("~0", "~")]
    return current


def read_version_source(repository: Path, source: dict[str, Any] | None) -> str | None:
    if not source:
        return None
    path = repository / str(source["path"])
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if "pattern" in source:
        match = re.search(str(source["pattern"]), text)
        if not match:
            return None
        return match.groupdict().get("version") or match.group(1)
    kind = source.get("kind", "text")
    if kind == "text":
        return text.strip()
    if kind == "json":
        return str(_pointer(json.loads(text), str(source["pointer"])))
    if kind == "toml":
        return str(_pointer(tomllib.loads(text), str(source["pointer"])))
    raise ValueError(f"unsupported version source kind: {kind}")


def classify_occurrence(path: str, line: str) -> str:
    lower = f"{path} {line}".lower()
    if path.endswith("VERSION") or ("pyproject.toml" in path and "version" in line):
        return "authoritative version"
    if path.endswith("contracts.json") and "release_version" in line:
        return "required mirror"
    if "supported_contract" in lower or "contracts_release" in lower and "src/" in lower:
        return "supported-contract declaration"
    if "expected-release" in lower or "expected_release" in lower:
        return "candidate expectation"
    if "uses:" in lower and "quantik-core-contracts" in lower:
        return "published action reference" if path.lower().endswith((".md", ".rst")) else "consumer action reference"
    if path.startswith("fixtures/") or path.endswith(".jsonl"):
        return "fixture metadata"
    if path.startswith("tests/") or "/tests/" in path:
        return "source assertion"
    if path.endswith(("action.yml", "action.yaml")) and "release" in lower:
        return "candidate expectation"
    if "docs/superpowers" in lower or "research/" in lower:
        return "historical compatibility test"
    if "changelog" in lower:
        return "release record"
    if path.lower().endswith((".md", ".rst")):
        return "documentation example"
    return "unclassified version occurrence"


def iter_text_files(root: Path) -> Iterable[Path]:
    excluded = {".git", ".venv", "target", "dist", "build", "__pycache__", ".mypy_cache"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in excluded for part in path.parts):
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        yield path


def scan_occurrences(root: Path) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    for path in iter_text_files(root):
        relative = str(path.relative_to(root))
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in VERSION_RE.finditer(line):
                occurrences.append(
                    {
                        "path": relative,
                        "line": number,
                        "value": match.group(0),
                        "classification": classify_occurrence(relative, line),
                        "text": line.strip()[:300],
                    }
                )
    return occurrences


def scan_action_references(root: Path) -> list[dict[str, Any]]:
    references: list[dict[str, Any]] = []
    github = root / ".github"
    if not github.exists():
        return references
    for path in iter_text_files(github):
        relative = str(path.relative_to(root))
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            action = ACTION_RE.search(line)
            if action:
                references.append({"path": relative, "line": number, "action": action.group(1), "ref": action.group(2)})
            expected = EXPECTED_RE.search(line)
            if expected:
                references.append({"path": relative, "line": number, "expected_release": expected.group(1)})
    return references
