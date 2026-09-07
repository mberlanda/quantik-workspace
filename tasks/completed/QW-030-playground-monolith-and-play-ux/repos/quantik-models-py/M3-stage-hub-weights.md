# M3 — Stage Hub weights into a directory

**Branch:** `feat/fetch-stage`

`play.registry.scan_models` scans a directory of checkpoints. `hub` fetches into
the Hugging Face cache. Nothing bridges them, which is why the Docker image bakes
in `runs/train/*/best`.

Add `--stage <dir>` to `quantik-models-fetch` (and a `stage()` function beside
`prefetch()` in `hub.py`): for each requested model, resolve it, then materialize
`<dir>/<short-name>/` from the snapshot so that `--models <dir>` picks it up
unchanged. Symlink if the platform allows and copy otherwise — a Docker layer
needs real files, so make the copy path the one that is tested.

**Tests:** a staged directory satisfies `scan_models` and yields `status ==
"ready"`; the staged name matches the short name, not the Hub repo id; staging
twice is idempotent. Use the existing Hub test doubles — **do not hit the network
in tests.**

Note the naming trap: `export.huggingface.stage` renames `weights.safetensors` to
`model.safetensors` on the way to the Hub, and `arena.registry` reads both. A
staged directory must keep whichever name the snapshot has.

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

Decision references: none.
