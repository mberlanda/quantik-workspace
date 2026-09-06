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

**M2–M4 implemented, 2026-09-06 — PRs open, not merged.** All three
`quantik-models-py` work items are done and green (650 passed, mypy clean
on each branch) with PRs open; merging each is the user's call, not made in
this pass. See `handoffs/quantik-models-py.md` for the full record of each.

- **M2** (#64, `feat/api-advertises-recording`): `GET /api` now reports
  `"recording": <bool>`. Unblocks visualizer V5.
- **M3** (#65, `feat/fetch-stage`): `hub.stage()` + `--stage`/`--copy` on
  `quantik-models-fetch`. One gap found and fixed *within this pass*, before
  merge: the initial symlink-or-copy-on-OSError fallback doesn't cover the
  Docker case (a symlink into a build stage's own Hub cache resolves fine
  within that stage, then dangles once a later stage copies the directory
  alone) — added an explicit `--copy`/`copy=True` to force real files.
- **M4** (#66, `chore/docker-from-hub`, **stacked on #65** — depends on
  `--copy`, so merge #65 first): the Docker image now builds from
  `quantik-models-py` alone (no sibling `quantik-qfen-visualizer` context)
  and fetches all four published weights from the Hub at build time
  instead of a hand-staged local `runs/` copy. Built and ran it for real —
  not just written the Dockerfile — and measured **498 MB** (four
  architectures; down from 553 MB after dropping the unused
  `model.safetensors` `--runtime onnx` never opens). `scripts/build_docker_image.sh`
  and `docker/staging/` are now stale and were flagged rather than
  silently left to look current — both fall outside M4's `allowed_paths`.

**Next action:** merge #64, #65, #66 in that order (M4 needs M3's
`--copy` flag) when the user is ready, then `quantik-models-py` M5 —
blocked on the visualizer's V1–V5, which this pass did not touch.
