

## 2026-09-20 — W7 merged: every work item is now completed

[contracts#31](https://github.com/mberlanda/quantik-core-contracts/pull/31) records the deadlock demonstration in `docs/consistency-checks.md`. Rust summary at 1.3.0 (sibling main) against a Python summary at 1.4.0, contracts on 1.3.0, no tag: main and the `v1.3.0` tag validators pass; the `v1.2.0` validator (control) fails "summaries differ"; an explicit `--expected-release 1.3.0` and a real one-edge difference still fail, so the check has not gone blind. **Limit:** the summaries are hand-built to the real depth-4 shape (11739 positions, 340680 edges), not engine-generated, and only the validator command ran, not the composite action or a live CI run. Contracts CI does not run pytest.

**Not yet done, so the initiative stays active:** regenerate the compatibility matrix. `supported` is still withheld there because no cross-stack portability smoke has run and both portability adapters exit 2 (workspace.yaml declares them without their required `--contracts-root` / `--output` arguments). That is a separate, unowned fix.
