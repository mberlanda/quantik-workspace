# QW-024 Status

**ready-to-run.** The tooling is merged and smoke-tested; nothing blocks the run.

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
