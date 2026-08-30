# QW-019 Decisions

1. **Contract-first, with CI asserting the implementation matches.** Rejected:
   `utoipa` generating the spec from the Rust handlers. That inverts the source of
   truth — the spec would then describe whatever the handlers happen to do, and a
   handler bug becomes a spec change. It also privileges one of three implementations.

2. **OpenAPI 3.1 is preferred over a bare JSON Schema pair**, because 3.1 is JSON
   Schema 2020-12 compatible — so nothing is given up — and it additionally describes
   the routes, which enables client generation for the visualizer and any future
   consumer. Recorded as preferred, not yet final; criterion 2 requires the decision to
   be written down either way.

3. **The naming question is opened, not pre-decided.** Dropping `quantik.` matches
   every other registered contract. Keeping it avoids breaking deployed clients that
   pin the string. Whichever is chosen must be recorded here with its migration.
   Rejected as a non-option: registering under the convention-violating name and never
   mentioning it, which is what would happen by default.

4. **All three implementations validate, including `quantik-models-py`.** Rejected:
   registering the schema and validating only in Rust. A contract validated by one of
   its three implementations is a contract that describes one implementation.
