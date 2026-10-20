# Independent QA report: batch 63 fixed candidates

## Executive disposition

| Candidate | Technical | Visual | Factual | Specification | Runtime parse | Independent disposition |
|---|---|---|---|---|---|---|
| Siphusauctum r001 | PASS | PASS | PASS, bounded | PASS | PASS | ACCEPT BOUNDED |
| Esker r001 | PASS | PASS | PASS, bounded | PASS | PASS | ACCEPT BOUNDED |
| Caldera r001 | PASS | REVISE | REVISE, feature evidence incomplete | REVISE | PASS | REVISE |
| Dogtooth spar cavity r002 | PASS | PASS | PASS, generic habit bounded | PASS | PASS | ACCEPT BOUNDED |

“Accept bounded” is an independent QA recommendation for technical, visual, factual, specification and CPU parser criteria only. The project candidate/profile validator still says valid/pending with approved_for_brief=false. GPU rendering, populated-scene rendering, formal approval, user approval and publication are not established. No approval flag was changed.

## Exact source, selections and integrity

- Source: `/tmp/lowpoly-batch63-20261020`, branch `candidate/small-life-batch63-concept-20261020`, clean HEAD `d840b363277c9f0727ffb93fdf9ca7dd27ca6f4b`.
- Exact selected GLBs:
  - Siphusauctum r001: `cc0b3d56057bba735d422feaae49485572e669cda131eb2b8d21830e892c31dc`.
  - Esker r001: `4415be20721b7002b0db1319287626915af648a2086c3ba50a54a8c4ca48b3ed`.
  - Caldera r001: `5d84c7b706351559d6217e558fc8ef5458a9374043a8d001a91708c788b51258`.
  - Dogtooth-spar-cavity r002: `3db7f65435d8117dd71285b3fc7afb9d3e73f4ba68b3f2c99e219303dbb2b80c`.
- Independently matched handoff, candidate artifact records, brief/reference/source/generator/config pins, and each selected inventory row against the original inventory. Original inventory unchanged; source worktree remains clean.
- Maker revision chronology is documented: dogtooth r002 targeted visual refinement pins the original freeze and says no scope changes; caldera r002 starburst-like attempt rejected; r001 retained without alteration. No post-hoc scope narrowing is relied on.

## Per-candidate findings

### siphusauctum r001 — ACCEPT BOUNDED

- **Visual / factual / specification:** Whole external organism reads as a coherent holdfast + bilayered stem + closed ovoid calyx. Six actual basal through-ports and one terminal top opening are present; no petal/arm/tentacle reading. The ROM source supports the external fossil morphology; uncertain affinity, exact proportions and palette stay illustrative. No modern phylum or internal-anatomy claim.
- **Primary source page:** [https://burgess-shale.rom.on.ca/fossils/siphusauctum-gregarium/](https://burgess-shale.rom.on.ca/fossils/siphusauctum-gregarium/). Actual locally consulted reference-image SHA256: `c5a8198f50b969bae0c0126b10c3ed06030420c0dadf1af910a908f8fc1b3026`.

- **Hashes:** GLB `cc0b3d56057bba735d422feaae49485572e669cda131eb2b8d21830e892c31dc`; frozen brief `61525d81d701637b1477c0f29e497cd963ef50c2ba409720bb81d51231485ac3`; references `0ef7c59d18b8aaa27063fb60fdc13b1d8339ada4627242b5679381c1d7f3050d`; Blender source `c02dc9653a356a529149177ffeef754d42a66b7dc4c79d437d6d666ad64ad1fd`.
- **Geometry:** 2,756 triangles; 149,920 bytes; 4 materials; 6 primitives; 0 textures. Measured GLB envelope X×Y×Z: `[0.07244999706745148, 0.2199999988079071, 0.06768354773521423]` m. Nominal plan only, not a measurement: `[0.07, 0.07, 0.22]` Blender XYZ m; `Nominal22cm complete specimen height, not a measured holotype; approximately11cm stem and11cm calyx. Actual export envelope reported separately.
- **Build provenance:** local procedural seed `6300`; generator/config/source SHA256s as above; pinned dependencies `{'Blender': '4.3.2', 'Three.js': '0.180.0', 'GLTF exporter': 'Khronos glTF Blender I/O v4.3.47'}`. Provider image-generation seed/version was not returned; it is not fabricated.
- **Blender source reopen:** 4 mesh object(s), 2,756 evaluated triangles reconcile with exported GLB; Blender XYZ bounds `[0.07244999706745148, 0.06768354773521423, 0.2199999988079071]` m (axis-converted bounds reconcile). Every mesh: zero welded boundary/nonmanifold/wire edges and zero degenerate triangulated faces.
- **Exact proof render:** 2026-10-20T13:05:12.039680+00:00 by pinned CPU runner SHA256 `568582dccbe712f289eaabe528c4ddd574f7c77b10fa91d277c420b7d9e5ef1b`; `hero, reversehero, front, side, rear, top, clay, silhouette` frames, each actual 512×512, individually inspected and hash-checked. Manifest subject binds selected GLB, brief and references. This is CPU-render evidence only, not GPU proof.
- **Two queue rebuilds:** run1 PID 344 2026-10-20T13:04:24.464721+00:00→2026-10-20T13:04:27.525244+00:00 SHA cc0b3d56057bba735d422feaae49485572e669cda131eb2b8d21830e892c31dc semantic 5734298a547c7ff2dc6f5125988c99ac4336ceea1cf21f6a34d39d3cc3b8fbe7, run2 PID 366 2026-10-20T13:04:27.526922+00:00→2026-10-20T13:04:30.749423+00:00 SHA cc0b3d56057bba735d422feaae49485572e669cda131eb2b8d21830e892c31dc semantic 5734298a547c7ff2dc6f5125988c99ac4336ceea1cf21f6a34d39d3cc3b8fbe7. Distinct successful queue-bound requests/PIDs/output dirs; semantic digest independently recomputed on each output. Runner records remain attestations, not cryptographic execution proof.

### esker r001 — ACCEPT BOUNDED

- **Visual / factual / specification:** A positive, sinuous S-ridge with rounded uneven crest and sloping flanks; top/oblique views do not read as a channel, riverbed or canyon. Generic full-volume landform, not named, dated, or directionally asserted. Surface is intentionally quiet/texture-free and scale remains illustrative.
- **Primary source page:** [https://www.usgs.gov/media/images/a-simple-esker-iceland](https://www.usgs.gov/media/images/a-simple-esker-iceland). Actual locally consulted reference-image SHA256: `630a6296a521b88caffe3d539fec856bd758f3a25cbdaab4d60510cf22c92adb`.

- **Hashes:** GLB `4415be20721b7002b0db1319287626915af648a2086c3ba50a54a8c4ca48b3ed`; frozen brief `eab68e8711f05103181cfdb85957a4d218da9273088fca3d58aca609cc3185e6`; references `4ce774fb42f3c57025b71f0f3cae7a4b93bbc2fad08697c2e0d65447fe02448a`; Blender source `6d3d5d0d30dce12551d2cd61c513927490799c2447fde21c7bfc416ef90b980e`.
- **Geometry:** 2,142 triangles; 164,388 bytes; 3 materials; 3 primitives; 0 textures. Measured GLB envelope X×Y×Z: `[225.45072174072266, 34.762596130371094, 700.0]` m. Nominal plan only, not a measurement: `[230, 700, 35]` Blender XYZ m; `Nominal700m long ridge with70m local full width and35m relief. Sideways sinuous displacement widens overall footprint to approximately230m; no measured locality claim.
- **Build provenance:** local procedural seed `6301`; generator/config/source SHA256s as above; pinned dependencies `{'Blender': '4.3.2', 'Three.js': '0.180.0', 'GLTF exporter': 'Khronos glTF Blender I/O v4.3.47'}`. Provider image-generation seed/version was not returned; it is not fabricated.
- **Blender source reopen:** 1 mesh object(s), 2,142 evaluated triangles reconcile with exported GLB; Blender XYZ bounds `[225.45071411132812, 700.0, 34.762596130371094]` m (axis-converted bounds reconcile). Every mesh: zero welded boundary/nonmanifold/wire edges and zero degenerate triangulated faces.
- **Exact proof render:** 2026-10-20T13:05:24.260074+00:00 by pinned CPU runner SHA256 `568582dccbe712f289eaabe528c4ddd574f7c77b10fa91d277c420b7d9e5ef1b`; `hero, reversehero, front, side, rear, top, clay, silhouette` frames, each actual 512×512, individually inspected and hash-checked. Manifest subject binds selected GLB, brief and references. This is CPU-render evidence only, not GPU proof.
- **Two queue rebuilds:** run1 PID 388 2026-10-20T13:04:30.750055+00:00→2026-10-20T13:04:33.412139+00:00 SHA 4415be20721b7002b0db1319287626915af648a2086c3ba50a54a8c4ca48b3ed semantic 58419b5fe951c50fc09a055b8f9988ebdc8260c2352855e4ed311fdbb3dc4b0c, run2 PID 410 2026-10-20T13:04:33.412992+00:00→2026-10-20T13:04:36.463910+00:00 SHA 4415be20721b7002b0db1319287626915af648a2086c3ba50a54a8c4ca48b3ed semantic 58419b5fe951c50fc09a055b8f9988ebdc8260c2352855e4ed311fdbb3dc4b0c. Distinct successful queue-bound requests/PIDs/output dirs; semantic digest independently recomputed on each output. Runner records remain attestations, not cryptographic execution proof.

### caldera r001 — REVISE

- **Visual / factual / specification:** Broad subsided basin, floor, inward scarp and outward slope are present and low relief is appropriate. However hero/reverse/front/top show a largely continuous, nearly regular terraced rim; the subdued breach is only a shallow, hard-to-read dip, so the frozen uneven remnant rim and one-breach obligations are not clearly evidenced. Minimal repair: preserve r001 scale and basin, make one small but unambiguous low saddle interrupt the rim in top + oblique views, and vary only adjacent rim/scarp heights into restrained irregular bays. Do not add a dramatic opening, starburst fluting, lava, or any new claim. r002 attempt was correctly rejected for starburst-like regularity; r001 is unchanged.
- **Primary source page:** [https://home.nps.gov/articles/000/older-caldera-complexes.htm](https://home.nps.gov/articles/000/older-caldera-complexes.htm). Actual locally consulted reference-image SHA256: `521addd6146d20e9eee40e7a1ca3a5006b07ea0d8c586830e48f5053325b5508`.

- **Hashes:** GLB `5d84c7b706351559d6217e558fc8ef5458a9374043a8d001a91708c788b51258`; frozen brief `01f3faf7a696d3f7a60a127535ce877a8115001f21318a52c32ff27c37adc54d`; references `2f9689b429ed45683b3b06a6eb6181b6ff69db80254a0fe2c7cfe2b0714cd25b`; Blender source `495e3968dc88f24b3aa2bcfcc4310c5e76a55c2178766579d72dd1b1b7d59c44`.
- **Geometry:** 1,294 triangles; 102,176 bytes; 4 materials; 4 primitives; 0 textures. Measured GLB envelope X×Y×Z: `[4075.9818115234375, 529.3335571289062, 3474.0985107421875]` m. Nominal plan only, not a measurement: `[4000, 3400, 550]` Blender XYZ m; `Illustrative nominal4000m by3400m footprint and550m relief; broad approximately2200m basin. No measured named-site proportions or chronological claim.
- **Build provenance:** local procedural seed `6302`; generator/config/source SHA256s as above; pinned dependencies `{'Blender': '4.3.2', 'Three.js': '0.180.0', 'GLTF exporter': 'Khronos glTF Blender I/O v4.3.47'}`. Provider image-generation seed/version was not returned; it is not fabricated.
- **Blender source reopen:** 1 mesh object(s), 1,294 evaluated triangles reconcile with exported GLB; Blender XYZ bounds `[4075.98193359375, 3474.0986328125, 529.3335571289062]` m (axis-converted bounds reconcile). Every mesh: zero welded boundary/nonmanifold/wire edges and zero degenerate triangulated faces.
- **Exact proof render:** 2026-10-20T13:05:41.635361+00:00 by pinned CPU runner SHA256 `568582dccbe712f289eaabe528c4ddd574f7c77b10fa91d277c420b7d9e5ef1b`; `hero, reversehero, front, side, rear, top, clay, silhouette` frames, each actual 512×512, individually inspected and hash-checked. Manifest subject binds selected GLB, brief and references. This is CPU-render evidence only, not GPU proof.
- **Two queue rebuilds:** run1 PID 432 2026-10-20T13:04:36.464634+00:00→2026-10-20T13:04:40.465277+00:00 SHA 5d84c7b706351559d6217e558fc8ef5458a9374043a8d001a91708c788b51258 semantic 24d534c0dc305fa8a75958a18d9611a102f0a6ed2f1b32b99d5fbf6e55fb7a29, run2 PID 454 2026-10-20T13:04:40.466248+00:00→2026-10-20T13:04:43.198448+00:00 SHA 5d84c7b706351559d6217e558fc8ef5458a9374043a8d001a91708c788b51258 semantic 24d534c0dc305fa8a75958a18d9611a102f0a6ed2f1b32b99d5fbf6e55fb7a29. Distinct successful queue-bound requests/PIDs/output dirs; semantic digest independently recomputed on each output. Runner records remain attestations, not cryptographic execution proof.

### dogtooth-spar-cavity r002 — ACCEPT BOUNDED

- **Visual / factual / specification:** Open-front, deep cavity with thick closed host/back; irregular inward-pointing acute crystals have triangular/scalenohedral planes, mixed lengths/depths and preserve a readable void. NPS supports pointed calcite dogtooth spar lining limestone pockets; the Smithsonian National Museum of Natural History source also explicitly identifies dogtooth calcite as scalenohedral. Supports a generic habit, not an assay, measured specimen, or specific cave-site claim.
- **Primary source page:** [https://www.nps.gov/wica/learn/nature/cave-formations-speleothems.htm](https://www.nps.gov/wica/learn/nature/cave-formations-speleothems.htm). Actual locally consulted reference-image SHA256: `dc6d532a76a34e349dfaf4c877a71c11278d712afcc6422eb2650d25cfe8a4e0`.
- **Supplementary morphology check:** [Smithsonian NMNH calcite record](https://naturalhistory.si.edu/explore/collections/geogallery/10026196) supports the generic dogtooth/scalenohedral label; this does not narrow or alter the frozen claim scope.

- **Hashes:** GLB `3db7f65435d8117dd71285b3fc7afb9d3e73f4ba68b3f2c99e219303dbb2b80c`; frozen brief `9446f34a9da82429c0551f43de15c3a3147b935464ec8dc19288e31c9608e1d9`; references `a5cf9e0b0a89c40eb0b1199d6a67dd139541db9761de92186b14ad0558834b72`; Blender source `55d421ce9acc4dd259d4c4df88e251c7550fb90e76ebbeaa0d43232723daefc0`.
- **Geometry:** 1,284 triangles; 89,488 bytes; 5 materials; 5 primitives; 0 textures. Measured GLB envelope X×Y×Z: `[0.4968913793563843, 0.40902290120720863, 0.2941199988126755]` m. Nominal plan only, not a measurement: `[0.45, 0.3, 0.38]` Blender XYZ m; `Illustrative hand-specimen scale45cm width,30cm depth,38cm height, cavity approximately25cm across; individual visible crystals2-8cm. Not a measurement from source photograph.
- **Build provenance:** local procedural seed `6303`; generator/config/source SHA256s as above; pinned dependencies `{'Blender': '4.3.2', 'Three.js': '0.180.0', 'GLTF exporter': 'Khronos glTF Blender I/O v4.3.47'}`. Provider image-generation seed/version was not returned; it is not fabricated.
- **Blender source reopen:** 3 mesh object(s), 1,284 evaluated triangles reconcile with exported GLB; Blender XYZ bounds `[0.4968913793563843, 0.29412001371383667, 0.40902289748191833]` m (axis-converted bounds reconcile). Every mesh: zero welded boundary/nonmanifold/wire edges and zero degenerate triangulated faces.
- **Exact proof render:** 2026-10-20T13:09:32.620117+00:00 by pinned CPU runner SHA256 `568582dccbe712f289eaabe528c4ddd574f7c77b10fa91d277c420b7d9e5ef1b`; `hero, reversehero, front, side, rear, top, clay, silhouette` frames, each actual 512×512, individually inspected and hash-checked. Manifest subject binds selected GLB, brief and references. This is CPU-render evidence only, not GPU proof.
- **Two queue rebuilds:** run1 PID 224 2026-10-20T13:08:09.534100+00:00→2026-10-20T13:08:12.622851+00:00 SHA 3db7f65435d8117dd71285b3fc7afb9d3e73f4ba68b3f2c99e219303dbb2b80c semantic 529f0cff8a348a717c7ab49aabc9dd458a5488656602b00114414c758bddb0af, run2 PID 246 2026-10-20T13:08:12.623694+00:00→2026-10-20T13:08:15.604889+00:00 SHA 3db7f65435d8117dd71285b3fc7afb9d3e73f4ba68b3f2c99e219303dbb2b80c semantic 529f0cff8a348a717c7ab49aabc9dd458a5488656602b00114414c758bddb0af. Distinct successful queue-bound requests/PIDs/output dirs; semantic digest independently recomputed on each output. Runner records remain attestations, not cryptographic execution proof.

## Independent validation and approval boundaries

- Candidate/profile validator: `valid=true`, no errors, profile contract pass, but `approved_for_brief=false`; all formal candidate stages remain pending/unknown. Concept evidence validators are structurally valid but incomplete for all four because `concept_generated_at` and `modeling_started_at` are unknown. These exact provider/modeling timestamps were not disclosed/sampled; no file mtimes were used to invent them.
- Independent project GLB checks passed on separate exact copies. Khronos validator: zero errors and zero warnings on each. Independent Node Three.js r180 `GLTFLoader.parseAsync` parsed each exact hash and reconciled triangle counts/bounds. This is CPU parser evidence, not a browser GPU render or populated-scene result.
- Read-only Blender 4.3.2 reopen on all four exact `.blend` files; authored/evaluated vertices/polygons/triangle-equivalents match. Per-mesh welded topology audits show zero boundary, nonmanifold, wire, zero-area/degenerate, or duplicate triangles. Axis-converted source/export bounds reconcile within tolerance.
- Two actual successful queue-bound rebuilds per selected final GLB were verified independently: separate requests, results, PIDs, timestamps and output paths; Blender, queue runner, generator, config, helper and audit identities pinned; output GLB byte hashes match the selected GLB; semantic digests independently recomputed and match. Repro logs themselves are not cryptographic proof.
- Concept chronology: request/completion-observer/inspection records precede each freeze; actual successful queue generator executions follow freeze. Exact provider concept-generation and modeling-start timestamps are absent, as is an ImageGen provider seed; the concept evidence gate correctly remains incomplete. The selected local deterministic build seeds are recorded above and are distinct from an ImageGen provider seed.
- GPU stage: **not run**. Intended composed scene: **not run**. Formal/user approval: **not granted**. Publication authority: separate. No approval, upload, commit, push, merge or publish action was taken.
- External reference pixels are consult-only; no source image was copied into this report.

## QA artifacts

- Machine-readable summary: `machine-summary.json`.
- Independent integrity/rebuild/render-binding script: `audit_batch63_integrity.py`.
- Blender read-only source inspector: `work/read_blend_readonly.py`.
- Independent GLB topology auditor: `work/audit_glb_topology.py`.
- Independent Three.js parser: `work/runtime_parse_exact.mjs`.
- Khronos, Project QA, runtime parse, Blender per-mesh and two-run semantic-rebuild outputs are under `work/` (private exact GLB copies only).
- This report is a QA recommendation; it is not formal or user approval.
