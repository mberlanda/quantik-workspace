# Models and Data Agent

Apply `operating-contract.md`.

## Scope

`quantik-models-py` only: data materialization/dataset/labels, model spec/network,
trainer, arena/autoplay, the play service, checkpoint export/evaluation. Engine rules,
contracts, and the visualizer are out of scope even when a task motivates a change
there — file a handoff instead of reaching across.

## Inputs

Models packet, contracted dataset/action/tensor/value rules, repository task, exact
starting revision, and — for any torch-touching change — which install profile
(`[dev]`, `[dev,arrow]`, `[dev,arrow,torch,onnx,viz]`) it must keep importing under.

## Outputs

Readers/materializers/model/checkpoint changes, focused tests, and handoff evidence
that states tensor shapes/dtypes/channels, action indexing/remapping, mask semantics,
value perspective, and the exact dataset/checkpoint revisions touched.

## Permissions

`quantik-models-py` only. No sibling or remote writes. Preserve pre-existing dirty work
under `runs/` and elsewhere rather than cleaning it up unasked.

## Prohibited

- Implicit tensor/action/value assumptions — state shape, indexing, and perspective
  explicitly every time; see the mover-relative/colour-ordered ambiguity below.
- A bare `import torch` at test-file scope — it fails *collection* for the whole file
  rather than skipping. Use `pytest.importorskip("torch")`, module-scope when every test
  needs it, function-scope when only some do.
- Treating a human game's outcome as a label. Only positions travel to the corpus;
  labels come only from the exact oracle (`data.exact_corpus`, `data.merge_corpus`) —
  for autoplay and human play alike.
- Inheriting a hyperparameter (learning rate, epoch budget) from another architecture's
  run and reporting the result as architecture-neutral. A shared *protocol* (same grid,
  same budget, best result enters the comparison) is fine; a shared *value* is not — it
  produced three false published conclusions once already.
- Planning a training run around a timing taken while the machine was under load.

## Verification

```
.venv/bin/python -m pytest -q                       # full suite
.venv/bin/python -m pytest -q -k <focused>           # focused change
.venv/bin/python -m quantik_models.train.preflight …  # projected wall-clock before a long run
```

`mypy` is declared in `[dev]` but wired into no script or CI job — available, not a
gate; never report it as passing unless it was actually run. `[dev,arrow]` (no torch) is
a CI-tested configuration (`e2e-data-pipeline.yml`): `env`, `selfplay`, `arena`, `play`
and `data` must stay importable with torch blocked; only `model/*` and `train/*` may
import it at module scope, everywhere else lazily inside the function that needs it
(`arena.registry.load_evaluator` is the pattern to copy). `tests.yml` fails the run if
any test skips with "could not import" against the full extra set — a skip there is a
missing dependency, not a legitimate pass.

## Failure modes specific to this repo

- **Two encodings share the contract name `tensor-board.v1`.** `fastboard.encode_tensors`
  is mover-relative and is what training actually uses; `quantik_core.ml_data.qfen_to_tensor`
  and `fastboard.to_core_tensor` are colour-ordered and used by nothing here. Building or
  reviewing against the wrong one gives a model that plays legally and confidently wrong
  on half of all positions, with no error raised anywhere.
- **A timing taken under load is an upper bound, not a budget** — solver cost alone
  varies roughly 7x per ply; re-measure on a quiet machine before sizing a run.
- **Held-out policy accuracy has failed to predict play strength four separate times.**
  When validation top-1 and the arena disagree, report both and say so plainly; do not
  resolve the disagreement by preferring the more favorable number.
- **The seat effect (roughly 68–88% mover win rate) dwarfs any model difference.** An
  unbalanced win rate is not evidence of anything; always report seat-balanced results.

> **Load with:** [`../context/repositories/quantik-models-py.md`](../context/repositories/quantik-models-py.md) · [`../context/system/canonical-invariants.md`](../context/system/canonical-invariants.md) · [`../context/system/release-model.md`](../context/system/release-model.md)
