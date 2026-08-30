# quantik-models-py task

Objective: none pending — this packet documents completed work. If picked up,
the only in-scope action is keeping the citations below current as QW-012 and
QW-013 land, not re-running or re-deriving any part of the program.

Relevant modules: `src/quantik_models/model/` (registry, architectures),
`src/quantik_models/train/supervised.py`, `src/quantik_models/eval/shift.py`,
`src/quantik_models/arena/{autoplay,pack,probe}.py`,
`src/quantik_models/data/merge_corpus.py`, `src/quantik_models/export/huggingface.py`.

Inputs and outputs: none new — reads the existing `runs/` tree.

Required contracts release: `model-checkpoint.v1`, `observation.v1`, unchanged.

Constraints: do not restate numbers from `docs/*.md` here; link to them. Do not
re-run any part of the lineup or corpus chain under this packet — that is
QW-012's and QW-013's scope respectively.

Dependencies: none.

Commands and focused tests: none — no code change is in scope for this packet
as recorded.

Expected artifacts: none new.

Completion criteria: already met — this task exists to record, not to
implement. Close it if a future reconciliation finds nothing further to link.

Handoff path: none — no `handoffs/` directory needed unless this packet's scope
changes.
