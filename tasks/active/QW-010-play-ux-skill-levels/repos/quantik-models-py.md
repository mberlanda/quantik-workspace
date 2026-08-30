# quantik-models-py task

Objective: produce a written, numbers-backed skill-level derivation document
(e.g. `docs/skill-levels.md`) mapping easy/medium/hard to specific opponent specs
from `play/opponents.py`'s roster, using seat-balanced win rates only.

Relevant modules: `docs/oracle-benchmark.md`, the lineup tables in
`WORKSTREAMS.md` §11 / `docs/decisions/0001-architecture-lineup.md`,
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
