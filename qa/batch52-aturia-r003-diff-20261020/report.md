# Batch 52 Aturia r003 targeted difference QA

**Decision:** Close the original Aturia r002 visual blocker for this targeted retest. The r003 repair removes the reported hard-edged radial sector, and I found no new must-fix issue in the eight reviewed views. This is a differential visual/technical review, not formal candidate approval.

## Scope and pins

- Original independent QA: [`qa/batch52-independent-20261020/report.md`](../batch52-independent-20261020/report.md), commit `f3f793f6f9024d43453dbd302623c98eb34af5e7`.
- Baseline candidate: commit `352d81995b33fc1e7a95980184ab6641dd5738a5`; Aturia r002 GLB SHA-256 `65f2c625334872f5e849d3bee11ff6085cc3245c93cb2cd86ba4baf13a74287b`.
- Repair candidate: `candidate/small-life-batch52-concept-20261020` at commit `110ec9772e1854ab9c4ccfa23848541b8e3aa1d7`.
- Reviewed target: [Aturia r003 GLB](../../assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/aturia.glb), SHA-256 `74b4e090382777b9d8b358dd1dad2df57f9751d8266437e95d9d144448cf31d1` (662,872 bytes). Source `.blend` SHA-256: `f2e7b514dc4adfcb9acfc268335a372d99714f2a81f4011f2b2cef2991f5f675`.
- Original concept pixels checked: `concept-original.png`, SHA-256 `55722e90c04098cdc12a4d5f8df5edaefb06ab70c946bfa0e153eeae2978dce6`.

## Retest of the original finding

The original report's exact finding was: “A prominent hard-edged angular radial/annular patch reads as a cutaway or segmentation and conflicts with the smooth-shell brief; it is absent from the concept. Remove that sector or make the fossil variation much subtler and irregular, then rerender the same eight views. The shell profile itself is recognizable.”

I opened and compared the baseline and r003 exact-GLB renders for `hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, and `silhouette`. The baseline patch is plainly visible in several color views. In r003, the sharp brown sector is gone in every view; the former sector shares the shell's base color. The shell outline, involute seam, rounded rim, and silhouette are retained. Clay and silhouette decoded pixels are identical between revisions. The original concept shows the same quiet beige shell and pale rounded rim, without a cutaway. No new must-fix regression was apparent in the reviewed views.

The eight new images are bound by [the r003 render manifest](../../assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r003/proof-final/render-manifest.json), SHA-256 `7021ec700b139fe314e169665036a3e89877261093eebabd25a7d9024aa82cd3`. All eight frame hashes and the manifest's source GLB hash were checked. The old and new renders use the same render configuration SHA-256 `222ddc37e787008a5683088c341d460bb7b7d86264cd84067ad9a328a54a7e74`.

## Targeted technical verification

- Re-ran the r002-to-r003 color-only comparison: pass. The GLB binary chunk is identical; only the pale fossil-patch material's base color changed (`#C2A77A` to `#D8C7A2`). Geometry, normals, scene graph, accessors, buffer indices, transforms, roughness, metallic, alpha, and sidedness remain identical. The former sector and shell base colors now match.
- Reopened the r002 and r003 Blender sources with Blender 4.3.2 and compared source measurements: both have 6,082 vertices, 6,144 polygons, the same shell bounds and volume, no non-finite vertex normals, and no non-positive face areas. The source geometry identity report also binds the same topology/normals digest, `cb374075792afd7e56a21ba98685422131a49a5a35b409c06bd0ce43ede2d934`.
- Re-ran source/export verification on r003: pass. Blender reopened the source and imported the exact GLB; 12,160 source/export triangles matched, bounds matched within `5.65e-9 m`, and there were no errors or warnings.
- Rechecked both recorded semantic rebuild outputs: each is byte-identical to the r003 GLB and has semantic SHA-256 `2235055d94ccf19cccee5ddc2dddc7b5fd3165d52106d7baeedf295cb9486102`. The reproducibility checker compares the bound rebuild outputs; it does not execute the generator during this verification.
- Re-ran the Khronos glTF Validator 2.0.0-dev.3.10 against the exact r003 GLB: 0 errors, 0 warnings, 0 infos, and 0 hints. The independent static GLB audit also passed: 12,160 triangles, 3 materials, 3 primitives, no extensions, and no textures.
- Verified [the protected-files proof](../../production/continuous-small-life-round18-20261020/work/batch-52/aturia-r003-protected-files.json) against both the pinned baseline and current candidate tree: all 560 listed files match byte-for-byte. Aturia r001/r002 and all retained files for the other three items are unchanged. Their three handoff item values also match the baseline exactly.

## Preserved original batch findings

The other three assets are carried forward from the original independent report without re-review: Phoenicopsis r001 passed in the reviewed scope; Cave popcorn r003 passed; Curvolithus trilobed trail r001 passed with the original intentional smooth-face style warning accepted. This task does not extend those scopes or claim a new review of those assets.

The factual scope remains “Aturia-inspired fossil shell prop,” with no exact specimen anatomy, color, size, age, or locality claim. As recorded in the original QA, the linked official specimen-photo request returned HTTP 403 through the proxy; no official photo pixels were inspected.

## Unknowns and approval boundary

- The exact ImageGen provider generation timestamp remains unknown; no time was inferred from file dates.
- r003 target-browser parsing, physical GPU/hardware, and target-device behavior remain untested. Earlier r002 SwiftShader evidence is not promoted to r003.
- No populated parent-scene or scene-performance pass is asserted.
- Formal candidate approval remains pending, and this QA does not modify approval records, production catalogs, `main`, site, or release state.

The new review evidence is in [`review-evidence.json`](review-evidence.json). This report is committed on `qa/batch52-aturia-r003-diff-20261020`; it is an ordinary branch update, with no force push or merge.
