# quantik-models-py task

Objective: execute [`plan.md`](../plan.md)
exactly as written. Check `src/quantik_models/play/export.py`'s current state
first — an implementation already exists, untracked, as of 2026-08-30 (see
`status.md`); this may be a review-and-finish task rather than a from-scratch
build.

Relevant modules: `src/quantik_models/play/export.py`,
`src/quantik_models/play/store.py` (`distinct_positions`, `connect`),
`src/quantik_models/arena/pack.py` (`merge_qfens` docstring, `write_gzip`),
`src/quantik_models/play/record.py` (`_canonical_key`).

Inputs and outputs: reads `~/.local/share/quantik/games.db`; writes
`to-solve.qfen.gz` and `summary.json` under a chosen output directory.

Required contracts release: `game-result.v1`, unchanged.

Constraints: read-only against the games database; no outcome-derived labels,
not even behind a flag; torch-free (guard any torch import inside a test
function, not at module scope).

Dependencies: QW-008 (the store this reads from).

Commands and focused tests: `python -m quantik_models.play.export --db
~/.local/share/quantik/games.db --corpus runs/oracle/corpus/exact-sampled-v3.npz
--out runs/play/packed --max-ply 6`; `pytest tests/test_play_export.py`.

Expected artifacts: `runs/play/packed/to-solve.qfen.gz`, `runs/play/packed/summary.json`.

Completion criteria: brief's "Verification" section done end to end — exporter
run against the real database, its output accepted by the solver path
unmodified, `data/merge_corpus.py` accepts the solver's output.

Handoff path: create `tasks/active/QW-013-play-store-solver-queue-export/handoffs/`
only once a handoff exists.
