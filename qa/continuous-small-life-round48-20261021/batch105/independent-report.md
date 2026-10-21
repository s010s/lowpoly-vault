# QA105 independent fullbatch report

Reviewed: 2026-10-21T04:22:23.250091+00:00
Source: `9188a1ef90c7f61762e4bb4877ff9a8b4a5103dd` on `candidate/small-life-batch105-concept-20261021`.

## Result

Three bounded-static passes: **Penniretepora r001, Constellaria r002, Cystodictya r003**.
**Archimedes r001 needs one narrow visual/specification repair.** GPU and composed-scene status remain UNKNOWN for all four. This is not whole-batch release, website, PR or publication approval.

## Exact failure and minimum repair

Archimedes’s original frozen visual-acceptance criterion says: “Keep actual holes and taper incomplete ends; no massive root base.” Both original axial terminations instead have full-radius flat octagonal caps. Actual cap and adjacent-ring radii stay about 0.65 mm; the newly rendered exact-GLB lower/upper details visibly confirm the blunt ends. This is a frozen artistic requirement, not a newly asserted fossil trait.

Repair only the two axial terminal regions in actual geometry while retaining genuine frond attachment and the open helix. No arbitrary taper ratio, percentage or precision target is added. Preserve r001 and make a new revision with affected source/GLB, closure, rebuild, binding and image checks. The other three accepted subjects need no regeneration.

Evidence: `reports/archimedes-terminal-taper.json`, `archimedes-lower-end/detail.png`, `archimedes-upper-end/detail.png` (each pins the original subject).

## Seven-stage outcomes

- archimedes r001: technical PASS, visual FAIL, factual PASS, specification FAIL, runtime_parse PASS, gpu UNKNOWN, scene UNKNOWN.
- penniretepora r001: technical PASS, visual PASS, factual PASS, specification PASS, runtime_parse PASS, gpu UNKNOWN, scene UNKNOWN.
- constellaria r002: technical PASS, visual PASS, factual PASS, specification PASS, runtime_parse PASS, gpu UNKNOWN, scene UNKNOWN.
- cystodictya r003: technical PASS, visual PASS, factual PASS, specification PASS, runtime_parse PASS, gpu UNKNOWN, scene UNKNOWN.

## Independent verification

- Rehashed all 322 declared payload files plus manifest, all 23 original freeze entries and all 23 dependency-closure files against the fixed commit. Final source readback is unchanged and Git status clean.
- Personally inspected all cited original texts, five fossil image files, four original concepts, all 32 individual final 512 frames, four lossless sheets and three original macro details. Eight cells in each sheet exactly match the original frame pixels.
- Decoded unmodified original GLBs: all component edges closed/oppositely directed and volumes outward. Source indexed topology independently agrees. No weld, normal recalculation or repaired diagnostic copy used.
- Fresh reopening and full-collection re-export of all four Blend files produced byte-identical original GLBs. Transformed dimensions/contact and real all-scene exposure were checked. No hidden-geometry or camera/material masking.
- Two separate maker rebuild PIDs per asset and their exact retained outputs were independently rehashed; request/result/execution provenance and semantic comparisons all agree. Final render requests use the bound exact triplets after binding.
- Project candidate/profile validation, Khronos validator (zero errors and zero warnings), and actual Three GLTFLoader parsing pass for all exact final GLBs. Legacy zero-turntable diagnostic remains preserved under the original explicit static-profile interpretation.

## Geometry and scientific bounds

- Archimedes: 9,396 triangles, 673,344 bytes. One actual helix and one connected genus300 perforated frond; nominal extent19 × 40.928 ×19 mm in exported axes. Genus-only KGS material, complete coil/extent/sampling disclosed as artistic.
- Penniretepora: 7,472 triangles, 518,820 bytes. Main width0.32 mm, lateral widths about0.18 mm, angles about70°, same-rank spacing0.72 mm, aperture width0.07 mm. Each of the 17 components has two exposed rows on its pore-bearing face; no lateral-to-lateral intersections. 199 of 200 bottom-normal rays are unblocked; the redundant blocked junction aperture does not remove a row.
- Constellaria: 8,568 triangles, 584,516 bytes. Actual projected broad width about12.184 mm (12 mm is a nominal art target), thickness3.5 mm within cited3–5 mm. All 36 local stellate depressions are real and exposed, with centers about0.22 mm below the curved host. Source OUIP24 and primary comparative text support this broad form, not the narrow interwoven comparison taxon.
- Cystodictya: 5,824 triangles, 413,056 bytes. Width about0.88 mm and total relief thickness0.616 mm remain inside actual formosa bounds. Five physical aperture rows on both faces, real0.14 mm cavities and attached roots. 196 of 230 bottom-normal rays are unblocked; overlap clips some repeated junction pores but no required row is lost. r003 has no original fourfold root edge.

## Transparent diagnostic correction

The initial reviewer Constellaria test incorrectly required a macula center to be globally lower than every surrounding vertex, which is invalid on a curved host. The failed report remains untouched. A separate same-coordinate local-envelope measurement resolves it and establishes all 36 genuine depressions. This changes neither source geometry nor acceptance requirements.

All 166 declared retired delivery files, including the actual failed Cystodictya r002 history, remain present with matching hashes. Primary fossil observations remain distinct from bounded whole-colony extrapolation.

## Evidence and pins

The machine-readable `independent-report.json` contains complete per-asset GLB/Blend/generator/config/brief/reference/freeze hashes and seven-stage reasoning. `evidence-manifest.json` pins the compact new evidence. Source package bytes are not duplicated except four fresh small re-exports; source media stay consult-only.
