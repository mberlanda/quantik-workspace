# QW-012 Decisions

All substantive decisions are recorded in
[`briefs/lineup-under-patience.md`](../../../briefs/lineup-under-patience.md)
and are not repeated here. That brief is the plan; this file exists so the
initiative is not "plan-required" — the plan already exists and is approved.

The one decision this packet adds:

1. **`patience-cpool-v2` is NOT a substitute for this initiative's `cpool` run —
   verified, corrects the brief's own suggestion to check it.** The brief says
   "check its config before spending a run on it." Checked 2026-08-30:
   `runs/train/patience-cpool-v2/config.json` trains on
   `runs/oracle/corpus/exact-sampled-v2.npz`, but the published lineup this
   initiative revises (`runs/train/swept-cpool/config.json`,
   `runs/train/lineup-cpool/config.json`) both train on
   `runs/oracle/corpus/exact-sampled.npz` — a different, smaller corpus. A
   `patience` run on the wrong corpus answers a different question (does a
   bigger corpus need more epochs too) than the one this initiative needs (does
   the *published* lineup's `cpool` need more epochs). `patience-cpool-v2` is
   still useful evidence that the mechanism works and that `cpool` peaks well
   past epoch 16, cited in the brief itself — it just is not epoch 0 of this
   initiative's own `cpool` arm, which must train on `exact-sampled.npz`.
