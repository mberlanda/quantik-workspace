# QW-015: Release-Engineering Hardening

> **Purpose:** Separate "the two engines agree" from "both stacks are on the same
> release", so a normal PR stops requiring a coordinated four-repo tag.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/system/release-model.md`](../../../context/system/release-model.md)

## Problem and motivation

The 1.2.0 release deadlocked. The root cause is one line in a shared validator, and
it is still there.

`quantik-core-contracts/scripts/validate_opening_book_summary.py` builds a normalized
summary dict that **includes `contract_version`** (line 118), and `main()` fails when
the Rust and Python dicts differ (line 142). The check is advertised as
cross-implementation agreement about the *game*; it also enforces agreement about the
*release*. Those two claims have different lifetimes — engines can and should agree
about the game across a version skew — and fusing them means every change that moves
one repo's version breaks the other repo's PRs until both are tagged.

The composite action makes it worse: `actions/opening-book-consistency/action.yml:23`
declares `default: "1.2.0"`. Removing `expected-release` from a caller does not remove
the constraint; it reintroduces the literal.

## Existing and desired behaviour

Existing: the equality compares a dict carrying `contract_version`; `--expected-release`
exists as a separate flag but the fused comparison makes it redundant and the action
default makes it unavoidable.

Desired: the equality compares only game facts (`depth`, `total_positions`,
`terminal_positions`, `total_edges`, `per_depth`). `--expected-release` remains the one
place a release assertion is made, is opt-in, and has no default.

## Contracts and repositories

`opening-book-summary.v1` is read, not changed — this is a validator and workflow
change, not a schema change. `quantik-core-contracts` owns the fix;
`quantik-core-rust` and `quantik-core-py` own dropping the input from their callers.

## Constraints and preserved invariants

- **Contracts stay the source of truth.** The schema is unchanged; only what the
  validator chooses to compare changes.
- **Lockstep versioning survives** for contracts / rust / py — this initiative removes
  the enforcement from the *wrong check*, not the policy. See
  [`release-model.md`](../../../context/system/release-model.md).
- **Tag contracts first; tag py before rust.** Rust's tag build checks out py at the
  same ref. Any preflight added here must not break that ordering.

## Ordering

1 removes the deadlock on its own and is worth landing alone. 2 prevents its return.
3-5 are hardening and can follow.

## Provenance

Migrated from WORKSTREAMS §2 ("Release-engineering hardening — NOT STARTED"). Every
line number above was re-verified against the working tree on 2026-08-30, not copied.
