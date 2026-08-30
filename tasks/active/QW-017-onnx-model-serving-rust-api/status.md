# QW-017 Status

**decision-superseded-not-started.** No inference code exists.

Verified 2026-08-30:

- `quantik-api-rust` is at `f814093` on `main`, in sync with
  `git@github.com:mberlanda/quantik-api-rust.git`. It has four commits and one document.
  (The long-repeated claim that this repo has no remote is false; see
  [`QW-022`](../QW-022-workspace-repo-hygiene/initiative.md).)
- `docs/model-serving.md` still reads "Status: **decision not yet made.**" and still
  recommends candle.
- `02bfcd1` is the encoding correction, and it is pushed.

Next action: rewrite `docs/model-serving.md` and write the Rust-runtime ADR. That is a
documentation change with no dependencies and it unblocks every other criterion.

Full history: [`workstreams-archive.md`](../../../docs/history/workstreams-archive.md) §4 and §9.
