# QW-008: Local Play Service — Analysis and Recording

> **Purpose:** Record, as a workspace task packet, the local HTTP play service that
> already exists and runs — so future sessions stop treating it as unstarted.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)

## Problem and motivation

Seven repository-scoped PRs in `quantik-models-py` (#45, #47–#51) and three in
`quantik-qfen-visualizer` (#3–#6) — ten total, both merged 2026-08-29 — built a
service that serves the visualizer, plays twenty opponents, analyses positions, and
records finished games to `~/.local/share/quantik/games.db` with symmetry-aware
dedup. This was tracked only in `quantik-ns/WORKSTREAMS.md`, never here, so the
control plane undercounts the repository's actual surface.

## Existing and desired behaviour

Existing, verified in code: `play/registry.py` discovers playable checkpoints from
a models directory; `play/opponents.py` builds the roster under the same agent
names the arena stamps into `games.json`, so a human game and a benchmark game are
one comparable dataset; `play/service.py` validates and plays a move
(`quantik.engine-request.v1` in, `quantik.engine-response.v1`-shaped out);
`play/record.py` replays and verifies a submitted game before it is trusted;
`play/store.py` is the SQLite layer, with `game_positions` and
`distinct_positions` existing specifically to feed a later solver queue (see
QW-013); `play/server.py` is a threaded stdlib HTTP server, chosen because
inference is already serialized behind a lock. Desired: the packet exists so a
session can pick up its remaining edges (see acceptance criteria) without
re-discovering all of the above from source.

## Contracts and repositories

`quantik-models-py` only, in this registry — `quantik-qfen-visualizer` is not a
repository `workspace.yaml` knows about, so the browser-client half of the ten PRs
(the play client, solver-verified examples, mobile piece picker, evaluation bar)
is described here in prose but cannot carry a `repos/quantik-qfen-visualizer.md`
task packet without a workspace-level change that is out of this task's scope.
Contracts touched: `game-result.v1` (the store's `games` table matches its column
order exactly, so a parquet export is a plain `SELECT *`), `model-checkpoint.v1`
(`registry.py` validates `weights_hash` against the manifest before serving a
model).

## Constraints and preserved invariants

- `game_positions.canonical_key` is a **decimal string**
  (`str(int(fb.canonical_keys(boards)[0]))`), not the `uint64` array
  `ExactCorpus` produces — the mismatch is silent if compared unconverted (see
  QW-013's trap section).
- `games.winner` is never a training label; only positions travel to the corpus.
- `model_id` is the models-directory subdirectory name a person chose, not
  `manifest["model_id"]` — both are kept, distinctly.

## Migration and compatibility strategy

None required; this is a recording task, not a design task. No behavior changes.

## Release strategy and ordering

N/A — already merged and running.

## Risks and exclusions

Excludes the storeless-deployment work (new image, `OnnxEvaluator`, licence
carrying) — that is QW-009. Excludes the skill-level/how-to-play UI — that is
QW-010. Excludes the puzzle-mode browser UI — that is QW-011.

## Acceptance criteria

See `manifest.yaml`.
