# QW-030 Status

Created 2026-09-05, immediately after `quantik-models` 1.0.0 reached PyPI.

**Why now:** the release is what exposed the gap. `pip install quantik-models`
succeeds and then serves no app, because `play/__main__.py:28` resolves
`--static` through `parents[4]` to a sibling checkout that exists only inside the
`quantik-ns` workspace. Verified against the published wheel, from outside the
workspace tree.

**Scope set by the user, 2026-09-05:** one-port packaging plus the WS14 play UX
(this packet's V1–V5 and M1–M5), plus the two QW-009 leftovers that share the same
surface — the storeless 503 the client shows at the end of every game, and the
Docker image sourcing weights from the Hub rather than from local `runs/`. Puzzle
mode (QW-011) was considered and excluded.

**Relationship to the existing packets:**

- **QW-009** — this initiative delivers its criteria 3 and 4 (Hub weights at build
  time, `--no-store` preserved) and leaves criterion 5 (GHCR) untouched.
- **QW-010** — this initiative delivers the *shape* of the non-expert UI: the mode
  prompt, the how-to-play explainer, and the advanced disclosure that its sixth
  acceptance criterion asks to specify. It delivers **none** of the skill-level
  mapping, which stays blocked.
- **QW-024** — unchanged and still `ready-to-run`. It is the blocker on the
  ladder, and running it is the next action for QW-010, not for this packet.

**M1 done, 2026-09-06:** `quantik-models-py` PR #62, squash-merged at `d402e319`.
Vendors the app, re-points `DEFAULT_STATIC` at package data, and the CI smoke
test (fresh install, no sibling checkout) is green on macOS/Ubuntu/Windows ×
py3.12/py3.13. See `handoffs/quantik-models-py.md` for the full record,
including a scope deviation: the PR also fixed a real bug in
`play/server.py` (outside M1's `allowed_paths`) — `HTTPServer.server_bind`'s
reverse-DNS lookup was hanging macOS CI for ~30s per run, the actual cause
behind three earlier failed fix attempts. Flagged for coordinator review.

**Next action:** `quantik-models-py` M2 — `GET /api` reports a `recording`
bool. Unblocks visualizer V5, which is otherwise independent of M1's path.
