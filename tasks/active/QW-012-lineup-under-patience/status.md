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
