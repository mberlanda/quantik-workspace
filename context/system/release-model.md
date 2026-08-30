# Release Model

> **Purpose:** How `quantik-core-contracts` / `quantik-core-rust` / `quantik-core-py` version and tag together, and the deadlock that is the reason this is written down.
> **Load with:** [`canonical-invariants.md`](canonical-invariants.md) (invariant 5: contracts are the source of truth) · [`repository-map.md`](repository-map.md) (which repos this applies to)

## Lockstep versioning

`quantik-core-contracts`, `quantik-core-rust`, and `quantik-core-py` share one version
number. Contracts' `VERSION` file is the source of truth. **`quantik-models-py`, the API,
the visualizer, and `articles` are not part of this lockstep** and version independently
(`repository-map.md`).

**Tag order matters: contracts first, then py, then rust.** Rust's tag build checks out py
at the same tag ref and fails outright if that ref is missing. Tagging rust before py is
not a style preference — it breaks the build.

`v1.2.0` shipped 2026-08-28: contracts#19, rust#37/39/40, py#46, annotated `v1.2.0` tags on
all three.

## Two independent version axes, not one (ADR 0007)

Package/crate version, contracts repository release, wire contract ID (`selfplay.v1`,
`qfen.v1`, …), action ref, CI's expected-release value, and a consumer's
supported-contract declaration are separate axes with separate lifetimes. Conflating any
two of them is the exact failure mode below.

## Two-phase validation (ADR 0008)

A release candidate cannot depend on a tag that does not exist yet, while consumers need
proof against the immutable external ref. So validation runs twice: **source/candidate
mode** tests the checked-out release candidate through relative paths; **published mode**,
after tagging, tests the exact external tag and its assets. Skipping straight to published
mode reintroduces the circular dependency; testing only source mode never catches a
publication defect.

## The 1.2.0 deadlock — six weeks, one fused comparison

Both release branches referenced the shared GitHub Actions at `@v1.2.0` before that tag
existed — contracts had `1.2.0` in `VERSION` on `main` with no tag behind it for six weeks
(`v1.1.0` was cut 14 July; nothing followed until 28 August). Every job died in seconds
with an action-resolution error that pointed at the wrong place, and the Python leg of the
release (py#46) had not even been opened for most of that window — a three-way lockstep
release in which one of the three parties had not turned up.

**The structural root cause**, and the reason a shared validator function is now suspect
project-wide: `normalize_summary()` in
`quantik-core-contracts/scripts/validate_opening_book_summary.py` returns a dict that
includes `contract_version`, and `main()` fails whenever the Rust and Python dicts differ.
So the cross-implementation check — *do the two engines agree about the game?* — silently
also enforced *are both stacks on the same release?* Two claims with different lifetimes,
fused into one equality. A release that is correct but not yet fully tagged cannot pass
this check even though the engines agree perfectly, which is what made the six weeks hard
to diagnose rather than merely slow: every failure looked like an engine disagreement.

**Broken by process, not yet by code:** merging one release PR while its own `main` was
knowingly red, then merging the second, then re-running the first. The fix at the root —
excluding `contract_version` from the Rust-vs-Python equality while keeping it for the
`--expected-release` assertion — is not yet applied; it is workstream 2
("release-engineering hardening"), not started as of 2026-08-30. Until it lands, the same
class of deadlock can recur on the next lockstep release.

Full account: `articles/the-deadlock.md` (draft, unpublished) and WORKSTREAMS.md §1–§2.
