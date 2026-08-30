# QW-022: Workspace Repo Hygiene — Remaining Items

> **Purpose:** Close the three hygiene items that survive, and keep one correction
> visible on purpose.
> **Load with:** [`context/system/repository-map.md`](../../../context/system/repository-map.md)

## Problem and motivation

Three items are open. One is closed and stays on the record because of how it failed.

**1. `e2e-data-pipeline.yml` checks out `quantik-core-py` with no `ref:`.** Verified
2026-08-30 at lines 78-79: `repository: mberlanda/quantik-core-py` and
`path: quantik-core-py`, with no ref. It tracks that repository's `main` and inherits
its breakage silently — a failure that looks like a bug in `quantik-models-py`.

The newer `tests.yml` deliberately does the opposite: it installs the *published*
`quantik-core>=1.2` from PyPI, so unit-test green does not depend on another repo's
in-flight work. **These two workflows answer different questions** — one asks "does the
published stack work", the other asks "do the two repos' current heads integrate" — so
the fix is to make the e2e workflow's choice explicit, not to make it identical.

**2. `articles` has no git remote.** Verified 2026-08-30: `git remote -v` is empty,
one commit at `7d8b75b`. Three finished Season Two drafts exist on one disk. This is
also an acceptance criterion of
[`QW-016`](../QW-016-season-two-article-publication/initiative.md); it is repeated here
because it is a hygiene failure independent of whether anything is ever published.

**3. `.oracle-worktree/` sits at the workspace root** with no recorded owner or purpose.

## The correction that stays visible

`quantik-api-rust` **has** a remote: `git@github.com:mberlanda/quantik-api-rust.git`,
with local `main` in sync at `f814093`. Verified three ways on 2026-08-30 —
`git remote -v`, `git ls-remote origin HEAD` matching local `HEAD`, and the public
GitHub page.

The opposite was recorded as fact for weeks. It propagated into the root `CLAUDE.md`
repository table and into the Docker workstream, where it read as a hard blocker and
kept [`QW-020`](../QW-020-rust-api-container-distribution/initiative.md) parked. Both
documents are corrected; the false claim is **kept visible** in
[`workstreams-archive.md`](../../../docs/history/workstreams-archive.md) §12 rather than
deleted, because a wrong fact that survived that long is more useful as an exhibit than
as a gap.

## Contracts and repositories

`quantik-models-py` owns item 1. `articles` owns item 2. Item 3 is at the workspace
root and belongs to no repository, so it is tracked in this packet's status.

## Provenance

Migrated from WORKSTREAMS §12 ("Repo hygiene — OPEN"), with the resolved entries
dropped: `py#9` merged, and `quantik-models-py` local `main` came back in sync on
2026-08-28.
