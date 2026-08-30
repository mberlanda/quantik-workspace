# QW-021 Decisions

1. **The new partition is designed before any labelling starts.** Rejected: label
   everything, then work out what to hold out. Once plies 4-6 are in the training set,
   no amount of later partitioning restores an untouched probe — the choice would be
   made by an accident of ordering.

2. **The old 99.63% figure is scoped, not deleted.** It was a true measurement of a real
   partition. The write-up should say which partition, and that the partition no longer
   exists. Rejected: quietly restating the number against the new split, which would
   present two different measurements under one label.

3. **Arena evaluation is required, not optional.** Held-out accuracy has failed to
   predict play strength four times here, most explicitly in the v3 corpus result. A
   coverage change that improves accuracy and is never played is not evidence.

4. **The opening book still answers in the opening.** Rejected: using a better-covered
   network there. The book is exact; the network would at best approximate it. Coverage
   is for the *network's* competence in the region, which matters for search quality and
   for positions the book does not reach, not for replacing a solved answer.

5. **Sequenced after QW-012.** Rejected: running them together to save wall-clock.
   That confounds corpus with epoch budget — the exact confound QW-012's packet already
   records for `patience-cpool-v2`.

6. **A smoke run precedes the full solve.** The project has paid twice for estimates
   taken from a differently-shaped workload; a per-level throughput measurement on a
   real slice is the only usable number.
