# Batch 52 independent QA

**Result:** the batch is **not ready for approval**. Aturia r002 has one must-fix visual issue: a large, sharply bounded radial color sector across the shell. The other three assets have no must-fix visual or factual issue in the reviewed scope.

This review is bound to candidate commit `352d81995b33fc1e7a95980184ab6641dd5738a5`, handoff SHA256 `74a8cd809f19c7150ba2faea2a22b1aa51882b2f9b2eac97688e5b190586e568`, and the four exact GLB hashes recorded in [pinned-inputs.json](replay-20261020T003048Z/pinned-inputs.json). The dispatch QA-SCOPE file had null commit/hash fields and `ready_for_qa:false`; the dispatch instruction supplied the exact commit and handoff, which this report binds directly. All 32 hash-bound eight-view frames and all four original concept images were checked and visually reviewed.

The QA-SCOPE shell, repository instructions (no `AGENTS.md` was present), and the asset-factual-review, blender-lowpoly-pipeline, standardized-pipeline, concept-guided-lowpoly, and lowpoly-art-direction skill guidance were consulted. The review kept image inspection, factual claims, authored dimensions, export/runtime evidence, and formal approval as separate questions.

## Decision by asset

| Asset | Visual | Factual scope | Independent finding |
|---|---|---|---|
| Aturia r002 | **Fail; fix required** | Limited pass | A prominent hard-edged angular radial/annular patch reads as a cutaway or segmentation and conflicts with the smooth-shell brief; it is absent from the concept. Remove that sector or make the fossil variation much subtler and irregular, then rerender the same eight views. The shell profile itself is recognizable. |
| Phoenicopsis r001 | Pass | Limited pass | Three detached shoots carry 15 separate strap-shaped leaves. The leaves are unbranched; apparent Y intersections are overlaps between leaves. No must-fix item. |
| Cave popcorn r003 | Pass | Limited pass | The fused knobby calcite crust reads clearly on its slab. No must-fix item. |
| Curvolithus trilobed trail r001 | Pass | Limited pass | Three positive raised lobes, a broader central lobe, and separating furrows are clear from top and side views. It does not read as a negative impression. No must-fix item. |

Aturia's reference text from the Digital Atlas of Ancient Life was reviewed for the limited identification claim. The linked specimen-photo download returned HTTP 403 from the network proxy: **no official photo pixels were viewed**. The recorded access result is in [source-access.json](../../assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r002/source-access.json). Keep the model described as an Aturia-inspired fossil shell prop; do not claim exact specimen anatomy, color, locality, age, or specimen dimensions. [Digital Atlas of Ancient Life](https://www.digitalatlasofancientlife.org/learn/mollusca/cephalopoda/nautiloidea/)

Other consulted sources support only the stated narrow scope: the HKU museum catalogue names Phoenicopsis, the National Park Service describes small knobby calcite cave growths, and the Kansas Geological Survey describes Curvolithus's trilobed surface and positive relief. No source photos or other third-party media were included in the assets. [HKU Stephen Hui Geological Museum](https://shmuseum.hku.hk/education/earth-evolution/mesozoic/dinosaur-world/plants-in-the-dinosaur-world), [National Park Service](https://www.nps.gov/wica/learn/nature/cave-formations-speleothems.htm), [Kansas Geological Survey](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno.html)

## Technical and runtime checks

- All four exact GLBs pass the repository static audit and Khronos glTF Validator 2.0.0-dev.3.10 with zero errors and zero warnings. All are within the per-brief caps: 14,000 triangles, 6 materials, 30 estimated scene primitives, and 1,000,000 GLB bytes. All have no textures and use no glTF extensions.
- Blender 4.3.2 reopened each pinned `.blend`, imported its exact pinned GLB into a clean scene, and matched triangle counts: Aturia 12,160; Phoenicopsis 1,394; Cave popcorn 7,398; Curvolithus 2,790. Source-export checks pass for the first three. Curvolithus reports a smooth-face intentional-style warning; I reviewed the clay and profile views and accept it as deliberate, with no repair needed.
- Three.js 0.180.0 `GLTFLoader` parsed and rendered all four exact GLBs in Chromium 154 with WebGL2. The renderer was ANGLE/SwiftShader software (`SwiftShader Device (Subzero)`), not physical GPU hardware. The four-asset 2×2 scene loaded four instances at authored scales (translation only), totaling 23,742 asset triangles, with no reported GL errors, lost contexts, page errors, or failed resources. **This proves software WebGL parsing and scene functionality only; physical GPU compatibility and target-device performance remain unknown.**
- The candidate record validators reported structurally valid records. Formal approval remains pending; this review did not modify candidate records or mark an asset approved.

Replay outputs, including fresh static/Khronos reports, source checks, Blender imports, concept-evidence validations, runtime report, and screenshots, are in [the replay directory](replay-20261020T003048Z/). The concept evidence validators return `valid:true`, but `evidence_complete:false` for every item only because the exact ImageGen provider generation timestamp is unknown. The `--require-complete` checks therefore exit 1 for that disclosed blocker. No timestamp was inferred from file dates or fabricated.

## Nominal scale and measured bounds

Dimensions below are in meters and are kept separate. Blender dimensions are XYZ with Z up; glTF bounds are XYZ with Y up. Nominal values are artistic targets, never specimen measurements.

| Asset | Nominal Blender XYZ | Measured Blender XYZ | Measured GLB XYZ | Triangles | Materials / primitives | GLB bytes |
|---|---:|---:|---:|---:|---:|---:|
| Aturia r002 | `[0.24, 0.105, 0.22]` | `[0.23999648, 0.10205488, 0.22]` | `[0.23999648, 0.22, 0.10205488]` | 12,160 | 3 / 3 | 662,876 |
| Phoenicopsis r001 | `[0.32, 0.12, 0.26]` | `[0.32, 0.12, 0.26]` | `[0.32, 0.26, 0.12]` | 1,394 | 5 / 19 | 87,960 |
| Cave popcorn r003 | `[0.55, 0.40, 0.26]` | `[0.55, 0.40, 0.26]` | `[0.55, 0.26, 0.40]` | 7,398 | 3 / 3 | 578,792 |
| Curvolithus r001 | `[0.24, 0.32, 0.047]` | `[0.24, 0.32, 0.047]` | `[0.24, 0.047, 0.32]` | 2,790 | 3 / 3 | 71,848 |

Phoenicopsis's 19 estimated primitives are below the 30 limit. They are separate leaf and shoot meshes, consistent with the stylized foliage construction.

## Candidate disposition

Keep all candidate approval records pending. The repair request is limited to Aturia's radial patch; after that correction, rerender and review the same eight views. No general polish pass is recommended. The hardware GPU remains untested, and exact provider generation times remain unknown; neither is silently treated as passed. Concept-image inspection and candidate approval are separate decisions.

## Replay

From the repository root, install the locked JavaScript dependencies if needed (`npm ci --ignore-scripts`), then run:

```bash
bash qa/batch52-independent-20261020/replay.sh
```

The script verifies the frozen handoff and GLB pins, writes a fresh timestamped evidence directory, runs the static/Khronos/WebGL checks, and reopens the Blender sources and imports the GLBs. It does not write to model files, `main`, or release paths.
