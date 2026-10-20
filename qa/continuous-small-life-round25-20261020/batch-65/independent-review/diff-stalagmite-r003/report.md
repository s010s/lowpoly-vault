# Independent differential QA: stalagmite-group r003

Date: 2026-10-20 UTC  
Scope: targeted, read-only review of the repaired stalagmite-group r003 only. The three previously accepted candidates were neither rebuilt nor rerendered. Producer checkout: `/workspace/shared/lowpoly-batch65-20261020`, branch `candidate/small-life-batch65-concept-20261020`, clean at `cdf3fcfdd59413ca882d0a1e6cefe4aeadb9164f` before and after. This is a static candidate recommendation, not formal/user approval or authority to publish.

## Result

**stalagmite-group r003: ACCEPT BOUNDED as a static candidate recommendation.** The original r001 visual defect is sufficiently corrected in the actual r003 pixels: the many thick, regular, stacked-looking horizontal rings no longer dominate; the remaining growth terraces are fewer, weaker and uneven. Longitudinal raised ribs/grooves read clearly from side and rear views and remain visible in the untextured clay image, so the relief is geometric rather than a color-strip substitute. The five unequal, rounded, solid floor-rooted columns remain clear; the top view shows convex caps without central holes.

This is a bounded visual pass, not a claim of photographic cave realism. Residual short ledges/bands remain visible, particularly on the shorter front columns in front/hero views. They read as subordinate irregular terraces rather than the defining repeated ring stack seen in r001. The comparison is supported by fresh full-resolution r003 inspection of all eight final views and a targeted check of the retained r001 hero and clay views.

## Differential against the original failure

The original brief is byte-identical between r001 and r003 (`fbcc33563b0b3adb9cb8bee2c12bae5f3f3b26212f20f271c96b73898f1cebd8`). The retained r001 GLB remains `3b5e8892435c365a612965648f7f1150fad34899b76dfc84edc99d99e34a8668`; the original independent report still has SHA-256 `f6866f3c37b3fdf8cd0024c72756c4508fce1cdc4ef6879f1b71eb51a4da447a`. The retained r002 model and maker rejection also remain in place. No target-scope relaxation or overwrite was found.

In r001 hero/clay, roughly repeated, thick horizontal stair rings wrap every column and obscure any vertical drip pattern. In r003, the hero/reversehero, front, side and rear views show weakened, uneven terrace steps; the side and rear most clearly expose longitudinal grooves/ribs. The clay view confirms that the vertical relief persists without material color variation. Short foreground columns retain some local horizontal ledges, the residual reason for keeping the recommendation bounded.

## Seven-stage review (this reviewer’s findings only)

| Stage | Result | Basis / limit |
|---|---|---|
| Technical | PASS | Project static GLB audit; independent Khronos validation; independent read-only Blender source reopen; closed-solid topology/volume. |
| Visual | PASS, bounded | Original r001 ring-dominance concern is resolved in all eight inspected r003 views; residual ledges on shorter columns noted. |
| Factual | PASS, bounded | Matches the frozen generic stalagmite obligation: rounded, solid, floor-grown columns. No site-specific, measured cave or scientific reconstruction claim. |
| Specification | PASS | Five unequal rounded columns and low crust retained; final geometry includes irregular longitudinal relief; within numeric budget. |
| Runtime parse | PASS | Fresh Three.js 0.180.0 `GLTFLoader.parseAsync` on the exact final GLB. This is a parser check, not a browser/GPU render. |
| GPU | NOT RUN | No target GPU/device claim. |
| Scene | NOT RUN | No populated-scene integration or performance claim. |

## Exact final artifact and technical checks

Final GLB SHA-256: `3e696fcb6e2b2ffb21e7ea850522c5f2f6498a11e13bb7ce429f6376df3de5e0` (629,868 bytes). Saved Blender source SHA-256: `b4288340b0288bb017de713f6a2094bc0a6b92779ecd0d4e8e3e699cbe3f0ac3` (943,072 bytes).

- Project static audit: PASS, 11,640 triangles, 11 primitives, 3 exported materials, 22,960 POSITION entries; no errors or warnings. Limits checked: 14,000 triangles, 1,000,000 bytes, 6 materials, 30 primitives. Actual: 11,640 / 629,868 / 3 / 11.
- Khronos glTF Validator: PASS, 0 errors and 0 warnings.
- Fresh Three.js 0.180.0 parse: PASS, 11 meshes/primitives and 11,640 triangles. Exported material names are `floor`, `mineral`, `light`; the source palette also has an unused `ochre` entry that is omitted from exported GLB materials.
- Independently reopened `source.blend` read-only with Blender 4.3.2 under the blocking production lock and two threads. Six mesh parts / 11,640 triangles; all six have zero boundary and non-manifold edges and positive enclosed volume. Measured Blender bounds are 2.353597 × 1.745315 × 2.199790 m. Exported Y-up GLB bounds are 2.353597 × 2.199790 × 1.745315 m; bounds and triangles match the saved source/export audit.

## Final render binding and actual views

The final render manifest SHA-256 is `14b269b86a3564e1ac8f2c4be0720e44fa49e79dcccfc2b279a09c0595bf8004`, with manifest time `2026-10-20T14:24:43.425060+00:00`. Both `source_glb_sha256` and `subject.glb_sha256` bind to the exact final GLB above, at revision r003. Each of the eight exact delivery PNGs was independently checked for manifest SHA-256, byte length and 512×512 dimensions, and decoded RGBA pixels were hashed. All eight files match their manifest; images were individually inspected at full resolution: hero, reversehero, front, side, rear, top, clay and silhouette. No old pixels were relabeled as r003.

## Rebuild provenance

Two actual successful Blender generator jobs are preserved as distinct queued jobs under the same sequential queue invocation. They have different job IDs, request fingerprints, attempt directories, PIDs, start/end times and source.blend output hashes; both stdout logs contain the successful `BUILT` line, all declared outputs match their result records, both model outputs equal the final pinned GLB, and both semantic comparisons are byte-identical and semantically equal (digest `5db49ed621bd6886ca30fdc1a477c97c98c5067d2ae5dc58e512ac5853c6a77d`).

| Job | PID | Start → finish (UTC) | Request fingerprint | Request SHA-256 | Result SHA-256 | Built GLB SHA-256 | Built source.blend SHA-256 |
|---|---:|---|---|---|---|---|---|
| semantic-rebuild-1 | 123 | 14:24:43.827605 → 14:24:51.002625 | `a42c59d7c6f6e5d7cdacb9379236af0f357c480de5d28dc2f6d13c239b28a064` | `33c62aa722e167b4dbd474bc42790ef0a1213729fdf08724203bc90e1b616287` | `22e56185cfaf86036f97ff5f272ca3535dbd2b9a23789d019e6085bcfa9df6b6` | `3e696fcb6e2b2ffb21e7ea850522c5f2f6498a11e13bb7ce429f6376df3de5e0` | `26e45b24771d84192281a765296c063d05f79cde0808b710de2f4e08c8de2668` |
| semantic-rebuild-2 | 146 | 14:24:51.013682 → 14:25:21.433469 | `fb7959684eacccc3356ac6fe51f744dc99658f8aa5fc78d4cc2e79e04a4db088` | `0e115f06f21da9d39578265c5cb3e67d682c74f2dab712209336004ade11138a` | `766604737507d12911650c7427c08617f7a7fb157ad84098fea65726b318f385` | `3e696fcb6e2b2ffb21e7ea850522c5f2f6498a11e13bb7ce429f6376df3de5e0` | `7aa56e7a87acc9eb942caeba7ee1c443ef5d746b9cbfe82f287bfacf626a64c6` |

## Accepted-three preservation and approval limits

I independently compared all current files against the saved after-hashes in `accepted-three-unchanged.json`: 64/64 files each for Burgessochaeta r002, Breccia outcrop r002 and rotational landslide r001 match. No accepted candidate was rebuilt or rerendered.

The r003 candidate record is valid but still `approved_for_brief: false`; required stages and formal approval remain pending/unknown in the producer record. Concept integrity is valid but evidence completeness remains false because the provider-internal generation timestamp is unavailable; I did not infer or fabricate it. This independent result is only a static recommendation; formal/user approval and any publication decision remain separate.

## Evidence files

- `differential-evidence.json`: pins, exact frame file/dimension/pixel hashes, rebuild requests/results/output hashes, preservation checks, validation outputs and visual-review record.
- `project-static.json` / `.log`, `khronos.json`, `three-parse.json`: independent exact-GLB checks.
- `source-reopen.json` / `.log`: independent read-only Blender reopen and per-part topology/volume.
- `khronos-three.mjs`: the local read-only Khronos and Three.js check harness.

No producer files or approval states were changed. The original batch report remains outside this subfolder and its hash was verified unchanged. No upload, push, merge, GPU test or populated-scene test was performed.
