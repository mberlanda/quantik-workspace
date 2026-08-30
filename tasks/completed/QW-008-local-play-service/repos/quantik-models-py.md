# quantik-models-py task

Objective: close the recorded remaining edges on the play service, not rebuild it.
Backfill the seed-dependent finding (`docs/autoplay.md`) into any earlier arena
write-up quoting a pre-2026-08-29 margin. Confirm `GET /api`'s response carries a
store-availability field the client can branch on (verify, do not assume the field
exists — if it does not, add it here before the visualizer can consume it).

Relevant modules: `src/quantik_models/play/{registry,opponents,service,record,
store,server,__main__}.py`; tests: `tests/test_play_*.py`.

Inputs and outputs: reads `runs/train/*/best` checkpoints via a models directory
of symlinks; reads/writes `~/.local/share/quantik/games.db`.

Required contracts release: current `quantik-core` 1.2.0.

Constraints: read-only against a live games database outside of `record_game`;
never derive a training label from `games.winner`.

Dependencies: none.

Commands and focused tests: `pytest tests/test_play_service.py tests/test_play_server.py tests/test_play_store.py tests/test_play_registry.py`.

Expected artifacts: no new artifacts — this is a documentation/edge-case task.

Completion criteria: the two remaining edges in `status.md` are closed or
explicitly deferred with a reason; existing play-service tests still pass.

Handoff path: `tasks/active/QW-008-local-play-service/` (no `handoffs/` directory
exists yet — create one only if a handoff is actually produced).
