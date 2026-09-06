# QW-022 Status

**partially-resolved.**

| item | state (verified 2026-08-30) |
|---|---|
| `e2e-data-pipeline.yml` unpinned `quantik-core-py` checkout | **open** — lines 78-79, no `ref:` |
| `articles` has no remote | **closed, false** (2026-09-06) — `origin git@github.com:mberlanda/quantik-articles.git`, `ls-remote HEAD` == local `HEAD` == `97db37c`, `main` tracking `origin/main` clean |
| `.oracle-worktree/` at the workspace root | **open** — present, unowned |
| `quantik-api-rust` "has no remote" | **closed, false** — in sync at `f814093`, verified three ways |
| `py#9` smoke-checkpoint fixture and `contract_version` fix | closed, merged |
| `quantik-models-py` `main` diverged from `origin/main` | closed, in sync since 2026-08-28 |

Next action: item 1. It is a one-line workflow change plus a recorded reason, and it
removes a class of failure that misattributes breakage to the wrong repository.

Full history: [`workstreams-archive.md`](../../../docs/history/workstreams-archive.md) §12.

## 2026-09-06 — the false-negative recurred, on the other repo

`articles` **has a remote** and did when this table was written. Verified the
three ways this workspace already settled on: `git remote -v`, `git ls-remote
origin HEAD` matching local `HEAD` (`97db37c`), and a clean `main...origin/main`.

This is the *same defect* the row below it records — the `quantik-api-rust`
"has no remote" claim that was false in three documents at once. The correction
was applied to that repo and the identical claim about `articles`, sitting one
row above it in this very table, was left standing. A verified correction to one
instance of a claim is not a correction to the claim.

Both remaining items are still open, re-verified today:

- **`e2e-data-pipeline.yml` unpinned checkout** — `.github/workflows/e2e-data-pipeline.yml`
  still checks out `mberlanda/quantik-core-py` with no `ref:`. Still the next action.
- **`.oracle-worktree/`** — still present at the `quantik-ns` root, still unowned.
