# W1 — Derive the skill-level mapping from the arena, with numbers

**Repository:** `quantik-models-py` · **Branch:** `docs/skill-levels-derivation` · one PR
**Blocked on:** QW-024 (both work items) merged. **Dispatch:** judgment — capable model, human
review before W2.

The play service exposes twenty opponents keyed by architecture and simulation count, which assumes
the player already knows what `cpool@128` means. An easy/medium/hard mapping has to come from arena
numbers, not intuition, because **the seat effect is larger than the strength gaps between most
opponents**: mover 68-88%, responder 15-39%.

This item writes `docs/skill-levels.md` and changes no code.

## Before you start

Read QW-024's `docs/opening-arena-ply0.md`, including its **Reading** section. If it concluded that
the networks are indistinguishable at ply 0 — a live and expected possibility, since every
checkpoint is uniform to three decimals on the empty board — then a ply-0-derived ladder is not
supportable, and this item's job is to say so and use what QW-024 recommended instead. Do not
manufacture an ordering the evidence does not carry.

`decisions.md#D4` of QW-010 explicitly rejected deriving levels from the existing ply-3/6/9 tables.
That rejection stands.

## Decide and record in `docs/skill-levels.md`

1. **The mapping.** Each skill level to a specific opponent spec — architecture, checkpoint,
   simulation count. Named exactly as `play/opponents.py` will consume them.
2. **The derivation, with numbers.** Every level justified from QW-024's arena, quoting
   **balanced-seat** win rates, never raw ones. Show the numbers inline; a reader must be able to
   check the mapping without opening another file.
3. **The uncertainty.** Where two candidate opponents are within noise, say so and state which you
   picked and why. A ladder whose rungs are indistinguishable is worse than a shorter ladder.
4. **Which checkpoints are eligible.** No v3-corpus checkpoint enters the mapping or the Hub on
   current evidence: `cpool-v3`, `patience-v2` and `patience-v3` stay local staging symlinks under
   `runs/play/models/` only. State this explicitly so W2 cannot reintroduce them by accident.
5. **The advanced toggle.** Specify the toggle that exposes the full opponent roster, not just the
   simplified default view. The roster is 6 classical opponents plus 2 per discovered model, so its
   size is a function of what is staged — specify it as a rule, not a fixed number.

## Completion criteria

- All five sections present, each a decision with its supporting numbers.
- Every win rate quoted is balanced-seat, and says so.
- `git diff --stat` touches `docs/skill-levels.md` only.
- The PR is marked as requiring human review before W2.

## Handoff

Record the mapping, and whether QW-024's evidence supported a ladder at all.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
