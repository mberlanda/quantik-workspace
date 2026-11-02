# Release Plan

The forward version ladder for every repository that cuts releases, and the initiatives
that gate each cut. Companion to [`release-policy.md`](release-policy.md) (the rules) and
[`release-runbook.md`](release-runbook.md) (the steps).

**These are planned versions, not release trains.** A `QREL-YYYY-NNN` record is created
with `quantik-workspace release plan` **when the gating initiatives have merged**, not
before. QREL-2026-001 is the reason for that rule: it was opened while its work was still
in flight, sat in `releases/active/` as `planned` for six weeks while the release it
described actually shipped, and had to be reconciled retroactively on 2026-09-07. An open
train with no imminent cut is a record that rots, and it makes `release drift` report every
consumer as lagging a version nobody is working toward.

## Where the ledger stands

| Repository | Latest | Ledger |
|---|---|---|
| `quantik-core-contracts` | `v1.4.0` | QREL-2026-001 (1.2.0), QREL-2026-002 (1.3.0), QREL-2026-004 (1.4.0), all `completed` |
| `quantik-core-py` | `v1.4.0` | tagged, publish pending (PyPI still 1.3.0, #51); declares contracts 1.4.0 |
| `quantik-core-rust` | `v1.4.0` | tagged, publish pending (crates.io still 1.3.0, #48); declares contracts 1.4.0 |
| `quantik-models-py` | `v1.1.0` | contracts release derived from `quantik-core-py` at runtime |
| `quantik-api-rust` | *never tagged* | `0.1.0` in `Cargo.toml`, no `v0.1.0` tag |
| `quantik-qfen-visualizer` | *never tagged* | `0.2.0` in `package.json`, no `v0.2.0` tag |

The compatibility matrix withholds `supported` at every release, including the current
one. The portability adapters now run (their arguments are optional) and the smoke passes
for Python and Rust, but only on post-tag checkouts and over 3 cases, so no cut has tag-exact
cross-stack evidence yet. See [`../generated/compatibility-matrix.md`](../generated/compatibility-matrix.md).
Running the smoke at each release tag is the cheapest way to close that gap.

## Core trio — `quantik-core-contracts`, `quantik-core-py`, `quantik-core-rust`

The three share a minor line; contracts may take patch releases the consumers do not follow
(a patch tag of this kind, 1.3.1, was withdrawn: its tag and release no longer exist on origin). Tag contracts first, then **py before rust** — rust's tag build
checks out py at the same ref.

| Version | Tag | What it carries | Gated on | Kind |
|---|---|---|---|---|
| 1.4.0 | `v1.4.0` | Consolidates the former 1.4.0 and 1.5.0 rows: `engine-request.v1` / `engine-response.v1` (settling the `quantik.` prefix), the opening-probe contract and `engine-response.v2`. Tagged 2026-11-02, publish pending (PyPI and crates.io still 1.3.0) | QW-019, QW-004, QW-018 | additive + a recorded rename migration |
| 1.6.0 | `v1.6.0` | Checkpoint consumer compatibility: capability negotiation, cross-language numerical parity | QW-007 | additive — **verify**, the checkpoint surface is the one most likely to break |
| 1.7.0 | `v1.7.0` | Book-guided self-play: opening-book, pairing and provenance semantics | QW-003 | additive |
| 1.8.0 | `v1.8.0` | Search and H2H active-learning feedback loop | QW-005 | additive |

**1.4.0 shipped as one release.** QW-019, QW-004 and QW-018 all merged before the cut, so the planned 1.4.0 and 1.5.0 rows were consolidated; 1.5.0 is no longer a separate planned release. It is tagged on all three repositories (2026-11-02) and publishing is deferred (mberlanda/quantik-core-py#51, mberlanda/quantik-core-rust#48).

QW-006 (search-derived policy targets) touches `quantik-core-rust` and `quantik-models-py`
but registers no contract. It rides whichever core minor is open when it lands and gates no
cut of its own.

## `quantik-models-py`

Versioned independently; it consumes contracts but publishes its own PyPI line. v1.1.0
shipped QW-030 (the one-port playground) on 2026-09-07.

| Version | Tag | What it carries | Gated on |
|---|---|---|---|
| 1.2.0 | `v1.2.0` | Public play: storeless deployment, the ply-0/ply-1 arena, and the skill-level ladder it makes derivable | QW-009, QW-024, QW-010 |
| 1.3.0 | `v1.3.0` | Training foundation: versioned pipeline profiles, the settled corpus axis, corpus label structure and the shallow-ply floor | QW-002, QW-023, QW-027 |
| 1.4.0 | `v1.4.0` | Opening book: coverage expansion to plies 0-6 and the finished exact solve | QW-021, QW-028 |

QW-024 is the ordering constraint inside 1.2.0: QW-010's mapping is derived from its arena,
and QW-030 shipped the UI slot for a ladder whose data does not exist yet. Run the arena
first and 1.2.0 falls out; skip it and 1.2.0 ships another control panel.

QW-011 (puzzle mode) and QW-029 (shallow-ply standing metric) are deliberately unscheduled.
Both need a scoping pass before they can anchor a release — see
[`../../tasks/complexity-assessment.md`](../../tasks/complexity-assessment.md).

## `quantik-api-rust` — first release

Never tagged. `0.1.0` sits in `Cargo.toml` with no `v0.1.0` behind it, which is what
`release drift` reports today.

| Version | Tag | What it carries | Gated on |
|---|---|---|---|
| 0.2.0 | `v0.2.0` | Speaks the registered engine contracts; engine response type | QW-019 (W2), QW-018 |
| 0.3.0 | `v0.3.0` | ONNX model serving behind a Cargo feature | QW-017 |
| 0.4.0 | `v0.4.0` | Multi-arch container distribution | QW-020 |

Cutting `v0.2.0` rather than back-filling `v0.1.0` is deliberate: 0.1.0 speaks a contract
that does not exist in the registry, and tagging it would publish that as a supported
surface.

## `quantik-qfen-visualizer` — first release

| Version | Tag | What it carries | Gated on |
|---|---|---|---|
| 0.3.0 | `v0.3.0` | Registered engine-contract adoption; puzzle picker UI | QW-019 (W3), QW-011 |

The visualizer is consumed two ways — opened from `file://`, and vendored into
`quantik-models-py` by `scripts/sync_visualizer.py`. A tag gives the vendoring step
something immutable to record in `app/SOURCE.json` instead of a branch commit.

## Cutting one

1. Confirm every gating initiative is merged (`quantik-workspace task status`, and the
   `blocked_by` column of [`../generated/task-dependency-graph.md`](../generated/task-dependency-graph.md)).
2. `quantik-workspace release plan --repository <repo> --version <x.y.z> --id QREL-2026-NNN`.
3. Follow [`release-runbook.md`](release-runbook.md). Tag and publish are separate guarded
   commands, and exact tags never move.
4. Record evidence in the compatibility matrix from a passing run — not from agreement
   between declarations, which is what every entry rests on today.
