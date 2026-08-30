# QW-005 Status

Plan required. The contracts and individual stages exist, but the closed loop
does not. Pick this task to generate the missing specification and plan.

## 2026-08-30 reconciliation — left active, most of the mechanism now exists but unspecified

Substantially more exists than when this initiative was written, verified directly:

- `arena.autoplay` generates positions (not labels) by engine self-play.
- `arena.pack` pools runs, deduplicates on canonical key, and writes the gzipped
  `to-solve.qfen.gz` solver queue (`merge_qfens` filters against a corpus at *pack*
  time specifically to avoid re-solving known positions — see its docstring).
- `data/merge_corpus.py` folds solved positions back into a corpus, holding the
  probe out of the *merged* result rather than just new rows.
- The exact oracle labels the queue.
- This full cycle ran twice for real: v2 (2026-08-29, 5,226 positions solved,
  118,053 rows) and v3 (2026-08-29, 17,062 positions solved, 380,041 rows), each
  followed by a shift evaluation and an oracle-benchmark arena that decided whether
  the result changed anything (`docs/corpus-v3.md`).

So the position-selection -> solve -> merge -> retrain -> evaluate cycle this
initiative calls "the closed loop" has been **executed**, twice, with real gates
(paired significance tests, Wilson intervals, a fixed opponent). What is still
missing, and is exactly this initiative's remaining scope:

1. **No design spec or implementation plan was ever written for it.** It was run as
   a sequence of separately-invoked scripts by an operator who decided by hand what
   to run next, not as one mechanism with the selection/disagreement/promotion
   semantics this initiative's acceptance criteria require.
2. **Book write-back does not exist.** Nothing here writes a discovery back into
   `opening-book.v1` — the loop only ever produces a training corpus. Decision 2 in
   `decisions.md` ("what evidence may update the opening book") is still fully open.
3. **The v3 promotion decision is itself unresolved**, not just unautomated:
   `WORKSTREAMS.md` records that v3 is not published pending the epoch-budget protocol
   question (see new initiative QW-014). A human is still the promotion gate; there is
   no "either promotes or rejects without manual data surgery" mechanism.
4. **The play-store solver-queue export** (new initiative QW-013, in progress) adds a
   second, human-play-derived position source into the same `to-solve.qfen.gz` /
   `merge_corpus.py` path — the same non-negotiable rule this initiative's decision 4
   implies (`game-result.v1` outcomes are not labels) is independently upheld there.

Net: the *infrastructure* pieces this initiative's problem statement calls
"disconnected stages" are now connected and have been run end to end. The *design
and write-back* work is not done. Leaving active rather than closing, because
picking this up now is materially cheaper — describe and gate a mechanism that has
already been operated twice, rather than design one from nothing.

See QW-013 and QW-014 for the concrete work this initiative should link to rather
than duplicate.
