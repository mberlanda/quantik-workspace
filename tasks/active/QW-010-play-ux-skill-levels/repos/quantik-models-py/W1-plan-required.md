# W1 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-010-quantik-models-py` (one PR)

## Objective

# quantik-models-py task

Objective: produce a written, numbers-backed skill-level derivation document
(e.g. `docs/skill-levels.md`) mapping easy/medium/hard to specific opponent specs
from `play/opponents.py`'s roster, using seat-balanced win rates only.

Relevant modules: `docs/oracle-benchmark.md`, the lineup tables in
[`WORKSTREAMS.md`](../../../../../docs/history/workstreams-archive.md) §11 / `docs/decisions/0001-architecture-lineup.md`,
`src/quantik_models/play/opponents.py` (the roster this mapping selects from).

Inputs and outputs: reads existing `runs/eval/*/games.json` leaderboards; writes
one markdown document plus (optionally) a small lookup table the play service or
a future UI can read.

Required contracts release: none — no contract is touched.

Constraints: every number cited must be seat-balanced (average of mover and
responder rates, or an explicitly stated single seat), and must cite its source
run directory.

Dependencies: QW-008 (the roster this maps onto).

Commands and focused tests: none required for the research half; if a lookup
table module is added, it needs a focused test asserting every roster opponent
name it references still exists in `opponents.py`.

Expected artifacts: `docs/skill-levels.md` (or equivalent), reviewed.

Completion criteria: the mapping is approved before any `quantik-qfen-visualizer`
UI work references it.

Handoff path: create `tasks/active/QW-010-play-ux-skill-levels/handoffs/` only
once a handoff exists.

## Implementation and scope

**Acceptance criteria 4-6 (how-to-play explainer, advanced toggle over the
full roster) are superseded, not open** — QW-030 (fully shipped, merged
2026-09-07) built exactly this: a collapsible how-to-play drawer cross-
checked against `quantik-core-contracts`' rule text (QW-030 V3), and a mode
chooser with an advanced drawer exposing the full opponent roster (QW-030
V1/V2/D8), vendored into `quantik-models-py`'s `play/app/`. No further work
item needed for those three.

**Criteria 1-3 (the ply-0/1 arena and the numbers-backed skill-level
mapping) remain genuinely open, and are blocked on QW-024** ("The Opening
Arena — Measuring From Ply 0", itself still `plan-required` in this same
pass) — QW-030's own `decisions.md#D4` already made this call explicitly:
"No skill-level ladder ships here... QW-024 is `ready-to-run` and is one
arena run, not a research programme." `allowed_paths` names the eventual
artifact (`docs/skill-levels.md`) and the roster it maps onto
(`play/opponents.py`), but the mapping itself cannot be written — there is
no ply-0/1 arena on disk to source numbers from. `decisions`/`invariants`
stay empty.

Top-level `status` corrected from `not-started` (which was wrong for the
UX half) to reflect both halves' real state.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
