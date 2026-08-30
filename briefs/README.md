# Delegation briefs

Self-contained charters for work that can be handed to a **separate session** without
that session needing the cross-repo context in `WORKSTREAMS.md`.

Each brief states the repo it touches, what already exists so nothing is rebuilt, the
decisions already taken so they are not relitigated, the traps that fail silently, and
the working agreement. A brief is a starting point, not a spec: if it turns out to be
wrong about the codebase, the codebase wins — and say so.

| brief | repo | shape | status |
|---|---|---|---|
| [`lineup-under-patience.md`](lineup-under-patience.md) | `quantik-models-py` | low ambiguity, **long compute**; the risk is protocol, not diff | open |
| [`play-solver-queue-export.md`](play-solver-queue-export.md) | `quantik-models-py` | low ambiguity, small diff, no compute; the smallest complete charter open | **done, py#53** |

Cross-repo work is deliberately **not** here — workstreams 13, 7, 2, 4 and 12 span
packages and belong in a session that holds the whole workspace. See `WORKSTREAMS.md`.
