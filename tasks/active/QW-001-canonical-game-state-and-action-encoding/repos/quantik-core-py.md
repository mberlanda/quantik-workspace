# quantik-core-py task

Objective: implement a repository-owned adapter over existing public APIs, without changing semantics silently. Focus on QFEN/state, move generation, symmetry transform/move mapping, canonical bytes, ML data, and portability reporting.

Preserve the user's current dirty release checkout. Add focused tests for valid cases, invalid states, D4/action mapping, deterministic serialization, masks, and value perspective. Run `./auto-lint.sh` and `./dev-check.sh`. Handoff must record full commit, dirty-state, exact contracts source/ref, output report, and classified differences.
