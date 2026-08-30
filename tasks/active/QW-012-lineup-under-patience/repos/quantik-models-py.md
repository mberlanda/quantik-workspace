# quantik-models-py task

Objective: execute [`briefs/lineup-under-patience.md`](../../../../../briefs/lineup-under-patience.md)
exactly as written — that document is the repository task; this file is a
pointer to it plus the one correction in `decisions.md`.

Relevant modules: `src/quantik_models/train/supervised.py` (`--patience`),
`scripts/evaluate_lineup.sh`, `src/quantik_models/registry.py`
(`ArchitectureEntry.default_lr`).

Inputs and outputs: reads `runs/oracle/corpus/exact-sampled.npz` (the lineup's
corpus — not v2/v3, see `decisions.md`); writes
`runs/train/patience-{resnet,mlp,cpool,attn}/` and a fresh
`runs/eval/patience-<date>/`.

Required contracts release: none — no contract is touched.

Constraints: `--patience` stays off by default; fixed-budget checkpoints and
`runs/eval/swept-2026-08-30/` are not modified; a fresh arena seed, not
`20260829` or any training seed.

Dependencies: none blocking — QW-014 records the methodology this continues,
but this initiative's work does not require QW-014 to be re-touched.

Commands and focused tests: see the brief's "Smoke test before any long run"
and "Re-run the whole evaluation" sections verbatim.

Expected artifacts: four new checkpoints, one new evaluation directory, updated
`docs/decisions/0001-architecture-lineup.md`, `WORKSTREAMS.md` §11,
`docs/shift-evaluation.md`, `docs/autoplay.md`.

Completion criteria: the brief's step 4 report answers, explicitly, whether the
cpool/attn tie survives.

Handoff path: create `tasks/active/QW-012-lineup-under-patience/handoffs/` only
once a handoff exists.
