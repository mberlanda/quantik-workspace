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
