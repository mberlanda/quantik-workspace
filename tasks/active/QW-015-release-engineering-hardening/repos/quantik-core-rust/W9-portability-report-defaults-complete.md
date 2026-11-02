# W9 — Same fix for the Rust portability adapter

**Repository:** `quantik-core-rust` · **Branch:** `fix/portability-report-defaults` · one PR
**Dispatch:** mechanical. The Rust half of W8; the two are independent and can run in parallel.

```
command failed (2): cargo run --bin quantik-portability-report --
error: the following required arguments were not provided:
  --contracts-root <CONTRACTS_ROOT>
  --output <OUTPUT>
```

## Steps

1. `--contracts-root` defaults to the sibling checkout (`../quantik-core-contracts` relative to
   the repository root) when omitted; if absent, fail naming the attempted path and the flag.
2. `--output` defaults to stdout when omitted, so the workspace's declared command works as-is.
3. Both flags keep working exactly as now. Additive only.
4. Test both defaults and both explicit forms.

Match W8's behaviour exactly — the same defaults, the same error text shape. Two adapters that
default differently would reintroduce the divergence this initiative is about.

## Completion criteria

```sh
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
cargo run --bin quantik-portability-report          # must now succeed
```

- The bare invocation exits 0 and prints valid JSON to stdout.
- Behaviour matches W8's; state that you read W8's packet.

## Handoff

Paste the bare invocation's output and confirm it matches W8's shape.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
