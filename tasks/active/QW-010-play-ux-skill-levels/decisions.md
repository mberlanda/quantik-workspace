# QW-010 Decisions

Open decisions:

1. How many levels — three (easy/medium/hard) as requested, or more, once the
   arena numbers are actually laid out and the gaps between adjacent opponents
   are seen?
2. Does a level pin one fixed opponent, or a narrow band the service samples
   from, to avoid a player memorizing one engine's exact behavior?
3. Does the mapping hold search budget fixed within the roster (e.g. always
   128-sim MCTS) and vary only architecture, or vary both?

Recorded, not open:

4. **`quantik-qfen-visualizer` is not a formal `affected_repositories` entry.**
   Same reasoning as QW-008/QW-009: it is not registered in `workspace.yaml`.
   The UI half of this initiative is real future work, described in prose only.

## Serving decision, 2026-08-30 — blocked on one measurement

Following the v3 investigation and [ADR 0014](../../../docs/adr/0014-corpus-coverage-and-epoch-budget-are-separate-axes.md).

1. **No v3-corpus checkpoint is served or published on current evidence.**
   `runs/play/models/` already carries live symlinks for `cpool-v3`,
   `patience-v2` and `patience-v3` beside the published four. They stay local
   staging: out of the skill-level mapping, off the Hub.

   The reason is not that `cpool-v3` is weak — it is the only checkpoint in the
   family that beats `minimax-d2` from a ply-3 start (59.7% and 60.2% across two
   arena seeds, against the published `cpool`'s 48.9% tie), and it improves in
   both seats. The reasons are that **nothing in the evidence picks it over
   `patience-cpool-v2`**, which matches it on every metric and every arena board
   at matched budget, and that **its ranking is depth-dependent** — first at ply
   3, mid-field at ply 6, indistinguishable at ply 9. A model with no single
   position in a strength ordering cannot be assigned a skill level.

2. **The skill-level ordering must be sourced from an arena that starts at ply 0
   and ply 1.** No arena on disk starts before ply 3. Every start ply recorded
   in `runs/arena/*.json` and `runs/eval/*/*/games.json` is 3, 4, 5, 6 or 9. At
   ply 0 every checkpoint is uniform to three decimal places — measured max legal
   prior 0.016-0.023 — so the regime a human game actually begins in is
   **unmeasured for every model in the family**, published or not.

   Deriving skill levels from ply-3 numbers would rank opponents on a phase of
   the game the player does not start in.

3. **Rejected: serve `cpool-v3` now as an extra difficulty.** It is the least
   effort and it is what the symlink directory already implies. Rejected because
   choosing it means choosing the 16-epoch checkpoint of a corpus increment that
   ADR 0014 finds null, on the strength of an arena that never tested the phase
   where its advantage is claimed to matter.

4. **Rejected: derive levels from the existing ply-3/6/9 tables and re-derive
   later.** A published skill ladder is hard to change once players have opinions
   about it, and the ply-0 arena is one run rather than a research programme.
