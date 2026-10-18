# Batch 03 independent review

**Reviewed candidate:** `candidate/small-life-batch-03-20261018` at `da240359dabe69c775c9d251d6530cf30db25dad`

**Maker:** Leon Made This `<8357465+s010s@users.noreply.github.com>`

**Review scope:** Independently assess the frozen exact GLBs against the batch brief and accepted trio-v002 natural refined low-poly direction. These are static stylized-inspired teaching props, not strict scientific reconstructions.

## Verdicts

| Asset / revision | Verdict | Frozen GLB SHA-256 | Source `.blend` SHA-256 | Visible basic-form result |
|---|---|---|---|---|
| `cephalaspis` r001 | **PASS** | `f316d7a8b4315ab65d9aa790dd16dda8637fd0fa7e1357e433aee0ed71125b70` | `ccb304d7b875cff4df04d47a371831f8edec96fe181803fcf09cc36fa50554f3` | Broad swept shield, high-set eyes, clear taper into a long body and restrained fins/tail. |
| `saccocoma` r001 | **PASS** | `32f722fff198376ff46d635f31393bcf0dc3ba8b1828b9390d789b68b0b2afea` | `453e5b5404b175d40e45db377379fea623ddfdb61ecb82b58d072aff8dcd8069` | Small stemless central cup with open, branching featherlike arms. |
| `archaeocidaris` r001 | **PASS** | `a8fc01de01aaa8665c23015d64dc537835dcafd738da2c7680107df1fc61526a` | `6daa4dac12cb1aeb5a5bea7c770e3643e5f9d418808287de0804d07003805b93` | Rounded plated test remains readable among orderly tapered primary spines. |
| `onoclea` r002 | **PASS** | `a6cfc0c662603b3fe19fe11d11fa9426195e42e9611e43ce064edbbadb038a84` | `383040388e697fb8642984d534c4f0c7154b31ad2a3d191563ce32151ed2393a` | Broad lobed sterile fronds and narrow beaded fertile fronds read as one plant network on a creeping rhizome. |

**Required repairs: none.** All four pass the required technical-integrity, normal-view-recognition, basic-form, delivery/label, target-loader, functional-render, and representative-scene gates within the brief's stated claim scope. No obvious missing faces, detached major parts, accidental intersections, collapsed forms, or broken shading stood out in the reviewed views.

## Evidence checked

- Opened and inspected all eight exact-GLB images per item (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`), plus the individual browser runtime angle, size-envelope and nine-copy scene images. The exact render manifests and runtime JSON bind the views to the GLB hashes above.
- Independently replayed the pinned Three.js 0.180 browser QA in an isolated copy of the reviewed commit. All four single models and all four nine-copy scenes loaded with zero console errors and zero failed requests in SwiftShader WebGL2. The 48 regenerated browser PNGs were byte-identical to the frozen screenshots. This is functional software-render evidence, not physical GPU performance.
- Independently reopened each frozen `.blend` with Blender 4.3.2 and compared its evaluated source geometry to the exact GLB. Triangle counts and axis-converted bounds matched; the maximum bound delta by item was 3.73e-9 m, 4.66e-10 m, 9.32e-10 m, and 1.17e-8 m respectively. The source/export checker reports `pass_with_warnings` only for intentional smooth faces; the inspected clay and alternate views show these transitions are deliberate.
- Independently ran the Khronos validator on temporary copies of the four frozen GLBs: **0 errors, 0 warnings each**. Verified all **259** entries in the submitted `checksums.sha256`. The submitted reproducibility records also bind two deterministic rebuilds per asset to the same GLB bytes; I checked their frozen hashes but did not rerun those rebuilds.
- Inspected `qa/continuous-small-life-20261018/batch-03/independent-review/true-relative-scale.png`, rendered by reimporting these exact GLBs together in Blender at authored meter scale. Only layout translation was applied (and a 90° Z rotation to Cephalaspis to align its length for comparison); no asset was scaled. The art-direction sizes line up: Cephalaspis body length 0.22 m, Saccocoma span 0.05 m, Archaeocidaris total span 0.10 m, and Onoclea patch height 0.45 m (0.541 m maximum width). The candidate's per-item nine-copy scenes remain isolated benchmarks; this brief does not require museum integration or a mixed-habitat performance test.

| Asset | GLB dimensions `[X,Y,Z]` (m) | Triangles | GLB bytes | Runtime single → nine-copy work |
|---|---:|---:|---:|---|
| `cephalaspis` | `[0.098, 0.038, 0.220]` | 2,998 | 67,700 | 11 calls / 2,998 → 100 calls / 26,984 triangles |
| `saccocoma` | `[0.050, 0.013, 0.050]` | 9,436 | 219,228 | 6 calls / 9,436 → 55 calls / 84,926 triangles |
| `archaeocidaris` | `[0.093, 0.048, 0.100]` | 10,680 | 209,288 | 7 calls / 10,680 → 64 calls / 96,122 triangles |
| `onoclea` | `[0.541, 0.450, 0.361]` | 12,776 | 260,148 | 8 calls / 12,776 → 73 calls / 114,986 triangles |

The displayed dimensions are the frozen GLB bounds. Counts and sizes are within this batch's recorded limits. There are no textures. The plate, spine, shield, cup and plant structures meet the basic stylized-inspired obligations; this review does not assert exact anatomy, species-level diagnostic certainty, fossil measurements, or a particular habitat coexistence.

## Non-blocking notes

- `saccocoma` is correctly small beside the other props at true scale; in a future mixed-size habitat it will need close placement or a deliberate display-scale decision for the intended 80–240 px viewing envelope.
- In `onoclea`'s top view, fertile and sterile fronds overlap near the center. Both architectures and their shared plant network remain legible; slightly staggering them could improve separation if this prop is later revised for a larger gallery view.
- The independent relative-scale sheet is a review-only comparison, not a mixed-scene integration or performance claim. No cross-asset adjustment is needed for this candidate batch.

**Disposition:** PASS all four frozen revisions; no model, threshold, CI, release, or queue-state changes made as part of this review.
