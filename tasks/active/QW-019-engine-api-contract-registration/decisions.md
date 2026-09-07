# QW-019 Decisions

## Recorded, not open

### D1

**Contract-first, with CI asserting the implementation matches.** Rejected: `utoipa` generating
the spec from the Rust handlers. That inverts the source of truth — the spec would then describe
whatever the handlers happen to do, and a handler bug becomes a spec change. It also privileges
one of three implementations.

### D2

**Register a JSON Schema 2020-12 pair. An OpenAPI 3.1 document is additive, and separate.**

Settled 2026-09-07, refining the earlier "OpenAPI 3.1 preferred" note. The reason for that
preference — 3.1 is JSON Schema 2020-12 compatible, so nothing is given up, and it enables client
generation — is real, but it does not survive contact with the registry: `contracts.json` entries
carry `schema: "schemas/<name>-v1.json"`, and `validate fixtures` validates every fixture row
against that file. An OpenAPI document is not a JSON Schema and cannot go in that slot, so
choosing it means either registering payload schemas anyway or changing the registry machinery
for two contracts out of sixteen.

So: the payload schemas are what gets registered, exactly like the other fourteen. The OpenAPI
3.1 document is a **separate, optional deliverable (W5)** that `$ref`s those same schema files
and adds only the route description. Because 3.1 is 2020-12 compatible the `$ref` is legal, the
schemas stay the single source of truth, and client generation is available to anyone who wants
it without the registry growing a second toolchain.

### D3

**Drop the `quantik.` prefix. The registered names are `engine-request.v1` and
`engine-response.v1`.**

Settled 2026-09-07. All fourteen registered contracts are bare (`qfen.v1`, `observation.v1`,
`model-checkpoint.v1`, …). Amending a convention that holds fourteen times to accommodate two
newcomers costs more than renaming the newcomers, and the prefixed strings are not yet load-bearing
anywhere outside this workspace: `quantik-api-rust` has never been tagged, and the visualizer is
served from the same deployment as the API it talks to.

**Migration.** Servers accept both spellings for one minor cycle and always *emit* the bare name:

- `quantik-api-rust` and `quantik-models-py`'s play service accept `engine-request.v1` **and**
  `quantik.engine-request.v1` on input, starting in the release that carries this initiative.
- Both emit `schema: "engine-response.v1"` from that same release. Nothing emits the prefixed
  form again.
- The prefixed spelling is rejected on input starting at the **next** minor after that. Removing
  it is not part of this initiative; the acceptance is written so that deleting one branch and
  its test is the whole future change.

### D4

**All three implementations validate against the registered schema in their own suites**, including
`quantik-models-py`. Rejected: registering the schema and validating only in Rust. A contract
validated by one of its three implementations is a contract that describes one implementation.

### D5

**W1 captures the format that is actually spoken; it does not redesign it.**

The two implementations do not emit identical optional fields today. Capture real payloads from
both and let the schema accept the union, recording in the docs which implementation emits which.
Reconciling them is a real question, but it is `QW-018`'s (engine response type: candidates, PV,
certainty), not this one's. A registration PR that also changes a payload is a rewrite wearing a
registration's clothes.
