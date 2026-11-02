# W1 — Publish the play image to GHCR

**Repository:** `quantik-models-py` · **Branch:** `feat/publish-image-workflow` · one PR
**Dispatch:** mechanical.

**Most of QW-009 is already built. Do not rebuild it.** Verified 2026-09-07:

- `OnnxEvaluator` exists at `src/quantik_models/selfplay/evaluator.py:81`, implementing the
  `Evaluator` protocol's `(boards, legal) -> (priors, values)` with `onnxruntime` and numpy only.
- The torch-vs-ONNX agreement test exists at `tests/test_onnx_evaluator_agreement.py`
  (`test_onnx_and_torch_evaluators_agree_on_a_real_checkpoint`), against a real checkpoint.
- `docker/Dockerfile` and `docker/NOTICE` exist and already pull weights from the Hugging Face
  Hub at build time and carry the MIT-code / CC-BY-NC-4.0-weights split (delivered by QW-030 M4).
- `scripts/build_docker_image.sh` exists.

What is missing is the publication step: there is no `.github/workflows/publish-image.yml`.

## Steps

1. `.github/workflows/publish-image.yml` — build `docker/Dockerfile` and push to **GHCR**
   (`ghcr.io/mberlanda/quantik-models-play`), not Docker Hub. The rate-limit rationale is already
   recorded; do not reopen it.
2. Trigger on published releases and on `workflow_dispatch`. Do **not** publish on every push to
   `main`: the image pulls CC-BY-NC-4.0 weights at build time, so every build republishes weights.
3. Authenticate with the built-in `GITHUB_TOKEN` and `permissions: packages: write`. Add no new
   secrets.
4. Tag the image with the release tag and `latest`. Read `.github/workflows/publish.yml` first
   and match its conventions — that workflow already publishes this repository's package.
5. Reuse `scripts/build_docker_image.sh` rather than duplicating its `docker build` line, so the
   local and CI builds cannot drift.
6. Add a `docs/play-service.md` subsection naming the image, its tags, and the licence split a
   consumer is accepting.

## Completion criteria

```sh
python -m pytest -q
python -m mypy
```

- Both clean.
- The workflow is valid YAML and its job graph is what you intend — verify with
  `gh workflow view publish-image.yml` **or**, if it is not yet on the default branch,
  `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/publish-image.yml'))"`.
- The workflow does **not** trigger on push-to-main. Confirm by reading the `on:` block back.
- `docs/play-service.md` names the image and both licences.

Do not run the publish workflow as part of this item. Publishing an image is a release action and
belongs to whoever cuts the release.

## Handoff

Record the workflow's triggers, the image name and tags, and the pytest/mypy counts.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions
win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
