# M2 — `GET /api` says whether there is a store

**Branch:** `feat/api-advertises-recording`

`_API_INDEX` in `play/server.py` is a module-level constant, so it cannot know
whether `db_path` is set. Make the `/api` payload a function of the handler's
`db_path` and add `"recording": <bool>`. Keep every existing key.

**Tests** in the existing server test module: storeless → `recording` is `false`
and `POST /api/games` still answers 503; with a store → `recording` is `true`.
Assert both in the same test file so the pair cannot drift apart.

This unblocks visualizer **V5**. Land it before V5 is reviewed.

## Execution contract

**Read before starting:** repository `AGENTS.md`, `DEVELOPMENT.md` invariants and release checklist. Base dependencies remain numpy + quantik-core; the app adds no dependency. Run `python -m pytest -q` and `python -m mypy` before the PR and report actual results.

**One logical change per commit. One PR for this work item. Do not stack
unrelated changes in one branch.** Each PR must be independently reviewable and
leave `main` green.

- Branches: `feat/…`, `fix/…`, `chore/…`, `docs/…`.
- Commit messages explain **why**, not what — the diff already shows what. A
  subject line under ~72 characters, then a body when the why is not obvious from
  the subject.
- **No commit trailers.** This repository commits as its owner: no
  `Co-Authored-By:`, no `Claude-Session:`. The eight commits behind PR #61 are the
  reference.
- Before opening each PR: `python -m pytest -q` and `python -m mypy`. Both, every
  time, and report the actual counts.

## Scope and handoff

Edit only the manifest allowed paths. Record exact starting and final revisions, branch, PR, commands and results, and dependency evidence in a work-item-specific handoff. Path expansion requires coordinator review.

Decision references: `decisions.md#D6`.
