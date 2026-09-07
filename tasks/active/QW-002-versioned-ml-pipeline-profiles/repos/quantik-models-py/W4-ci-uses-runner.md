# W4 — CI uses the same runner

**Repository:** `quantik-models-py` · **Branch:** `ci/pipeline-profiles` · one PR
**Depends on:** W3 merged. **Dispatch:** mechanical.

`.github/workflows/e2e-data-pipeline.yml` and `.github/workflows/train-smoke.yml` assemble tiers
from inline environment variables. Point them at the runner and the committed profiles instead, so
local and CI runs cannot drift.

## Steps

1. `.github/workflows/e2e-data-pipeline.yml` — invoke the runner with the `ci` profile. Delete the
   inline tier variables that the profile now owns; keep anything genuinely CI-specific (paths,
   caching, runner selection).
2. `.github/workflows/train-smoke.yml` — same, with the profile `docs/pipeline.md` assigns it.
3. Do not change what CI *asserts*. This item changes how the run is configured, not what counts
   as passing. If a check has to change to keep passing, that is a finding for the handoff, not a
   silent edit.

## Completion criteria

- Both workflows are valid YAML:
  `python -c "import yaml; [yaml.safe_load(open(p)) for p in ['.github/workflows/e2e-data-pipeline.yml','.github/workflows/train-smoke.yml']]"`
- No environment variable that a profile now owns remains set inline in either workflow.
- `python -m pytest -q` and `python -m mypy` clean.
- The PR description lists every deleted variable and the profile field that replaced it.

## Handoff

Record the deleted variables and whether any assertion had to move.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
