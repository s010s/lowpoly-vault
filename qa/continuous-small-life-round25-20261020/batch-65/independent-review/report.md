# Independent QA: continuous-small-life round 25, batch 65

Date: 2026-10-20 UTC  
Scope: exactly the four final pinned candidates in `/workspace/shared/lowpoly-batch65-20261020`, source commit `8cdcfe5c512c146e8a2dbd71e582b828e696e5de`, branch `candidate/small-life-batch65-concept-20261020`.  
This is an independent static candidate review, not formal/user approval, a publication decision, or authorization to upload, merge or release.

## Executive result

- burgessochaeta r002: **ACCEPT BOUNDED** as a static candidate. The full slender animal, two palps and repeated paired parapodial fans are present and match the more recent primary anatomical revision. The axial views are necessarily foreshortened; individual fine bristles are represented by simplified samples.
- stalagmite-group r001: **REVISE** before recommending this candidate. It is clearly five solid, rounded, floor-rooted stalagmites, but the visual design is dominated by unusually regular, thick, stacked-looking horizontal terraces. That misses the frozen brief's “subtle irregular growth terraces” and makes longitudinal drip relief hard to read. This is a visual finding, not a mesh/parser failure.
- breccia-outcrop r002: **ACCEPT BOUNDED** as a generic teaching asset. Angular clasts are visible across the crown and sides, embedded in coherent matrix, with no obvious floaters. Many read as shallow plate-like protrusions, so it is a stylized outcrop rather than a geological reconstruction.
- rotational-landslide r001: **ACCEPT BOUNDED** as an educational cutaway. The high rear scarp, curved slip interface, back-tilted displaced bench and toe are present. This is not a geotechnical model; the authored bench drop is about 0.725 m across its 6.3 m modeled span, near the freeze's illustrative 0.8 m design note.

Across all four exact GLBs, independent project static audit, Khronos validation, Three.js 0.180.0 parse and read-only Blender source reopen passed. Each source part is closed-manifold with nonzero volume. All four are within the batch budget: under 14,000 triangles, 1,000,000 bytes, 6 materials and 30 primitives. GPU and composed-scene stages were not run. The candidate records remain pending and `approved_for_brief:false`.

## Seven QA stages

Stage labels below are this reviewer’s findings, not edits to the producer's approval ledger.

| Stage | burgessochaeta r002 | stalagmite-group r001 | breccia-outcrop r002 | rotational-landslide r001 |
|---|---|---|---|---|
| Technical | PASS | PASS | PASS | PASS |
| Visual | PASS, bounded | REVISE | PASS, bounded | PASS, bounded |
| Factual | PASS, bounded | PASS, bounded | PASS, bounded | PASS, bounded |
| Specification | PASS | PASS on counts/deliverables; visual mismatch noted separately | PASS | PASS, illustrative dimension caveat |
| Runtime parse | PASS | PASS | PASS | PASS |
| GPU | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| Scene | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

These static-stage results do not satisfy the product's full formal-approval gates. The frozen candidate validations still have required stage statuses unknown, blockers open, and approval pending. Concept-evidence integrity is valid for each asset, but evidence completeness is false because no provider-generation timestamp was returned; the original record correctly leaves that time unknown. I have not inferred a timestamp or treated concept provenance as approval.

## Exact artifact and technical checks

| Asset | Revision | GLB SHA-256 | Triangles | Bytes | Materials | Primitives | Blender source triangles / volume sum |
|---|---|---|---:|---:|---:|---:|---|
| burgessochaeta | r002 | `6a505f5960c6c973e42ec644dfc078e977c576dff9ed470bc7fc07a27fa9bec4` | 13,116 | 767,732 | 4 | 8 | 13,116 / 3.4441691563e-7 m³ |
| stalagmite-group | r001 | `3b5e8892435c365a612965648f7f1150fad34899b76dfc84edc99d99e34a8668` | 4,320 | 239,460 | 4 | 12 | 4,320 / 1.6820162162 m³ |
| breccia-outcrop | r002 | `bfe0389608e76cd908e46e1b3cbbab91cb4ce282dcc5aa070a098da85d1169af` | 2,116 | 115,304 | 5 | 8 | 2,116 / 10.4260656301 m³ |
| rotational-landslide | r001 | `4b8c7caad83fc07bbddacdd15fcb7647148c8f382105639fdf0426d6f454d543` | 1,388 | 60,712 | 5 | 6 | 1,388 / 696.5227605894 m³ |

The pins above were re-hashed from the candidate files and matched the handoff. Their saved Blender sources were each reopened read-only under the blocking production Blender lock with two threads. Authored and evaluated vertices match in all four saved sources: 9,168 for Burgessochaeta, 2,172 for the stalagmite group, 1,300 for breccia, and 702 for landslide. Exported POSITION accessor counts are 28,392; 8,500; 3,954; and 1,964 respectively. All source parts report zero boundary and nonmanifold edges and positive enclosed volume.

The official Khronos validator returned 0 errors and 0 warnings for every exact pinned GLB. The independent project static audit passed for each under the batch's 14,000-triangle / 1 MB / 6-material / 30-primitive policy. A fresh independent `THREE.GLTFLoader.parseAsync` from Three.js 0.180.0 parsed each exact file, returned the same triangle count, and found 8, 12, 8 and 6 primitives respectively. The parser runs are not GPU renders; each GPU and scene stage remains explicitly not run.

The producer dependency-closure files were independently re-hashed and matched; all referenced generator/config/brief/helper/dependency pins remain intact. The generator files do not load reference images or network resources; the GLBs have no texture/image payload. Consulted primary reference pixels were inspected from their actual local originals, with only their paths and hashes retained in the independent evidence. They are not copied into this package.

## Per-asset visual and factual review

### burgessochaeta r002 — ACCEPT BOUNDED

Inspected all eight individual final 512×512 views (`hero`, `reversehero`, `front`, `side`, `rear`, `top`, `clay`, `silhouette`) and the lossless contact sheet. The side and top views clearly show a continuous, slender segmented organism with 25 paired stations, equant upper/lower rami and laterally radiating bristle fans. Hero/front views show a differentiated head with exactly two smooth anterior palps. The body remains whole and in volume; I found no dorsal Canadia-like thatch, shell plates, unsupported eyes/jaws or invented long tail. The short tapered posterior is not mistaken for the fossil's dark fecal strand. Front/rear axial frames compress the slender form as expected; the side/top/hero angles carry the anatomy.

The factual check uses Parry, Vinther & Edgecombe's primary 2015 revision, which interprets all trunk segments as biramous and the rami as equant; it supersedes the ROM webpage's older first-segment-uniramous wording. The ROM61042 fossil photograph was inspected for overall slenderness and lateral repeated bristle fans, not used as geometry or redistributed: [Parry et al. (2015), DOI 10.1098/rsbl.2015.0763](https://pmc.ncbi.nlm.nih.gov/articles/PMC4650189/) and [Royal Ontario Museum specimen page](https://burgess-shale.rom.on.ca/fossils/burgessochaeta-setigera/). Twenty-five stations and four chaetae samples per ramus are honestly labeled as representative artistic sampling, not exact specimen counts.

### stalagmite-group r001 — REVISE

Inspected all eight individual final 512×512 views and the lossless sheet. Five unequal, closed solid columns visibly rise from a low irregular floor crust. They are not tubes, stalactites or joined floor-to-ceiling columns; no central holes appear in the top view. NPS speleothem guidance supports solid convex floor-growing stalagmites with rounded tops: [National Park Service, Speleothems](https://home.nps.gov/subjects/caves/speleothems.htm).

The revision need is visible in hero, front, rear, top, clay and silhouette views: each column has a sequence of thick, nearly level, strongly repeated concentric bands. The bands read as stacked rings and dominate the form rather than as subtle irregular terraces; the promised longitudinal drip relief is not legible. Keep the five solid floor-grown silhouettes and broad roots, but soften and vary the terrace spacing/height, reduce the repeated ring profile, and introduce visible vertical drip relief before asking for a targeted differential review. This visual outcome does not imply any topology, file or factual error.

### breccia-outcrop r002 — ACCEPT BOUNDED

Inspected all eight individual final 512×512 views and the lossless sheet. The irregular host is a coherent volumetric matrix with sharp angular contrasting clasts distributed across crown, front, sides and rear. The clasts look embedded and protruding; I saw no clearly detached floaters. The fragments are deliberately shallow, and several read as plate-like slabs, so keep the teaching-asset claim bounded rather than implying natural clast dimensions or a specific outcrop. The factual distinction is supported by NPS classification material contrasting angular breccia clasts with rounded conglomerate clasts, plus the consulted USGS flow-breccia photo: [NPS geologic resource material](https://www.nps.gov/articles/cabr_gri_test.htm) and [USGS flow-breccia reference](https://www.usgs.gov/media/images/photos-flow-breccia-central-plateau-member-rhyolites-yellowstone-national-park). The candidate disclaims a named locality, origin, age and assay.

The r002 design was frozen before its repair generator and geometry were authored. The delivered clast field is visible on all exposed faces and follows the explicit angular-host obligation; the retained r001 history was not edited or overwritten.

### rotational-landslide r001 — ACCEPT BOUNDED

Inspected all eight individual final 512×512 views and the lossless sheet. Hero and side show a high rear plateau/main scarp, a coherent grass-topped displaced block with a modest uphill back-tilt, a curved concave-up cutaway slip interface and a lower forward toe. The high rear wall occludes some interior detail in the rear view; the hero/side/top views carry the landform reading. The slip interface is an intentional exposed educational cutaway, not exposed vegetation or a physical engineering surface. The geometric directionality is consistent with British Geological Survey descriptions of rotational slides (curved/listric slip surface, main scarp and back-tilted block): [BGS, How to classify a landslide](https://www.bgs.ac.uk/discovering-geology/earth-hazards/landslides/how-to-classify-a-landslide/).

The freeze/config describes an illustrative 0.8 m forward-to-rear bench-height difference. The generator's bench formula yields about 0.725 m over its 6.3 m block-top run, a modest difference; the direction is correct and the feature is visible. This is a generic diagrammatic 12×16×about-7 m patch, not a hazard-prediction model, surveyed site or Holbeck Hall replica.

## Render, source and queue provenance

All 32 actual final delivery PNGs were inspected individually at 512×512, in addition to each lossless contact sheet (2048×1060, including labels). I re-hashed each output against its render manifest, recomputed decoded RGBA pixel hashes, checked the corresponding proof-final pixels, and compared them with the delivery pixel-equivalence ledger. All matched. This was not an old-image relabel: every final delivery render command ran after its exact new `references.delivery-v001.json` rights-note ledger was created, named that ledger and the exact pinned GLB, completed with return code 0, and created the pinned new proof-delivery manifest. Times are in the independent audit JSON.

There are two actual queued Blender generator executions per selected candidate, each with separate job IDs (`semantic-rebuild-1` and `semantic-rebuild-2`), attempt directory, request fingerprint, Blender PID, start/end times, stdout, output files, and a successful result. Both runs for each candidate emitted the exact final pinned GLB SHA-256. For stalagmite and landslide, a later resume summary labels already completed attempts “reused”; the evidence relied upon here is their distinct successful executions in the original run, whose saved stdout includes Blender writing the source file. The exact PIDs, request timestamps, fingerprints, paths and output hashes are recorded in `provenance/independent_audit.json`.

The genuine original ImageGen concept pixels were inspected and their image and prompt hashes match the frozen evidence. The tool output did not supply a provider-generation timestamp; request/result observation times are recorded as observations only. Consulted fossil, geological photo and diagram pixel assets remain outside this report package.

## Evidence map and limits

- `provenance/independent_audit.json`: independently rechecked source/GLB/reference/render hashes, actual image pixel digests, source reopen results, dependency closure, candidate approval state, exact queued job provenance and new render chronology.
- `technical/project-<asset>.json`: independent project static audit and position counts.
- `technical/khronos-<asset>.json`: independent Khronos validator output.
- `technical/three-<asset>.json`: independent Three.js 0.180.0 parse report.
- `source/reopen-<asset>.json` and `.log`: fresh read-only Blender source reopen/topology/volume results.
- `provenance/independent_audit.py`: local read-only verification script used to create the independent audit JSON.

No candidate, approval field, source, validator, site, CI configuration, or repository file was edited. The producer checkout remained on the specified source commit and clean at the final check. No GPU renderer or full composed scene was run; no graphics-device or scene-performance statement is made. Static recommendation only: Burgessochaeta, Breccia and rotational landslide are bounded candidates; Stalagmite group should be visually revised. Formal review, user approval and publication authority remain separate.
