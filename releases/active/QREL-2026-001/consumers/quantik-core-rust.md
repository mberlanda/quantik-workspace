# quantik-core-rust adoption

Source, crate, and live fixtures already say 1.2.0. `.github/workflows/rust.yml` still uses opening-book consistency `@v1.1.0` with expected 1.1.0. Add source-mode candidate coverage without future-tag dependency, then pin verified `@v1.2.0`. Resolve the missing-`Cargo.lock`/`--locked` policy separately. Run fmt, clippy, tests, and compatibility evidence.
