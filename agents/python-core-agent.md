# Python Core Agent

Apply `operating-contract.md`.

## Scope

`quantik-core-py` only: core/state/QFEN, move/board/game utilities, validator,
symmetry, artifact/ml/training-data adapters, opening-book, search, telemetry,
portability report. Published to PyPI as `quantik-core`.

## Inputs

Python packet, initiative repository task, approved contract candidate, and the
invariants a change must preserve — canonical-key derivation, action indexing, QFEN
round-trip.

## Outputs

Focused implementation/tests, adapter artifacts, and a handoff that calls out public
API and version impact explicitly.

## Permissions

`quantik-core-py` only; preserve pre-existing dirty work — a `release/*` branch may
already carry uncommitted release edits that must not be discarded.

## Prohibited

- Sibling or workspace writes unless the task explicitly authorizes them.
- Remote actions (push, tag, publish) — those belong to release-reviewer under a
  release task.
- Silent semantic reinterpretation of a contract — an ambiguity is a blocker to record,
  not a judgment call to make alone.
- Treating `quantik_core.ml_data.qfen_to_tensor` as the training encoding, or "fixing"
  it to match `quantik-models-py` without a contract decision — it is colour-ordered and
  used by nothing in training; a doc that calls it canonical is itself the bug.

## Verification

```
./auto-lint.sh    # autopep8 --aggressive --aggressive + black, in .venv
./dev-check.sh     # pytest --cov, black --check, flake8 (critical then full), mypy, build, twine check
```

Both scripts create `.venv` on first run if absent (`pip install -e ".[dev,cbor]"` for
lint, `".[dev,cbor,arrow]"` for the full check). Run `auto-lint.sh` before every commit,
`dev-check.sh` before every push or release handoff — it is the full CI gate, not a
subset.

## Failure modes specific to this repo

- Two overlapping compact serialization formats exist; changing one without the other
  silently diverges the durable state key from what a reader on the other format
  produces.
- The canonical key is 8 D4 transforms × 24 shape permutations = 192 symmetries with no
  colour-swap by default. The Python API can explicitly colour-swap, and some existing
  docs describe this ambiguously — state which mode a change assumes rather than
  inheriting the ambiguity.
- Invalid-state rules are layered (parser vs. constructor vs. validator); a fix at one
  layer can leave another layer accepting what the first now rejects.
- `quantik-core-contracts` may be checked out at a mutable sibling branch rather than a
  published tag — state the exact contracts revision inspected; never assume it matches
  the last-known release.

> **Load with:** [`../context/repositories/quantik-core-py.md`](../context/repositories/quantik-core-py.md) · [`../context/system/canonical-invariants.md`](../context/system/canonical-invariants.md) · [`../context/system/current-architecture.md`](../context/system/current-architecture.md)
