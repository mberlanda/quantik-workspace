# QW-008 Status

Created 2026-08-30, during reconciliation. Largely complete.

Built and merged 2026-08-29: `quantik-models-py` #45 (move handler), #47
(replay-and-verify), #48 (HTTP server), #49 (the inert seed), #50 (analysis
endpoint), #51 (puzzle generator, shared with QW-011); `quantik-qfen-visualizer`
#3 (play client), #4 (solver-verified examples), #5 (mobile piece picker), #6
(evaluation bar and move analysis). Verified directly in
`src/quantik_models/play/`: `registry.py`, `opponents.py`, `service.py`,
`record.py`, `store.py`, `server.py`, `__main__.py` all exist and match
`docs/play-service.md`'s description.

Remaining edges, not yet picked up:

1. The browser client still attempts `POST /api/games` against a `--no-store`
   server and would show a raw `503` error to a public visitor — needs to read
   `GET /api`'s store-availability field first (visualizer-side, unregistered
   repository, see `decisions.md`).
2. `docs/autoplay.md`'s seed finding has not been backfilled onto every earlier
   arena write-up that quotes a margin.

Nothing here blocks QW-009, QW-010, or QW-011, all of which build on this
service rather than modify it.

## 2026-08-30 — closed

Every acceptance criterion is met: the `play/` modules and their tests are the implementation, each endpoint has a focused test, and the seed finding is recorded in `docs/autoplay.md`. The one remaining edge — the browser client showing a storage error against a `--no-store` server — is carried by QW-009, which owns the storeless deployment, rather than holding this initiative open.
