# W1 — quantik-api-rust

Repository: `quantik-api-rust`
Branch: `plan/qw-020-quantik-api-rust` (one PR)

## Objective

# quantik-api-rust

## Objective

A multi-stage Dockerfile and a GHCR publish workflow, multi-arch, with a
container-level smoke test.

## Inputs

- `Cargo.toml`, `Cargo.lock` — dependencies are already locked (`8cc75f8`, "Lock
  deployable service dependencies").
- `src/lib.rs` — the engine dispatch the smoke test exercises.

## Approach

1. Multi-stage build; final stage distroless or scratch. Record the image size.
2. `buildx` for `linux/amd64` and `linux/arm64`.
3. Publish to `ghcr.io` on tag.
4. Smoke test **against the running container**, not the binary: one request per engine
   kind, asserting a legal move. A test that runs `cargo test` inside CI does not tell
   you the image works.
5. Add the `-model` variant once QW-017 lands, gated on the Cargo feature.

## Completion criteria

- A tag produces two architectures of `ghcr.io/mberlanda/quantik-api:X.Y.Z`.
- The smoke test runs against the pulled image in CI.
- The image size is recorded in the handoff, for both variants once both exist.
- Handoff records the decision made for criterion 4.

## Implementation and scope

Not yet planned. Replace this item's placeholder `allowed_paths` in `manifest.yaml` with explicit repository-relative paths, select the `decisions`/`invariants` references it actually needs, and split into further work items wherever another branch/PR is needed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
