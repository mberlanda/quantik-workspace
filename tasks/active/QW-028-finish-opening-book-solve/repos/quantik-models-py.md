# quantik-models-py

## Objective

Resume the ply-6 opening solve to completion and produce `opening-exact.npz`.

## Work items

1. **Confirm the resume.** Run the oracle against the existing `frontier.jsonl`
   for a few seconds; it must report `resuming: N of M already solved` with N
   matching the file's line count.

2. **Progress reporting in `solve_opening.py`.** Print solved-of-total before
   starting, and write `progress.json` beside the JSONL. The reason two solves
   sat abandoned is that their state was only visible by comparing `wc -l` on
   two files.

3. **Run the ply-6 frontier to completion** — 891,916 positions, about 4.5 hours
   on 14 threads, on an idle machine.

4. **Back-induct and write `opening-exact.npz`** through the existing code path.
   Expect 1,019,275 rows across plies 0-6, values exact throughout, optimal-move
   masks exact at plies 0-5 and empty at ply 6 (its children were never solved,
   which the script already encodes).

5. **Cross-check the overlap.** v3 already holds all 726 ply-3 positions and
   part of plies 4-6. Every shared position must agree on value; a disagreement
   means one of the two labelling paths is wrong and is a stop-the-line result.

6. **Do not merge into a training corpus** until QW-021's partition exists.

## Completion criteria

- The resume is demonstrated before the long run, not assumed.
- `opening-exact.npz` exists with 1,019,275 rows and a recorded sha256.
- Every position shared with `exact-sampled-v3.npz` agrees on value.
- `progress.json` makes an unfinished solve visible without counting lines.
- The corpus merge is explicitly deferred, with the reason recorded.
