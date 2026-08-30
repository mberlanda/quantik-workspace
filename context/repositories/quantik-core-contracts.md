# quantik-core-contracts Packet

> **Purpose:** interoperability authority — owns the schemas both stacks are validated against.
> **Load with:** [`../system/release-model.md`](../system/release-model.md), [`../system/domain-glossary.md`](../system/domain-glossary.md), [`../system/repository-map.md`](../system/repository-map.md)

Important areas: `contracts.json`, `VERSION`, `schemas/`, `fixtures/`, validators, `actions/`, workflows, and normative docs. Version source is `VERSION`; required mirror is `contracts.json.release_version`. Current inspected candidate: clean `release/v1.2.0` at `beb26e7e07184b2fd61b9aef242358788400d861`; latest local tag **`v1.2.0`** (verified 2026-08-30 — `git tag`; superseded the `v1.1.0` this packet previously listed).

Commands: stdlib unittest discovery and `scripts/validate_contracts.py`. Published interfaces: cross-language-smoke and opening-book-consistency composite actions; Python/Rust reusable workflows. Responsibilities: bundle release, schemas/fixtures/actions, migration/version policy.

Failure/drift hotspots: premature external `@v1.2.0` docs; stale 1.1 examples; candidate actions not exercised relatively; consumer refers to nonexistent validate-contracts action. Never implement game logic here.
