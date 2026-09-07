# W1 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-002-quantik-models-py` (one PR)

## Objective

# quantik-models-py task

Objective: design, then implement the canonical pipeline runner and versioned
profiles. Inspect `scripts/run_smoke_pipeline.sh`, training examples, both CI
workflows, materialization, trainer, and output verifier. Preserve existing
commands through documented wrappers or migration notes. Add configuration
validation, override-precedence, stage-selection, and end-to-end smoke tests.
Record the effective profile and exact sibling revisions with every run.

Completion requires an approved plan, focused tests, repository checks, updated
pipeline/scaling docs, and a handoff with exact commands and artifacts.

## Implementation and scope

`allowed_paths` in `manifest.yaml` names the real surface: the existing
runner (`scripts/run_smoke_pipeline.sh`) and verifier
(`scripts/verify_smoke_outputs.py`) to wrap or replace; `data/materialize.py`,
`train/trainer.py` and `train/provenance.py` (already records code/corpus/
hardware/dependency identity per `docs/pipeline.md` — profile identity is the
one axis it doesn't cover yet) as the stages a profile selects between; the
two workflows (`e2e-data-pipeline.yml`, `train-smoke.yml`) that need to call
the same runner CI and local dev use; and a new `src/quantik_models/pipeline/`
module for the profile schema/runner itself, since no such module exists
today (verified — no `profile`/`tier` abstraction anywhere in the tree, only
the scattered env vars and duplicated wrappers `problem` describes).

No `invariants` apply — this is pipeline plumbing, not game-rule or tensor
encoding surface. No `decisions` selected: `decisions.md`'s five questions
(config format, stage mandatoriness, override precedence, revision capture,
legacy-wrapper migration) are genuinely still open, not yet resolved to a
citable heading — that resolution is real design work for whoever picks this
up, not a mechanical field to fill during this pass.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
