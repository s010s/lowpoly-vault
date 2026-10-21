# Independent differential QA: banded-gneiss-outcrop r005

Decision: **ACCEPT_STATIC_QA_ONLY** for GLB SHA-256 `c86d8b9ef0bda9b0cbd0bc9820fc7f11d561b619608e8a7e3dc676adf6524fad` at producer commit `843e9b80d4aca535c5fe27ebc4c2e264fa9d77b3`. This is a narrow static QA result, not release or publication approval.

## What changed and why it passes

The original r003 defect was repeated high-contrast sawtooth material steps across the cap in hero, reverse-hero, and top. In the exact r005 pixels those repeated teeth are absent; broad pale/dark bands follow coherent contours across the cap and remain connected to the folded sides. The palette, camera, renderer, overall fold, and original scope are retained. Clay shows physical folded ribs and coarse facets. Broad banding remains distinctly coarser than BIF lamination; no crosscutting vein or named-location claim is implied.

I personally inspected all eight exact 512×512 final frames, their lossless contact sheet, the r003 comparison views, retained r004 diagnostic views, the original concept pixels, and the actual consult-only reference pixels. No unrelated remake or material/camera/renderer masking was needed.

## Independent checks

- Final GLB: `c86d8b9ef0bda9b0cbd0bc9820fc7f11d561b619608e8a7e3dc676adf6524fad`; 3,702 triangles, 4 materials, 4 primitives, 0 textures, 283,244 bytes. All within the frozen budgets.
- Reopened the saved Blender 4.3.2 source and re-exported the complete `EXPORT` collection; the GLB is byte-identical to the candidate. Authored/evaluated source: 1,853/1,853 vertices and 3,502/3,502 polygons; exported POSITION stream: 10,704 vertices.
- Fresh Three.js 180 parse and Khronos 2.0.0-dev.3.10 validation: 0 errors, 0 warnings. Measured Blender XYZ bounds: [3.4980521202087402, 1.6197673082351685, 2.3452324867248535] m; GLB Y-up XYZ: [3.4980520009994507, 2.3452324867248535, 1.6197673082351685] m. The nominal [3.4, 1.6, 2.2] m target is illustrative, not a measured natural specimen.
- Fresh source-BVH check: closed manifold, no nonadjacent self-intersection pairs, no boundary/nonmanifold edges. This is corroborative only, not a universal zero-overlap rule.
- Verified the 160-entry r004/r005 evidence manifest against local bytes, SHA-256, and committed Git blobs; two distinct semantic rebuilds each actually executed with separate run IDs, PIDs, fingerprints, requests/results, logs, and outputs matching the final GLB.
- The r003 report remains unchanged; r004’s diagnostic and its 15 rim T-junction failure are preserved. The fixed Parvancorina r001, glacial-horn r002, and eruptive-fissure r003 remain unchanged from the archive baseline.

## Stage status and limits

Technical, visual, factual, specification, and runtime_parse: **PASS**. GPU and composed-scene stages: **NOT RUN**. Provider-internal ImageGen timing/full authoring duration remain unknown; no filesystem timestamps were substituted. `evidence_complete=false` and `approved_for_brief=false` remain in force. No formal, user, website, publication, or release approval is asserted.

Raw evidence manifest: `/workspace/shared/lowpoly-round30-qa75/diff-gneiss-r005/raw-manifest.json`.
