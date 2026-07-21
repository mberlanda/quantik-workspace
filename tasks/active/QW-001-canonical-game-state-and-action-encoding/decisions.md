# QW-001 Decisions

Open decisions:

1. Is canonical equivalence D4 × shape permutation only, or does any interface include colour swap?
2. How is a move/action mapped to and from every canonical transform?
3. Does terminal include blocked-side loss in every contracted operation, or only board/game APIs?
4. Which invalid-state checks are required at parser, state constructor, and adapter boundaries?
5. Is the canonical 18-byte key the portable identity, with numeric language hashes explicitly excluded?
6. Does a self-play legal mask mean all legal actions or only actions with positive visits?
