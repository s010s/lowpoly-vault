# Conifer v2: independent near-view study

This is a heavier, original close-to-medium-view sample. The existing 2,382-triangle production conifer remains the default. This experiment does not claim compliance with the reference collection's vertex limits.

## Same-camera comparison

Both versions use the same union-bounds framing, neutral lights, Standard transform, 1024px resolution and 32 samples. The invisible framing fixture is never exported or saved in a source blend.

| View | Retained base | v2 sample |
| --- | --- | --- |
| Hero | [Base hero](comparison-v1/preview-hero.png) | [v2 hero](preview-hero.png) |
| Reverse hero | [Base reverse](comparison-v1/preview-reversehero.png) | [v2 reverse](preview-reversehero.png) |
| Gray model | [Base clay](comparison-v1/preview-clay.png) | [v2 clay](preview-clay.png) |

The new sample exposes main boughs, secondary branchlet fans, fine woody shoots and short narrow solid needle groups. The first rendered version was too thin and skeletal; the final version enlarges existing needle envelopes without increasing its triangle count. Earlier images remain in `iteration-01/`.

## Measured cost

| Metric | Base | v2 |
| --- | ---: | ---: |
| Source vertices | 1,365 | 11,607 |
| Exported POSITION vertices | 4,938 | 36,144 |
| Triangles | 2,382 | 14,118 |
| Primitives | 15 | 15 |
| Materials | 6 | 6 |
| GLB bytes | 145,732 | 964,328 |

v2 costs 5.93× the triangles and 7.32× the exported vertices. Flat normals and material boundaries account for much of the source-to-export vertex increase. Dimensions are 4.336 × 7.252 × 4.656m in glTF XYZ (Y-up).

Preferred object coverage is roughly 350–650px, for an isolated focal tree or sparse near-view grove. At thumbnail scale, the fine foliage loses detail; the intentionally open, spiky crown is not a universal visual improvement over broad, economical masses. No runtime FPS claim or mass-forest suitability is made. No further LOD work is included.

## Deliverables and checks

- Editable source: `conifer-v2.blend`
- Runtime asset: `conifer-v2.glb`
- Source and GLB geometry checks pass; Khronos validator: 0 errors, 0 warnings.
- Two independent builds have identical GLB bytes and semantic hashes.
- GLB roundtrip retains 14,118 triangles; bounds discrepancy is about 0.00000012m.
- Actual hero, reverse, side, clay, alternate clay, silhouette, reimport and wireframe images were inspected. See `visual-review.json` for the visible fix and remaining tradeoffs.
- Import topology warnings caused by flat-normal split vertices were reviewed separately; source components have no boundary/nonmanifold edges. WebGL runtime benchmarking was not performed for this sample.

## Rebuild

From the repository root:

```sh
blender -b --threads 2 --python-exit-code 1 --python scripts/experiments/build_conifer_quality_v2.py
blender -b --threads 2 --python-exit-code 1 --python scripts/experiments/build_conifer_quality_v2.py -- --compare-v1
node scripts/validate_gltf.cjs experiments/quality-v2/conifer-v2
```

All geometry and code are independently authored. The unlicensed reference repository was used only for visual study; no reference meshes, code, materials or images are distributed. Model and previews: CC-BY-4.0, Leon Made This / s010s. Generator: MIT.
