# Task Complexity Assessment

**Date:** 2026-09-07. **Scope:** every initiative in `active/` at the time of writing
(QW-002 through QW-030; QW-001 was already resolved and moved to `completed/`).
**Purpose:** a single read-only pass over each initiative's `manifest.yaml`, rated for
engineering complexity, to use as a proxy for which agent/session a work item is dispatched
to. This is not itself a `work_items` field and the validator does not read it — it is a
standing reference doc, refreshed by re-running the pass, not maintained field-by-field.

## Scale

Rated on scope breadth, cross-repo coordination, and whether a real design/judgment call
is still open — not on wall-clock cost (a long-running solve and a five-minute script edit
can carry the same complexity rating).

| Rating | Meaning |
|---|---|
| S | Mechanical/narrow, single repo, spec fully nailed down. |
| M | Single repo but multi-file, or a genuine (if contained) design/experimental step. |
| L | Multi-repo coordination, or single-repo with a real judgment call. |
| XL | Multi-repo plus an open design decision plus empirical/numerical work — high blast radius if wrong. |

## Assessment

| ID | Title | Repos | Complexity | Why |
|---|---|---|---|---|
| QW-002 | Versioned ML Pipeline Profiles | 1 | M | Single repo, but a real abstraction to design (profile schema, overrides, migration) across pipeline/trainer/CI. No cross-repo coupling. |
| QW-003 | Book-Guided Self-Play Runner | 3 | XL | 3 sequential work items (contracts→rust→py), new opening-book/pairing/provenance semantics, "unsafe canonical-orientation" correctness risk in Rust. |
| QW-004 | Opening Probe Contract and Runtime | 2 | L | 2 sequential items, new compact contract + symmetry-safe Rust abstraction. Contained but real design. |
| QW-005 | Active-Learning Feedback Loop | 3 | XL | Depends on QW-002/003/004/006/007 (all unfinished) — biggest blast radius in the set, full loop design (selection, write-back authority, promotion gates). Do not dispatch until its dependencies land. |
| QW-006 | Search-Derived Policy Targets | 2 | L | 2 sequential items, well-bounded acceptance criteria, but genuine weighting/fallback design plus baseline comparison. |
| QW-007 | Checkpoint Consumer Compatibility | 4 | XL | 4 items, cross-language numerical parity (Python and Rust) to a tolerance, new contract plus capability negotiation. |
| QW-009 | Public Play Deployment (storeless Docker) | 1 | M | Decision already made (ONNX over torch, measured) — mostly implementation: evaluator, Dockerfile, GHCR, parity test. `largely-complete`. |
| QW-010 | Play UX Skill Levels | 1 | M, blocked | Narrow file scope, but the mapping derivation needs judgment (seat-effect control) and is hard-blocked on QW-024. Not dispatchable yet. |
| QW-011 | Puzzle Mode in Browser | 1 as scoped | S, but under-scoped | Generator is already merged; what's actually left (the visualizer picker UI) lives in `quantik-qfen-visualizer`, which is not in `affected_repositories`. Same structural gap pattern as QW-017/QW-023 — needs a work item added before dispatch, the way QW-019's W4 was. |
| QW-015 | Release-Engineering Hardening | 3, 2 done | S | Only the contracts work item (W1) remains; mechanical fix with exact line numbers already cited. |
| QW-016 | Season Two Article Publication | 1 | M | Not code, but a real judgment call (cut to house length vs. publish long) plus a fact-recheck against another repo's line numbers. |
| QW-017 | ONNX Model Serving in Rust API | 2 | XL | Empirical runtime bake-off (tract-onnx vs ort) required "not by argument," a new Cargo-feature-gated subsystem, hash verification, cross-language parity. Blocked on QW-019. |
| QW-018 | Engine Response Type | 2 | L | Design is largely settled by the problem statement already (candidates/PV/certainty); mostly implementation once QW-019's contract lands. |
| QW-019 | Register Phantom Engine Contracts | 4 | L | 4 repos but each item is a narrow, single-file change; the one real decision (OpenAPI vs JSON Schema, prefix fix) is contained. Good candidate to unblock QW-017/QW-018/QW-020. |
| QW-020 | Rust API Container Distribution | 1 | M | Standard multi-arch Docker/CI work, unblocked, spec is fully concrete. |
| QW-021 | Opening Coverage Expansion (plies 0-6) | 1 | XL | High-stakes: a wrong partition design destroys the current held-out probe; large compute; results propagate into published article claims. |
| QW-022 | Workspace Repo Hygiene | 2, 1 done | S | Remaining items are a CI ref-pin decision and a directory cleanup/doc note. |
| QW-023 | Corpus Axis at Converged Budget | 1 | M | Methodology fully specified (epochs/lr/seed given) — execution-heavy, not design-heavy. |
| QW-024 | Opening Arena from Ply 0 | 1 | M | Fully specified methodology; blocks QW-010/QW-030's skill mapping, so worth prioritizing. |
| QW-026 | Patience Arena Independent Seed | 1 | S | Mechanical rerun against a fully specified constraint (seed not in a given exclusion list) plus doc updates. |
| QW-027 | Corpus Label Structure | 1 | L | Single repo, but correctness-sensitive: bit-exact round-trip converter, back-induction with a completeness assertion, independent oracle confirmation. |
| QW-028 | Finish Opening Book Solve | 1 | M | Implementation is small (progress reporting; resume already exists in `exact_oracle`) — wall-clock is hours, agent-complexity is not. |
| QW-029 | Shallow-Ply Standing Metric | 1 | XL, not scopable yet | `problem: "To be refined"`, no real acceptance criteria — needs a scoping pass before any implementation agent, not an implementation dispatch. |
| QW-030 | Playground Monolith and Play UX | 2 | — | All 10 work items already `status: completed`. Not future work — a `task complete QW-030` housekeeping pass is the right next step, not an agent assignment. |

## Dispatch groupings

- **Ready now, low-risk (S/M, unblocked):** QW-002, QW-009, QW-015, QW-016, QW-020,
  QW-022, QW-023, QW-024, QW-026, QW-028.
- **Ready now but design-heavy (L, unblocked):** QW-004, QW-006, QW-018, QW-019, QW-027.
- **High-complexity, unblocked (XL):** QW-003, QW-007, QW-021 — deserve the most capable
  agent plus a human-reviewed plan before code starts, given the correctness/irreversibility
  risk (especially QW-021's train/test partition).
- **Blocked — do not dispatch yet:** QW-005 (needs QW-002/QW-003/QW-004/QW-006/QW-007),
  QW-010 (needs QW-024), QW-017 (needs QW-019), QW-020's `-model` variant (needs QW-017).
- **Needs a scoping/structural fix before any implementation agent:** QW-011 (missing
  visualizer work item), QW-029 (no real problem statement yet).
- **Housekeeping, not a dispatch at all:** QW-030 (already fully done, should move to
  `tasks/completed/`).
