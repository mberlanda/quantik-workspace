# QW-019: Register the Phantom Engine API Contracts

> **Purpose:** Promote the two most-used wire formats in the project from string
> literals to registered, validated contracts.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-core-contracts.md`](../../../context/repositories/quantik-core-contracts.md)

## Problem and motivation

`quantik.engine-request.v1` and `quantik.engine-response.v1` look like contracts. They
carry the naming convention, and the API rejects a request whose `schema` field does not
match. But they are **not in the registry**, so there is no schema, no fixture, and no
validator. Verified 2026-08-30:

| where | what |
|---|---|
| `quantik-api-rust/src/lib.rs:22` | `pub const REQUEST_SCHEMA: &str = "quantik.engine-request.v1";` |
| `quantik-qfen-visualizer/src/engines.js:54` | `schema: "quantik.engine-request.v1",` |
| `quantik-core-contracts/contracts.json` | absent |

Nothing keeps the two in agreement. The check that exists — string equality on the
`schema` field — asserts that both sides *claim* the same format, which is the one thing
a mismatch would not change.

This directly contradicts the project's own rule that **contracts are the source of
truth**. Two repositories currently define a wire format by hardcoding it, and the
registry is unaware.

Two problems ride along:

1. **Naming.** Every registered contract is `observation.v1`, `qfen.v1`,
   `game-result.v1` — no `quantik.` prefix. These two are the exception, and it is an
   accident of being written outside the registry.
2. **A third implementation now exists.** The Python play service in
   `quantik-models-py` speaks the same format. When §7 was written there were two
   hardcoded copies; there are three.

## Existing and desired behaviour

Existing: a shared string constant, duplicated, unvalidated, and a naming convention
violated by exactly the contracts nobody registered.

Desired: both schemas in the registry with fixtures, all three implementations
validating against them in their own tests, and one recorded decision about the name.

## Contracts and repositories

Creates `engine-request` and `engine-response` in `quantik-core-contracts`.
`quantik-api-rust` and `quantik-qfen-visualizer` are the two implementations named in
the original workstream; `quantik-models-py` is the third and is tracked here as a
follow-on rather than a fourth affected repository, to keep this packet executable.

## Constraints and preserved invariants

- **Contracts are the source of truth.** Code is validated against schemas, not the
  reverse. This is the ADR that makes contract-first non-negotiable here.
- **A rename is a breaking change to deployed clients.** Whatever is decided about the
  `quantik.` prefix, an already-running visualizer pins the old string. Either accept
  both for a release or do not rename.

## Ordering

This packet blocks [`QW-018`](../QW-018-engine-response-type/initiative.md), which would
otherwise add five fields to two hardcoded copies by hand.

## Provenance

Migrated from WORKSTREAMS §7 ("Engine API contract — NOT STARTED"). Both line numbers
re-verified 2026-08-30; the third implementation is new since.
