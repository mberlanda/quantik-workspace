# QW-011: Puzzle Mode in the Browser

> **Purpose:** Get the already-built puzzle generator's output in front of a
> player — commit a pack, replace the hand-picked examples with a themed picker.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)

## Problem and motivation

`src/quantik_models/play/puzzles.py` (merged as models-py #51) mines the exact
corpus by theme and writes a JSON pack — verified: `--per-theme 40` over
`exact-sampled-v3` yields 40/40/40/29/40 across `mate-in-1`, `only-move`,
`double-threat`, `endgame`, `already-lost`. Nothing in `quantik-qfen-visualizer`
consumes it yet.

## Existing and desired behaviour

Existing: the generator, tested (`tests/test_play_puzzles.py`), producing
themed puzzles with `solutions` verified through a second code path, and
`already-lost` entries deliberately carrying no solution (a study, not a
puzzle). Desired: a committed pack and a picker in the visualizer, which needs
no play service and no loaded model — the pack is static JSON, making this the
one piece of the public-deployment surface that works even with nothing else
running.

## Contracts and repositories

`quantik-models-py` only, in this registry — the picker UI lands in
`quantik-qfen-visualizer`, unregistered (see `decisions.md`). No contracts are
touched; the pack format is this initiative's own, not a `quantik-core-contracts`
schema.

## Constraints and preserved invariants

- `already-lost` puzzles have no `solutions` field, on purpose — the picker must
  not treat a missing solution as a bug to paper over.
- `double-threat` puzzles do not always land the win on the same square across
  instances of the theme; a picker or hint system must not assume one canonical
  answer square per theme.

## Migration and compatibility strategy

N/A — new, additive feature; no existing behavior changes.

## Release strategy and ordering

1. Generate and commit a pack.
2. Build the picker against it.
3. Replace the five hand-picked examples currently in the visualizer.

## Risks and exclusions

Excludes skill levels (QW-010) and the storeless deployment container (QW-009);
independent of both and the fastest of the three to ship, per
`quantik-ns/WORKSTREAMS.md` workstream 15's own note.

## Acceptance criteria

See `manifest.yaml`.
