# W3 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-005-quantik-models-py` (one PR)

## Objective

# quantik-models-py task

Own loop orchestration, iteration manifests, selection, corpus composition,
training, H2H evaluation, and promotion/rejection reports. Prevent train/test
leakage, retain baseline artifacts, and make every input revision and effective
configuration reproducible.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: the existing arena (H2H match/agents/autoplay/pack/probe/registry) and `eval/shift.py` (regression gate) modules, `data/*.py` (corpus composition), and a new `loop/` package for iteration orchestration (nothing like it exists today — verified). depends_on W2. Provisional pending the same cross-repo dependencies as W1.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
