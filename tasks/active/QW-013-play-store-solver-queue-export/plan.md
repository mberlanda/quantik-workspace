# Brief — export the play store to a solver queue

**Repo:** `quantik-models-py` (single repo; nothing else is touched)
**State:** every piece exists except the entry point that joins them
**Shape:** low ambiguity, small diff, no compute. **The smallest complete charter open.**
**Suggested model:** Sonnet. Haiku is plausible if the key-format trap below is handled explicitly.

---

## Why this exists

The play service records human games. Nothing consumes them yet, so the positions people
reach by actually playing never reach the corpus — the training data has been fed
exclusively by autoplay, which explores where the *engines* go, not where *people* go.

This closes that loop by producing the **same artifact the autoplay pipeline already
produces**: a `to-solve.qfen.gz` that the existing exact solver consumes and
`data/merge_corpus.py` folds into a corpus. No new format, no new consumer, no new
schema.

### The non-negotiable rule

**Human game outcomes are never labels. Only positions travel.**

This is the same discipline autoplay follows and it is not a matter of taste: a human
game's result says who won between two fallible players, which is not the value of the
position. Positions reach the corpus **only** through the exact oracle, like everything
else. See `docs/labeling-strategy.md` and `docs/autoplay.md`. If the implementation ever
reads `games.winner` for anything other than a report, it is wrong.

## What already exists — read this before writing anything

Almost all of it. The remaining work is genuinely an entry point plus a corpus filter.

| piece | where | state |
|---|---|---|
| Positions extracted per game | `play/store.py`, table `game_positions (game_id, ply, qfen, canonical_key)` | **done at record time** — every recorded game already has its positions rows |
| Symmetry-deduplicated query | `play.store.distinct_positions(conn, max_ply=6)` | **done, tested** (`tests/test_play_store.py:172`), and exported from `play/__init__.py` |
| The output format | `arena.pack.write_gzip(text, path)` writes `to-solve.qfen.gz` | done |
| The corpus filter pattern | `arena.pack.merge_qfens` filters against `ExactCorpus.load(corpus)` canonical keys | done — **copy this, and read its docstring** |
| The ply cut-off | 6, matching `autoplay --max-solve-ply` | decided |
| Live data to test against | `~/.local/share/quantik/games.db` — 20 games, 161 positions, **101 distinct canonical keys** | exists |

`distinct_positions` was written *for* this and currently has no production caller. Its
docstring explains the `MIN(rowid)` grouping trick; do not reimplement it.

## The one real trap

**The two canonical-key representations do not match, and nothing will tell you.**

- `play/record.py:_canonical_key` returns **`str(int(fb.canonical_keys(boards)[0]))`** — a
  *decimal string* of a uint64, and that string is what is stored in
  `game_positions.canonical_key`.
- `ExactCorpus` gives you `fb.canonical_keys(corpus.boards)` — a **numpy uint64 array**.

Compare them without converting and `np.isin` finds nothing in common, the filter removes
zero rows, and you queue positions the corpus already has. The failure is **silent and
looks like success**: a plausible-sized queue, no error, hours of solver time spent
re-labelling known positions.

This exact class of waste has already happened once here: the first oracle runs filtered
against a superseded corpus and **35% of a 26,157-position queue was already labelled —
about twelve hours of solver time.** That is why `merge_qfens` re-filters at *pack* time
rather than trusting the filtering done earlier. Read its docstring.

**Write the failing test for this first**: seed a store with a position that *is* in a
fixture corpus, assert the exporter drops it. A test that only checks "some rows came
out" would pass with the filter completely broken.

## The work

Add `src/quantik_models/play/export.py` with a `main(argv)` and wire it as a module
entry point (`python -m quantik_models.play.export`), matching how `arena.pack` and the
other tools are invoked.

```
python -m quantik_models.play.export \
  --db ~/.local/share/quantik/games.db \
  --corpus runs/oracle/corpus/exact-sampled-v3.npz \
  --out runs/play/packed \
  --max-ply 6
```

It should:

1. Open the store with `play.store.connect` — **not** a bare `sqlite3.connect`. The
   pragmas matter: `foreign_keys = ON`, and `journal_mode = WAL` so this can read while
   the service is writing a game.
2. Call `distinct_positions(conn, max_ply)`.
3. Filter against the corpus's canonical keys — **minding the trap above**. `--corpus`
   should be optional; with no corpus, export everything and say so in the manifest.
4. Write `to-solve.qfen.gz` via `arena.pack.write_gzip`, so the artifact is
   byte-compatible with the autoplay one.
5. Write a small `summary.json` beside it recording: positions found, positions dropped
   as already-known, positions written, the corpus filtered against, the ply cut-off, and
   the source database. **The drop count is the number that tells you the filter worked** —
   the earlier incident was invisible precisely because nobody was counting it.
6. Print the summary. Exit non-zero on a database that does not exist; **exit zero on an
   empty queue** — "every position is already known" is a success, not a failure, and a
   cron job should not page on it.

## Verification — do this, do not assume it

The point of the artifact is that the *existing* solver eats it. Prove that end to end:

1. Run the exporter against the real `~/.local/share/quantik/games.db` (20 games, 101
   distinct keys — expect the filtered count to be well under that, since human games
   pass through common openings the corpus already covers).
2. Feed the resulting `to-solve.qfen.gz` to the existing solver path and confirm it is
   accepted without a format change.
3. Confirm `data/merge_corpus.py` accepts the solver's output — and note that it holds the
   probe out of the **merged** result, not just the new rows, because solving a position
   also labels its children.

If the filtered queue comes out **empty**, that is a legitimate outcome worth reporting
rather than a bug to work around: it would mean twenty games of human play reached
nothing the corpus lacks, which is itself a finding about whether collecting human games
is worth it. Say so plainly.

## Guard rails

- **Read-only against the games database.** The exporter must never write to it. It is
  the one irreplaceable artifact in this project — checkpoints can be retrained, these
  games cannot be replayed. It deliberately lives outside `runs/`, which is gitignored
  and routinely deleted.
- **Do not add outcome-derived labels**, not even behind a flag. See the rule above.
- **Torch-free.** Nothing in this path needs torch, and the torch-free install is a tested
  CI configuration. If a test needs torch, `pytest.importorskip("torch")` goes **inside
  the test function** — an unguarded module-scope import fails collection for the whole
  file.
- Do not change `game_positions` or `distinct_positions`. If the query needs something it
  does not provide, that is worth raising rather than quietly widening.

## Working agreement

- One PR, atomic commits, merged when CI is green. Do not stack open work.
- Commit as the user only — **no `Co-Authored-By:` or `Claude-Session:` trailers**.
- Failing test first for the filter behaviour, per the trap section.
- Documentation in the same PR: `docs/autoplay.md` describes the position pipeline and
  should gain the human-games branch; [`WORKSTREAMS.md`](../../../docs/history/workstreams-archive.md) §11 "Still to build" lists this.

## Where to read first

- `src/quantik_models/play/store.py` — module docstring, then `distinct_positions`
- `src/quantik_models/arena/pack.py` — `merge_qfens` docstring (the twelve-hour lesson) and `write_gzip`
- `src/quantik_models/play/record.py` — `_canonical_key`, `replay`
- `docs/labeling-strategy.md` and `docs/autoplay.md` — why outcomes do not travel
