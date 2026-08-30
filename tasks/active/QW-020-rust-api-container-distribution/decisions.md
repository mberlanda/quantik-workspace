# QW-020 Decisions

1. **GHCR over Docker Hub as primary.** Docker Hub applies anonymous pull rate limits
   that bite CI; `ghcr.io` is free for public images and tied to the repository that
   builds them. Rejected: Docker Hub primary — the rate limit is a CI failure mode that
   appears under load, which is the worst time to discover it.

2. **Multi-arch, `linux/amd64` and `linux/arm64`, via `buildx`.** arm64 is not a
   nice-to-have: local development is arm64, and an image the author cannot run is an
   image nobody smoke-tests.

3. **Multi-stage onto distroless or scratch.** A Rust binary needs no runtime;
   shipping a distro base ships a CVE surface for nothing.

4. **The base image ships before QW-017.** Rejected: waiting for model support so the
   first image is the interesting one. The classical engines are already worth serving,
   and a working publish pipeline is easier to extend than to build under pressure later.

5. **The naming stays honest.** The contract is authoritative; the container is a
   distribution artifact. Do not name or document the image as though it defines the
   engine interface — that is `engine-request` / `engine-response`, which
   [`QW-019`](../QW-019-engine-api-contract-registration/initiative.md) registers.

6. **Whether this or QW-009 is *the* public deployment is deliberately left open here**
   and is criterion 4. Recorded now: they are not interchangeable — QW-009 serves the
   networks today and this does not.
