# W2 — Implement profile loading, validation and override precedence

**Repository:** `quantik-models-py` · **Branch:** `feat/pipeline-profiles` · one PR
**Depends on:** W1 merged. **Dispatch:** mechanical — W1 already made every decision.

Implement exactly what `docs/pipeline.md` specifies. If you find yourself choosing, stop: that is
a gap in W1, and it goes back there rather than being decided here.

## Steps

1. Create `src/quantik_models/pipeline/` with the profile dataclass/schema from `docs/pipeline.md`,
   loading and validation. Reject an unknown field loudly — a typo'd profile key that is silently
   ignored is the failure mode this initiative exists to remove.
2. Commit the four profiles (`smoke`, `ci`, `small`, `target`) as data, in the location
   `docs/pipeline.md` names.
3. Implement override resolution in precedence order, as one function with no side effects, so it
   is directly testable.
4. `tests/test_pipeline_profiles.py`:
   - each committed profile loads and validates;
   - an unknown field raises, with the field name in the message;
   - the three-layer precedence example from `docs/pipeline.md` resolves to the documented value —
     assert on that exact worked example;
   - a profile missing a required field raises before any stage runs.

## Completion criteria

```sh
python -m pytest -q tests/test_pipeline_profiles.py
python -m pytest -q
python -m mypy
```

All clean. The precedence test must fail if you swap two layers — verify by actually swapping
them, watching it fail, then restoring.

## Handoff

Record the counts and any place `docs/pipeline.md` was silent.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
