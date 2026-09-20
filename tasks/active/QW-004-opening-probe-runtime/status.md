

## 2026-09-20 — W2 merged

[contracts#30](https://github.com/mberlanda/quantik-core-contracts/pull/30) registers `opening-probe.v1` (`schemas/opening-probe-v1.json`, `contracts.json` entry, a stdlib reference probe in `validate_contracts.py`, 5 valid rows and 22 invalid cases, two clarifying sentences in `opening-book-v1.md`). `allowed_paths` widened to `scripts/validate_contracts.py` and `tests/test_contracts_validator.py`, as with QW-018 W2.

- **Fixture format decided in W2** (the W1 paper had prose only): each JSONL row is a decoded probe file `{header, records, file_length?, probe_cases}`, values synthetic. W3 and W4 cross-produce against it; it is written up in `docs/opening-probe-v1.md`.
- **Tension recorded:** the schema is closed (unknown header keys fail fixture validation) while runtime readers must still open a file with a newer optional key. Adding a key is a schema change and a minor release.
- The validator reimplements legality; it is now cross-checked against the engine-request and search-summary fixtures and `quantik_core` (checked by the coordinator with jsonschema and `quantik_core` installed: 54 tests, none skipped). The agent's own venvs skipped one or the other.
- Contracts CI runs only the validator; the test suite is local evidence.
- W3 needs `find_canonical_with_transform` in core plus a Python analogue.
