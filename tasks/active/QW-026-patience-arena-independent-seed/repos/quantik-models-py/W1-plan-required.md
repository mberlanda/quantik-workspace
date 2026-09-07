# W1 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-026-quantik-models-py` (one PR)

## Objective

# quantik-models-py task

Objective: re-run the arena/shift evaluation `scripts/evaluate_lineup.sh` was
supposed to run on a fresh seed the first time, and report both results
together.

Relevant modules: `scripts/evaluate_lineup.sh` (the `SEED` variable, defaults
to `20260829` — override it), `src/quantik_models/eval/shift.py`,
`src/quantik_models/arena/`.

Inputs and outputs: reads `runs/train/patience-{resnet,mlp,cpool,attn}/best`
(already on disk, produced by QW-012 — do not retrain); writes a new
`runs/eval/patience-<date>-seed2/`, leaving `runs/eval/patience-2026-08-30/`
untouched.

Required contracts release: none.

Constraints: seed must not be `20260827`, `20260828`, `20260829`, `20260901`
or `20260909` (see `manifest.yaml`). No training. No modification of the
first run's output directory.

Dependencies: QW-012 (checkpoints and first-run numbers to compare against).

Commands and focused tests: smoke first —
`GAMES=2 SEED=<chosen> scripts/evaluate_lineup.sh /tmp/smoke-seed2 ...` — then
the full run at the script's default `GAMES=300`.

Expected artifacts: `runs/eval/patience-<date>-seed2/`, an updated seed-caveat
paragraph (or its removal, if the result is confirmed) in
`docs/decisions/0001-architecture-lineup.md`, `docs/shift-evaluation.md`,
`docs/autoplay.md`.

Completion criteria: the write-up states directly whether the ply-6 MCTS-128
`cpool`-vs-`attn` margin (0.8 points on the first seed) holds its sign and
rough magnitude on the second seed, and whether the ply-3 result (6.5 points,
`cpool` ahead) does too.

Handoff path: create `handoffs/` only once a handoff exists.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `evaluate_lineup.sh` (the `SEED` default to override), `eval/shift.py` and `arena/*.py` (the evaluation code path), and the three docs criterion 4 names — all confirmed to exist at these exact paths. `runs/train/patience-*/best` are read-only inputs; the first run's output directory (`runs/eval/patience-2026-08-30/`) must not be touched, per decisions.md#2. Closing QW-012's own `status.md`/`manifest.yaml` (criterion 5) happens in `quantik-workspace`, outside this item's `allowed_paths` — that's workspace bookkeeping, not implementation surface, same as every other initiative's handoff writing. decisions/invariants stay empty: decisions.md's three points are already resolved as unheaded prose.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
