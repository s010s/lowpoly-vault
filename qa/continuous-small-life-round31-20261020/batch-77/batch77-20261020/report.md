# Batch 77 independent static QA

## Scope and disposition

Reviewed the pinned commit `72a9aed63791e4aca88b837ed701dabd8872b3fd` and only these final candidates:

- `ernietta/r004` — `cf1533f03d458d13d62e3836a01f2cd1470a2e410bfee9ace39f1d90bb6e4da3` — **REVISE (static QA)**. The frozen requirement for a basal zigzag joining seam is not legible in any of the eight required final views. Keep the legitimate incomplete basal-sack fossil scope; do not add the missing trunk or fans. Make the seam visibly readable in a required view.
- `loess-bluff/r005` — `eb824a1302d10cde887467418e7ba2ba38158d37ae95a4a67807b0d1da273c5a` — **ACCEPT_STATIC_QA_ONLY**.
- `rock-glacier/r002` — `a66f2c03cc1f26885209973ea1123c6fda9d3138a9accb38117c60a8e618acc7` — **ACCEPT_STATIC_QA_ONLY**.
- `slump-folded-bed/r003` — `6b28721c6563de8a3510b5b188aa6cb68c1e517ee18887b9d28f9e1c06aea172` — **ACCEPT_STATIC_QA_ONLY**.

These are bounded static-QA findings, not formal acceptance, user approval, publication, release, GPU, or composed-scene approvals. I did not edit producer source, briefs, validators, or candidate files.

## Seven stages, kept separate

| Candidate | Technical | Visual | Factual | Specification | Runtime parse | GPU | Scene |
|---|---|---|---|---|---|---|---|
| Ernietta r004 | Pass | Revise: basal zigzag seam not visible in fixed views | Revise: one required fossil-form feature lacks visible evidence; incomplete basal-sack scope itself is correct | Pass | Pass: fresh Node GLTFLoader 0.180.0 | Not run | Not run |
| Loess bluff r005 | Pass | Pass | Pass: generic loess bluff, no unsupported exact-site claim | Pass | Pass: fresh Node GLTFLoader 0.180.0 | Not run | Not run |
| Rock glacier r002 | Pass | Pass | Pass: generic rubble tongue; no unsupported ice, age, speed, or locality claim | Pass | Pass: fresh Node GLTFLoader 0.180.0 | Not run | Not run |
| Slump folded bed r003 | Pass | Pass | Pass: bounded soft-sediment slump, not claimed as tectonic/metamorphic or exact locality | Pass | Pass: fresh Node GLTFLoader 0.180.0 | Not run | Not run |

“Pass” here is only this static reviewer’s result for the named stage. The Node parse is not browser, hardware-GPU, or composed-scene evidence. No release or formal approval is implied.

## Visual and source review

I personally inspected all 32 original-resolution final 512×512 images, all four lossless contact sheets, all four original concept pixels, and the primary reference pixels: Smith 2017 Ernietta Fig. 3e/f/g, the specific NPS Natchez Milepost 12.4 loess bluff photo, the NPS Sourdough Peak rock-glacier photo, and Alsop & Marco 2012 Fig. 5c/d on page 105. The 32 final frames and four sheets’ hashes, dimensions, and subject bindings were independently checked against the committed render manifests and pixel-inspection receipts.

- **Ernietta:** r004 is a compressed, elliptical, open/truncated ribbed basal sack with an exposed central cavity and modest infill. It does not depict a whole animal; there is no invented trunk, paired fans, legs, roots, or feeding claim. This matches the frozen incomplete-fossil scope. However, the explicitly required basal zigzag seam is not discernible in hero, reversehero, front, side, rear, top, clay, or silhouette. The source generator encodes only a very slight relief and the maker’s own note also calls it understated. This is a specific brief-level visibility gap, not a demand to reconstruct the missing organism.
- **Loess bluff:** the simplified broad fine-silt wall, unequal near-vertical incisions, gullied irregular crest, and subdued apron remain legible. It is an original generic form, not claimed as a measured Natchez replica; no obvious separate column cylinders or tiled face are visible.
- **Rock glacier:** the elongated lobate rubble tongue, subdued unequal curved transverse ridges, irregular facets, and steep rounded toe read coherently. No ice cutaway, mountain backdrop, or mechanical belts/tiles appear.
- **Slump folded bed:** the asymmetrically contorted middle laminae are bounded by more orderly beds and a flatter cap; the chunk remains full depth. It is not presented as metamorphic foliation or a surveyed locality.

I did not impose a zero-intersection or zero-natural-regularity standard. Existing saved-source surface reports, and direct pixel review, showed no visible overlap artifact in the inspected final views.

## Fresh technical and provenance checks

- Pinned worktree is clean at the requested commit. The actual SHA-256 of `production/small-life-batch77/handoff.json` is `ce9f9c7001ba7575608cae2b9592f6ca5b699f9f80418a3dd46788d32a8ded45`.
- Independently rehashed all 1,023 entries in `source-evidence-manifest.json`, matched each path to the pinned Git-tree blob and current worktree bytes, and confirmed the total is 107,123,938 bytes. This was cross-checked against (not merely copied from) the committed-blob verification record.
- The original premodel freezes are timestamped 2026-10-20 15:55:52 UTC. Each freeze’s original brief, references, build config, concept, prompt, and generation receipt hashes match. Candidate delivery briefs preserve original required criteria and claim scopes; final render manifests and all eight frame hashes bind to the exact final GLB, delivery brief, references, and revision.
- Fresh independent Khronos validation (`gltf-validator` 2.0.0-dev.3.10): all four exact GLBs have 0 errors and 0 warnings. Fresh Three.js 0.180.0 Node parses succeed; counts are 5,040 / 3,148 / 4,938 / 7,340 triangles for Ernietta / Loess / Rock / Slump.
- I reopened each saved `.blend` with Blender 4.3.2 in read-only mode, checked source/export counts and axis-converted bounds, then independently re-exported under the frozen metadata options. Each re-export is byte-identical to the delivered GLB; source and original GLB hashes were unchanged before/after. Source/export triangle counts match and maximum bound errors are below 0.000001 m for all four.
- Independently rechecked two separate semantic queue jobs per asset: distinct PIDs, job IDs, times, request/result hashes and fingerprints; successful result records; declared generator/config hashes; matching stdout build lines; and output model hashes matching the final candidate. All eight job outputs are separately present. This corroborates real distinct execution but is still evidence-based provenance, not cryptographic proof of the original processes.
- Frozen budgets pass for all four: under 14,000 triangles, 6 materials, 30 primitives, and 1 MB; no textures are shipped. Existing source/BVH surface checks pass, with no visible defects in the reviewed frames.
- Referenced third-party materials are recorded as consulted-only, with no source pixels, mesh, or texture incorporated. Candidate assets are recorded CC-BY-4.0 and generator code MIT. Concept invocation/result times are recorded, but provider-generated times and internal durations are unknown; I leave those unknown and do not treat them as a static rejection gate.

## Evidence and limitations

Own QA outputs are under `/workspace/shared/lowpoly-round31-qa77/batch77-20261020/`. `integrity-check.json` records the independent 1,023-file manifest, candidate bindings, 32 frame checks, eight rebuild-job checks, and fresh validator results. `khronos-fresh.jsonl`, `three-fresh.jsonl`, per-candidate `source-export.report.json`, and per-candidate `reexport.report.json` contain the check outputs. Per-candidate `reexport.glb` files are QA-generated, byte-identical copies from read-only source re-exports, not producer artifacts. `input-sha256-before.txt` and `input-sha256-after.txt` show the pinned handoff/brief/freeze/config/generator/source/GLB/sheet hashes remained unchanged.

No GPU device, browser renderer, populated target scene, website display, formal review, user approval, or publication was run or inferred from CPU stills or Node parsing. Ernietta’s required seam should be addressed as a new candidate revision without changing its original fossil scope or rewriting failed attempts.
