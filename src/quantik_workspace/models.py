"""Validated file-model helpers; intentionally small and dependency-free."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


class ValidationError(ValueError):
    pass


def _type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, True)


def validate_instance(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    expected = schema.get("type")
    if isinstance(expected, str) and not _type_matches(value, expected):
        return [f"{path}: expected {expected}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not one of {schema['enum']!r}")
    if isinstance(value, str) and "pattern" in schema and not re.fullmatch(schema["pattern"], value):
        errors.append(f"{path}: {value!r} does not match {schema['pattern']!r}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: expected at least {schema['minItems']} items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_instance(item, item_schema, f"{path}[{index}]"))
    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                errors.extend(validate_instance(item, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property {key!r}")
    return errors


@dataclass(frozen=True)
class CompatibilityResult:
    repository: str
    operation: str
    status: str
    category: str
    diagnostics: str = ""
    output: dict[str, Any] | None = None


@dataclass
class ReleaseTrain:
    id: str
    status: str
    producer: dict[str, Any]
    consumers: dict[str, Any] = field(default_factory=dict)
    compatibility: dict[str, Any] = field(default_factory=dict)
    release_order: list[str] = field(default_factory=list)

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "ReleaseTrain":
        missing = [key for key in ("id", "status", "producer") if key not in value]
        if missing:
            raise ValidationError(f"release train missing: {', '.join(missing)}")
        return cls(
            id=str(value["id"]),
            status=str(value["status"]),
            producer=dict(value["producer"]),
            consumers=dict(value.get("consumers", {})),
            compatibility=dict(value.get("compatibility", {})),
            release_order=list(value.get("release_order", [])),
        )
