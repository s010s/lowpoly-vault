# Batch 54 independent QA report

- Candidate: `candidate/small-life-batch54-concept-20261020` @ `54d5380ec3c63ae3e9ab4f36cb377db65ab16c75`.
- Reviewer: GPT-6 Luna xhigh; review date 2026-10-20 UTC.
- Subjects: Didymoceras r003; Spirematospermum r003; Cave-shield r002; Psammichnites-ribbon-trace r002.
- Complete file/frame hash bindings and test evidence are in [`report-data.json`](report-data.json); copied evidence is under [`evidence/`](evidence/).

## Stage conclusions

| Stage | Result |
|---|---|
| Technical validity | **PASS (all four exact source/GLB pairs)** — Pinned artifact hashes match handoff/candidate records. Source export/reopen checks and exact GLB round-trips have no errors; all pass independent Khronos validation with 0 errors and 0 warnings; static-stylized-v1 candidate check is valid. All geometry, materials, primitives, GLB-byte and zero-texture budgets pass. |
| Visual | **PASS for the reviewed eight fixed views and inspected actual GLB round-trip previews** — All four frozen eight-view sheets and selected full resolution views were independently viewed. No critical visual defect; individual observations are below. |
| Factual | **PASS for the bounded stylized claims in the frozen briefs** — Consulted the cited institutional/primary sources; source grounding and reconstruction limits are documented in report.md. |
| Specification | **PASS for frozen artifact/view/size/budget constraints** — All four eight-view packages present and manifest hashes verified; measures fit hard ceilings; nominal sizes are treated as artistic envelopes, not natural measurements. |
| Runtime parse | **PASS** — Actual candidate GLB files loaded through Three.js 0.180.0 GLTFLoader in Chromium 154; zero console and GL errors. |
| Software WebGL | **PASS** — WebGL2 on SwiftShader software renderer; actual models rendered individually and in the retained true-scale common-ground composition. |
| Physical GPU | **UNKNOWN / NOT TESTED** — No physical GPU device was exposed (/dev/dri absent, nvidia-smi unavailable); software SwiftShader is not physical GPU evidence. |
| Intended scene | **UNKNOWN / PARTIAL** — A documented software-WebGL composed-layout smoke test is retained. The handoff and scope contain no authored target scene definition, so it cannot substantiate intended production-scene fit/contact acceptance. |
| Evidence completeness | **INCOMPLETE** — The concept checker reports valid=true and evidence_complete=false solely because the exact ImageGen provider generation timestamp is unknown. The report binds the actual concept image, prompt, generation record and artifact hashes; the timestamp is not inferred. The dispatch-scope placeholder is noted separately; this review follows the explicit user-pinned source commit and exact GLB hashes. |
| Formal approval | **NO — candidate remains pending; no publication approval** — Required physical-GPU and intended-scene criteria remain unverified; concept evidence completeness remains incomplete. Each candidate record remains approved_for_brief=false/pending. This review report does not change those records. |

## Asset findings and frozen hashes

### didymoceras r003

- Visual: Continuous descending loose helix with two separated whorls, broad terminal hook and recessed aperture read consistently across hero/reverse/front/side/rear/top/clay/silhouette. No critical twist/seam or silhouette defect observed.
- Factual: Digital Atlas of Ancient Life supports Didymoceras heteromorph basic-form context; the artifact makes no species, locality, specimen-copy or soft-body claim. Continuous 3D path is a bounded stylized reconstruction.
- Specification: 0.230×0.170×0.300 m nominal Blender XYZ design envelope; 8,180 tris, 1 material, 1 primitive, 442,360 bytes, 0 textures; fits all hard ceilings.
- Budget/scale: 8,180 triangles; 1 material; 1 primitive; 442,360 bytes; 0 textures; nominal Blender XYZ [0.23, 0.17, 0.3] m. Measured Blender bounds size `[0.22999998927116394, 0.17000000178813934, 0.29999998211860657]` m; glTF XYZ bounds size `[0.22999999672174454, 0.29999998514540493, 0.17000000178813934]` m.
- GLB SHA-256: `32526e504c03f9a7ababc367cb4291d7a3286d811d270ca7c90e8e3068272d8d`
- Blender source SHA-256: `4a45666f0d20cab05873179c5c2e7de9fc92ded2e528b1458d0f1165b8cfec28`
- Generator SHA-256: `4a4e93cd8749e7875a3b27ae67ebd66b459a69dad794a5149c77c9b63e75e059`
- Candidate record SHA-256: `f98075de91c43bfd072380ae5aa3174bdee0a090072e4a04d9d4175823cbc89d`; delivery-freeze SHA-256: `3e5635ff0ba8df22210c05e22077b85e4b2a763565dcbe1b3978fab1541ada36`
- Eight-view sheet SHA-256: `b46c7d8f9ecec8b1dde999c1620464390685033bc2d2ce03089b48a1654b0c8e`; render-manifest SHA-256: `cbac8a2102d2ec7c544b7d2ae90eb0844265e4150ef96a609a5b0284794cfc5b`. All eight frame file hashes are listed and verified in `report-data.json`.
- Blender source reopen/export and actual GLB round-trip: no errors. Khronos validation: PASS, 0 errors, 0 warnings. Blender round-trip warnings about smooth/boundary edges were reviewed; no cracks or missing geometry appeared in the inspected previews.

### spirematospermum r003

- Visual: One capsule with three separate embedded seeds; longitudinal grooves/striations are visible on top/clay at full sheet scale but subtle in the small hero. Shape and embedded seeds remain readable; no critical defect.
- Factual: Li et al. (2018) describe elongated capsules, curved basal stalk, longitudinal ribs/striations and seeds. Three seeds are explicitly a simplified visual interpretation; no disputed family affinity or plant-wide claim is made.
- Specification: 0.018×0.062×0.016 m nominal Blender XYZ; 10,936 tris, 3 materials, 5 primitives, 577,504 bytes, 0 textures; fits all hard ceilings.
- Budget/scale: 10,936 triangles; 3 materials; 5 primitives; 577,504 bytes; 0 textures; nominal Blender XYZ [0.018, 0.062, 0.016] m. Measured Blender bounds size `[0.017999999225139618, 0.06199999898672104, 0.01600000075995922]` m; glTF XYZ bounds size `[0.018000000156462193, 0.01600000033795368, 0.06199999898672104]` m.
- GLB SHA-256: `816fac9a751596664f39da97257acdc70a60efe39e83042b31e8d84d72f648f1`
- Blender source SHA-256: `ef1300be85201b1b2cf62a1bf9d267d74bbcedd97d8dc351ddfd2104dffd14ee`
- Generator SHA-256: `4a4e93cd8749e7875a3b27ae67ebd66b459a69dad794a5149c77c9b63e75e059`
- Candidate record SHA-256: `4812625e458d703af8f9a6cd23cbc9bd31b45ea79183305710798b3392a49655`; delivery-freeze SHA-256: `5648d2ce3194cb9303a40e2d57f6c594a2afd951b68094eef7de6a2629ca6a9f`
- Eight-view sheet SHA-256: `ed850c337a6d727a69b77484cc0265260015746669eef926898333dfca6d7bdc`; render-manifest SHA-256: `35451e430898a84a883f857b0506fba474cdbe7676840289efc2e69be011e537`. All eight frame file hashes are listed and verified in `report-data.json`.
- Blender source reopen/export and actual GLB round-trip: no errors. Khronos validation: PASS, 0 errors, 0 warnings. Blender round-trip warnings about smooth/boundary edges were reviewed; no cracks or missing geometry appeared in the inspected previews.

### cave-shield r002

- Visual: Two distinct thick, near-parallel plates attached to the wall block; the medial gap/crack remains visible in side/top/clay views. Facets are quiet and do not hide the plate construction.
- Factual: NPS cave geology reference supports round/oval near-parallel shield plates with medial crack across cave surfaces. Model is generic; no cave locality, age, specimen or natural measurement is asserted.
- Specification: 1.000×0.840×0.670 m nominal Blender XYZ; 2,372 tris, 2 materials, 3 primitives, 119,696 bytes, 0 textures; fits all hard ceilings.
- Budget/scale: 2,372 triangles; 2 materials; 3 primitives; 119,696 bytes; 0 textures; nominal Blender XYZ [1.0, 0.84, 0.67] m. Measured Blender bounds size `[1.0, 0.8400000333786011, 0.6699999570846558]` m; glTF XYZ bounds size `[0.9999999701976776, 0.669999971985817, 0.8400000035762787]` m.
- GLB SHA-256: `4c772ba8705c9921836accd4607f15dae75f34ad9bdf67d8ef9970bbea961028`
- Blender source SHA-256: `2a19392c990e37c1f77002e0addfa2f1805ce6ef71997cdac440d1852afcc88c`
- Generator SHA-256: `a5ec704a7d7b7711d1fa575edaf4e2a8d2e4c7381583cc7e1f46b59a1e01ab21`
- Candidate record SHA-256: `f8327e28883fd1de199f2ba1760fd95e5a5c27b458bc9546c04d4f20742a1793`; delivery-freeze SHA-256: `961e35f008c5585a3d897b607d9aedbe882fb9fd2e815eb73559099662afb528`
- Eight-view sheet SHA-256: `16e3e368a362e0cb0591251c86ff250ff221dc861e481576acb7f67012936ca1`; render-manifest SHA-256: `eea11d3cc7077c417232e407b328b29a11d9f00fd0825e7924b470cd72828bd7`. All eight frame file hashes are listed and verified in `report-data.json`.
- Blender source reopen/export and actual GLB round-trip: no errors. Khronos validation: PASS, 0 errors, 0 warnings. Blender round-trip warnings about smooth/boundary edges were reviewed; no cracks or missing geometry appeared in the inspected previews.

### psammichnites-ribbon-trace r002

- Visual: One raised S ribbon on slab; central ridge and transverse/arcuate divisions are visible in top/clay and silhouette. Median ridge is quieter than concept art but recognizable and consistent with frozen brief.
- Factual: Kansas Geological Survey description/figure supports horizontal trace, median dorsal structure and transverse/arcuate ridges. Raised relief is a display convention; no producer/behavior certainty or coexistence claim is made.
- Specification: 0.280×0.380×0.045 m nominal Blender XYZ; 6,988 tris, 2 materials, 2 primitives, 273,184 bytes, 0 textures; fits all hard ceilings.
- Budget/scale: 6,988 triangles; 2 materials; 2 primitives; 273,184 bytes; 0 textures; nominal Blender XYZ [0.28, 0.38, 0.045] m. Measured Blender bounds size `[0.2800000011920929, 0.3799999952316284, 0.04500000178813934]` m; glTF XYZ bounds size `[0.2800000011920929, 0.04500000178813934, 0.3799999952316284]` m.
- GLB SHA-256: `d6e23b814e3aa68fa1f47cf23755e3fd15d895748fe4720ba5a49b7a6744ec87`
- Blender source SHA-256: `cdc84db78f44065fb6ec02828d2bc4ff629b7f189eacd82647a4e34d41d42caa`
- Generator SHA-256: `a5ec704a7d7b7711d1fa575edaf4e2a8d2e4c7381583cc7e1f46b59a1e01ab21`
- Candidate record SHA-256: `f50307bf859549bc6eb20e4fad0d44996892aeea25e2c579ea8e76daa83a02c1`; delivery-freeze SHA-256: `cb957473df30e2803706ce0d1e0344c1f1226006a13dc195fe958105f8dcece7`
- Eight-view sheet SHA-256: `b7a53f878d20a25a49e6dc5a8a92905c0a921b51767afa47da4e141ff6df38b4`; render-manifest SHA-256: `ea4cafcc5f47d3e80f10ae514846cbd89404078c560656b273edbdcf42ae928b`. All eight frame file hashes are listed and verified in `report-data.json`.
- Blender source reopen/export and actual GLB round-trip: no errors. Khronos validation: PASS, 0 errors, 0 warnings. Blender round-trip warnings about smooth/boundary edges were reviewed; no cracks or missing geometry appeared in the inspected previews.

All budget limits pass: 14,000 triangles; 6 materials; 30 primitives; 1,000,000 GLB bytes; zero textures. Blender XYZ to glTF XYZ maps X,Z,-Y. Nominal dimensions are artistic design envelopes, not natural specimen measurements.

## Concept provenance

- Concept provider: ImageGen; exact `concept_generated_at`: **unknown**. Receipt observed at `2026-10-20T00:29:14Z`; inspection separately recorded at `2026-10-20T00:29:26.916218+00:00`. No time was reconstructed from filesystem/image metadata.
- Concept image SHA-256: `bb7fb4d66a28075770d03ffbc55d145542d35d683ab5efde2d985a2d8fc8db46`; prompt SHA-256: `0bc4d5c78c714ae18aeb2d9c8506ff836fec41ac419e944d5683f2b7a42a54cc`; generation-record SHA-256: `e1d91fae6c27b70c3bfd147dd26bbf813b1401b22b026e18db0f10bb396023e6`. The checker is `valid=true`, `evidence_complete=false`, blocked solely by the unknown provider timestamp.

## Browser and scene evidence

The exact GLBs loaded via Three.js 0.180.0 GLTFLoader in Chromium 154 and rendered with WebGL2. Each asset had zero GL errors; the browser reported zero console errors. Renderer: `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)`. This is SwiftShader software rendering, not physical GPU evidence.
The retained common-ground composition contains four exact model instances at their authored scale, with a temporary 90-degree Y presentation rotation for Spirematospermum to show its long axis, and renders 28,478 triangles including ground in 12 draw calls. This presentation rotation changes no candidate file or scale. Screenshot SHA-256: `9980533feb93cb8f4fafbaa7d662811d5f9969a6593981ec248f1856113243b2`. This composed-layout smoke test passed. The handoff and QA scope do not define an intended production scene, so intended scene/contact acceptance remains UNKNOWN.

## Scope, evidence status, and next steps

The exact subject is the source commit and four GLB hashes provided in the user instruction. The in-tree dispatch scope remains an unmodified placeholder with null source/GLB pins and `ready_for_qa=false`; this report independently verifies the provided bindings and records that state.
Technical validity passes. Evidence completeness remains **incomplete** solely because the exact ImageGen provider timestamp is unknown. Formal approval is **NO**; candidate records remain pending and `approved_for_brief=false`. No model repair is required from the inspected evidence.

To reach formal approval, the remaining work is:

- Obtain the original provider timestamp if the receipt contains it, otherwise preserve the unknown status.
- Run the required target graphics runtime on a physical GPU and capture device/work evidence.
- Identify the intended composed scene and run exact-GLB scene fit/contact/material/scene-work acceptance.

## Commit identity

The report commit uses the verified GitHub profile `s010s` with no-reply address `8357465+s010s@users.noreply.github.com`; identity record SHA-256: `360ab44efaa4e538d3dd0132ad1fc4c502ee755b3b73d9bfcc28a5b2ea865e11`.

## Factual sources consulted

- [Digital Atlas of Ancient Life, “Ammonoidea”](https://www.digitalatlasofancientlife.org/learn/mollusca/cephalopoda/ammonoidea/)
- [Li et al. (2018), “Spirematospermum wetzleri ...”](https://link.springer.com/article/10.1186/s42501-018-0007-1)
- [U.S. National Park Service, “Cave Geology in Depth”](https://www.nps.gov/grba/planyourvisit/cave-geology-in-depth.htm)
- [Kansas Geological Survey, Bulletin 245, “Ichnofossils”](https://www.kgs.ku.edu/Publications/Bulletins/245/04_ichno2.html)

Sources were consulted for factual descriptions only. No third-party media/assets are incorporated.

## Change boundary

This branch contains only the independent report and reproducibility evidence. Candidate assets, main, formal catalog, and site were not edited. No PR was created.
