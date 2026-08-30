# QW-024: The Opening Arena — Measuring From Ply 0

> **Purpose:** Measure the phase a human game actually starts in, which has
> never been measured, and unblock the skill-level mapping.
> **Load with:** [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)
> **Run it with:** [`plan.md`](plan.md) — exact commands, measured timings, and the
> trap that makes a naive run worthless.

## Problem and motivation

Every arena on disk starts at ply 3 or later. So the opening — the only phase a
person is guaranteed to play — has never been measured for any checkpoint.

The reason is mechanical and visible in the data: **no corpus holds a single
position from plies 0, 1 or 2.** Not one. Every checkpoint is correspondingly
uniform to three decimal places on the empty board. Whether that uniformity
costs anything in play is exactly what has not been tested.

[`QW-010`](../QW-010-play-ux-skill-levels/initiative.md) cannot proceed without
it. A skill ladder derived from ply-3 numbers ranks opponents on a phase the
player never starts in, and a published ladder is hard to change once players
have opinions about it.

## The trap, which is the reason this packet exists

**A naive ply-0 arena produces a confident, wrong answer.**

Network agents are deterministic at the default temperature, and ply 0 has
exactly one start position — the empty board. So a pairing replays the same game
every time. Measured, 8 games, two `cpool` checkpoints:

```
distinct games: worst pairing 1/8
patience-cpool  100.0%  (16/16)
cpool             0.0%  (0/16)
```

That 100% is one game's result reported as sixteen. With `temperature 1.0` over
the first four plies, the same pairing at 40 games:

```
distinct games: worst pairing 40/40
patience-cpool   52.5%  (42/80)
cpool            47.5%  (38/80)
```

A different answer, and a real one. `scripts/evaluate_opening_arena.sh` sets the
temperature and ends by telling the reader to check the distinct-game count
before reading any win rate.

## Existing and desired behaviour

Existing: five arenas at plies 3, 6 and 9, and nothing below.

Desired: one arena at plies 0 and 1, policy and MCTS, with the `uniform-mcts`
control, reported side-balanced.

## Contracts and repositories

`quantik-models-py` only. No contracts. The tooling is merged and smoke-tested;
this initiative is the run and its write-up.

## Constraints and preserved invariants

- **Check the distinct-game count first.** It is the whole point.
- **Side-balanced or unreadable.** Mover 68-88%, responder 15-39%.
- **The `uniform-mcts` control is not optional** — it is what separates "these
  networks are close at ply 0" from "no network knows anything at ply 0", and
  the second is the live hypothesis.
- **One training seed** across every checkpoint compared, so no margin here has
  a run-to-run error bar under it. Say so in the write-up.

## Provenance

Raised by the 2026-08-30 v3 investigation and made an acceptance criterion of
QW-010 the same day. The tooling landed in models-py #57.
