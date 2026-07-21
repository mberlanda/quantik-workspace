# ADR 0004: Arrow and Parquet for Bulk Data

## Context
Self-play, benchmarks, and training require columnar scale.

## Decision
Use Arrow IPC for high-throughput interchange and Parquet for persisted shards, with explicit logical/physical schemas, releases, and generator metadata.

## Alternatives
JSONL, SQLite, protobuf, or CBOR as the primary bulk format.

## Consequences
Analytics and ML readers can scan efficiently. Native dependencies and schema-evolution discipline are required; derived tensor stores must remain reproducible.
