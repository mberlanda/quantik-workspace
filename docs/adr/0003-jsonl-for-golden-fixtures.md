# ADR 0003: JSONL for Golden Fixtures

## Context
Smoke evidence must be readable, deterministic, and cross-language.

## Decision
Use JSON Schema and small JSONL fixtures with release metadata and wire IDs.

## Alternatives
Opaque binaries, databases, or large Parquet fixtures.

## Consequences
Diffs and debugging are easy; parsing is dependency-light. JSONL is verbose and deliberately not the bulk-training format.
