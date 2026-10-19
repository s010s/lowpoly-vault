# Three-case concept-first lesson, 19 October 2026

## R1: original pilot observations

The producing task invoked ImageGen and inspected its concept sheet before Blender
construction. This is a producer account; the retained bundle alone cannot
independently re-establish that chronology without the original tool receipt. Three original volumetric assets were then authored, exported to
GLB, reimported into clean Blender scenes and rendered in hero, rear, top and side
views. These observations support a small concept-guided study, not a universal
production standard or a promise of concept-identical meshes.

| Asset / 中文标签 | Design dimensions (Blender X/Y/Z, m) | Triangles | GLB bytes | Images/textures | Khronos errors/warnings |
| --- | --- | ---: | ---: | ---: | ---: |
| River rock / 石头 | 0.24 / 0.18 / 0.14 | 142 | 18,816 | 0 / 0 | 0 / 0 |
| Branching coral / 枝状珊瑚 | 0.30 / 0.16 / 0.26 | 3,000 | 240,024 | 0 / 0 | 0 / 0 |
| Small fish / 小鱼 | 0.16 / 0.05 / 0.11 | 1,532 | 142,420 | 0 / 0 | 0 / 0 |

Dimensions are intentional stylized design sizes, not measured specimens.
The ~1 MB goal applied only to each GLB, not editable sources or render packages.
Materials/primitives were 10/10, 10/10 and 16/41 respectively. Small files alone do
not establish low draw-call cost in a populated scene.

What transferred: broad subject identity, distinctive silhouettes, palette regions
and major landmarks. Hero and alternate views showed real depth and completed
rear surfaces. The comparison used the actual exported-GLB renders; it did not
retouch them into concept art. A single image does not constrain a unique camera
or the unseen geometry, so the comparison was approximate rather than calibrated.

What still differed:
- Rock: regular facet rhythm and a clean, nearly uniform mineral-band boundary.
- Coral: branches straighter than the concept, with some elongated triangles and
  less rounded tips/fork transitions. Rear branches were authored decisions.
- Fish: face, cheek transitions and fins remained more angular than the concept.

Refine those specific structures before adding indiscriminate subdivisions,
random surface noise or more render samples. Preserve broad readable planes.
The next revision should keep comparison settings fixed and record whether the
named weakness actually improved. Preserve these R1 observations and original
evidence. The separate R2 snapshot below does not replace or re-approve R1.

## Evidence boundaries

The original study used Blender 4.3.2 and Khronos glTF Validator
2.0.0-dev.3.10. All three saved validator reports had zero errors and warnings.
The source and GLB files, prompt, concept, scripts and 12 proof renders were
retained. The original bundle does not contain a separately persisted ImageGen
invocation/result receipt or the new helper renderer’s hash-bound render manifest.
Keep those gaps explicit in retrospective sidecars; retain the genuine image and
prompt without manufacturing timestamps or tool receipts. Mesh inspection after
clean import reported closed components with
nonzero absolute signed-volume magnitude after welding coincident split vertices
at 1e-7 m. Because the inspection used an absolute value, this does not independently
prove outward-facing orientation. This is a
particular inspection method, not proof of printable union geometry: the fish
has 15 closed components with intersecting attachments. It has no billboard
parts, textures, skin or animation in this pilot.

Pilot camera labels describe geometric directions, not a verified
canonical-forward contract. The historical `rear` and `top` cameras are oblique;
use descriptive retrospective labels `rear-oblique` and `top-oblique` while
preserving the original filenames, hashes and actual camera transforms. Do not
change their angles to fit canonical schema names. The +X camera called `side`
is an end view for the fish, whose length runs along X. Map views to the frozen
anatomical/asset axes; none of these historical labels establishes canonical
front/side/top QA. R2 reuses the same baseline transforms, so this caveat also
applies to its comparison views.

The pilot did **not** run target-browser/GPU/populated-scene acceptance. It did
not establish the full formal candidate contract, independently executed rebuild
parity, scientific species accuracy or batch throughput. Stage-level wall times
were not fully recorded; do not infer them from file dates. The retained generator
is useful source material, not by itself a reproducibility verdict.

Original evidence bundle identifiers (paths are relative to that study bundle,
which is separate from this reusable skill; no cloud filesystem path is required):

- `concepts/imagegen-concept-sheet.png` SHA-256
  `be842f2b7ee06b4df9a6c5091008e0b55c2e38aef00ce31bfea47372087ae8e9`
- `concepts/imagegen-prompt.txt` SHA-256
  `8bb5ef8ac1337276a5649d8844942b5e2f452a4405d72204ceb9331e8197b368`
- `models/river-rock.glb` SHA-256
  `22f967d23ae3a7f3708afcdbb38139b277194aa7684a8cda9f77cd47bfb6e6c5`
- `models/branching-coral.glb` SHA-256
  `53c0ff88fef8de2c165e1fba66d8ab08bbbe0a39c90f9d1e2e3fc11df6cf642f`
- `models/small-fish.glb` SHA-256
  `ae66a8362b79524a9843bcf386f56d13ee277cb43de927dbd11b4659f8aa9f0d`

Supporting observations are in `brief/modeling-brief.md`,
`reports/build-summary.json`, `reports/glb-validation-summary.json`,
`reports/*-reimport-inspection.json`, `reports/*-cameras.json`, and
`reports/review.md`. `delivery-manifest.json` binds the original deliverable files.
The concept-to-model and alternate-view contact sheets are comparison layouts,
not replacement mesh evidence. Keep this original bundle immutable.

## R2: bounded refinement snapshot, 19 October 2026

This is a separate provisional revision. The final rendered comparison has been
visually inspected; user acceptance and the formal production gates remain
separate. The metrics alone do not establish closer concept fidelity. R1 remains
unchanged.

| Asset / 中文标签 | Triangles | GLB bytes | Khronos errors/warnings |
| --- | ---: | ---: | ---: |
| River rock / 石头 | 142 | 18,812 | 0 / 0 |
| Branching coral / 枝状珊瑚 | 4,200 | 332,120 | 0 / 0 |
| Small fish / 小鱼 | 1,784 | 102,648 | 0 / 0 |

The same ImageGen concept and design dimensions are retained. The authored changes
address the named R1 gaps: an irregular geometry-bounded rock band; fuller curved
coral branch paths and tip transitions; fish cheek volume, curved closed-fin
support loops and smooth eye normals. The reviewed comparison shows a less
uniform rock band, fuller coral tips/curved branches and rounder fish fins. The
coral also has a denser facet pattern, a visible tradeoff rather than an unqualified
upgrade. More triangles are not the acceptance criterion.

The R2 comparison locks camera transforms and orthographic scales to the R1
baseline and uses the same lighting recipe and color settings. Lights are
bounds-scaled, with negligible floating-point position differences; do not call
their transforms byte-identical. Historical `rear`/`top` labels remain oblique,
and the fish +X view remains an end view. Target-browser/GPU/populated-scene
acceptance is still unrun. All three R2 GLBs have zero textures/images; the three
official Khronos reports record zero errors and warnings.

All material slots are double-sided. This is a separate normal/backface and
target-runtime cost advisory, not a Khronos validation failure. The actual
runtime impact was not measured. Neither validator success nor the reviewed
comparison establishes production acceptance or permission for batch expansion.

Source: the separate `concept-first-refinement-20261019` evidence bundle,
`reports/build-summary.json`, `reports/glb-validation-summary.json`, the three
`reports/*-gltf-validator.json` files and `reports/*-cameras.json`. Keep R2 files,
measurements and eventual review decisions separate from the R1 bundle above.

## User decision after the R2 comparison

At 15:20 UTC the user preferred the original coral and judged the other changes
small: “珊瑚还是原版更好看一点，其他差别不大。” R2 is not promoted. Retain R1 as
the design-direction baseline for all three cases; this is not production release
approval. The experiment demonstrates a useful rejection decision: fuller tips or
more triangles did not necessarily improve the preferred silhouette/facet rhythm.
Future refinement should name the visible benefit and let comparative review,
including the user's preference, decide whether to keep it. Do not summarize R2
as a quality improvement merely because it was called a refinement pass.

R2 GLB SHA-256 values (retained only as comparison evidence):
- Rock: `cf620bb604ec5bf2c182f929c025ac14be656350ad21cc9c8a50987883688fb6`
- Coral: `a313ef602f02b353ee34eda1825ffe6b0ded3f450c97b5888c3bc536b1ed78e7`
- Fish: `1e28d3c51433b36d9b54b2dafc8945c71fdd826ec762b45bd4007579fb36130e`

## What is reusable now

A concept/brief checkpoint; deliberate complete geometry; editable and scripted
sources; exact-GLB hero plus alternate-angle proof; clearly separated concept and
model imagery; matched revision comparisons; measured metrics and honest missing
stages; explicit user review before expansion. The reusable evidence checker and
templates add mechanical checks for these records without changing the existing
approval or release rules.

Copyright (c) 2026 Leon Made This / s010s. Prose and original art: CC BY 4.0;
executable code: MIT. Third-party source rights and factual claims remain separate.
