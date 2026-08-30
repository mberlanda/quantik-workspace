# QW-008 Decisions

Recorded, not open — this initiative documents work already merged.

1. **`quantik-qfen-visualizer` is not carried as a formal `affected_repositories`
   entry.** `workspace.yaml` registers only `quantik-core-contracts`,
   `quantik-core-py`, `quantik-core-rust`, `quantik-models-py`. Adding the
   visualizer (or `quantik-api-rust`) is a `workspace.yaml`/`context/` change, out
   of this task's scope (`Do NOT touch workspace.yaml`). The visualizer-side half
   of the play service (PRs #3–#6) is real and merged; it is described in
   `initiative.md` prose only, with no `repos/quantik-qfen-visualizer.md`.
2. **The seed-dependent finding is recorded here rather than re-litigated.**
   `PolicyAgent` defaults to argmax and `NetMCTSAgent`'s RNG only ever fed
   disabled Dirichlet noise, so every arena number published before this was
   discovered (2026-08-29) came from random starting positions only, never a
   seed-varied network. This does not invalidate published margins; it narrows
   what "reproducible with a different seed" means for them.
