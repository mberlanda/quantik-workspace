# Task Complexity Assessment

**Purpose:** rate each initiative's engineering complexity, to use as a proxy for which
agent/session a work item is dispatched to.

**Where the data lives.** The rating and a one-line rationale are fields on the initiative
itself — `complexity` and `complexity_notes` in each `tasks/active/<QW-ID>/manifest.yaml` —
not in this file. That is the single source of truth; `task validate` covers it like any
other manifest field. This file is the scale definition plus the curated read that doesn't
belong on any one manifest.

**See the current ratings, alongside status and the dependency graph, in
[`../docs/generated/task-dependency-graph.md`](../docs/generated/task-dependency-graph.md)**
(Mermaid diagram plus an adjacency table) — generated from every manifest by
`quantik-workspace reports generate` and checked for staleness by
`quantik-workspace validate generated`, so it never drifts from what's on disk. Grep the
table for a quick per-initiative complexity/state lookup; render the diagram for the shape
of what blocks what.

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

Rate a new initiative by adding `complexity`/`complexity_notes` to its manifest (both are
optional properties in `schemas/initiative.schema.json`) — not by editing this file.

## Curated reads, not derivable from the graph alone

These are judgment calls on top of the raw graph/complexity data, current as of the last
time someone re-read every manifest (2026-09-07). Re-derive rather than trust blindly once
initiatives move.

- **Structurally under-scoped — fix before dispatch, not during it:** QW-011 (the remaining
  work is a `quantik-qfen-visualizer` picker UI, but that repo isn't in
  `affected_repositories` — same gap pattern QW-019's W4 fixed for QW-017/QW-018/QW-020),
  QW-029 (`problem: "To be refined."`, no real acceptance criteria yet).
- **High-complexity and unblocked — worth a human-reviewed plan before code starts, given
  correctness/irreversibility risk:** QW-003, QW-007 (cross-language parity, new
  contracts), QW-021 (a wrong train/test partition destroys the current held-out probe and
  the result feeds published article claims).
- **Where each initiative is headed:** [`../docs/releases/release-plan.md`](../docs/releases/release-plan.md)
  maps every initiative on this page to the release version it gates, across all five
  repositories that cut releases.
