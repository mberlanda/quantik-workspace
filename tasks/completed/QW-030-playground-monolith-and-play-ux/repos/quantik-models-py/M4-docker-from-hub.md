# M4 — Docker builds from the published weights

**Branch:** `chore/docker-from-hub`

`docker/Dockerfile` currently installs `.[serve]` and copies local checkpoints.

- Install `.[serve,hub]`.
- `RUN quantik-models-fetch --all --stage /app/models` in its own layer, with
  `HF_HOME` set to a build-time path so the cache does not bloat the final image.
  Use a build stage if that is what it takes to leave the cache behind.
- Run with `--models /app/models --runtime onnx --no-store`.
- Carry `docker/NOTICE` into the image and reference it from the image labels.
  Weights are CC BY-NC 4.0; the code is MIT. An image that ships weights without
  the notice is the mistake to avoid.
- Re-measure the image size and update the table in `docs/play-service.md`. The
  recorded figures are 441 MB (`best`) and 498 MB (`full`) from local weights —
  state the new number, and do not carry the old one forward as if it still held.

**Do not push anything to GHCR.** Publication is QW-009 criterion 5 and is not in
scope here.

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

Decision references: `decisions.md#O3`.
