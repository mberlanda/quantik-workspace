# quantik-core-py adoption

Preserve the existing dirty `release/v1.2.0` checkout. Resolve `.github/workflows/contracts.yml`: the advertised `actions/validate-contracts` path is absent, and current refs/expectations are 1.1.0. During candidate work, check out contracts source and invoke relative actions; after producer verification, pin exact `@v1.2.0`, update expectations/declarations/live fixtures, run `./auto-lint.sh` and `./dev-check.sh`, and record the full commit and evidence.
