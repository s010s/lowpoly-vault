# Batch 07 — independent QA

**Reviewer:** GPT-6 Luna xhigh  
**Review source commit:** `dc58b12e0aa3dce39fbef23754dafa3408276235`  
**Review branch:** `qa/s010s/small-life-batch07-20261018`  
**Scope:** exact frozen candidates `syringopora`, `vauxia`, `halimeda`, and `isoxys`. This report records an independent art, source/export, format, and runtime review; it does not edit candidate assets or candidate acceptance records.

## Decision

**Model, visual, and exact-GLB checks: PASS for all four. No model repair is required.** The silhouettes and structural connections remain readable in all eight frozen source views and the exact-GLB runtime views, including a neutral 9-copy scene at about 89 px per asset and independently rendered 210 px single-asset views. All four sit within the accepted natural, refined stylized direction. I found no missing faces, broken silhouettes, or materially bad joints at the intended views.

**Formal candidate-record gate: BLOCKED for all four by one shared metadata error.** The unchanged repository validator reports `references.<source-id>.license: nonempty text required` on each frozen record. Each reference is marked consulted-only and each bundle says no source media, mesh, or texture was incorporated. The reference schema still requires an explicit value such as `reference-only; no source media incorporated`; recording that fact would satisfy the existing schema without claiming a reuse license or changing a threshold. The fix belongs in candidate metadata, then the exact validator should be rerun. I left the candidate commits untouched.

The batch handoff notes a zero-turntable contract difference. Each frozen brief requires the eight named still views and sets `turntable_frames` to `0`; this review inspected all eight plus the exact-GLB runtime views and a 9-copy scene. The repository visual guide describes 24–36 turntable frames as a starting study profile, not a universal hard gate. I did not change or relax a failure threshold.

## Per-asset results

| Asset | QA result | Required issue | Nonblocking observation |
|---|---|---|---|
| **Syringopora** | **PASS** — the upright open tubes and intermittent cross-connections form a clear pipe-coral colony; top, side, reverse, and clay views show no accidental opening or broken connection. The palette-only finish is consistent with the brief. | Shared missing explicit `license`/`reference-only` value in `references.json`. | The cited Digital Atlas page supports tabulate-coral group morphology and includes chain-coral comparisons, but does not establish a genus-specific Syringopora reconstruction. Keep the existing “inspired” / non-strict label. The open tube mouths account for the Blender reimport boundary-edge warning; they are intentional and visible. |
| **Vauxia** | **PASS** — variable-width dichotomous branches, visible open tips, and a bush-like outline read as a branching sponge prop. Front, rear, side, and top views show continuous branch roots; no broken joints or missing surfaces. | Shared missing explicit `license`/`reference-only` value in `references.json`. | The fibrous wall cue is restrained at the 210 px view, so the branch form carries most of the identity. The open tips and irregular taper are clear enough for this stylized scope; adding finer fiber detail is optional and not a return condition. |
| **Halimeda** | **PASS** — the branching chains of flattened, faceted segments and narrow nodes read as a green segmented alga. Side and top views confirm that the plates are not just spheres; the crowded center remains coherent at 210 px and in the 9-copy scene. | Shared missing explicit `license`/`reference-only` value in `references.json`. | GLB is 33,188 bytes, below the brief’s usual size range, which the brief explicitly allows. No size padding or extra detail is warranted. A little more negative space in the dense central cluster could help a future variant, but is not needed here. |
| **Isoxys** | **PASS** — paired convex valves, opposing spines, paired eyes, and simplified underside appendages remain legible from hero, front, side, top, reverse, and runtime views. No face loss or visibly broken appendage connection. The full bounding length is about 97 mm because the spines extend beyond the brief’s nominal 50 mm valve-body axis. | Shared missing explicit `license`/`reference-only` value in `references.json`. | Static audit warns that the lowest glTF Y is −14.35 mm. The brief does not define a ground-contact origin, and the neutral runtime scene has no floor, so this is not a demonstrated mesh defect. If a host scene places Y=0 on the seabed, supply a placement offset or state the intended origin. |

## Exact identities and independent measurements

All candidate branch commits, handoff hashes, candidate-record hashes, and runtime-report GLB hashes match. Every committed file listed by each bundle’s `checksums.sha256` passed `sha256sum -c`.

| Asset | Candidate commit | Editable Blend SHA-256 | Exact GLB SHA-256 | GLB bytes / triangles | GLB bounds (m, X × Y × Z) |
|---|---|---|---|---:|---|
| Syringopora | `d0894b30b0fbeedb4d946d0d976a4e98abeb5aff` | `134e342519950ae080ff614adbf2255885dff3bbb3d67ae99e44e888c140f83c` | `63024697f0b688183d6a4de8f681c4cb17e8d002ba6efaff33cb74db9ce68036` | 155,628 / 8,020 | 0.13261 × 0.18000 × 0.11550 |
| Vauxia | `fd443ffd5eb8342a11956a574ab11bf73bd5a0ea` | `3214aedd961a88169dc07be0d44444ee4fd8d60790f0899e5c6b39f786dc2498` | `1b55a5dbc587b8574c40d9086fb759c8b1ce6da9d86a8b10c03e4f6fa096dfe5` | 172,096 / 8,944 | 0.23612 × 0.18000 × 0.17656 |
| Halimeda | `5ea23624b9e56ccfc4b6700ef9b54774bc5acd6c` | `893b2f6b30ef74045ef14c048f93ddc8e883a62ca78516338a1722e0cc50745a` | `5e1b7e2940482c1ad27b156b7457354d1c04fe98a46a36fc3ae904a5a16517ea` | 33,188 / 1,520 | 0.13676 × 0.15000 × 0.10665 |
| Isoxys | `c017f7acec8027555cadf5a754fa982478bab9f8` | `d5017d668c3df38e77559babcac20392d0fa600df6d11361327d513af88753b2` | `cd846786dcaf001d7c1c50631a28924e2ed4278c490d67034ba37b6774e48923` | 124,252 / 6,012 | 0.02760 × 0.02589 × 0.09702 |

For each asset, the read-only Blender source audit found no nonfinite coordinates or normals, zero-area polygons, boundary edges, or nonmanifold edges in the source `EXPORT` meshes. Source triangle totals equal exact-GLB scene triangle totals. Axis-converted source bounds match GLB bounds at **0.00000 m maximum error**; fresh Blender GLB imports also preserve triangle totals and bounds. The source Blend files contain no cameras or lights. The exact GLBs pass the independent static `qa_glb.py` audit; Isoxys retains the ground-origin warning above. Each bundle’s `qa.json.khronos_validator` entry records the matching GLB SHA, and the Khronos reports show zero errors and warnings. Blender’s reimport wireframes show open corallite/sponge tips and shell/component seams, not missing surfaces.

The candidate runtime evidence and this review’s added medium renders both use exact GLB hashes. This review independently ran Three.js **r180** through Chromium **154.0.8037.57** on ANGLE SwiftShader software WebGL: 512 × 512 viewport, one GLB per screenshot at about **210 px** maximum projected extent, three-to-seven render calls, and **zero WebGL errors**. The existing 9-copy runtime view fits each maximum extent at about **89 px**. These results verify rendering and scene readability; they are not physical-device performance measurements.

## Factual scope

- **Syringopora:** The [Digital Atlas of Ancient Life tabulate-coral collection](https://www.digitalatlasofancientlife.org/vc/cnidaria/anthozoa/tabulata/) provides group-level tabulate-coral morphology and examples of chain corals. It does not provide a Syringopora-specific specimen in this collection. The bundle limits its label to inspired teaching art, so no genus-level reconstruction claim is accepted here.
- **Vauxia:** The [Royal Ontario Museum Burgess Shale entry](https://burgess-shale.rom.on.ca/fossils/vauxia-gracilenta/) describes branching forms, open central cavities and openings, plus a fibrous, reticulated skeleton. The candidate uses the broad branch/open-tip form and does not claim strict skeletal fidelity.
- **Halimeda:** The cited Hillis paper could not be fetched from ScienceDirect during review (HTTP 403). The [Smithsonian NEMESIS entry](https://invasions.si.edu/nemesis/species_summary/6925) independently describes Halimeda as branching, jointed, and made of calcified segments with varied shapes. The candidate is genus-inspired and does not identify a modern species or assert fossil-age specifics.
- **Isoxys:** The [Royal Ontario Museum Burgess Shale entry](https://burgess-shale.rom.on.ca/fossils/isoxys-acutangulus/) describes the two-valve carapace, front and rear spines, bulbous lateral eyes, and appendages. Those broad features are present; no exact specimen, swimming-mechanism, or strict species reconstruction is claimed.

## Contact sheets and machine evidence

- [All frozen source views, 4 × 8](source-views-contact.png)
- [All bundled exact-GLB runtime views, 4 × 7](runtime-views-contact.png)
- [Independently reimported GLB hero and wireframe views](glb-roundtrip-contact.png)
- [Independent 210 px Three.js runtime renders](runtime-medium-contact.png)
- Exact commit/hash reconciliation: [handoff-hash-audit.json](checks/handoff-hash-audit.json)
- Compact technical results: [independent-summary.json](independent-summary.json)
- Independent per-asset measurements, validators, logs, and rendered frames: [`checks/`](checks/)
- Reproduction commands: [COMMANDS.md](COMMANDS.md)

The task’s original QA07 container produced no result and was not used as evidence. No candidate, model, brief, threshold, CI, permission, or release file was changed by this review.
