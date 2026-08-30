# QW-010: Play UX for Non-Expert Players — Skill Levels and How-to-Play

> **Purpose:** Derive an evidence-based easy/medium/hard opponent mapping and a
> rules explainer, so a public visitor is not handed a roster of twenty engines
> keyed by architecture name.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)

## Problem and motivation

The play service (QW-008) roster assumes the player already knows what
`cpool@128` or `minimax-d2` means. That is the wrong default for a public
audience without giving up the audience that does want the roster. Requested
2026-08-29, not started as of 2026-08-30.

## Existing and desired behaviour

Existing: `docs/oracle-benchmark.md` and the lineup tables already carry the
numbers a level mapping needs, but no derivation from them to a three-tier
mapping exists. Desired: a written mapping, checkable against the numbers it
cites, produced *before* any UI work — this splits cleanly into a research half
(here) and a UI half (`quantik-qfen-visualizer`, unregistered, out of formal
scope — see `decisions.md`).

## Contracts and repositories

`quantik-models-py` only, in this registry. No contracts are touched — this is a
research and documentation task over existing arena output, not new data.

## Constraints and preserved invariants

- **The seat effect dwarfs the model differences it would otherwise be tempting
  to rank by.** Mover win rates run 68–88%, responder 15–39%
  (`docs/oracle-benchmark.md`). A level assigned from an unbalanced win rate is
  wrong by construction; every number behind the mapping must be seat-balanced.
- Do not invent a numeric "ELO-like" score without deriving it from the existing
  paired/Wilson-interval methodology this project already uses.

## Migration and compatibility strategy

N/A — additive documentation, then an additive UI layer over the existing
roster; the full opponent list stays available behind "advanced."

## Release strategy and ordering

Research half (this initiative) blocks the UI half by design — the mapping is
the input, not a parallel workstream.

## Risks and exclusions

Excludes the puzzle-mode UI (QW-011) and the storeless-deployment container
(QW-009), which do not depend on this initiative and can ship independently.

## Acceptance criteria

See `manifest.yaml`.
