# QW-013 Decisions

Recorded, not open — the brief already made these calls:

1. **The ply cut-off is 6**, matching `autoplay --max-solve-ply`.
2. **`--corpus` is optional.** With none given, every distinct position is
   exported and `summary.json` records a null `filtered_against` rather than
   silently exporting nothing.
3. **Exit code:** non-zero on a missing database; zero on an empty filtered
   queue — "every position is already known" is success, not failure.

One open item, found 2026-08-30, not in the brief:

4. **This session found the implementation already present, untracked, in the
   working tree — not written by this reconciliation task.** Whoever picks this
   packet up next should check its current state before starting (it may already
   satisfy every acceptance criterion, or may have moved since 2026-08-30) rather
   than assuming a blank slate.
