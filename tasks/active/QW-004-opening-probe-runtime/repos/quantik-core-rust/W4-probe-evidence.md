# W4 — Cross-produced evidence

**Repository:** `quantik-core-rust` · **Branch:** `test/opening-probe-evidence` · one PR
**Depends on:** W3 merged. **Dispatch:** execute and record.

Acceptance criterion 4 asks for evidence across hits, misses, corrupt data, incompatible versions
and transformed moves — produced by running, not by assertion.

## Steps

1. Build a probe from a real opening book with `probe_builder`, not a synthetic fixture.
2. Exercise all five cases against it and capture real output for each.
3. For transformed moves, verify a sample of returned actions are legal in the **caller's**
   orientation using `quantik-core`'s own move generation. An action that is legal only in the
   representative's orientation is the exact defect being hunted; state how many you checked.
4. Record the transcript in `crates/quantik-core/tests/opening_probe.rs` as a documented
   integration test, or in the repository's docs if it is too slow for the default suite — say
   which you chose and why.

## Completion criteria

- All five cases have real captured output.
- The legality check names the number of sampled actions and the result.
- `cargo test` clean.

## Handoff

Record the probe source, entry count, and the five transcripts.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
