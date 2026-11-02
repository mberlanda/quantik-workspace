# W2 — Publish multi-arch images to GHCR on tag

**Repository:** `quantik-api-rust` · **Branch:** `ci/publish-image` · one PR
**Depends on:** W1 merged. **Dispatch:** mechanical.

## Steps

1. `.github/workflows/publish-image.yml` — build and push to `ghcr.io` **on tag only**, not on
   every push to `main`.
2. **Multi-arch via buildx: `linux/amd64` and `linux/arm64`.** arm64 is not optional — local
   development is arm64, and an amd64-only image is one a developer cannot run.
3. Authenticate with the built-in `GITHUB_TOKEN` and `permissions: packages: write`. No new secrets.
4. Tag as `quantik-api:X.Y.Z` from the git tag. Leave `latest` policy to whoever cuts releases and
   say what you chose in the PR description.
5. Do not run the workflow as part of this item. Publishing is a release action.

## Completion criteria

- Valid YAML:
  `python -c "import yaml; yaml.safe_load(open('.github/workflows/publish-image.yml'))"`
- The `platforms:` line names both architectures — read it back and confirm.
- The trigger is tag-only; confirm by reading the `on:` block back.
- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings` and `cargo test` still clean.

## Handoff

Record the triggers, platforms, and image naming.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
