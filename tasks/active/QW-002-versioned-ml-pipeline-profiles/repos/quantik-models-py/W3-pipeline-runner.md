# W3 — One runner, replacing the duplicated tier defaults

**Repository:** `quantik-models-py` · **Branch:** `feat/pipeline-runner` · one PR
**Depends on:** W2 merged. **Dispatch:** mechanical.

One runner executes the stages `docs/pipeline.md` lists, driven by a profile from W2.

## Steps

1. Add the runner to `src/quantik_models/pipeline/`, executing the documented stages in order and
   honouring skips.
2. Record the reproducibility metadata `docs/pipeline.md` specifies for each run, reusing
   `src/quantik_models/train/provenance.py` rather than a parallel mechanism.
3. Migrate `scripts/run_smoke_pipeline.sh` and `scripts/verify_smoke_outputs.py` to call the
   runner with the `smoke` profile. Keep the script entry points and their arguments working —
   they are called from CI and from the README.
4. Apply W1's migration decision for old environment variables exactly: honour-with-warning or
   ignore, whichever `docs/pipeline.md` says. Do not invent a third behaviour.
5. `tests/test_pipeline_runner.py`: the smoke profile runs end to end in the test environment; a
   skipped stage is genuinely skipped (assert on an observable effect, not a log line); the
   recorded metadata names the profile and the resolved overrides.

## Completion criteria

```sh
scripts/run_smoke_pipeline.sh          # still works, unchanged interface
python -m pytest -q
python -m mypy
```

- The smoke pipeline produces the same outputs it did before this change. Compare against a run
  from before your branch and state in the handoff that you did.
- No tier default remains duplicated between a script and a profile: `grep -rn` the env var names
  from W1's inventory and show each now has one home.

## Handoff

Record the before/after smoke outputs comparison and the grep results.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
