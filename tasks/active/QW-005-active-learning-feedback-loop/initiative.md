# QW-005: Search and H2H Active-Learning Feedback Loop

Turn the diagrammed feedback loop into a measurable mechanism: search/H2H
evidence selects openings or positions, self-play/search produces new training
evidence, authorized results update the next-round source, a candidate model is
trained, and H2H evaluation promotes or rejects it.

## Mandatory planning task

Use `FEEDBACK_LOOP_SEED.md` as the source brief. Produce a reviewed design spec
and implementation plan before code. The first slice must be smaller than the
full vision and must identify its causal hypothesis and evaluation gate.

## Constraints

- Reuse existing contracts unless the design proves an additive/new surface is
  necessary.
- `game-result.v1` remains calibration/evaluation evidence unless a contract
  decision explicitly changes its role.
- Book write-back must distinguish exact, bounded, and heuristic/model evidence.
- Do not promote a candidate from win rate alone without declared uncertainty
  and regression checks.
