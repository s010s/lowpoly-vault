# Batch96 independent review

Fixed commit: `37a0a42092c6b7a5f02a3f6e72436dfe92191122`.

## Outcome

Two static reviews pass with limitations: **Lyginopteris r002** and **Medullosa r003**. Two require geometry correction: **Paralycopodites r002** and **Cordaites r003**. None is formally accepted, user-approved, website-tested or released. GPU and composed-scene stages are **not run** for all four.

## Required corrections

### PARA-01: main-axis microphylls buried inside the trunk

59 of the72 trunk microphyll groups (`leaf-392` through`leaf-449`, plus`leaf-453`) are entirely enclosed in `main-axis`. Independent three-direction ray parity placed every vertex inside; independent surface-overlap query found zero leaf/trunk triangle intersections for those59 closed leaves. They therefore contribute no exposed trunk leaf surface, despite having nonempty groups and valid base attachment. This explains the visually bare main stem and fails the already-frozen persistent trunk microphyll requirement. This is not merely a subpixel-size issue.

The actual branch scaffold, slim cones, two opposed rows, two crown leaders and counts remain correct. Repair only placement against the actual tapered polygonal stem surface, with buried bases but exposed blades. Do not increase leaf dimensions, delete counts, weaken the freeze or relabel the failure.

### CORD-01: leaf tips are long points, not the selected rounded taper

All105 source leaves have four longitudinal stations with normalized widths approximately0.13,1,1,0.05. A new exact-GLB detail render shows long triangular spear tips. The last30% parameter span narrows from full width to5%, contradicting the immutable “modest rounded-taper tip” and explicit rejection of over-tapered willow shapes.

This is **not** a claim that all Cordaites species must have rounded leaves: Seward describes acute tips in other forms. It is a failure against this selected reference-based frozen design. Change only the tip outline to a short faceted rounded/blunt terminal form while retaining105 leaves,5 equal bands and the14k ceiling. One added station is estimated to produce13024 total triangles with current topology, but a rebuilt result must prove that.

For either repair, retain all originals and create a new revision. Recheck source reopening, full geometry/contact/exposure, both real queued rebuilds, project/Khronos/Three, exact binding, eight new512px views and a lossless sheet.

## Independently completed

- Fixed branch/commit/clean readback;312 delivery entries match both local bytes and committed Git blobs. Original inventory bytes and selected records match;12 frozen brief/reference/config files are unchanged. All358 raw-preservation entries still hash-match.
- All32 final512px images personally inspected individually, plus4 actual ImageGen concepts and original source/reconstruction pixels. Original final32 PNGs match their lossless sheet crops pixel-for-pixel with label-aware offsets. Pre-render subject bindings precede the completed render processes.
- Fresh project and official Khronos audits:9776/11150/12964/10504 triangles;521128/519504/624248/549428 GLB bytes, all below14k and1MB. Khronos errors/warnings0/0 for every asset.
- Source reopens, editable vertices, closed topology, exact hard component counts and1486 actual geometric base connections pass. Full leaf/gland exposure test finds no wholly buried leaf/gland component in the other three assets.
- Eight new serialized two-thread Blender builds, two different PIDs per asset, reproduce byte-identical GLB and matching semantic digests. Source/config/helper/lockfile closure is pinned. Fresh Three.js parse succeeds; that is not GPU evidence.

## Scientific and chronology boundaries

2020 Paralycopodites text supports branch architecture and distal slender cones; unavailable2020 original figure pixels were **not** seen. Personally viewed Seward186A/B and the1980 synonym linkage support historical anatomy only, never complete branching. The inventory's old Chinese spherical-cone phrase is not adopted as fact.

Lyginopteris2007 primary abstract and Seward405 support leaning/climbing interpretation, lobed divided foliage and glands. Medullosa2015 Figure6A supports one erect reconstruction, not the whole genus; original Alberta anatomy pixels are not complete fossil trees. The2011 Caltech page was unavailable in this fresh read and is not falsely claimed inspected. Cordaites2005 primary institutional abstract supports a sterile upland upper-crowned tree; juvenile scale is an artistic choice.

The source addendum honestly records405/466 inspected before freeze and404/467 later. Concept invocation/return receipts, original freezes, authoring record and executed-build timestamps support the recorded order. Provider internal generation time and exact first-authoring time remain unknown, and concept records remain valid but incomplete. No file modification times were used to invent history.

Original failed budget, r002 tube-frame defects and interrupted five-PNG run are intact. The completed Cordaites eight-frame evidence is a separate new run. CPU renders and Node parsing do not establish GPU/scene, formal, user, website or release acceptance.

Full per-asset verdicts, source links/pins, measurements and process logs are bound in `independent-qa-report.json` and the evidence manifest. No production file was changed.
