# Batch07 durable handoff

Candidate branches are independent from production main `ead18cecfc135a26b0d3884a01a04ea36bccf575`. This handoff branch contains records only; it does not merge candidates or publish assets.

Read `final-handoff.jsonl` for complete repository-relative paths and SHA-256 values. Paths refer to the exact candidate commit in each row, not files necessarily present in this handoff branch. `worktree` is only a local convenience; retrieval never requires `/tmp`.

| ID | Remote branch | Exact commit | GLB bytes | Triangles |
|---|---|---|---:|---:|
| syringopora | `refs/heads/candidate/batch07-syringopora-20261018` | `d0894b30b0fbeedb4d946d0d976a4e98abeb5aff` | 155628 | 8020 |
| vauxia | `refs/heads/candidate/batch07-vauxia-20261018` | `fd443ffd5eb8342a11956a574ab11bf73bd5a0ea` | 172096 | 8944 |
| halimeda | `refs/heads/candidate/batch07-halimeda-20261018` | `5ea23624b9e56ccfc4b6700ef9b54774bc5acd6c` | 33188 | 1520 |
| isoxys | `refs/heads/candidate/batch07-isoxys-20261018` | `c017f7acec8027555cadf5a754fa982478bab9f8` | 124252 | 6012 |

Each branch changes only its own asset bundle and corresponding work directory. Syringopora additionally contains the batch07 exclusive `claim.json`; no other asset, CI, site, release, or shared helper changes. The full changed-path list is in `branch-scope.json`.

Each bundle includes `HANDOFF.md`, editable Blend, GLB, deterministic generator/config, frozen inputs, bilingual metadata, cover, eight views and actual-GLB runtime evidence. Independent QA remains pending. Legacy checker failures and zero-turntable contract differences remain recorded in the candidate bundles; no PASS was fabricated.

Retrieve with `git fetch origin <branch>` then inspect `<commit>:<repository-relative-path>` or create a separate worktree at that exact commit.
