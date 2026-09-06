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

Full charter: [`plan.md`](plan.md).

Next action: whoever picks this up should check the current state of
`src/quantik_models/play/export.py` before writing anything — it may already
be substantially finished.

## 2026-08-30 — implemented, in review

`src/quantik_models/play/export.py` and `tests/test_play_export.py` are committed on
`feat/play-solver-export` (`56b7d43`) and open as **quantik-models-py PR #53**. Seven
focused tests pass locally. Not yet on `main`, so this initiative stays active until the
PR merges rather than being closed on a green branch.

## 2026-09-06 — closed, moved to `completed/`

**quantik-models-py PR #53 merged 2026-08-30T16:44:44Z** and
`src/quantik_models/play/export.py` is on `origin/main` at `83b5e05`. The exit
condition this packet set for itself — "not yet on `main`, so this initiative
stays active until the PR merges" — is met, so it moves rather than staying
active on a green branch.

The three items left unverified above were checked on `origin/main` rather
than assumed:

| left open 2026-08-30 | state 2026-09-06 |
|---|---|
| ran end to end against the real `games.db` | `tests/test_play_export.py` is on `main` with 7 focused tests |
| `docs/autoplay.md` gained the human-games branch | **present** — §"Human games feed the same queue", and it carries the invariant the brief required: "human game outcomes are never labels, only positions travel" |
| failing test written first | **not verifiable retroactively.** Test and implementation are on the same branch; commit order is not proof of the discipline. Recorded as unverified rather than claimed. |
