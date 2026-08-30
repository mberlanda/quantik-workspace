# QW-014 Decisions

Recorded, not open — this initiative documents decisions already made and
executed:

1. **Shared learning rate is wrong; shared protocol is right.** ADR 0001 was
   amended: the same LR grid at the same budget for every architecture, best
   validation result entering the comparison, rather than one literal rate.
2. **A tie does not buy more epochs**, and **`T_max` stays the cap rather than
   being rescaled** — both carried forward as constraints on QW-012.
3. **One repo per architecture on Hugging Face**, not one monorepo — because
   `model-index` is per repository, so a monorepo would misattribute metrics to
   architectures that did not produce them.
4. **A second training seed is deliberately deferred**, twice now — once during
   the learning-rate flaw, once for v3 — with the same stated reason: replicating
   a possibly-unfair configuration is the wrong thing to spend compute on. Seeds
   come after the protocol is settled, not before. QW-012 is that settling; a
   second seed remains open *after* QW-012, not as part of it.

One open item this initiative surfaces rather than resolves:

5. **Whether the published model should optimise arena strength or held-out
   accuracy** is explicitly undecided in `WORKSTREAMS.md` §11, ahead of any Hub
   revision. Not this initiative's call to make.
