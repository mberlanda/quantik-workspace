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
