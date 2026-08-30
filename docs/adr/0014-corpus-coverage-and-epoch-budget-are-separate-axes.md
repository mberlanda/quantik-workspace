# ADR 0014: Corpus Coverage and Epoch Budget Are Separate Axes

## Context

`docs/corpus-v3.md` in `quantik-models-py` concluded on 2026-08-29 that "the v3
corpus was compensating for undertraining, not adding information". That
conclusion propagated into the workspace, into memory, and into the framing of
the opening-coverage work — where it read as evidence that shallow-ply data is
not worth collecting.

It was wrong, and the reason it survived review is a label. `swept-cpool`, the
published Hub `cpool`, trains on `exact-sampled.npz` — **v1**. The document
called it "v2" throughout its sixteen-epoch rows, while `patience-cpool-v2`
genuinely uses `exact-sampled-v2.npz`. So "v2" named two different corpora
inside one table, and the row carrying the causal claim moved corpus and epoch
budget together.

The three corpora are strictly nested (`v1 ⊂ v2 ⊂ v3`, zero canonical keys lost
at either step) and plies 8-13 are byte-identical across all three. Every
difference lives at plies 3-7.

`runs/train/patience-cpool` — v1 corpus, `--epochs 60 --patience 5`,
**early-stopped at 43** — is the first converged run on the published corpus and
did not exist when that conclusion was drawn. Neither `patience-cpool-v2` nor
`-v3` is converged; both hit their 40-epoch cap.

## Decision

Treat **corpus coverage** and **epoch budget** as separate, additive axes, and
never attribute an effect to one on evidence that moved both.

Measured on the shared probe (`runs/oracle/probe-large.jsonl`, 7,800 positions
sharing no canonical key with any corpus — common ground, unlike the per-corpus
validation splits the original conclusion used):

1. **Shallow coverage (v1 → v2, plies 3-6) is real and corpus-caused.** About
   five points of ply-4 accuracy and a threefold cut in value MAE, from 109,602
   positions. Converging on v1 does not recover it — ply 4 goes *down*, 0.8780
   to 0.8551, while shallow-corpus checkpoints sit at 0.90-0.91.
2. **The v2 → v3 increment is null at matched budget.** 323,568 more positions
   of the same shallow distribution buy nothing on any probe band, any value
   metric, or any of five arena conditions.
3. **The epoch budget buys deep-band accuracy within a corpus** and costs
   shallow accuracy. `patience-cpool` has the best deep band of all five at
   0.9953.

## Consequences

- **Opening coverage has a measured payoff.** The v1 → v2 step is the pilot for
  extending coverage to plies 0-2, which no corpus reaches at all.
- **Densifying an already-covered ply band is not worth it.** The v2 → v3 step
  is the counterexample: more of the same distribution hit diminishing returns
  immediately. Extend to new plies, do not densify old ones.
- **A per-corpus validation split is not evidence for a cross-corpus claim.**
  Use the shared probe. The original deep-band conclusion was drawn from split
  comparisons after explicitly noting they were not common ground.
- **A run that hits its epoch cap is not a converged run** and must not be
  described as one. Record `stopped_early` and the cap alongside every result.
- **Held-out accuracy still does not rank play strength.** This is the fifth
  case. Everything above is probe accuracy; the arena remains the ranking that
  matters, and no arena on disk starts before ply 3.

## Alternatives rejected

- **Retire the whole v3 line as a negative result.** Rejected: it reaches the
  right operational answer for the lineup re-run but files the wrong finding,
  and would remove the motivation for the opening-coverage initiative — when the
  strongest measured result in the family is precisely that shallow data works.
- **Promote v3 to the standard corpus.** Rejected on the one clean
  single-variable comparison available: `patience-cpool-v2` vs
  `patience-cpool-v3`, matched cap, nested corpora, null in all five arena
  conditions and on the probe. It would make the corpus 10% larger and slower to
  buy a measured zero.
