# W5 — The `-model` image variant

**Repository:** `quantik-api-rust` · **Branch:** `feat/model-image-variant` · one PR
**Blocked on:** **QW-017** (ONNX model serving) landed, and W2 merged. **Dispatch:** mechanical.

This is the only item in this initiative that waits for QW-017. The base image (W1/W2) ships first,
deliberately — see acceptance criterion 3.

## Steps

1. Extend `Dockerfile` with a variant building the ONNX-enabled binary behind the Cargo feature
   QW-017 introduces. Keep the base variant unchanged and still ML-free.
2. Publish it as `quantik-api:X.Y.Z-model` alongside `quantik-api:X.Y.Z`, same multi-arch matrix.
3. Record both image sizes side by side. The gap is the cost of ML serving and is worth knowing.
4. Extend W3's container smoke to cover the model engine in the `-model` image only.

## Completion criteria

- Both variants build; both sizes recorded together.
- The base image still contains no ML dependency — verify and show it.
- The `-model` smoke covers the model engine; the base image's smoke is unchanged.
- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test` clean.

## Handoff

Record both sizes and the base-image ML-free check.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
