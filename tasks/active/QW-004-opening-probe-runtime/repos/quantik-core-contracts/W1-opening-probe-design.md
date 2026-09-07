# W1 — Design `opening-probe.v1`

**Repository:** `quantik-core-contracts` · **Branch:** `docs/opening-probe-design` · one PR
**Dispatch:** judgment — capable model, human review before W2.

Opening-book data exists, but there is no compact probe contract and no symmetry-safe runtime
abstraction. This item decides the contract and writes it down. It registers nothing.

The correctness risk is orientation. Per `context/system/canonical-invariants.md`, the canonical
key is D4 (8 transforms) × 24 shape permutations = **192 symmetries**, the representative is the
lexicographically least serialized payload, and durable identity is the serialized bytes rather
than a language-native hash. A probe that returns a move in the representative's orientation
without transforming it back returns a legal-looking, wrong move — silently.

## Decide and record in `docs/opening-probe-v1.md`

1. **Probe keys.** What identifies a position — the canonical key, in exactly which serialization.
   Byte-level, not "the canonical key".
2. **Values and bounds.** What a hit returns (value, best action, both), the value range, and what
   an unknown/absent entry is. Distinguish "not in the book" from "in the book, drawn/unknown".
3. **Move and action transforms.** The exact rule for mapping a stored action back into the
   caller's orientation, and which direction each transform runs. Include a worked example with
   real numbers: a position, its representative, the stored action, the returned action.
   `action = shape * 16 + position`, `ACTION_COUNT = 64`
   (`context/system/canonical-invariants.md#I6`).
4. **Metadata.** What the probe file records about how it was built — source book, ply coverage,
   entry count, producing version — so a stale probe is detectable rather than merely wrong.
5. **Errors.** The taxonomy: corrupt data, truncated file, incompatible version, key not found.
   Which are fail-fast and which are ordinary misses. Fail-fast is the default; say where it isn't.
6. **Migration.** How this relates to the existing `opening-book.v1` and
   `opening-book-summary.v1`, and whether either changes. If they do, say exactly how.

## Completion criteria

- All six sections present, each a decision rather than options.
- Section 3 contains a worked numeric example a reader can verify by hand.
- `git diff --stat` touches `docs/opening-probe-v1.md` only.
- The PR is marked as needing human review before W2.

## Handoff

Record the key serialization chosen and any question decided without an obvious right answer.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
