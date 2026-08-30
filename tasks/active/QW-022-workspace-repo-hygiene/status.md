# QW-022 Status

**partially-resolved.**

| item | state (verified 2026-08-30) |
|---|---|
| `e2e-data-pipeline.yml` unpinned `quantik-core-py` checkout | **open** — lines 78-79, no `ref:` |
| `articles` has no remote | **open** — `git remote -v` empty at `7d8b75b` |
| `.oracle-worktree/` at the workspace root | **open** — present, unowned |
| `quantik-api-rust` "has no remote" | **closed, false** — in sync at `f814093`, verified three ways |
| `py#9` smoke-checkpoint fixture and `contract_version` fix | closed, merged |
| `quantik-models-py` `main` diverged from `origin/main` | closed, in sync since 2026-08-28 |

Next action: item 1. It is a one-line workflow change plus a recorded reason, and it
removes a class of failure that misattributes breakage to the wrong repository.

Full history: [`workstreams-archive.md`](../../../docs/history/workstreams-archive.md) §12.
