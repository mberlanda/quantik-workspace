# ADR 0010: A Single Opponent Registry, Classical Engines Included

## Context
The play service must offer classical engines and trained models as opponents to a
human, with results comparable to the arena's published benchmarks rather than a
separate dataset needing reconciliation.

## Decision
One factory, `arena.registry.build_agent(spec)`, constructs every agent kind — random,
minimax, mcts, beam, uniform-mcts, and every trained model — behind one
`Agent.select(board, seed)` interface. `play.opponents.roster()` serves all of them
through it, using the same opponent ids (`model@simulations`, e.g. `cpool@128`) that
`arena.match` and `arena.autoplay` already stamp into `games.json`.

## Alternatives
A separate, handcrafted opponent list for the play service — rejected; it would produce
two datasets needing translation before a human-vs-`cpool@128` win rate could be pooled
with a benchmark number. Route classical engines through `quantik-api-rust` and only
trained models through the Python play service — rejected as the status quo split this
registry collapses.

## Consequences
A game recorded by the play service and a benchmark game recorded by the arena name the
same opponent the same way, so they pool without translation. Stated plainly: this makes
`quantik-api-rust` redundant for playing, though not for its other roles.
