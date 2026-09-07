# Release Roadmap — Core and Models, 2026-09

Forward-looking envisioning, not a release-train record. It groups the initiatives in
`tasks/active/` into candidate release cuts for `quantik-core-rust`, `quantik-core-py`
(lockstep with `quantik-core-contracts`, the producer) and `quantik-models-py` (versioned
independently), using each initiative's `complexity`, `dependencies`, and
`affected_repositories` fields. Creating an actual release train (`QREL-NNNN-NNN`) still
goes through `quantik-workspace release plan` per `docs/releases/release-policy.md`, when a
repository maintainer is ready to commit to a candidate — nothing here is that commitment.

## State observed (from git tags, not from `releases/active/`)

| Repository | Latest tag | What it shipped |
|---|---|---|
| `quantik-core-contracts` | `v1.3.1` | v1.3.0: QW-001's canonicalization group, action-index remap, invalid-state boundaries. v1.3.1: fixed an `opening-book-consistency` release deadlock. |
| `quantik-core-rust` | `v1.3.0` | QW-001's action-index remap contract and Python validation-boundary parity. |
| `quantik-core-py` | `v1.3.0` | Same QW-001 contract; `SUPPORTED_CONTRACTS_RELEASE` bumped, consumes contracts `v1.3.1`'s action. |
| `quantik-models-py` | `v1.1.0` | QW-030: `quantik-models-play` serves the board and the API on one port, no sibling checkout — released today. |

**`releases/active/QREL-2026-001/release.yaml` and `docs/generated/release-status.md` still
describe a `planned` v1.2.0 cut** (contracts producer, three pending consumers). All three
core repos are two patch/minor releases past that now. This is the same staleness pattern
as `tasks/active/QW-030` (manifest `status: planned`, work actually shipped) — a tracking
record, not the underlying work, is out of date. Reconciling it (retire QREL-2026-001,
open its successor at the real state, or fold the check into QW-015's remaining contracts
work item) is a release-engineering task in its own right and is not attempted here.

## Core trio: candidate next cut

QW-001 landing in v1.3.0 unblocks four initiatives that all listed it as their only
dependency (all `plan-required`, none started):

| ID | Complexity | Repos | What it adds |
|---|---|---|---|
| QW-004 | L | contracts, rust | Opening-probe contract and a symmetry-safe runtime abstraction. |
| QW-006 | L | rust, models-py | Search-derived observation policy targets (weighting/fallback design). |
| QW-003 | XL | contracts, rust, models-py | Book-guided self-play runner — new opening-book/pairing/provenance semantics, canonical-orientation correctness risk. |
| QW-007 | XL | contracts, py, rust, models-py | Checkpoint consumer compatibility — cross-language numerical parity to a tolerance, capability negotiation. |

Proposed **v1.4.0 wave 1**: QW-004 + QW-006. Both are `L`, contained to a single new
contract/abstraction each, and neither depends on the other — they can land in parallel
and close out a cut without touching the two `XL` items. Proposed **v1.5.0 wave 2**:
QW-003 + QW-007, each reviewed and planned on its own given the correctness risk flagged
in `tasks/complexity-assessment.md`. QW-005 (active-learning feedback loop, `XL`,
depends on all four) is the earliest a v1.6.0-class cut becomes conceivable — do not plan
its release before wave 2 is actually merged, per its manifest's own dependency list.

QW-015 (release-engineering hardening, `S`, only its contracts work item remains) and
QW-022's CI ref-pin item are good candidates to land *inside* wave 1 rather than as their
own cut — they are exactly the kind of drift wave 1's reconciliation would otherwise
leave for later.

## `quantik-models-py`: candidate next cut

v1.1.0 shipped QW-030 (the vendored-app monolith) today. Two independent themes are ready
to follow it, and there's no dependency forcing them into the same cut:

**Public-deployment/UX wave (v1.2.0 candidate).** QW-009 (`M`, largely-complete —
storeless Docker deployment) has the least left to do. QW-024 (`M`, fully specified
ply-0/ply-1 arena) is worth prioritizing on its own merits: it's what QW-010's skill-level
mapping and QW-030's deferred skill ladder are both blocked on (QW-010's `dependencies` was
missing that edge until this pass added it — see `task-dependency-graph.md`). Landing
QW-024 then QW-010 completes the "easy/medium/hard, not `cpool@128`" UX promise QW-030's
acceptance criteria explicitly deferred.

**Corpus/training-foundation wave (independent of the above).** QW-023 (`M`, converged
corpus axis), QW-021 (`XL`, opening coverage plies 0-6 — high-stakes partition design,
plan this one first and separately), QW-028 (`M`, finish the opening-book solve — depends
on QW-021's partition landing before its `.npz` can be merged into any corpus), and QW-027
(`L`, corpus label structure and the shallow-ply floor). These change what the *next
trained checkpoint* looks like, not what the package ships; group them under whichever
checkpoint-publishing release actually consumes the resulting corpus, not necessarily
v1.2.0 itself.

QW-002 (`M`, versioned ML pipeline profiles) is orthogonal internal tooling with no
dependents in either wave — fits either cut, or ships standalone whenever it's done.

QW-011 and QW-029 are excluded from both waves until their scoping gaps (noted in
`tasks/complexity-assessment.md`) are closed — an under-scoped item shouldn't anchor a
release plan.
