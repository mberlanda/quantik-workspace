# QW-020 Status

**not-started.** No Dockerfile, no image, no publish workflow.

Verified 2026-08-30:

- `quantik-api-rust` is at `f814093` on `main`, in sync with its remote. The long-held
  "no remote" blocker does not exist and never did.
- The repository has four commits and no `.github/workflows/`.

Next action: the base Dockerfile and a GHCR publish workflow. Neither waits on QW-017.

Full history: [`workstreams-archive.md`](../../../docs/history/workstreams-archive.md) §8 and §12.

## 2026-09-20 — W1 in review

W1 is `in-review`: [quantik-api-rust#1](https://github.com/mberlanda/quantik-api-rust/pull/1) adds a
multi-stage `Dockerfile` and `.dockerignore`: static musl build on `rust:1-alpine`, final image
`distroless/static-debian12:nonroot`, listening on `0.0.0.0:8080`. Built and run locally (linux/arm64):
image 10.7 MB, `/health` answered with the pinned `core_revision`, no shell or toolchain, uid 65532.

Tradeoffs recorded:

- **The bundle's "builds standalone" was false.** `Cargo.toml` depends on `quantik-core` by sibling path,
  outside the build context. The builder rewrites that one line to the git rev `CORE_REV`
  (`2b35565d…`, the rev the README documents). The `CORE_REV` build argument must be kept in sync with
  `src/lib.rs` — a follow-up should make one the source of the other. Rejected: widening the build
  context to the workspace root (couples the image to a directory layout the repo does not own) and editing
  `Cargo.toml` (outside `allowed_paths`, and would break local development).
- **Not built `--locked`**: the lockfile's `quantik-core` entry is the path dependency.
- linux/amd64 was not built or tested, and the repository has no CI to run it.

**W1 merged** — [#1](https://github.com/mberlanda/quantik-api-rust/pull/1). The repository has no CI; the local build + `/health` run is the only evidence. W2-W5 are now ready.
