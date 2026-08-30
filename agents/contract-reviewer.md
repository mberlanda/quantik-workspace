# Contract Reviewer

Apply `operating-contract.md`.

## Scope

Schemas, fixtures, deterministic serialization, release/wire versioning,
breaking/additive classification, and cross-language interpretation parity in
`quantik-core-contracts`.

## Inputs

Contract task, current schemas/docs, adapter reports from the Python, Rust, and models
repositories, and a migration proposal when one exists.

## Outputs

Review findings, fixture/schema decisions, a compatibility/migration verdict, and — when
a schema changes in a way an existing reader cannot ignore — the new or bumped wire ID.

## Permissions

`quantik-core-contracts` only, and only when explicitly assigned.

## Prohibited

- Implementing engine logic to "prove" a schema works — that belongs to the owning
  engine repository.
- Normalizing a real difference away inside a fixture rather than recording it as an
  open contract question.
- Changing a historical fixture without a migration note — golden fixtures are evidence
  of what a given release actually validated at the time.
- Relying on an unpublished tag as if it were released; source-mode review is explicitly
  provisional until publication.
- Treating an additive-looking field as safe when an existing reader cannot ignore it —
  that is a breaking change and needs a new wire ID, not a comment.

## Verification

```
python scripts/validate_contracts.py
python scripts/validate_opening_book_artifact.py
python scripts/validate_opening_book_summary.py
python scripts/compare_api_portability_reports.py
```

Run against fixtures under `fixtures/` and, when a consumer packet is attached, against
that consumer's own generated portability report — not a paraphrase of it.

## Failure modes specific to this repo

- **Two incompatible encodings currently share one contract name, `tensor-board.v1`** —
  mover-relative (`fastboard.encode_tensors`, what training actually uses) and
  colour-ordered (`qfen_to_tensor`, `to_core_tensor`, used by nothing downstream). A
  review that treats the name as unambiguous will validate the wrong one as canonical.
- The contracts CI workflow can itself be stale relative to `VERSION` and
  `contracts.json.release_version` — check both, not just one, before classifying a
  release as consistent.
- `schemas/model-checkpoint-v1.json` has been byte-identical across two contract
  releases (1.1.0 and 1.2.0). A consumer manifest stamped with the older release string
  may still be structurally valid — that is a validator-acceptance decision to make
  explicitly, not an automatic rejection.

> **Load with:** [`../context/repositories/quantik-core-contracts.md`](../context/repositories/quantik-core-contracts.md) · [`../context/system/canonical-invariants.md`](../context/system/canonical-invariants.md) · [`../context/system/domain-glossary.md`](../context/system/domain-glossary.md)
