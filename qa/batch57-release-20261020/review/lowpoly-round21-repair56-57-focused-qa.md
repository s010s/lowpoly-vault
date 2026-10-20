# Focused differential QA: Cycadeoidea r003 and Quatsinoporites r004

Date: 2026-10-20 UTC  
Scope: two targeted corrections only. Read-only review of the repair worktrees and exact fixed-eight image sets, with a fresh Blender source-geometry inspection. This audit made no candidate or state changes; the maker’s revisions and local commits are described below. No remote push, PR, or merge was made.

## Disposition

The two narrow visual blockers identified in the earlier audit appear corrected in the named revisions. This is focused evidence, not formal acceptance of either candidate. Both `candidate-validation.json` records remain `approved_for_brief: false`, all required approval stages remain unknown/pending, and GPU/scene are explicitly unrun. No publication authority is implied.

## Cycadeoidea r003

- Worktree/branch: `/workspace/shared/lowpoly-round21-repair56-20261020`, `repair/batch56-three-pockets-20261020`; original base `5485316a065c2e63e64f7b9f7087b49eb9f1afda`; final local commit `1e90635f5d3bc9940f23fb17d3d581cd8f409170` retains the new revision and execution/rebuild logs. Worktree was verified clean. No remote push or PR was made.
- Selected model: `assets/candidates/continuous-small-life-round21-20261020/batch-56/cycadeoidea/r003/model.glb`, 297,776 bytes, 5,296 triangles, SHA-256 `d326b3d5f2c3e14256d56afaf444db61b7f14963dc9cb0105aece89c5545cedf`.
- Brief preserved: `r003/brief.json` SHA-256 `565e599fe3326edcfe53774d1da297c7c44623cbc83db884c068bb0154aa91e4`, matching the repair handoff’s predecessor brief pin.
- Pixel inspection: the exact-GLB fixed-eight sheet and individual hero/clay images show exactly three distinct recessed sites on the trunk, each visibly open and recessed. The full eight PNGs each match their `proof-final/render-manifest.json` byte length and SHA-256; the manifest’s `source_glb_sha256` matches the selected GLB.
- Fresh source-geometry check: opened `source.blend` in Blender 4.3.2 without saving. `embedded_reproductive_recesses` has exactly three connected mesh components, each with 62 faces. The generator uses one three-entry pocket list to drive both trunk-core recess geometry and armor omissions as well as the three cups. This independently confirms three—not four—sites in the editable source, not merely a painted/render-only count.
- Relevant maker evidence is hash-bound to the same GLB: static GLB, source/export, Khronos, Node parser, two queue-bound rebuild reports, and candidate validation pass. I reviewed those reports but did not repeat unrelated automated jobs. GPU and scene remain unrun.

## Quatsinoporites r004 (selected; r003 not selected)

- Worktree/branch: `/workspace/shared/lowpoly-round21-repair57-20261020`, `repair/batch57-irregular-pores-20261020`; original base `c49dded6cbfc89429800933d39f8a0b1c2b3db81`; final local commit `75f08656c73718ad707c0493e9bf8137f3efb45d` retains the new revisions and execution/rebuild logs. Worktree was verified clean. No remote push or PR was made. The failed cutter-top r003 attempt remains separate; this audit concerns r004 only.
- Selected model: `assets/candidates/continuous-small-life-round21-20261020/batch-57/quatsinoporites/r004/quatsinoporites.glb`, 94,332 bytes, 2,216 triangles, SHA-256 `22e3a5e8c35086c7931b25f9caa5198c5d533f379c8f080311e6bcd1b0b6ec4b`.
- Brief preserved: `r004/brief.json` SHA-256 `1d4c516bd4dbb5cd893615f785a35f5b5a7bcc894c8404e174a00cb39813a64f`, matching the handoff’s predecessor-brief pin.
- Pixel inspection: the actual exact-GLB eight-view sheet, especially top and clay, shows distinctly varied pore diameter/ellipticity and spacing with no obvious regular lattice. Openings remain structurally recessed rather than painted dots. All eight proof PNGs match their manifest hashes and byte lengths; `source_glb_sha256` in the manifest equals the selected GLB.
- Fresh source-geometry check: opened `quatsinoporites.blend` in Blender 4.3.2 without saving. I regenerated the frozen-seed candidate-center sequence (43 pores) and BVH-raycast the actual source mesh vertically at every center. All 43 rays hit below the top skin at z=0.0060–0.0099 m while the slab top is z=0.027 m, confirming openings through the top surface that terminate at blind floors. The mesh has 0 non-manifold edges (1,710 total edges), consistent with closed blind-cavity geometry rather than uncapped holes.
- Relevant maker evidence is hash-bound to this exact r004 GLB: static GLB, source/export, Khronos, Node parser, two queue-bound rebuild reports, and candidate validation pass. These maker reports were reviewed, not treated as my own executions. GPU and scene remain unrun.

## Preservation and evidence boundaries

- Both current `delivery-checksums.sha256` manifests passed locally after final log commits: 84/84 files for Cycadeoidea r003 and 75/75 for Quatsinoporites r004.
- Both final worktrees are clean. A direct base-to-head Git diff shows only additions (85 new files for batch 56, 131 for batch 57), with zero modified or deleted existing files. The new revisions and logs are committed locally only, and the prior selected Cycadeoidea r002 GLB remains `9388a918314ca5426c992d9f1702e881d369bc5a15ad43d5dce18afcf80c0fd0`; prior Quatsinoporites r001 remains `8d1dbd00dab4303b667d48048d5a8df737f07cb54d53a8173bb72fc025d622c2`. These hashes were recomputed from the final local commits’ Git blobs and match the original pins. The old selected model files and their briefs were not overwritten.
- Candidate/repair attestations report requested maker dispatch as GPT-6.1 Sol Medium; effective runtime model is not exposed. Exact provider generation times remain unknown. The proof images are static proof, not GPU/target-scene evidence.

## Suggested next step

Use the exact r003/r004 pins above for a fresh, focused independent visual/spec review if the parent wishes to advance them. Keep approval and publication pending until all formal acceptance stages are explicitly reviewed and recorded.
