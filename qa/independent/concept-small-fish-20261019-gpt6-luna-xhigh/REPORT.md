# Independent QA: four concept-led small fish

**Decision:** all four assets pass this bounded visual, brief, file, scale, and source-to-export review. No model repair is recommended. This is not formal production acceptance or release approval; the open evidence and runtime limits below remain explicit.

**Candidate frozen for review:** [`3196c36c51d5a14487dcd4ebbebcafc00aa933d7`](https://github.com/s010s/lowpoly-vault/commit/3196c36c51d5a14487dcd4ebbebcafc00aa933d7), draft PR #22. The frozen candidate descends from main [`bac6621fc39144b3759c53b1b27231ac1b6e21c6`](https://github.com/s010s/lowpoly-vault/commit/bac6621fc39144b3759c53b1b27231ac1b6e21c6), which contains the current review skills and contract. No `AGENTS.md` exists in the checked tree. Requested QA model: GPT-6 Luna XHigh.

This QA record is on branch `qa/independent-concept-small-fish-20261019`. Only QA documentation and supporting evidence are added on this branch. The four source and model files are unchanged. Nothing was merged to main, released, deployed, or used to change repository permissions; no CI rerun was triggered.

## Scope and inspected evidence

The review follows the checked-in concept-guided, low-poly art-direction, factual-review, and standardized Blender QA standards. It treats each object as the brief's **original stylized, taxon-inspired scene prop**, not as a specimen reconstruction. Generated concepts guide aesthetic choices; source records and claims are considered separately.

I opened the original four-row concept image and each fish's individual exact-GLB concept-angle image. I inspected all 11 full-resolution proof images for each of the four exports: hero, reverse hero, front, rear, both lateral views, top, bottom, clay, alternate-key clay, and triangulated wire. I also reviewed each brief, source ledger, build configuration, and image manifest. The 44 multiview proof PNGs and four individual concept-match PNGs were hash- and dimension-checked against their manifests and exact GLB hashes; the original concept, prompt, source, brief, and GLB bindings were independently hashed as well.

The review did not use maker self-check scores as its verdict. Independent results and scripts are in [`evidence/`](evidence/); the SHA-256 inventory lists **121 files**: relevant frozen candidate files, all reviewed images, and the QA evidence. See [`evidence/artifact-hashes.json`](evidence/artifact-hashes.json). The manifest verification confirms the concept sidecars' artifact hashes and every rendered proof hash/byte length/dimension.

## Per-asset result

| Asset | Result for this study | Independent visual and structural observations | Factual scope / scale note |
|---|---|---|---|
| **Metaspriggina** | **PASS — no model correction** | Slender spindle, large paired eyes, seven paired flank landmarks, and a continuous tapered tail fold remain readable in side, top, rear, clay, and opposite three-quarter views. The gill cues are raised exterior marks, consistent with the brief's explicit stylization rather than exposed internal arches. Coral/cream grouping and faceting match the concept direction without depending on a single camera. | GLB length **0.06552 m** versus approximate **0.070 m** brief scale (6.4% shorter). Primary redescription supports paired camera-type eyes and branchial bars with externally located gills; exact color and species-level proportions are not claimed. [Conway Morris & Caron 2014](https://pubmed.ncbi.nlm.nih.gov/24919146/). |
| **Falcatus** | **PASS — no model correction** | Fusiform body, paired fins, forked caudal outline, and the narrow anterior-curving dorsal spine distinguish it from the other fish. The spine remains visibly separate from the snout as required; it does not rely on tip-to-nose contact. Opposite-side and top views preserve its attachment and the family palette/facet scale. | GLB length **0.26712 m** versus approximate **0.280 m** brief scale (4.6% shorter). The male-inspired spine cue matches the stated scope; no female or exact sex/age reconstruction is asserted. [Smithsonian Ocean](https://ocean.si.edu/ocean-life/sharks-rays/ancient-shark-falcatus-falcatus); primary morphology paper DOI [Lund 1985](https://doi.org/10.1080/02724634.1985.10011842). |
| **Pteraspis** | **PASS for stylized concept scope — anatomy remains partly unknown** | Thick shield volume survives top and rear views; pointed rostrum, narrow trunk, single shield spine, lateral flanges, and lower-lobe-led tail remain visible. The ochre/brown material split reinforces the shield/trunk distinction. A clean-import measurement shows the lower lobe tip extends **9.2 mm farther rearward** than the upper tip, matching the brief's shape hierarchy. This is a model measurement, not a validated fossil ratio. No disconnected-looking feature or missing rear/underside volume rose to a rework defect. | GLB length **0.23920 m** versus approximate **0.230 m** brief scale (4.0% longer). I leave shield plate layout, proportions, and exact tail-lobe restoration **unknown**: the cited UCL page could not be fetched (502), while Kermack 1943 is a primary treatment of the hypocercal tail but does not establish the model's detailed armor restoration in the accessible abstract. This is not blocking for the accurately labeled inspired prop. [Kermack 1943](https://journals.biologists.com/jeb/article/20/1/23/4799/The-Functional-Significance-of-the-Hypocercal-Tail). |
| **Dorypterus** | **PASS — no model correction; non-blocking scale disclosure** | Deep, laterally compressed body, high rear-swept pennant dorsal fin, small tail, paired pectorals and jugular pelvic fins read in profile, top, bottom, and rear. The large sail and broad body are intentional stylization, not a silhouette failure. The sparse sail ridges stay subordinate to the body and fin outline. | GLB length **0.09960 m** versus approximate **0.120 m** brief/config scale (**17.0% shorter**). This is still a plausible small-fish scale and the brief labels it approximate, so I do not recommend changing geometry. If a downstream scene relies on exactly 12 cm, update the declared length or scale before that integration. Westoll's primary abstract supports the very compressed body form, long dorsal fin, and jugular pelvic fins. [Westoll 1941](https://zslpublications.onlinelibrary.wiley.com/doi/abs/10.1111/j.1469-7998.1941.tb00042.x). |

### Shared art and brief gates

- **Recognition — pass:** each fish has a distinct color-independent major outline/landmark: Metaspriggina's gill-cued spindle, Falcatus's curved dorsal spine, Pteraspis's shield/rostrum, and Dorypterus's deep body and tall sail.
- **Structural completeness — pass in inspected views:** fins and landmarks retain visible thickness and connections from both sides, top, and underside. I saw no accidental holes, collapsed forms, clipped tail, or single-camera-only construction needing repair.
- **Planes, color, lighting — pass:** broad facets and calm color groups remain legible in both clay lights and color renders. No obvious flipped-face or unexpected shading break was apparent. The original concept's softer rendering and each GLB's more angular planes are a documented style translation, not a defect.
- **Family consistency — pass:** consistent matte, faceted low-poly language and eye treatment; each asset differs by structure rather than recolor alone.
- **Claim honesty — pass:** the briefs and labels say “inspired” and “not a scientific reconstruction.” Artistic color, exact dimensions, and simplified fin detail are not represented as fossil observations.

## Independent technical checks

Blender 4.3.2 clean-imported each delivered GLB independently, then compared it with the corresponding saved `.blend`. Evaluated triangle totals, Blender-space dimensions, used material names, linear base colors, roughness, and metallic factors matched for every pair; dimensions and triangle totals matched exactly at the reported precision. The Falcatus source file also contains one unused `transition` material slot; the GLB correctly exports only its five used materials.

| Asset | GLB bytes / triangles / primitives / used materials | GLTF dimensions (X width × Y height × Z length, metres) | GLB SHA-256 | `.blend` SHA-256 |
|---|---:|---:|---|---|
| Metaspriggina | 143,812 / 2,296 / 30 / 6 | 0.01200 × 0.01365 × 0.06552 | `f81fd7312d73ee25ebf03b6d2984ccb0b87cc64e30136d57693358d925396950` | `5799ef37289782744d4f7b35cca8d2771182e1590698b4fac9ba56438a46ce80` |
| Falcatus | 108,568 / 1,628 / 23 / 5 | 0.12320 × 0.11340 × 0.26712 | `6af92b103b6c43ff50cdc400254ac6640985e7a70ee0c2a7981d073c9fea0063` | `eb285c675f7796ca4f0a86d33059649e163a46ff8f9541d20978579ec6e90176` |
| Pteraspis | 91,952 / 1,336 / 16 / 6 | 0.07820 × 0.08234 × 0.23920 | `3e2672cdef0f412d29a3c6de23b204ca966e65d827e99503850e314fb74b0674` | `73cc00ccf544182481ce56664574ce3b99e55a128f3245263096f1a5654cbc08` |
| Dorypterus | 107,160 / 1,532 / 22 / 6 | 0.03480 × 0.08112 × 0.09960 | `33955b1156a50104edbbab7f00bd244c6b17c650ec07bf6d1416ab2d3f7ef06e` | `7a67801423711974d3d82f69ed86a5be8b2260dde7cd54122009392d93833df4` |

Additional independent evidence:

- **Khronos glTF Validator 2.0.0-dev.3.10:** each exact GLB has 0 errors, 0 warnings, 0 infos, and 0 hints. Full reports are in [`evidence/khronos/`](evidence/khronos/).
- **Three.js Node GLTFLoader 0.180.0:** all four parse; triangle counts, materials, and dimensions match the Blender import. See [`threejs-node-loader.json`](evidence/threejs-node-loader.json).
- **Pteraspis caudal cue:** an independent clean-import measurement confirms the lower lobe apex is 9.2 mm farther rearward than the upper apex in this model. See [`pteraspis-tail-measurement.json`](evidence/pteraspis-tail-measurement.json); this checks the brief's design decision only.
- **Browser small scene:** all four exact GLBs loaded into one Three.js 0.180.0 scene and rendered in Chromium WebGL2. Measured result: **91 draw calls / 6,792 triangles** for one copy of each. The renderer identifies as ANGLE SwiftShader, so this is a real browser software-WebGL render, not a hardware-GPU test. The saved image is [`threejs-webgl-scene.png`](evidence/threejs-webgl-scene.png); raw environment/result is [`threejs-webgl-result.json`](evidence/threejs-webgl-result.json).

The declared swimming-midline origin explains that the fish extend below the nominal origin; this is not a ground-contact failure. Their meshes are not intended to sit on a floor.

## Remaining formal gates and blockers

1. **Chronology evidence is incomplete for a formal candidate.** All four concept sidecars retain `concept_generated_at: null` and `concept_inspected_at: null`; the generation record says both times were unrecorded. The genuine prompt and image are present, and the brief's model-start times are recorded, but missing times must not be inferred from file mtimes. `binding-verification.json` confirms these values. This blocks a complete chronology record, not the models' visual pass.
2. **Hardware GPU and production populations remain unverified.** The local browser used SwiftShader and one copy of each model. No hardware-GPU run or 8/32-copy target-scene performance run was made. Do not interpret 91 calls / 6,792 triangles as a performance pass for the target museum scene.
3. **Pteraspis exact reconstruction remains out of scope and unknown.** The source access limit above must stay visible if the claim is ever upgraded from “inspired” to a species reconstruction.
4. **CI is not independent QA evidence.** The candidate handoff records the GitHub Actions/Pages service incident and queued main CI; no workflow rerun was attempted. Confirm current CI separately before any later release.

These open gates prevent describing this study as `accepted_for_brief`, production-approved, or release-ready. They do not justify unnecessary geometry changes to the four current stylized assets.

## Reproduction

From the repository root, the saved scripts reproduce the independent file/import and format checks. For the browser run, start a local read-only static server from the repository root, then execute the Playwright runner with its output paths:

```sh
blender --background --factory-startup --disable-autoexec --threads 2 \
  --python-exit-code 1 \
  --python qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/blender_reimport.py -- \
  /tmp/independent-blender-reimport.json \
  metaspriggina production/concept-small-fish-20261019/metaspriggina/r001/output/metaspriggina.blend production/concept-small-fish-20261019/metaspriggina/r001/output/metaspriggina.glb \
  falcatus production/concept-small-fish-20261019/falcatus/r001/output/falcatus.blend production/concept-small-fish-20261019/falcatus/r001/output/falcatus.glb \
  pteraspis production/concept-small-fish-20261019/pteraspis/r001/output/pteraspis.blend production/concept-small-fish-20261019/pteraspis/r001/output/pteraspis.glb \
  dorypterus production/concept-small-fish-20261019/dorypterus/r001/output/dorypterus.blend production/concept-small-fish-20261019/dorypterus/r001/output/dorypterus.glb
node qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/threejs_node_load.mjs
node qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/validate_gltf.mjs
python3 qa/independent/concept-small-fish-20261019-gpt6-luna-xhigh/evidence/verify_artifact_bindings.py
```
