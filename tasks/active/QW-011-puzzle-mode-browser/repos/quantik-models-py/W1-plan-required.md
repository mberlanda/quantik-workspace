# W1 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-011-quantik-models-py` (one PR)

## Objective

# quantik-models-py task

Objective: generate a puzzle pack from the current best corpus and hand it off
in a form `quantik-qfen-visualizer` can commit and consume directly (static
JSON, no further transformation needed).

Relevant modules: `src/quantik_models/play/puzzles.py`,
`tests/test_play_puzzles.py`.

Inputs and outputs: reads an `ExactCorpus` (`exact-sampled-v3` unless superseded);
writes one JSON pack file.

Required contracts release: none — the pack format is not a registered contract.

Constraints: `already-lost` entries must not carry a `solutions` field;
`double-threat` verification must go through the second code path the existing
tests already exercise, not be re-derived.

Dependencies: none beyond an existing exact corpus on disk.

Commands and focused tests: `python -m quantik_models.play.puzzles --per-theme 40
--corpus <path> --out <pack.json>`; `pytest tests/test_play_puzzles.py`.

Expected artifacts: one generated pack file, handed to the visualizer to commit.

Completion criteria: pack generated, spot-checked (a `mate-in-1` and a
`double-threat` instance solved by hand against `solutions`), and handed off.

Handoff path: create `tasks/active/QW-011-puzzle-mode-browser/handoffs/` only
once a handoff exists.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `play/puzzles.py` (the generator, already merged as models-py#51 per `problem`) and its test file — the picker UI itself lives in `quantik-qfen-visualizer`, not a formal `affected_repositories` entry (decisions.md#4). `decisions`/`invariants` stay empty: decisions.md's three questions (which corpus, grouping, already-lost presentation) are open.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
