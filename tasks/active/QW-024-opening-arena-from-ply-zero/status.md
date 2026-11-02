# QW-024 Status

**W1 merged (2026-11-02 bookkeeping); W2 open.** The run is recorded in `docs/opening-arena-ply0.md` in models-py. The paragraphs below are the pre-run state, kept for the cost figures.

`scripts/evaluate_opening_arena.sh` landed in models-py #57 and was smoke-tested
end to end at `GAMES=6 START_PLIES=0 MCTS_SIMS=16`.

Measured cost on this machine, CPU, from the smoke runs:

| | s/game |
|---|---|
| `net-policy` | ~0.22 |
| `net-mcts` at 128 sims | ~0.89 |

Six agents is 30 ordered pairings. At the default 300 games per pairing that is
9,000 games per condition — roughly **35 minutes** for a policy arena and
**2¼ hours** for an MCTS arena, per start ply. Both start plies, both arms, is
about **5½ hours**. Halve `GAMES` to halve it; the distinct-game count matters
more than the raw count here.

Next action: [`plan.md`](plan.md), which is the runnable command.

Blocks [`QW-010`](../QW-010-play-ux-skill-levels/initiative.md).


## 2026-11-02 — W1 merged

[models-py#78](https://github.com/mberlanda/quantik-models-py/pull/78) (squash, `5a4794c63c608cb61a26169b00d6ed23ffb2ed95`) adds `docs/opening-arena-ply0.md`. Besides the doc it adds three figures, `scripts/plot_opening_arena.py` and a `docs/README.md` index line; those are outside the packet's `allowed_paths` and were required by `test_docs_crossrefs`.

**Run parameters.** Seed `20261001`, `GAMES` 300, `MCTS_SIMS` 128, `TEMP` 1.0. Output dirs `runs/eval/opening-ply0` and `runs/eval/opening-ply0-tp6` (gitignored). The console logs were lost, so wall-clock time is unrecorded.

**Distinct-games audit (worst pairing), checked before any rate was read.**

Config A, `TEMP_PLIES=4`:
- policy ply 0: 292/300
- policy ply 1: 296/300
- MCTS ply 0: 103/300, FAILED. No win rates are reported for it.
- MCTS ply 1: 257/300

Config B, rerun at `TEMP_PLIES=6`, ply 0 only (the script was not modified; the value was set by environment override):
- policy: 299/300
- MCTS: 244/300, passes

Config B is reported as a separate configuration, not merged into A.

**Seat-split caveat for W2.** "Mover" means the first engine-chosen side. At ply 1 the mover is the second player of the full game, so the ply-1 mover rates of 29-41% (responder 50-58%) are a parity effect. The packet's expectation of 68-88% mover / 15-39% responder matches the ply-6 arenas, not ply 0 or 1. Policy ply-0 mover rates are 49-58%. There is one training seed per checkpoint.

W2 stays open and untouched. The initiative is not complete.
