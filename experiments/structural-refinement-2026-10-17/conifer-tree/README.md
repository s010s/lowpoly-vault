# Conifer structural refinement, 2026-10-17

Original asset ID: `conifer-tree`. Original `assets/prehistoric/plants/conifer-tree/**` is immutable and byte-checked in `original-integrity.json` and `candidate-r3/original-integrity-check.json`.

## Current frozen candidate

`candidate-r3/` contains the editable Blender source, standalone GLB, deterministic generator and config, frozen brief and reference ledger, machine-readable candidate record, exact-GLB visual evidence and technical reports. Approval is pending fresh independent review and actual browser/GPU/composed-scene evidence. It is not a released replacement.

- GLB SHA-256: `beefce3d0baddcf7fa781d2fa9246746dd2cbfc6d6c635e237094c5b7d970cbb`
- 23,784 exported triangles; 5 materials; 18 primitives; 1,651,140 GLB bytes; no textures
- 26 primary boughs, 211 subordinate branchlets, 3,846 distributed narrow foliage elements
- Actual source/export comparison, project audit, official Khronos validator and independent-process reproducibility pass. Rebuild GLB is byte-identical.
- Pinned Three.js 0.180.0 Node parsing passes. No browser/GPU or composed-scene success is implied.

## Inspect the evidence

Start with `candidate-r3/evidence/original-vs-revised.png`, then open the individual images under `candidate-r3/evidence/revised/`. They include all 24 azimuths at 15-degree intervals, front/rear/both sides/top/bottom, two clay key directions, triangulated wireframe, and middle-crown join detail. `candidate-r3/evidence/original/` provides the same plan for the exact original GLB. Both use the same meter-space framing, camera, lights and color management; there is no per-model scale normalization. Montages are navigation aids; original frames are retained.

The quick full-angle set is 256px/8 samples. Earlier 512px/4-sample preflights are preserved separately. Final high-resolution polish is intentionally waiting on independent structural review. The source blend does not contain the preview stage.

## Attempts and construction

- r1: retained sparse first pass, 22,518 triangles. Maker preflight rejected excessive twig sparsity and the unshortened bare bough. Its original config and generator are in `attempt-inputs/structure-r1/`.
- r2: fuller, still narrow foliage shoots, and a shortened broken branch; source/config preserved in `attempt-inputs/structure-r2/`.
- r3: r2 geometry retained while freezing the valid `study` brief, explicit 2MB byte budget, runtime obligations and executable byte-budget guard. The increase from the preliminary 1.5MB byte estimate accounts for flat-normal vertex splitting; it is not additional geometry. No universal 500KB target is used.

Build and rendering use repository helpers and one worker with two Blender threads, bounded timeouts and isolated append-only queue attempts. Blender 4.3.2 is `/usr/bin/blender`. Everything runs in the current cloud; the user's computer is not used.

## Reproduce and validate

From repository root, choose a fresh empty output directory inside this experiment:

    timeout 180 /usr/bin/blender -b -t 2 --factory-startup --python-exit-code 1 --python experiments/structural-refinement-2026-10-17/conifer-tree/candidate-r3/build_conifer.py -- --output-dir experiments/structural-refinement-2026-10-17/conifer-tree/new-build --config experiments/structural-refinement-2026-10-17/conifer-tree/candidate-r3/build-config.json

The queue manifests retain the actual build and rendering inputs, identity hashes, timings and results. The technical reproducibility report binds the successful independent queue run.

    python3 scripts/validate_candidate.py candidate-r3/candidate.json --root experiments/structural-refinement-2026-10-17/conifer-tree --json

This verifies record integrity, not acceptance. The `--require-approved` variant must remain failing until all required gates are complete and an independent decision is recorded.

## Scope and licenses

This is an original evidence-informed conifer architectural concept. Its approximately seven-meter scale and amplified foliage groups are design choices. Modern botanical analogues are not claims that this is an identified extinct species. Reference images and third-party meshes are not incorporated. Code is MIT; geometry, source, documentation and renders are CC-BY-4.0, Leon Made This / s010s.

## r4 clustered-foliage option

`candidate-r4/` is the later art-direction alternative. It retains the rounded primary woody structure but replaces the fine individual-like spikes with 161 lateral and seven leader compound shoots, each a narrow volumetric body with three forward, staggered lobes. This is explicitly aggregated needle-bearing shoot imagery, not measured individual leaves. Only three palette materials and three primitives are used.

Measured r4 cost: 9,634 triangles; 21,022 exported POSITION-stream vertices; 565,716 raw bytes, 207,498 gzip9 bytes, 165,897 Brotli11 bytes. This is a substantive new foliage design, not a repack of r3. Its 128px silhouette and 512px hero/detail/clay comparisons are in `candidate-r4/evidence/`. Current-artifact technical and parser checks pass, including a byte-identical separate-process rebuild. Full-angle review and independent acceptance remain pending.

The earlier `delivery-study-r1/` also retains the distinct r3 lossless-consolidation and 16-bit-quantization study. Its cost/precision reports and matched pixels do not approve r3's fine-spike art direction. They are preserved as controlled packaging evidence, not substitutes for r4. Gzip/Brotli values are lossless transport/archive sizes, not directly loadable GLB files or measured GPU allocations.
