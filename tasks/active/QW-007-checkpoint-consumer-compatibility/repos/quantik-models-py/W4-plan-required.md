# W4 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-007-quantik-models-py` (one PR)

## Objective

# quantik-models-py task

Provide deterministic reference checkpoints/inputs/outputs and export any
additional compatible representation approved by the design. Do not change the
canonical format without migration evidence. Record model config, weights hash,
environment, tolerance, and exact reference outputs.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `export/checkpoint.py` (the existing checkpoint writer, source of the reference artifacts), the committed 80 KB smoke checkpoint fixture (`tests/fixtures/checkpoints/smoke-best`), and `docs/models.md`. depends_on W1.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
