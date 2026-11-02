# W1 — Multi-stage Dockerfile onto a minimal base

**Repository:** `quantik-api-rust` · **Branch:** `feat/dockerfile` · one PR
**Dispatch:** mechanical. **Not blocked on QW-017** — see below.

`quantik-api-rust` ships as source only: no Dockerfile, no image, no CI that builds one. The
section that tracked this carried "the repo has no git remote, nothing for CI to build from" for
weeks; that was false when written — `origin` is `git@github.com:mberlanda/quantik-api-rust.git`
and local `main` was in sync at `f814093`, verified three ways on 2026-08-30.

This initiative's acceptance criterion 3 says the base variant **"is shippable before QW-017 and
should not wait for it"**. That is why this item carries no dependency; only W5 waits.

## Steps

1. `Dockerfile` — multi-stage: build a **static** binary, then copy it onto a distroless or
   scratch base. No toolchain in the final image.
2. The base variant has **no ML dependency**. It builds without the ONNX feature QW-017 introduces.
3. Record the resulting image size in the PR description — the criterion asks for it, and it is the
   number that tells you whether the base was chosen correctly.
4. `EXPOSE` the API port and set a sensible default `CMD`. No secrets, no build args carrying
   credentials.

## Completion criteria

```sh
docker build -t quantik-api:dev .
docker images quantik-api:dev --format '{{.Size}}'
docker run --rm -d -p 8080:8080 --name quantik-api-dev quantik-api:dev
curl -fsS localhost:8080/health
docker rm -f quantik-api-dev
```

- The build succeeds and `/health` answers.
- The image size is recorded.
- The final stage contains no build toolchain — show it (`docker history`, or the Dockerfile's
  final stage read back).

## Handoff

Record the image size and the `/health` transcript.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
