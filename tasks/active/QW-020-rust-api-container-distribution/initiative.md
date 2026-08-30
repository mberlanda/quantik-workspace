# QW-020: Container Distribution for the Rust API

> **Purpose:** Ship `quantik-api-rust` as a container, and settle whether it or the
> Python play service is the public deployment.
> **Load with:** [`context/repositories/quantik-api-rust.md`](../../../context/repositories/quantik-api-rust.md),
> [`context/system/release-model.md`](../../../context/system/release-model.md)

## Problem and motivation

The gateway exists and runs the classical engines. It ships as source.

This section was blocked for weeks on a claim that turned out to be false — that
`quantik-api-rust` has no git remote, so there is nothing for CI to build from. It has
one. `origin` is `git@github.com:mberlanda/quantik-api-rust.git`, local `main` is in
sync at `f814093`, and this was verified three ways on 2026-08-30: `git remote -v`,
`git ls-remote origin HEAD` matching local `HEAD`, and the public GitHub page. The
correction is kept visible in [`QW-022`](../QW-022-workspace-repo-hygiene/initiative.md)
because it propagated into the root `CLAUDE.md` and shaped a delegation plan.

## Existing and desired behaviour

Existing: `cargo run`, on a developer machine, from a checkout.

Desired: `docker run ghcr.io/mberlanda/quantik-api:X.Y.Z` on amd64 or arm64.

## Contracts and repositories

`quantik-api-rust` only. No contracts. The *contract* is authoritative and the container
is a distribution artifact — the naming should keep that straight and not imply the
image defines anything.

## The decision this initiative forces

[`QW-009`](../QW-009-public-play-deployment/initiative.md) containerizes the **Python**
play service, which serves all four models plus the classical engines through one
opponent registry, plus the visualizer, storeless. This initiative containerizes the
**Rust** gateway, which today serves the classical engines only and gains models with
[`QW-017`](../QW-017-onnx-model-serving-rust-api/initiative.md).

Two containers for one purpose is a choice, not a consequence. QW-009 is further along
and answers the request that prompted it. This packet's honest justification is a
single static binary with no Python runtime and a much smaller image — a real
distribution benefit, and not a reason to duplicate the play experience.

Criterion 4 exists so that this is decided rather than drifted into.

## Ordering

The base image does **not** depend on QW-017 and should ship first — it is small,
demonstrable, and independently useful. The `-model` variant depends on QW-017.

## Provenance

Migrated from WORKSTREAMS §8 ("Dockerize the API — NOT STARTED"), including its
correction.
