# Batch 30 independent QA — source `8364657631781954cb8a855e1fd9bd23371507cd`

**Overall: PASS.** Four reviewed candidate refs are pinned individually below. No model changes were made; no must-fix issues were found. Capinatator is accepted with a readability note: the two ribbed head-spine fans are visible in hero/near images but become small in the nine-copy scene view at its nominal hand scale.

## Source and scope binding

- Batch handoff ref: `handoff/batch30-20261018` @ `8364657631781954cb8a855e1fd9bd23371507cd` (the checked-out QA base).
- Handoff docs SHA-256: `969eeedfce26dbbf9a81b6a0854c3a30994b0a813a5ddb85d90f30018e9886f9`.
- `final-handoff.jsonl` SHA-256: `fc5e64ec764f5db9afa81f2d0cc403eb3c4ccd1408fbff8d7a168e1e51b3fd5a`.
- `scope.json` SHA-256: `d16ac0afd2e8e081c65353bf9929c096adba5935639189a10ae5f06b47437d48`.
- Allowed IDs: peltaspermum, capinatator, cothurnocystis, pyrite-cube-cluster.

## Per-item result and exact artifact binding

### peltaspermum — PASS

- Candidate `candidate/batch30-peltaspermum-20261018` @ `e49e64e8c3ad92eb7a4c962466648a90f6badccd`; editable Blend SHA-256 `1ed28d198578faa1c9458759ec329a0ecca53aac0a1d37b654dcd16bf69fb1d4`.
- GLB SHA-256 `8881b5b2eb3fb1a26b9f829ecf078ab99b8102e06f17c8e9ad4c431ee0aed53d` (111112 bytes), 3,296 triangles, 3 materials, 5 primitives, 0 textures; matches the handoff pin.
- Nominal art scale 0.08 m, hand-scale class (preserved disc-and-stalk span); independently measured GLB bounds 0.06282 × 0.08000 × 0.05520 m.
- Visual finding: The thin scalloped peltate disc, curved cut stalk, and attached underside ring of simplified ovulate bases remain legible together in neutral and color views. The connections read as one preserved reproductive organ, without implying a mushroom, flower, or parent plant.
- Technical findings: static profile 2026-10-18.1 passes; Blend reopens at unit scale 1 with identity root and finite/nonzero faces; fixed8/transparent-cover hashes match; fresh rebuild reproduces the exact GLB SHA; Khronos validation reports 0 errors / 0 warnings; runtime succeeds with 0 GL errors.
- Nine-copy runtime: 45 draw calls, 29,664 triangles, 14,991 foreground pixels; functional/software-runtime evidence only.

### capinatator — PASS_WITH_NOTE

- Candidate `candidate/batch30-capinatator-20261018` @ `02e5844cb85ac7527e1dfb8fc73c3fe8ec4b36a4`; editable Blend SHA-256 `646752ef69d241fade056edd038d18c07c33775ceadff2244179e45d4bd87f67`.
- GLB SHA-256 `05fc25048a80525e84e4e0511ce6943bcbef85c431637ea2d95e6a38bcb6b616` (89140 bytes), 4,760 triangles, 2 materials, 2 primitives, 0 textures; matches the handoff pin.
- Nominal art scale 0.08 m, hand-scale class (body length); independently measured GLB bounds 0.01018 × 0.00725 × 0.08480 m.
- Visual finding: The continuous slender body and two opposed ribbed, gently curved head-spine fans are visible in the hero, reverse, and near GLB views. The fans become small in the nine-copy scene view, but remain adequate at the nominal 8 cm hand scale; the static stylized form avoids exaggerated fangs and action.
- Technical findings: static profile 2026-10-18.1 passes; Blend reopens at unit scale 1 with identity root and finite/nonzero faces; fixed8/transparent-cover hashes match; fresh rebuild reproduces the exact GLB SHA; Khronos validation reports 0 errors / 0 warnings; runtime succeeds with 0 GL errors.
- Nine-copy runtime: 18 draw calls, 42,840 triangles, 2,107 foreground pixels; functional/software-runtime evidence only.

### cothurnocystis — PASS

- Candidate `candidate/batch30-cothurnocystis-20261018` @ `bdf75953e0669c340c6f3ac20e43ed1c33c8dc80`; editable Blend SHA-256 `020b6e85a1bd99d5e6eb59107a99257a559b948a98436d1dcdee61e32c5a3312`.
- GLB SHA-256 `a85958e6a41329e7b312c5e4ce79c743b3b9aa6444c9af90d699c18952ede398` (27620 bytes), 1,062 triangles, 3 materials, 4 primitives, 0 textures; matches the handoff pin.
- Nominal art scale 0.08 m, hand-scale class (body and appendage span); independently measured GLB bounds 0.02617 × 0.00434 × 0.08000 m.
- Visual finding: The flattened asymmetric plated theca reads as a boot-like body with one long curved, jointed appendage seated at its base. Normal and near views show the body-to-appendage transition; no second appendage or spherical/starfish-like stretch is present.
- Technical findings: static profile 2026-10-18.1 passes; Blend reopens at unit scale 1 with identity root and finite/nonzero faces; fixed8/transparent-cover hashes match; fresh rebuild reproduces the exact GLB SHA; Khronos validation reports 0 errors / 0 warnings; runtime succeeds with 0 GL errors.
- Nine-copy runtime: 36 draw calls, 9,558 triangles, 3,516 foreground pixels; functional/software-runtime evidence only.

### pyrite-cube-cluster — PASS

- Candidate `candidate/batch30-pyrite-cube-cluster-20261018` @ `5e3b7beb7f26f5d6abbf150eb7ca293037f6ee5d`; editable Blend SHA-256 `1ce5e585e2458455a9c6a61cced6479540322de4c76f14ae2e0556dfaccd73c0`.
- GLB SHA-256 `a251f2af26008af409b94dd11e61dd52e76087926a5dbcaad29990cf53ed0ce6` (24556 bytes), 380 triangles, 3 materials, 3 primitives, 0 textures; matches the handoff pin.
- Nominal art scale 0.18 m, hand-scale class (crystal cluster span); independently measured GLB bounds 0.18000 × 0.12065 × 0.12143 m.
- Visual finding: The composition has a faceted host matrix, a dominant cubic crystal, subordinate intergrowths, and stepped face offsets. It reads as a stylized natural-process cluster rather than a repeated industrial grid; palette and exact mineral chemistry are not asserted.
- Technical findings: static profile 2026-10-18.1 passes; Blend reopens at unit scale 1 with identity root and finite/nonzero faces; fixed8/transparent-cover hashes match; fresh rebuild reproduces the exact GLB SHA; Khronos validation reports 0 errors / 0 warnings; runtime succeeds with 0 GL errors.
- Nine-copy runtime: 27 draw calls, 3,420 triangles, 28,634 foreground pixels; functional/software-runtime evidence only.

## Review method and outcomes

- Rechecked every candidate’s `checksums.sha256`; all entries pass. The fixed manifest contains exactly `hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`, with 0 turntable frames. Seven views are 512×512 and the silhouette is 128×128; the separate transparent cover is also hash-bound. Every image hash matches its manifest and the manifest binds the exact submitted GLB SHA.
- Reopened each submitted Blend in Blender 4.3.2 without saving. Unit scale is 1.0, root transform is identity, evaluated and authored vertex counts match, all vertex normals are finite, face areas are positive, and component edges are manifold. Source-export bounds/triangle reports match the GLBs.
- Fresh rebuilds yielded byte-identical GLBs for all four items. Independent static GLB audits pass. Khronos glTF Validator 2.0.0-dev.3.10 returned 0 errors and 0 warnings per GLB.
- Independently reloaded each exact GLB using Chromium + Three.js r180 `GLTFLoader`. All seven runtime views rendered with no page errors or GL errors. Rendering used ANGLE SwiftShader software WebGL; timings are not a physical-device or production benchmark.
- Reviewed the five disclosed smooth-face style prompts in the actual pixels: peltaspermum’s disc/stalk and underside attachments (2), capinatator’s continuous body and paired spine fans (2), and cothurnocystis’s segmented appendage (1). These read as intentional soft surfaces/connections; no missing-face or broken-mesh issue was found. Pyrite has none.
- The profile contract and candidate-record validity pass for all four under `static-stylized-v1 / 2026-10-18.1`. Maker `approved_for_brief` remains false and maker independent stages remain unknown; this report is the separate review result and does not alter those records or publication authority.

## Must-fix items

None for this independent asset QA.

## Separate gate / limitation

The handed-off legacy project checker still reports missing license-key values on four consulted-only reference records (`FL-peltaspermum.license`, `IV-CAPINATATOR.license`, `IV-ECHINODERM-FORMS.license`, `EN-MI2.license`). No third-party license was inferred or fabricated. This QA does not clear that separate licensing/publication gate. Runtime evidence is SwiftShader-only.

Machine-readable review: [`review.json`](./review.json).
