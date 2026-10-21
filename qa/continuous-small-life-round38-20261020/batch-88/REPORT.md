# Batch88 independent QA

Exact commit: `b7c7f1c9ec495ad528568770a789b5d15a2de3a4`
Handoff SHA-256: `2c3f73e4f0fa69e8387bd26ba0563b579bc27f9746821c1b4971bacc9d71551f`

Decision: **2 static candidates PASS; 2 REVISE.** No formal/user/website/release approval. GPU and scene are unrun/blocked for all.

## Required fixes

1. **Baragwanathia r003: REVISE.** All32 final individual views across the batch, including its eight views, were inspected directly. Its512px hero/front/rear/clay/silhouette remain exposed-axis / hairlike rather than convincingly dense bottlebrush. Keep the whole-plant hierarchy and source-led narrow spiral leaf anatomy; improve real foliar volume/readability within the original brief.646 actual leaves is within the original rough500–650 range. The retained650 prose arithmetic error alone is not the failure.

2. **Phycosiphon r002: REVISE specification.** The explicit1.0–1.4mm core-width range cannot be passed using the nominal1.2mm parameter or colored band. Real triangular geometry has low core skirts spreading to2.00mm at bends/2.26mm at a cap using a5µm diagnostic threshold; even a50µm threshold yields1.65mm. Non-cap minimal reproduction: path0/sample10, centerXY(-0.02752910,-0.01671097)m, normal(0.98030448,0.19749208). Actual face453 at+0.9mm is0.894341mm from the entire centerline and retains72.457µm core height. At+1.0mm, it remains59.283µm. See core-overhang-minimal-repro.json and reproduce-core-overhang.py for source vertex IDs, material, coordinates and barycentric decomposition. Constrain actual core/mantle profile triangulation and re-export a new immutable revision. Raised relief/core-mantle recognition and source uncertainty otherwise pass.

## Static candidates passing

- **Chondrites r002:** true fine branched relief, quiet host, no hollow wall/lobes/pellets. KGS Waverly identification stays tentative; supplementary2012 Chondrites species evidence does not replace original period or species scope. Fork unions broaden beyond the approximate ordinary-shaft width, not a new global hardmax violation.
- **Planolites r003:** one gently winding unlined homogeneous fill, real cut-face fill, no second sheath/animal, closed integrated topology. Original full r001 failed-final and r002 topology-failure evidence remain preserved.

## Fresh checks

- Four source files independently reopened and re-exported byte-identically, each under process-scoped flock and Blender threads2. Actual authored/evaluated/exported counts and full bounds measured independently.
- Fresh project audit, candidate schema validation, Khronos zero errors/zero warnings, Three.js0.180.0 parsing all pass.
-58/58 provenance checks pass, including original inventory/freeze, exact final GLB/derived brief/references fixed before rendering, two distinct real queued rebuilds per asset, and364 retained local/consult-only files totaling126,997,013 bytes.
- Directly inspected32 final512px individuals,4 genuine original concepts and11 primary/reference page/image pixel files. No contact-sheet substitution.
- Plant measurements:551+95=646 closed leaf components; all leaf bases inside measured axis envelopes; seven axes linked in the intended hierarchy. Leaf width≈5.000mm, base-tip chord54.36–56.23mm, swept centerline58.62–60.64mm. Original approximate dimensions and global artistic targets are not converted into invented exact maxima.
- Phycosiphon body, bends and caps measured, including full source material envelopes. Material assignment alone is not geometric width. Planolites actual fill envelope is6.000002mm radius; host interpolation residual is not incorrectly labeled fill diameter.

## Seven-stage result

- baragwanathia r003: technical PASS, visual REVISE, factual REVISE, specification REVISE, runtime_parse PASS, gpu BLOCKED, scene BLOCKED.
- chondrites-branching-trace r002: technical PASS, visual PASS, factual PASS, specification PASS, runtime_parse PASS, gpu BLOCKED, scene BLOCKED.
- phycosiphon-looping-trace r002: technical PASS, visual PASS, factual PASS, specification REVISE, runtime_parse PASS, gpu BLOCKED, scene BLOCKED.
- planolites-smooth-burrow r003: technical PASS, visual PASS, factual PASS, specification PASS, runtime_parse PASS, gpu BLOCKED, scene BLOCKED.

Full criterion-level decisions, numeric evidence and limitations are in report.json. Source/model/previous QA remained read-only. No publication action was taken.
