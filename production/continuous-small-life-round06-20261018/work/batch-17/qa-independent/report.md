# Batch 17 independent QA

**Decision: PASS for all four frozen candidate artifacts.** This is an independent review of the exact source commit and hashes below. It is not a publication approval.

## Scope and evidence lock

- Candidate branch: `candidate/small-life-batch17-20261018`
- Exact candidate source commit: `fa28e9b9743702e64170f646884a035e44c9ff88`
- Current-main QA rules baseline: `ccf48bb446dd4d0a710ab14dfc05d6fbf7064cdb`
- Applied the existing `static-stylized-v1`, rule version `2026-10-18.1`, and each item's frozen limits without changes.
- All four recorded checkpoint commits are ancestors of the candidate source commit. The handoff-pinned files and rendered frames/sheets were independently rehashed; there were no mismatches. See [`hash-audit.json`](../hash-audit.json) and [`evidence/manifest-runtime-audit.json`](evidence/manifest-runtime-audit.json).

| Asset | Checkpoint | Blender source SHA-256 | GLB SHA-256 | GLB bytes | Triangles / materials / primitives |
|---|---|---|---|---:|---:|
| `isastraea` | `a05292a7b52654271597927f3428a21b0348bdd6` | `952aae3d8fd74e3f44a07bd09e28579477b4cbf8a12ef592d19ab8adf256a822` | `6380b1770d80a0f6e9521fb69189cce836f2b42be07e4b0aa238adc1cfb0ece9` | 184,356 | 8,528 / 3 / 3 |
| `araucaria-mirabilis` | `63ad3910a885e95130e0ce0dd1de159a534050ee` | `82779a3f0d209738f686a486907ae0172dcaf1e655b42575e7b1cddf25661605` | `40ec7b84c24c7406631c46252811efca43c6e9a2c361794cca38012d279d1614` | 136,564 | 6,914 / 4 / 5 |
| `onychonycteris` | `5435f99203d681a8b96f32f608499745f876c4e5` | `b284ce6db4235bec8cd1c44494bcfdbcfc28af5b8f0f7460bc982140a6c1a02f` | `762fa3aabcaa37cae5f374e9d3fa22beb9f227ed86195919f8bdc02c1c1bf02f` | 231,000 | 12,292 / 5 / 8 |
| `pillow-lava-outcrop` | `aa6f970efd6aed2d93c706561cb4ff86e3b3deb2` | `2471cdc816ed976c54158357684c696ee7a0a5a9d36bdba5ecd9f4714f0d7f51` | `ae72e9c5f1e4971ce5b7fb60828be0119c4a9c27f64c45a8256a3e303617f437` | 141,820 | 7,636 / 2 / 2 |

## Independent results

Each item passed the repository GLB audit with no errors or warnings; the Khronos glTF validator reported zero errors and warnings; and the frozen production profile contract validated. All files are below the frozen 14,000-triangle, 6-material, 30-primitive, and 1,000,000-byte limits. Exact command lines and raw outputs are in [`evidence/command-results.json`](evidence/command-results.json) and `evidence/checks/<asset>/`.

Blender 4.3.2 reopened the exact `.blend` files with factory startup and auto-execution disabled. For each asset, source and GLB triangle counts agree; axis-converted bounds agree within `0.0001 m` (observed maximum per asset: 0 to `3.73e-9 m`). Every exported source mesh reports zero boundary and zero nonmanifold edges. The checker emitted only its standard smooth-face style-review warning; I reviewed those faces in the actual multi-angle source and runtime views and found the smoothing intentional for this low-poly direction. The exact runtime JSON binds to each listed GLB SHA and reports no load errors; the single-asset and six-instance scenes both render.

The handoff's 8 source views and 12 runtime views per asset were checked against their pinned manifests. The runtime viewer is Three.js 0.180.0 with Chromium ANGLE SwiftShader; the view manifest records 80, 160, 240, and 480 pixel render extents. I inspected the multi-angle source and exact-GLB runtime sheets, including front/side/rear/top/bottom, and the 80/160/240 views. Runtime PNG captures are 640×640 evidence canvases; their recorded viewer extents are separate from that capture canvas size. No obvious missing faces, malformed seams, detached joins, intersections, or pose/proportion faults appear at normal views or moderate close view. The six-copy scene has clear separation.

### Per-item visual and form decision

- **`isastraea` — PASS.** The low, continuous colony plate has adjoining polygonal cups and a distinct, legible calyx-like radial pattern. Its thin profile holds in side/rear views, and no gaps or breaks appear between cups. The author-uploaded caption describes polygonal calices for *Isastrea*; the mesh is an appropriately simplified, stylized colony and does not claim exact species or microscopic septal counts ([source caption](https://www.researchgate.net/figure/A-Isastrea-whitneyi-Wells-1932-MCCC2-025-upper-surface-view-of-prismatic_fig2_320306296)).
- **`araucaria-mirabilis` — PASS.** The deliverable is one short twig with one attached, rounded, overlapping-scale cone. Its attachment is clear and continuous in front, side, reverse, and top views; the cone remains readable at 160/240 pixel views. This matches the frozen organ-only scope and the museum entry's note that a cone is preserved attached to a branch ([Fukui Prefectural Dinosaur Museum](https://www.dinosaur.pref.fukui.jp/guide/education/photo/F0007.html)). No whole tree or canopy is required.
- **`onychonycteris` — PASS.** A compact mammal body, broad membranous wings, long supporting digits, tail web, and feet/claws read as a bat in both front and top silhouettes. Wing membranes meet their supporting digits without apparent holes or detached joins. Its friendly eyes and rounded face are evident stylistic choices in the frozen child-friendly brief. The restrained fossil-informed features align with the AMNH summary of short broad wings, claws on all five fingers, and relatively long hind legs/shorter forearms ([AMNH](https://www.amnh.org/explore/news-blogs/bats-flight-echolocation)); this is a teaching prop, not a strict reconstruction.
- **`pillow-lava-outcrop` — PASS.** The low outcrop reads as connected, uneven bulbous lobes with constricted necks from front, side, rear, top, and underside. The lobes remain connected in silhouette without visible clipping or holes. This fits the broad teaching form of interconnected pillow-like lobes described by Oregon State's Volcano World ([OSU Volcano World](https://volcano.oregonstate.edu/faq/what-are-different-types-basaltic-lava-flows-and-how-do-they-form)). No exact locality or diagnostic geological claim is made.

## Nonblocking notes

- The frozen inventory identifier `isastraea` is retained, while the consulted author caption spells the genus *Isastrea*. Keep the inventory key stable; if the display name is later made taxonomically strict, reconcile that label separately. This does not block this stylized, genus-inspired artifact.
- At 80 pixel extent, fine texture and small facial/claw features naturally recede; the 160/240 views show them adequately. No additional detail pass is warranted for this brief.
- Smooth shading appears on the organic surfaces. It was inspected in context and is intentional; no corrective action is requested.

## Frozen candidate/profile status

The current-main validator reports profile-contract `pass` and `approved_for_brief: false` while the independent acceptance stages remain pending. That status is expected before recording review in the parent task; it is not a model-quality failure and was not changed by this review. This QA branch contains only the report and copied/derived audit evidence; it does not modify candidate models, candidate metadata, CI, permissions, or publication state.

