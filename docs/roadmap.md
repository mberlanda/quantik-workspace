# Roadmap — open work by epic

A high-level view of the planned work and which initiatives support which goal. The grouping into epics is an editorial layer written on 2026-11-02; the manifests under `tasks/active/` remain the source of truth for status. Refresh the numbers with `quantik-workspace task status`, and see the generated [dispatch board](generated/dispatch-board.md) and [dependency graph](generated/task-dependency-graph.md) for dispatchable items.

Status words are the manifest `status`. "Items" counts work items as `done/total`.

## Epic A — Lockstep releases and contract hardening

Goal: contracts, core-py and core-rust ship together, and a normal PR never needs a coordinated four-repo tag. Release ladder: [release-plan](releases/release-plan.md).

| Initiative | What it delivers | Status | Items |
|---|---|---|---|
| QW-015 Release-engineering hardening | Fixture checkout in CI, consistency checks, compatibility matrix | all items done; **open on one decision**: `supported` for 1.4.0 | 9/9 |
| 1.4.0 release (QREL-2026-004) | Tagged on all three repos | **tagged, publish pending**: core-py#51, core-rust#48 | n/a |
| QW-007 Checkpoint consumer compatibility | `model-checkpoint.v1` consumer boundary, runtime choice, numerical parity (ladder 1.6.0) | plan-required | 0/4 |

Outstanding: publish 1.4.0 to PyPI and crates.io; tag-exact portability smoke; reword the contracts changelog "rejected from 1.5.0" line; decompose QW-007 (XL, four repos, the checkpoint surface is the one most likely to break).

## Epic B — Measuring and improving playing strength

Goal: know how strong each model is at every ply, and fix the plies where it is weak.

| Initiative | What it delivers | Status | Items |
|---|---|---|---|
| QW-024 Opening arena from ply zero | Measures the phase a human game starts in; unblocks skill levels | planned | 1/2 |
| QW-026 Patience arena on an independent seed | Confirms or corrects QW-012's cpool-vs-attn result | planned | 1/2 |
| QW-021 Opening coverage expansion | Training data for plies 0 to 6 | planned | 1/7 |
| QW-023 Corpus axis at converged budget | Separates corpus coverage from epoch budget | planned | 0/3 |
| QW-027 Corpus label structure | Audit of corpus contents; fix the thin policy signal and shallow-ply floor | planned | 3/6 |
| QW-028 Finish the opening book solve | Exact solve, written and abandoned twice | not-started, plan-required | 0/1 |
| QW-029 Shallow-ply scoring as a standing metric | Makes the shallow-ply floor a tracked number | plan-required; needs scoping with the user | 0/1 |

Outstanding: QW-024 and QW-026 each have one item left (verify and close); QW-028 is small once QW-021's partition lands; QW-029 has no acceptance criteria yet.

## Epic C — Training pipeline and the feedback loop

Goal: reproducible pipelines first, then search and head-to-head results that feed the next training round.

| Initiative | What it delivers | Status | Items |
|---|---|---|---|
| QW-002 Versioned ML pipeline profiles | One runner with reviewable profiles | planned; W1 design in review | 0/4 |
| QW-006 Search-derived policy targets | Real root policy mass instead of a synthetic selected-action visit | plan-required | 0/2 |
| QW-003 Book-guided self-play runner | Reproducible runner sampling book and frontier openings (ladder 1.7.0) | plan-required | 0/3 |
| QW-005 Active-learning feedback loop | Search and H2H evidence selects positions for the next round (ladder 1.8.0) | plan-required; do not decompose yet | 0/3 |

Dependencies: QW-005 waits on QW-002, QW-003, QW-006 and QW-007. Outstanding: approve QW-002 W1 (the design); QW-006 is the best value-per-effort of the undecomposed set (two items, no cross-language parity).

## Epic D — Public play and serving

Goal: a visitor can play a sensibly-leveled opponent in a browser without cloning anything.

| Initiative | What it delivers | Status | Items |
|---|---|---|---|
| QW-009 Public play deployment | Storeless Docker for the play service and visualizer | planned | 1/2 |
| QW-010 Skill levels and how-to-play | Evidence-based easy/medium/hard mapping and a rules explainer; needs QW-024 | planned | 0/2 |
| QW-011 Puzzle mode in the browser | Picker UI over the shipped puzzle generator | plan-required; needs the visualizer repo added to scope | 0/1 |
| QW-020 Container distribution for the Rust API | Container image; settles Rust API vs Python play service as the public deployment | planned | 4/5 |
| QW-017 ONNX model serving in the Rust API | Policy/value runtime in `quantik-api-rust` (`tract-onnx` vs `ort`) | decision superseded, not started | 0/2 |

Outstanding: the deployment decision (QW-020), CI for api-rust and the visualizer, QW-017's runtime choice settled by loading all four published graphs.

## Epic E — Publication and hygiene

| Initiative | What it delivers | Status | Items |
|---|---|---|---|
| QW-016 Season two article publication | Publish the deadlock article; back up three drafts held on one disk | planned | 0/2 |
| QW-022 Workspace repo hygiene | Remaining hygiene items; one correction kept visible on purpose | partially resolved | 1/2 |

## Open decisions awaiting the user

- QW-002 W1 design approval.
- `0001` Decision review and ADR 0014.
- Whether post-tag portability evidence is enough to set 1.4.0 to `supported`, or the smoke is re-run at the tags.
- Scope for QW-029 and QW-011.
- Dropping the redundant `quantik-api-rust` stash `api-rust-cargolock-2026-11`.

## Recommended order

1. Publish 1.4.0 (hand steps in core-py#51 and core-rust#48), then close QW-015.
2. Close QW-024 and QW-026 (one item each), which unblocks QW-010 (skill levels) and then QW-009.
3. QW-006, then decompose QW-007 and QW-003; QW-005 last.
