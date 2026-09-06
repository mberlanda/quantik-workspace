# QW-028 Decisions

1. **Resume `opening` (ply-6 frontier), not `opening5`.** The measured cost
   ladder makes the two nearly equal in wall-clock — about 4.5 hours against
   about 70 minutes for a level 8.5x larger — while ply 6 yields strictly more:
   exact policy at ply 5 as well as ply 4, and exact values one ply deeper.
   Rejected: finishing `opening5` first because it is 60.6% done. Sunk cost is
   not a reason; and if both are eventually wanted, `opening5` is the one that
   stays cheap.

2. **Solve now, merge later.** The solve writes a standalone `.npz` under
   `runs/oracle/` and touches no training corpus, so it carries none of QW-021's
   partition risk. Rejected: waiting for the partition design before starting
   hours of solver time that nothing else is blocked on.

3. **Neither partial directory is deleted or restarted from scratch.** Both
   resume, and `opening5` represents about 3.5 hours of solver time.

4. **Add a progress line to `solve_opening.py`, not a new tool.** The reason two
   abandoned solves sat unnoticed for three days is that "unfinished" was only
   visible by comparing `wc -l` on two files. Printing solved-of-total at start,
   and writing it to a small `progress.json`, makes the state legible. Rejected:
   a separate audit script — the information belongs where the work happens.

5. **Verify the resume before spending the hours.** The resume lives in
   `exact_oracle`'s `already_solved()`, not in the Python, and the Python
   docstring describes it as though it were local. That is exactly the kind of
   split that turns out to be wrong under test, so it gets tested first.
