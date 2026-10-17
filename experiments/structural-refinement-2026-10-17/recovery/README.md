# Structural refinement recovery archive — 17 October 2026

These immutable archives preserve every committed maker attempt through arch `cf50296ae965`, fern `e45768ed964c`, and conifer `387735baa33d`. They are recovery evidence, not acceptance decisions. Original commit identities and per-commit asset changes are retained. The original rejected screenshots, source, models, logs, reports and later revisions can be recovered from the Git history inside each bundle.

## Scope and storage

- The baseline is `92f4c4ab73df2f4d0ee3ef66ea9cc0b810d3a6b6` in `s010s/lowpoly-vault`.
- Each archive contains only commits after its required baseline. Every changed path was checked to be inside that asset's experiment directory. Baseline history is a prerequisite, not duplicated into these bundles.
- Conifer `387735baa33d` is incremental and requires the `df678f6af898` archive to be imported first.
- GitHub stores bundles as ordered parts smaller than 8 MiB to stay below the connector's 16 MiB request-body limit. Google Drive stores the same full bundle bytes and a companion ZIP of these instructions/manifests.
- These are 16 original commits in total: arch 6, fern 4, conifer 6. Existing earlier recovery backups remain untouched.
- Historical asset authors and committers, and this recovery publication, use `Leon Made This <8357465+s010s@users.noreply.github.com>`.
- Common credential signatures and sensitive filenames were scanned across changed blobs; none were found. This is a bounded scan, not a guarantee of absence.

## Restore from this GitHub branch

1. Clone `https://github.com/s010s/lowpoly-vault.git` with the branch `backup/structural-refinement-recovery-20261017` and full history. Do not use `--single-branch` for a later workflow that needs other remote branches.
2. Enter `experiments/structural-refinement-2026-10-17/recovery/`.
3. Run `sha256sum -c SHA256SUMS` (macOS: `shasum -a 256 -c SHA256SUMS`).
4. Run `python3 restore.py --repo ../../../`. It verifies parts, reconstructs exact full bundles, verifies the full-bundle checksum, imports each into a new `recovered/<asset>-<commit>` ref, and checks every archived changed blob against the manifest.
5. Inspect a recovered branch with `git log recovered/conifer-387735baa33d`, or create a separate worktree with `git worktree add ../recovered-conifer recovered/conifer-387735baa33d` from the repository root.

The script never overwrites a maker or main branch. It refuses a mismatched existing bundle, failed checksum, missing prerequisite, or divergent existing recovered ref. A matching already-imported recovered ref is safe to reuse.

## Restore from owner-only Google Drive

Download the four `.bundle` files and the companion recovery-instructions ZIP into one directory. Extract the ZIP there, preserving the manifests, `index.json`, and `restore.py`. First clone the GitHub repository containing the baseline. Then run `python3 restore.py --repo /path/to/clone`. Full bundle checksums are verified directly; the GitHub parts are not needed for this route. Check `index.json` for dependency order. This archive intentionally depends on the established GitHub baseline and is not a self-contained backup of every past repository revision.

## Verification performed

Each bundle passed `git bundle verify`. A new bare receiver was seeded only with the required baseline snapshot, then all four bundles were imported in dependency order. All 16 commits and all 1,247 per-archive changed-blob checksum entries were validated; `git fsck --full --no-dangling` passed. `restore-verification.jsonl` records the results. A separate parts-only reconstruction test verified the exact assembled bundle SHA-256 values. GitHub's returned blob SHAs were checked against locally calculated Git blob SHAs before publication.

The manifests contain the full SHA-256 of each bundle and part, Git blob identities, source branch/tip, prerequisite commit, all changed paths for every commit, and content checksums for archived changed blobs. Use the full hashes when validating recovery.
