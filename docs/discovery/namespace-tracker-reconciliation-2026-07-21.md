# Namespace Tracker Reconciliation — 2026-07-21

## Scope and evidence

Reviewed namespace `CLAUDE.md`, `FEEDBACK_LOOP_SEED.md`,
`PIPELINE_WORKFLOW_ASSESSMENT.md`, `QUANTIK_NAMESPACE_CONTEXT.md`, and
`QUANTIK_PROGRESS_BOARD.md` against the current local repositories and public
GitHub PR/tag state. Local working trees were not modified during verification.

Exact local starting state:

- contracts `beb26e7e07184b2fd61b9aef242358788400d861`, clean
  `release/v1.2.0`;
- Rust `8360a573b35a6e5fc48288d9c35ef0eb1290b5a0`, clean
  `release/v1.2.0`;
- Python `728b03205707a8bb5a21afd091c6656b7c69c3fa`, dirty
  `release/v1.2.0` with 13 release files modified;
- models `ea8f32ad4fac8fdf4f9620e9a4163e08bb6f2469`, clean `main`.

Public verification found contracts PR #19 open at
`f444652c07e0b3fb637f861d57f7339d1502ff49`, Rust PR #37 open at
`e141b93c4d9c3c8ee2464f8ecc1a2b30f96f7ee1`, no open Python PR, and no
`v1.2.0` tag in contracts, Rust, or Python.

## Reconciliation

| Tracked claim | Verified disposition | Queue action |
| --- | --- | --- |
| Register and adopt `search-summary.v1` | Implemented on main in contracts/Rust/Python | No task |
| Add Python/Rust Parquet readers/writers | Implemented for self-play, observations, and game results | No task |
| Materialize the training-dataset view | Implemented in Python | No task |
| Publish coordinated contracts/Rust/Python 1.2.0 | Prepared but not published; local/remote heads differ | Retain `QREL-2026-001` |
| Canonical state/action/tensor/value portability | Evidence and decisions incomplete | Retain `QW-001` |
| One versioned pipeline definition and run tiers | Not implemented; no approved plan | Add `QW-002` |
| Book-guided, engine-paired self-play with provenance | Not implemented; no approved plan | Add `QW-003` |
| `opening-probe.v1` and safe runtime lookup | Mentioned only as proposed | Add `QW-004` |
| H2H/search-driven active-learning loop | Design-only; no approved spec/plan | Add `QW-005` |
| Faithful observation policy distributions | Current projection sets one selected action to one visit | Add `QW-006` |
| Engine-side checkpoint compatibility/inference | Producer/parser surfaces exist; consumers absent | Add `QW-007` |

## Historical prompt audit

`quantik-ai` is a dirty historical prototype. Useful patterns were explicit
role scope, dependency inputs, output contracts, and quality gates. Outdated or
unsupported assumptions include a fixed six-agent topology, Python/C++ as the
engine architecture, mandatory provider libraries, Redis/SQLAlchemy/FastAPI,
invented throughput/concurrency targets, and a custom agent runtime. The
replacement prompts in `agents/` are capability-based and do not depend on a
model vendor, orchestration product, command tool, or communication transport.

## Result

Only outstanding implementation or required planning work is present in the
active task queue. Completed work remains evidence in this reconciliation and
is not represented as an active task.
