# Non-biota natural-appearance review

Review date: 2026-10-19  
Frozen published baseline: `de413ef720463a2999516faf92c606bcdf9ab1b7` (175 assets).  
Scope: geology, terrain and trace assets; animal, plant, fungi and wood categories excluded.

## Coverage

The inventory is keyed by exact `asset_id` so the same asset is never counted twice as a separate model just because a revision exists. It covers the 175-asset frozen baseline and the latest available handoffs for batches 40–50. The batch-44 source is the requested handoff commit `49b1d6cddd807c89884935974ee2de1bc27bd0fb`.

- Total discovered across baseline and handoffs: **219** asset records.
- In-scope asset IDs: **76** = **51** frozen-baseline assets + **23** available candidate models + **2** in-scope models not generated in batch 50.
- Available in-scope models visually inspected: **74**; all have a six-angle contact sheet tied to source GLB SHA-256 in `evidence/visual-manifest.json`.
- Per-asset results: **58 usable**, **16 needs change**, **2 unavailable**.
- Two batch-50 in-scope IDs (`karst-sinkhole`, `fault-scarp`) were prepared but not built; they are uninspected, not visual passes.
- Batches 49 and 50 remain paused/incomplete per their handoffs. Visual inspection of available candidate GLBs here does not assert independent QA or batch completion.
- The baseline `dinosaur-nest` and `three-toed-track` are included because the frozen manifest categorizes them as traces; this review covers those exact IDs as traces.

The complete source paths, revision/attempt labels, source commits, hashes, scope relation, verdict, and image paths are in `review.csv` and `review.json`. `coverage.csv` and `coverage.json` retain all 219 discovered baseline/candidate records, including excluded categories and source handoff status.

## How the pixels were reviewed

Each available source GLB was hash-checked against the pinned inventory, imported into a controlled orthographic studio setup, rendered as six 512×512 angles (hero, reverse hero, front, side, rear, top), and assembled as a 1600×1182 contact sheet. I directly inspected all 74 contact sheets. The standardized light and background make silhouettes, proportions, relief, layering, repetition and broad material/color cues comparable; this is an asset-level visual review, not a product-scene or lighting integration check. No visual pass is inferred from QA JSON alone.

Verdicts describe whether the model reads naturally enough for a stylized child-friendly 3D world. They are not claims of strict scientific reconstruction. Purposeful sections, cast surfaces, and trace slabs remain labeled as such; their flat display face is not by itself treated as a defect. Recommendations are deliberately bounded to small visible edits, not micro-detail work.

## Main visual findings

| Asset | Exact version | Priority | What reads unnaturally | Smallest improvement | Evidence |
|---|---|---:|---|---|---|
| `cave-boxwork` | r001 | P2 | The raised walls make a regular maze with many similarly sized polygon cells and near-uniform wall heights; the result reads like a manufactured maze on a flat plinth. | Keep the connected boxwork network, but vary cell size and wall height and interrupt a few wall runs; the flat display base can stay. | [six views](evidence/multiview/cave-boxwork.jpg) |
| `boudinaged-rock-layer` | r001 / attempt-02 | P2 | The layer break is legible in section, but four nearly matching sausage-shaped segments sit at regular intervals in a rectangular matrix. Their repeated size and rhythm feel assembled. | Preserve the exposed section and continuous matrix; change only one or two segment lengths or neck widths and make their spacing slightly less even. | [six views](evidence/multiview/boudinaged-rock-layer.jpg) |
| `ophiomorpha-pellet-lined-burrow` | r001 / attempt-02 | P2 | The burrow tube is a very even curved pipe, and small pellets repeat at nearly equal spacing in orderly rows along it. This reads like a manufactured hose with studs. | Keep the open burrow form and pellet lining, but vary tube curvature slightly and make pellet sizes and spacing less uniform. | [six views](evidence/multiview/ophiomorpha-pellet-lined-burrow.jpg) |
| `shale-scree` | r001 / attempt-02 | P2 | The cliff face is a stack of thin, nearly equal, parallel plates; the talus is a very regular apron of similar flakes on a clean wedge base. Together they read as a staircase display rather than broken shale on a slope. | Keep the layered face and downslope debris, but vary slab thickness and tilt, break the stack edge in a few places, and mix a few larger and smaller scree flakes. | [six views](evidence/multiview/shale-scree.jpg) |
| `columnar-jointed-outcrop` | r001 (frozen published baseline) | P2 | The top view shows a clear polygonal joint pattern, but the exposed columns are short, broad, and packed like paving blocks. Their nearly level tops and similar heights weaken the vertical column impression. | Preserve the polygonal end pattern, while exposing a few taller, unequal column segments and varying some column widths or top heights. | [six views](evidence/multiview/columnar-jointed-outcrop.jpg) |
| `conglomerate-outcrop` | r001 (frozen published baseline) | P2 | The clasts repeat as similarly sized rounded bumps that sit proud of the matrix like studs across an oblong block. The even exposure and smooth oval host mass make it look decorated rather than cemented gravel. | Sink most clasts further into the matrix, vary their scale and angularity more, and leave a few partly hidden; keep the playful multicolor range. | [six views](evidence/multiview/conglomerate-outcrop.jpg) |
| `cross-bedded-sandstone` | r001 (frozen published baseline) | P1 | The inclined laminae and set-boundary truncations read clearly, as the brief intends. The full object still reads like a rigid rectangular brick: broad unbroken top plane, straight outer edges, and a very regular rhythm of parallel bands on the sides. | Keep the three physically truncated sets and flat teaching face. Soften or vary only a few outer edge runs and vary spacing or thickness of a small number of laminae; do not rebuild the cutaway or add microtexture. | [six views](evidence/multiview/cross-bedded-sandstone.jpg) |
| `desiccation-crack-surface` | r001 (frozen published baseline) | P2 | The flat teaching tile is appropriate, but its crack network is a neat tessellation of similar polygons with consistently thin, dark seams and straight tile edges. | Keep the tile, but vary polygon size and crack width, add one less regular junction, and give the exposed perimeter a small amount of edge variation. | [six views](evidence/multiview/desiccation-crack-surface.jpg) |
| `entobia-sponge-boring-network` | r001 (frozen published baseline) | P2 | On the block top, round chambers joined by narrow cylinders read as a molecular model sitting above the rock surface rather than a boring network within the rock. | Keep the connected chamber plan, but recess more of it into the top face and vary chamber size and connector width so the rock remains the host. | [six views](evidence/multiview/entobia-sponge-boring-network.jpg) |
| `hydrothermal-chimney` | r001 (frozen published baseline) | P1 | Repeated horizontal color bands form square, stair-stepped rings of almost equal thickness. From the front and top this looks voxel-built or mechanically stacked instead of a mineral chimney with uneven accretion. | Keep the hollow chimney and broad banded color cue, but vary ring width and height and let a few band edges drift or break across the faceted body. | [six views](evidence/multiview/hydrothermal-chimney.jpg) |
| `pahoehoe-lava-surface` | r001 (frozen published baseline) | P2 | The entire slab is covered by smooth, parallel, similarly spaced rope-like ridges. The repeated rhythm reads as corrugation rather than overlapping ropy lava lobes. | Retain the rope-like relief, but interrupt or merge a few ridges and vary their spacing, direction, and amplitude. | [six views](evidence/multiview/pahoehoe-lava-surface.jpg) |
| `paleodictyon-mesh-trace` | r001 (frozen published baseline) | P2 | The diagnostic net is clear, but its near-perfect hexagonal cells are arranged in a regular honeycomb patch, which looks CAD-generated. | Keep a readable connected mesh, but vary cell size and angles modestly and let the mesh terminate less symmetrically at the edges. | [six views](evidence/multiview/paleodictyon-mesh-trace.jpg) |
| `reticulite-clast` | r001 (frozen published baseline) | P1 | The form reads as a thin wire cage made from straight rods, with open gaps across most of its volume. Reticulite should read as a very porous foamy glass clast rather than a constructed frame. | Keep the open porosity, but replace several long rod spans with a few thin, irregular connecting walls or membranes and vary strut thickness. No need to fill the pores or add fine microtexture. | [six views](evidence/multiview/reticulite-clast.jpg) |
| `sea-stack` | r001 (frozen published baseline) | P2 | The stack is a tall, almost uniform-sided round-cornered pillar with a flat polygonal top and broad level color bands. It reads as a cut post more than an isolated eroded sea stack. | Keep its upright silhouette and stratification, but taper or notch one side, roughen the top outline, and vary a few band edges. | [six views](evidence/multiview/sea-stack.jpg) |
| `tafoni-outcrop` | r001 (frozen published baseline) | P2 | The cavities are similar dark ovals placed in tidy rows across an otherwise simple block. The regular spacing and repeated opening shape make the honeycomb erosion look drilled. | Keep multiple cavities, but vary their size and orientation, merge one or two neighboring hollows, and break up the tidy rows. | [six views](evidence/multiview/tafoni-outcrop.jpg) |
| `wave-ripple-surface` | r001 (frozen published baseline) | P2 | The parallel wave ripples have nearly identical wavelength and amplitude across the whole rectangular slab, creating a regular corrugated sheet. | Keep the broad parallel ripple direction, but vary wavelength and height gently and allow a few ridges to fade or drift near the perimeter. | [six views](evidence/multiview/wave-ripple-surface.jpg) |

The cross-bedded sandstone is a special case. Its brief describes a child-friendly teaching exposure with three cross-bed sets and physical lamina truncations; the flat teaching face and cutaway are intentional. The fresh views show those wedges reading clearly. The finding is limited to the uniform brick-like exterior and repetitive side rhythm, and the recommended tweak leaves the teaching geometry intact. The brief’s reference record says source image pixels were not viewed, so this is not a comparison against a specimen photograph.

## Items visually usable as delivered

The remaining **58** available IDs are marked usable for this bounded natural-appearance check. Their specific identity, exact version, source hash and inspected contact sheet are listed in `review.csv` / `review.json`; no required natural-appearance edit was apparent at the six reviewed angles. This includes intentional teaching sections whose flat display planes support the stated use.

## Not available to inspect

| Asset | Handoff | State | Visual result |
|---|---|---|---|
| `fault-scarp` | `396d9d1fa72fb3b9d1dfb564cec8d760d5401b38` | not generated | no pixels available; not inspected |
| `karst-sinkhole` | `396d9d1fa72fb3b9d1dfb564cec8d760d5401b38` | not generated | no pixels available; not inspected |

## Limits and disposition

This is a read-only visual review. No model, gate, website, CI, or release file was changed. It does not change candidate QA state or release authority. The high-priority shape and repetition findings are suitable for the baseline-correction discussion before another publish batch; no merge or deployment was performed.

## Evidence and machine-readable deliverables

- `review.csv` — one row per in-scope asset ID with verdict, version, source hash and contact-sheet link.
- `review.json` — same per-asset results plus aggregate counts.
- `coverage.csv` / `coverage.json` — source/handoff coverage for all discovered records, with hash pins and incomplete handoff states.
- `evidence/multiview/` — full 6-angle pixel evidence for all 74 available models.
- `evidence/visual-manifest.json` — render settings, source hash, contact-sheet hash and dimensions.
- `review_decisions.json` — authored concise dispositions and minimum suggested improvements.
