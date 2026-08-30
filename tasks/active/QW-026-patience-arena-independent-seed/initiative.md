# QW-026: Re-run the Patience-Lineup Arena on an Independent Seed

> **Purpose:** Confirm — or correct — QW-012's headline result on a seed that
> was never supposed to be reused.
> **Load with:** [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)
> **Depends on:** [`QW-012`](../../completed/QW-012-lineup-under-patience/initiative.md) — reuses its checkpoints, does not retrain them.

## Problem and motivation

[`QW-012`](../../completed/QW-012-lineup-under-patience/status.md) trained all four
architectures under `--patience 5 --epochs 60` and then ran
`scripts/evaluate_lineup.sh` to evaluate them — but the run launched without
overriding `SEED`, so it took the script's default, `20260829`. That is the
exact value QW-012's own `plan.md` said not to reuse ("Use a fresh arena
seed, not `20260829`"), and it had already been spent on a different
comparison, `runs/eval/epoch-test/`. The mistake was caught after the ~3.6h
run finished, not before — see QW-012 `status.md`'s "arena run, but on the
seed this brief said not to use" entry.

The result itself is not neutral. It is the thing QW-012 was built to
answer: `cpool` beats `attn` outright at ply-3 MCTS-128 (66.4% vs 59.9%) and
only trails by 0.8 points at ply-6 — a margin small enough that a
seed-linked artifact is a real candidate explanation, not a remote one. The
whole reason the script's own comment insists on varying the seed is that a
repeated seed makes exactly this kind of bias invisible rather than absent.

## Existing and desired behaviour

Existing: one arena run, `runs/eval/patience-2026-08-30/`, on seed
`20260829`, published with a caveat in three `quantik-models-py` docs and in
QW-012's own status.

Desired: a second arena run, same four checkpoints
(`runs/train/patience-{resnet,mlp,cpool,attn}/best`), same script, on a seed
that has never been used anywhere in this project — training or evaluation —
so the two runs are an honest independent check of each other rather than a
restatement.

## Contracts and repositories

`quantik-models-py` only. No contracts touched, and no new training —
`scripts/evaluate_lineup.sh` against the checkpoints QW-012 already produced.

## Constraints and preserved invariants

- **Do not retrain.** This is an evaluation-only re-run; `runs/train/
  patience-{arch}/best` stay exactly as QW-012 left them.
- **The seed must be genuinely new.** Not `20260827`, `20260828`, `20260901`
  (training seeds), not `20260829` or `20260909` (both spent on prior arena
  runs). `20260830` has not been used as an arena seed and is a reasonable
  default; anything else new is fine too, but state which one and confirm it
  against this list before running.
- **Write both runs' numbers side by side.** The deliverable is a comparison,
  not a second number reported alone — if the two seeds disagree materially
  on the cpool/attn ply-6 margin, that disagreement is the finding.
- **Leave `runs/eval/patience-2026-08-30/` on disk, unmodified**, so the
  first run stays reproducible and comparable.

## Provenance

Raised 2026-08-30, the same session that found the seed reuse while bringing
QW-012's status up to date. Not part of QW-012 itself because QW-012's
training and write-up are otherwise complete — this is a narrower,
independent check that should not block closing it.
