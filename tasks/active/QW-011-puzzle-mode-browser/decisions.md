# QW-011 Decisions

Open decisions:

1. Which corpus generates the committed pack — `exact-sampled-v3` (current, per
   the verified `--per-theme 40` run) or a later corpus if one supersedes it
   before this ships?
2. Does the picker group by theme, difficulty, or both?
3. How does the picker present an `already-lost` study differently from a graded
   puzzle, given it structurally has no `solutions` to check against?

Recorded, not open:

4. **`quantik-qfen-visualizer` is not a formal `affected_repositories` entry.**
   Same reasoning as QW-008/009/010: unregistered in `workspace.yaml`. The
   picker UI is described in prose only.
