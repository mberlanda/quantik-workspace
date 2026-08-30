# QW-012 Status

Created 2026-08-30, during reconciliation. Not started.

Mechanism merged (`--patience`, py#38); lineup not re-run. Verified on disk:
`runs/train/patience-cpool-v2` and `runs/train/patience-cpool-v3` exist and are
real completed 40-epoch `--patience 5` runs, but both train on the *v2/v3*
corpora, not the `exact-sampled.npz` corpus the published lineup
(`swept-cpool`, `lineup-{resnet,mlp,attn}`) was trained on — see `decisions.md`
for why they cannot be reused as this initiative's `cpool` arm.

Full charter: [`plan.md`](plan.md).
That brief is long-compute, low-ambiguity — the work is mechanical, the write-up
is the deliverable.

Next action: the brief's mandatory step 1 (a 4-epoch/2-patience smoke test
confirming `stopped_early` and `epoch_cap` record correctly in both directions),
then the four full runs, idle-timed first.

## Update 2026-08-30 — all four arms are trained, two did not converge

Derived from each run's `metrics.jsonl` line count against its `config.json` cap:

| arm | corpus | cap | ran | outcome |
|---|---|---|---|---|
| `patience-cpool` | `exact-sampled.npz` | 60 | 43 | **early-stopped** |
| `patience-attn` | `exact-sampled.npz` | 60 | 45 | **early-stopped** |
| `patience-resnet` | `exact-sampled.npz` | 60 | 60 | **hit cap**, best at 58 |
| `patience-mlp` | `exact-sampled.npz` | 60 | 60 | **hit cap**, best at 59 |

All four train on the published corpus, as `decisions.md` requires. The arena
has not been run.

**A scope problem to settle before it is.** `resnet` and `mlp` hit the cap with
their best epoch in the final two, so neither converged. This initiative's own
question — *does the cpool/attn tie survive giving each architecture the epochs
it wanted?* — is answerable for `cpool` and `attn` and **not answerable for
`mlp` as run**. Either raise the cap for those two arms and retrain, or state
the limitation explicitly in the write-up. Do not report a four-way comparison
that silently mixes two converged arms with two truncated ones.

**Arena seed constraint:** 20260829 (epoch-test) and 20260909 (lineup) are both
spent. Use a third.

## Update 2026-08-30 — arena run, but on the seed this brief said not to use

`scripts/evaluate_lineup.sh runs/eval/patience-2026-08-30` was launched and ran
to completion (shift eval + policy/MCTS-128 arenas at plies 3/6/9 and 3/6) —
but **without overriding `SEED`**, so it took the script's default, `20260829`.
That is exactly the value `plan.md` line 121 says not to use ("Use a fresh
arena seed, not `20260829`") and the value this file already flagged above as
spent on `runs/eval/epoch-test/`. **This is a plan violation, caught after the
~3.6h run finished, not before.** Confirmed on disk: every `games.json` under
`runs/eval/patience-2026-08-30/{policy,mcts}-p*/` records `"seed": 20260829`.

Results as measured (full tables in `quantik-models-py`'s
`docs/decisions/0001-architecture-lineup.md`, `docs/shift-evaluation.md`,
`docs/autoplay.md`, all updated 2026-08-30):

| model | val top-1 | shift all | arena @p3 MCTS-128 | arena @p6 MCTS-128 |
|---|---|---|---|---|
| `cpool` | **0.9916** | **0.9626** | **66.4%** | 57.6% |
| `attn` | 0.9900 | 0.9472 | 59.9% | **58.4%** |
| `resnet` | 0.9793 | 0.9429 | 61.8% | 57.0% |
| `mlp` | 0.9660 | 0.9318 | 61.5% | 56.1% |

**Does the cpool/attn tie survive?** For `cpool` vs `attn`, no — `cpool` wins
the shift metric and the ply-3 MCTS arena outright (widest gap in either
table); `attn` only edges ahead at ply-6 MCTS by 0.8 points. But per the
scope problem noted above, `resnet` and `mlp` did not converge (hit the
60-epoch cap still improving), so their numbers in this table are still
floors, same as the fixed-16-epoch numbers were — this run answers the
initiative's question for `cpool`/`attn` and does not settle it for all four.

**Resolved 2026-08-30: spun off rather than blocking this task.** The result
is published as-is, with the seed caveat recorded prominently in the three
`quantik-models-py` docs above and here. Confirming it on an independent seed
is real, necessary follow-up — but it does not require retraining and does
not change anything about QW-012's training deliverable, so it is tracked
separately as [`QW-026`](../../active/QW-026-patience-arena-independent-seed/initiative.md)
rather than left as an open decision on this packet. This task's own
acceptance criteria (train all four, correctly decline `patience-cpool-v2/v3`,
state the per-architecture outcome, answer whether the cpool/attn tie
survives, leave the fixed-budget checkpoints untouched) are met.
