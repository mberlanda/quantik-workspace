# W2 — Extend the registered schema and its fixtures

**Repository:** `quantik-core-contracts` · **Branch:** `feat/engine-response-candidates` · one PR
**Depends on:** W1 merged and reviewed. **Dispatch:** mechanical.

## Steps

1. `schemas/engine-response-v1.json` — add the fields W1 specifies. `certainty` is **required**
   with `enum: ["estimate", "proof"]`. Candidates and PV per W1 sections 1-2.
2. Adding a required field to a registered schema breaks existing payloads. Apply W1 section 5:
   if the design says older servers stay valid, `certainty` cannot be required at the top level of
   the same version — implement whatever W1 decided (a new version, or a required field with a
   documented migration). **Do not silently invent a third answer**; if W1 is ambiguous here, stop
   and send it back. This is the one place this item can go quietly wrong.
3. `fixtures/engine-response/*.jsonl` — add rows covering: a candidate list with visit-unit scores,
   one with logit-unit scores, an exact-oracle response with `certainty: proof`, a network response
   with `certainty: estimate`, and a response with a principal variation.
4. `docs/engine-response-v1.md` — keep the prose and the schema in agreement.

## Completion criteria

```sh
python -m pytest -q
quantik-workspace validate contracts
quantik-workspace validate fixtures
```

- Every new fixture validates; the checked count increases.
- The existing QW-019 fixtures still validate, or the migration W1 specified is implemented and
  documented.

## Handoff

Record the fixture counts and how backward compatibility was handled.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
