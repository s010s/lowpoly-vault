# Independent differential QA: caldera r003

**Disposition: ACCEPT BOUNDED** for this exact candidate on technical, visual, factual, specification, and CPU parser criteria. This is not GPU/scene qualification, candidate approval, user approval, or publication authority. No source records or approval flags were changed.

## Exact subject and scope

Source `/tmp/lowpoly-batch63-20261020`, branch `candidate/small-life-batch63-concept-20261020`, clean HEAD `108c548ae7b237150c6ac8b5f8a9996fedc618b3`. Reviewed `assets/candidates/continuous-small-life-round24-20261020/batch-63/caldera/r003/model.glb`, SHA256 `ca635b44f8007bea8b2b29e83e330663b34acce95a8d3914df69b2a083e2bc95`, bound to the original brief `6dfe4d60921917f33caf94454a3572abfc0cc1624333d9ad26478f906090f504`, candidate brief `c1781bb5bafb01c3b0d65eaef44f35ab439ef58d27af6b5a2a31c1671c83f8f5`, and references `2f9689b429ed45683b3b06a6eb6181b6ff69db80254a0fe2c7cfe2b0714cd25b`.

The exact post-r003 selection remains Siphusauctum r001, Esker r001, Caldera r003, Dogtooth-spar-cavity r002. The three previously accepted assets were not fully re-reviewed: their exact GLB hashes still match the original independent report and pre/post-repair records, and their candidate trees plus Caldera r001/r002 show no diff from the baseline QA commit. Their earlier ACCEPT BOUNDED verdicts carry forward.

## Visual and obligation review

I inspected the original concept pixels and all eight actual final 512×512 subject-bound GLB views (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`). The model reads as a broad, low collapse basin with a depressed broad floor, steep inward scarps, gentler outer slopes, and an uneven remnant rim. The top and front/reverse-oblique views now show one recognizable shallow southern saddle interrupting the rim, with restrained adjacent irregular bays. It is sufficiently legible for the frozen **one subdued breach** requirement without a dramatic opening or starburst; the floor and overall landform remain intact. This resolves the specific r001 visual/specification defect without relaxing the original claim.

An independent position comparison of r001 and r003 finds the same 649 unique XZ locations and footprint. Only heights changed: 123 positions on outer radial rings (0.60–1.00); the central/floor rings stay unchanged. The deepest difference is about 112.8 m, localized around the saddle/bays. This supports the claim that the revision is targeted rather than a mislabeled old render or scope rewrite.

Original inventory still describes a large collapse basin with steep arcuate rim and broken inner walls. Frozen feature obligations remain unchanged: broad low subsided basin; uneven enclosing remnant rim with inward scarps and gentler outward slopes; wide depressed floor above a closed underside plus one subdued breach; and no lava, meteor-impact rays, eruption spectacle, named site, or age claim. All are visible or verified in r003. The underside is closed and manifold.

## Factual boundary and primary reference

The consulted primary page is NPS, “Older Caldera Complexes” (last updated April 17, 2023), <https://home.nps.gov/articles/000/older-caldera-complexes.htm>. Its text supports caldera formation by collapse/subsidence following partial drainage of shallow magma reservoirs and notes later erosion/tectonism can obscure older structures. The actual locally consulted NPS Montezuma landscape photo was inspected at `/tmp/lowpoly-round24-primary-consulted/batch63/caldera.jpg`; its hash matches the reference ledger (`521addd6146d20e9eee40e7a1ca3a5006b07ea0d8c586830e48f5053325b5508`). It shows an open mountainous landscape, not a complete surveyed ring or a breach template. Therefore factual acceptance is bounded to a generic educational caldera/process analogue; detailed rim, breach shape, color and scale remain illustrative, not a site-specific or measured reconstruction. The brief claims no named caldera, age, or measured proportions.

## Technical, source, and runtime checks

- Independently ran project `validate_candidate.py` with `static-stylized-v1` and the exact profile contract: **valid**, with no errors, but **not approved** and with acceptance gates still unknown/pending. Independently ran `validate_concept_evidence.py`: **valid, evidence incomplete** because `concept_generated_at` and `modeling_started_at` are null. Do not infer either from filesystem mtimes.
- Independently ran project static GLB QA on a separate exact copy: pass, 1,294 triangles, 102,176 bytes, four materials/primitives, zero textures; below all frozen geometry/file/texture budgets.
- Khronos validator on the separate exact copy: 0 errors, 0 warnings. Three.js `GLTFLoader.parseAsync` r180 independently parsed the exact hash: pass, 1,294 triangles, four mesh/primitive groups, expected bounds. This is a CPU parse, not hardware-render evidence.
- Reopened the exact `.blend` read-only in Blender 4.3.2 with auto-execution disabled, under the required blocking Blender lock and two threads. Source hash matched `dcc5152cad2ae5a0abbf28c28a54c655784daaf38ccee68fb4cea804ee7fee03`. Authored/evaluated counts reconcile at 649 vertices, 1,225 polygons, 1,294 triangle-equivalent. Per-mesh welded checks found zero boundary/nonmanifold/wire edges or degenerate triangulated faces. Source/export bounds agree within 0.0001 m; nominal `[4000, 3400, 550]` m is illustrative, while measured Blender bounds are `[4075.9819, 3474.0986, 527.9156]` m and GLB-axis bounds `[4075.9818, 527.9156, 3474.0985]` m.
- Independent exact-GLB topology audit found zero boundary/nonmanifold edges, degenerate or duplicate triangles after positional welding. Material partition duplicates 3,744 exported POSITION-stream vertices across 649 source vertices; that is reconciled and expected.

## Freeze, provenance, renders, and rebuilds

The original concept request/completion-observed/inspection boundaries were 2026-10-20 12:57:32.283Z, 12:58:03.154Z (upper bound), and 12:59:21.100Z; the original design freeze was 13:01:08.792067Z. The ImageGen provider did not return its exact generation timestamp or model seed. Exact modeling-start time was not sampled. These limitations remain explicit; evidence is valid but not complete.

For r003, the unchanged original freeze is hash-linked, and the localized repair delta froze at 13:47:13.713876Z before the lifecycle-recorded build start at 13:48:13.718080Z. Original scope, full original brief, refs, and concept are hash-identical to r001/r002. The candidate brief changes only packaging metadata: it fills the required-deliverables list and adds an adapter note; every other original brief field/content is identical. The r003 local procedural seed is 6302; generator, build configuration, source, Blender 4.3.2, Three.js 0.180.0, and glTF Blender I/O 4.3.47 are pinned; no external build assets or dependencies changed.

The final CPU render runner imports the exact GLB, and the manifest binds the exact r003 GLB, candidate brief and reference hashes, its configuration, runner hash and render time (2026-10-20 13:48:51.933677Z). All eight frame hashes/dimensions match. The manifest is a real post-build render, not a relabeling of an earlier candidate. Cycles CPU output does not prove GPU rendering.

Two successful, separate build-lane queue runs are independently checked against request/result hashes, identities, runner/dependency hashes, PIDs and distinct output directories. Run 1 PID 124 completed 13:49:04.215488Z; run 2 PID 149 completed 13:49:09.416252Z. Each rebuilt GLB hash is exactly `ca635b44…e2bc95`; each independently recomputed semantic digest is `0fd41c00cb7ec4fdccabe3225c9f8a8dc9b26eefefb04eadd45477cb9c484680`. They were not cache reuse. Queue records remain auditable attestations, not cryptographic proof of process execution.

## Separate acceptance states

- Technical: PASS.
- Visual: ACCEPT BOUNDED.
- Factual: ACCEPT BOUNDED, generic analogue only; detailed rim/breach remain illustrative.
- Specification: ACCEPT BOUNDED against unchanged obligations and budgets.
- Runtime parse: PASS (Node Three.js CPU parser only).
- GPU rendering: NOT RUN.
- Populated-scene rendering/performance: NOT RUN.
- Formal candidate and user approval: PENDING; no approval status changed.
- Publication: not authorized/performed here.

Machine-readable independent checks and per-asset dispositions are in `machine-summary.json`; rerunnable read-only audit is `audit_caldera_r003.py`. No output contains the copyrighted primary-reference image.
