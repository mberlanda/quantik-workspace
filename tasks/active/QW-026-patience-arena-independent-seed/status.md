# QW-026 Status

Created 2026-08-30, spun off from [`QW-012`](../../completed/QW-012-lineup-under-patience/status.md)
while bringing its status up to date. Not started.

QW-012's arena/shift evaluation ran on seed `20260829`, a value its own
`plan.md` said not to reuse and that was already spent on
`runs/eval/epoch-test/`. That run's headline margin — `attn` beating `cpool`
by only 0.8 points at ply-6 MCTS-128, versus `cpool` beating `attn` by 6.5
points at ply-3 — is close enough that this task exists to check it rather
than let it stand unconfirmed.

Next action: pick a seed genuinely unused in this project (candidate:
`20260830`; confirm against the exclusion list in `manifest.yaml` before
running), then `SEED=<chosen> scripts/evaluate_lineup.sh
runs/eval/patience-<date>-seed2 resnet=runs/train/patience-resnet/best
mlp=runs/train/patience-mlp/best cpool=runs/train/patience-cpool/best
attn=runs/train/patience-attn/best`. Cost: ~3.6h, same as QW-012's original
run — a smoke test (`GAMES=2`) first is worth the two minutes given the
projection already exists.
