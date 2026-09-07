# W1 — Design the profile schema and write it down

**Repository:** `quantik-models-py` · **Branch:** `docs/pipeline-profile-design` · one PR
**Dispatch:** judgment — capable model, human review before W2 starts.

Run tiers are assembled from scattered environment variables and duplicated wrappers. This item
decides what replaces them. **It writes no runner and no package** — it produces the design the
next three items implement, and it is the only item in this initiative with an open question in it.

There is no `src/quantik_models/pipeline/` package today. Read `scripts/run_smoke_pipeline.sh`,
`scripts/verify_smoke_outputs.py`, `scripts/run_patience_lineup.sh`, `src/quantik_models/train/provenance.py`
and both pipeline workflows (`.github/workflows/e2e-data-pipeline.yml`, `train-smoke.yml`) and
inventory **every** environment variable and duplicated default they carry today. That inventory
is the input to the design; a schema that cannot express something the scripts do today is a
regression.

## Decide and record, in `docs/pipeline.md`

1. **Profile schema.** Field names, types, required vs optional, and what a profile is *not*
   allowed to contain. Four profiles must be expressible: `smoke`, `ci`, `small`, `target`.
2. **Override precedence.** The exact order — committed profile, then what? Environment variable,
   CLI flag, both? State the order and one worked example resolving a conflict between all layers.
   This is the part that produces silent wrong runs when it is vague.
3. **Stages.** The stage list and their order: data generation, materialization, optional
   training, evaluation, verification. Which are skippable, and how a profile expresses that.
4. **Migration.** Which existing env var maps to which profile field, and what happens to a
   caller still setting the old variable — honoured with a warning, or ignored? Say which.
5. **Reproducibility metadata.** What each run records so a result can be traced back to the
   exact profile and overrides that produced it. Relate it to what `train/provenance.py` already
   records; do not duplicate that mechanism.

## Completion criteria

- `docs/pipeline.md` contains all five sections above, each with a decision, not options.
- The env-var inventory is in the document, and every entry has a stated destination.
- One worked override-precedence example resolving a three-layer conflict.
- No code changes: `git diff --stat` touches `docs/pipeline.md` only.

## Handoff

Record the inventory count and any question you had to decide without an obvious right answer, so
review can focus there.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
