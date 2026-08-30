# ADR 0011: Human Game Outcomes Never Become Labels

## Context
The play service records human games, including a client-reported outcome the server
does not fully trust (`play/record.py` replays moves and derives the result rather than
accepting the client's claim). Autoplay already treats engine-vs-engine outcomes the
same way.

## Decision
Only positions travel from a game to the training corpus — from a human game or an
autoplay game alike. A game's winner is never itself a label; positions get their labels
from the exact oracle (`data.exact_corpus`, `data.merge_corpus`), the same as every
other corpus row. `play/store.py` states this directly: "a human's win does not tell the
solver anything an autoplay game against the same opening wouldn't."

## Alternatives
Use the human result as a cheap policy/value signal directly — rejected; a human's
implicit skill is not comparable across players or sessions and duplicates what the
oracle already does exactly on this state space. Trust the client's self-reported
outcome outright — rejected; it is recorded beside the derived one (`client_*` fields),
not in place of it, since a client miscount would otherwise corrupt the same table the
arena writes to with nothing downstream able to tell the two apart.

## Consequences
A human game contributes exactly what an autoplay game contributes: reached positions
for the solver queue, never a bypass around the oracle.
