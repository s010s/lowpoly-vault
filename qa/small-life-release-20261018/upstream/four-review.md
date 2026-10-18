# Independent small-life candidate review

Date: 2026-10-18 UTC. Reviewer: review_small_scene_candidates (separate from makers).
Repository: s010s/lowpoly-vault. Scope: static artistic environment props for a child-oriented imaginative prehistoric world. This is a pragmatic visual/export review, not a scientific reconstruction certification, runtime release approval, or merge approval.

## Result

All four candidates PASS the inspected visual/basic-form scope with minor ADVISORIES. No blocking visual defect was found. No geometry repair or cosmetic revision is requested. Required untested runtime gates remain UNKNOWN, not passed.

## Exact subjects and per-asset decisions

### Juracimbrophlebia r1, rebuilt 2026-10-18
- GLB SHA-256: `b6fa8ebf0995614401b27cafea2e5095f6f48bbdcb69fd99957cacd60272fa94`
- Independently measured: 117,624 bytes; 2,128 triangles; 5 primitives; 4 materials.
- Visual: PASS WITH ADVISORY. Four leaflike wings, segmented narrow body, head and six main legs are legible in top/hero views. No conspicuous major penetration, missing major body region, or accidental extra limb is visible.
- Advisory: front/right edge-on views naturally flatten the wings; thin legs and antennae become faint at the smallest illustrated size. Favor a slightly elevated viewing angle and contrasting surroundings. No model change required.
- Technical: independent static GLB audit PASS WITH WARNING; negative lowest Y is consistent with documented suspended body-center pivot, not a ground-mount defect. Stored Khronos report records zero errors/warnings. Three.js loader and actual GPU/scene tests remain untested here.

### Asteroxylon r2, rebuilt 2026-10-18
- GLB SHA-256: `028eca80ede2eb4fc95f87c17465aee8dd3284c43d3d5633cb8343db91abcc8e`
- Independently measured: 425,752 bytes; 5,744 triangles; 5 primitives; 4 materials.
- Visual: PASS WITH ADVISORY. Upright branching green shoots, short repeated leaflike projections, a connecting horizontal axis and descending roots form a coherent plant silhouette. No gross break, unusable faceting or major unintended penetration is visible.
- Advisory: exposed roots are useful in the diagnostic views but can look suspended in a scene. Set the soil level deliberately, rather than assuming the lowest root-tip origin is the intended soil surface. Fine botanical distinctions are outside this artistic review.
- Technical: independent static GLB audit PASS. Stored Khronos report records zero errors/warnings. Three.js loader and actual GPU/scene tests remain untested here.

### Bothriolepis r001
- GLB SHA-256: `311da456d83b2bb722f654769ce4a937393d7f771e5ae71185eb7db473a14f98`
- Independently measured: 46,000 bytes; 736 triangles; 8 primitives; 4 materials.
- Visual: PASS WITH ADVISORY. Broad armored-looking front, paired lateral appendages, tapering fish body and tail read clearly even in the supplied 80-pixel example. No obvious impossible major attachment or large accidental intersection is visible.
- Advisory: restrained palette and tucked appendages simplify taxon-specific detail. Keep the artistic/inspired-by labeling; no scientific precision or shape repair is required.
- Technical: independent static GLB audit PASS WITH WARNING; negative Y matches suspended body-center mounting. Stored Khronos report records zero errors/warnings. Stored Three.js 0.180.0 Node GLTFLoader report passes for this hash; this review did not rerun that loader or a GPU renderer.

### Waptia r001
- GLB SHA-256: `300e2ef721c7822cc717f808941bc19cb2ff00b8ef4b147a0c634e6b6683033b`
- Independently measured: 85,668 bytes; 1,452 triangles; 7 primitives; 4 materials.
- Visual: PASS WITH ADVISORY. Paired shell, stalked eyes, antennae, articulated abdomen, repeated appendages and paired terminal lobes give a recognizable small shrimp-like animal. The shell's dorsal division is consistent across views, not evidence of a broken export.
- Advisory: the dark shell division and fine antennae are conspicuous at close viewing and reduced at small scale; acceptable stylization. No repair requested.
- Technical: independent static GLB audit PASS WITH WARNING; negative Y matches suspended body-center mounting. Stored Khronos report records zero errors/warnings. Stored Three.js 0.180.0 Node GLTFLoader report passes for this hash; this review did not rerun that loader or a GPU renderer.

## Evidence and checks actually performed

- Read the recovered pragmatic acceptance profile at planner commit `58e13487f6e8e2bdea2c7a6ee087e1a8e147275b`.
- Inspected actual pixels of six-view contact sheets (hero/front/right/rear/top/clay) and supported-size examples for all four. Insect/plant scale examples were on the contact sheets; aquatic scale sheets show 80/160/240/360 pixels.
- Insect/plant evidence was read from the maker's local recovered package: `qa/small-fauna-v1/{asset}/recovered-20261018/`. The parent identifies binary checkpoint `9bd81db2c9ccdc46a23b5d5d124b08dfa102e755`; this review binds to the locally recomputed hashes above, not an independently fetched insect/plant remote snapshot.
- Aquatic GLBs, six original frames per asset, manifests and technical records were fetched through the GitHub connector from exact commit `d0735b414baae2edd4a35d0f911bc3afdbe9c624`, branch `production/small-aquatic-pair-20261017`.
- Independently recomputed all four GLB SHA-256 values, ran the repository static GLB audit on each with 12,000-triangle / 4-material / 8-primitive limits, and found zero audit errors. All are below the 2 MiB GLB ceiling.
- Verified all 24 original frame hashes against their manifests; zero mismatches. Each manifest's GLB subject equals the independently computed GLB hash. Six-view evidence is current for these exact files.
- Read the supplied technical records. Their clean source/reimport/rebuild and official validator results are recorded evidence, not newly rerun Blender/Khronos checks by this reviewer. Original insect/plant GLB identities are preserved; regenerated blend files do not claim original blend byte identity.

## Explicitly untested / not approved

Actual browser/WebGL/GPU rendering, target-device performance, repeated-instance scene behavior, scene lighting/background integration, animation/rigging and full scientific anatomy are not established by this review. Actual GPU/runtime: 未测. Aquatic Node parsing is recorded evidence only; insect/plant Node parsing remains unknown. Unknown required gates must stay pending. No asset, source geometry, approval record, branch, merge, museum integration or existing release was modified.

Machine evidence: `independent-integrity.json` and four `*-independent-glb-audit.json` files alongside this report.
