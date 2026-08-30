# QW-013 Status

Created 2026-08-30, during reconciliation. In progress — do not treat as
not-started.

Verified directly 2026-08-30: `src/quantik_models/play/export.py` (128 lines)
and `tests/test_play_export.py` exist in the `quantik-models-py` working tree
and are **untracked** (`git status --porcelain` shows `??` for both), meaning
another session is actively building this right now, separate from this
reconciliation task. The present `export.py` implements `export_queue`,
converts the canonical-key mismatch explicitly (`_known_canonical_keys` builds
a decimal-string set from `ExactCorpus`), and writes via
`arena.pack.write_gzip` — matching the brief's shape.

What is not yet verified: whether the failing-test-first requirement was
honored, whether it has been run end to end against the real
`~/.local/share/quantik/games.db`, and whether `docs/autoplay.md` has gained
the human-games branch the brief's working agreement requires. Not re-verified
here to avoid interfering with in-flight work.

Full charter: [`briefs/play-solver-queue-export.md`](../../../../briefs/play-solver-queue-export.md).

Next action: whoever picks this up should check the current state of
`src/quantik_models/play/export.py` before writing anything — it may already
be substantially finished.
