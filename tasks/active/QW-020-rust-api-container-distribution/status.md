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

## 2026-09-20 — W2 merged

[api-rust#3](https://github.com/mberlanda/quantik-api-rust/pull/3) adds `.github/workflows/publish-image.yml`:
a `vX.Y.Z` tag push builds `linux/amd64,linux/arm64` and pushes `ghcr.io/<owner>/quantik-api:X.Y.Z` (no `latest`);
`workflow_dispatch` builds without pushing, tagged by sha. The workflow has never run.

- **Precondition for the first release tag:** `workflow_dispatch` only exists once the workflow is on `main`. Run it
  from `main` and confirm the QEMU arm64 build completes before pushing a tag.
- **Risk:** the `gha` cache is ref-scoped, so tag runs start cold. QEMU-emulated arm64 compiling Rust plus bundled
  SQLite C could be very slow; a dispatch run from `main` warms the cache. W3's smoke test builds natively and will not catch this.
- Docker actions are pinned at qemu/buildx/login v3, metadata v5, build-push v6 (no fleet precedent); checkout is v7 like the rest.
- The W2 packet's start revision was stale (`f814093`). W3 and W4 are now ready.
