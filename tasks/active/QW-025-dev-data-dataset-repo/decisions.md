# QW-025 Decisions

1. **A dataset repo, not more model repos.** These artefacts are inputs and
   evidence, not models. A model repo's card format, metadata and `model-index`
   describe a checkpoint, and none of it fits a corpus.

2. **Staging never uploads.** The command prints the `huggingface-cli` line
   rather than running it. Publishing is not reversible the way a local
   directory is, and the staged tree is worth reading before it is pushed.
   Rejected: a `--push` flag — it makes the irreversible step the easy one.

3. **Paths stay relative to the repository root** inside each group, so restore
   is `cp -r corpora/runs/ .` rather than a mapping the reader has to work out.
   Costs some path depth in the repo; worth it.

4. **Six groups rather than one flat upload.** Each has a different cost, a
   different reproduction path, and different rules about use — the probe most
   sharply. One flat tree would lose all of that, and the per-group `README` is
   the actual deliverable.

5. **Checkpoints are included even though four are already published as
   models.** The unpublished ones — the patience family, the v3-corpus runs —
   are the ones that would be lost, and `--init-from` makes them reusable
   starting points rather than dead weight.

6. **A restore must be demonstrated, not assumed.** Criterion 4 exists because
   an untested backup is not a backup. The failure mode is silent: LFS pointers
   download as small text files that look like success.
