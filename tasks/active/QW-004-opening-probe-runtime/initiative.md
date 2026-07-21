# QW-004: Opening Probe Contract and Runtime

Define the compact runtime boundary between the SQLite opening-book source and
search/self-play consumers. The contract must make canonical key identity,
value/bound meaning, action orientation, versioning, and unsupported data
explicit before the Rust abstraction is implemented.

This is not a new book builder or a model runtime. It is a portable probe
surface with deterministic conversion and fail-fast compatibility behavior.
