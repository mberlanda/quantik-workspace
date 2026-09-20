# QW-002 Status

Plan required. The current smoke and training paths are implemented; the
versioned multi-tier runner is not. Pick this task to generate and review the
design and implementation plan first.

## 2026-08-30 reconciliation

Still `plan-required`. Verified: no `profile`, `profiles.py`, or equivalent module
exists anywhere under `quantik-models-py/src/quantik_models/`. `scripts/run_smoke_pipeline.sh`,
`scripts/evaluate_lineup.sh`, `scripts/oracle_benchmark.sh`, and `scripts/stage_hub_repos.sh`
have all grown since this initiative was written — the tier/wrapper sprawl this initiative
describes has gotten larger, not smaller, over the training program (see new initiative
QW-014). Nothing about that sprawl closes this initiative; it is more evidence for it.

Left active, unchanged in substance.

## 2026-09-20 — W1 (design) in review

W1 is `in-review`: [quantik-models-py#70](https://github.com/mberlanda/quantik-models-py/pull/70) rewrites
`docs/pipeline.md` with the profile design (35-variable inventory with file:line, TOML schema with
one-level `extends`, precedence profile -> legacy env -> `--set`, five stages with explicit skip,
legacy env honoured with a warning, `pipeline-run.json` referencing `train/provenance.py`). Every
decision carries its rejected alternatives; the ten calls made without an obvious right answer are
listed at the end of the document.

**Human review gate: W2-W4 do not start until #70 is reviewed and merged.** Start with the
"Decided without an obvious right answer" list.

Findings from the inventory that nobody owns yet:

- `quantik-models-train` (`trainer.py`) never calls `provenance.capture`, so the CI `smoke-checkpoint`
  has no `provenance.json`. The fix is in `trainer.py`, outside every W2-W4 `allowed_paths`; it needs
  its own work item.
- `train-smoke.yml` never runs `verify_smoke_outputs.py`; only `e2e-data-pipeline.yml` does (W4 territory).
- `run_smoke_pipeline.sh` is named "smoke" but its defaults are not; the tiny values live only in the
  workflow `env:` blocks and `examples/train_smoke.sh`.
- The ONNX parity check hard-codes `resnet` and `smoke`.
- Profiles as package data need a `pyproject.toml` edit (`pyproject.toml:134-136`), which is outside
  W2's `allowed_paths` — widen W2 when it is dispatched. `small`/`target` numbers need measuring.
