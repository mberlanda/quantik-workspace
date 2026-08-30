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
