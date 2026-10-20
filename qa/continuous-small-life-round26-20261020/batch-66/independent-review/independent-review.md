# Batch 66 independent QA review

- Source: `c0a2ef787b8744495603fc4f1d3258891421504b` on `candidate/small-life-batch66-concept-20261020`; clean before/after.
- Scope: read-only source inspection and independent static review; no producer modifications, no release or approval.
- Visual evidence: individually opened the genuine original concept images and all 32 final original-resolution 512×512 frames, plus all four contact sheets. Contact-sheet and frame hashes are recorded in `machine-findings.json`. Public-reference pixels were inspected from the named primary sources and were not copied into this QA directory.
- Generation/authoring provenance: two distinct queued successful semantic rebuilds per asset, with IDs, fingerprints, PID, request/result hashes, timestamps, outputs, exact GLB and semantic hashes bound in the machine record. Queue records are process attestations, not cryptographic proof. Exact provider-image generation timestamp and generator authoring start timestamp remain unknown.
- Source integrity: clean producer tree at pinned commit; original inventory hash unchanged between parent/head; original modeling briefs/reference ledger/freezes are preserved. Postbuild candidate brief only adds artifact bindings.
- Static export limits: 14,000 triangles, 1 MB GLB, 6 materials, 30 primitives. All four pass, use zero textures. Independent Blender source reopens, project static audits, Khronos validation and Three.js GLTFLoader parse pass. No GPU/browser render or composed scene was run.
- Technical, visual, factual, specification, runtime_parse, GPU and scene are distinct per-asset stages; see dispositions below. GPU and scene remain blocked/unknown for every asset.

| Asset | GLB SHA-256 | Triangles / bytes / materials / primitives | Static disposition | Stage disposition |
|---|---|---:|---|---|
| louisella | `4632a79722f7caaa3b4df476237b438cc9277ab28f3075f3afdd5e2a488e4b62` | 10272 / 543760 / 6 / 9 | **REVISE** | technical ACCEPT, visual REVISE, factual REVISE, specification REVISE, runtime_parse ACCEPT, gpu BLOCKED (not run; unknown), scene BLOCKED (not run; unknown) |
| hoodoo | `769455c71d8b433913e37e12b961fb06fda15f7a7d0c84eddaa2332b016e2038` | 1244 / 70072 / 4 / 4 | **REVISE** | technical ACCEPT, visual REVISE, factual ACCEPT, specification REVISE, runtime_parse ACCEPT, gpu BLOCKED (not run; unknown), scene BLOCKED (not run; unknown) |
| graben-basin | `27c5dc00cfadcefd096555918a6163cfe6df2c5577721a06c062fab10e413fc6` | 1184 / 68332 / 5 / 13 | **ACCEPT** | technical ACCEPT, visual ACCEPT, factual ACCEPT, specification ACCEPT, runtime_parse ACCEPT, gpu BLOCKED (not run; unknown), scene BLOCKED (not run; unknown) |
| meandering-river-reach | `a1eb45790b033e06f7bfaf7084d361e0701de426413fb1d74d69307f041b2af4` | 3142 / 187652 / 5 / 5 | **ACCEPT** | technical ACCEPT, visual ACCEPT, factual ACCEPT, specification ACCEPT, runtime_parse ACCEPT, gpu BLOCKED (not run; unknown), scene BLOCKED (not run; unknown) |

## Findings

- Louisella: REVISE. Frozen obligation/reference calls for a smooth, blunt-rounded unspined posterior and paired trunk papilla rows. Final retains a conspicuously pointed/tapered posterior; paired rows and zone separations are too weak at 512px. It is not sufficient to distinguish confidently from a generic long annulated worm. Rework posterior silhouette and make paired papilla/zonal cues legible; ringed proboscis is present. Do not treat Miskoia as a separate taxon.
- Hoodoo: REVISE. Refined final keeps a modest cap and irregular radial cross section, but four similarly spaced, full-rim ledges plus aligned bands still read as mechanical tiers. Break spacing/continuity and make pillar layering less repetitive. Original attempt retained.
- Graben basin: ACCEPT static. Model is a down-dropped central block bounded by opposing normal-fault scarps with displaced marker layers, not an eroded valley. No named location/age/measurement is claimed.
- Meandering river reach: ACCEPT static. Connected sinuous reach; point-bar accents are inside bends and cutbank accents outside. Unified closed terrain mesh. No named site/age/measurement claim.

## Stage boundary and decision

Technical and runtime_parse ACCEPT means static geometry/source/format/parser checks passed, not that the user brief or full runtime has been approved. Louisella and Hoodoo remain REVISE for visual/specification (and Louisella factual distinctiveness). Graben and river meet the inspected static brief. GPU and populated-scene stages were not run and remain BLOCKED / UNKNOWN, not passed. Candidate validation itself reports `approved_for_brief:false`; publication/release is outside this QA.

Full quantitative measurements, build/dependency pins, per-view bindings, queue request/result provenance, inspected reference pixel hashes and limitations are in `machine-findings.json`.
