# ADR 0012: Storeless-First Public Deployment

## Context
A public deployment needs to be shareable before it is known whether the games it would
collect are worth collecting.

## Decision
`python -m quantik_models.play --no-store` opens no database and never creates the file;
`POST /api/games` answers 503 in that mode. Storage is deferred deliberately, and the
server needs nothing new to run this way — it already does.

## Alternatives
Ship with a store enabled by default and add an opt-out — rejected; that makes data
collection the default posture of a public-facing service before its value is
established. Defer the whole deployment until the storage question is settled —
rejected; serving moves and analysing positions do not depend on it, so gating on it
would delay everything else for no benefit.

## Consequences
The client must learn from `GET /api` that no store exists and stay quiet, rather than
surface a storage error to a visitor. Adding a store later is a separate decision, not a
default to restore casually.
