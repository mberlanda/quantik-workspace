# W2 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-006-quantik-models-py` (one PR)

## Objective

# quantik-models-py task

Validate, materialize, weight, and report the improved policy targets. Add tests
for normalization, masks, fallback provenance, malformed distributions, and
baseline comparison. Update training/reporting docs with measured evidence.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `data/materialize.py` and `data/labels.py` (validate/weight the new distribution), `train/supervised.py` (consumes it), `docs/labeling-strategy.md`, `test_materialize.py`. depends_on W1. `decisions`/`invariants` stay empty — same open questions as W1.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
