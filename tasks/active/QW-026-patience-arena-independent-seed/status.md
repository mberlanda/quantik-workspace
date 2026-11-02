# QW-026 Status

Created 2026-08-30, spun off from [`QW-012`](../../completed/QW-012-lineup-under-patience/status.md)
while bringing its status up to date. W1 merged 2026-11-02 (see the end of this file); W2 open.

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


## 2026-11-02 — W1 merged

[models-py#77](https://github.com/mberlanda/quantik-models-py/pull/77) (squash, `7009a6740cf291e6b899af51b8b728a0b79a80f9`) adds `docs/patience-arena-second-seed.md`. It also adds figures, `scripts/plot_patience_second_seed.py`, a `docs/README.md` index line and an `AGENTS.md` rule against committing local paths.

**Seed.** `20261015`. A grep found it only in the run's own outputs. The run was executed 2026-10-24.

**Audit.** Policy ply 9 is NOT reportable on both seeds (135/300 on the original, 134/300 on the new seed). All other arenas pass (for example MCTS ply 6: 230/300 and 231/300).

**Verdict as stated in the doc.**
- The ply-3 MCTS-128 cpool lead holds on both seeds: mover +8.0 and +7.5, each +-3.4.
- The 0.8-point ply-6 MCTS-128 margin does not survive. The pooled sign reverses (attn +0.8 becomes cpool +1.5). That is inside noise on the pooled figure (+-3.1) and on raw mover-seat (+2.6 +-3.0), and marginally outside on distinct-game mover-seat (+3.7 +-3.4).
- Head-to-head favours cpool at ply 6 on both seeds (+4.0 +-7.5 and +7.7 +-7.1).
- Two seeds do not settle ply 6.

**Original run untouched, but not proven so.** `runs/eval/patience-2026-08-30` has mtimes 2026-08-30 19:05-19:20, but the pre-run listing was lost, so byte-identity is not shown.

**For W2:** propagate the caveat that the ply-6 margin is not a settled ranking. W2 stays open and untouched; the initiative is not complete.
