# Ernietta r012 independent differential static QA

## Disposition: PASS_STATIC_ONLY

The required basal zigzag joining seam, unreadable in r004, is now clearly readable in the unchanged required front direction at 512 × 512. The side no longer exhibits r009's projecting basal shelf. The incomplete, compressed, open/truncated ribbed basal-sack scope is retained. This passes this independent static review only; it is not formal acceptance, user approval, website acceptance, release, or publication authorization.

Exact reviewed subject:

- Branch: `candidate/batch77-ernietta-repair-20261020`.
- Commit: `d1a3aa6a277908cd3aee66aa38e4d6dca818879b`.
- Candidate: `production/batch77-ernietta-repair/assets/ernietta/r012`.
- GLB SHA-256: `72b30dfed8b7786a357e63102bd36ff26007cfb45af28923c6393b7314018e6b`.
- Editable source SHA-256: `41851d81db91af4808dad70bd26bc21dedf88fe4378df69f038ca4c91d8225e3`.
- Delivery brief SHA-256: `75f0845911f1a92479081f7911f1714090df64779545623ddaa6cb5ecf80844b`.
- References SHA-256: `1d9e1f03ee1c23190ff5c533f5494ec1250331a3c1162444dc23467b278f6f3b`.
- Maker handoff SHA-256: `370ecc2aa196ae9a7f8be3e7a9d0d8d1ddf71731c3b81af3e1466cae8f093a07`.

The tip is an evidence-closure child of `aa2694546b2fd70be07b577ccbe5f2d8bd958643`; that commit is directly based on `43e40fc89f2b369a5f1858e72fa58a0d10318124`. The tip itself is not a direct main43 child. The worktree was clean before and after review.

## Seven separate stages

| Stage | Independent result | Scope |
|---|---|---|
| Technical | Pass | Fresh source reopen/re-export, geometry measurements, provenance, project and Khronos checks |
| Visual | Pass | All eight final individual images, lossless sheet, original images and differential fresh front/side renders inspected |
| Factual | Pass, bounded stylization | Incomplete basal fossil-form retained; exact forward flexure is an interpretation, not a measured specimen claim |
| Specification | Pass for static candidate | Original criteria, view directions, budgets, frozen records and editable/deterministic closure preserved |
| Runtime parse | Pass | Fresh Three.js 0.180.0 Node GLTFLoader parse only |
| GPU | Not run / unknown | No hardware or target browser render |
| Scene | Not run / unknown | No intended composed-scene or website review |

The project candidate record remains valid but pending, with `approved_for_brief: false`. This QA does not rewrite that record or self-grant an approval. The intentionally retained legacy diagnostic rejects the zero-turntable setting; the applicable frozen `static-stylized-v1` contract validates successfully. No legacy result was suppressed.

## Actual source and pixel review

I personally viewed the original Smith 2017 Figure 3 image, including panels e/f/g and their caption, the genuine original concept, every original r004 final single view, the rejected r009 side comparison, all eight r012 final single views, and the r012 contact sheet. I read the local primary Smith text and independently opened the primary [Ivantsov article](https://onlinelibrary.wiley.com/doi/10.1111/let.12164).

The Smith photographs distinguish a lengthwise suture and curved rib terminations from an ornamental circumferential band. Its text describes irregular sac-like sandstone casts, parallel/subparallel ribs and partial sediment fill. [Smith 2017 primary paper](https://assets.science.nasa.gov/content/dam/science/psd/astrobiology/for-researchers/early-career-field-research-fund/Report_LC_Smith_Emily_Article_2.pdf).

Ivantsov describes classic upright examples as incomplete and distally truncated. The basal long horizontal axis parallels the zigzag suture where the tubular wall fields meet; pliability and variable preservation limit precise biometric interpretation. These statements support the retained scope and join orientation, not the exact amount or direction of the new bend. [Ivantsov primary article](https://onlinelibrary.wiley.com/doi/10.1111/let.12164).

My inference is that the local forward-flexed base is acceptable within this expressly genus-level, original fossil-form study. It remains low in the sack, joins opposed basal fields, and adds neither missing trunk/fans nor new appendages or ecology. It must not be described as a demonstrated exact deformation of a named fossil. No new universal ratio, tube-count or zero-regularity requirement was imposed.

The original concept is more vase-like and includes a conspicuous belt-like zigzag. Its frozen corrections explicitly reject the round-vase appearance. The final join is an integral long-axis groove, not a literal copy of that conceptual belt. Consult-only primary pixels remain outside the repository and were not incorporated into the asset or this QA package.

Per-view observations:

- Front: the joining groove forms a clearly visible internal dark zigzag immediately above the lower basal edge, not merely a serrated silhouette. This resolves the specific original failure.
- Side: the lower profile narrows continuously into an asymmetric compressed base. The r009 projecting step/ledge is absent; there is no detached foot.
- Hero and reversehero: ribbed walls, broken/open rim, central cavity and modest infill are retained. The seam is largely occluded and is not claimed readable here.
- Rear: upright ribs and basal convergence remain coherent. No claim that the join is readable from behind.
- Top: the elliptical open cavity, thick ribbed wall and recessed floor remain clear; there is no added fan/trunk.
- Clay: confirms the retained wall/cavity and lower geometry without the sandstone palette. The seam is mostly occluded at this elevated hero angle; this is not seam-visibility evidence.
- Silhouette: keeps the compact truncated sack outline, with local basal serration but no r009 shelf or added appendage. A silhouette alone cannot prove the internal join.

The final front and side were independently rendered again with the exact unchanged renderer and exact GLB/brief/reference triplet. I personally inspected both fresh frames. Their decoded RGBA pixels are identical to the maker's corresponding final frames. PNG hashes differ because fresh render metadata differs; they are separately retained, not rebound old images.

## Fresh source geometry and source/export closure

A fresh Blender 4.3.2 process reopened original r004 and candidate r012 without scripts or saving either source. The independent script extracts the source mesh, compares coordinates/connectivity/material nodes, checks topology/intersections, measures bounds and re-exports using the declared export options. The QA-generated GLB is byte-identical to the candidate.

Measured results:

- Authored/evaluated vertices: 2,610 / 2,610. Exported POSITION-stream vertices: 15,289. Triangles: 5,216. Materials/primitives: 3 / 3. Textures: 0. GLB: 401,724 bytes. All frozen budgets pass.
- Blender XYZ extent: 84.820755 × 53.129867 × 54.134030 mm. GLB XYZ extent: 84.820755 × 54.134032 × 53.129867 mm. Axis-converted source/export maximum bound error is about 1.63e-9 m.
- Exactly 718 existing vertices change, all in indices 0–719, the bottom four rings. The 1,800 vertices at indices 720–2519 and the cavity-floor center are exactly unchanged in authored coordinates. First 4,680 wall triangles have unchanged connectivity.
- Old bottom fan center is replaced by 89 joining-chain vertices, producing net +88 vertices and +176 triangles. The chain spans 60 mm along X, stays within the basal region, and has a measured central recess up to 1.45 mm.
- Maximum local displacement in the first ring is 15.2585 mm, so this is not merely a tiny relief edit. It is a localized basal-flexure construction; no claim that its displacement is specimen-measured is warranted.
- Material values and shader-node inputs are identical. Object/root rotation and scale are unchanged. The normal grounding translation changes from −1.0 mm to −2.3 mm as the physical minimum changes. Thus upper coordinates are unchanged before grounding, not at identical world Z.
- One connected closed mesh; zero boundary/nonmanifold triangle edges; zero nonadjacent BVH intersection pairs; positive signed volume; positive triangle areas. BVH excludes shared-vertex adjacency and is not an exhaustive no-intersection proof at every tolerance. The actual final pixels show no visible overlap artifact.

The render script, helper, angles, sample count, color transform and exposure are byte-identical or equal to the original settings. The enclosing-radius-derived camera scale/target and light sizes/energies change slightly automatically with the new grounded bounds. These values are recorded in `integrity-check.json`; it would be inaccurate to say every numeric camera/light value is identical. No renderer edit, angle trick, manual scaling or material workaround caused the seam.

## Integrity, chronology and historical rebuilds

- Rehashed all 129 committed source-evidence entries, totaling 10,910,857 bytes, and compared every entry to the pinned Git blob, not only the working files.
- Verified all 16 original byte-identity copies, original r004 source/GLB/generator, eight original premodel-freeze entries, and both original independent QA files. Original brief criteria/scope/views/budgets remain unchanged; the derived delivery brief adds only required-deliverable closure and a packaging adapter.
- Rehashed all 187 retained failed-revision/raw files, totaling 21,725,373 bytes. r005–r011 remain retained. r009's historical technical success does not override its later visual rejection.
- Verified two distinct historical executed semantic jobs, PIDs 69 and 94, different job IDs/fingerprints/output directories, full request/result/input/output hashes, successful result records and stdout build lines. Each output GLB is byte-identical to the candidate. This is corroborated execution provenance, not cryptographic proof of historical execution. I did not redundantly rebuild the whole asset batch.
- Rebuilds finished at 22:32:13.470670 and 22:32:33.286861 UTC. Exact preproof triplet binding was recorded at 22:32:33.810722 UTC, schema verification at 22:32:33.820119 UTC, then final render invocation began at 22:32:33.820928 UTC and completed at 22:33:03.960217 UTC. Actual frame hashes/dimensions and eight saved-frame log entries match. No filesystem mtime was used to manufacture chronology.
- Fresh Khronos 2.0.0-dev.3.10 validation reports zero errors and zero warnings. Fresh Three.js 0.180.0 Node parsing succeeds with matching triangle/material/bound measurements.
- Original concept-provider generation time and original modeling-start time remain unknown. They were not reconstructed from filesystem timestamps or promoted to known facts.

## Evidence, safeguards and limits

Independent outputs are under `/workspace/shared/lowpoly-ernietta-r012-independent-qa-20261020/`: `integrity-check.json`, `reopen-diff.report.json`, `source-mesh-diff-raw.json`, `reexport.glb`, `project-fresh.json`, `khronos-fresh.json`, `three-fresh.json`, the independent two-frame render and comparison, inspection receipts, before/after input snapshots, and raw execution logs.

A first QA-report serialization attempt failed because PNG EXIF bytes needed a JSON-safe representation. Its log is retained. The assertions had completed; the reporter was repaired and rerun successfully. This did not alter any source or producer evidence. Blender's optional Draco-library warning is retained; Draco export is disabled and the standalone uncompressed GLB passes validation.

Every Blender process used blocking `flock /tmp/lowpoly-production-blender.lock` and `--threads 2`, releasing the lock per process. Only the existing read-only dependency directory was used. No installation, website build, source edit, push, PR, merge, credential, permission, security or environment change occurred. CPU stills and Node parsing are not GPU or scene evidence. Publication remains separate.
