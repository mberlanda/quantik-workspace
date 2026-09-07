# M5 — Re-sync the app and document the result

**Branch:** `docs/one-port-playground` (last to land)

1. Re-run `scripts/sync_visualizer.py` after V1–V5 have merged. This PR's diff is
   the vendored app plus documentation and nothing else.
2. `README.md` — the "Playing against them" section becomes two commands and no
   caveats. It currently implies a checkout.
3. `docs/play-service.md` — a section on the vendored app: where it comes from,
   that `quantik-qfen-visualizer` is the source of truth, how to serve a live
   checkout with `--static` while working on it, and the new `recording` field on
   `GET /api`.
4. `DEVELOPMENT.md` — add re-running the sync script to the release checklist,
   next to the existing step 6 about the Hugging Face model cards. A release that
   ships a stale app is the failure mode this step prevents.
5. `CHANGELOG.md` — under `## Unreleased`. The version bump is not yours to make.

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

Decision references: `decisions.md#D1`, `decisions.md#D2`, `decisions.md#D3`, `decisions.md#D5`, `decisions.md#D6`.
