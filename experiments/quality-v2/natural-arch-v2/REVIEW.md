# Natural arch v2 · independent quality sample

Status: **complete for visual review; not an approved replacement for the baseline pack.**

The original ten assets remain the base package. This experiment changes only one natural arch and its own render/comparison files. It is deliberately scoped as a single example, not a new production batch.

## What changed

- Two tilted weak beds now change the actual surface depth and support width. The upper bed has stronger retreat on the left shoulder; the lower bed is stronger on the right foot. These recesses remain legible in neutral gray.
- The left shoulder has a broad, deliberately located loss of material. Its removed volume is retained as an editable fallen fragment near the left support, plus one small chip. Detail is concentrated around the failure area.
- Crown height, opening shape, support width, and front/back thickness have unequal rhythms. The rear-right shoulder is thinner, while the upper crown keeps broad quiet planes.
- Color variation is subordinate to these shapes. The original full-width dark bands have been reduced to local weak-bed exposures.

The result is still a stylized landmark. Some bedding edges are deliberately graphic, and the detached flake is rather planar. The experiment demonstrates a specific improvement in medium-scale structure; it does not establish that it is a photoreal geological reconstruction or universally preferable to the simpler base model.

## Actual measurements

All source counts below refer to the **EXPORT collection only**, excluding the hidden editable construction cutter. Exported vertices are POSITION-accessor stream vertices, including splits caused by flat normals and material boundaries. They are not authored mesh vertices.

| Measurement | Baseline v1 | Experimental v2 |
|---|---:|---:|
| Authored source vertices | 344 | 626 |
| Evaluated source vertices | 344 | 626 |
| Exported POSITION stream vertices | 1,312 | 2,354 |
| Source / exported triangles | 672 | 1,240 |
| glTF primitives | 6 | 6 |
| Materials | 3 | 3 |
| GLB bytes | 40,656 | 69,264 |

The extra 568 triangles describe undercut cross-sections, the shoulder break, and local thickness changes. This is a focal landmark/gallery-inspection budget, not a universal cap or a triangle target. One close/medium mesh is supplied. Distant LODs, target-device frame times, and an eight-instance stress scene have **not** been measured.

Size including the local fragment: 5.450685 × 2.398272 × 3.487207 meters (Blender X/Y/Z). Ground contact is at Z=0; exported axes follow the shared glTF pipeline.

## Evidence and checks

- Source mesh audit: 1,240 triangles, three closed manifold mesh components, no source errors or warnings.
- Khronos glTF Validator 2.0.0-dev.3.10: **0 errors, 0 warnings**. Full report: `gltf-validator.report.json`.
- Independent GLB import: 1,240 triangles and bounds error **0 m**. Actual imported mesh and wireframe images were opened for review. The importer's raw boundary/smooth-face warnings are normal-split topology/style flags, not evidence of holes: the source meshes have zero boundary and nonmanifold edges, and no missing surface was observed in the roundtrip render.
- Own hero, alternate-key gray, rear, side, and imported-GLB renders were inspected. The initial draft's overly continuous grooves were reduced, the opening crown was raised, and the fallen fragment was laid on its broad fracture face rather than left perched on a corner.
- A comparison-camera initialization error was found by opening the pixels and corrected before delivery. It affected temporary comparison images only.
- `comparison/index.html` pairs old/new color, gray hero, gray reverse, and gray side. Each pair uses the **same camera transform, orthographic span, fixed light rig and exposure** based on the union of both asset bounds. No independent size normalization or high-contrast v2-only lighting is used. All comparison renders are 1024×1024, Cycles CPU, 32 samples, Standard, exposure 0; key/fill power is 3:1.
- Main previews are 1024×1024 at 32 samples. GLB roundtrip diagnostic is 512×512 at 24 samples. Fine sampling noise is left visible; there is no 256-sample beauty pass.

## Reproduction

From the repository root, using Blender 4.3.2:

```sh
/usr/bin/blender -b -t 3 --python-exit-code 1 --python scripts/experiments/build_natural_arch_v2.py
/usr/bin/blender -b -t 3 --python-exit-code 1 --python scripts/experiments/build_natural_arch_v2.py -- --compare
node scripts/validate_gltf.cjs experiments/quality-v2/natural-arch-v2/natural-arch-v2.glb
/usr/bin/blender -b -t 2 --factory-startup --python-exit-code 1 --python scripts/check_glb_roundtrip.py -- experiments/quality-v2/natural-arch-v2/natural-arch-v2.glb --samples 24 --resolution 512
```

The generator is deterministic, but this sample has not been subjected to a second independent byte-identical rebuild test. Do not substitute the baseline pack's rebuild evidence for this sample.

## Ownership and study

Original geometry and generator by Leon Made This / s010s; model and preview assets: **CC-BY-4.0**. General erosion context is identified in `metadata.json`. This is not a reconstruction of a named arch or a measured geological locality.

The design lesson is documented in `qa/reference-quality-study.md`: recognizable intermediate structure and meaningful placement of detail. No RHS059 model, generator code, palette, texture, or screenshot is incorporated. No third-party reference license is implied.
