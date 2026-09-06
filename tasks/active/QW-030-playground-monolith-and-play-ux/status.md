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

**Next action:** `quantik-models-py` M1 — vendor the app and re-point
`DEFAULT_STATIC`. It is the change every other one is aimed at, and its
verification step (a wheel installed in a venv **outside** `~/Code/quantik-ns`)
is the step that would have caught the bug before 1.0.0 shipped.
