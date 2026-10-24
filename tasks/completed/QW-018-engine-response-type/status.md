

## 2026-09-20 — W3 merged; QW-018 is complete apart from a core follow-up

[api-rust#6](https://github.com/mberlanda/quantik-api-rust/pull/6) makes the gateway emit `engine-response.v2`: `certainty` on every response (minimax `proof` only when its headline score is proven, dropping the heuristic tail; MCTS and beam always `estimate`), `candidates` (max 8, legal, distinct, selected first), a replay-checked `pv` (minimax and beam), `engine_config`, and validation against the registered schema in tests. `engine_version` stays the core revision.

- **Known gap:** minimax and MCTS candidate lists are ranked *subsets* (the core collapses symmetric root children). Complete per-move coverage needs a quantik-core-rust item: a public root-score accessor on `MinimaxResult`, and an MCTS visit list that is orbit-expanded or run without the transposition table. Not yet an owned work item.
- `Unit` in the gateway has only `visits|value`; it is not a general v2 reader.
- `is_proven` relies on the core's squashed scale (proven is exactly +-1); a test now pins that a deep unproven search stays strictly inside the interval.
- **Cross-repo mismatch:** JSON Schema `integer` accepts `1.0` as a visits score; the contracts stdlib hook rejects it. The gateway emits integer counts and a test checks it.
- api-rust has no CI, so all of this is local evidence (17 lib + 2 integration tests, fmt, clippy). The diff was reviewed unfiltered by the coordinator.
- The visualizer's `lastAnalysis` renders nowhere yet (W4's paths excluded the UI); a certainty badge is a follow-up item if wanted. The Python play service still emits the v1 shape.
- The models-py vendored copy of the visualizer is behind visualizer main (`9810407`) and needs `scripts/sync_visualizer.py`.
